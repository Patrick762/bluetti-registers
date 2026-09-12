import json
from os.path import join

from generator import read_protocol_def_csv, read_devices_csv, read_enum_csv

if __name__ == "__main__":
    protocols = read_protocol_def_csv()

    with open(join("out", "protocols.json"), "w") as f:
        json.dump([o.to_dict() for o in protocols], f, indent=2)

    devices = read_devices_csv(protocols)

    with open(join("out", "devices.json"), "w") as f:
        json.dump([d.to_dict() for d in devices], f, indent=2)

    enums = read_enum_csv()

    with open(join("out", "enums.json"), "w") as f:
        json.dump([e.to_dict() for e in enums], f, indent=2)
