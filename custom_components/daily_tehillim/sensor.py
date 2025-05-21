import logging
from datetime import date
from homeassistant.helpers.entity import Entity
from homeassistant.const import STATE_ON
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.typing import HomeAssistantType

from .const import DOMAIN
from .schedules import get_tehillim_portion, HDate

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    schedule_type = entry.data.get("schedule_type", "5_per_day")
    async_add_entities([DailyTehillimSensor(hass, schedule_type)], True)

class DailyTehillimSensor(Entity):
    def __init__(self, hass: HomeAssistantType, schedule_type: str):
        self._hass = hass
        self._attr_name = "Daily Tehillim"
        self._attr_icon = "mdi:book-open-page-variant"
        self._attr_unique_id = f"daily_tehillim_{schedule_type}"
        self._schedule_type = schedule_type
        self._attr_extra_state_attributes = {}
        self._state = None

    async def async_update(self):
        today = date.today()
        portion = get_tehillim_portion(self._schedule_type, today)
        hdate = HDate(today)

        self._state = portion
        self._attr_extra_state_attributes = {
            "schedule_type": self._schedule_type,
            "hebrew_day": hdate.hebrew_day(),
            "hebrew_month": hdate.hebrew_month_name(),
            "date": str(today),
        }

    @property
    def state(self):
        return self._state

