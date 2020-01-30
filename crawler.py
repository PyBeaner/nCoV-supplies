import json
import time

import scrapy
from scrapy.http import Response

from downloader import NoticeDownloader

START_URL = 'https://www.baidu.com/s?ie=utf-8&mod=1&isbd=1&isid=970fdfc8002e4d9d&wd=%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&pn=0&oq=%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&ct=2097152&ie=utf-8&si=gov.cn&rsv_idx=1&rsv_pq=970fdfc8002e4d9d&rsv_t=5aa9Qix4xgmd4KPWFGmMOzo1fj3wYu7PxB8kv6F7tiSu%2BqZ14dYQNbboZ6A&gpc=stf%3D1580276343%2C1580362743%7Cstftype%3D1&tfflag=1&bs=%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&rsv_sid=undefined&_ss=1&clist=882c6731e60591fc%098812c631e533d725%098812c631e533d725%098812c631e533d725%098812c631e533d725%099e750bf6fc48f135&hsug=%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&f4s=1&csor=8&_cr1=43609'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}


class NoticeSpider(scrapy.Spider):
    name = 'notice-spider'
    start_urls = [START_URL]

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': headers,
    }

    def parse(self, response):
        """
        :type response: Response
        """
        for i, result in enumerate(response.css('div.result .f13')):
            item = result.css('::attr(data-tools)').get()
            item = json.loads(item)
            title = item['title']
            url = item['url']
            host = result.css('.c-showurl ::text').get()
            try:
                host = host.split('/', 1)[0]
            except:
                host = ''
            if 'nor-src-wrap' in host:
                continue  # 忽略百家号的...
            print(title, host)
            NoticeDownloader(url, title, host)  # TODO:download the notice

        next_page = response.css('a.n ::attr(href)').getall()
        next_page = next_page[-1] if next_page else None
        if next_page:
            import random
            time.sleep(random.randint(1, 5))
            # TODO:stop?
            yield response.follow(next_page, self.parse)
