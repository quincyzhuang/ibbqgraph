#!/usr/bin/env python3
from bluepy import btle
from bluepy.btle import BTLEException
from pprint import pprint
from prom_client import *
import struct
import time
import sys

FILE_PATH = "temp.txt"
deviceMAC = "00:35:ff:d8:64:54"
setUUID = "0000fff1-0000-1000-8000-00805f9b34fb"
authUUID = "0000fff2-0000-1000-8000-00805f9b34fb"
rtUUID = "0000fff4-0000-1000-8000-00805f9b34fb"
setDataUUID = "0000fff5-0000-1000-8000-00805f9b34fb"
historyUUID = "0000fff3-0000-1000-8000-00805f9b34fb"
notify = b"\x01\x00"
authData = bytearray(b'\x21\x07\x06\x05\x04\x03\x02\x01\xb8\x22\0\0\0\0\0')
rtEnable = bytearray(b'\x0b\x01\0\0\0\0')
batteryEnable = bytearray(b'\x08\x24\0\0\0\0')
LEGACY_MODE=0


class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        result = list()
        if cHandle == 37:
            if data[0] == 0x24:
                #print("Received battery data")
                currentV = struct.unpack("<H", data[1:3])
                maxV = struct.unpack("<H", data[3:5])
                batteryPct = int(
                    100
                    * ((batMax * currentV[0] / maxV[0] - batMin) / (batMax - batMin))
                )
        else:
            while len(data) > 0:
                v, data = data[0:2], data[2:]
                upacked_data = struct.unpack("<H",v)
                raw_data = upacked_data[0] / 10
                result.append(raw_data)
            probe_one = result[0]*9.0/5.0 + 32
            probe_two = result[1]*9.0/5.0 + 32
            if LEGACY_MODE == 1:
                output_text = str(time.ctime()) 
                print(output_text + " probe 1: " + str(probe_one) + " probe 2: " + str(probe_two))
                with open(FILE_PATH,'w') as output:
                    output.write(output_text)
            else:  # Prometheus code here
                push_temperature(probe_one,1)
                push_temperature(probe_two,2)

print("Connecting...")

for i in range(0,5):
    try:
        dev = ''
        dev = btle.Peripheral(deviceMAC)
        print("Connected to " + str(dev.addr)+ "!")
        auth = dev.getCharacteristics(uuid=authUUID)[0] # fff2 authentication characteristic
        rt = dev.getCharacteristics(uuid=rtUUID)[0]
        set = dev.getCharacteristics(uuid=setUUID)[0]
        setD = dev.getCharacteristics(uuid=setDataUUID)[0]
        histD = dev.getCharacteristics(uuid=historyUUID)[0]
        print("Authentication UUID: " + str(auth.uuid))
        print("RealTime UUID: " + str(rt.uuid))
        print("SettingResult UUID: " + str(set.uuid))
        print("SettingData UUID: " + str(setD.uuid))
        print("HistoryData UUID: " + str(histD.uuid))
        auth.write(authData,withResponse=True)
        dev.writeCharacteristic(rt.getHandle() + 1,notify)
        dev.writeCharacteristic(set.getHandle() + 1,notify)
        setD.write(batteryEnable)
        setD.write(rtEnable)
        print("Authenticated successfully!")
    except BTLEException:
        print("Bluepy exception. Retrying connection. Attempt " + str(i) + " of 5")
        continue
    except BrokenPipeError as e:
        print("IO exception. Retrying connection. Attempt " + str(i) + " of 5")
        continue
    except Exception as e:
        print(str(type(e)) + " exception. Retrying connection. Attempt " + str(i) + " of 5")
        continue
    break
else:
    print("All attempts failed. Please try again.")
    if dev:
        dev.disconnect()
    sys.exit()

print("Waiting for data...")

dev.setDelegate(MyDelegate())
for i in range(0,5):
    try:
        while True:
            if dev.waitForNotifications(1):
                continue
    except BTLEException:
        print("Retrying data transfer. Attempt " + str(i) + " of 5")
        continue
    except AttributeError:
        print("Retrying data transfer. Attempt " + str(i) + " of 5")
        continue
    except Exception as e:
        print(str(type(e)) + "Retrying data transfer. Attempt " + str(i) + " of 5") 
        continue
else:
    print("Data transfer failure. Please try again.")
    dev.disconnect()
    raise SystemExit
