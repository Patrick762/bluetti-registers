from os.path import join

from .datacls import DataField, DataProtocol


base_dir = "csv/"


def read_protocol_def_csv() -> list[DataField]:
    """protocols/*.csv - Describes each field per protocol. Includes starting registers, datatypes, field length and scaling"""
    protocols: list[DataField] = []

    with open(join(base_dir, "protocols", "registers.csv"), "r") as f:
        lines = f.readlines()

        head = lines[0].rstrip()
        field_names = head.split(",")[2:]

        for l in lines[1:]:
            l = l.rstrip()
            cols = l.split(",")
            registers = cols[2:]

            fields: list[DataField] = []
            for col, reg in enumerate(registers):
                if reg == "":
                    continue

                fields.append(DataField(field_names[col], int(reg)))

            protocol = DataProtocol(int(cols[0]), str(cols[1]), fields)
            protocols.append(protocol)

    with open(join(base_dir, "protocols", "datatypes.csv"), "r") as f:
        lines = f.readlines()

        head = lines[0].rstrip()
        field_names = head.split(",")[2:]

        for l in lines[1:]:
            l = l.rstrip()
            cols = l.split(",")
            types = cols[2:]

            protocol = next(
                filter(
                    lambda x: x.version == int(cols[0]) and x.comm_type == str(cols[1]),
                    protocols,
                ),
                None,
            )
            if not protocol:
                continue

            copy = protocol.fields

            for col, t in enumerate(types):
                if t == "":
                    continue

                field = next(filter(lambda x: x.name == field_names[col], copy), None)
                if field is not None:
                    field.datatype = t

            protocol.fields = copy

    with open(join(base_dir, "protocols", "lengths.csv"), "r") as f:
        lines = f.readlines()

        head = lines[0].rstrip()
        field_names = head.split(",")[2:]

        for l in lines[1:]:
            l = l.rstrip()
            cols = l.split(",")
            lengths = cols[2:]

            protocol = next(
                filter(
                    lambda x: x.version == int(cols[0]) and x.comm_type == str(cols[1]),
                    protocols,
                ),
                None,
            )
            if not protocol:
                continue

            copy = protocol.fields

            for col, length_val in enumerate(lengths):
                if length_val == "":
                    continue

                field = next(filter(lambda x: x.name == field_names[col], copy), None)
                if field is not None:
                    field.length = int(length_val)

            protocol.fields = copy

    with open(join(base_dir, "protocols", "scalings.csv"), "r") as f:
        lines = f.readlines()

        head = lines[0].rstrip()
        field_names = head.split(",")[2:]

        for l in lines[1:]:
            l = l.rstrip()
            cols = l.split(",")
            scalings = cols[2:]

            protocol = next(
                filter(
                    lambda x: x.version == int(cols[0]) and x.comm_type == str(cols[1]),
                    protocols,
                ),
                None,
            )
            if not protocol:
                continue

            copy = protocol.fields

            for col, scaling in enumerate(scalings):
                if scaling == "":
                    continue

                field = next(filter(lambda x: x.name == field_names[col], copy), None)
                if field is not None:
                    field.scaling = float(scaling)

            protocol.fields = copy

    return protocols


def read_devices_csv():
    """devices.csv - Describes which device uses which protocol and what fields are available"""
    pass


def read_datasheet_csv():
    """specs.csv - Contains specs per powerstation such as max. input voltage / power to filter out invalid values if needed"""
    pass
