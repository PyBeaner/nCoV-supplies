from extractors.common import Extractor, get_demo


class TitleExtractor(Extractor):
    def extract(self):
        page = self.page
        import re
        titles = re.findall(r'\S+接[受|收]\S*捐赠\S*公告', page.text)
        titles.sort(key=lambda x: len(x))
        if titles and len(titles[0]) <= 40:
            title = titles[0]
        else:
            title = page.title.string if page.title and page.title.string else ''
        title = title.strip()
        return title


if __name__ == '__main__':
    page = get_demo(url='http://www.lanshan.gov.cn/lanshan/tzgg/202001/dff536b29c964f71b91a16c2532e9744.shtml')
    e = TitleExtractor(page=page)
    print(e.extract())
