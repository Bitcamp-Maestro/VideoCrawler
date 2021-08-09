from bs4 import BeautifulSoup as bs 
from selenium import webdriver as wb 
from pytube import YouTube
from moviepy.editor import *
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
import time
import os 


class VideoModul:
    def VideoCrawler(options):
        "main에서 옵션으로 searchname을 받으면 name으로 링크, 이름, 시간, 조회수 등을 DB에 저장한다."
        driver = wb.Chrome() 
        search_keywords = "+".json(options['keywords'])
        url = ('https://www.youtube.com/results?search_query=%s&sp=EgQQASAB'%(search_keywords))
        driver.get(url)
        body = driver.find_element_by_tag_name('body')
        body.send_keys(Keys.PAGE_DOWN)

        # 스크롤 0.5초마다 한번씩 총 50번 내리기
        for i in range(1,51):
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)

        soup = bs(driver.page_source, 'lxml')
        title =soup.select('a#video-title')
        times = soup.select('span#text')
        video_url = soup.select('a#video-title')

        soup.select('span.style-scope.ytd-video-meta-block')
        view =soup.select('div#metadata-line > span:nth-child(1)')

        title_list = []
        view_list = []
        times_list = []
        url_list=[]
        origin_list = []

        for i, a in zip(range(len(title)), video_url):
            title_list.append(re.sub("([^(가-힣)(ㄱ-ㅎ)(ㅏ-ㅣ)(a-z)(A-Z)])+","", title[i].text.strip()))
            view_list.append(view[i].text.strip())
            times_list.append(times[i].text.strip())
            origin_list.append("Youtube")
            url_list.append('{}{}'.format('https://www.youtube.com',a.get('href')))

        info = {'link':url_list, 'time':times_list, 'title':title_list, 'view':view_list, 'origin':origin_list}
        data = pd.DataFrame(info)
        data.to_csv("%s.csv"%(searchname))


        return data





    def VideoDownload(searchname, storage):
        "searchname 입력받으면 DB 에서 name을 검색해서 링크를 받아와 다운로드 한다."
        data = pd.read_csv('%s.csv'%(searchname))
        for urls, name in zip(data['link'], data['title']):
            url = urls
            yt = YouTube(url)
            vids = yt.streams.all()
            for i in range(len(vids)):
                print(i,'. ',vids[i])
            yt.streams.filter(adaptive=True,
                                file_extension='mp4',
                                only_video=True).order_by('resolution').desc().first().download(storage,'%s.mp4'%(name))
            yt.streams.filter(adaptive=True,
                                file_extension='mp4',
                                only_audio=True).order_by('abr').desc().first().download(storage,'%s.mp3'%(name))

            # 영상 합치기 작업(영상 mp4+ 음성 mp3)
            # videoclip = VideoFileClip("C:/JGBH/Project/final_project/youtube/test.mp4")
            # audioclip = AudioFileClip("C:/JGBH/Project/final_project/youtube/test.mp3")
            # videoclip.audio = audioclip
            # videoclip.write_videofile("test2.mp4")

if __name__ == '__main__':
    storage_path = os.getcwd() + '\\data'
    searchname = input("검색할 단어를 입력하시오 :")
    VideoModul.VideoCrawler(searchname)
    # VideoModul.VideoDownload(searchname, storage_path)