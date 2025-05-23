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

SENSOR_TITLES = {
    "5_per_day": "Daily Tehillim – 5 Chapters",
    "monthly":    "Daily Tehillim – Yom LaChodesh",
    "weekly":     "Daily Tehillim – Weekly Cycle",
}


class DailyTehillimSensor(SensorEntity):
    """Reports the daily Tehillim portion for one schedule."""

    _attr_icon = "mdi:book-open-page-variant"
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, schedule: str, entry_id: str) -> None:
        self.hass = hass
        self._schedule = schedule
        self._attr_name = SENSOR_TITLES[schedule]
        # Use entry_id to guarantee uniqueness across restarts
        self._attr_unique_id = f"{entry_id}_{schedule}"
        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        """Run an immediate update, then every 24 hours."""
        await self.async_update()
        async_track_time_interval(self.hass, self.async_update, SCAN_INTERVAL)

    async def async_update(self, now=None) -> None:
        """Fetch today’s portion and update the sensor state."""
        try:
            val = get_tehillim_portion(self._schedule)
            _LOGGER.debug("%s → %s", self._schedule, val)
            self._attr_native_value = val
        except Exception:
            _LOGGER.exception("Error updating Tehillim sensor [%s]", self._schedule)
            self._attr_native_value = None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up three sensors—one per schedule—under a single config entry."""
    schedules = ["5_per_day", "monthly", "weekly"]
    sensors = [
        DailyTehillimSensor(hass, s, entry.entry_id)
        for s in schedules
    ]
    async_add_entities(sensors)
