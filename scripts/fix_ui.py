import re

with open("Core/Src/ui.c", "r") as f:
    text = f.read()

# Remove the old LCD_printf injection at the top
text = re.sub(r'#include <stdarg\.h>\n#include <stdio\.h>\n\nvoid LCD_printf.*?\n}\n\n', '', text, flags=re.DOTALL)

# Create the proper LCD_printf function
lcd_printf_code = """
#include <stdarg.h>
#include <stdio.h>

void LCD_printf(const char *format, ...) {
    char buffer[64];
    va_list args;
    va_start(args, format);
    vsnprintf(buffer, sizeof(buffer), format, args);
    va_end(args);
    
    // Remove newline if present
    for(int i=0; i<64; i++) {
        if(buffer[i] == 0) break;
        if(buffer[i] == '\\n' || buffer[i] == '\\r') {
            buffer[i] = ' ';
        }
    }
    printString(buffer);
}
"""

# Inject after #include "gfx.h" which is where printString is defined
text = text.replace('#include "gfx.h"', '#include "gfx.h"\n' + lcd_printf_code)

with open("Core/Src/ui.c", "w") as f:
    f.write(text)
