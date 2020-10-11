from bluepy import btle
from bluepy.btle import BTLEException
from prom_client import * 
import struct
import time

deviceMAC = "00:35:ff:d8:64:54"
setUUID = "0000fff1-0000-1000-8000-00805f9b34fb"
authUUID = "0000fff2-0000-1000-8000-00805f9b34fb"
rtUUID = "0000fff4-0000-1000-8000-00805f9b34fb"
setDataUUID = "0000fff5-0000-1000-8000-00805f9b34fb"
historyUUID = "0000fff3-0000-1000-8000-00805f9b34fb"
notify = '\x01\0'
authData = '\x21\x07\x06\x05\x04\x03\x02\x01\xb8\x22\0\0\0\0\0'
rtEnable = '\x0b\x01\0\0\0\0'
batteryEnable = '\x08\x24\0\0\0\0'

count=0

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
	#print("Received something")
	result = list()
	if cHandle == 37:
		if data[0] == 0x24:
			print("Received battery data")
	else:
		while len(data) > 0:
			v, data = data[0:2], data[2:]
			result.append(struct.unpack("<H",v)[0] / 10)
		#push_temperature(result[0])
		print(result[0])

			# ... process 'data'

print "Connecting..."

for i in range(0,5):
	try:
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
		print("Retrying connection. Attempt " + str(i) + " of 5")
		continue
	break
else:
	print("All attempts failed. Please try again.")	
	raise SystemExit

#print "Authenticating..."
#for i in range(0,5):
#	try:
#		auth = dev.getCharacteristics(uuid=authUUID)[0] # fff2 authentication characteristic
#		rt = dev.getCharacteristics(uuid=rtUUID)[0]
#		set = dev.getCharacteristics(uuid=setUUID)[0]
#		setD = dev.getCharacteristics(uuid=setDataUUID)[0]
#		histD = dev.getCharacteristics(uuid=historyUUID)[0]
#		print("Authentication UUID: " + str(auth.uuid))
#		print("RealTime UUID: " + str(rt.uuid))
#		print("SettingResult UUID: " + str(set.uuid))
#		print("SettingData UUID: " + str(setD.uuid))
#		print("HistoryData UUID: " + str(histD.uuid))
#
#		auth.write(authData,withResponse=True)
#		dev.writeCharacteristic(rt.getHandle() + 1,notify)
#		dev.writeCharacteristic(set.getHandle() + 1,notify)
#		setD.write(batteryEnable)
#		setD.write(rtEnable)	
#	
#		print("Authenticated successfully!")
#	except BTLEException:
#		print("Retrying authentication. Attempt " + str(i) + " of 5")
#		time.sleep(1)
#		continue
#	break
#else:
#	print("Authentication failure. Please try again.")
#	dev.disconnect()
#	raise SystemExit
			
print "Waiting for data..."
for i in range(0,5):
	try:
		dev.setDelegate(MyDelegate())
		while count < 60:
			if dev.waitForNotifications(1):
				continue
			count=count+1
			print "."
			time.sleep(2)
	except BTLEException:
		print("Retrying data transfer. Attempt " + str(i) + " of 5")
		continue
	finally:
		print("Disconnecting")
		dev.disconnect()
else:
	print("Data transfer failure. Please try again.")
	dev.disconnect()
	raise SystemExit
