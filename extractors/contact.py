import re
from collections import defaultdict

from extractors.common import Extractor, get_demo


class ContactExtractor(Extractor):
    def extract(self):
        content = self.content.replace('联系电话', '').replace('电话', '').replace('联系', '').replace('手机号码', '')
        result = defaultdict(set)
        # 姓名+手机号
        p = re.compile(r':?：?\s*(\D{2,3})[:：，,]??\s*\(?（?\s*(1[3-9]\d*)\)?）?')
        contacts = p.findall(content)
        for i, (name, phone) in enumerate(contacts):
            if len(phone) != 11:
                continue
            name = name.strip(',，（(：:、；').strip()
            for ch in (':', '：'):
                try:
                    name = name.split(ch)[1]
                except:
                    pass
            contacts[i] = (name, phone)
            if name:
                result[name].add(phone)
        # TODO:优化
        # 座机
        if not result:
            telephones = re.findall(r'(\d{3,4}-{1,2}\d{7})', content)
            if telephones:
                result[''] = set(x.replace('--', '-') for x in telephones)
        return dict(result)


if __name__ == '__main__':
    page = get_demo()
    e = ContactExtractor(page.text)
    print(e.extract())
