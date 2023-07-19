#include "timeOptions.h"
#include "uartOptions.h"
#include "kiloLib.h"
#include <reg52.h>

void SendData(BYTE msg)
{
	SBUF = msg;		// �򻺴�Ĵ�������װ����Ϣ
	while(TI==0);  	// �ȴ���һ�ε����ݱ�����
	TI = 0;				// �жϱ�־λ����
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
	//����ͨ�����ó�ʼ��
	SCON = 0x50;
	PCON |= 0x80;
	AUXR |= 0x40;
	AUXR &= 0xFE;
	TMOD &= 0x0F; //����߰�λ��׼�����ö�ʱ��1��ģʽ
	TMOD |= 0x20; //���߰�λ���ƶ�ʱ��1�ļĴ���ֵ����Ϊ0b0010����8bit�Զ���װ��ʱ�� 
	TL1 = 0xFD;  //���ò�����Ϊ9600����ʱʹ�ü�ʱ��1�����Ƶ��4
	TH1 = 0xFD;
	ET1 = 0;
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