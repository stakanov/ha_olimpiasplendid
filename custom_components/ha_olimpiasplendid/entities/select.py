from homeassistant.components.select import SelectEntity
from ..const import DOMAIN


class OlimpiaBitSelect(SelectEntity):
    def __init__(self, hub, device, register, field):
        self._hub = hub
        self._device = device
        self._register = register
        self._field = field
        self._options = field["enum"]
        self._attr_name = f"{device.name} {field}"

        hub.register(
            device.slave,
            register["address"],
            self._update,
        )

    def _update(self, value):
        raw = (value >> self._field["start"]) & (
            (1 << self._field["len"]) - 1
        )
        self._attr_current_option = self._options.get(raw)
        self.async_write_ha_state()

    @property
    def options(self):
        return list(self._options.values())

    async def async_select_option(self, option):
        inv = {v: k for k, v in self._options.items()}
        await self._hub.write_bits(
            self._device.slave,
            self._register["address"],
            self._field["start"],
            self._field["len"],
            inv[option],
        )

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device.device_id)},
            "name": self._device.name,
            "manufacturer": "Olimpia Splendid",
            "model": self._device.model,
            "via_device": (DOMAIN, self._device.hub_id),
        }
