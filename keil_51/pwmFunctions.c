#include "pwm.h"
#include <reg52.h>
void InitPwm()
{
	// PWM配置
	// CMOD B1:CPS0,B2:CPS1,B3:CPS2
	CMOD = 0x04; // PCA模块时钟设置，使用T0的溢出频率，空闲时PCA模块保持运行，禁止PCA计数器溢出中断
	CCON = 0x00; // 停止PCA计数器阵列，初始化，设置完成后于函数最后起动
	CL = 0;
	CH = 0;
	// 控制第一路输出的PWM的占空比

	// CCAP0H = CCAP0L = 0xCC;  //占空比  20
	// CCAP0H = CCAP0L = 0xBF;  //占空比  25
	CCAP0H = CCAP0L = 0xB2; // 占空比  30
	// CCAP0H = CCAP0L = 0xA6;  //占空比  35
	// CCAP0H = CCAP0L = 0x9A;  //占空比  40

	PCAPWM0 = 0x00;
	// CCAPM0 = 0x42;	//控制PCA0输出PWM波形，作为8位PWM，无中断
	// CCAPM0 = 0x53;  //控制PCA0输出PWM波形，作为8位PWM，从高到低可产生中断
	CCAPM0 = 0x73; // 控制PCA0输出PWM波形，作为8位PWM，从高到低与从低到高均可产生中断
	// 控制第二路输出的PWM的占空比
	CCAP1H = CCAP1L = 0x80;
	PCAPWM1 = 0x00;
	CCAPM1 = 0x42; // 控制PCA1输出PWM波形
	CR = 1;		   // 起动PCA模块
}