import re

from extractors.common import Extractor, get_demo


class AddressExtractor(Extractor):
    remove_spaces = False

    def extract(self):
        p = re.compile(r'捐?赠?地[址点]：?:?([\w\d()（）、，-]+)')  # TODO:换行
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
    page = get_demo(url='http://www.ya.gov.cn/zwgk/tzgg/gggs/202001/t20200130_1470375.htm')
    e = AddressExtractor(page=page)
    print(e.extract())
