#ifndef __UARTOPTIONS_H__
#define __UARTOPTIONS_H__

#include "kiloLib.h"
#include <reg52.h>

#define BAUD 9600

// ���崮��У��ģʽ
#define	NONE_PARITY 0 //����У��
#define ODD_PARITY 1  //��У��
#define EVEN_PARITY 2 //żУ��
#define MARK_PARITY 3  //���У��
#define SPACE_PARITY 4  //����У��

#define PARITYBIT EVEN_PARITY //ʹ��żУ��

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