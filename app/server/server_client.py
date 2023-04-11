import socket
from threading import Thread
# from datetime import datetime
from arrow import now


class serverData:

    def __init__(self, serverIP, serverPort):
        self.buffer = None
        self.clientAddress = None
        self.clientSocket = None
        self.serverIP = serverIP  # 设置服务器（PC）的IP地址
        self.serverPort = serverPort  # 设置服务器（PC）的端口
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个TCP套接字

    def startReceive(self):
        self.serverSocket.bind((self.serverIP, self.serverPort))  # 绑定IP地址和端口
        self.serverSocket.listen(1)
        print("Server is listening on {}:{}".format(self.serverIP, self.serverPort))

        while True:
            self.clientSocket, self.clientAddress = self.serverSocket.accept()
            print("Connection from", self.clientAddress)
            clientThread = Thread(target=self.handleClient, args=(self.clientSocket,))
            clientThread.start()

    def handleClient(self, clientSocket):
        while True:
            self.buffer = bytearray()  # 创建一个字节缓冲区以保存接收到的数据
            self.clientSocket = clientSocket
            while True:
                msg = self.clientSocket.recv(3)  # 每次接收1个字节
                if not msg:  # 如果没有接收到数据，跳出循环
                    break
                self.buffer.extend(msg)  # 将接收到的字节添加到缓冲区

                if len(self.buffer) >= 6:  # 当缓冲区长度至少为6个字节时
                    if self.buffer[0] == ord('!') and self.buffer[-2:] == b'\r\n':  # 如果缓冲区的第一个值为b'!'且最后两个字节为'\r\n'
                        channel = self.buffer[1]
                        adcHigh = self.buffer[2]
                        adcLow2 = self.buffer[3] & 0b11  # 只保留低2位
                        adcValue = (adcHigh << 2) | adcLow2  # 将高8位与低2位合并
                        adcResult = adcValue / 1023 * 5  # 计算ADC结果
                        nowData = now()  # 获取当前时间
                        dateTimeStr = nowData.format('YYYY-MM-DD HH:mm:ss.SSSSSSSSSSS')  # 将日期和时间格式化为字符串
                        with open("app/server/data/data{}.txt".format(channel), "a") as file:
                            file.write(dateTimeStr +
                                       "-" +
                                       "Source: {}, ADC : {:.5f}V".format(channel, adcResult) + "\n")
                        self.buffer.clear()  # 清空缓冲区
                    else:
                        self.buffer.clear()
            self.clientSocket.close()  # 关闭客户端连接
