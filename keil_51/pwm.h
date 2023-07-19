#ifndef __PWM_H__
#define __PWM_H__

//��ʼ��PWMģ����ؼĴ���
sfr CCON = 0xD8;				//PCA�������Ĵ���
sbit CCF0 = CCON^0;
sbit CCF1 = CCON^1;
sbit CR = CCON^6;
sbit CF = CCON^7;
sfr CMOD = 0xD9;
sfr CL = 0xE9;
sfr CH = 0xF9;
sfr CCAPM0 = 0xDA;
sfr CCAP0L = 0xEA;
sfr CCAP0H = 0xFA;
sfr CCAPM1 = 0xDB;
sfr CCAP1L = 0xEB;
sfr CCAP1H = 0xFB;
sfr PCAPWM0 = 0xf2;
sfr PCAPWM1 = 0xf3;

extern void InitPwm();

#endif