from os.path import join

from .datacls import BluettiDevice, BluettiEnum, DataField, DataProtocol


base_dir = "csv/"


def read_protocol_def_csv() -> list[DataProtocol]:
    protocols: list[DataProtocol] = []

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

    with open(join(base_dir, "protocols", "writeable.csv"), "r") as f:
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

            for col, writeable in enumerate(scalings):
                if writeable != "1":
                    continue

                field = next(filter(lambda x: x.name == field_names[col], copy), None)
                if field is not None:
                    field.writeable = True

            protocol.fields = copy

    with open(join(base_dir, "protocols", "units.csv"), "r") as f:
        lines = f.readlines()

        field_names = lines[0].rstrip().split(",")

        for l in lines[1:]:
            l = l.rstrip()
            cols = l.split(",")

            for protocol in protocols:
                copy = protocol.fields

                for col, unit in enumerate(cols):
                    if unit == "":
                        continue

                    field = next(
                        filter(lambda x: x.name == field_names[col], copy), None
                    )

                    if field is not None:
                        field.unit = unit

                protocol.fields = copy

    with open(join(base_dir, "protocols", "categories.csv"), "r") as f:
        lines = f.readlines()

        field_names = lines[0].rstrip().split(",")

        for l in lines[1:]:
            l = l.rstrip()
            cols = l.split(",")

            for protocol in protocols:
                copy = protocol.fields

                for col, category in enumerate(cols):
                    if category == "":
                        continue

                    field = next(
                        filter(lambda x: x.name == field_names[col], copy), None
                    )

                    if field is not None:
                        field.category = category

                protocol.fields = copy

    with open(join(base_dir, "protocols", "sensors.csv"), "r") as f:
        lines = f.readlines()

        field_names = lines[0].rstrip().split(",")

        for l in lines[1:]:
            l = l.rstrip()
            cols = l.split(",")

            for protocol in protocols:
                copy = protocol.fields

                for col, sensor in enumerate(cols):
                    if sensor == "":
                        continue

                    field = next(
                        filter(lambda x: x.name == field_names[col], copy), None
                    )

                    if field is not None:
                        field.sensor = sensor

                protocol.fields = copy

    with open(join(base_dir, "protocols", "state_types.csv"), "r") as f:
        lines = f.readlines()

        field_names = lines[0].rstrip().split(",")

        for l in lines[1:]:
            l = l.rstrip()
            cols = l.split(",")

            for protocol in protocols:
                copy = protocol.fields

                for col, state_type in enumerate(cols):
                    if state_type == "":
                        continue

                    field = next(
                        filter(lambda x: x.name == field_names[col], copy), None
                    )

                    if field is not None:
                        field.state_type = state_type

                protocol.fields = copy

    return protocols


def read_devices_csv(protocols: list[DataProtocol]) -> list[BluettiDevice]:
    devices: list[BluettiDevice] = []

    with open(join(base_dir, "devices.csv"), "r") as f:
        lines = f.readlines()

        head = lines[0].rstrip()
        field_names = head.split(",")[3:]

        for l in lines[1:]:
            l = l.rstrip()
            cols = l.split(",")
            supported_fields = cols[3:]

            fields: list[DataField] = []
            for col, supp in enumerate(supported_fields):
                if supp != "1":
                    continue

                fname = field_names[col]

                found_proto = next(
                    filter(
                        lambda x: x.version == int(cols[1])
                        and x.comm_type == str(cols[2]),
                        protocols,
                    ),
                    None,
                )

                if found_proto is None:
                    raise Exception(
                        f"Protocol with version {cols[1]} and comm_type {cols[2]} not found (device: {cols[0]})"
                    )

                found_field = next(
                    filter(lambda x: x.name == str(fname), found_proto.fields), None
                )

                if found_field is None:
                    raise Exception(
                        f"Field {fname} not defined in protocol with version {cols[1]} and comm_type {cols[2]} (device: {cols[0]})"
                    )

                fields.append(found_field)

            device = BluettiDevice(
                str(cols[0]), int(cols[1]), str(cols[2]), fields, [], {}
            )
            devices.append(device)

    with open(join(base_dir, "contributors.csv"), "r") as f:
        lines = f.readlines()

        head = lines[0].rstrip()

        for l in lines[1:]:
            l = l.rstrip()
            cols = l.split(",")
            contributors = list(filter(lambda x: x != "", cols[3:]))

            device = next(
                filter(
                    lambda x: x.name == str(cols[0])
                    and x.proto_version == int(cols[1])
                    and x.comm_type == str(cols[2]),
                    devices,
                ),
                None,
            )
            if not device:
                continue

            device.contributors = contributors

    with open(join(base_dir, "specs.csv"), "r") as f:
        lines = f.readlines()

        head = lines[0].rstrip()
        spec_names = head.split(",")[1:]

        for l in lines[1:]:
            l = l.rstrip()
            cols = l.split(",")
            specs = cols[1:]

            device = next(
                filter(
                    lambda x: x.name == str(cols[0]),
                    devices,
                ),
                None,
            )
            if not device:
                continue

            specififations = {}
            for col, spec in enumerate(specs):
                specififations[spec_names[col]] = spec

            device.specififations = specififations

    return devices


def read_enum_csv():
    enums: list[BluettiEnum] = []

    with open(join(base_dir, "protocols", "enums.csv"), "r") as f:
        lines = f.readlines()

        for l in lines[1:]:
            l = l.rstrip()
            cols = l.split(",")
            values = cols[1:]

            values_dict: dict[int, str] = {}
            for col, val in enumerate(values):
                if val == "":
                    continue

                values_dict[col] = val

            enum = BluettiEnum(str(cols[0]), values_dict)
            enums.append(enum)

    return enums
