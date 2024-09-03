from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.news_crwal_spider_selenium import Naver_News, Daum_News
import pandas as pd
import os
import glob

def open_url_df(open_path):
    url_df = pd.read_csv(open_path)
    
    return url_df


def naver_news():
    reactor._handleSignals = lambda: None
    
    open_path = 'G:\\다른 컴퓨터\\내 노트북\\sasac\\part2\\project\\ref\\naver_url.csv'
    
    naver_url_df = open_url_df(open_path)
    process = CrawlerProcess(get_project_settings())
    process.crawl(Naver_News, df=naver_url_df)
    process.start()
    

def daum_news():
    reactor._handleSignals = lambda: None
    
    open_path = '../../ref/data/daum_news'
    
    csv_files = glob.glob(os.path.join(open_path, '*.csv'))
    dataframes = []
    
    for file in csv_files:
        df = pd.read_csv(file)
        dataframes.append(df)
        
    daum_url_df = pd.concat(dataframes, ignore_index=True)

    process = CrawlerProcess(get_project_settings())
    process.crawl(Daum_News, df=daum_url_df)
    process.start()
        
        
if __name__ == '__main__':
    naver_save_folder = '../../ref/data/naver_news'
    daum_save_folder = '../../ref/data/daum_news'
    os.makedirs(naver_save_folder, exist_ok=True)
    os.makedirs(daum_save_folder, exist_ok=True)
    
    # naver_news()
    daum_news()