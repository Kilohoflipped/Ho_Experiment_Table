import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from re import search
from collections import deque
from threading import Timer
from queue import Queue, Empty
from copy import deepcopy
from collections import Counter


class paraSignal:
    def __init__(self, source, data_queue):
        self.source = source
        self.data_queue = data_queue
        self.time = []
        self.voltage = []
        self.rms = None
        self.period = None
        self.frequency = None
        self.samplingRate = None
        self.parasCalculate()
        self.print_statistics()

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
        self.period = maxLikelihoodPeriod / self.samplingRate
        self.frequency = 1 / self.period

    def samplingRateCalculate(self):
        if len(self.time) >= 2:
            timeArrange = self.time[-1] - self.time[0]
            timeArrange = timeArrange.value * 1e-9
            self.samplingRate = len(self.time) / timeArrange

    def plot_signal(self):
        plt.plot(self.time, self.voltage)
        plt.xlabel('Time')
        plt.ylabel('Voltage')
        plt.title('Signal from source {}'.format(self.source))
        plt.show()

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
        self.signal_objects = None
        self.dataProcessQueue = dataProcessQueue

    def processData(self):
        while self.dataProcessQueue.dataQueue.full():
            source = self.dataProcessQueue.dataQueue.queue[0]['Source']  # 提取第一行数据确定数据来源
            with self.dataProcessQueue.lock:
                # 实例化Signal参数对象，初始化值，保存队列的快照
                self.signal_objects = paraSignal(source, self.dataProcessQueue.dataQueue.queue)
                self.dataProcessQueue.dataQueue = Queue(maxsize=self.dataProcessQueue.queueLength)  # 清空队列
            print('Processed data')
        Timer(2, self.processData).start()  # 递归调用自己，保持连接
