import json
from os.path import join

from generator import read_protocol_def_csv

if __name__ == "__main__":
    obj = read_protocol_def_csv()

    with open(join("out", "protocols.json"), "w") as f:
        json.dump([o.to_dict() for o in obj], f, indent=2)
