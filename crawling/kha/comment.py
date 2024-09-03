import requests
from bs4 import BeautifulSoup

import datetime as dt
from dateutil import rrule

import pandas as pd
import json
import os

import time
import calendar
from math import ceil

from parameters import params_init, params_more


cmt_url = 'https://n.news.naver.com/mnews/article/comment/092/0002300844'
cmt_url = 'https://n.news.naver.com/mnews/article/comment/003/0012757566'

rq_url = "https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
           "Referer": cmt_url}
p_time = calendar.timegm(dt.datetime.now().timetuple())

# Get init comments
# Parameter setting
params_init['_'] = p_time
params_init['objectId'] = "news" + ",".join(cmt_url.split('/')[-2:])

# Get request results
response = requests.get(rq_url, headers=headers, params=params_init)
soup = BeautifulSoup(response.text, 'html.parser')
res_text = response.text

res_js = json.loads(res_text.split('(', 1)[1][:-2])

cmt_list = []
cmt_raw_list = res_js['result']['commentList']
for cmt in cmt_raw_list:
    cmt_id = cmt['commentNo']
    cmt_contents = cmt['contents']
    user_id = cmt['userIdNo']
    cmt_reg_date = cmt['regTime']
    cmt_reg_date_gmt = cmt['regTimeGmt']
    cmt_mod_date = cmt['modTime']
    cmt_list.append([cmt_id, cmt_contents, user_id, cmt_reg_date])

cmt_cnt = res_js['result']['count']
print(cmt_cnt)


page_num = ceil(cmt_cnt['comment'] / 20)
for page_idx in range(2, page_num+1):

    mp_prev = res_js['result']['morePage']['prev']
    mp_next = res_js['result']['morePage']['next']
    p_current = cmt_list[-1][0]
    p_prev = cmt_list[0][0]

    # Get more comments
    params_more['objectId'] = "news" + ",".join(cmt_url.split('/')[-2:])
    params_more['_'] = p_time
    params_more['moreParam.prev'] = mp_prev
    params_more['moreParam.next'] = mp_next
    params_more['current'] = p_current
    params_more['current'] = p_prev
    params_more['page'] = page_idx
    params_more['currentPage'] = page_idx-1

    response = requests.get(rq_url, headers=headers, params=params_more)
    soup = BeautifulSoup(response.text, 'html.parser')
    res_text = response.text

    res_js = json.loads(res_text.split('(', 1)[1][:-2])

    cmt_raw_list = res_js['result']['commentList']
    for cmt in cmt_raw_list:
        cmt_id = cmt['commentNo']
        cmt_contents = cmt['contents']
        user_id = cmt['userIdNo']
        cmt_reg_date = cmt['regTime']
        cmt_reg_date_gmt = cmt['regTimeGmt']
        cmt_mod_date = cmt['modTime']
        cmt_list.append([cmt_id, cmt_contents, user_id, cmt_reg_date])


for i, cmt in enumerate(cmt_list):
    print(i, cmt)
