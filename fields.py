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
        field["num_min"] = 0
        field["num_max"] = 100
        field["state_class"] = "measurement"
        field["device_class"] = "battery"

    if n in BATTERY_SOH:
        field["content"] = "uint"
        field["unit"] = "%"
        field["num_min"] = 0
        field["num_max"] = 100
        field["category"] = "diagnostic"
        field["state_class"] = "measurement"

    if n in ENUM_FIELDS:
        field["content"] = "enum"

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
            field["unit"] = "%"
            field["num_min"] = 0
            field["num_max"] = 100
            field["writeable"] = True
            field["category"] = "config"
        case "b_soc_high":
            field["content"] = "uint"
            field["unit"] = "%"
            field["num_min"] = 0
            field["num_max"] = 100
            field["writeable"] = True
            field["category"] = "config"
        case "d_time_remaining":
            field["content"] = "uint"
            field["unit"] = "h"
            field["scale"] = 0.1
        case "d_power_off":
            field["content"] = "bool"
            field["writeable"] = True
        case "dc_eco_mode":
            field["options"] = "eco_mode"
        case "ac_eco_mode":
            field["options"] = "eco_mode"
        case "d_charging_mode":
            field["options"] = "charging_mode"
        case "ac_o_mode":
            field["options"] = "output_mode"
        case "ac_ups_mode":
            field["options"] = "ups_mode"
        case "d_display_mode":
            field["options"] = "display_mode"
        case "d_split_phase_mode":
            field["options"] = "split_phase_mode"
        case "d_led_mode":
            field["options"] = "led_mode"

    if n in ENUM_FIELDS:
        field["category"] = "diagnostic"

    return field
