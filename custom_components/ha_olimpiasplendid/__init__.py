"""Olimpia Splendid modbus integration for Home Assistant."""

from homeassistant.core import HomeAssistant

DOMAIN = "ha_olimpiasplendid"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the integration via configuration.yaml (optional)."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    """Set up the integration via UI."""
    hass.data[DOMAIN] = {}
    return True
