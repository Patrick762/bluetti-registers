# bluetti-registers
A json file containing all known bluetti registers.

Just import registers using the json file of a release or use the json files provided here: https://patrick762.github.io/bluetti-registers/

## Naming convention for field names

1. Type (PV/AC/DC/Grid/Device/Battery) (short: pv/ac/dc/g/d/b)

2. Phase/String/Battery number if available

3. in/out (short: i/o) or destination

4. power/voltage/current/energy/frequency/temperature (short: p/v/c/e/f/t)

5. **total** / **avg** (if total over all phases/strings or average over all cells)

## Workflow for new devices

1. Add new line in `csv/devices.csv` and select supported fields.
2. Generate a new `devices.json` using `python src/generate.py`
3. Check if the json includes the new device and fields are correct
4. Git commit and push

Note: Changing anything in `csv/scalings.csv` might break the fields `b_i_e` and `b_o_e`. The scalings for both should be `0.001`, not 1
