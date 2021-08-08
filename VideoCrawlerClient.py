import socket
import threading



class VideoCrawlerClientMain:
    IP = 'localhost'
    PORT = 9999

    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        
    def main(self):
        self.socket.connect((self.IP, self.PORT))
        print('Connected to ', self.IP, self.PORT)

        send_thread = threading.Thread(target=self.send, args=(self.socket,))
        recv_thread = threading.Thread(target=self.recv, args=(self.socket,))

        send_thread.start()
        recv_thread.start()

    def send(self, sock):
        while True:
            send_data = bytes(input().encode())
            sock.send(send_data)

    def recv(self, sock):
        while True:
            recv_data = sock.recv(1024).decode()
            print(recv_data)

        

if __name__ == '__main__':
    client = VideoCrawlerClientMain()
    client.main()



