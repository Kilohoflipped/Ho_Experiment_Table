#ifndef __TIMEOPTIONS_H__
#define __TIMEOPTIONS_H__

#define FOSC 18432000L

#define MODE1T  //������1Tģʽ�»���12Tģʽ��
#ifdef MODE1T  //���ݹ���ģʽ��1ms�ļ�������
	#define T1MS (65536-FOSC/1000)
#else 
	#define T1MS (65536-FOSC/1000/12)
#endif

sfr AUXR = 0x8e;
sfr WAKE_CLKO =0x8f; 

#endif