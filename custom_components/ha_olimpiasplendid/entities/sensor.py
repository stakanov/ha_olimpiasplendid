from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import EntityCategory

from ..const import DOMAIN
from ..registers import REGISTER_MAP


class OlimpiaBitSensor(SensorEntity):
    """Sensore basato su uno o più bit di un registro Modbus."""

    def __init__(self, hub, device, register, field_name, field):
        self._hub = hub
        self._device = device
        self._register = register
        self._field = field
        self._field_name = field_name

        self._attr_name = f"{device.name} {field_name}"
        self._attr_entity_category = EntityCategory.DIAGNOSTIC

        # Registrazione al polling centralizzato
        hub.register(
            device.slave,
            register["address"],
            self._update_from_register,
        )

    def _update_from_register(self, value: int):
        """Callback chiamata dal hub quando il registro cambia."""
        start = self._field["start"]
        length = self._field["len"]

        mask = (1 << length) - 1
        raw = (value >> start) & mask

        if "enum" in self._field:
            self._attr_native_value = self._field["enum"].get(raw)
        else:
            self._attr_native_value = raw

        self.async_write_ha_state()

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._device.device_id)},
            "name": self._device.name,
            "manufacturer": "Olimpia Splendid",
            "model": self._device.model,
            "via_device": (DOMAIN, self._device.hub_id),
        }
