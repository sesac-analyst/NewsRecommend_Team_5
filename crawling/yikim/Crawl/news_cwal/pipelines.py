# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import os
import logging


class TutorialPipeline:
    def process_item(self, item, spider):
        return item

class NaverNewsPipeline:
    def open_spider(self, spider):
        self.files = {}
        
        # self.file = open('naver_news.json', 'w', encoding='utf-8')
        # self.file.write('[\n')
        
    def close_spider(self, spider):
        for file in self.files.values():
            file.seek(file.tell() - 2, os.SEEK_END)
            file.write('\n]')
            file.close()
    
    def process_item(self, item, spider):
        date = item['date']
        year = date.split('-')[0]
        filename = f'naver_news_{year}.json'
        
        directory = 'naver_news/'
        
        # 디렉토리가 존재하지 않으면 생성
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        filepath = os.path.join(directory, filename)
        
        if year not in self.files:
            file_exists = os.path.isfile(filepath)
            # self.files[year] = open(f'naver_news_{year}.json', 'w', encoding='utf-8')
            
            try:
                if file_exists:
                    self.files[year] = open(filepath, 'r+', encoding = 'utf-8')
                    self.files[year].seek(0, os.SEEK_END)
                    self.files[year].seek(self.files[year].tell() - 2, os.SEEK_END)
                    self.files[year].write(',\n')
                    
                else:
                    self.files[year] = open(filepath, 'w', encoding='utf-8')
                    self.files[year].write('[\n')
            except Exception as e:
                logging.error(f'file open/close error {filepath} : {e}')
                return item
        try:
            line = json.dumps(dict(item), ensure_ascii=False)
            self.files[year].write(line + ',\n')
            self.files[year].flush()  # 강제 플러시
        except Exception as e:
            logging.error(f'writing error {filepath} : {e}')
        
        return item