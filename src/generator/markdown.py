from os.path import join

from .datacls import BluettiDevice, DataProtocol


def generate_md(
    protocols: list[DataProtocol],
    devices: list[BluettiDevice],
    translations: dict[str, dict[str, str]],
):
    t_en = translations["en"]
    
    bt_devices = []
    bt_devices_sections = []
    modbus_devices = []
    modbus_devices_sections = []

    for d in devices:
        if d.name in ["BT1", "BT2"]:
            continue

        contributors = ", ".join(
            [
                (
                    f"[{n}](https://github.com/{n.removeprefix('@')})"
                    if n.startswith("@")
                    else n
                )
                for n in d.contributors
            ]
        )

        row = f"|{d.name}|{contributors}|[Details](#{d.comm_type}-{d.name.lower()})"

        fields = "\n".join([f"- {t_en[f.name]} ({f.name})" for f in d.fields])

        section = f"""### <a id="{d.comm_type}-{d.name.lower()}"></a>{d.name}

Protocol version: {d.proto_version}

Supported fields:

{fields}

"""

        if d.comm_type == "bt":
            bt_devices.append(row)
            bt_devices_sections.append(section)
        elif d.comm_type == "modbus":
            modbus_devices.append(row)
            modbus_devices_sections.append(section)

    bt_devices = "\n".join(bt_devices)
    modbus_devices = "\n".join(modbus_devices)

    bt_devices_sections = "\n\n\n".join(bt_devices_sections)
    modbus_devices_sections = "\n\n\n".join(modbus_devices_sections)

    data_all = f"""<!--- Generated file. Do not edit. -->

# Bluetti Registers

There are two different protocols:

[Bluetooth (reverse engineered)](#bt) and [Modbus-TCP (official)](#modbus)

## <a id="bt"></a>Bluetooth Devices

The following bluetooth devices are currently supported:

|Device name|Contributor|Details|
|---|---|---|
{bt_devices}

{bt_devices_sections}

## <a id="modbus"></a>Modbus Devices

The following modbus devices are currently supported:

|Device name|Contributor|Details|
|---|---|---|
{modbus_devices}

{modbus_devices_sections}
"""

    data_bt = f"""<!--- Generated file. Do not edit. -->

# Bluetooth Devices

The following bluetooth devices are currently supported:

|Device name|Contributor|Details|
|---|---|---|
{bt_devices}

{bt_devices_sections}
"""

    data_modbus = f"""<!--- Generated file. Do not edit. -->

# Modbus Devices

The following modbus devices are currently supported:

|Device name|Contributor|Details|
|---|---|---|
{modbus_devices}

{modbus_devices_sections}
    """

    with open(join("out", "devices.md"), "w") as f:
        f.write(data_all)
        f.close()

    with open(join("out", "devices-bt.md"), "w") as f:
        f.write(data_bt)
        f.close()

    with open(join("out", "devices-modbus.md"), "w") as f:
        f.write(data_modbus)
        f.close()
