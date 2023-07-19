#ifndef __ADCOPTIONS_H__
#define __ADCOPTIONS_H__

#include "kiloLib.h"

#define ADC_POWER 0x80  //上电
#define ADC_FLAG 0x10 //结束标志
#define ADC_START 0x08  //开始标志
#define ADC_SPEEDLL 0x00
#define ADC_SPEEDL 0x20
#define ADC_SPEEDH 0x40
#define ADC_SPEEDHH 0x60

sfr	ADC_CONTR = 0xBC;  //ADC控制器寄存器
sfr ADC_RES = 0xBD;  //ADC八位高位结果寄存器
sfr ADC_LOW2 = 0xBE;  //ADC两位低位结果寄存器
sfr P1ASF = 0x9D;  //P1管脚功能复用寄存器
sfr AUXR1 = 0xA2;

extern void InitADC();
extern void GetADCResult(BYTE channel);
extern void SendADCResult(BYTE channel);

#endif