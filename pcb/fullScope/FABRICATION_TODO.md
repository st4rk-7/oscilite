# FABRICATION TODO — Header Spacing Fix Required

## Measured vs. PCB values

| Dimension | PCB file (current) | Measured (real board) | Delta |
|---|---|---|---|
| J2↔J4 center-to-center | 35.56 mm | **38.1 mm** | **+2.54 mm (1 pitch)** |

The PCB was laid out one pin pitch too narrow. The board **will not seat** without this fix.

## Fix steps (KiCad GUI, ~10 min)

1. Open `fullScope.kicad_pcb` in KiCad PCB editor.
2. Select J4 → press `E` → change X from `135.56` to `138.1`. Hit OK.
3. Reconnect the 15 broken traces (thin white ratsnest lines). Press `X` to route.
4. Run DRC: Inspect → Design Rules Checker → 0 violations.
5. Re-export Gerbers: File → Fabrication Outputs → Gerbers.
6. Re-zip and replace `fullScope_gerbers.zip`.

## Other dimensions (confirmed safe)

- Pin pitch: 2.54 mm (standard)
- Row-to-row inside each header: 2.54 mm (standard dual-row)
- Board size: 45 mm x 60 mm

## After fix — order checklist

- [ ] J4 moved to X=138.1
- [ ] DRC clean (0 violations)
- [ ] Gerbers re-exported
- [ ] Upload to JLCPCB/PCBWay and verify preview
- [ ] Order
