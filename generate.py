import requests
import json
from jsonschema import validate

from helpers import getDevicesBluetooth

print("Loading devices list schema")

schema = requests.get("https://raw.githubusercontent.com/Patrick762/bluetti-registers/refs/heads/main/schemas/all-devices.json").json()

print("Getting device files")

device_files = getDevicesBluetooth()

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

with open("./bluetooth.json", "w") as f:
    f.write(json.dumps(result))

print("Done")
