from urllib.parse import urlparse, urlencode, quote
import requests
from bs4 import BeautifulSoup
import re 
import os 
import pathlib


'''
노래 제목을 이용해서 song id를 반환한다.
'''

def search_id(title):
    host = "https://www.melon.com/search/total/index.htm?"
    payload = {
        'searchGnbYn' : ['Y'],
        'kkoSpl' :  ['Y'],
        'mwkLogType' : ['T']
    }
    payload['q'] = [title]
    #사용자가 넘겨준 제목을 검색어로 사용함


    url = host + urlencode(payload, doseq=True)
    #노래 제목을 키워드로 검색하여 url을 생성
    r = my_request(url, 'get')
    #header가 붙어 크롤링이 가능할 수 있도록 하는 코드 생성
    bs = BeautifulSoup(r.text,'lxml')
    target = bs.find("div", class_="tb_list d_song_list songTypeOne").find_all("tr")[1].find("button","btn_icon play" )
    target = str(target)
    #크롤링 후 필요한 정보를 사용하기 위한 전처리
    
    p = re.compile("playSong\(\'([0-9]+)\',([0-9]+)\)")
    # 해당 페이지에서 숫자로 된 song id를 찾아온다.
    return p.findall(target)[0][-1]


'''
노래 제목, song id를 이용해서 해당 노래의 가사를 작성한 파일을 저장한다.
'''


def save_lyrics(songid, path='lyrics'):

    url = f"https://www.melon.com/song/detail.htm?songId={songid}"
    r = requests.get(url)
    head = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'}

    r = requests.get(url, headers=head)
    bs = BeautifulSoup(r.text, 'lxml')
    lyrics = BeautifulSoup(str(bs.find("div", id="d_video_summary")).replace("<br/>", "\n"),'lxml').text


    pathlib.Path(f"./{path}").mkdir(parents=True, exist_ok=True)

    title = bs.find("div", class_="song_name").text.replace("곡명", "").strip()
    artist = bs.find("div", class_="artist").text.strip()
    f = open(f"./{path}/{artist}-{title}.txt", 'w', encoding='utf-8')
    f.write(lyrics.strip())
    f.close()
        

'''받은 url에 head 정보를 함께 넘겨주는 함수'''
def my_request(url, method='get'):
        head = {
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0'
    }
        if method=='get':
            return requests.get(url, headers=head)
