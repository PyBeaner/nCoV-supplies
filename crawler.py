import json

import scrapy
from scrapy.http import Response

from handler import NoticeHandler

START_URL = 'https://www.baidu.com/s?wd=%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&pn=0&oq=%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&ie=utf-8&rsv_idx=1&rsv_pq=d96174b400709c1f&rsv_t=d450%2BFEbA4QKmzZnPLZKtNfrY1Nxg63XGmfP4rOQ6RygFBGok7d6w5xnxd4&gpc=stf%3D1579609750%2C1580214550%7Cstftype%3D1&tfflag=1'
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
            NoticeHandler(url, title, host).download()
        exit()

        next_page = response.css('a.n ::attr(href)').extract_first()
        yield response.follow(next_page, self.parse)
