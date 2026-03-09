import asyncio

from utils.config_loader import ConfigLoader
from bluetooth.core.user import ScaleUser
from bluetooth.drivers.qn_handler import QNHandler
from bluetooth.ble.client import BLEScaleClient
from metrics.body_composition import BodyCompositionCalculator

class Sync:
    async def sync(self):
        self.UWeight = None
        self.UResistance1 = None
        self.UResistance2 = None

        self.config = ConfigLoader().load()
        self.user_cfg = self.config["scale"]["user"]
        self.user = ScaleUser(

            id=self.user_cfg["id"],
            age=self.user_cfg["age"],
            height=self.user_cfg["height"],
            gender=self.user_cfg["gender"],
            unit=self.config["scale"]["unit"]
        )
        self.address = self.config["scale"]["address"]
        self.handler = QNHandler()
        self.client = BLEScaleClient(self.address, self.handler)

        await self.client.run(self.user)
        if self.handler.finished == True:
            self.UWeight = self.handler.CompWeight
            self.UResistance1 = self.handler.CompResistance1
            self.UResistance2 = self.handler.CompResistance2

class SynCalc:
    async def calc(self):
        self.unpacked = Sync()
        await self.unpacked.sync()

        self.calculate_metrix = BodyCompositionCalculator(self.unpacked.user_cfg["height"], self.unpacked.UWeight, self.unpacked.user_cfg["gender"])
        self.calculated_metrix_dict = self.calculate_metrix.calculate(self.unpacked.UWeight, self.unpacked.UResistance2)

if __name__ == "__main__":
    syncal = SynCalc()
    asyncio.run(syncal.calc())
    print(syncal.calculated_metrix_dict)
