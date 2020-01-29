import re

from extractors.common import Extractor, get_demo


# TODO:暂时通过公告尾部发布日期判断需求方
class ReceiverExtractor(Extractor):
    def extract(self):
        page = self.page
        result = ''
        most_probably = None
        for node in page.find_all(re.compile(r'span|div|p')):
            text = node.text.strip()
            for ch in (':', '：', '接受', '捐赠', '公告', ';', '!'):
                if ch in text:
                    continue
            if len(text) > 30:
                continue
            if '备案' in text:
                continue
            maybe = False
            for kw in ['红十字', '医院', '慈善', '部', '健康', '卫生', '局']:
                if kw in node.text:
                    maybe = True
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
            pass
            # with open('tmp.html', 'w', encoding='utf8') as f:
            #     f.write(page.prettify())
            #     import webbrowser
            #     webbrowser.open_new_tab('tmp.html')
        else:
            print(result, page.title.string)
        return result


if __name__ == '__main__':
    page = get_demo()
    e = ReceiverExtractor('', page)
    e.extract()
