#include "main.h"
#include <intrins.h>

void main()
{
	float IRCF = 11059.2;  // kHz,系统时钟频率,这里先写成常数
	float OPwmF = 3;  //kHz,输出PWM波的目标频率
	BYTE ADCChannel = 6; //使用P1.6作为ADC模块的输入口

	//AUXR = 0xc0;  // 定时器的速度为传统8051的12倍，不分频
	AUXR = 0x00;  // 定时器的速度为传统8051的速度，12分频

	//时钟配置
	WAKE_CLKO = 0x03;
	TMOD = 0x22;  // 将计时器0和计时器1作为8bit自动重载计时器使用

	//TL0 = TH0 = 0xE6;  // 重置计数器0  144Hz
	//TL0 = TH0 = 0xF6;  // 重置计数器0  360hZ
	TL0 = TH0 = 0xFB;  // 重置计数器0  720hZ
	
	TL1 = TH1 = 0x00;  // 重置计数器1

	ET0 = 1;  // 是否启用定时0中断
	EA = 1;  // 是否启用全局中断
	ES = 1;  //是否启动UART中断
	TR0 = 1;  // 是否使能定时器0
	TR1 = 1;  // 是否使能定时器1

	InitPwm();  //初始化PWM模块
	InitUart();  //初始化串口通信模块
	InitADC();  //初始化AD采样模块
	while(1)
	{
		//LowFreqPWM();
		SendADCResult(ADCChannel);
	}
}

//void roundFloatF(float num1,float num2)  //四舍五入取整函数
//{
//}

//void patternAutoSelect()  //根据输入的目标频率自动选择分频与否及计算分频常数k
//{
//}