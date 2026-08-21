import requests
import json
from jsonschema import validate

from helpers import getDevicesModbusTcp, getDevicesV1Bluetooth, getDevicesV2Bluetooth, getBaseV1Bluetooth, getBaseV2Bluetooth

print("Loading devices list schema")

schema = requests.get("https://raw.githubusercontent.com/Patrick762/bluetti-registers/refs/heads/main/schemas/all-devices.json").json()

print("Getting device files")

# region Bluetooth

result = []

# Load base fields
base_fields_v1 = list()
base_fields_v2 = list()

with open(getBaseV1Bluetooth(), "r") as f:
    data = json.load(f)
    base_fields_v1 = data["fields"]

with open(getBaseV2Bluetooth(), "r") as f:
    data = json.load(f)
    base_fields_v2 = data["fields"]

# Load device files
for i, fun in enumerate([getDevicesV1Bluetooth, getDevicesV2Bluetooth]):
    device_files = fun()
    base_fields: list = base_fields_v1 if i == 0 else base_fields_v2

    for f in device_files:
        print(f"Loading device definition {f}")

        with open(f, "r") as f:
            data = json.load(f)
            del data["$schema"]
            for bf in base_fields:
                data["fields"].append(bf)
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
