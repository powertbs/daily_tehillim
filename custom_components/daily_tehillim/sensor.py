# custom_components/daily_tehillim/sensor.py

import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .schedules import get_tehillim_portion

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(hours=24)

SCHEDULES = {
    "5_per_day": "Daily Tehillim – 5 Chapters",
    "monthly": "Daily Tehillim – Yom LaChodesh",
    "weekly": "Daily Tehillim – Weekly Cycle"
}

class DailyTehillimSensor(SensorEntity):
    _attr_icon = "mdi:book-open-page-variant"
    _attr_should_poll = False
    _attr_entity_registry_enabled_default = True

    def __init__(self, schedule_type: str) -> None:
        self._schedule_type = schedule_type
        self._attr_name = SCHEDULES[schedule_type]
        self._attr_unique_id = f"daily_tehillim_{schedule_type}"
        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        await self.async_update()
        async_track_time_interval(self.hass, self.async_update, SCAN_INTERVAL)

    async def async_update(self, now=None) -> None:
        try:
            portion = get_tehillim_portion(self._schedule_type)
            _LOGGER.debug("%s → %s", self._schedule_type, portion)
            self._attr_native_value = portion
        except Exception as e:
            _LOGGER.error("Error updating Tehillim sensor [%s]: %s", self._schedule_type, e)
            self._attr_native_value = None

async def async_setup_entry(
    hass: HomeAssistant,
    entry,
    async_add_entities: AddEntitiesCallback
) -> None:
    sensors = [
        DailyTehillimSensor("5_per_day"),
        DailyTehillimSensor("monthly"),
        DailyTehillimSensor("weekly")
    ]
    async_add_entities(sensors)