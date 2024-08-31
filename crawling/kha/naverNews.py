import requests
from bs4 import BeautifulSoup

import datetime as dt
import calendar
from dateutil import rrule

import pandas as pd
import json

def get_info(soup:BeautifulSoup):
    info_list = []
    for box in soup.select('ul.sa_list'):
        articles = box.select('div.sa_text')
        # print(len(articles))
        for article in articles:
            # 제목, url, 언론사 # 댓글수
            title = article.select_one('strong.sa_text_strong').text
            news_url = article.select_one('a')['href']
            press = article.select_one('div.sa_text_press').text
            # print(title[:10], press, news_url)
            info_list.append([title, press, news_url])
    return info_list

def scrap_pages(date_str, headers):
    info_list = []

    # 첫 화면
    init_url = f"https://news.naver.com/breakingnews/section/101/259?date={date_str}"
    res = requests.get(init_url, headers= headers)
    soup = BeautifulSoup(res.text, 'html.parser') 
    info_list.extend(get_info(soup))

    # 더보기 클릭 후 나오는 기사들
    for i in range(100):
        try:
            p_next = soup.select_one('div.section_latest_article')['data-cursor']
            p_time = calendar.timegm(dt.datetime.now().timetuple())
            next_url = f"https://news.naver.com/section/template/SECTION_ARTICLE_LIST_FOR_LATEST?sid=101&sid2=259&cluid=&pageNo={i}&date={date_str}&next={p_next}&_={p_time}"
        except TypeError:
            return info_list
        
        res = requests.get(next_url, headers=headers)
        content_json = json.loads(res.text)
        res_text = content_json['renderedComponent']['SECTION_ARTICLE_LIST_FOR_LATEST']
        soup = BeautifulSoup(res_text, 'html.parser')

        info_list.extend(get_info(soup))
    
    return info_list

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}

date_str = '20240731'
info_list = scrap_pages(date_str, headers)

for i, row in enumerate(info_list):
    title, press, news_url = row
    print(i, title)
