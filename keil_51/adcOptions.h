#ifndef __ADCOPTIONS_H__
#define __ADCOPTIONS_H__

#include "kiloLib.h"

#define ADC_POWER 0x80  //�ϵ�
#define ADC_FLAG 0x10 //������־
#define ADC_START 0x08  //��ʼ��־
#define ADC_SPEEDLL 0x00
#define ADC_SPEEDL 0x20
#define ADC_SPEEDH 0x40
#define ADC_SPEEDHH 0x60

sfr	ADC_CONTR = 0xBC;  //ADC�������Ĵ���
sfr ADC_RES = 0xBD;  //ADC��λ��λ����Ĵ���
sfr ADC_LOW2 = 0xBE;  //ADC��λ��λ����Ĵ���
sfr P1ASF = 0x9D;  //P1�ܽŹ��ܸ��üĴ���
sfr AUXR1 = 0xA2;

extern void InitADC();
extern void GetADCResult(BYTE channel);
extern void SendADCResult(BYTE channel);

#endif