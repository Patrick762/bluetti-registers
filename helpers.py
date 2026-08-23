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


def is_not_base(path: str):
    return (not path.endswith("base.json") and path.endswith(".json"))


def getDevicesV1Bluetooth():
    v1_dir = "./bluetooth/v1"
    v1_devices = [join(v1_dir, f) for f in listdir(v1_dir) if isfile(join(v1_dir, f))]

    return filter(is_not_base, v1_devices)


def getDevicesV2Bluetooth():
    v2_dir = "./bluetooth/v2"
    v2_devices = [join(v2_dir, f) for f in listdir(v2_dir) if isfile(join(v2_dir, f))]

    return filter(is_not_base, v2_devices)


def getDevicesBluetooth():
    return list(getDevicesV1Bluetooth()) + list(getDevicesV2Bluetooth())


def getBaseV1Bluetooth():
    v1_dir = "./bluetooth/v1"
    return join(v1_dir, "base.json")


def getBaseV2Bluetooth():
    v2_dir = "./bluetooth/v2"
    return join(v2_dir, "base.json")


def getDevicesModbusTcp():
    v1_dir = "./modbus-tcp/v1"
    v1_devices = [join(v1_dir, f) for f in listdir(v1_dir) if isfile(join(v1_dir, f))]

    return filter(is_not_base, v1_devices)


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
        outp["category"] = "config"
        outp["writeable"] = True
    elif "_serial_" in n or n.endswith("_serial"):
        outp["content"] = "serial"
        outp["category"] = "diagnostic"

    return create_special_fields(n, outp)
