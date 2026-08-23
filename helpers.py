from os import listdir
from os.path import isfile, join

from fields import create_special_fields

field_sorting = [
    "name",
    "address",
    "content",
    "length",
    "options",
    "unit",
    "scale",
    "num_min",
    "num_max",
    "writeable",
    "category",
    "state_class",
    "device_class",
]

SORT_ORDER = {attr: idx for idx, attr in enumerate(field_sorting)}


def is_json(path: str):
    return path.endswith(".json")


def getDevicesBluetooth():
    dir = "./bluetooth"
    devices = [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]

    return filter(is_json, devices)


def getDevicesModbusTcp():
    dir = "./modbus-tcp"
    devices = [join(dir, f) for f in listdir(dir) if isfile(join(dir, f))]

    return filter(is_json, devices)


def checkSortedFieldAttributes(field) -> bool:
    last_idx = -1
    for attr in field:
        # Ignore attributes not present in the reference sorting list
        if attr not in SORT_ORDER:
            continue

        current_idx = SORT_ORDER[attr]
        if current_idx < last_idx:
            return False
        last_idx = current_idx

    return True


def create_field(n: str):
    outp = {
        "name": n,
        "address": -1,
    }

    if "_p_" in n or n.endswith("_p"):
        outp["content"] = "uint"
        outp["unit"] = "W"
        outp["state_class"] = "measurement"
        outp["device_class"] = "power"
    elif "_v_" in n or n.endswith("_v"):
        outp["content"] = "uint"
        outp["unit"] = "V"
        outp["state_class"] = "measurement"
        outp["device_class"] = "voltage"
    elif "_c_" in n or n.endswith("_c"):
        outp["content"] = "uint"
        outp["unit"] = "A"
        outp["scale"] = 0.1
        outp["state_class"] = "measurement"
        outp["device_class"] = "current"
    elif "_e_" in n or n.endswith("_e"):
        outp["content"] = "uint"
        outp["unit"] = "kWh"
        outp["scale"] = 0.1
        outp["category"] = "diagnostic"
        outp["state_class"] = "total_increasing"
        outp["device_class"] = "energy"
    elif "_f_" in n or n.endswith("_f"):
        outp["content"] = "uint"
        outp["unit"] = "Hz"
        outp["scale"] = 0.1
        outp["state_class"] = "measurement"
        outp["device_class"] = "frequency"
    elif "_t_" in n or n.endswith("_t"):
        outp["content"] = "uint"
        outp["unit"] = "°C"
        outp["scale"] = 0.1
        outp["state_class"] = "measurement"
        outp["device_class"] = "temperature"
    elif n.endswith("_switch"):
        outp["content"] = "bool"
        outp["writeable"] = True
    elif "_ver_" in n or n.endswith("_ver"):
        outp["content"] = "version"
        outp["category"] = "diagnostic"
    elif "_mode_" in n or n.endswith("_mode"):
        outp["content"] = "enum"
        outp["options"] = ""
        outp["writeable"] = True
        outp["category"] = "config"
    elif "_serial_" in n or n.endswith("_serial"):
        outp["content"] = "serial"
        outp["category"] = "diagnostic"

    return create_special_fields(n, outp)
