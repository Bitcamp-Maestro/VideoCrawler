import json
from controller.DBManager import DBManager
from controller.VideoCrawlerManager import VideoCrawlerManager
from src.Option import Option


class MessageHandlerServer():

    def __init__(self, crawl_manager : VideoCrawlerManager, db_manager : DBManager) -> None:
        self.crawl_manager = crawl_manager
        self.db_manager = db_manager
        
    def handle_data(self, data):
        num = data['menu']
        if num == Option.CRAWLING:
            result = self.crawl_manager.start_crawling(data['data'])
            print(result)
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
                    conn.send(bytes(msg.encode())) 
            except: 
                pass

    def recv(self, conn, count, send_queue):
        while True:
            msg = conn.recv(1024).decode()
            data = json.loads(msg)
            data['data'] = json.loads(data['data'])
            print('recieved : ', data)
            send_queue.put([data, conn, count])
            self.handle_data(data, send_queue)