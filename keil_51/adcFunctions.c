#include "adcOptions.h"
#include "kiloLib.h"
#include <intrins.h>

extern void SendData(BYTE msg);
extern void SendString(char *s);

void InitADC()
{
	// ADC模块配置初始化
	P1ASF = 0x02;						 // 配置哪些IO口作为AD采样输入，此处使用P1.6口
	ADC_RES = 0;						 // 初始化AD采样结果寄存器
	ADC_CONTR = ADC_POWER | ADC_SPEEDHH; // 给ADC采样上电并使用超快采样，使用P1.6口作为模拟输入
	AUXR1 &= 0xFB;						 // 选择十位ADC转换值的存储方式，此处为高八位放在ADC_RES寄存器中，低二位放在ADC_LOW2寄存器中
	_nop_();							 // 等待4个nop，使得AD模块稳定
	_nop_();
	_nop_();
	_nop_();
}

void GetADCResult(BYTE channel)
{
	ADC_CONTR |= /* ADC_POWER| ADC_SPEEDHH| */ channel | ADC_START; // 选择通道号并启动ADC转换
	while (!(ADC_CONTR & ADC_FLAG))									// 等待转换完成，标志位置1
	{
	};
	ADC_CONTR &= ~ADC_FLAG; // 清除转换完成标志位
}

void SendADCResult(BYTE channel) // 发送通道号和转换结果
{
	SendData(0x21);		   // 发送！，标志数据开始
	SendData(10);		   // 发送设备编号
	GetADCResult(channel); // 进行AD转换
	SendData(ADC_RES);	   // 发送高八位结果
	SendData(ADC_LOW2);	   // 发送低二位结果
	SendData(0x0a);		   // 发送换行符(LF)，标志数据结束
}