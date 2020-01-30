import re

from bs4 import BeautifulSoup

from extractors.common import Extractor


class LocationExtractor(Extractor):
    remove_spaces = False

    def extract(self):
        p = re.compile(r'捐?赠?地[址点]：?:?(\S*)')
        result = ''
        for node in self.page.find_all(re.compile(r'span|div|p')):
            text = node.text.strip().replace(' ', '').replace(' ', '')
            if '地址' in text or '地点' in text:
                result = p.findall(text)[0]
        result = result.strip().strip('。')
        return result


if __name__ == '__main__':
    # page = get_demo()
    html = BeautifulSoup(
        '''<p style="text-indent: 2em; text-align: left">地&nbsp;&nbsp;址：霸州市金康东道228号（霸州市卫健局325房间）</p>''')
    e = LocationExtractor(html.text, html)
    print(e.extract())
