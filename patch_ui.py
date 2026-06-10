import re

with open("Core/Src/ui.c", "r") as f:
    text = f.read()

# Replace printf with LCD_printf
text = re.sub(r'\bprintf\(', 'LCD_printf(', text)

# Inject LCD_printf at the top of the file
lcd_printf_code = """
#include <stdarg.h>
#include <stdio.h>

void LCD_printf(const char *format, ...) {
    char buffer[64];
    va_list args;
    va_start(args, format);
    vsnprintf(buffer, sizeof(buffer), format, args);
    va_end(args);
    
    // Remove trailing newline as setCursor is used explicitly
    for(int i=0; buffer[i] != '\0'; i++) {
        if(buffer[i] == '\\n') {
            buffer[i] = ' ';
        }
    }
    printString(buffer);
}

"""

text = text.replace('#include "ui.h"', '#include "ui.h"\n' + lcd_printf_code)

with open("Core/Src/ui.c", "w") as f:
    f.write(text)
