import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import threading
import time
from re import search
from collections import deque


class paraSignal:
    def __init__(self, source, dequeLength=30000):
        self.source = source
        self.dequeLength = dequeLength
        self.time = deque(maxlen=dequeLength)
        self.voltage = deque(maxlen=dequeLength)
        self.rms = None
        self.period = None
        self.frequency = None
        self.samplingRate = None

    def parasCalculate(self, data):
        time, voltage = [], []
        for line in data:
            if line:
                timeAbstract = search(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d+', line).group(0)
                voltageAbstract = search(r'\d+\.\d+', line.split(',')[1]).group()
                time.append(pd.to_datetime(timeAbstract, format='%Y-%m-%d %H:%M:%S.%f'))
                voltage.append(float(voltageAbstract))
        self.time = np.append(self.time, np.array(time))
        self.voltage = np.append(self.voltage, np.array(voltage))
        self.rmsCalculate()
        self.samplingRateCalculate()
        self.periodFreqCalculate()

    def rmsCalculate(self):
        self.rms = np.sqrt(np.mean(np.square(self.voltage)))

    def periodFreqCalculate(self):

        dft = np.fft.fft(self.voltage)
        acf = np.fft.ifft(dft * np.conjugate(dft))
        peaks, _ = find_peaks(np.abs(acf))
        T = peaks[0]
        self.period = T * 1 / self.samplingRate
        self.frequency = 1 / self.period

    def samplingRateCalculate(self):
        if len(self.time) >= 2:
            timeDelta = self.time[-1] - self.time[0]
            timeDelta = timeDelta.value * 1e-9
            self.samplingRate = self.time.size / timeDelta

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
    def __init__(self):
        self.signal_objects = {}

    def process_file(self, file_path):
        with open(file_path, 'r') as f:
            data = f.read()
            source = search(r"Source:\s(\d+)", data.split("\n")[0])  # 提取第一行数据确定数据来源
            source = source.group(1)
            if source not in self.signal_objects:
                self.signal_objects[source] = paraSignal(source)  # 实例化Signal参数对象，初始化值
            signal = self.signal_objects[source]
            data = data.split('\n')
            data = data[-30000:]
            signal.parasCalculate(data)
        print('Processed file {}'.format(file_path))
        signal.print_statistics()

    def dataProcess(self, file_path):
        t = threading.Thread(target=self.process_file, args=(file_path,))
        t.start()
        while t.is_alive():
            time.sleep(1)  # Wait until thread finishes processing
        print('All files processed')
