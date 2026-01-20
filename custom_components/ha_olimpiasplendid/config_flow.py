from homeassistant import config_entries
from .const import DOMAIN

class HAOlimpiaSplendidConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for My Integration."""

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="HA OlimpiaSplendid", data=user_input)
        return self.async_show_form(step_id="user", data_schema={})

