class ScaleDeviceHandler:

    def __init__(self):

        self.client = None
        self.user = None
        self.CompWeight = None
        self.CompResistance1 = None
        self.CompResistance2 = None
        self.finished = False

    def attach_client(self, client):

        self.client = client

    async def write(self, characteristic, data):

        await self.client.write_gatt_char(characteristic, data)

    def publish(self, measurement):

        print("\n===== SCALE MEASUREMENT =====")
        print(f"user id: {measurement.user_id}")
        self.CompWeight = measurement.weight
        print(f"Weight: {measurement.weight}")
        self.CompResistance1 = measurement.resistance1
        print(f"impendence r1 5Mhz {measurement.resistance1}")
        self.CompResistance2 = measurement.resistance2
        print(f"impendence r2 50Mhz {measurement.resistance2}")
        print("=============================\n")

        # stop the BLE loop
        self.finished = True

    def log(self, *msg):

        print("[SCALE]", *msg)
