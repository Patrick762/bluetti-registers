import json
from os.path import join

from .datacls import DataField, DataProtocol


base_dir = "csv/"

def read_protocol_def_csv() -> list[DataField]:
    """protocols/*.csv - Describes each field per protocol. Includes starting registers, datatypes, field length and scaling"""
    protocols: list[DataField] = []

    with open(join(base_dir, "protocols", "registers.csv"), "r") as f:
        lines = f.readlines()

        head = lines[0]
        field_names = head.split(",")[2:]

        fields: list[DataField] = []
        for l in lines[1:]:
            cols = l.split(",")
            registers = cols[2:]

            for col, reg in enumerate(registers):
                fields.append(DataField(field_names[col], reg))

            protocol = DataProtocol(int(cols[0]), str(cols[1]), fields)
            protocols.append(protocol)

    # TODO datatypes csv

    # TODO lengths csv

    # TODO scalings csv

    return protocols

def read_devices_csv():
    """devices.csv - Describes which device uses which protocol and what fields are available"""
    pass

def read_datasheet_csv():
    """specs.csv - Contains specs per powerstation such as max. input voltage / power to filter out invalid values if needed"""
    pass
