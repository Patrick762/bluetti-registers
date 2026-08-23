import json

from os.path import join

from helpers import create_field


def by_addr(f):
    return f["address"]


def generate(
    name: str,
    contributors: list[str],
    field_registers: dict[str, int],
    output_dir: str,
):
    if name == "":
        return

    obj = {
        "$schema": "https://patrick762.github.io/bluetti-registers/device.json",
        "name": name,
        "contributors": contributors,
        "fields": [],
    }

    fields = []

    for n, a in field_registers.items():
        field = create_field(n)
        field["address"] = a

        fields.append(field)

    fields.sort(key=by_addr)
    obj["fields"] = fields

    with open(join(output_dir, name.lower() + ".json"), "w") as f:
        f.write(json.dumps(obj, indent=4))


with open("modbus-tcp/modbus-tcp.csv") as f:
    all = f.readlines()
    header = all[0].split(",")

    for line in all[1:]:
        name = line.split(",")[0]
        contributors = line.split(",")[1].split(" ")
        dev = {}
        for idx, col in enumerate(line.split(",")):
            if idx < 2:
                continue
            if col != "" and header[idx] != "":
                addr = str(col).strip()
                if addr == "":
                    continue
                dev[str(header[idx]).strip()] = int(addr)

        generate(name, contributors, dev, "modbus-tcp/")

with open("bluetooth/bluetooth.csv") as f:
    all = f.readlines()
    header = all[0].split(",")

    for line in all[1:]:
        name = line.split(",")[0]
        contributors = line.split(",")[1].split(" ")
        dev = {}
        for idx, col in enumerate(line.split(",")):
            if idx < 2:
                continue
            if col != "" and header[idx] != "":
                addr = str(col).strip()
                if addr == "":
                    continue
                dev[str(header[idx]).strip()] = int(addr)

        generate(name, contributors, dev, "bluetooth/")
