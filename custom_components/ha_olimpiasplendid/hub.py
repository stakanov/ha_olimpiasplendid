from pymodbus.client.async_serial import AsyncModbusSerialClient
from pymodbus.client.async_tcp import AsyncModbusTcpClient

class OlimpiaSplendidHub:
    def __init__(self, method="rtu", port="/dev/ttyUSB0", baudrate=9600, host=None, tcp_port=None):
        self.method = method
        if method == "rtu":
            self.client = AsyncModbusSerialClient(
                method="rtu",
                port=port,
                baudrate=baudrate,
                stopbits=1,
                bytesize=8,
                parity='N',
                timeout=1
            )
        elif method == "tcp":
            self.client = AsyncModbusTcpClient(host, port=tcp_port)
        else:
            raise ValueError("Unsupported method")

    async def read_register(self, address, slave):
        rr = await self.client.read_holding_registers(address, 1, unit=slave)
        return rr.registers[0] if rr.isError() == False else None

    async def write_register(self, address, value, slave):
        await self.client.write_register(address, value, unit=slave)
