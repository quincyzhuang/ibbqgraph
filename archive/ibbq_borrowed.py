"""
worker for inkbird ibbq and other equivalent cooking/BBQ thermometers.
Thermometer sends every ~2sec the current temperature.
"""
import struct
import json

REQUIREMENTS = ["bluepy"]

class ibbqThermometer:
    SettingResult = "fff1"
    AccountAndVerify = "fff2"
    RealTimeData = "fff4"
    SettingData = "fff5"
    Notify = b"\x01\x00"
    realTimeDataEnable = bytearray([0x0B, 0x01, 0x00, 0x00, 0x00, 0x00])
    batteryLevel = bytearray([0x08, 0x24, 0x00, 0x00, 0x00, 0x00])
    KEY = bytearray(
        [
            0x21,
            0x07,
            0x06,
            0x05,
            0x04,
            0x03,
            0x02,
            0x01,
            0xB8,
            0x22,
            0x00,
            0x00,
            0x00,
            0x00,
            0x00,
        ]
    )

    def getBattery(self):
        self.Setting_uuid.write(self.batteryLevel)

    def connect(self, timeout=5):
        from bluepy import btle

        try:
            device = btle.Peripheral(self.mac)
            print("%s connected ", self.mac)
            return device
        except btle.BTLEDisconnectError as er:
            print("failed connect %s", er)

    def __init__(self, mac, timeout=5):
        self.cnt = 0
        self.batteryPct = 0
        self.timeout = timeout
        self.mac = mac
        self.values = list()
        self.device = self.connect()
        self.offline = 0
        if not self.device:
            return
        self.device = self.subscribe()

    @property
    def connected(self):
        return bool(self.device)

    def subscribe(self, timeout=5):
        from bluepy import btle

        class MyDelegate(btle.DefaultDelegate):
            def __init__(self, caller):
                btle.DefaultDelegate.__init__(self)
                self.caller = caller
                print("init mydelegate")

            def handleNotification(self, cHandle, data):
                batMin = 0.95
                batMax = 1.5
                result = list()
                #    safe = data
                if cHandle == 37:
                    if data[0] == 0x24:
                        currentV = struct.unpack("<H", data[1:3])
                        maxV = struct.unpack("<H", data[3:5])
                        self.caller.batteryPct = int(
                            100
                            * ((batMax * currentV[0] / maxV[0] - batMin) / (batMax - batMin))
                        )
                else:
                    while len(data) > 0:
                        v, data = data[0:2], data[2:]
                        result.append(struct.unpack("<H", v)[0] / 10)
                    self.caller.values = result

        #    _LOGGER.debug("called handler %s %s", cHandle, safe)

        if self.device is None:
            return
        try:
            services = self.device.getServices()
            for service in services:
                if "fff0" not in str(service.uuid):
                    continue
                for schar in service.getCharacteristics():
                    if self.AccountAndVerify in str(schar.uuid):
                        self.account_uuid = schar
                    if self.RealTimeData in str(schar.uuid):
                        self.RT_uuid = schar
                    if self.SettingData in str(schar.uuid):
                        self.Setting_uuid = schar
                    if self.SettingResult in str(schar.uuid):
                        self.SettingResult_uuid = schar

            self.account_uuid.write(self.KEY)
            print("Authenticated %s", self.mac)
            self.RT_uuid.getDescriptors()
            self.device.writeCharacteristic(self.RT_uuid.getHandle() + 1, self.Notify)
            self.device.writeCharacteristic(
                self.SettingResult_uuid.getHandle() + 1, self.Notify
            )
            self.getBattery()
            self.Setting_uuid.write(self.realTimeDataEnable)
            self.device.withDelegate(MyDelegate(self))
            print("Subscribed %s", self.mac)
            self.offline = 0
        except btle.BTLEException as ex:
            print("failed %s %s", self.mac, ex)
            self.device = None
            print("unsubscribe")
        return self.device

    def update(self):
        from bluepy import btle

        if not self.connected:
            return list()
        self.values = list()
        self.cnt += 1
        try:
            if self.cnt > 5:
                self.cnt = 0
                self.getBattery()
            while self.device.waitForNotifications(1):
                pass
            if self.values:
                self.offline = 0
            else:
                print("%s is silent", self.mac)
                if self.offline > 3:
                    try:
                        self.device.disconnect()
                    except btle.BTLEInternalError as e:
                        print("%s", e)
                    self.device = None
                    print("%s reconnect", self.mac)
                else:
                    self.offline += 1
        except btle.BTLEDisconnectError as e:
            print("%s", e)
            self.device = None
        finally:
            return (self.batteryPct, self.values)

