import pandas as pd
import ast
import os

class News:
    def __init__(self, data_path) -> None:
        # DataFrame 불러오기
        self.df = pd.read_csv(data_path).set_index('article_url')
        return
    
    def recommend_articles(self, article_url):
        now_row = self.df.loc[article_url]
        if 'naver' in article_url:
            in_urls = now_row['n_sim']
            cross_urls = now_row['d_sim']
        else:
            in_urls = now_row['d_sim']
            cross_urls = now_row['n_sim']

        return {'in_urls': list(ast.literal_eval(in_urls).keys()), 'cross_urls': list(ast.literal_eval(cross_urls).keys())}