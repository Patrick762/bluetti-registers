import requests
import json
from jsonschema import validate

from helpers import (
    getDevicesModbusTcp,
    getDevicesBluetooth,
)

print("Loading devices list schema")

schema = requests.get(
    "https://patrick762.github.io/bluetti-registers/all-devices.json"
).json()

print("Getting device files")

# region Bluetooth

result = []

# Load device files
for f in getDevicesBluetooth():
    print(f"Loading device definition {f}")

    with open(f, "r") as f:
        data = json.load(f)
        del data["$schema"]
        result.append(data)

    print("added to result")

print("Validating output")

validate(result, schema=schema)

print("Writing result to file")

with open("./bluetooth.json", "w") as f:
    f.write(json.dumps(result))

# region Modbus TCP

device_files = getDevicesModbusTcp()

result = []

for f in device_files:
    print(f"Loading device definition {f}")

    with open(f, "r") as f:
        data = json.load(f)
        del data["$schema"]
        result.append(data)

    print("added to result")

print("Validating output")

validate(result, schema=schema)

print("Writing result to file")

with open("./modbus-tcp.json", "w") as f:
    f.write(json.dumps(result))

print("Done")
