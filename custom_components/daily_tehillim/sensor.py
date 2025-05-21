from homeassistant.components.sensor import SensorEntity
from .schedules import get_today_portion

class DailyTehillimSensor(SensorEntity):
    def __init__(self, hass, schedule_type):
        self._hass = hass
        self._schedule_type = schedule_type
        self._attr_name = "Daily Tehillim"
        self._attr_icon = "mdi:book-open-page-variant"
        self._attr_unique_id = "daily_tehillim"
        self._attr_native_value = None

    async def async_update(self):
        self._attr_native_value = get_today_portion(self._schedule_type)

async def async_setup_entry(hass, entry, async_add_entities):
    schedule_type = entry.data.get("schedule_type", "5_per_day")
    async_add_entities([DailyTehillimSensor(hass, schedule_type)])
