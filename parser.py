import datetime
import os

from bs4 import BeautifulSoup

from database import get_cursor
from extractors.contact import ContactExtractor
from extractors.date import DateTimeExtractor
from item import AllItems


class NoticeParser:
    def __init__(self, html):
        self.html = html

    def parse(self):
        page = BeautifulSoup(self.html, features='lxml')
        title = page.title.string

        notice_body = None
        for div in page.find_all('div'):
            text = div.get_text()
            if '版权所有' in text:
                continue
            if '物资' not in text:
                continue
            for kw in ('新型', '肺炎', '防疫', '防控', '疫情'):
                if kw in text:
                    break
            notice_body = div
        if not notice_body:
            print('Failed to extra notice info...', title)
            return
        notice = notice_body.get_text().upper()
        # 物资需求
        demands = self.extract_demands(notice)
        # 联系人信息
        contacts = ContactExtractor(notice).extract()
        # 发布日期
        date = DateTimeExtractor(notice).extract()
        return NoticeParseResult(demands, date, contacts)

    # 所需物资
    def extract_demands(self, notice):
        from item import AllItems

        result = []
        for item in AllItems:
            found = False
            for keyword in item.keywords:
                if keyword in notice:
                    found = True
                    break
            if found:
                result.append(item)
        return result


class NoticeParseResult:
    def __init__(self, demands, published_at, contacts):
        """

        :type published_at: datetime.datetime
        """
        self.demands = demands
        self.published_at = published_at
        self.contacts = contacts

    def format(self):
        demands = set([x.name for x in self.demands])
        row = []
        for item in AllItems:
            if item.name in demands:
                row.append('1')
            else:
                row.append('')
        contact_str = []
        for name, phones in self.contacts.items():
            contact_str.append(name + ":" + ",".join(phones))
        contact_str = '/'.join(contact_str)
        row.append(contact_str)
        row.append('')  # TODO
        row.append(self.published_at.strftime('%Y-%m-%d') if self.published_at else '')
        return ','.join(row)


def get_headers():
    result = []
    for item in AllItems:
        result.append(item.name)
    result.append('联系人/联系方式')
    result.append('来源')
    result.append('发布日期')
    return ','.join(result)


if __name__ == '__main__':

    c = get_cursor()
    c.execute('select id,notice_id,raw_html from notice_detail where content is null')
    rows = c.fetchall()
    result = []
    csv = open('data/demands.csv', 'w', encoding='utf8')
    csv.write(get_headers() + os.linesep)
    for row in rows:
        html = row['raw_html']
        p = NoticeParser(html)
        r = p.parse()
        csv.write(r.format() + os.linesep)
