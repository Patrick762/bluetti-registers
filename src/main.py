import json
from os.path import join

from generator import read_protocol_def_csv, read_devices_csv

if __name__ == "__main__":
    protocols = read_protocol_def_csv()

    with open(join("out", "protocols.json"), "w") as f:
        json.dump([o.to_dict() for o in protocols], f, indent=2)

    devices = read_devices_csv(protocols)

    with open(join("out", "devices.json"), "w") as f:
        json.dump([d.to_dict() for d in devices], f, indent=2)

    # TESTING ONLY
    with open(join("out", "short.json"), "w") as f:
        json.dump(
            [
                {"n": d.name, "c": len(d.fields), "r": [f.start for f in d.fields]}
                for d in devices
            ],
            f,
            indent=2,
        )
