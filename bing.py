import time

import scrapy
from bs4 import BeautifulSoup, Tag
from scrapy.http import Response
from urllib3.util import parse_url

from downloader import NoticeDownloader

START_URL = 'https://cn.bing.com/search?q=intitle%3a%e6%8e%a5%e5%8f%97+%e6%8d%90%e8%b5%a0+%e5%85%ac%e5%91%8a&filters=ex1%3a%22ez5_18281_18292%22&qs=n&sp=-1&pq=intitle%3a%e6%8e%a5%e5%8f%97+%e6%8d%90%e8%b5%a0+%e5%85%ac%e5%91%8a&sc=1-16&cvid=DA8BBD2C7D6E4550B29C2942A70F25F8&qpvt=intitle%3a%e6%8e%a5%e5%8f%97+%e6%8d%90%e8%b5%a0+%e5%85%ac%e5%91%8a&first=1&FORM=PERE'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
}


class NoticeSpider(scrapy.Spider):
    name = 'bing-spider'
    start_urls = [START_URL]

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': headers,
    }

    def parse(self, response):
        """
        :type response: Response
        """
        duplicate_cnt = 0
        page = BeautifulSoup(response.body, features='lxml')
        for i, result in enumerate(page.find_all('li', class_='b_algo')):
            title_info: Tag = result.find('a')
            url = title_info['href']
            title = title_info.text
            if '公告' not in title:
                print('ignore', title, url)
                continue
            print(title, url)
            host = parse_url(url).host
            nd = NoticeDownloader(url, title, host)
            if nd.get_status() is not None:
                duplicate_cnt += 1
        # if duplicate_cnt == 10:  # TODO
        #     print('Crawling Finished!')
        #     return

        next_page = page.find('a', class_='sb_pagN')
        if next_page:
            import random
            time.sleep(random.randint(1, 5))
            yield response.follow(next_page['href'], self.parse)
