from homeassistant import config_entries
import voluptuous as vol
from .const import (
    DOMAIN,
    CONF_ENTRY_TYPE,
    ENTRY_TYPE_HUB,
    ENTRY_TYPE_DEVICE,
)


class OlimpiaSplendidConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        return await self.async_step_hub(user_input)

    async def async_step_hub(self, user_input=None):
        if user_input:
            user_input[CONF_ENTRY_TYPE] = ENTRY_TYPE_HUB
            return self.async_create_entry(
                title=f"Modbus {user_input['port']}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="hub",
            data_schema=vol.Schema(
                {
                    vol.Required("port"): str,
                    vol.Required("baudrate", default=9600): int,
                    vol.Required("parity", default="N"): vol.In(["N", "E", "O"]),
                    vol.Required("stopbits", default=1): vol.In([1, 2]),
                }
            ),
        )

    async def async_step_device(self, user_input=None):
        hubs = {
            entry.entry_id: entry.title
            for entry in self._async_current_entries()
            if entry.data.get(CONF_ENTRY_TYPE) == ENTRY_TYPE_HUB
        }

        if user_input:
            user_input[CONF_ENTRY_TYPE] = ENTRY_TYPE_DEVICE
            return self.async_create_entry(
                title=user_input["name"],
                data=user_input,
            )

        return self.async_show_form(
            step_id="device",
            data_schema=vol.Schema(
                {
                    vol.Required("name"): str,
                    vol.Required("device_type"): vol.In(["pdc", "fancoil"]),
                    vol.Required("slave"): vol.All(int, vol.Range(min=1, max=247)),
                    vol.Required("hub_id"): vol.In(hubs),
                }
            ),
        )
