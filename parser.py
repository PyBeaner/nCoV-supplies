from bs4 import BeautifulSoup

from database import get_cursor
from extractors.contact import ContactExtractor
from extractors.date import DateTimeExtractor


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
        requirements = self.extract_requirements(notice)
        contacts = ContactExtractor(notice).extract()
        date = DateTimeExtractor(notice).extract()
        print(requirements, contacts, date)

    # 所需物资
    def extract_requirements(self, notice):
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
    def __init__(self, ):
        pass


if __name__ == '__main__':

    c = get_cursor()
    c.execute('select id,notice_id,raw_html from notice_detail where content is null')
    rows = c.fetchall()
    for row in rows:
        html = row['raw_html']
        p = NoticeParser(html)
        p.parse()
