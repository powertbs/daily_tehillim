import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .schedules import get_today_portion

_LOGGER = logging.getLogger(__name__)


class DailyTehillimSensor(SensorEntity):
    def __init__(self, hass: HomeAssistant, schedule_type: str) -> None:
        self._schedule_type = schedule_type
        self._attr_name = "Daily Tehillim"
        self._attr_icon = "mdi:book-open-page-variant"
        self._attr_unique_id = "daily_tehillim"
        self._attr_should_poll = False
        self._attr_native_value = None
        self._attr_entity_registry_enabled_default = True  # Ensure sensor is enabled by default

    async def async_update(self) -> None:
        try:
            portion = get_today_portion(self._schedule_type)
            _LOGGER.debug("Tehillim portion for '%s': %s", self._schedule_type, portion)
            self._attr_native_value = portion
        except Exception as e:
            _LOGGER.error("Failed to calculate Tehillim portion: %s", e)
            self._attr_native_value = None


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    schedule_type = entry.data.get("schedule_type", "5_per_day")
    async_add_entities([DailyTehillimSensor(hass, schedule_type)])


