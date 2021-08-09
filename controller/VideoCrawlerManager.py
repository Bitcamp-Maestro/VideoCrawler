import json
import sys
from .Manager import Manager
from src.videoModule import VideoModul


class VideoCrawlerManager(Manager):
    def __init__(self):
        self.crawler = VideoModul()

    def start_crawling(self, option: str):
        option_dict = json.load(option)
        result = self.crawler.VideoCrawler(option_dict)
        self.result_handler(result, 'start_crawling')

    def start_download(self, option: str):
        option_dict = json.load(option)
        result = self.crawler.download(option_dict)
        self.result_handler(result, 'start_download')
