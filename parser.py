from bs4 import BeautifulSoup

from extractors.contact import ContactExtractor


class NoticeParser:
    def __init__(self, html):
        self.html = html

    def parse(self):
        page = BeautifulSoup(self.html)
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
        contacts = self.get_contacts(notice)
        print(notice, requirements, contacts)

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

    def get_contacts(self, notice):
        return ContactExtractor(notice).extract()


if __name__ == '__main__':
    import glob

    for file in glob.glob('data/notices/*.html'):
        html = open(file, encoding='utf8').read()
        p = NoticeParser(html)
        p.parse()
