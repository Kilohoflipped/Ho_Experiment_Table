#ifndef __MAIN_H__
#define __MAIN_H__


#include <reg52.h>
#include "kiloLib.h"
#include "timeOptions.h"
#include "adcOptions.h"
#include "uartOptions.h"
#include "pwm.h"

sbit lowPwmOut = P1^3;

extern void LowFreqPWM();

#endif