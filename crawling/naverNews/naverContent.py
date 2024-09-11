import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

from utils.saveFile import save_mat2DF

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"}


def save_empty_csv(f_name, columns):
    save_mat2DF([], columns, f_name)
    return

def get_specific_info(article_url, f_name, columns):
    res = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    title = soup.select_one("h2.media_end_head_headline").get_text()
    reg_date = soup.select_one(".media_end_head_info_datestamp").get_text()[4:15]
    publisher = soup.find('img', class_='media_end_head_top_logo_img').get('alt')
    author = soup.select_one("em.media_end_head_journalist_name").get_text().split()[0]

    sub_title = ''
    sub_title_tag = soup.select_one("strong.media_end_summary")
    if sub_title_tag:
        sub_title = sub_title_tag.get_text(separator=' ')
        sub_title_tag.extract()
    content = soup.select_one("div#newsct_article").get_text(separator=' ').strip()
    content = re.sub(r'\n\s*\n[\n\s]+', r'\n\n', content)

    # recommand_list_raw = soup.find(class_ = "_reactionModule u_likeit").find_all(class_ = "u_likeit_list_count _count")
    # recommend_list = [int(i.get_text()) for i in recommand_list_raw]
    # print(recommend_list)

    info_list = [[article_url, title, reg_date, publisher, author, sub_title, content]]
    save_mat2DF(info_list, columns, f_name)

    return 


if __name__=='__main__':
    article_url = "https://n.news.naver.com/mnews/article/092/0002300844"
    # res = get_specific_info(article_url)
    # print(res)