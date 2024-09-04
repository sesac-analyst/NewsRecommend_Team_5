from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

import pandas as pd
import json
import os

import time
import calendar
import datetime as dt
from dateutil import rrule


from crawling.kha.naverComment import get_naver_comments
from crawling.kha.naverContent import get_specific_info, save_empty_csv


contents_file_name = 'news_naver_IT_contents.csv'
contents_columns = ['article_url', 'title', 'reg_date', 'publisher', 'author', 'sub_title', 'content']
comments_file_name = 'news_naver_IT_comments.csv'
comments_columns = ['article_url', 'cmt_id', 'cmt_contents', 'user_id', 'cmt_reg_date']


def tpe_func_cmmts(article_url):
    print(f"Scrape in {article_url}")
    get_naver_comments(article_url, comments_file_name, comments_columns)
    return

def tpe_func_contents(article_url):
    print(f"Scrape in {article_url}")
    get_specific_info(article_url, contents_file_name, contents_columns)
    return


f_path = os.path.join('D:\python_project\sesac02\data', 'news_naver_IT_sample.csv')
df = pd.read_csv(f_path)

save_empty_csv(comments_file_name, comments_columns)
save_empty_csv(contents_file_name, contents_columns)

test_num = len(df)
test_num = 3

# 댓글 가져오기
with ThreadPoolExecutor() as executor:
    results = list(tqdm(executor.map(tpe_func_cmmts, df['article_url'][:test_num]), total=test_num))

# 상세 내용 가져오기
with ThreadPoolExecutor() as executor:
    results = list(tqdm(executor.map(tpe_func_contents, df['article_url'][:test_num]), total=test_num))
# contents = get_specific_info(article_url)
# print(contents)