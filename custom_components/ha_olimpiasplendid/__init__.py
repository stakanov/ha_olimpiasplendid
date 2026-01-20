from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from .const import (
    DOMAIN,
    CONF_ENTRY_TYPE,
    ENTRY_TYPE_HUB,
    ENTRY_TYPE_DEVICE,
)
from .hub import OlimpiaModbusHub
from .devices import OlimpiaDevice

PLATFORMS = ["sensor", "select", "number"]


async def async_setup(hass: HomeAssistant, config: dict):
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})

    if entry.data[CONF_ENTRY_TYPE] == ENTRY_TYPE_HUB:
        hub = OlimpiaModbusHub(entry)
        await hub.connect()
        hass.data[DOMAIN][entry.entry_id] = hub
        return True

    if entry.data[CONF_ENTRY_TYPE] == ENTRY_TYPE_DEVICE:
        hub = hass.data[DOMAIN][entry.data["hub_id"]]
        device = OlimpiaDevice(
            device_id=entry.entry_id,
            name=entry.data["name"],
            device_type=entry.data["device_type"],
            slave=entry.data["slave"],
            hub_id=entry.data["hub_id"],
        )
        hass.data[DOMAIN][entry.entry_id] = device
        await hass.config_entries.async_forward_entry_setups(
            entry, PLATFORMS
        )
        return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    if entry.data[CONF_ENTRY_TYPE] == ENTRY_TYPE_HUB:
        hub = hass.data[DOMAIN].pop(entry.entry_id)
        await hub.close()
        return True

    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
