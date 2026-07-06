# ⚠️ VERIFY BEFORE ORDERING — Header Spacing

The Diymore STM32F407VGT6 board (45mm x 60mm) plugs into J2 (2x16) and J4 (2x18).

## Confirmed (safe to lock in layout)
- Pin pitch: 2.54 mm (0.1")
- Row-to-row INSIDE each header: 2.54 mm (standard dual-row)
- Board size: 45 mm x 60 mm

## NOT confirmed from datasheet — MEASURE THE REAL BOARD
- Center-to-center distance BETWEEN J2 and J4 (across board width).
  - Estimated ~38-43 mm (edge headers on a 45mm-wide board).
  - **Measure with calipers before fabrication.** If off by >0.5mm the board will not seat.

Source: https://stm32-base.org/boards/STM32F407VGT6-diymore.html
