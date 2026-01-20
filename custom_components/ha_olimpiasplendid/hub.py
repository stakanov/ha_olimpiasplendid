import asyncio
from collections import defaultdict
from pymodbus.client import AsyncModbusSerialClient


class OlimpiaModbusHub:
    def __init__(self, entry):
        self.entry = entry
        self.client = AsyncModbusSerialClient(
            port=entry.data["port"],
            baudrate=entry.data["baudrate"],
            parity=entry.data["parity"],
            stopbits=entry.data["stopbits"],
        )
        self._cache = {}
        self._listeners = defaultdict(list)
        self._task = None

    async def connect(self):
        await self.client.connect()
        self._task = asyncio.create_task(self._poll_loop())

    async def close(self):
        if self._task:
            self._task.cancel()
        await self.client.close()

    async def _poll_loop(self):
        while True:
            for (slave, address), callbacks in self._listeners.items():
                rr = await self.client.read_holding_registers(
                    address=address,
                    count=1,
                    slave=slave,
                )
                value = rr.registers[0]
                self._cache[(slave, address)] = value
                for cb in callbacks:
                    cb(value)
            await asyncio.sleep(5)

    def register(self, slave, address, callback):
        self._listeners[(slave, address)].append(callback)

    def get(self, slave, address):
        return self._cache.get((slave, address))

    async def write_bits(self, slave, address, start, length, value):
        current = self._cache.get((slave, address), 0)
        mask = ((1 << length) - 1) << start
        new_val = (current & ~mask) | ((value << start) & mask)
        await self.client.write_register(address, new_val, slave=slave)
