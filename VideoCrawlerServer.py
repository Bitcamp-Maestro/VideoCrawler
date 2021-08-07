import socket
import threading
from socketserver import StreamRequestHandler
import json
from VideoCrawlerManager import VideoCrawlerManager
from DBManager import DBManager

class RequestHandler(StreamRequestHandler):
    def handle(self):
        c_sock = self.request

        while True:
            try:
                ...

                msg = c_sock.recv(1024).decode('utf-8')
                if msg == "":
                    c_sock.close()
                    print('정상 연결 종료', e)
                    break
                print("수신 : " + msg)
                options = json.loads(msg)
                # c_sock.send(strPacket.encode())               # 바로 재전송
                # print("송신 : " + strPacket)                      # 화면 출력
            except Exception as e:
                c_sock.close()
                print('[Error] 비정상 연결 종료', e)


class VideoCrawlerServerMain:
    IP = ''
    PORT = 9999

    def __init__(self):
        self.clientList = []
        self.handler = RequestHandler()
        # self.server = ThreadingTCPServer((self.IP, self.PORT), self.handler)
        self.vc_manager = VideoCrawlerManager()
        self.db_manager = DBManager()


    def main(self):
        self.server.serve_forever()

#
# def sendAll(msg, exceptSock):
#     for connSock in clientList:
#         if connSock != exceptSock:
#             connSock.send(msg.encode())


class RequestHandler(StreamRequestHandler):
    def handle(self):  # 스레드가 담당하는 메서드
        print("Connection From ", self.client_address)
        connSock = self.request
        # 클라이언트와 연결소켓을 리스트에 저장
        # clientList.append(connSock)
        while True:
            try:
                msg = connSock.recv(1024).decode('utf-8')
                if msg == '':
                    connSock.close()
                    print('{0} 정상 접속 종료'.format(self.client_address))
                    # clientList.remove(connSock)
                    break
                # connSock은 제외한 다른 접속 클라이언트에 전송
                # sendAll(msg=msg, exceptSock=connSock)
                print("{0}으로부터 수신 : {1}".format(
                    self.client_address, msg))
            except Exception as e:
                connSock.close()
                print('{0} 비정상 접속 종료 = {1}'.format(
                    self.client_address, e))
                # clientList.remove(connSock)


