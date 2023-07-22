#include "timeOptions.h"
#include "uartOptions.h"
#include "kiloLib.h"
#include <reg52.h>

void SendData(BYTE msg)
{
	SBUF = msg; // �򻺴�Ĵ�������װ����Ϣ
	while (TI == 0)
		;	// �ȴ���һ�ε����ݱ�����
	TI = 0; // �жϱ�־λ����
}

void SendString(char *s)
{
	while (*s)
	{
		SendData(*s++);
	}
}

void InitUart()
{
	// ����ͨ�����ó�ʼ��
	PCON |= 0x80; // ʹ�ܲ����ʱ���λSMOD
	SCON = 0x50;  // 8λ����,�ɱ䲨����
	AUXR |= 0x40; // ��ʱ��1ʱ��1Tģʽ
	AUXR &= 0xFE; // ����1ѡ��ʱ��1Ϊ�����ʷ�����
	TMOD &= 0x0F; // ����߰�λ��׼�����ö�ʱ��1��ģʽ
	TMOD |= 0x20; // ���߰�λ���ƶ�ʱ��1�ļĴ���ֵ����Ϊ0b0010����8bit�Զ���װ��ʱ��
	TL1 = 0xFD;	  // ���ö�ʱ��ʼֵ�����ò�����Ϊ230400����ʱʹ�ü�ʱ��1�����Ƶ��
	TH1 = 0xFD;	  // ���ö�ʱ����ֵ
	ET1 = 0;	  // ��ֹ��ʱ���ж�
	TR1 = 1;	  // ��ʱ��1��ʼ��ʱ
}

/*void Uart_Isr() interrupt 4 using 1
{
	if(RI)
	{
		RI = 0;		//����жϱ�־
	}

	if (TI)
	{
		TI= 0;
		uartBuzy = 0;
	}
}*/