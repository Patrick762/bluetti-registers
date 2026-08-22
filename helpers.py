from os import listdir
from os.path import isfile, join

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
    return not path.endswith("base.json")


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
