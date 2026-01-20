from dataclasses import dataclass
from typing import Literal

DeviceType = Literal["pdc", "fancoil"]


@dataclass
class OlimpiaDevice:
    device_id: str
    name: str
    device_type: DeviceType
    slave: int
    hub_id: str
    model: str | None = None
