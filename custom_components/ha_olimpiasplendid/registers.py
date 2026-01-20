DEVICES = [
    {
        "name": "Pompa di Calore",
        "slave": 1,
        "registers": [
            {
                "name": "commands",
                "address": 101,
                "type": "holding",
                "entities": {
                    "mode": {"platform": "select", "bits": (13, 2), "options": {1:"heat",2:"cool"}},
                    "fan_speed": {"platform":"select", "bits":(0,3), "options": {0:"auto",1:"min",2:"night",3:"max"}}
                }
            }
        ]
    },
    {
        "name": "Fancoil",
        "slave": 2,
        "registers": [
            {
                "name": "commands",
                "address": 101,
                "type": "holding",
                "entities": {
                    "fan_speed": {"platform":"select", "bits":(0,3), "options": {0:"auto",1:"min",2:"night",3:"max"}},
                    "standby": {"platform":"switch", "bit":7}
                }
            }
        ]
    }
]
