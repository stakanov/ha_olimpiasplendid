REGISTER_MAP = {
    "fancoil": {
        "commands": {
            "address": 101,
            "fields": {
                "mode": {"start": 13, "len": 2, "enum": {1: "Heat", 2: "Cool"}},
                "presence": {"start": 12, "len": 1},
                "standby": {"start": 7, "len": 1},
                "fan": {
                    "start": 0,
                    "len": 3,
                    "enum": {
                        0: "Auto",
                        1: "Min",
                        2: "Night",
                        3: "Max",
                    },
                },
            },
        }
    },
    "pdc": {
        "commands": {
            "address": 1,
            "fields": {
                "mode": {"start": 0, "len": 2, "enum": {1: "Auto", 2: "Cool", 3: "Heat"}},
            },
        }
    },
}
