from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.news_crwal_spider_selenium import Naver_News, Daum_News
import pandas as pd
import numpy as np
import os
import glob
import logging
from multiprocessing import Process

def set_log(process_id, log_folder):
    
    logger = logging.getLogger(f'process_{process_id}')
    logger.setLevel(logging.DEBUG)
    
    log_file = os.path.join(log_folder, f'error_log_{process_id}.log')
    file_handle = logging.FileHandler(log_file)
    file_handle.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handle.setFormatter(formatter)
    
    logger.addHandler(file_handle)
    
    return logger

def run_spider(spider_class, df, process_id, save_folder, log_folder):
    
    make_logger = set_log(process_id, log_folder)
    reactor._handleSignals = lambda: None
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_class, df=df, process_id=process_id, save_folder=save_folder, make_logger=make_logger)
    process.start()
    

def open_url_df(open_path):
    url_df = pd.read_csv(open_path)
    
    return url_df

def naver_news():
    
    open_path = 'G:\\다른 컴퓨터\\내 노트북\\sasac\\part2\\project\\ref\\naver_url.csv'
    naver_url_df = open_url_df(open_path)

    split_dataframes = np.array_split(naver_url_df, 4)
    save_folder = '../../ref/date/naver_news/naver_crwal_data'
    log_folder = '../../ref/date/naver_news/naver_crwal_data/log'
    os.makedirs(save_folder, exist_ok=True)
    os.makedirs(log_folder, exist_ok=True)
    
    processes = []
    
    for i, df in enumerate(split_dataframes):
        p = Process(target=run_spider, args=(Naver_News, df, i, save_folder, log_folder))
        processes.append(p)
        p.start()
    
    for p in processes:
        p.start()
    

def daum_news():
    
    open_path = '../../ref/data/daum_news'
    
    csv_files = glob.glob(os.path.join(open_path, '*.csv'))
    dataframes = []
    
    for file in csv_files:
        df = pd.read_csv(file)
        dataframes.append(df)
        
    daum_url_df = pd.concat(dataframes, ignore_index=True)

    split_dataframes = np.array_split(daum_url_df, 8)
    save_folder = '../../ref/data/daum_news/daum_crwal_data'
    log_folder = '../../ref/data/daum_news/daum_crwal_data/log'
    os.makedirs(save_folder, exist_ok=True)
    os.makedirs(log_folder, exist_ok=True)
    
    processes = []
    
    for i, df in enumerate(split_dataframes):
        p = Process(target=run_spider, args=(Daum_News, df, i, save_folder, log_folder))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.start()    
        
if __name__ == '__main__':
    
    # naver_news()
    daum_news()