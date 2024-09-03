import requests
from bs4 import BeautifulSoup

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

import datetime as dt
import calendar
from dateutil import rrule

import pandas as pd
import json
import os


sec_dict = {'경제': 101, 'IT': 105}
eco_dict = {'증권': 258, '금융': 259, '부동산': 260, '산업/재계': 261,
                '글로벌 경제': 262, '경제 일반': 263, '생활경제': 310, '중기/벤처': 771}
it_dict = {'모바일': 731, '인터넷/SNS': 226, '통신/뉴미디어': 227, 'IT 일반': 230, '보안/해킹': 732, '컴퓨터': 283, '게임/리뷰': 229, '과학 일반': 228}
child_sec_dict = {101: eco_dict, 105: it_dict}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'}


def save_dataframe(df: pd.DataFrame, file_path: str):
    # 최초 생성 이후 mode는 append
    if not os.path.exists(file_path):
        df.to_csv(file_path, index=False, mode='w')
    else:
        df.to_csv(file_path, index=False, mode='a', header=False)
    print(f"Saved in {file_path}")
    return

def get_info(soup:BeautifulSoup):
    info_list = []
    for box in soup.select('ul.sa_list'):
        articles = box.select('div.sa_text')
        # print(len(articles))
        for article in articles:
            # 제목, article_url, cmt_url, 언론사 # 댓글수
            title = article.select_one('strong.sa_text_strong').text
            article_url = article.select_one('a')['href']
            cmt_url = article.select_one('a.sa_text_cmt')['href']
            publisher = article.select_one('div.sa_text_press').text
            # print(title[:10], publisher, article_url)
            info_list.append([title, publisher, article_url, cmt_url])
    return info_list

def scrap_pages(sid1, sid2, date_str):
    info_list = []

    # 첫 화면
    init_url = f"https://news.naver.com/breakingnews/section/{sid1}/{sid2}?date={date_str}"
    # print(init_url)
    res = requests.get(init_url, headers= headers)
    soup = BeautifulSoup(res.text, 'html.parser') 
    info_list.extend(get_info(soup))

    # 더보기 클릭 후 나오는 기사들
    for i in range(100):
        try:
            p_next = soup.select_one('div.section_latest_article')['data-cursor']
            p_time = calendar.timegm(dt.datetime.now().timetuple())
            next_url = f"https://news.naver.com/section/template/SECTION_ARTICLE_LIST_FOR_LATEST?sid={sid1}&sid2={sid2}&cluid=&pageNo={i}&date={date_str}&next={p_next}&_={p_time}"
        except TypeError:
            return info_list
        
        res = requests.get(next_url, headers=headers)
        content_json = json.loads(res.text)
        res_text = content_json['renderedComponent']['SECTION_ARTICLE_LIST_FOR_LATEST']
        soup = BeautifulSoup(res_text, 'html.parser')

        info_list.extend(get_info(soup))
    return info_list

def crawling_day(sector: str, day: dt.datetime) -> int:
    print(f"{day.strftime(r'%Y-%m-%d')} Day start!")

    sid1 = sec_dict[sector]
    df_day= pd.DataFrame()

    date_str = day.strftime(r'%Y%m%d')
    for sec2, sid2 in child_sec_dict[sid1].items():
        info_list = scrap_pages(sid1, sid2, date_str)
        df_day_sec2 = pd.DataFrame(info_list, columns=['title', 'publisher', 'article_url', 'cmt_url'])
        df_day_sec2['category2'] = sec2

        df_day = pd.concat([df_day, df_day_sec2], ignore_index=True)
        print(f"category2: {sec2}, {len(df_day_sec2)}개")

    df_day['publication_date'] = day.strftime(r'%Y-%m-%d')
    df_day['category1'] = sector

    f_path = os.path.join('D:\python_project\sesac02\data', f'news_naver_{sector}.csv')
    save_dataframe(df_day, f_path)

    print(f"{day} Day finished! + {len(df_day)}개")
    return len(df_day)

# 병렬 처리 <- 일별로
def crawling_all(sector, max_data, day_range):
    cnt = 0

    std_date = pd.to_datetime('2024-08-01')
    # 날짜 거꾸로 타고 가기
    while cnt < max_data:
        std_date -= pd.DateOffset(months=1)
        print(f"{std_date.strftime(r'%Y-%m')} Month start!")

        # 병렬 처리 (daily)
        day_list = []
        for d in range(1, day_range):
            try:
                now_date = dt.datetime(std_date.year, std_date.month, d)
                day_list.append(now_date)
            except ValueError:
                break

        # $$$ 병렬 처리
        for day in day_list:
            df_day = crawling_day(sector, day)
            cnt += len(df_day)
            # file save

            print(f"Total: {cnt}개")

        print(f"{std_date.strftime(r'%Y-%m')} Month finished! -> now: {cnt}개")
        print()

    return

def crawling_term_date(sector, start_date="2023-08-01", end_date="2024-07-31"):

    day_list = list(map(lambda x: x.to_pydatetime(), pd.date_range(start=start_date, end=end_date)))
    sector_list = [sector]*len(day_list)

    with ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(crawling_day, sector_list, day_list), total=len(day_list)))

    return


if __name__=='__main__':
    # sec2_dict = {'증권': 258, '금융': 259, '부동산': 260, '산업/재계': 261,
    #              '글로벌 경제': 262, '경제 일반': 263, '생활경제': 310, '중기/벤처': 771}

    # test_params = {'sector': 'IT', 'max_data': 2e5, 'day_range': 35}
    # crawling_all(**test_params)

    # test_params = {'sector': 'IT', 'start_date': "2023-08-01", 'end_date': "2023-08-02"}
    # crawling_term_date(**test_params)

    crawling_term_date(sector='IT')