import re

from extractors.common import Extractor


class ContactExtractor(Extractor):
    def extract(self):
        p = re.compile(r'(\D{2,4})\(?（?\s?(1[3-9]\d{9})\)?）?')
        contacts = p.findall(self.content)
        for i, (name, phone) in enumerate(contacts):
            name = name.strip(',，（(：:').strip()
            contacts[i] = (name, phone)
        # TODO:座机
        return contacts


if __name__ == '__main__':
    content = '''
 各爱心组织、爱心人士：
根据益阳市委市政府和桃江县委县政府的总体部署，桃江县红十字会为积极应对新型冠状病毒感染的肺炎疫情，全力配合做好接收社会各界捐赠工作，现将相关事宜公告如下：

一、接收物资

N95口罩、护目镜、一次性帽子、防护服、一次性手套、一次性医用口罩、医用防护口罩、一次性鞋套、一次性隔离衣、防护面罩、医用外科口罩、体温枪、84消毒液、免洗手消毒液、过氧乙酸、漂白粉。

捐赠接收地点：

桃江县红十字会（桃花江镇建设路69号）

捐赠接收联系人及电话：

刘江晖    13549718234

张彬彬    15197746155

说  明：

各类捐赠物资要求在保质期内，正规企业产品，符合国家质量标准，无污损。

为方便接受捐赠物资，请先行与联系人沟通捐赠意向，得到确认后再行捐赠。

二、接收捐款

户  名：桃江县红十字会

账  号：597672454397

开户行：中国银行桃江劳动支行

说  明：

为方便开具捐赠发票，捐赠时请注明捐赠人单位及联系人和联系电话。

捐款请备注：疫情防控。

感谢社会各界爱心机构、企业、个人伸出援手，与我们一起守望相助、共克时坚，共同打赢这场疫情防控阻击战！
'''
    e = ContactExtractor(content)
    e.extract()
