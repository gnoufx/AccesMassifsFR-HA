"""Data update coordinator for Accès Massifs Forestiers France."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

import aiohttp


from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_change
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    DATA_URL_TEMPLATE,
    DEPARTMENTS,
    DOMAIN,
    LEVEL_COLORS,
    LEVEL_LABELS,
    MASSIFS,
    MASSIFS_BY_DEPT,
    SEASON_END_DAY,
    SEASON_END_MONTH,
    SEASON_START_DAY,
    SEASON_START_MONTH,
)
from .storage import AccesMassifsStorage

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL_IN_SEASON = timedelta(hours=1)
UPDATE_INTERVAL_OFF_SEASON = timedelta(hours=6)


class AccesMassifsCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch massif access data for all selected departments and keep it up-to-date."""

    def __init__(
        self,
        hass: HomeAssistant,
        storage: AccesMassifsStorage,
        scan_hour: int,
        scan_minute: int,
        departments: list[str],
    ) -> None:
        """Initialise the coordinator.

        Args:
            hass: The Home Assistant instance.
            storage: Persistent storage helper.
            scan_hour: Hour for the daily scheduled scan.
            scan_minute: Minute for the daily scheduled scan.
            departments: List of department codes to monitor (e.g. ["13", "83"]).
        """
        self.storage = storage
        self.scan_hour = scan_hour
        self.scan_minute = scan_minute
        # Normalize department codes (e.g. '4' -> '04')
        self.departments = [
            f"{int(d):02d}" if str(d).isdigit() and len(str(d)) == 1 else str(d)
            for d in departments
        ]

        # Pre-compute the massif IDs to monitor (from selected departments)
        self.monitored_massif_ids: list[str] = []
        for dept in self.departments:
            self.monitored_massif_ids.extend(MASSIFS_BY_DEPT.get(dept, []))

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=self._compute_interval(),
        )

        # Track the daily scan time
        self._unsub_track_time = async_track_time_change(
            hass,
            self._handle_daily_scan_time,
            hour=self.scan_hour,
            minute=self.scan_minute,
            second=0,
        )

    # ── Helpers ────────────────────────────────────────────────────────────

    async def _handle_daily_scan_time(self, _datetime_now: datetime) -> None:
        """Triggered at the daily scan time to fetch fresh data."""
        _LOGGER.info(
            "Scheduled daily scan time reached (%02d:%02d) - triggering data refresh",
            self.scan_hour,
            self.scan_minute,
        )
        await self.async_request_refresh()

    async def async_unload(self) -> None:
        """Unload the coordinator and cancel any scheduled tasks."""
        if self._unsub_track_time:
            self._unsub_track_time()
            self._unsub_track_time = None

    @staticmethod
    def _is_in_season(now: datetime | None = None) -> bool:
        """Return *True* when the current date falls within the active season."""
        if now is None:
            now = datetime.now()
        season_start = now.replace(
            month=SEASON_START_MONTH, day=SEASON_START_DAY,
            hour=0, minute=0, second=0, microsecond=0,
        )
        season_end = now.replace(
            month=SEASON_END_MONTH, day=SEASON_END_DAY,
            hour=23, minute=59, second=59, microsecond=999999,
        )
        return season_start <= now <= season_end

    def _compute_interval(self) -> timedelta:
        """Choose a polling interval depending on the season."""
        return (
            UPDATE_INTERVAL_IN_SEASON
            if self._is_in_season()
            else UPDATE_INTERVAL_OFF_SEASON
        )

    async def _fetch_json_for_dept(
        self, dept: str, date_str: str
    ) -> dict[str, Any] | None:
        """Fetch a single day's JSON file for a specific department.

        Returns *None* when the server responds with 404 or any other non-200 status.
        """
        session = async_get_clientsession(self.hass)
        url = DATA_URL_TEMPLATE.format(dept=dept, date=date_str)

        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status == 404:
                    _LOGGER.debug(
                        "Data not (yet) available for dept=%s date=%s (HTTP 404)",
                        dept, date_str
                    )
                    return None
                if resp.status != 200:
                    _LOGGER.warning(
                        "Unexpected HTTP %s when fetching %s", resp.status, url
                    )
                    return None
                return await resp.json(content_type=None)
        except aiohttp.ClientError as err:
            _LOGGER.warning("Network error fetching %s: %s", url, err)
            return None
        except ValueError as err:
            _LOGGER.warning("JSON decode error for %s: %s", url, err)
            return None

    @staticmethod
    def _parse_massif_data(
        raw: dict[str, Any] | None, massif_id: str, dept: str | None = None
    ) -> tuple[int, int]:
        """Extract *(level, procedure)* for a massif from a raw JSON payload.

        Handles various ID representations across departmental data feeds.
        Returns ``(0, 0)`` when data is missing.
        """
        if raw is None:
            return (0, 0)
        massifs_raw = raw.get("massifs", {})
        if not isinstance(massifs_raw, dict):
            return (0, 0)

        # Build candidate keys to look up in the department's JSON payload
        candidates: list[str] = [massif_id]
        if massif_id.isdigit():
            candidates.append(str(int(massif_id)))

        if dept:
            dept_str = str(dept)
            p1 = dept_str
            p2 = str(int(dept_str)) if dept_str.isdigit() else dept_str
            if massif_id.startswith(p1):
                sub = massif_id[len(p1):]
                candidates.extend([sub, str(int(sub)) if sub.isdigit() else sub])
            if massif_id.startswith(p2):
                sub = massif_id[len(p2):]
                candidates.extend([sub, str(int(sub)) if sub.isdigit() else sub])
            if dept_str == "20":
                for cp in ("20", "21", "2A", "2B"):
                    if massif_id.startswith(cp):
                        sub = massif_id[len(cp):]
                        candidates.extend([sub, str(int(sub)) if sub.isdigit() else sub])

        entry = None
        for cand in candidates:
            if cand in massifs_raw:
                entry = massifs_raw[cand]
                break

        if entry is None or not isinstance(entry, list) or len(entry) < 2:
            return (0, 0)
        try:
            return (int(entry[0]), int(entry[1]))
        except (TypeError, ValueError):
            return (0, 0)

    # ── Core update logic ──────────────────────────────────────────────────

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch fresh data from all selected department APIs."""
        now = datetime.now()
        in_season = self._is_in_season(now)

        # Adjust polling cadence dynamically
        self.update_interval = self._compute_interval()

        today_str = now.strftime("%Y%m%d")
        tomorrow_str = (now + timedelta(days=1)).strftime("%Y%m%d")

        _LOGGER.debug(
            "Fetching data for %d department(s), today=%s, tomorrow=%s",
            len(self.departments), today_str, tomorrow_str
        )

        # Fetch JSON for each selected department (today + tomorrow)
        raw_today: dict[str, dict[str, Any] | None] = {}
        raw_tomorrow: dict[str, dict[str, Any] | None] = {}

        try:
            for dept in self.departments:
                raw_today[dept] = await self._fetch_json_for_dept(dept, today_str)
                raw_tomorrow[dept] = await self._fetch_json_for_dept(dept, tomorrow_str)
        except Exception as err:
            raise UpdateFailed(f"Error fetching massif data: {err}") from err

        massifs_out: dict[str, Any] = {}
        today_storage: dict[str, Any] = {}

        for m_id in self.monitored_massif_ids:
            m_info = MASSIFS.get(m_id)
            if m_info is None:
                continue

            dept = str(m_info["dept"])
            dept_raw_today = raw_today.get(dept)
            dept_raw_tomorrow = raw_tomorrow.get(dept)

            # Today's level and procedure
            if dept_raw_today is not None:
                today_level, today_proc = self._parse_massif_data(
                    dept_raw_today, m_id, dept
                )
            else:
                today_level, today_proc = (1 if not in_season else 0), 0

            # Tomorrow's level and procedure
            if dept_raw_tomorrow is not None:
                tmrw_level, tmrw_proc = self._parse_massif_data(
                    dept_raw_tomorrow, m_id, dept
                )
            else:
                tmrw_level, tmrw_proc = (1 if not in_season else 0), 0

            massifs_out[m_id] = {
                "name": m_info["name"],
                "dept": dept,
                "dept_name": DEPARTMENTS.get(dept, dept),
                "today_level": today_level,
                "today_color": LEVEL_COLORS.get(today_level, "unknown"),
                "today_label": LEVEL_LABELS.get(today_level, "Non disponible"),
                "today_procedure": today_proc,
                "tomorrow_level": tmrw_level,
                "tomorrow_color": LEVEL_COLORS.get(tmrw_level, "unknown"),
                "tomorrow_label": LEVEL_LABELS.get(tmrw_level, "Non disponible"),
                "tomorrow_procedure": tmrw_proc,
                "latitude": m_info["latitude"],
                "longitude": m_info["longitude"],
            }

            # Prepare data for persistent storage (today only)
            today_storage[m_id] = {
                "level": today_level,
                "procedure": today_proc,
                "dept": dept,
            }

        # Persist today's snapshot if any department had data
        has_any_today = any(v is not None for v in raw_today.values())
        if has_any_today:
            await self.storage.async_save_day(today_str, today_storage)

        history = await self.storage.async_get_all_history()

        return {
            "is_season": in_season,
            "today_date": today_str,
            "tomorrow_date": tomorrow_str,
            "massifs": massifs_out,
            "history": history,
            "departments": self.departments,
        }

    async def async_download_year_history(self, year: int | None = None) -> int:
        """Download season access history for the specified (or current) year.

        Fetches all available daily JSON files for monitored departments from
        the season start (May 31) up to today (or season end Sept 30).
        Saves all parsed records into persistent storage and updates coordinator data.

        Returns:
            Number of successfully fetched and stored days.
        """
        now = datetime.now()
        target_year = year if year is not None else now.year

        season_start = datetime(
            target_year, SEASON_START_MONTH, SEASON_START_DAY
        )
        season_end = datetime(
            target_year, SEASON_END_MONTH, SEASON_END_DAY
        )

        end_date = min(now, season_end)
        if season_start > end_date:
            _LOGGER.info(
                "Season for year %d has not started yet (starts %02d/%02d)",
                target_year, SEASON_START_DAY, SEASON_START_MONTH,
            )
            return 0

        # Generate list of date strings (YYYYMMDD)
        dates: list[str] = []
        curr = season_start
        while curr <= end_date:
            dates.append(curr.strftime("%Y%m%d"))
            curr += timedelta(days=1)

        _LOGGER.info(
            "Downloading history for year %d: %d date(s) across %d department(s)",
            target_year, len(dates), len(self.departments),
        )

        sem = asyncio.Semaphore(10)

        async def _fetch_with_sem(dept: str, d_str: str) -> tuple[str, str, dict[str, Any] | None]:
            async with sem:
                res = await self._fetch_json_for_dept(dept, d_str)
                return dept, d_str, res

        tasks = [
            _fetch_with_sem(dept, d_str)
            for dept in self.departments
            for d_str in dates
        ]

        results = await asyncio.gather(*tasks)

        # Group fetched results by date_str -> {dept: json_data}
        dept_data_by_date: dict[str, dict[str, Any]] = {}
        for dept, d_str, raw in results:
            if raw is not None:
                if d_str not in dept_data_by_date:
                    dept_data_by_date[d_str] = {}
                dept_data_by_date[d_str][dept] = raw

        days_to_save: dict[str, dict[str, Any]] = {}

        for d_str, raw_depts in dept_data_by_date.items():
            day_entry: dict[str, Any] = {}
            for m_id in self.monitored_massif_ids:
                m_info = MASSIFS.get(m_id)
                if m_info is None:
                    continue
                dept = str(m_info["dept"])
                raw_dept = raw_depts.get(dept)
                if raw_dept is not None:
                    level, proc = self._parse_massif_data(raw_dept, m_id, dept)
                else:
                    level, proc = 0, 0

                day_entry[m_id] = {
                    "level": level,
                    "procedure": proc,
                    "dept": dept,
                }
            if day_entry:
                days_to_save[d_str] = day_entry

        if days_to_save:
            await self.storage.async_save_days(days_to_save)
            if self.data is not None:
                self.data["history"] = await self.storage.async_get_all_history()
                self.async_update_listeners()
            _LOGGER.info(
                "Successfully saved %d day(s) of historical data for %d",
                len(days_to_save), target_year,
            )

        return len(days_to_save)

