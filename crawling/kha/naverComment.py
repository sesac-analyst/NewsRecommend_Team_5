import requests
# from bs4 import BeautifulSoup

import datetime as dt
import calendar
# import time
# from dateutil import rrule

# import pandas as pd
# import os
import json
from math import ceil
import copy

from crawling.kha.parameters import params_init, params_more
from utils.saveFile import save_mat2DF
import sys


rq_url = "https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json"


def response2cmt_list(res_js: dict, article_url):
    cmt_raw_list = res_js['result']['commentList']

    cmt_list = []
    for cmt in cmt_raw_list:
        cmt_id = cmt['commentNo']
        cmt_contents = cmt['contents']
        user_id = cmt['userIdNo']
        cmt_reg_date = cmt['regTime']
        cmt_reg_date_gmt = cmt['regTimeGmt']
        cmt_mod_date = cmt['modTime']
        cmt_list.append([article_url, cmt_id, cmt_contents, user_id, cmt_reg_date])
    return cmt_list


def get_naver_comments(article_url, f_name, columns):
    cmt_url = article_url.replace('/article/', '/article/comment/')
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36', "Referer": cmt_url}
    p_time = calendar.timegm(dt.datetime.now().timetuple())

    cmt_list_total = []

    # Get init comments
    # Parameter setting
    p_init = copy.deepcopy(params_init)
    p_init['_'] = p_time
    p_init['objectId'] = "news" + ",".join(cmt_url.split('/')[-2:])

    # Get request results
    response = requests.get(rq_url, headers=headers, params=p_init)
    # soup = BeautifulSoup(response.text, 'html.parser')
    res_js = json.loads(response.text.split('(', 1)[1][:-2])
    cmt_list_total.extend(response2cmt_list(res_js, article_url))


    # Get other comments
    cmt_cnt = res_js['result']['count']
    page_num = ceil(cmt_cnt['comment'] / 20)

    p_more = copy.deepcopy(params_more)
    p_more['objectId'] = "news" + ",".join(cmt_url.split('/')[-2:])

    for page_idx in range(2, page_num+1):
        # Parameter setting
        p_more['_'] = p_time
        p_more['moreParam.prev'] = res_js['result']['morePage']['prev']
        p_more['moreParam.next'] = res_js['result']['morePage']['next']
        p_more['prev'] = cmt_list_total[0][1]
        p_more['current'] = cmt_list_total[-1][1]
        p_more['page'] = page_idx
        p_more['currentPage'] = page_idx-1

        response = requests.get(rq_url, headers=headers, params=p_more)
        # soup = BeautifulSoup(response.text, 'html.parser')
        # print(p_more)
        res_js = json.loads(response.text.split('(', 1)[1][:-2])
        cmt_list_total.extend(response2cmt_list(res_js, article_url))
    
    save_mat2DF(cmt_list_total, columns, f_name)
    return 

if __name__=='__main__':
    # cmt_url = 'https://n.news.naver.com/mnews/article/comment/092/0002300844'
    # cmt_url = 'https://n.news.naver.com/mnews/article/comment/003/0012757566'
    article_url = 'https://n.news.naver.com/mnews/article/003/0012757566'
    file_name = 'naver_IT_comments.csv'

    # cmt_list = get_naver_comments(article_url, file_name)
    # for i, cmt in enumerate(cmt_list):
    #     print(i, cmt)



# def parse_string_to_dict(input_string):
#     # 줄 단위로 분리하여 리스트로 변환
#     lines = input_string.strip().split('\n')
    
#     # 딕셔너리 생성
#     result_dict = {}
    
#     # 각 줄을 순회하며 key-value 쌍으로 분리
#     for line in lines:
#         key, value = line.split(':', 1)  # ':'를 기준으로 split, 최대 1회 split
#         result_dict[key.strip()] = value.strip()  # key, value 공백 제거 후 딕셔너리에 추가
    
#     return result_dict