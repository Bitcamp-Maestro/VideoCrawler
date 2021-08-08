import socket
import threading
from socketserver import StreamRequestHandler
import json
from VideoCrawlerManager import VideoCrawlerManager
from DBManager import DBManager
from queue import Queue




class RequestHandler():

    def __init__(self) -> None:
        pass
        
    def send(self, group, send_queue):
        while True:
            try:
                recv = send_queue.get()
                if recv == 'Group Changed':
                    print(recv)
                    break

                for conn in group:
                    msg = 'Client' + str(recv[2]) + ' >> ' + str(recv[0]) 
                    if recv[1] != conn: 
                        #client 본인이 보낸 메시지는 받을 필요가 없기 때문에 제외시킴 
                        conn.send(bytes(msg.encode())) 
                    else: 
                        pass 
            except: 
                pass



    def recv(self, conn, count, send_queue):
        while True:
            data = conn.recv(1024).decode()
            print('recieved : ', data)
            send_queue.put([data, conn, count])

class VideoCrawlerServerMain:
    IP = ''
    PORT = 9999
    count = 0

    def __init__(self):
        self.clientList = []
        self.handler = RequestHandler()
        self.vc_manager = VideoCrawlerManager()
        # self.db_manager = DBManager()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.IP, self.PORT))
        self.conn_list = []
        self.send_queue = Queue()
        

    def main(self):
        self.server.listen(10)
        print('server listen...')
        while True:
            self.count = self.count + 1
            conn, addr = self.server.accept()
            self.conn_list.append(conn)
            print('Connected : ' + str(addr))


            if self.count > 1:
                self.send_queue.put('Group Changed')
                send_thread = threading.Thread(target=self.handler.send, args=(self.conn_list, self.send_queue,))
                send_thread.start()

            else:
                send_thread = threading.Thread(target=self.handler.send, args=(self.conn_list, self.send_queue,))
                send_thread.start()
                
            recv_thread =  threading.Thread(target=self.handler.recv, args=(conn, self.count, self.send_queue,))
            recv_thread.start()



if __name__ == '__main__':
    server = VideoCrawlerServerMain()
    server.main()
 


