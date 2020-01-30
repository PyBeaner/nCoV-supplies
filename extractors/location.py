import re

from bs4 import BeautifulSoup

from extractors.common import Extractor


class LocationExtractor(Extractor):
    remove_spaces = False

    def extract(self):
        p = re.compile(r'捐?赠?地\s*址：?:?(\S*)')
        result = ''
        for node in self.page.find_all(re.compile(r'span|div|p')):
            if '地' in node.text and '址' in node.text:
                result = p.findall(node.text)[0]
        result = result.strip().strip('。')
        return result


if __name__ == '__main__':
    # page = get_demo()
    html = BeautifulSoup('''
    <p>（2）捐赠请备注：新型肺炎防控</p><p>感谢社会各界爱心企业、爱心人士对抗击新型冠状病毒感染肺炎疫情所给予的关心和大力支持，我们本着公开、透明、高效的原则，将接收的物资和捐款用于疫情防控工作，并接受社会各界的监督。</p><p>捐赠地址：宝鸡市行政中心6号楼F座301室</p><p>联系人：马宗强0917-326147115109173871</p>''')
    e = LocationExtractor(html.text,html)
    print(e.extract())
