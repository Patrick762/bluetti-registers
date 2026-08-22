import json

from helpers import create_field

names_file = "./schemas/field-name.json"

names_schema = {}

with open(names_file, "r") as f:
    names_schema = json.load(f)

names: list[str] = [str(n["const"]) for n in names_schema["anyOf"]]

fields = []

for n in names:
    outp = create_field(n)
    fields.append(outp)

with open("blocks.json", "w") as f:
    f.write(json.dumps(fields, indent=4))

csv_head = ",".join(["device"] + [str(n) for n in names])

with open("bluetooth.csv", "w") as f:
    f.write(csv_head)

with open("modbus-tcp.csv", "w") as f:
    f.write(csv_head)
