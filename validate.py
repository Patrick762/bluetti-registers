import requests
import json
from jsonschema import validate

from helpers import checkSortedFieldAttributes, getDevicesBluetooth, getDevicesModbusTcp

print("Loading device schema")

schema = requests.get(
    "https://raw.githubusercontent.com/Patrick762/bluetti-registers/refs/heads/main/schemas/device.json"
).json()

print("Getting device files")

device_files = getDevicesBluetooth()

for f in device_files:
    print(f"Loading device definition {f}")

    with open(f) as f:
        data = json.load(f)

    print("Validating")

    validate(data, schema=schema)

    # Check sorting for field attributes
    for f in list(data["fields"]):
        r = checkSortedFieldAttributes(f)
        if r is False:
            raise Exception(f'Field {f["name"]} of device {data["name"]} not sorted')

    print("Device validation complete")

device_files = getDevicesModbusTcp()

for f in device_files:
    print(f"Loading device definition {f}")

    with open(f) as f:
        data = json.load(f)

    print("Validating")

    validate(data, schema=schema)

    # Check sorting for field attributes
    for f in list(data["fields"]):
        r = checkSortedFieldAttributes(f)
        if r is False:
            raise Exception(f'Field {f["name"]} of device {data["name"]} not sorted')

    print("Device validation complete")

print("Done")
