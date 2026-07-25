#!/bin/python3

import requests
import json
from jsonschema import validate

print("Loading device schema")

schema = requests.get("https://raw.githubusercontent.com/Patrick762/bluetti-registers/refs/heads/main/schemas/device.json").json()

print("Loading device definition for EB3A")

with open("./devices/v1/eb3a.json") as f:
    data = json.load(f)

print("Validating")

validate(data, schema=schema)

print("Validation complete")
