import socket
from threading import Thread
from arrow import now
from threading import Timer
import queue
import pandas as pd


class serverClient:

    def __init__(self, serverIP, serverPort, dataProcessQueue):
        self.timeOut = 10
        self.dataProcessQueue = dataProcessQueue
        self.clientAddress = None
        self.clientSocket = None
        self.connectionStatus = False
        self.serverIP = serverIP  # 设置服务器（PC）的IP地址
        self.serverPort = serverPort  # 设置服务器（PC）的端口
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个TCP套接字
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 设置套接字关闭后的延留保持时间为0
        self.serverSocket.settimeout(self.timeOut)  # 设置套接字的超时时间为self.timeOut

    def startServer(self):
        self.serverSocket.bind((self.serverIP, self.serverPort))  # 绑定IP地址和端口
        self.serverSocket.listen(1)  # 设置只监听一个客户端连接
        print("Server is listening on {}:{}".format(self.serverIP, self.serverPort))
        self.checkConnection()

    def checkConnection(self):
        if not self.connectionStatus:  # 如果没有连接
            try:
                self.clientSocket, self.clientAddress = self.serverSocket.accept()
                self.clientSocket.settimeout(5)  # 设置客户端连接的超时时间为5
                print("Connection from", self.clientAddress)
                self.connectionStatus = True
                self.handleClient()
            except socket.timeout:
                pass

        Timer(1, self.checkConnection).start()  # 递归调用自己，保持连接

    def handleClient(self):
        while self.connectionStatus:
            buffer = bytearray()  # 创建一个字节缓冲区以保存接收到的数据
            while True:
                try:
                    msg = self.clientSocket.recv(3)  # 每次接收1个字节
                    if not msg:  # 如果没有接收到数据，跳出循环
                        break
                    buffer.extend(msg)  # 将接收到的字节添加到缓冲区

                    if len(buffer) >= 6:  # 当缓冲区长度至少为6个字节时
                        if buffer[0] == ord('!') and buffer[-2:] == b'\r\n':  # 如果缓冲区的第一个值为b'!'且最后两个字节为'\r\n'
                            channel = buffer[1]
                            adcHigh = buffer[2]
                            adcLow2 = buffer[3] & 0b11  # 只保留低2位
                            adcValue = (adcHigh << 2) | adcLow2  # 将高8位与低2位合并
                            adcResult = adcValue / 1023 * 5  # 计算ADC结果
                            dataItem = {
                                "Source": channel,
                                "Time": pd.to_datetime(now().datetime),
                                "adcVoltage": adcResult
                            }
                            with self.dataProcessQueue.lock:
                                if self.dataProcessQueue.dataQueue.full():
                                    self.dataProcessQueue.dataQueue.get()
                                self.dataProcessQueue.dataQueue.put(dataItem)  # 将数据加入队列
                            buffer.clear()  # 清空缓冲区
                        else:
                            buffer.clear()
                except socket.timeout:  # 如果clientSocket.recv抛出异常，表示链接丢失
                    break
            self.clientSocket.close()  # 关闭客户端连接
            self.connectionStatus = False
