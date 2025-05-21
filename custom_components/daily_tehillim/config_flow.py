import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from .const import DOMAIN

SCHEDULE_OPTIONS = {
    "5_per_day": "5 Chapters Per Day",
    "monthly": "Yom LaChodesh",
    "weekly": "Yom Tehillim (Weekly)"
}

class DailyTehillimConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Daily Tehillim."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Daily Tehillim", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("schedule_type", default="5_per_day"): vol.In(SCHEDULE_OPTIONS)
            }),
            description_placeholders={
                "schedule_type": "Choose your preferred Tehillim cycle."
            }
        )
