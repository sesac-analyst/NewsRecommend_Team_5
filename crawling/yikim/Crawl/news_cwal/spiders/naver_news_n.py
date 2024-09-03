import scrapy
import pandas as pd
import json
from urllib.parse import urlparse, parse_qs


# 네이버 뉴스
class Naver_News(scrapy.Spider):
    name = "naver_news"
    allowed_domains = ["news.naver.com", "n.news.naver.com", "apis.naver.com"]

    def __init__(self, url_df, *args, **kwargs):
        super(Naver_News, self).__init__(*args, **kwargs)
        self.url_df = url_df
        self.news_data = []

    def start_requests(self):
        for url in self.url_df['url']:
            yield scrapy.Request(url=url, callback=self.parse_article, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': url}, meta={'original_url': url})

    def parse_article(self, response):
        original_url = response.meta.get('original_url')

        # 데이터 추출
        title = response.css('#title_area > span::text').get().strip() if response.css('#title_area > span::text') else None
        sub_title = ' '.join(response.css('strong.media_end_summary::text').getall()).strip()
        date = response.css('.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME::attr(data-date-time)').get()
        media = response.css('.media_end_linked_more_point::text').get().strip() if response.css('.media_end_linked_more_point::text') else None
        reporter = response.css('.media_end_head_journalist_name::text').get().strip() if response.css('.media_end_head_journalist_name::text') else None
        content = ' '.join(response.xpath('//article[@id="dic_area"]//text()[not(ancestor::strong or ancestor::em)]').getall()).strip()

        # 추천 수 가져오기
        recommend_list_raw = response.css('._reactionModule.u_likeit .u_likeit_list_count._count::text').getall()
        recommend_list = [int(recommend.strip()) for recommend in recommend_list_raw if recommend.strip().isdigit()]

        # 댓글 수 가져오기 (현재 댓글 수)
        comment_count = response.css('ul.u_cbox_comment_count li:first-child span.u_cbox_info_txt::text').get()
        if comment_count:
            comment_count = int(comment_count.strip())  # 숫자로 변환
        else:
            comment_count = 0  # 기본값 설정

        # URL에서 oid와 aid 추출
        parsed_url = urlparse(original_url)
        query_params = parse_qs(parsed_url.query)

        if 'oid' in query_params and 'aid' in query_params:
            office_id = query_params['oid'][0]
            article_id = query_params['aid'][0]
        else:
            path_parts = parsed_url.path.split('/')
            office_id = path_parts[-2]
            article_id = path_parts[-1]

        # 댓글 API 요청 URL 동적 생성
        comment_api = f"https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=news&templateId=default_news&pool=cbox5&lang=ko&country=KR&objectId=news{office_id},{article_id}&categoryId=&pageSize=10&indexSize=10&groupId=&listType=OBJECT&pageType=more&sort=FAVORITE&current=1"

        # 댓글 수집을 위한 요청 추가
        yield scrapy.Request(comment_api, callback=self.parse_comment, meta={
            'title': title,
            'sub_title': sub_title,
            'date': date,
            'media': media,
            'reporter': reporter,
            'content': content,
            'recommend_list': recommend_list,
            'comment_count': comment_count,
            'original_url': original_url,
            'office_id': office_id,
            'article_id': article_id
        })

    def parse_comment(self, response):
        # 기사 메타 정보 복원
        title = response.meta['title']
        sub_title = response.meta['sub_title']
        date = response.meta['date']
        media = response.meta['media']
        reporter = response.meta['reporter']
        content = response.meta['content']
        recommend_list = response.meta['recommend_list']
        comment_count = response.meta['comment_count']  
        original_url = response.meta['original_url']

        try:
            # JSON 데이터 파싱
            json_data = json.loads(response.text[10:-2])  # JSONP 응답에서 JSON으로 변환
            reply_l = json_data.get('result', {}).get('list', [])
            reply_count = len(reply_l)  # 모든 댓글의 수

        except json.JSONDecodeError:
            reply_count = 0
            self.logger.error(f"JSON decoding failed for URL: {response.url}")

        # 수집한 데이터를 딕셔너리 형태로 저장
        news_dic = {
            "title": title,
            "sub_title": sub_title,
            "date": date,
            "url": original_url,
            "media": media,
            "reporter": reporter,
            "content": content,
            "recommend_list": recommend_list,
            "comment": comment_count,  
            "reply_count": reply_count  # 댓글 수
        }

        self.news_data.append(news_dic)

    def closed(self, reason):
        save_path = './news_data.csv'
        df = pd.DataFrame(self.news_data)
        df.to_csv(save_path, index=False, encoding='utf-8-sig')
        self.log(f'Data save complete: {save_path}')



