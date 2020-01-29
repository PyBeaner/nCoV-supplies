# @see https://shimo.im/docs/tcXtdyK9cVhP8cRh/read
class Item:
    def __init__(self, name, keywords=None):
        self.name = name
        self.keywords = [name] if not keywords else keywords
        self.keywords = set(self.keywords + [name])

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


# 口罩类
N95 = Item('N95口罩', ['N95防护口罩', '防护口罩'])
医用外科口罩 = Item('医用外科口罩', ['外科口罩'])
一次性医用口罩 = Item('一次性医用口罩', ['一次性口罩'])
# 防护类
防护服 = Item('防护服')
一次性医用帽 = Item('一次性医用帽', ['一次性工作帽'])
护目镜 = Item('护目镜', ['防护眼镜'])
防冲击眼罩 = Item('防冲击眼罩')
防护面罩 = Item('防护面罩', ['防护面屏'])
医用一次性乳胶手套 = Item('医用一次性乳胶手套', ['一次性乳胶手套', '一次性医用手套'])
一次性手术衣 = Item('一次性手术衣')
# 消毒类
消毒液 = Item('84消毒液')
过氧化氢消毒液 = Item('过氧化氢消毒液')
医用酒精 = Item('医用酒精', ['医用消毒酒精'])

# TODO:其他需求的处理，以及生活物资等
# TODO:医用标准
AllItems = [N95, 医用外科口罩, 一次性医用口罩, 防护服, 一次性医用帽, 护目镜, 防冲击眼罩, 防护面罩, 医用一次性乳胶手套, 一次性手术衣, 消毒液, 医用酒精]
