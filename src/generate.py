import json
from os.path import join, exists
from os import mkdir

from generator import (
    read_protocol_def_csv,
    read_devices_csv,
    read_enum_csv,
    read_translations_csv,
)

if __name__ == "__main__":
    if not exists("out"):
        mkdir("out")

    protocols = read_protocol_def_csv()

    with open(join("out", "protocols.json"), "w") as f:
        json.dump([o.to_dict() for o in protocols], f, indent=2)

    devices = read_devices_csv(protocols)

    with open(join("out", "devices.json"), "w") as f:
        json.dump([d.to_dict() for d in devices], f, indent=2)

    enums = read_enum_csv()

    with open(join("out", "enums.json"), "w") as f:
        json.dump([e.to_dict() for e in enums], f, indent=2)

    translations = read_translations_csv()

    with open(join("out", "translations.json"), "w") as f:
        json.dump(translations, f, indent=2)
