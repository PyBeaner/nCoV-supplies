import datetime

from bs4 import BeautifulSoup

from database import get_cursor
from extractors.contact import ContactExtractor
from extractors.date import DateTimeExtractor
from extractors.location import LocationExtractor
from extractors.receiver import ReceiverExtractor
from item import AllItems


class NoticeParser:
    def __init__(self, html):
        self.html = html

    def parse(self):
        page = BeautifulSoup(self.html, features='lxml')
        title = page.title.string.strip() if page.title and page.title.string else ''
        title = '' if title is None else title

        notice_body = None
        for div in page.find_all('div'):
            text = div.get_text()
            if '版权所有' in text:
                continue
            if '物资' not in text:
                continue
            ok = False
            for kw in ('新型', '肺炎', '防疫', '防控', '疫情'):
                if kw in text:
                    ok = True
                    break
            if ok:
                notice_body = div
        if not notice_body:
            print('Failed to extract notice info...', title)
            return
        notice = notice_body.get_text().upper()
        # 物资需求
        demands = self.extract_demands(notice)
        # 联系人信息
        contacts = ContactExtractor(notice).extract()
        # 发布日期
        date = DateTimeExtractor(notice).extract()
        # 接收方
        receiver = ReceiverExtractor(notice, notice_body).extract()
        # 物资捐赠地址
        location = LocationExtractor(notice, notice_body).extract()
        return NoticeParseResult(title, receiver, location, demands, date, contacts)

    # 所需物资
    def extract_demands(self, notice):
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
    def __init__(self, title, receiver, location, demands, published_at, contacts):
        """
        :type published_at: datetime.datetime
        """
        self.title = title
        self.receiver = receiver
        self.location = location
        self.demands = demands
        self.published_at = published_at
        self.contacts = contacts

    def set_notice(self, notice):
        self.notice = notice

    def format(self):
        date = self.published_at.strftime('%Y-%m-%d') if self.published_at else ''
        row = [date, self.receiver, self.location, self.title]

        demands = set([x.name for x in self.demands])
        for item in AllItems:
            if item.name in demands:
                row.append('1')
            else:
                row.append('')
        contact_str = []
        for name, phones in self.contacts.items():
            contact_str.append(name + ":" + "、".join(phones))
        contact_str = '  '.join(contact_str)
        row.append(contact_str)
        url = self.notice['url'] if self.notice else ''
        row.append(url)
        return row


def get_headers():
    result = ['发布日期', '物资需求机构', '捐赠地址', '公告标题']
    for item in AllItems:
        result.append(item.name)
    result.append('联系人/联系方式')
    result.append('来源')
    return result


if __name__ == '__main__':
    # TODO:更新状态
    c = get_cursor()
    c.execute('select id,notice_id,raw_html from notice_detail')
    rows = c.fetchall()
    notice_ids = []
    for row in rows:
        notice_ids.append(row['notice_id'])

    if notice_ids:
        in_sql = 'id in (' + ','.join(['?'] * len(notice_ids)) + ')'
    else:
        in_sql = '1=0'
    c.execute('select id,title,url from notice where ' + in_sql, notice_ids)
    notices = c.fetchall()
    noticeById = {}
    for notice in notices:
        noticeById[notice['id']] = notice

    result = []
    import csv

    f = open('data/demands.csv', 'w', encoding='utf8', newline='')
    f: csv.DictWriter = csv.writer(f)
    f.writerow(get_headers())
    for row in rows:
        html = row['raw_html']
        p = NoticeParser(html)
        r = p.parse()
        if not r:  # TODO
            continue
        notice = noticeById.get(row['notice_id'])
        if notice:
            r.set_notice(notice)
        f.writerow(r.format())
