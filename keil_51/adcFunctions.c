#include "adcOptions.h"
#include "kiloLib.h"
#include <intrins.h>

extern void SendData(BYTE msg);
extern void SendString(char *s);

void InitADC()
{
	// ADCģ�����ó�ʼ��
	P1ASF = 0x02;						 // ������ЩIO����ΪAD�������룬�˴�ʹ��P1.6��
	ADC_RES = 0;						 // ��ʼ��AD��������Ĵ���
	ADC_CONTR = ADC_POWER | ADC_SPEEDHH; // ��ADC�����ϵ粢ʹ�ó��������ʹ��P1.6����Ϊģ������
	AUXR1 &= 0xFB;						 // ѡ��ʮλADCת��ֵ�Ĵ洢��ʽ���˴�Ϊ�߰�λ����ADC_RES�Ĵ����У��Ͷ�λ����ADC_LOW2�Ĵ�����
	_nop_();							 // �ȴ�4��nop��ʹ��ADģ���ȶ�
	_nop_();
	_nop_();
	_nop_();
}

void GetADCResult(BYTE channel)
{
	ADC_CONTR |= /* ADC_POWER| ADC_SPEEDHH| */ channel | ADC_START; // ѡ��ͨ���Ų�����ADCת��
	while (!(ADC_CONTR & ADC_FLAG))									// �ȴ�ת����ɣ���־λ��1
	{
	};
	ADC_CONTR &= ~ADC_FLAG; // ���ת����ɱ�־λ
}

void SendADCResult(BYTE channel) // ����ͨ���ź�ת�����
{
	SendData(0x21);		   // ���ͣ�����־���ݿ�ʼ
	SendData(10);		   // �����豸���
	GetADCResult(channel); // ����ADת��
	SendData(ADC_RES);	   // ���͸߰�λ���
	SendData(ADC_LOW2);	   // ���͵Ͷ�λ���
	SendData(0x0a);		   // ���ͻ��з�(LF)����־���ݽ���
}