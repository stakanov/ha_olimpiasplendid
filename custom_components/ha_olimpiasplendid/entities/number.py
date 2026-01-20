from homeassistant.components.number import NumberEntity
from ..const import DOMAIN


class OlimpiaBitNumber(NumberEntity):
    def __init__(self, hub, device, register, field):
        self._hub = hub
        self._device = device
        self._register = register
        self._field = field
        self._attr_name = f"{device.name} {field}"

        hub.register(
            device.slave,
            register["address"],
            self._update,
        )

    def _update(self, value):
        self._attr_value = (value >> self._field["start"]) & (
            (1 << self._field["len"]) - 1
        )
        self.async_write_ha_state()

    async def async_set_native_value(self, value):
        await self._hub.write_bits(
            self._device.slave,
            self._register["address"],
            self._field["start"],
            self._field["len"],
            int(value),
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
