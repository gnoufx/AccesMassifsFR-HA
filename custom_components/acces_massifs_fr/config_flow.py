"""Config flow for Accès Massifs Forestiers France."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlow,
)
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    BooleanSelector,
    SelectOptionDict,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
)

from .const import (
    CONF_DEPARTMENTS,
    CONF_DOWNLOAD_HISTORY,
    CONF_SCAN_HOUR,
    CONF_SCAN_MINUTE,
    DEFAULT_DEPARTMENTS,
    DEFAULT_DOWNLOAD_HISTORY,
    DEFAULT_SCAN_HOUR,
    DEFAULT_SCAN_MINUTE,
    DEPARTMENTS,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

# Default departments pre-selected (the original 13 for users migrating)
DEFAULT_DEPARTMENTS = ["13"]


def _departments_selector() -> SelectSelector:
    """Return a multi-select selector for departments."""
    return SelectSelector(
        SelectSelectorConfig(
            options=[
                SelectOptionDict(value=dept_id, label=f"{dept_id} — {name}")
                for dept_id, name in sorted(DEPARTMENTS.items())
            ],
            multiple=True,
            mode=SelectSelectorMode.LIST,
        )
    )


class AccesMassifsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Accès Massifs Forestiers France."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialise the config flow."""
        self._user_config: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step (department selection & schedule)."""
        # Only one instance allowed
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        errors: dict[str, str] = {}

        if user_input is not None:
            if not user_input.get(CONF_DEPARTMENTS):
                errors[CONF_DEPARTMENTS] = "no_departments"
            else:
                self._user_config = dict(user_input)
                return await self.async_step_download_history()

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_DEPARTMENTS, default=DEFAULT_DEPARTMENTS
                ): _departments_selector(),
                vol.Required(
                    CONF_SCAN_HOUR, default=DEFAULT_SCAN_HOUR
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=23)),
                vol.Required(
                    CONF_SCAN_MINUTE, default=DEFAULT_SCAN_MINUTE
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=59)),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )

    async def async_step_download_history(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the step asking whether to download current year history."""
        if user_input is not None:
            self._user_config.update(user_input)
            return self.async_create_entry(
                title="Accès Massifs Forestiers France",
                data=self._user_config,
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_DOWNLOAD_HISTORY, default=DEFAULT_DOWNLOAD_HISTORY
                ): BooleanSelector(),
            }
        )

        return self.async_show_form(
            step_id="download_history", data_schema=schema
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> AccesMassifsOptionsFlow:
        """Return the options flow handler."""
        return AccesMassifsOptionsFlow(config_entry)


class AccesMassifsOptionsFlow(OptionsFlow):
    """Handle options for Accès Massifs Forestiers France."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialise the options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        errors: dict[str, str] = {}

        if user_input is not None:
            if not user_input.get(CONF_DEPARTMENTS):
                errors[CONF_DEPARTMENTS] = "no_departments"
            else:
                return self.async_create_entry(title="", data=user_input)

        current = self._config_entry.options or self._config_entry.data
        current_depts = current.get(CONF_DEPARTMENTS, DEFAULT_DEPARTMENTS)

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_DEPARTMENTS, default=current_depts
                ): _departments_selector(),
                vol.Required(
                    CONF_SCAN_HOUR,
                    default=current.get(CONF_SCAN_HOUR, DEFAULT_SCAN_HOUR),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=23)),
                vol.Required(
                    CONF_SCAN_MINUTE,
                    default=current.get(CONF_SCAN_MINUTE, DEFAULT_SCAN_MINUTE),
                ): vol.All(vol.Coerce(int), vol.Range(min=0, max=59)),
                vol.Optional(
                    CONF_DOWNLOAD_HISTORY,
                    default=False,
                ): BooleanSelector(),
            }
        )

        return self.async_show_form(
            step_id="init", data_schema=schema, errors=errors
        )

