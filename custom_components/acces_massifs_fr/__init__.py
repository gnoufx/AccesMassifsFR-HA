"""The Accès Massifs Forestiers France integration."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.loader import async_get_integration

from .const import (
    CONF_DEPARTMENTS,
    CONF_DOWNLOAD_HISTORY,
    CONF_SCAN_HOUR,
    CONF_SCAN_MINUTE,
    DEFAULT_SCAN_HOUR,
    DEFAULT_SCAN_MINUTE,
    DOMAIN,
)
from .coordinator import AccesMassifsCoordinator
from .storage import AccesMassifsStorage

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.TIME]

SERVICE_FORCE_UPDATE = "force_update"
SERVICE_DOWNLOAD_HISTORY = "download_history"



async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Accès Massifs Forestiers France from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # ── Storage ────────────────────────────────────────────────────────────
    storage = AccesMassifsStorage(hass)
    await storage.async_load()

    # ── Config values ──────────────────────────────────────────────────────
    scan_hour: int = entry.options.get(
        CONF_SCAN_HOUR, entry.data.get(CONF_SCAN_HOUR, DEFAULT_SCAN_HOUR)
    )
    scan_minute: int = entry.options.get(
        CONF_SCAN_MINUTE, entry.data.get(CONF_SCAN_MINUTE, DEFAULT_SCAN_MINUTE)
    )
    raw_departments = entry.options.get(
        CONF_DEPARTMENTS, entry.data.get(CONF_DEPARTMENTS, DEFAULT_DEPARTMENTS)
    )
    if isinstance(raw_departments, str):
        raw_departments = [raw_departments]
    departments: list[str] = [
        f"{int(d):02d}" if str(d).isdigit() and len(str(d)) == 1 else str(d)
        for d in raw_departments
    ]

    # ── Coordinator ────────────────────────────────────────────────────────
    coordinator = AccesMassifsCoordinator(
        hass,
        storage=storage,
        scan_hour=scan_hour,
        scan_minute=scan_minute,
        departments=departments,
    )

    # First data fetch
    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    # ── Initial history download if requested ──────────────────────────────
    should_download_history = (
        entry.options.get(CONF_DOWNLOAD_HISTORY, False)
        or (
            CONF_DOWNLOAD_HISTORY not in entry.options
            and entry.data.get(CONF_DOWNLOAD_HISTORY, False)
        )
    )
    if should_download_history:
        _LOGGER.info("Initial history download requested – fetching season data")
        hass.async_create_task(coordinator.async_download_year_history())
        # Reset the option flag if it was enabled via options
        if entry.options.get(CONF_DOWNLOAD_HISTORY, False):
            new_options = dict(entry.options)
            new_options[CONF_DOWNLOAD_HISTORY] = False
            hass.config_entries.async_update_entry(entry, options=new_options)

    # ── Forward platforms ──────────────────────────────────────────────────
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # ── Register services ──────────────────────────────────────────────────
    async def handle_force_update(call: ServiceCall) -> None:  # noqa: ARG001
        """Force an immediate data refresh."""
        _LOGGER.info("force_update service called – refreshing data")
        await coordinator.async_request_refresh()

    async def handle_download_history(call: ServiceCall) -> None:
        """Download historical access data for a specific year (default: current)."""
        year = call.data.get("year")
        _LOGGER.info("download_history service called (year=%s)", year)
        for coord in hass.data.get(DOMAIN, {}).values():
            if isinstance(coord, AccesMassifsCoordinator):
                await coord.async_download_year_history(year=year)

    if not hass.services.has_service(DOMAIN, SERVICE_FORCE_UPDATE):
        hass.services.async_register(
            DOMAIN, SERVICE_FORCE_UPDATE, handle_force_update
        )

    if not hass.services.has_service(DOMAIN, SERVICE_DOWNLOAD_HISTORY):
        hass.services.async_register(
            DOMAIN, SERVICE_DOWNLOAD_HISTORY, handle_download_history
        )


    # ── Register www directory for Lovelace card assets ────────────────────
    await _async_register_www(hass)

    # ── Automatically register Lovelace resources for UI Editor support ───
    await _async_register_lovelace_resources(hass)

    # ── Listen for options updates ─────────────────────────────────────────
    entry.async_on_unload(entry.add_update_listener(_async_options_updated))

    return True


async def _async_register_www(hass: HomeAssistant) -> None:
    """Serve the integration's ``www/`` folder as a static path.

    This makes Lovelace card JS files loadable via:
        ``/local/community/acces_massifs_fr/<file>``
    """
    www_path = Path(__file__).parent / "www"
    if www_path.is_dir():
        await hass.http.async_register_static_paths(
            [
                StaticPathConfig(
                    url_path=f"/local/community/{DOMAIN}",
                    path=str(www_path),
                    cache_headers=True,
                )
            ]
        )
        _LOGGER.debug("Registered static path for %s", www_path)
        await _async_register_lovelace_resources(hass)


async def _async_options_updated(
    hass: HomeAssistant, entry: ConfigEntry
) -> None:
    """Reload the integration when options change."""
    _LOGGER.debug("Options updated – reloading integration")
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    )
    if unload_ok:
        coordinator = hass.data[DOMAIN].get(entry.entry_id)
        if coordinator and hasattr(coordinator, "async_unload"):
            await coordinator.async_unload()

        hass.data[DOMAIN].pop(entry.entry_id, None)
        # Clean up domain data dict if empty
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN, None)
            # Remove services when no entries remain
            if hass.services.has_service(DOMAIN, SERVICE_FORCE_UPDATE):
                hass.services.async_remove(DOMAIN, SERVICE_FORCE_UPDATE)
            if hass.services.has_service(DOMAIN, SERVICE_DOWNLOAD_HISTORY):
                hass.services.async_remove(DOMAIN, SERVICE_DOWNLOAD_HISTORY)


    return unload_ok


async def _async_register_lovelace_resources(hass: HomeAssistant) -> None:
    """Register the Lovelace card resources automatically."""
    lovelace_data = hass.data.get("lovelace")
    if not lovelace_data or getattr(lovelace_data, "mode", "storage") != "storage":
        _LOGGER.debug("Lovelace is not in storage mode, skipping automatic resource registration")
        return

    resources = lovelace_data.resources
    if not resources:
        _LOGGER.debug("Lovelace resources repository not found, skipping registration")
        return

    if not resources.loaded:
        await resources.async_load()

    # Load version dynamically from integration manifest
    version = "2.0.3"
    try:

        integration = await async_get_integration(hass, DOMAIN)
        version = integration.version
    except Exception as err:
        _LOGGER.warning("Could not read version from integration manifest: %s", err)

    card_resources = [
        {
            "url": f"/local/community/{DOMAIN}/acces-massifs-forecast-card.js?v={version}",
            "path": f"/local/community/{DOMAIN}/acces-massifs-forecast-card.js",
        },
        {
            "url": f"/local/community/{DOMAIN}/acces-massifs-history-card.js?v={version}",
            "path": f"/local/community/{DOMAIN}/acces-massifs-history-card.js",
        },
    ]

    try:
        existing_items = resources.async_items()

        for r in card_resources:
            found_item = None
            for item in existing_items:
                item_url = item.get("url", "") if hasattr(item, "get") else getattr(item, "url", "")
                if r["path"] in item_url or item_url.startswith(r["path"]):
                    found_item = item
                    break

            if found_item is None:
                _LOGGER.info("Automatically registering Lovelace resource: %s", r["url"])
                await resources.async_create_item({
                    "url": r["url"],
                    "res_type": "module"
                })
            else:
                found_url = found_item.get("url", "") if hasattr(found_item, "get") else getattr(found_item, "url", "")
                if found_url != r["url"]:
                    _LOGGER.info(
                        "Updating Lovelace resource for cache busting: %s -> %s",
                        found_url,
                        r["url"]
                    )
                    found_item_id = found_item.get("id") if hasattr(found_item, "get") else getattr(found_item, "id", None)
                    if found_item_id:
                        await resources.async_update_item(found_item_id, {
                            "url": r["url"],
                            "res_type": "module"
                        })
    except Exception as err:
        _LOGGER.error("Failed to automatically register Lovelace resources: %s", err)
