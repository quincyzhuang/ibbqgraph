#!/usr/bin/env python3
from bluepy import btle
from bluepy.btle import BTLEException

print("Connecting...")

try:
    dev = btle.Peripheral("00:35:ff:d8:64:54")
except BTLEException:
    print("Unable to connect, please try again.")
    raise SystemExit

print("Services...")
for svc in dev.getServices():
	print(str(svc))
	print("Service UUID...")
	print(str(svc.uuid))
	print("Characteristics...")
	for ch in svc.getCharacteristics():
		print("Characteristic: ",str(ch))
		print("   UUID: ",str(ch.uuid))
		print("   Prop: ",str(ch.propertiesToString()))
		print("   Handle: ",str(ch.getHandle()))

print("Disconnecting...")
dev.disconnect()
