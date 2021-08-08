import json
import sys
from tqdm import tqdm
from Manager import Manager


class VideoCrawler:
    def __init__(self):
        pass

    def crawling(self, option):
        ...
        return 200

    def download(self, option):
        ...
        return 400


class VideoDAOOracle:
    def __init__(self):
        pass

    def update(self):
        pass

    def select(self):
        pass

    def insert(self):
        pass

    def delete(self):
        pass

    def connect(self):
        pass

    pass


class VideoCrawlerManager(Manager):
    def __init__(self):
        self.crawler = VideoCrawler()

    def start_crawling(self, option: str):
        option_dict = json.load(option)
        result = self.crawler.crawling(option_dict)
        self.result_handler(result, 'start_crawling')

    def start_download(self, option: str):
        option_dict = json.load(option)
        result = self.crawler.download(option_dict)
        self.result_handler(result, 'start_download')
