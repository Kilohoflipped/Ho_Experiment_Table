[TOC]

#  Ho_Experiment_Table

## STC12C5A60S2

### PWM(PCA模块:脉宽调制输出功能)

#### 接线

&emsp;&emsp;此项目使用**P1.3**和**P1.4**分别作为PWM0和PWM1的输出口，相关寄存器为：**AUXR1.6(PCA_P4)**
&emsp;&emsp;若`AUXR1.6(PCA_P4) = 0`，则PWM在**P1.3**和**P1.4**输出
&emsp;&emsp;若`AUXR1.6(PCA_P4) = 1`，则PWM在**P4.2**和**P4.3**输出
&emsp;&emsp;于`main.c`里的`main()`修改**AUXR**

#### 相关代码

&emsp;&emsp;PWM波形的占空比调制与初始化，详见[`InitPwm()`](#InitUart())

### UART(串口通信模块)

#### 接线

&emsp;&emsp;此项目使用串口1作为设备的串口通信模块，即**P3.1**作为TxD发送引脚，**P3.0**作为RxD接收引脚。

#### 相关代码

&emsp;&emsp;UART模块的初始化与波特率设置，详见[`InitUart()`](#InitPwm())

<p>&emsp;&emsp; 这是一个缩进的段落。</p>

### 函数库


#### pwmFunctions.c

##### InitPwm()

```` c
void InitPwm()
	{
		// PWM配置
		//CMOD B1:CPS0,B2:CPS1,B3:CPS2
		CMOD = 0x04;  //使用T0的溢出频率 0b 0 - 010 1
		CCON = 0x00;  //0b00-00
		CL = 0;
		CH = 0;
		//控制第一路输出的PWM的占空比
		PCAPWM0 = 0x00;
		CCAP0H = CCAP0L = 0x80;
		CCAPM0 = 0x42;	//控制PCA0输出PWM波形 
		//控制第二路输出的PWM的占空比
		PCAPWM1 = 0x00;
		CCAP1H = CCAP1L = 0xff;
		CCAPM1 = 0x42;  //控制PCA1输出PWM波形
		CR=1;  //启动PCA模块，输出PWM
	}
````

|CMOD||||||
|:-:|:-:|:-:|:-:|:-:|:-:|
|B7|B6-4|B3|B2|B1|B0|
|**CIDL**||**CPS2**|**CPS1**|**CPS0**|**ECF**|

&emsp;&emsp;**CIDL**:空闲模式下PCA模块是否继续工作。当`CIDL=1`时，空闲模式下PCA模块继续工作，当`CIDL=0`时，空闲模式下PCA模块停止工作。
&emsp;&emsp;**CPS2、CPS1、CPS0**:PCA模块计数器时钟源控制器：如下表

|CPS2|CPS1|CPS0|时钟源|
|:-:|:-:|:-:|:-:|
|0|0|0|系统时钟/12,SYSclk/12|
|0|0|1|系统时钟/2,SYSclk/2|
|***0***|***1***|***0***|***定时器0的溢出脉冲/T0***|
|0|1|1|**ECI(P1.2/P4.1)**脚输入的外部时钟(最大速率SYSclk/2)|
|1|0|0|系统时钟,SYSclk|
|1|0|1|系统时钟/4,SYSclk/4|
|1|1|0|系统时钟/6,SYSclk/6|
|1|1|1|系统时钟/8,SYSclk/8|

&emsp;&emsp;此项目使用**定时器0的溢出脉冲**作为PCA模块的时钟源。
&emsp;&emsp;**ECF**:PCA计数溢出中断控制位。当`ECF=1`时，允许**CCON.1(CF)**位的中断，当`ECF=0`时，禁止**CCON.1(CF)**位的中断。

|CCON|||||
|:-:|:-:|:-:|:-:|:-:|
|B7|B6|B5-2|B1|B0|
|**CF**|**CR**|-|**CCF1**|**CCF0**|

&emsp;&emsp;**CF**:PCA计数器阵列溢出标志位，PCA计数器溢出时，**CF**由硬件置位，如果**CMOD.0(ECF)**置位，则CF标志可以用来产生中断。**CF**可以由硬件或软件置位，但只能用软件清零。
&emsp;&emsp;**CR**:PCA计数器阵列运行控制位。当`CR=1`时，PCA模块起动，`CR=0`时，PCA模块关闭。
&emsp;&emsp;**CCF1**:PCA模块1中断标志，出现匹配或捕获时由硬件置位，必须由软件清零。
&emsp;&emsp;**CCF0**:PCA模块0中断标志，出现匹配或捕获时由硬件置位，必须由软件清零。

&emsp;&emsp;**CL、CH**:用于保存PCA的装载值，实际上相当于PCA模块的计数器，在PCA模块不同的运行模式下，这两个寄存器以不同的方式自增。

|PCAPWMn|||
|:-:|:-:|:-:|:-:|
|B7-2|B1|B0|
|-|EPCnH|EPCnL|

&emsp;&emsp;**EPCnH、ECPnL**:PCA模块作PWM输出时，分别与**CCAPnH、CCAPnL**组成9位数。

&emsp;&emsp;**CCAPnL、CCAPnH**:PCA模块的比较/捕获寄存器，用来存放需要比较/捕获的值。在此项目中，PCA模块用来输出PWM波，故这两个值用来控制PWM波的占空比。
&emsp;&emsp;当`(0,CL)<(EPCnL,CCAPnL)`时，PWM输出0(低电平)。
&emsp;&emsp;当`(0,CL)>(EPCnL,CCAPnL)`时，PWM输出1(高电平)，故PWM波的占空比可以表示为：
$$
\alpha =\left\{ \begin{array}{c}
	1-\frac{CCAPnL}{0xFF}, \left( EPCnL=0 \right)\\
	0,\left( EPCnL=1 \right)\\
\end{array} \right.
$$
&emsp;&emsp;而**CCAPnH**和**EPCnH**是用来更新PWM的，当**CL**的值由0xFF溢出至0x00时，**CCAPnH**的值装载至**CCAPnL**，**EPCnH**的值装载至**EPCnL**，可以实现无干扰的改变占空比，因此想要在运行过程中调整占空比的值请调整**CCAPnH**和**EPCnH**。

|CCAPWMn||||||||
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|B7|B6|B5|B4|B3|B2|B1|B0|
|-|**ECOMn**|**CAPPn**|**CAPNn**|**MATn**|**TOGn**|**PWMn**|**ECCFn**|

&emsp;&emsp;**ECOMn**:当`ECOMn=1`时，允许比较器功能。
&emsp;&emsp;**CAPPn**:当`CAPPn=1`时，允许上升沿捕获。
&emsp;&emsp;**CAPNn**:当`CAPNn=1`时，允许下降沿捕获。
&emsp;&emsp;**MATn**:当`MATn=1`时，且PCA计数值与模块的比较/捕获寄存器(**CCAPnL、CCAPnH**)匹配时，允许置位匹配中断标志位**CCON.n(CCFn)**。
&emsp;&emsp;**TOGn**:当`TOGn=1`时，PCA模块工作在高速输出模式，PCA计数器的值与模块的比较/捕获寄存器(**CCAPnL、CCAPnH**)匹配时，PCA模块的输出引脚将翻转。
&emsp;&emsp;**PWMn**:当`PWMn=1`时，PCA模块工作在PWM输出模式。
&emsp;&emsp;**ECCFn**:当`ECCFn=1`时，使能**CCON.n(CCFn)**中断。
&emsp;&emsp;此项目的**CCAPWM**的值为0x42，即0b01000010，即工作在无中断的8位PWM输出模式。

#### uartFunctions.c

##### InitUart()

```` c
void InitUart()
{
	//串口通信配置初始化
	SCON = 0x50;	//设置为8位数据，波特率可变，使能串行接收
	PCON &= 0x7F;	//波特率不倍速
	AUXR |= 0x40;	//将AUXR的第6位置1，使定时器1工作在1T模式	
	AUXR &= 0xFE;	//将AUXR的第0位置0，使串口模块的时钟来源为计时器1
	TMOD &= 0x0F;	//清零高八位，准备配置定时器1的模式
	TMOD |= 0x20;	//配置定时器1的工作模式八位自动重装
	TL1 = 0xDC;		//修改定时器1溢出率为波特率：9600
	TH1 = 0xDC;		
	ET1 = 0;		//禁止定时器1中断
}
````

|SCON||||||||
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|B7|B6|B5|B4|B3|B2|B1|B0|
|**SM0/FE**|**SM1**|**SM2**|**REN**|**TB8**|**RB8**|**TI**|**RI**|

&emsp;&emsp;**SM0/FE、SM1**:
&emsp;&emsp;当`PCON.6(SMOD0)=1`时，该位用于帧错误检测，当检测到一个无效停止位时，通过UART接收器设置该位。它必须由软件清零
&emsp;&emsp;当`PCON.6(SMOD0)=0`时，该位和**SCON.6(SM1)**一起指定串行通信的工作方式

|SM0|SM1|功能说明|
|:-:|:-:|:-:|
|0|0|同步移位串行寄存器|
|**0**|**1**|**8位UART，波特率可变**|
|1|0|9位UART|
|1|1|9位UART，波特率可变|

&emsp;&emsp;此项目选择的工作方式为8位UART，波特率可变。
&emsp;&emsp;**SM2、TB8、RB8**:本项目所用串口工作方式与这些值无关，介绍略去。
&emsp;&emsp;**REN**:当`REN=1`时，允许串行接受，当`REN=0`时，禁止串行接受。
&emsp;&emsp;**TI、RI**:分别为发送、接收中断请求标志位，当串行发送数据第8位结束后，由内部硬件自动置位，向主机请求中断，响应中断后必须由软件清零。

|PCON|||
|:-:|:-:|:-:|
|B7|B6|B5-B0|
|SMOD|SMOD0|略|

&emsp;&emsp;**SMOD**:波特率选择位。当`SMOD=1`时，波特率加倍，当`SMOD=0`时，波特率不加倍。
&emsp;&emsp;**SMOD0**:
&emsp;&emsp;当`SMOD0=0`时，**SCON.1(SM0/FE)**用于**FE**，即帧错误检测功能，
&emsp;&emsp;当`SMOD0=1`时，**SCON.1(SM0/FE)**用于**SM0**，即与**SCON.6(SM1)**一起指定串行口的工作方式。

|AUXR||||||||
|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
|B7|B6|B5|B4|B3|B2|B1|B0|
|T0x12|T1x12|UART_M0X6|BRTR|S2SMOD|BRTx12|略|S1BRS|

&emsp;&emsp;**Tnx12**:定时器n速度设置位，当`Tnx12=0`时，定时器n是传统8051速度，12分频，工作在12T模式。当`Tnx12=1`时，定时器n是传统8051速度的12倍，不分频，工作在1T模式。
&emsp;&emsp;**UART_M0x6**:串行口模式0(`SCON.7(SM0)=SCON.6(SM1)=0`)的通信速度设置位。当`UART_M0x6=0`时，UART串口的模式0的速度是传统8051单片机的速度，12分频。当`UART_M0x6=1`时，UART串口的模式0的速度是传统8051单片机的速度的6倍，2分频。
&emsp;&emsp;**BRTR**:独立波特率发生器运行控制位，当`BRTR=1`时，允许独立波特率发生器运行。当`BRTR=0`时，禁止独立波特率发生器运行。
&emsp;&emsp;**S2SMOD**:当`S2SMOD=1`时，串口2的波特率加倍。当`S2SMOD=0`时，串口2的波特率不加倍。
&emsp;&emsp;**BRTx12**:独立波特率发生器级数控制位。当`BRTx12=1`时，独立波特率发生器每1个时钟计数一次。当`BRTx12=0`时，独立波特率发生器每12个时钟计数一次。&emsp;&emsp;**S1BRS**:串行口波特率发生器选择器。当`S1BRS=1`时，串行口选择独立波特率发生器作为作为波特率发生器。当`BRTx12=0`时，串行口选择定时器1作为作为波特率发生器。

&emsp;&emsp;**TL1、TH1**:定时器1的计数器，当定时器1该工作在此项目选择的8位自动重装定时器时，当**TL1**的值从0xFF溢出至0x00时，TH1的值自动重装至TL1。这里的赋值是为了改变定时器1的溢出率使得波特率为选定的值，具体数值可由STC-ISP的波特率计算器给出。