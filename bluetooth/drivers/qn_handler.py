import time

from bluetooth.core.device_handler import ScaleDeviceHandler
from bluetooth.core.measurement import ScaleMeasurement


class QNHandler(ScaleDeviceHandler):

    SCALE_UNIX_TIMESTAMP_OFFSET = 946702800

    NOTIFY_CHAR = "0000fff1-0000-1000-8000-00805f9b34fb"
    WRITE_CHAR = "0000fff2-0000-1000-8000-00805f9b34fb"

    def __init__(self):

        super().__init__()

        self.weight_scale = 100.0
        self.protocol_type = 0
        self.protocol_received = False
        self.session_published = False

    def checksum(self, buf):

        return sum(buf) & 0xFF

    def u16be(self, a, b):

        return (a << 8) | b

    async def on_connected(self, user):

        self.user = user

        self.weight_scale = 100
        self.protocol_received = False
        self.session_published = False

        self.log("Connected to QN scale")

    async def notification(self, sender, data):

        opcode = data[0]

        if self.protocol_type == 0 and len(data) > 2:
            self.protocol_type = data[2]

        handlers = {

            0x10: self.handle_live_weight,
            0x12: self.handle_scale_info,
            0x14: self.handle_time_request,
            0x21: self.handle_handshake,
            0x23: self.handle_history

        }

        handler = handlers.get(opcode)

        if handler:
            await handler(data)

    async def handle_scale_info(self, data):

        if len(data) <= 10:
            return

        self.weight_scale = 100 if data[10] == 1 else 10

        self.log("Weight scale factor:", self.weight_scale)

        if not self.protocol_received:

            self.protocol_received = True
            await self.send_configuration()

    async def handle_live_weight(self, data):

        if self.session_published:
            return

        raw = self.u16be(data[3], data[4])
        stable = data[5]

        r1 = self.u16be(data[6], data[7])
        r2 = self.u16be(data[8], data[9])

        if stable != 1:
            return

        # FIXED scaling
        weight = raw / (self.weight_scale * 10)

        # print first
        self.log("Weight:", weight, "Resistance:", r1, r2)

        measurement = ScaleMeasurement(
            user_id=self.user.id,
            weight=weight,
            resistance1=r1,
            resistance2=r2
        )

        # publish after logs
        self.publish(measurement)

        self.session_published = True

    async def handle_time_request(self, data):

        epoch = int(time.time()) - self.SCALE_UNIX_TIMESTAMP_OFFSET

        msg = bytearray([

            0x20,
            0x08,
            self.protocol_type,
            epoch & 0xFF,
            (epoch >> 8) & 0xFF,
            (epoch >> 16) & 0xFF,
            (epoch >> 24) & 0xFF,
            0

        ])

        msg[-1] = self.checksum(msg[:-1])

        await self.write(self.WRITE_CHAR, msg)

    async def handle_handshake(self, data):

        msg = bytearray([

            0xa0,
            0x0d,
            0x04,
            0xfe,
            0,0,0,0,0,0,0,0,
            0

        ])

        msg[-1] = self.checksum(msg[:-1])

        await self.write(self.WRITE_CHAR, msg)

        self.log("Handshake sent")

    async def handle_history(self, data):

        self.log("Historical record received")

    async def send_configuration(self):

        unit = 1 if self.user.unit == "kg" else 2

        cfg = bytearray([

            0x13,
            0x09,
            self.protocol_type,
            unit,
            0x10,
            0,0,0,0

        ])

        cfg[-1] = self.checksum(cfg)

        await self.write(self.WRITE_CHAR, cfg)

        self.log("Configuration sent")
