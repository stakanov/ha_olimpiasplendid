class OlimpiaSplendidHub:
    def __init__(self, client, slave):
        self.client = client
        self.slave = slave

    async def read_register(self, address):
        return await self.client.read_holding_registers(address, 1, unit=self.slave)

    async def write_register(self, address, value):
        await self.client.write_register(address, value, unit=self.slave)
