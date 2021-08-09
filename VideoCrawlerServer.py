import socket
import threading
from queue import Queue
from controller.VideoCrawlerManager import VideoCrawlerManager
from controller.DBManager import DBManager
from controller.MessageHandlerServer import MessageHandlerServer
from src.Sqlite_DAO import SqliteDao

class VideoCrawlerServerMain:
    IP = ''
    PORT = 9999
    count = 0

    def __init__(self):
        self.clientList = []
        self.vc_manager = VideoCrawlerManager()
        self.db_manager = DBManager(SqliteDao)
        self.handler = MessageHandlerServer(self.vc_manager, self.db_manager)
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
         

            send_thread = threading.Thread(target=self.handler.send, args=(self.conn_list, self.send_queue,))
            send_thread.start()
                
            recv_thread =  threading.Thread(target=self.handler.recv, args=(conn, self.count, self.send_queue,))
            recv_thread.start()


if __name__ == '__main__':
    server = VideoCrawlerServerMain()
    server.main()
 


