import json

names_file = "./schemas/field-name.json"

names_schema = {}

with open(names_file, "r") as f:
    names_schema = json.load(f)

names: list[str] = [str(n["const"]) for n in names_schema["anyOf"]]

fields = []

for n in names:
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
        outp["state_class"] = "total_increasing"
        outp["device_class"] = "energy"
        outp["category"] = "diagnostic"
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
        outp["category"] = "config"
        outp["writeable"] = True
    elif "_serial_" in n or n.endswith("_serial"):
        outp["content"] = "serial"
        outp["category"] = "diagnostic"

    fields.append(outp)

with open("blocks.json", "w") as f:
    f.write(json.dumps(fields, indent=4))
