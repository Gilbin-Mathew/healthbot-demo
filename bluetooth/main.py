import asyncio

from utils.config_loader import ConfigLoader
from core.user import ScaleUser
from drivers.qn_handler import QNHandler
from ble.client import BLEScaleClient
from Bodyindex import body_composition


async def main():
    UWeight = None
    UResistance1 = None
    UResistance2 = None

    config = ConfigLoader().load()

    user_cfg = config["scale"]["user"]

    user = ScaleUser(

        id=user_cfg["id"],
        age=user_cfg["age"],
        height=user_cfg["height"],
        gender=user_cfg["gender"],
        unit=config["scale"]["unit"]

    )

    address = config["scale"]["address"]

    handler = QNHandler()

    client = BLEScaleClient(address, handler)

    await client.run(user)
    if handler.finished == True:
        UWeight = handler.CompWeight
        UResistance1 = handler.CompResistance1
        UResistance2 = handler.CompResistance2

    bmical(UWeight, UResistance1, UResistance2)


def bmical(weight, r1, r2):
    print(f"weight: {weight}")
    print(f"r1: {r1}")
    print(f"r2: {r2}")



if __name__ == "__main__":

    asyncio.run(main())
