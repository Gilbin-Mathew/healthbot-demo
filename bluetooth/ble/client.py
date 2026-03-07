import asyncio
from bleak import BleakClient, BleakScanner


class BLEScaleClient:

    def __init__(self, address, handler):

        self.address = address
        self.handler = handler

    async def discover_device(self):

        devices = await BleakScanner.discover()

        for d in devices:
            if d.address == self.address:
                return d

        return None

    async def run(self, user):

        device = await self.discover_device()

        if not device:
            raise RuntimeError("Scale not found. Turn the scale on and try again.")

        async with BleakClient(device.address) as client:

            self.handler.attach_client(client)

            await self.handler.on_connected(user)

            await client.start_notify(
                self.handler.NOTIFY_CHAR,
                self.handler.notification
            )

            print("Listening for scale data...")

            while not self.handler.finished:
                await asyncio.sleep(1)
