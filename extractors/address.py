import re

from bs4 import BeautifulSoup

from extractors.common import Extractor


class AddressExtractor(Extractor):
    remove_spaces = False

    def extract(self):
        p = re.compile(r'捐?赠?地[址点]：?:?([\w\d()（）、，-]+)')
        result = ''
        for node in self.page.find_all(re.compile(r'span|div|p')):
            text = node.text.strip().replace(' ', '').replace(' ', '')
            if '地址' in text or '地点' in text:
                tmp = p.findall(text)
                if not tmp:
                    continue
                if len(tmp[0]) < 100:
                    result = tmp[0]
        result = result.strip().strip('。')
        return result


class AddressInfo:
    def __init__(self, address):
        self.address = address
        self.result = self.parse()

    def parse(self):
        import cpca
        # TODO:umap
        result = cpca.transform([self.address]).iloc[0]
        return result

    def __getitem__(self, item):
        return self.result[item]


if __name__ == '__main__':
    # page = get_demo()
    html = BeautifulSoup(
        '''<p style="text-indent:43px;text-autospace:ideograph-numeric;line-height:36px"><span style=";font-family:宋体;font-size:21px"><span style="font-family:宋体">地址：</span></span><span style=";font-family:宋体;font-size:21px"><span style="font-family:宋体">文圣区衍水大街</span>38<span style="font-family:宋体">号（区便民服务大厅民政窗口）</span></span></p>''')
    e = AddressExtractor(html.text, html)
    print(e.extract())
