from os import listdir
from os.path import isfile, join

def getDevicesBluetooth():
    v1_dir = "./bluetooth/v1"
    v1_devices = [join(v1_dir, f) for f in listdir(v1_dir) if isfile(join(v1_dir, f))]

    v2_dir = "./bluetooth/v2"
    v2_devices = [join(v2_dir, f) for f in listdir(v2_dir) if isfile(join(v2_dir, f))]

    return v1_devices + v2_devices

def getDevicesModbusTcp():
    v1_dir = "./modbus-tcp/v1"
    v1_devices = [join(v1_dir, f) for f in listdir(v1_dir) if isfile(join(v1_dir, f))]

    return v1_devices
