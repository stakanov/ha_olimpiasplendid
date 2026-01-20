from .registers import DEVICES
from .hub import OlimpiaSplendidHub
from .bitfield import write_bits, write_bit, read_bits

for device in DEVICES:
    hub = OlimpiaSplendidHub(client, device["slave"])
    for reg in device["registers"]:
        for name, cfg in reg["entities"].items():
            if cfg["platform"] == "select":
                create_select_entity(hub, reg["address"], cfg)
            elif cfg["platform"] == "switch":
                create_switch_entity(hub, reg["address"], cfg)
