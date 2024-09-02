import requests
from bs4 import BeautifulSoup

import datetime as dt
import calendar
from dateutil import rrule

import pandas as pd
import json
import os

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

def scrap_pages(date_str, sid2):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}
    info_list = []

    # 첫 화면
    init_url = f"https://news.naver.com/breakingnews/section/101/{sid2}?date={date_str}"
    res = requests.get(init_url, headers= headers)
    soup = BeautifulSoup(res.text, 'html.parser') 
    info_list.extend(get_info(soup))

    # 더보기 클릭 후 나오는 기사들
    for i in range(100):
        try:
            p_next = soup.select_one('div.section_latest_article')['data-cursor']
            p_time = calendar.timegm(dt.datetime.now().timetuple())
            next_url = f"https://news.naver.com/section/template/SECTION_ARTICLE_LIST_FOR_LATEST?sid=101&sid2={sid2}&cluid=&pageNo={i}&date={date_str}&next={p_next}&_={p_time}"
        except TypeError:
            return info_list
        
        res = requests.get(next_url, headers=headers)
        content_json = json.loads(res.text)
        res_text = content_json['renderedComponent']['SECTION_ARTICLE_LIST_FOR_LATEST']
        soup = BeautifulSoup(res_text, 'html.parser')

        info_list.extend(get_info(soup))
    
    return info_list


if __name__=='__main__':

    sec2_dict = {'증권': 258, '금융': 259, '부동산': 260, '산업/재계': 261,
                 '글로벌 경제': 262, '경제 일반': 263, '생활경제': 310, '중기/벤처': 771}
    MAX_DATA = int('200,000'.replace(',', ''))
    cnt = 0

    std_date = pd.to_datetime('2024-08-01')

    # 날짜 거꾸로 타고 가기
    while cnt < MAX_DATA:
        # 월별 구분
        std_date = std_date - pd.DateOffset(months=1)
        print(f"{std_date} Month start!")

        # 일별 구분
        for d in range(1, 32):
            try:
                now_date = dt.datetime(std_date.year, std_date.month, d)
            except ValueError:
                break
            print(f"{now_date} Day start!")

            df_day= pd.DataFrame()

            # 특정 날짜에서 기사(하위 카테고리 전체) 가져오기
            date_str = now_date.strftime(r'%Y%m%d')
            for sec2, sid2 in sec2_dict.items():
                info_list = scrap_pages(date_str, sid2)
                df_day_sec2 = pd.DataFrame(info_list, columns=['title', 'press', 'url'])
                df_day_sec2['date'] = now_date.strftime(r'%Y-%m-%d')
                df_day_sec2['sec2'] = sec2

                df_day = pd.concat([df_day, df_day_sec2], ignore_index=True)
                print(f"Sector: {sec2}, {len(df_day_sec2)}개")
            cnt += len(df_day)
        
            # 최초 생성 이후 mode는 append
            if not os.path.exists('news_naver.csv'):
                df_day.to_csv('news_naver.csv', index=False, mode='w')
            else:
                df_day.to_csv('news_naver.csv', index=False, mode='a', header=False)
            print(f"{now_date} Day finished! -> now: {cnt}개")
            break
        print(f"{std_date} Month finished! -> now: {cnt}개")
        break