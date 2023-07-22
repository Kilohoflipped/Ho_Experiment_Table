#include "main.h"
#include <intrins.h>

void main()
{
	float IRCF = 11059.2;  // kHz,ϵͳʱ��Ƶ��,������д�ɳ���
	float OPwmF = 3;  //kHz,���PWM����Ŀ��Ƶ��
	BYTE ADCChannel = 6; //ʹ��P1.6��ΪADCģ��������

	//AUXR = 0xc0;  // ��ʱ�����ٶ�Ϊ��ͳ8051��12��������Ƶ
	AUXR = 0x00;  // ��ʱ�����ٶ�Ϊ��ͳ8051���ٶȣ�12��Ƶ

	//ʱ������
	WAKE_CLKO = 0x03;
	TMOD = 0x22;  // ����ʱ��0�ͼ�ʱ��1��Ϊ8bit�Զ����ؼ�ʱ��ʹ��

	//TL0 = TH0 = 0xE6;  // ���ü�����0  144Hz
	//TL0 = TH0 = 0xF6;  // ���ü�����0  360hZ
	TL0 = TH0 = 0xFB;  // ���ü�����0  720hZ
	
	TL1 = TH1 = 0x00;  // ���ü�����1

	ET0 = 1;  // �Ƿ����ö�ʱ0�ж�
	EA = 1;  // �Ƿ�����ȫ���ж�
	ES = 1;  //�Ƿ�����UART�ж�
	TR0 = 1;  // �Ƿ�ʹ�ܶ�ʱ��0
	TR1 = 1;  // �Ƿ�ʹ�ܶ�ʱ��1

	InitPwm();  //��ʼ��PWMģ��
	InitUart();  //��ʼ������ͨ��ģ��
	InitADC();  //��ʼ��AD����ģ��
	while(1)
	{
		//LowFreqPWM();
		SendADCResult(ADCChannel);
	}
}

//void roundFloatF(float num1,float num2)  //��������ȡ������
//{
//}

//void patternAutoSelect()  //���������Ŀ��Ƶ���Զ�ѡ���Ƶ��񼰼����Ƶ����k
//{
//}