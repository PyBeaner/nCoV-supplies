import json

import scrapy
from scrapy.http import Response

from handler import NoticeHandler

START_URL = 'https://www.baidu.com/s?ie=utf-8&mod=1&isbd=1&isid=ba8b41d1009d1115&wd=%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&pn=0&oq=%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&ct=2097152&ie=utf-8&si=gov.cn&rsv_idx=1&rsv_pq=ba8b41d1009d1115&rsv_t=57bch3AAsq4VjGzTKbwtKsjbwNWRlQuKoCrrJuu0eleRQ8lnd0Incj1GDc8&gpc=stf%3D1579658493%2C1580263293%7Cstftype%3D1&bs=%E6%8E%A5%E5%8F%97%20%E6%8D%90%E8%B5%A0%20%E5%85%AC%E5%91%8A&rsv_sid=undefined&_ss=1&clist=&hsug=&f4s=1&csor=8&_cr1=32935'
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