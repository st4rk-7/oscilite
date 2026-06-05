#ifndef __WAVE_H
#define __WAVE_H

float adcToVoltage(uint16_t samp);
float frontendVoltage(uint16_t samp);
void traceScreen();
void findTrigger();
void drawGraticule(uint16_t divx, uint16_t divy, uint16_t pix);
void dottedHLine(int x, int y, int l);
void dottedVLine(int x, int y, int l);
void drawTrace(uint16_t buf[], uint16_t trigPoint, uint16_t col);

#endif