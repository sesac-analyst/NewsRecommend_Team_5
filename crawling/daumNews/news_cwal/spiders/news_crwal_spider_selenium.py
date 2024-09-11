import scrapy
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from urllib.parse import urlparse, parse_qs
import pandas as pd
import re
from datetime import datetime
import time
import random
import os
from tqdm import tqdm

class Naver_News(scrapy.Spider):
    
    name = "naver_news"
    allowed_domains = ["news.naver.com", "n.news.naver.com"]
    
    def __init__(self, df, *args, **kwargs):
        super(Naver_News, self).__init__(*args, **kwargs)
        self.naver_url_df = df
        self.news_data =[]
        

    def start_requests(self):
        for url in self.naver_url_df['url']:
                yield scrapy.Request(url=url, callback=self.parse, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Referer': url}, meta={'original_url': url})
                
        
    def parse(self, response):
        original_url = response.meta.get('original_url')
        
        title = response.css('#title_area > span::text').get()
        title = title.strip() if title else None
        
        
        sub_title_list = response.css('strong.media_end_summary::text').getall()
        sub_title = ' '.join(sub_title_list).strip() if sub_title_list else None
        
        # category = 
        # url = 
        date_str = response.css('.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME::attr(data-date-time)').get()
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        date = date_obj.strftime("%Y-%m-%d")
        
        media = response.css('.media_end_linked_more_point::text').get()
        media = media.strip() if media else None
        
        reporter = response.css('.media_end_head_journalist_name::text').get()
        reporter = reporter.strip() if reporter else None
        
        content_list = response.xpath('//article[@id="dic_area"]//text()[not(ancestor::strong or ancestor::em)]').getall()
        content = ' '.join(content_list).strip() if content_list else None
        content = re.sub(r'\s+', ' ', content) if content else None
        
        # recommend = response.xpath('//*[@id="commentFontGroup"]/div[1]/div/a/span[2]').getall()
        # recommend = recommend.strip() if recommend else None
        
        # comment = response.css('li.u_cbox_count_info::text').getall()
        # comment = comment.strip() if comment else None
        
        comment_count = response.css('ul.u_cbox_comment_count > li:first-child > span.u_cbox_info_txt::text').get()
        comment_count = int(comment_count.strip()) if comment_count else 0  # change to digit

        news_dic = {
            "title" : title,
            "sub_title" : sub_title,
            "date" : date,
            # "category" : category,
            "url" : original_url,
            "media" : media,
            "reporter" : reporter,
            "content" : content,
            # "recommend" : recommend_list,
            "comment" : comment_count
        }
        self.news_data.append(news_dic)
        
        # yield scrapy.Request(meta={'news_dic' : news_dic})
            
    def closed(self, reason):
        save_path = './news_data.csv'
        df = pd.DataFrame(self.news_data)
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        self.log(f'data save complite. : {save_path}') 
        
        
# 다음 뉴스
class Daum_News(scrapy.Spider):
    
    name = "daum_news"
    allowed_domains = ["news.daum.net", "v.daum.net"]

    def __init__(self, df, process_id, save_folder, make_logger, *args, **kwargs):
        super(Daum_News, self).__init__(*args, **kwargs)
        self.daum_url_df = df
        self.process_id = process_id
        self.save_folder = save_folder
        self.make_logger = make_logger
        self.news_data = []
        
        # Selenium WebDriver init
        self.driver = webdriver.Chrome()   #executable_path='chromedriver.exe')  # 크롬 드라이버 경로를 설정(필요시)
        
    def start_requests(self):
        self.pbar = tqdm(total=len(self.daum_url_df), desc=f"Process {self.process_id}")
        for _, row in self.daum_url_df.iterrows():
            url = row['url']
            yield Request(url=url, callback=self.parse, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Referer': url}, meta={
                                        'original_url': url,
                                        'domain': row['domain'],
                                        'category': row['category'],
                                        'sub_category': row['sub_category'],
                                        'date': row['date']
                                        })
                                
    def parse(self, response):
        delay = random.uniform(1.7, 2.1)
        original_url = response.meta['original_url']
        try:
            # pass url to selenium 
            self.driver.get(response.url)
            
            domain = response.meta['domain']
            category = response.meta['category']
            sub_category = response.meta['sub_category']
            date = response.meta['date']
            
            title = response.css('h3.tit_view::text').get()
            title = title.strip() if title else None
            
            sub_title_list = response.css('strong.summary_view::text').getall()
            sub_title = ' '.join(sub_title_list).strip() if sub_title_list else None
            
            media = response.css('#kakaoServiceLogo::text').get()
            media = media.strip() if media else None
            
            reporter = response.css('div.info_view > span.txt_info::text').get()
            reporter = reporter.strip() if reporter else None
            
            content_list = response.css('div.article_view p::text').getall()
            content = ' '.join(content_list).strip() if content_list else None
            content = re.sub(r'\s+', ' ', content) if content else None
            
            time.sleep(delay)  # delay time
            
            recommend_count = 0 
            comment_count = 0 
            
            try:
                # load recommend count
                recommend_elements = self.driver.find_elements(By.CSS_SELECTOR, 'span.jsx-2157231875.🎬_count_label')
                recommend_count = sum(int(elem.text.strip()) for elem in recommend_elements if elem.text.strip().isdigit())
            except Exception as e:
                self.make_logger.debug(f"{original_url}-failed load recommend count: {recommend_count}, {e}")
                recommend_count = 0
            
            try:
                # comments count
                comment_str = self.driver.find_element(By.CSS_SELECTOR, 'span.txt_info em.txt_num').text
                comment_count = int(re.findall(r'\d+', comment_str)[0]) if comment_str else 0
            except Exception as e:
                self.make_logger.debug(f"{original_url}-failed load comments count: {comment_count}, {e}")
                comment_count = 0
                
            news_dic = {
                'domain': domain,
                'category': category,
                'sub_category': sub_category,
                'title': title,
                'sub_title': sub_title,
                'date': date,
                'url': original_url,
                'media': media,
                'reporter': reporter,
                'content': content,
                'recommend': recommend_count,
                'comment': comment_count
            }
            self.pbar.update(1)
            self.news_data.append(news_dic)
            self.make_logger.info(f'Processed URL: {response.url}')
        except Exception as e:
            self.make_logger.error(f'error url : {response.url}, {e}')

    def closed(self, reason):
        # Selenium driver off
        self.driver.quit()
        
        # data save
        save_path = os.path.join(self.save_folder, f'daum_news_data_part_{self.process_id}.csv')
        df = pd.DataFrame(self.news_data)
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        self.make_logger.info(f'Data saved successfully at: {save_path}')
        self.pbar.close()
