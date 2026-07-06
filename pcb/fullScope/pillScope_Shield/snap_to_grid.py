#!/usr/bin/env python3
"""Snap all coordinates in a KiCad schematic to the 1.27mm grid."""
import re
import sys

GRID = 1.27

def snap(val):
    """Snap a float value to nearest multiple of 1.27mm"""
    return round(round(val / GRID) * GRID, 4)

def snap_coords(match):
    """Snap coordinate pairs in (at X Y ...) or (xy X Y) patterns"""
    full = match.group(0)
    prefix = match.group(1)  # 'at' or 'xy'
    x = float(match.group(2))
    y = float(match.group(3))
    rest = match.group(4)  # everything after Y (angle, etc.)
    
    sx = snap(x)
    sy = snap(y)
    
    return f"({prefix} {sx} {sy}{rest}"

input_file = "/home/st4rk/Projects/scopef407/pcb/fullScope/pillScope_Shield/pillScope_Shield_clean.kicad_sch"
output_file = input_file  # overwrite

with open(input_file, 'r') as f:
    content = f.read()

# Match (at X Y ...) and (xy X Y) patterns
# Group 1: 'at' or 'xy'
# Group 2: X coordinate
# Group 3: Y coordinate  
# Group 4: rest of the expression
pattern = r'\((at|xy)\s+([-\d.]+)\s+([-\d.]+)([\s\d.)]*)'
result = re.sub(pattern, snap_coords, content)

with open(output_file, 'w') as f:
    f.write(result)

print(f"✅ Snapped all coordinates to {GRID}mm grid!")
