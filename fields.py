from typing import Any

AMOUNT_FIELDS = [
    "d_num_inverters",
    "d_num_battery_packs",
    "b_cycle_count",
    "b_cell_count",
    "b_ntc_count",
]

BATTERY_SOC = [
    "b_soc_total",
    "b_soc",
]

BATTERY_SOH = [
    "b_soh_total",
    "b_soh",
]

ENUM_FIELDS = [
    "d_inverter_status",
    "d_inverter_warning",
    "d_inverter_fault",
]


def create_special_fields(n: str, field: dict[str, Any]):
    if n in AMOUNT_FIELDS:
        field["content"] = "uint"
        field["category"] = "diagnostic"

    if n in BATTERY_SOC:
        field["content"] = "uint"
        field["unit"] = "%"
        field["state_class"] = "measurement"
        field["device_class"] = "battery"

    if n in BATTERY_SOH:
        field["content"] = "uint"
        field["unit"] = "%"
        field["category"] = "diagnostic"
        field["state_class"] = "measurement"

    if n in ENUM_FIELDS:
        field["content"] = "enum"
        field["category"] = "diagnostic"

    match (n):
        case "d_inverter_total":
            field["content"] = "uint"
            field["unit"] = "W"
            field["state_class"] = "measurement"
            field["device_class"] = "power"
        case "d_inverter_status":
            field["options"] = "inverter_status"
        case "d_inverter_warning":
            field["options"] = "inverter_warning"
        case "d_inverter_fault":
            field["options"] = "inverter_fault"
        case "d_inverter_type":
            field["content"] = "string"
            field["length"] = 6
            field["category"] = "diagnostic"
        case "b_type":
            field["content"] = "string"
            field["length"] = 6
            field["category"] = "diagnostic"
        case "b_cycle_count":
            field["state_class"] = "measurement"
        case "b_soc_low":
            field["content"] = "uint"
            field["writeable"] = True
            field["unit"] = "%"
            field["category"] = "config"
        case "b_soc_high":
            field["content"] = "uint"
            field["writeable"] = True
            field["unit"] = "%"
            field["category"] = "config"

    return field
