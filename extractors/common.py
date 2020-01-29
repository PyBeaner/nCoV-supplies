import random

from bs4 import BeautifulSoup

from database import get_cursor


class Extractor:
    def __init__(self, content='', page=None):
        """
        :type page: BeautifulSoup
        """
        self.content = content.replace(' ', '')
        self.page = page

    def extract(self):
        pass


def get_demo():
    c = get_cursor()
    offset = random.randint(0, 100)
    c.execute('select * from notice_detail where raw_html is not null limit ?,1', (offset,))
    row = c.fetchone()
    return BeautifulSoup(row['raw_html'], features='lxml')
