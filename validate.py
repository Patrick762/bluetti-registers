#!/bin/python3

import requests
import json
from jsonschema import validate

from helpers import getDevices

print("Loading device schema")

schema = requests.get("https://raw.githubusercontent.com/Patrick762/bluetti-registers/refs/heads/main/schemas/device.json").json()

print("Getting device files")

device_files = getDevices()

for f in device_files:
    print(f"Loading device definition {f}")

    with open(f) as f:
        data = json.load(f)

    print("Validating")

    validate(data, schema=schema)

    print("Device validation complete")

print("Done")
