import socket
import threading
from ClientView import ClientView
import json


class MessageHandler:

    def __init__(self) -> None:
        pass

    def create_msg(self, str : str, num : int = 1, type='json'):
        return json.dumps({'menu' : num, 'data' : str})

    def send(self, sock : socket, send_data : str = ""):
        if send_data == "":
                send_data = input('입력>>')
        sock.send(bytes(send_data.encode()))

    def recv(self, sock):
        while True:
            recv_data = sock.recv(1024).decode()
            print(recv_data)


class VideoCrawlerClientMain:
    IP = 'localhost'
    PORT = 9999

    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.handler = MessageHandler()
        self.view = ClientView()

    def connect(self):
        self.socket.connect((self.IP, self.PORT))
        print('Connected to ', self.IP, self.PORT)

        recv_thread = threading.Thread(target=self.handler.recv, args=(self.socket,))
        recv_thread.start()

    def main(self):
        self.connect()

        while True:
            self.view.show_crawl_menu()
            num = self.view.select_menu_num()

            if num == self.view.OPTION.CRAWLING:
                options = self.view.print_crawl_option()
                msg = self.handler.create_msg(json.dumps(options), num)
                self.handler.send(self.socket, msg)
                
            elif num == self.view.OPTION.SHOW_LIST:
                pass
            elif num == self.view.OPTION.DOWNLOAD:
                pass
            elif num == self.view.OPTION.SEARCH:
                pass
            elif num == self.view.OPTION.EXIT:
                print('종료')
                break
            else:
                print('다시 입력해주세요')
        

if __name__ == '__main__':
    client = VideoCrawlerClientMain()
    client.main()



