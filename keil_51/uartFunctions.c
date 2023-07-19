#include "timeOptions.h"
#include "uartOptions.h"
#include "kiloLib.h"
#include <reg52.h>

void SendData(BYTE msg)
{
	SBUF = msg;		// 向缓存寄存器里面装载消息
	while(TI==0);  	// 等待上一次的数据被发送
	TI = 0;				// 中断标志位清零
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
	//串口通信配置初始化
	SCON = 0x50;
	PCON |= 0x80;
	AUXR |= 0x40;
	AUXR &= 0xFE;
	TMOD &= 0x0F; //清零高八位，准备配置定时器1的模式
	TMOD |= 0x20; //将高八位控制定时器1的寄存器值设置为0b0010，即8bit自动重装定时器 
	TL1 = 0xFD;  //设置波特率为9600，此时使用计时器1的溢出频率4
	TH1 = 0xFD;
	ET1 = 0;
}

/*void Uart_Isr() interrupt 4 using 1
{
	if(RI)
	{
		RI = 0;		//清除中断标志
	}
	
	if (TI)
	{
		TI= 0;
		uartBuzy = 0;
	}
}*/