import re

from bs4 import BeautifulSoup

from extractors.common import Extractor, get_demo


# TODO:暂时通过公告尾部发布日期判断需求方
class ReceiverExtractor(Extractor):
    def extract(self):
        page = self.page
        node: BeautifulSoup
        p = re.compile(r'(\w*)\|2020')
        result = ''
        for node in page.find_all(re.compile(r'span|div|p')):
            text = node.get_text(strip=True, separator='|')
            if '2020' not in text:
                continue
            tmp = p.findall(text)
            if tmp:
                result = tmp[0]
        if len(result) <= 4:
            result = self.extract_v1()
        return result if len(result) > 4 else ''

    def extract_v1(self):
        page = self.page
        result = ''
        most_probably = None
        for node in page.find_all(re.compile(r'span|div|p')):
            text = node.text.strip()
            if len(text) > 30:
                continue
            if '备案' in text:
                continue
            ok = True
            for ch in (':', '：', '接受', '捐赠', '公告', '；', '！','？'):
                if ch in text:
                    ok = False
                    break
            if not ok:
                continue
            maybe = False
            for kw in ['红十字', '医院', '慈善', '健康', '卫生', '指挥部', '商务局']:
                if kw in text:
                    maybe = True
                    break
            if not maybe:
                continue
            result = text
            if '2020' in text:
                most_probably = text.split('2020')[0].strip()
            date_node = node.find_next_sibling()
            if date_node and '2020' in date_node.text:
                most_probably = text
        if most_probably:
            result = most_probably
        if not result:
            p = re.compile(r'户\s*名:|：\s*(\w*)')
            tmp = p.findall(self.content)
            if tmp:
                result = tmp[0]
        result = result.strip()
        return result


if __name__ == '__main__':
    page = get_demo(url='http://hksw.haikou.gov.cn/a/yaowendongtai/zhanhuihuodong/2020/0127/8468.html')
    e = ReceiverExtractor('', page)
    print(e.extract())
