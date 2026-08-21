# bluetti-registers
A json file containing all known bluetti registers.

Just import registers using the json file of a release.

## Naming convention for field names

1. Type (PV/AC/Grid/Device/Battery) (short: pv/ac/g/d/b)

2. Phase/String/Battery number if available

3. in/out (short: i/o) or destination

4. power/voltage/current/energy/frequency/temperature (short: p/v/c/e/f/t)

5. **total** / **avg** (if total over all phases/strings or average over all cells)
