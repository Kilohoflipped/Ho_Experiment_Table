#include "pwm.h"
#include <reg52.h>
void InitPwm()
{
	// PWM����
	// CMOD B1:CPS0,B2:CPS1,B3:CPS2
	CMOD = 0x04; // PCAģ��ʱ�����ã�ʹ��T0�����Ƶ�ʣ�����ʱPCAģ�鱣�����У���ֹPCA����������ж�
	CCON = 0x00; // ֹͣPCA���������У���ʼ����������ɺ��ں��������
	CL = 0;
	CH = 0;
	// ���Ƶ�һ·�����PWM��ռ�ձ�

	// CCAP0H = CCAP0L = 0xCC;  //ռ�ձ�  20
	// CCAP0H = CCAP0L = 0xBF;  //ռ�ձ�  25
	CCAP0H = CCAP0L = 0xB2; // ռ�ձ�  30
	// CCAP0H = CCAP0L = 0xA6;  //ռ�ձ�  35
	// CCAP0H = CCAP0L = 0x9A;  //ռ�ձ�  40

	PCAPWM0 = 0x00;
	// CCAPM0 = 0x42;	//����PCA0���PWM���Σ���Ϊ8λPWM�����ж�
	// CCAPM0 = 0x53;  //����PCA0���PWM���Σ���Ϊ8λPWM���Ӹߵ��Ϳɲ����ж�
	CCAPM0 = 0x73; // ����PCA0���PWM���Σ���Ϊ8λPWM���Ӹߵ�����ӵ͵��߾��ɲ����ж�
	// ���Ƶڶ�·�����PWM��ռ�ձ�
	CCAP1H = CCAP1L = 0x80;
	PCAPWM1 = 0x00;
	CCAPM1 = 0x42; // ����PCA1���PWM����
	CR = 1;		   // ��PCAģ��
}