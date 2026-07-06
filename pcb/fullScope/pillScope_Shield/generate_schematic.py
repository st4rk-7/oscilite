#!/usr/bin/env python3
"""
Generate a clean, professional pillScope Shield schematic for KiCad 10.
Organized like the original tviac1234 schematic with dashed section boxes,
section labels, and clean component placement.
"""

import uuid

def uid():
    return str(uuid.uuid4())

# ─── Layout Constants (mm coordinates) ──────────────────────────────────────
# KiCad A4 sheet: 297 x 210 mm

# Section: STM32 Core (center-left)
STM32_X = 80
STM32_Y = 75

# Section: Analog Frontend (bottom-left)
ANALOG_X = 55
ANALOG_Y = 155

# Section: Buttons (top-right)
BTN_X = 215
BTN_Y = 55

# Section: Display (bottom-right)
DISP_X = 220
DISP_Y = 150

# Section: Probe Input (far left)
PROBE_X = 25
PROBE_Y = 155

output = []

def emit(s):
    output.append(s)

# ─── Header ──────────────────────────────────────────────────────────────────
emit("""(kicad_sch
\t(version 20260306)
\t(generator "eeschema")
\t(generator_version "10.0")
\t(uuid "4c331a22-4b88-460e-bbed-7cdc709fd453")
\t(paper "A4")
\t(title_block
\t\t(title "pillScope Shield v1.0")
\t\t(company "st4rk")
\t\t(comment 1 "STM32F407VGT6 Diymore - Analog Frontend + UI")
\t\t(comment 2 "MCP6002 Buffer + 68k Bias + 500k Trimmer")
\t)""")

# ─── Library Symbols ────────────────────────────────────────────────────────
# Read from current file and reuse the lib_symbols section
import re, sys, os

current_sch = os.path.join(os.path.dirname(__file__), "pillScope_Shield.kicad_sch")
with open(current_sch, 'r') as f:
    content = f.read()

# Extract lib_symbols block
lib_start = content.find('\t(lib_symbols')
if lib_start == -1:
    print("ERROR: Could not find lib_symbols in current schematic", file=sys.stderr)
    sys.exit(1)

# Find the matching closing paren
depth = 0
i = lib_start
while i < len(content):
    if content[i] == '(':
        depth += 1
    elif content[i] == ')':
        depth -= 1
        if depth == 0:
            lib_end = i + 1
            break
    i += 1

emit(content[lib_start:lib_end])

# ─── Helper Functions ────────────────────────────────────────────────────────

def box(x1, y1, x2, y2, label=""):
    """Draw a dashed rectangle with optional label"""
    # Four polylines for the box
    emit(f"""
\t(polyline (pts (xy {x1} {y1}) (xy {x2} {y1}))
\t\t(stroke (width 0) (type dash) (color 0 0 0 0))
\t\t(uuid "{uid()}")
\t)
\t(polyline (pts (xy {x2} {y1}) (xy {x2} {y2}))
\t\t(stroke (width 0) (type dash) (color 0 0 0 0))
\t\t(uuid "{uid()}")
\t)
\t(polyline (pts (xy {x2} {y2}) (xy {x1} {y2}))
\t\t(stroke (width 0) (type dash) (color 0 0 0 0))
\t\t(uuid "{uid()}")
\t)
\t(polyline (pts (xy {x1} {y2}) (xy {x1} {y1}))
\t\t(stroke (width 0) (type dash) (color 0 0 0 0))
\t\t(uuid "{uid()}")
\t)""")
    if label:
        emit(f"""
\t(text "{label}" (at {x1 + 2} {y2 - 1} 0)
\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t(uuid "{uid()}")
\t)""")

def power_symbol(lib_id, ref_prefix, value, x, y, angle=0):
    """Place a power symbol (+3.3V or GND)"""
    emit(f"""
\t(symbol (lib_id "{lib_id}") (at {x} {y} {angle}) (unit 1)
\t\t(in_bom yes) (on_board yes) (fields_autoplaced)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref_prefix}" (at {x} {y - 3} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Value" "{value}" (at {x} {y - 2} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "" (at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" "" (at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(pin "1" (uuid "{uid()}"))
\t)""")

def resistor(ref, value, x, y, angle=0, fp="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal"):
    """Place a resistor"""
    emit(f"""
\t(symbol (lib_id "Device:R") (at {x} {y} {angle}) (unit 1)
\t\t(in_bom yes) (on_board yes) (fields_autoplaced)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}" (at {x + 2.54} {y - 1.27} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Value" "{value}" (at {x + 2.54} {y + 1.27} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Footprint" "{fp}" (at {x - 1.778} {y} 90)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" "~" (at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(pin "1" (uuid "{uid()}"))
\t\t(pin "2" (uuid "{uid()}"))
\t)""")

def label(name, x, y, angle=0):
    """Place a net label"""
    justify = "left" if angle == 0 else "right" if angle == 180 else "left"
    emit(f"""
\t(label "{name}"
\t\t(at {x} {y} {angle})
\t\t(effects (font (size 1.27 1.27)) (justify {justify}))
\t\t(uuid "{uid()}")
\t)""")

def wire(x1, y1, x2, y2):
    """Draw a wire"""
    emit(f"""
\t(wire (pts (xy {x1} {y1}) (xy {x2} {y2}))
\t\t(stroke (width 0) (type default) (color 0 0 0 0))
\t\t(uuid "{uid()}")
\t)""")

def junction(x, y):
    """Place a junction dot"""
    emit(f"""
\t(junction (at {x} {y}) (diameter 0) (color 0 0 0 0)
\t\t(uuid "{uid()}")
\t)""")

def no_connect(x, y):
    """Place a no-connect flag"""
    emit(f"""
\t(no_connect (at {x} {y}) (uuid "{uid()}"))""")

def pwr_flag(x, y):
    """Place a PWR_FLAG"""
    emit(f"""
\t(symbol (lib_id "power:PWR_FLAG") (at {x} {y} 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (fields_autoplaced)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "#FLG0{uid()[:4]}" (at {x} {y - 2} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Value" "PWR_FLAG" (at {x} {y + 2.54} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "" (at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" "~" (at {x} {y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(pin "1" (uuid "{uid()}"))
\t)""")

# ─── Section Boxes ───────────────────────────────────────────────────────────
box(22, 130, 115, 180, "Analog Frontend")
box(55, 38, 110, 120, "STM32 Core")
box(195, 38, 260, 100, "Buttons")
box(195, 130, 260, 180, "Display")

# ─── ANALOG FRONTEND SECTION ────────────────────────────────────────────────

# MCP6002 Unit A (Op-Amp triangle) at center of analog section
opamp_x = 75
opamp_y = 155

emit(f"""
\t(symbol (lib_id "Amplifier_Operational:MCP6002-xP") (at {opamp_x} {opamp_y} 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (fields_autoplaced)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "U1" (at {opamp_x} {opamp_y - 7} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Value" "MCP6002-xP" (at {opamp_x} {opamp_y - 9} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Footprint" "Package_DIP:DIP-8_W7.62mm" (at {opamp_x} {opamp_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" "http://ww1.microchip.com/downloads/en/DeviceDoc/21733j.pdf" (at {opamp_x} {opamp_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(pin "1" (uuid "{uid()}"))
\t\t(pin "2" (uuid "{uid()}"))
\t\t(pin "3" (uuid "{uid()}"))
\t)""")

# MCP6002 Unit C (Power pins)
pwr_x = 30
pwr_y = 145

emit(f"""
\t(symbol (lib_id "Amplifier_Operational:MCP6002-xP") (at {pwr_x} {pwr_y} 0) (unit 3)
\t\t(in_bom yes) (on_board yes) (fields_autoplaced)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "U1" (at {pwr_x} {pwr_y - 2} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Value" "MCP6002-xP" (at {pwr_x} {pwr_y + 2} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Footprint" "Package_DIP:DIP-8_W7.62mm" (at {pwr_x} {pwr_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" "" (at {pwr_x} {pwr_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(pin "4" (uuid "{uid()}"))
\t\t(pin "8" (uuid "{uid()}"))
\t)""")

# Power for Op-Amp
power_symbol("power:+3V3", "#PWR01", "+3.3V", pwr_x - 2.54, pwr_y - 7.62)
wire(pwr_x - 2.54, pwr_y - 7.62, pwr_x - 2.54, pwr_y - 3.81)

power_symbol("power:GND", "#PWR02", "GND", pwr_x - 2.54, pwr_y + 7.62)
wire(pwr_x - 2.54, pwr_y + 3.81, pwr_x - 2.54, pwr_y + 7.62)

# ─── Voltage Divider (R1=68k, R2=68k) ──────────────────────────────────────
# R1 from +3.3V to junction
r1_x = 55
r1_y = 148
resistor("R1", "68k", r1_x, r1_y)
power_symbol("power:+3V3", "#PWR03", "+3.3V", r1_x, r1_y - 7)
wire(r1_x, r1_y - 7, r1_x, r1_y - 3.81)

# R2 from junction to GND
r2_x = 55
r2_y = 162
resistor("R2", "68k", r2_x, r2_y)
power_symbol("power:GND", "#PWR04", "GND", r2_x, r2_y + 7)
wire(r2_x, r2_y + 3.81, r2_x, r2_y + 7)

# Connect R1 bottom to R2 top
wire(r1_x, r1_y + 3.81, r1_x, r2_y - 3.81)

# Junction at midpoint
mid_y = (r1_y + 3.81 + r2_y - 3.81) / 2
junction(r1_x, r1_y + 3.81)

# Wire from junction to Op-Amp Pin 3 (+)
wire(r1_x, r1_y + 3.81, opamp_x - 7.62, opamp_y + 2.54)

# ─── Trimmer Potentiometer (RV1=500k) ───────────────────────────────────────
rv_x = 42
rv_y = 165

emit(f"""
\t(symbol (lib_id "Device:R_Potentiometer") (at {rv_x} {rv_y} 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (fields_autoplaced)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "RV1" (at {rv_x - 5} {rv_y - 1.27} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Value" "500k" (at {rv_x - 5} {rv_y + 1.27} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Footprint" "Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical" (at {rv_x} {rv_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" "~" (at {rv_x} {rv_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(pin "1" (uuid "{uid()}"))
\t\t(pin "2" (uuid "{uid()}"))
\t\t(pin "3" (uuid "{uid()}"))
\t)""")

# RV1 Pin 1 (top) connects to Probe
label("PROBE_IN", rv_x, rv_y - 5.08, 0)
# RV1 Pin 2 (wiper) connects to junction (same node as R1/R2)
wire(rv_x + 2.54, rv_y, r1_x, r1_y + 3.81)
# RV1 Pin 3 (bottom) to GND
power_symbol("power:GND", "#PWR05", "GND", rv_x, rv_y + 7)
wire(rv_x, rv_y + 5.08, rv_x, rv_y + 7)

# ─── Unity Gain Feedback (Pin 1 to Pin 2) ───────────────────────────────────
# Op-Amp output (Pin 1) is at opamp_x + 7.62, opamp_y
# Op-Amp inverting input (Pin 2) is at opamp_x - 7.62, opamp_y - 2.54
fb_out_x = opamp_x + 7.62
fb_out_y = opamp_y
fb_in_x = opamp_x - 7.62
fb_in_y = opamp_y - 2.54

# Route feedback: output goes right, down, left, up to inverting input
wire(fb_out_x, fb_out_y, fb_out_x + 3, fb_out_y)
wire(fb_out_x + 3, fb_out_y, fb_out_x + 3, fb_out_y + 8)
wire(fb_out_x + 3, fb_out_y + 8, fb_in_x - 3, fb_out_y + 8)
wire(fb_in_x - 3, fb_out_y + 8, fb_in_x - 3, fb_in_y)
wire(fb_in_x - 3, fb_in_y, fb_in_x, fb_in_y)

# Junction at output for ADC_IN label
junction(fb_out_x, fb_out_y)

# ADC_IN label on output
label("ADC", fb_out_x + 1, fb_out_y, 0)

# ─── Probe Input Connector (J3) ─────────────────────────────────────────────
j3_x = 30
j3_y = 165

emit(f"""
\t(symbol (lib_id "Connector_Generic:Conn_01x02") (at {j3_x} {j3_y} 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (fields_autoplaced)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "J3" (at {j3_x} {j3_y - 4} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "PROBE" (at {j3_x} {j3_y + 5} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" (at {j3_x} {j3_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" "~" (at {j3_x} {j3_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(pin "1" (uuid "{uid()}"))
\t\t(pin "2" (uuid "{uid()}"))
\t)""")

# J3 Pin 1 -> PROBE_IN label
label("PROBE_IN", j3_x - 5.08, j3_y, 180)
# J3 Pin 2 -> GND
power_symbol("power:GND", "#PWR06", "GND", j3_x - 5.08, j3_y - 2.54 + 5)
wire(j3_x - 5.08, j3_y - 2.54, j3_x - 5.08, j3_y - 2.54 + 5)

# ─── 1.65V Offset voltage label ─────────────────────────────────────────────
emit(f"""
\t(text "1.65V Offset voltage" (at {r1_x - 5} {r2_y + 12} 0)
\t\t(effects (font (size 1.27 1.27)) (justify left bottom))
\t\t(uuid "{uid()}")
\t)""")

# ─── STM32 CORE SECTION ─────────────────────────────────────────────────────

# Header 1 (J1) — 2x16, 32 pins
h1_x = 70
h1_y = 75

emit(f"""
\t(symbol (lib_id "Connector_Generic:Conn_02x16_Odd_Even") (at {h1_x} {h1_y} 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (fields_autoplaced)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "J1" (at {h1_x + 1.27} {h1_y - 21} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "Header 1" (at {h1_x + 1.27} {h1_y + 21} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_2x16_P2.54mm_Vertical" (at {h1_x} {h1_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" "~" (at {h1_x} {h1_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)""")
for i in range(1, 33):
    emit(f'\t\t(pin "{i}" (uuid "{uid()}"))')
emit("\t)")

# Header 2 (J2) — 2x18, 36 pins
h2_x = 95
h2_y = 75

emit(f"""
\t(symbol (lib_id "Connector_Generic:Conn_02x18_Odd_Even") (at {h2_x} {h2_y} 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (fields_autoplaced)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "J2" (at {h2_x + 1.27} {h2_y - 23} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "Header 2" (at {h2_x + 1.27} {h2_y + 23} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "Connector_PinHeader_2.54mm:PinHeader_2x18_P2.54mm_Vertical" (at {h2_x} {h2_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" "~" (at {h2_x} {h2_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)""")
for i in range(1, 37):
    emit(f'\t\t(pin "{i}" (uuid "{uid()}"))')
emit("\t)")

# ─── Labels on Header Pins ──────────────────────────────────────────────────
# Header 1: Pin 6 = PB7 (Button Up), Pin 4 = 3.3V, Pin 1 = GND
# Conn_02x16 pins: odd on left at h1_x - 3.81, even on right at h1_x + 3.81 + 2.54
# Pin 1 at top, each row is 2.54mm apart
# Odd pins (1,3,5,...,31) on left side
# Even pins (2,4,6,...,32) on right side

def h1_pin_pos(pin):
    """Get position of Header 1 pin"""
    if pin % 2 == 1:  # odd = left side
        row = (pin - 1) // 2
        return (h1_x - 3.81, h1_y - 19.05 + row * 2.54)
    else:  # even = right side
        row = (pin - 2) // 2
        return (h1_x + 3.81 + 2.54, h1_y - 19.05 + row * 2.54)

def h2_pin_pos(pin):
    """Get position of Header 2 pin"""
    if pin % 2 == 1:  # odd = left side
        row = (pin - 1) // 2
        return (h2_x - 3.81, h2_y - 21.59 + row * 2.54)
    else:  # even = right side
        row = (pin - 2) // 2
        return (h2_x + 3.81 + 2.54, h2_y - 21.59 + row * 2.54)

# Header 1 labels  
# Pin 1 = GND
px, py = h1_pin_pos(1)
power_symbol("power:GND", "#PWR07", "GND", px - 3, py)
wire(px, py, px - 3, py)

# Pin 4 = 3.3V  
px, py = h1_pin_pos(4)
power_symbol("power:+3V3", "#PWR08", "+3.3V", px + 3, py)
wire(px, py, px + 3, py)

# Pin 6 = PB7 (Button Up)
px, py = h1_pin_pos(6)
label("Button_Up", px + 1, py, 0)

# Header 2 labels
# Pin 7 = 3.3V
px, py = h2_pin_pos(7)
power_symbol("power:+3V3", "#PWR09", "+3.3V", px - 5, py)
wire(px, py, px - 5, py)

# Pin 8 = GND
px, py = h2_pin_pos(8)
power_symbol("power:GND", "#PWR10", "GND", px + 3, py)
wire(px, py, px + 3, py)

# Pin 12 = PA0 (ADC)
px, py = h2_pin_pos(12)
label("ADC", px + 1, py, 0)

# Pin 14 = PA2 (LCD_RST)
px, py = h2_pin_pos(14)
label("LCD_RST", px + 1, py, 0)

# Pin 16 = PA3 (LCD_DC)
px, py = h2_pin_pos(16)
label("LCD_DC", px + 1, py, 0)

# Pin 17 = PA4 (LCD_CS)
px, py = h2_pin_pos(17)
label("LCD_CS", px - 5, py, 180)

# Pin 18 = PA5 (LCD_SCK)
px, py = h2_pin_pos(18)
label("LCD_SCK", px + 1, py, 0)

# Pin 20 = PA7 (LCD_SDA)
px, py = h2_pin_pos(20)
label("LCD_SDA", px + 1, py, 0)

# Pin 25 = PB8 (Button Select)
px, py = h2_pin_pos(25)
label("Button_Sel", px - 5, py, 180)

# Pin 26 = PB9 (Button Down)
px, py = h2_pin_pos(26)
label("Button_Down", px + 1, py, 0)

# No-connect flags on unused Header 1 pins
h1_used = {1, 4, 6}
for pin in range(1, 33):
    if pin not in h1_used:
        px, py = h1_pin_pos(pin)
        if pin % 2 == 1:
            no_connect(px, py)
        else:
            no_connect(px, py)

# No-connect flags on unused Header 2 pins
h2_used = {7, 8, 12, 14, 16, 17, 18, 20, 25, 26}
for pin in range(1, 37):
    if pin not in h2_used:
        px, py = h2_pin_pos(pin)
        no_connect(px, py)

# Pin name annotations on headers
emit(f"""
\t(text "GND" (at {h1_x - 10} {h1_pin_pos(1)[1]} 0)
\t\t(effects (font (size 0.8 0.8) (color 0 100 0 1)) (justify left))
\t\t(uuid "{uid()}")
\t)
\t(text "3.3V" (at {h1_pin_pos(4)[0] + 5} {h1_pin_pos(4)[1]} 0)
\t\t(effects (font (size 0.8 0.8) (color 200 0 0 1)) (justify left))
\t\t(uuid "{uid()}")
\t)
\t(text "PB7" (at {h1_pin_pos(6)[0] + 5} {h1_pin_pos(6)[1]} 0)
\t\t(effects (font (size 0.8 0.8)) (justify left))
\t\t(uuid "{uid()}")
\t)""")

# ─── BUTTONS SECTION ─────────────────────────────────────────────────────────
for i, (name, lbl, btn_y_off) in enumerate([
    ("SW1", "Button_Up", 0),
    ("SW2", "Button_Sel", 18),
    ("SW3", "Button_Down", 36),
]):
    sw_x = 230
    sw_y = BTN_Y + btn_y_off
    
    emit(f"""
\t(symbol (lib_id "Switch:SW_Push") (at {sw_x} {sw_y} 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (fields_autoplaced)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{name}" (at {sw_x} {sw_y - 5} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Value" "{lbl.replace('Button_', 'Btn ')}" (at {sw_x} {sw_y - 3} 0)
\t\t\t(effects (font (size 1.27 1.27)))
\t\t)
\t\t(property "Footprint" "Button_Switch_THT:SW_PUSH_6mm_H5mm" (at {sw_x} {sw_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" "~" (at {sw_x} {sw_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(pin "1" (uuid "{uid()}"))
\t\t(pin "2" (uuid "{uid()}"))
\t)""")
    
    # Left side label
    label(lbl, sw_x - 5.08, sw_y, 180)
    # Right side to GND
    power_symbol("power:GND", f"#PWR{20+i}", "GND", sw_x + 8, sw_y)
    wire(sw_x + 5.08, sw_y, sw_x + 8, sw_y)

# ─── DISPLAY SECTION ─────────────────────────────────────────────────────────
lcd_x = 240
lcd_y = 155

emit(f"""
\t(symbol (lib_id "Connector_Generic:Conn_01x08") (at {lcd_x} {lcd_y} 0) (unit 1)
\t\t(in_bom yes) (on_board yes) (fields_autoplaced)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "J4" (at {lcd_x + 3} {lcd_y - 2} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Value" "LCD" (at {lcd_x + 3} {lcd_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) (justify left))
\t\t)
\t\t(property "Footprint" "Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical" (at {lcd_x} {lcd_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(property "Datasheet" "~" (at {lcd_x} {lcd_y} 0)
\t\t\t(effects (font (size 1.27 1.27)) hide)
\t\t)
\t\t(pin "1" (uuid "{uid()}"))
\t\t(pin "2" (uuid "{uid()}"))
\t\t(pin "3" (uuid "{uid()}"))
\t\t(pin "4" (uuid "{uid()}"))
\t\t(pin "5" (uuid "{uid()}"))
\t\t(pin "6" (uuid "{uid()}"))
\t\t(pin "7" (uuid "{uid()}"))
\t\t(pin "8" (uuid "{uid()}"))
\t)""")

# LCD pin labels (pins go from 1=top to 8=bottom)
# Pin 1 (VCC) at lcd_y + offset for pin 1
lcd_pin_y = lambda pin: lcd_y - 8.89 + (pin-1) * 2.54  # approximate

# Pin 1 = VCC -> +3.3V
power_symbol("power:+3V3", "#PWR30", "+3.3V", lcd_x - 10, lcd_pin_y(1))
wire(lcd_x - 5.08, lcd_pin_y(1), lcd_x - 10, lcd_pin_y(1))

# Pin 2 = GND
power_symbol("power:GND", "#PWR31", "GND", lcd_x - 10, lcd_pin_y(2))
wire(lcd_x - 5.08, lcd_pin_y(2), lcd_x - 10, lcd_pin_y(2))

# Pin 3 = CS
label("LCD_CS", lcd_x - 5.08 - 1, lcd_pin_y(3), 180)

# Pin 4 = RST
label("LCD_RST", lcd_x - 5.08 - 1, lcd_pin_y(4), 180)

# Pin 5 = DC
label("LCD_DC", lcd_x - 5.08 - 1, lcd_pin_y(5), 180)

# Pin 6 = SDA
label("LCD_SDA", lcd_x - 5.08 - 1, lcd_pin_y(6), 180)

# Pin 7 = SCK
label("LCD_SCK", lcd_x - 5.08 - 1, lcd_pin_y(7), 180)

# Pin 8 = LED -> +3.3V
power_symbol("power:+3V3", "#PWR32", "+3.3V", lcd_x - 10, lcd_pin_y(8))
wire(lcd_x - 5.08, lcd_pin_y(8), lcd_x - 10, lcd_pin_y(8))

# Pin name annotations next to LCD
for pin, name in [(1,"VCC"), (2,"GND"), (3,"CS"), (4,"RST"), (5,"DC"), (6,"SDA"), (7,"SCK"), (8,"LED")]:
    emit(f"""
\t(text "{name}" (at {lcd_x + 6} {lcd_pin_y(pin)} 0)
\t\t(effects (font (size 0.8 0.8)) (justify left))
\t\t(uuid "{uid()}")
\t)""")

# ─── PWR_FLAGs ──────────────────────────────────────────────────────────────
# These tell KiCad that power is being provided
pwr_flag_x = 60
pwr_flag_y = 42
power_symbol("power:+3V3", "#PWR40", "+3.3V", pwr_flag_x, pwr_flag_y)
pwr_flag(pwr_flag_x, pwr_flag_y)

power_symbol("power:GND", "#PWR41", "GND", pwr_flag_x + 10, pwr_flag_y + 3)
pwr_flag(pwr_flag_x + 10, pwr_flag_y + 3)

# ─── Notes ──────────────────────────────────────────────────────────────────
emit(f"""
\t(text "Rref (R1 and R2) can be any matched value.\\nThey create a 1.65V DC bias at Pin 3." (at 25  185 0)
\t\t(effects (font (size 1.0 1.0)) (justify left bottom))
\t\t(uuid "{uid()}")
\t)""")

emit(f"""
\t(text "Buttons use STM32 internal pull-ups.\\nNo external resistors needed." (at 200  95 0)
\t\t(effects (font (size 1.0 1.0)) (justify left bottom))
\t\t(uuid "{uid()}")
\t)""")

# ─── Close ──────────────────────────────────────────────────────────────────
emit(")")

# ─── Write Output ────────────────────────────────────────────────────────────
output_path = os.path.join(os.path.dirname(__file__), "pillScope_Shield_clean.kicad_sch")
with open(output_path, 'w') as f:
    f.write('\n'.join(output))

print(f"✅ Generated: {output_path}")
print("Open this file in KiCad to see the organized schematic!")
