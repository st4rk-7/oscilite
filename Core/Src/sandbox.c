#include "sandbox.h"
#include "gfx.h"
#include "st7735.h"

// Screen dimensions
#define SCREEN_WIDTH 160
#define SCREEN_HEIGHT 128

// Box properties
#define BOX_SIZE 20
int16_t box_x = 10;
int16_t box_y = 10;
int16_t box_dx = 2; // X velocity
int16_t box_dy = 2; // Y velocity

// Colors we will cycle through when hitting a wall
uint16_t colors[] = {ST7735_RED, ST7735_GREEN, ST7735_BLUE, ST7735_YELLOW, ST7735_CYAN, ST7735_MAGENTA};
int color_index = 0;

// Text animation properties
int16_t text_x = -40; // Start slightly off-screen to the left

void sandboxInit(void)
{
    // Clear the screen to black once at the very beginning
    clearDisplay();
    
    // Print a title
    setCursor(10, 10);
    setTextColor(ST7735_WHITE, ST7735_BLACK);
    printString("Sandbox Mode!");
    flushDisplay(); // SEND TO PHYSICAL SCREEN!
    HAL_Delay(1000); // Wait 1 second so the user can read it
    
    // Clear the screen again before the animation starts
    clearDisplay();
}

void sandboxLoop(void)
{
    // 1. ERASE THE OLD FRAME
    // Instead of clearing the whole screen (which causes ugly flickering), 
    // we only erase the exact spot where the box used to be!
    fillRect(box_x, box_y, BOX_SIZE, BOX_SIZE, ST7735_BLACK);

    // 2. UPDATE THE MATH
    box_x += box_dx;
    box_y += box_dy;

    // 3. CHECK FOR COLLISION WITH WALLS
    uint8_t hit_wall = 0;

    // Did we hit the Left or Right wall?
    if (box_x <= 0 || box_x + BOX_SIZE >= SCREEN_WIDTH)
    {
        box_dx = -box_dx; // Reverse X direction
        hit_wall = 1;
    }

    // Did we hit the Top or Bottom wall?
    if (box_y <= 0 || box_y + BOX_SIZE >= SCREEN_HEIGHT)
    {
        box_dy = -box_dy; // Reverse Y direction
        hit_wall = 1;
    }

    // If we hit a wall, change the color!
    if (hit_wall)
    {
        color_index++;
        if (color_index > 5) color_index = 0; // Loop back to the first color
    }

    // 4. DRAW THE NEW FRAME
    fillRect(box_x, box_y, BOX_SIZE, BOX_SIZE, colors[color_index]);

    // Update text position
    text_x += 2; // Move 2 pixels right every frame
    if (text_x > SCREEN_WIDTH)
    {
        text_x = -40; // Wrap back to the left side when it goes off screen
    }

    // Draw the moving "st4rk" text
    setCursor(text_x, 60);
    setTextColor(ST7735_YELLOW, ST7735_BLACK);
    printString("st4rk");
    
    // SEND THE HIDDEN CANVAS TO THE PHYSICAL SCREEN
    flushDisplay();

    // 5. WAIT (Frame Rate Control)
    // 16 milliseconds delay is roughly 60 Frames Per Second (1000ms / 60 = ~16ms)
    HAL_Delay(16); 
}
