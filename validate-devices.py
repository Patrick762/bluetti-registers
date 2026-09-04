import requests
import json
from jsonschema import validate

from helpers import getDevicesBluetooth, getDevicesModbusTcp

print("Loading device schema")

schema = requests.get(
    "https://patrick762.github.io/bluetti-registers/device.json"
).json()

print("Getting device files")

device_files = getDevicesBluetooth()

for f in device_files:
    print(f"Loading device definition {f}")

    with open(f) as f:
        data = json.load(f)

    print("Validating")

    validate(data, schema=schema)

    if len(data["contributors"]) == 0:
        raise Exception(f'Contributors for device {data["name"]} missing')

    print("Device validation complete")

device_files = getDevicesModbusTcp()

for f in device_files:
    print(f"Loading device definition {f}")

    with open(f) as f:
        data = json.load(f)

    print("Validating")

    validate(data, schema=schema)

    print("Device validation complete")

print("Done")
