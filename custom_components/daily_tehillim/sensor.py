# custom_components/daily_tehillim/sensor.py

import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .schedules import get_tehillim_portion

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(hours=24)


class DailyTehillimSensor(SensorEntity):
    """Sensor that reports the daily Tehillim portion."""

    _attr_icon = "mdi:book-open-page-variant"
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, schedule_type: str, entry_id: str) -> None:
        self.hass = hass
        self._schedule_type = schedule_type
        self._attr_name = "Daily Tehillim"
        self._attr_unique_id = entry_id
        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        """Run immediately and then schedule daily updates."""
        await self.async_update()
        async_track_time_interval(self.hass, self.async_update, SCAN_INTERVAL)

    async def async_update(self, now=None) -> None:
        """Fetch today’s portion and update state."""
        try:
            portion = get_tehillim_portion(self._schedule_type)
            _LOGGER.debug("Daily Tehillim portion → %s", portion)
            self._attr_native_value = portion
        except Exception:
            _LOGGER.exception("Failed to calculate Tehillim portion")


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor from the UI config entry."""
    schedule = entry.data.get("schedule_type", "5_per_day")
    async_add_entities([DailyTehillimSensor(hass, schedule, entry.entry_id)])
