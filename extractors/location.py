import re

from extractors.common import Extractor, get_demo


class LocationExtractor(Extractor):
    remove_spaces = False

    def extract(self):
        content = self.content
        p = re.compile(r'捐?赠?地\s*址：?:?(\S*)')
        locations = p.findall(content)
        result = ''
        if locations:  # TODO:多地址（多公告内容）
            result = locations[0]
        else:
            print('failed to extra location info')
        return result


if __name__ == '__main__':
    page = get_demo()
    e = LocationExtractor(page.text, page)
    e.extract()
