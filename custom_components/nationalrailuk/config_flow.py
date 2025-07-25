"""Config flow for National Rail UK integration."""
from __future__ import annotations

import json
import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import (
    BASE_URL,
    CONF_API_KEY,
    CONF_FILTER_CRS,
    CONF_FILTER_TYPE,
    CONF_NUM_ROWS,
    CONF_STATION_CODE,
    CONF_TIME_OFFSET,
    CONF_TIME_WINDOW,
    DEFAULT_FILTER_TYPE,
    DEFAULT_NUM_ROWS,
    DEFAULT_TIME_OFFSET,
    DEFAULT_TIME_WINDOW,
    DOMAIN,
    FILTER_TYPES,
    USER_AGENT,
)

_LOGGER = logging.getLogger(__name__)


class NationalRailUKConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for National Rail UK."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Validate API key by making a test request
                await self._test_api_key(user_input[CONF_API_KEY])
                
                # Create unique ID based on station code and filter
                unique_id = f"{user_input[CONF_STATION_CODE]}_{user_input.get(CONF_FILTER_CRS, '')}"
                
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )
            except Exception as ex:  # pylint: disable=broad-except
                _LOGGER.error("Error during setup: %s", ex)
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME): str,
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_STATION_CODE): str,
                    vol.Optional(CONF_FILTER_CRS): str,
                    vol.Optional(CONF_FILTER_TYPE, default=DEFAULT_FILTER_TYPE): vol.In(
                        FILTER_TYPES
                    ),
                    vol.Optional(CONF_NUM_ROWS, default=DEFAULT_NUM_ROWS): vol.All(
                        vol.Coerce(int), vol.Range(min=1, max=50)
                    ),
                    vol.Optional(CONF_TIME_WINDOW, default=DEFAULT_TIME_WINDOW): vol.All(
                        vol.Coerce(int), vol.Range(min=1, max=300)
                    ),
                    vol.Optional(CONF_TIME_OFFSET, default=DEFAULT_TIME_OFFSET): vol.All(
                        vol.Coerce(int), vol.Range(min=-60, max=60)
                    ),
                }
            ),
            errors=errors,
        )

    async def _test_api_key(self, api_key: str) -> None:
        """Test the API key by making a request to the API."""
        url = f"{BASE_URL}/WAT"  # Use Waterloo as test station
        
        headers = {
            "x-apikey": api_key,
            "User-Agent": USER_AGENT,
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status != 200:
                    raise Exception(f"API test failed with status {response.status}")
                
                data = await response.json()
                if "error" in data:
                    raise Exception(f"API error: {data['error']}") 