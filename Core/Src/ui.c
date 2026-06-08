#include "main.h"
#include "scope.h"
#include "ui.h"


#include "wave.h"
#include "splash.h"
#include "st7735.h"
#include "gfx.h"

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
        if(buffer[i] == '\n' || buffer[i] == '\r') {
            buffer[i] = ' ';
        }
    }
    printString(buffer);
}

#include <stdio.h>
#include <string.h>

// Forward declarations
void outputSerial(char s[], uint8_t o);
void outputCSV(uint8_t o);
void outputTek(uint8_t o);

#define WHITE ST7735_WHITE
#define BLACK ST7735_BLACK

#define MENUPOS 134

// All kinds of variables, you'll see what these do in scope.c
extern uint16_t adcBuf[BUFFER_LEN];
extern int atten;
extern float vdiv;
extern float trigVoltage;
extern uint8_t trig;
extern uint8_t trigged;
extern int trigPoint;

extern float tdiv;
extern uint32_t sampRate;
extern float sampPer;

extern float maxVoltage, minVoltage;
extern float measuredFreq, sigPer;

volatile uint8_t outputFlag = 0; // whether or not we should output data to the USB or UART port
extern UART_HandleTypeDef huart1;

uint8_t autocalFlag = 0;
extern float offsetVoltage;

uint8_t fast = 1;

// Vertical autocalibration
void autoCal()
{
    clearDisplay();
    setCursor(0, 0);
    setTextColor(BLACK, WHITE);
    printString("Autocalibration\n\n");
    setTextColor(WHITE, BLACK);
    printString("Couple input to ground\nThen press Select");
    flushDisplay();
    while (HAL_GPIO_ReadPin(BTN2_GPIO_Port, BTN2_Pin))
        ;
    HAL_Delay(150);

    sample();

    clearDisplay();
    setCursor(0, 0);
    setTextColor(BLACK, WHITE);
    printString("Autocalibration\n\n");
    setTextColor(WHITE, BLACK);

    uint32_t adcAvg = 0;
    for (int i = 0; i < BUFFER_LEN; i++)
        adcAvg += adcBuf[i];
    adcAvg /= BUFFER_LEN;

    offsetVoltage = adcToVoltage(adcAvg);

    char st[15];
    printFloat(offsetVoltage, 2, st);
    LCD_printf("Offset voltage: %sV\n", st);

    printFloat(frontendVoltage(0), 2, st);
    LCD_printf("Min input voltage: %sV\n", st);

    printFloat(frontendVoltage(4096), 2, st);
    LCD_printf("Max input voltage: %sV\n", st);

    flushDisplay();

    while (HAL_GPIO_ReadPin(BTN2_GPIO_Port, BTN2_Pin))
        ;
    HAL_Delay(150);
}

// A little startup splash screen
void splash()
{
    drawBitmap(0, 0, 160, 128, logo);
    setTextColor(BLACK, WHITE);

    printString(" FW compiled: ");
    printString(__DATE__);
    flushDisplay();
    HAL_Delay(2500);
}

// The main UI function
void ui()
{
    clearDisplay();

    if (!HAL_GPIO_ReadPin(BTN1_GPIO_Port, BTN1_Pin) && !HAL_GPIO_ReadPin(BTN3_GPIO_Port, BTN3_Pin))
    {
        autocalFlag = 1;
        if (!HAL_GPIO_ReadPin(BTN2_GPIO_Port, BTN2_Pin)) // Reset if all 3 buttons are pressed at the same time
            HAL_NVIC_SystemReset();
    }

    if (autocalFlag) // Check if we need to calibrate
    {
        autoCal();
        autocalFlag = 0;
    }

    traceScreen(); // Draw the wave
    sideInfo();    // Print info on the side
    settingsBar();

    if (outputFlag)
    {
        if (outputFlag < 3) // If the computer requested data, we send it. This flag is modified in the USB receive handler in usbd_cdc_if.c and in the UART receive handler in scope.c
        {
            outputCSV(outputFlag);
            outputFlag = 0;
        }
        else
        {
            outputTek(outputFlag - 2);
            outputFlag = 0;
        }
    }

    flushDisplay();
}

// This function displays voltage info in the side menu
void sideInfo()
{
    char st[15];
    printFloat(minVoltage, 1, st);
    setTextColor(BLACK, WHITE);
    setCursor(MENUPOS, 1);
    printString("Min:");
    setTextColor(WHITE, BLACK);
    setCursor(MENUPOS, 10);
    LCD_printf("%s\n", st);

    printFloat(maxVoltage, 1, st);
    setTextColor(BLACK, WHITE);
    setCursor(MENUPOS, 21);
    printString("Max:");
    setTextColor(WHITE, BLACK);
    setCursor(MENUPOS, 30);
    LCD_printf("%s\n", st);

    setTextColor(BLACK, WHITE);
    setCursor(MENUPOS, 41);
    printString("Ppk:");
    setTextColor(WHITE, BLACK);
    setCursor(MENUPOS, 51);
    printFloat(maxVoltage - minVoltage, 1, st);
    LCD_printf("%sV\n", st);

    setTextColor(BLACK, WHITE);
    setCursor(MENUPOS, 61);
    printString("Freq");
    setTextColor(WHITE, BLACK);
    setCursor(MENUPOS, 71);

    if (measuredFreq >= 1000)
    {
        if (measuredFreq >= 100000)
            LCD_printf("%d\n", (int)measuredFreq / 1000);
        else
        {
            printFloat(measuredFreq / 1000, 1, st);
            printString(st);
        }
        setCursor(MENUPOS, 81);
        printString("kHz");
    }
    else
    {
        LCD_printf("%d\n", (int)measuredFreq);
        setCursor(MENUPOS, 81);
        printString("Hz");
    }

    setCursor(MENUPOS, 91);
    if (trigged)
    {
        setTextColor(ST7735_GREEN, BLACK);
        printString("Trig");
    }
}

// This function adjusts the settings
void settingsBar()
{
    extern uint8_t topClip, bottomClip;
    static uint8_t sel = 0;
    char st[10];

    // Print top row
    if (topClip || bottomClip)
        setTextColor(ST7735_RED, BLACK);
    else
        setTextColor(WHITE, BLACK);
    setCursor(0, 90);
    printString("Vdiv");

    setTextColor(WHITE, BLACK);
    setCursor(30, 90);
    printString("Trig");

    setCursor(60, 90);
    printString("Slope");

    setCursor(95, 90);
    printString("Atten");

    setCursor(130, 90);
    if (tdiv < 100)
        printString("us/d");
    else
        printString("ms/d");

    // Print bottom row
    if (sel == 0)
    {
        if (topClip || bottomClip)
            setTextColor(ST7735_RED, WHITE);
        else
            setTextColor(BLACK, WHITE);
    }
    else if (topClip || bottomClip)
        setTextColor(ST7735_RED, BLACK);
    else
        setTextColor(WHITE, BLACK);
    setCursor(0, 100);
    printFloat(vdiv, 1, st);
    LCD_printf("%sV\n", st);

    setTextColor(WHITE, BLACK);
    if (sel == 1)
    {
        setTextColor(BLACK, WHITE);
        drawFastHLine(0, (uint16_t)((PIXDIV * YDIV / 2 - 1) - (trigVoltage * PIXDIV / vdiv)), XDIV * PIXDIV, ST7735_RED);
    }
    setCursor(30, 100);
    printFloat(trigVoltage, 1, st);
    LCD_printf("%s\n", st);

    setTextColor(WHITE, BLACK);
    setCursor(60, 100);
    if (sel == 2)
        setTextColor(BLACK, WHITE);
    if (trig == RISING)
        LCD_printf("Rise\n");
    else
        LCD_printf("Fall\n");

    setTextColor(WHITE, BLACK);
    setCursor(95, 100);
    if (sel == 3)
        setTextColor(BLACK, WHITE);
    LCD_printf("%dx\n", atten);

    setTextColor(WHITE, BLACK);
    if (sel == 4)
        setTextColor(BLACK, WHITE);
    setCursor(130, 100);
    if (tdiv < 100)
        LCD_printf("%d\n", (int)tdiv);
    else if (tdiv < 1000)
        LCD_printf("0.%d\n", (int)tdiv / 100);
    else
        LCD_printf("%d\n", (int)tdiv / 1000);

    // Handle buttons
    if (!HAL_GPIO_ReadPin(BTN1_GPIO_Port, BTN1_Pin))
    {
        if (sel == 0) // volts per div
        {
            if (vdiv > 1.0)
                vdiv -= 0.5;
            else if (vdiv > 0.1)
                vdiv -= 0.1;
        }
        else if (sel == 1) // trigger level
        {
            trigVoltage -= 0.1;
        }
        else if (sel == 2) // trigger slope
        {
            trig = FALLING;
        }
        else if (sel == 3) // attenuation
        {
            atten = 1;
        }
        else if (sel == 4) // tdiv
        {
            if (tdiv > 10)
            {
                if (tdiv > 1000)
                    tdiv -= 1000;
                else if (tdiv > 100)
                    tdiv -= 100;
                else if (tdiv > 10)
                    tdiv -= 10;
            }

            sampRate = (PIXDIV * 1000 * 1000) / tdiv;
            sampPer = tdiv / (float)PIXDIV;
            setTimerFreq(sampRate);
        }
        HAL_Delay(150);
    }

    if (!HAL_GPIO_ReadPin(BTN3_GPIO_Port, BTN3_Pin))
    {
        if (sel == 0) // vdiv
        {
            if (vdiv < 1.0)
                vdiv += 0.1;
            else if (vdiv < 9.0)
                vdiv += 0.5;
        }
        else if (sel == 1) // trigLevel
        {
            trigVoltage += 0.1;
        }
        else if (sel == 2) // trigType
        {
            trig = RISING;
        }
        else if (sel == 3) // atten
        {
            atten = 10;
        }
        else if (sel == 4) // tdiv
        {
            if (tdiv >= 1000)
                tdiv += 1000;
            else if (tdiv >= 100)
                tdiv += 100;
            else if (tdiv >= 10)
                tdiv += 10;

            sampRate = (PIXDIV * 1000 * 1000) / tdiv;
            sampPer = tdiv / (float)PIXDIV;
            setTimerFreq(sampRate);
        }
        HAL_Delay(150);
    }

    if (!HAL_GPIO_ReadPin(BTN2_GPIO_Port, BTN2_Pin))
    {
        sel++;
        HAL_Delay(150);
    }
    if (sel > 4)
        sel = 0;
}

// This function dumps a string to either UART or USB port
void outputSerial(char s[], uint8_t o)
{
    switch (o)
    {
    case 1:
        // CDC_Transmit_FS(s, strlen(s));
        HAL_Delay(1);
        break;
    case 2:
        HAL_UART_Transmit(&huart1, (const uint8_t *)s, strlen(s), HAL_MAX_DELAY);
        break;
    default:
        break;
    }
}

// This function dumps the captured waveform as TekScope-compatible CSV data
void outputCSV(uint8_t o)
{
    char st[10];
    char s1[10];
    char buffer[30] = "";

    setCursor(2, 5);
    setTextColor(BLACK, WHITE);
    printString("Sending data");
    if (o == 1)
        printString(" via USB");
    else
        printString(" via UART");
    flushDisplay();

    sprintf(buffer, "\033[2J\033[H\033[3J");
    outputSerial(buffer, o);

    sprintf(buffer, "Model,TekscopeSW\n\r");
    outputSerial(buffer, o);

    sprintf(buffer, "Label,CH1\n\r");
    outputSerial(buffer, o);

    sprintf(buffer, "Waveform Type,ANALOG\n\r");
    outputSerial(buffer, o);

    sprintf(buffer, "Horizontal Units,s\n\r");
    outputSerial(buffer, o);

    printFloat(sampPer, 2, st);
    sprintf(buffer, "Sample Interval,%sE-06\n\r", st);
    outputSerial(buffer, o);

    sprintf(buffer, "Record Length,%d\n\r", BUFFER_LEN);
    outputSerial(buffer, o);

    sprintf(buffer, "Zero Index,%d\n\r", trigPoint);
    outputSerial(buffer, o);
    HAL_Delay(5);

    sprintf(buffer, "Vertical Units,V\n\r");
    outputSerial(buffer, o);

    sprintf(buffer, ",\n\rLabels,\n\r");
    outputSerial(buffer, o);

    sprintf(buffer, "TIME,CH1\n\r");
    outputSerial(buffer, o);

    for (int i = 0; i < BUFFER_LEN; i++)
    {
        float voltage = atten * frontendVoltage(adcBuf[i]);
        printFloat(voltage, 1, st);
        printFloat((float)i * sampPer, 3, s1);
        sprintf(buffer, "%sE-06,%s\n\r", s1, st);
        outputSerial(buffer, o);
    }
}

// This function dumps the captured waveform as raw data, for the TekScope data ingestion app
void outputTek(uint8_t o)
{
    char st[10];
    char buffer[30] = "";

    setCursor(2, 5);
    setTextColor(BLACK, WHITE);
    printString("Sending data");
    if (o == 1)
        printString(" via USB");
    else
        printString(" via UART");
    flushDisplay();

    // transmission begin marker
    sprintf(buffer, "BeginWave!\n\r");
    outputSerial(buffer, o);

    // sample period
    printFloat(sampPer, 2, st);
    sprintf(buffer, "%s\n\r", st);
    outputSerial(buffer, o);

    // number of samples
    if (fast)
        sprintf(buffer, "%d\n\r", BUFFER_LEN / 2);
    else
        sprintf(buffer, "%d\n\r", BUFFER_LEN);
    outputSerial(buffer, o);

    // trigger point in buffer
    if (fast)
        sprintf(buffer, "%d\n\r", 0);
    else
        sprintf(buffer, "%d\n\r", trigPoint);
    outputSerial(buffer, o);

    // frontend offset voltage
    printFloat(offsetVoltage, 4, st);
    sprintf(buffer, "%s\n\r", st);
    outputSerial(buffer, o);

    // attenuation factor of the probe
    sprintf(buffer, "%d\n\r", atten);
    outputSerial(buffer, o);
    HAL_Delay(1);

    // ADC samples
    if (fast)
        for (int i = 0; i < BUFFER_LEN / 2; i++)
        {
            sprintf(buffer, "%d\n\r", adcBuf[i + trigPoint]);
            outputSerial(buffer, o);
        }
    else
        for (int i = 0; i < BUFFER_LEN; i++)
        {
            sprintf(buffer, "%d\n\r", adcBuf[i]);
            outputSerial(buffer, o);
        }
    // transmission end marker
    sprintf(buffer, "SendWaveComplete!\n\r");
    outputSerial(buffer, o);
    sprintf(buffer, "\n\r");
    outputSerial(buffer, o);
}
