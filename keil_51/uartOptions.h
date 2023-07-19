#ifndef __UARTOPTIONS_H__
#define __UARTOPTIONS_H__

#include "kiloLib.h"
#include <reg52.h>

#define BAUD 9600

// 定义串口校验模式
#define	NONE_PARITY 0 //禁用校验
#define ODD_PARITY 1  //奇校验
#define EVEN_PARITY 2 //偶校验
#define MARK_PARITY 3  //标记校验
#define SPACE_PARITY 4  //空置校验

#define PARITYBIT EVEN_PARITY //使用偶校验

/*#if (PARITYBIT == NONE_PARITY)
	SCON = 0x50;
#elif (PARITYBIT == ODD_PARITY)||(PARITYBIT == EVEN_PARITY)||(PARITYBIT == MARK_PARITY)
	SCON = 0xda;
#elif (PARITYBIT == SPACE_PARITY)
	SCON = 0xd5;
#endif*/

sbit bit9 = P2^2;

extern void SendString(char *s);
extern void InitUart();
extern void SendData(BYTE msg);
//extern void Uart_Isr() ;
#endif