import logging
import os
import json
from datetime import datetime, date
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_change
from homeassistant.const import STATE_ON

from .const import PORTIONS, DOMAIN, STORAGE_FILE, SENSOR_NAME

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    sensor = DailyTehillimSensor(hass)
    async_add_entities([sensor])
    return True

class DailyTehillimSensor(Entity):
    def __init__(self, hass):
        self._hass = hass
        self._state = None
        self._index = 0
        self._last_advanced = None
        self._storage_path = hass.config.path(".storage", STORAGE_FILE)
        self.load_index()
        async_track_time_change(hass, self.update_daily, hour=0, minute=1, second=0)

    @property
    def name(self):
        return SENSOR_NAME

    @property
    def state(self):
        return PORTIONS[self._index]

    @property
    def icon(self):
        return "mdi:book-open-page-variant"

    def load_index(self):
        if os.path.exists(self._storage_path):
            try:
                with open(self._storage_path, "r") as f:
                    data = json.load(f)
                    self._index = data.get("index", 0)
                    self._last_advanced = data.get("last_advanced")
            except Exception as e:
                _LOGGER.error(f"Failed to load index: {e}")

    def save_index(self):
        data = {
            "index": self._index,
            "last_advanced": str(date.today())
        }
        try:
            with open(self._storage_path, "w") as f:
                json.dump(data, f)
        except Exception as e:
            _LOGGER.error(f"Failed to save index: {e}")

    async def update_daily(self, *_):
        today = date.today()

        # Don't advance if already advanced today
        if self._last_advanced == str(today):
            return

        if self._hass.states.get("binary_sensor.issur_melacha_today") == None:
            _LOGGER.warning("binary_sensor.issur_melacha_today not found. Skipping update.")
            return

        if self._hass.states.get("binary_sensor.issur_melacha_today").state == STATE_ON:
            _LOGGER.info("Skipping advancement due to issur melacha.")
            return

        self._index = (self._index + 1) % len(PORTIONS)
        self._last_advanced = str(today)
        self.save_index()
        self.schedule_update_ha_state()
