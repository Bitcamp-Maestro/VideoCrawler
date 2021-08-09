import json
from src.Option import Option

class MessageHandlerServer():

    def __init__(self, crawl_manager, db_manager) -> None:
        self.crawl_manager = crawl_manager
        self.db_manager = db_manager
        
    def handle_data(self, data):
        num = data['menu']
        if num == Option.CRAWLING:
            pass
        elif num == Option.SEARCH:
            pass
        elif num == Option.SHOW_LIST:
            pass
        elif num == Option.DOWNLOAD:
            pass
        elif num == Option.EXIT:
            pass
        else:
            print('undefined menu')

    def send(self, group, send_queue):
        while True:
            try:
                recv = send_queue.get()
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
            msg = conn.recv(1024).decode()
            data = json.loads(msg)
            data['data'] = json.loads(data['data'])
            print('recieved : ', data)
            send_queue.put([data, conn, count])
            self.handle_data(data)