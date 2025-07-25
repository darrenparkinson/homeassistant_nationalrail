"""Sensor platform for National Rail UK integration."""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any

import aiohttp
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util import dt as dt_util

from .const import (
    BASE_URL,
    CONF_API_KEY,
    CONF_FILTER_CRS,
    CONF_FILTER_TYPE,
    CONF_NUM_ROWS,
    CONF_STATION_CODE,
    CONF_TIME_OFFSET,
    CONF_TIME_WINDOW,
    DOMAIN,
    USER_AGENT,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=5)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the National Rail UK sensor."""
    config = config_entry.data
    
    async_add_entities(
        [
            NationalRailUKSensor(
                config_entry,
                config[CONF_STATION_CODE],
                config[CONF_API_KEY],
                config.get(CONF_FILTER_CRS),
                config.get(CONF_FILTER_TYPE, "to"),
                config.get(CONF_NUM_ROWS, 10),
                config.get(CONF_TIME_WINDOW, 120),
                config.get(CONF_TIME_OFFSET, 0),
            )
        ],
        True,
    )


class NationalRailUKSensor(SensorEntity):
    """Representation of a National Rail UK sensor."""

    def __init__(
        self,
        config_entry: ConfigEntry,
        station_code: str,
        api_key: str,
        filter_crs: str | None,
        filter_type: str,
        num_rows: int,
        time_window: int,
        time_offset: int,
    ) -> None:
        """Initialize the sensor."""
        self._config_entry = config_entry
        self._station_code = station_code.upper()
        self._api_key = api_key
        self._filter_crs = filter_crs.upper() if filter_crs else None
        self._filter_type = filter_type
        self._num_rows = num_rows
        self._time_window = time_window
        self._time_offset = time_offset
        
        # Create unique ID
        if self._filter_crs:
            self._attr_unique_id = f"{self._station_code}_{self._filter_crs}"
            self._attr_name = f"Train Schedule {self._station_code} to {self._filter_crs}"
        else:
            self._attr_unique_id = f"{self._station_code}_all"
            self._attr_name = f"Train Schedule {self._station_code}"
        
        self._attr_available = False
        self._attr_native_value = None
        self._attr_extra_state_attributes = {}

    async def async_update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            data = await self._fetch_departure_board()
            if data:
                self._attr_native_value = f"{len(data.get('trainServices', []))} trains"
                self._attr_extra_state_attributes = {
                    "station_name": data.get("locationName"),
                    "crs": data.get("crs"),
                    "generated_at": data.get("generatedAt"),
                    "trains": data.get("trainServices", []),
                    "bus_services": data.get("busServices", []),
                    "ferry_services": data.get("ferryServices", []),
                    "nrcc_messages": data.get("nrccMessages", []),
                    "platform_available": data.get("platformAvailable"),
                    "are_services_available": data.get("areServicesAvailable"),
                }
                self._attr_available = True
            else:
                self._attr_available = False
                _LOGGER.warning("No data received from National Rail API")
                
        except Exception as ex:  # pylint: disable=broad-except
            _LOGGER.error("Error updating National Rail sensor: %s", ex)
            self._attr_available = False

    async def _fetch_departure_board(self) -> dict[str, Any] | None:
        """Fetch departure board data from the API."""
        url = f"{BASE_URL}/{self._station_code}"
        
        params = {
            "numRows": self._num_rows,
            "timeWindow": self._time_window,
            "timeOffset": self._time_offset,
        }
        
        if self._filter_crs:
            params["filterCrs"] = self._filter_crs
            params["filterType"] = self._filter_type
        
        headers = {
            "x-apikey": self._api_key,
            "User-Agent": USER_AGENT,
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    _LOGGER.error(
                        "API request failed with status %s: %s",
                        response.status,
                        await response.text(),
                    )
                    return None

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:train"

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": self._attr_name,
            "manufacturer": "National Rail",
            "model": "Live Departure Board",
        } 