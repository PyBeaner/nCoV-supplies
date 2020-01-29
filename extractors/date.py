import datetime
import re

from extractors.common import Extractor


class DateTimeExtractor(Extractor):
    def extract(self):
        p = re.compile(R'(\d{4})年(\d{1,2})月(\d{1,2})日')
        result = p.findall(self.content)
        if not result:
            p = re.compile(R'(\d{4})-(\d{1,2})-(\d{1,2})')
            result = p.findall(self.content)
        if not result:
            return
        year, month, day = result[-1]
        result = datetime.date(year=int(year), month=int(month), day=int(day))
        return result


if __name__ == '__main__':
    print(DateTimeExtractor('2020年1月28日').extract())
