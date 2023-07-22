import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from threading import Timer
from queue import Queue
from collections import Counter
import seaborn as sns
from PyQt6.QtCore import pyqtSignal, QMutexLocker

from app.common.QtSignalBus import QtAppSignalBus
from app.server.MCUStateDict import MCUStateDict


class MCUState(dict):
    def __init__(self):
        super(MCUState, self).__init__()
        self['rms'] = None
        self['period'] = None
        self['frequency'] = None
        self['samplingRate'] = None
        self['workState'] = None
        self['group'] = None
        self['index'] = None
        self['fig'] = None


class paraSignal:
    def __init__(self, source, data_queue):
        self.source = source
        self.data_queue = data_queue
        self.time = []
        self.voltage = []
        self.rms = None
        self.period = None
        self.periodCount = None
        self.frequency = None
        self.samplingRate = None
        self.workState = None
        self.group = None
        self.index = None

    def parasCalculate(self):
        self.time, self.voltage = zip(*((item['Time'], item['adcVoltage']) for item in self.data_queue))
        self.rmsCalculate()
        self.samplingRateCalculate()
        self.periodFreqCalculate()

    def rmsCalculate(self):
        self.rms = np.sqrt(np.mean(np.square(np.array(self.voltage))))

    def periodFreqCalculate(self):
        dft = np.fft.fft(np.array(self.voltage))
        acf = np.fft.ifft(dft * np.conjugate(dft))
        peaks, _ = find_peaks(np.abs(acf))
        peaks = np.insert(peaks, 0, 0)
        peaksDiff = np.diff(peaks).tolist()
        sortedCounts = dict(sorted(Counter(peaksDiff).items(), key=lambda item: item[1], reverse=True))
        maxLikelihoodPeriod, _ = list(sortedCounts.items())[0]
        self.periodCount = maxLikelihoodPeriod
        self.period = maxLikelihoodPeriod / self.samplingRate
        self.frequency = 1 / self.period

    def samplingRateCalculate(self):
        if len(self.time) >= 2:
            timeArrange = self.time[-1] - self.time[0]
            timeArrange = timeArrange.value * 1e-9
            self.samplingRate = len(self.time) / timeArrange

    def print_statistics(self):
        print('Source: {}'.format(self.source))
        print('RMS: {:.6f}V'.format(self.rms))
        if self.period is not None and self.frequency is not None:
            print('Period: {:.6f}s (Frequency: {:.6f}Hz)'.format(self.period, self.frequency))
        else:
            print('Period and frequency cannot be calculated')
        if self.samplingRate is not None:
            print('Sampling rate: {:.6f}Hz'.format(self.samplingRate))
        else:
            print('Sampling rate cannot be calculated')


class dataProcessor:
    def __init__(self, dataProcessQueue):
        self.fig = None
        self.signalObjects = None
        self.dataProcessQueue = dataProcessQueue

    def processData(self):
        while self.dataProcessQueue.dataQueue.full():
            source = self.dataProcessQueue.dataQueue.queue[0]['Source']  # 提取第一行数据确定数据来源
            with QMutexLocker(self.dataProcessQueue.mutex):
                # 实例化Signal参数对象，初始化值，保存队列的快照
                self.signalObjects = paraSignal(source, self.dataProcessQueue.dataQueue.queue)
                self.signalObjects.parasCalculate()
                # self.signalObjects.print_statistics()
                self.plotSignal()
                # 把处理后的数据放入MCUStateDict
                MCUStateDict[source] = self.MCUStateUpdater()
                # self.PyQtSignalEmit()
                self.dataProcessQueue.dataQueue = Queue(maxsize=self.dataProcessQueue.queueLength)  # 清空队列
                pass
            # print('Processed data')
        Timer(2, self.processData).start()  # 递归调用自己，保持连接

    def plotSignal(self):
        df = pd.DataFrame({'Time': range(50 * self.signalObjects.periodCount),
                           'Voltage': self.signalObjects.voltage[:50 * self.signalObjects.periodCount]})
        self.fig, ax = plt.subplots(figsize=(5, 3))
        ax = sns.lineplot(x='Time', y='Voltage', data=df)
        ax.set_xlabel('Time')
        ax.set_ylabel('Voltage (V)')

        # 设置背景透明
        ax.patch.set_alpha(0.0)
        self.fig.patch.set_alpha(0.0)

        # plt.show()

    def MCUStateUpdater(self):
        MCUStateInstance = MCUState()
        MCUStateInstance['group'] = self.signalObjects.group
        MCUStateInstance['index'] = self.signalObjects.index
        MCUStateInstance['rms'] = self.signalObjects.rms
        MCUStateInstance['period'] = self.signalObjects.period
        MCUStateInstance['frequency'] = self.signalObjects.frequency
        MCUStateInstance['samplingRate'] = self.signalObjects.samplingRate
        MCUStateInstance['workState'] = self.signalObjects.workState
        MCUStateInstance['fig'] = self.fig
        return MCUStateInstance
        # QtAppSignalBus.getSignal('1', 'MCUSignals').emit(MCUStateInstance)
