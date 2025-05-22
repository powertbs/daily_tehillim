# custom_components/daily_tehillim/config_flow.py

from homeassistant import config_entries
from .const import DOMAIN


class DailyTehillimConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow: instantly create entry with no user input."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        return self.async_create_entry(title="Daily Tehillim", data={})
