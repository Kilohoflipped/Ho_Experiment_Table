#ifndef __TIMEOPTIONS_H__
#define __TIMEOPTIONS_H__

#define FOSC 18432000L

#define MODE1T  //工作在1T模式下还是12T模式下
#ifdef MODE1T  //根据工作模式求1ms的计数数量
	#define T1MS (65536-FOSC/1000)
#else 
	#define T1MS (65536-FOSC/1000/12)
#endif

sfr AUXR = 0x8e;
sfr WAKE_CLKO =0x8f; 

#endif