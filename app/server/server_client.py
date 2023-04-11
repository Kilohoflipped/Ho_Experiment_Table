import socket
from threading import Thread
from arrow import now
from threading import Timer


class serverClient:

    def __init__(self, serverIP, serverPort):
        self.timeOut = 5
        self.buffer = None
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
        self.serverSocket.listen(1)
        print("Server is listening on {}:{}".format(self.serverIP, self.serverPort))
        self.check_connection()
        while True:
            self.clientSocket, self.clientAddress = self.serverSocket.accept()
            print("Connection from", self.clientAddress)
            self.handleClient()
            # clientThread = Thread(target=self.handleClient, args=(self.clientSocket,))
            # clientThread.start()

    def check_connection(self):
        if not self.connectionStatus:  # 如果没有连接
            try:
                self.clientSocket, self.clientAddress = self.serverSocket.accept()
                print("Connection from", self.clientAddress)
                self.connectionStatus = True
                self.handleClient()
            except socket.timeout:
                pass

        Timer(self.timeOut, self.check_connection).start()

    def handleClient(self):
        while self.connectionStatus:
            self.buffer = bytearray()  # 创建一个字节缓冲区以保存接收到的数据
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
                        dateTimeStr = nowData.format('Time:YYYY-MM-DD-HH:mm:ss.SSSSSSSSSSS')  # 将日期和时间格式化为字符串
                        with open("app/server/data/dataFrom{}.txt".format(channel), "a") as file:
                            file.write(dateTimeStr +
                                       "|" +
                                       "Source:{}".format(channel) +
                                       "|" +
                                       "ADC:{:.5f}".format(adcResult) +
                                       "\n")
                        self.buffer.clear()  # 清空缓冲区
                    else:
                        self.buffer.clear()
            self.clientSocket.close()  # 关闭客户端连接
