import pandas as pd
import os

class News:
    def __init__(self, data_path) -> None:
        # DataFrame 불러오기
        self.df = pd.read_csv(data_path).set_index('article_url')
        return
    
    def recommend_articles(self, article_url):
        now_row = self.df.loc[article_url]
        if 'naver' in article_url:
            in_urls = now_row['naver_urls']
            cross_urls = now_row['daum_urls']
        else:
            in_urls = now_row['daum_urls']
            cross_urls = now_row['naver_urls']
        return {'in_urls': in_urls, 'cross_urls': cross_urls}