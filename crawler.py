import json
import time

import scrapy
from scrapy.http import Response

from downloader import NoticeDownloader

# START_URL = 'https://www.baidu.com/s?ie=utf-8&mod=1&isbd=1&isid=bc2f909300079a0e&ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&oq=%25E6%258E%25A5%25E6%2594%25B6%2520%25E6%258D%2590%25E8%25B5%25A0%2520%25E5%2585%25AC%25E5%2591%258A&rsv_pq=eded3efd00091080&rsv_t=9ef98hp0HSiUm0bNbdA84SEEpwePky%2BBs%2FjCdnuez7JYqJgE%2FgZJeXl0%2Ff4&rqlang=cn&rsv_enter=0&rsv_dl=tb&inputT=14413&si=gov.cn&ct=2097152&gpc=stf%3D1580299698%2C1580386098%7Cstftype%3D1&bs=%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&rsv_sid=undefined&_ss=1&clist=8812c631e533d725%098812c631e533d725&hsug=&f4s=1&csor=2&_cr1=42814'
START_URL = 'https://www.baidu.com/s?wd=intitle%3A%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&pn=0&oq=intitle%3A%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&ie=utf-8&rsv_idx=1&rsv_pq=a66d45cd000af21b&rsv_t=ac81QnzkqTYduFYQM8Oh8RaNGp9M1k9rLODvtWz877oIdASVx4KAsEtls0A&gpc=stf%3D1580375273%2C1580461673%7Cstftype%3D1&tfflag=1'
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
        duplicate_cnt = 0
        for i, result in enumerate(response.css('div.result .f13')):
            item = result.css('::attr(data-tools)').get()
            if not item:
                continue
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
            nd = NoticeDownloader(url, title, host)
            if nd.get_status() is not None:
                duplicate_cnt += 1
        if duplicate_cnt == 10:
            print('Crawling Finished!')
            return

        next_page = response.css('a.n ::attr(href)').getall()
        next_page = next_page[-1] if next_page else None
        if next_page:
            import random
            time.sleep(random.randint(1, 5))
            yield response.follow(next_page, self.parse)
