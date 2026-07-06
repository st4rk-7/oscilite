from PIL import Image
import sys

# Load image and resize to ST7735 screen size
img = Image.open("Frieren _ Sousou no Frieren.jpg")
img = img.convert("RGB")
img = img.resize((160, 128))
pixels = img.load()

# Generate the C header file
with open("Core/Inc/splash.h", "w") as f:
    f.write("#ifndef __SPLASH_H\n")
    f.write("#define __SPLASH_H\n\n")
    f.write("#include <stdint.h>\n\n")
    f.write("const uint16_t logo[20480] = {\n")
    
    count = 0
    for y in range(128):
        for x in range(160):
            r, g, b = pixels[x, y]
            
            # Convert 24-bit RGB to 16-bit RGB565
            r5 = (r >> 3) & 0x1F
            g6 = (g >> 2) & 0x3F
            b5 = (b >> 3) & 0x1F
            rgb565 = (r5 << 11) | (g6 << 5) | b5
            
            f.write(f"0x{rgb565:04X}, ")
            count += 1
            if count % 16 == 0:
                f.write("\n")
                
    f.write("};\n\n")
    f.write("#endif\n")

print("Conversion complete! splash.h generated.")
