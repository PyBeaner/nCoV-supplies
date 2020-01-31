import json
import os
from threading import Thread

from urllib3.util import parse_url

from database import get_cursor
from utils.response import to_soup

site_file = os.path.abspath(os.path.dirname(__file__) + '/../data/sites.json')
siteMap = {}


def load_site_map():
    global siteMap
    if os.path.exists(site_file):
        siteMap = json.load(open(site_file, encoding='utf8'))


# 网站名称
def get_cached_name(site):
    if not siteMap:
        load_site_map()
    host = parse_url(site).host
    return siteMap[host] if host in siteMap else host


def get_site_name(site):
    import requests
    print('getting site name...', site)
    try:
        if '://' not in site:
            site = 'http://' + site
        resp = requests.get(site, timeout=10)
    except Exception as e:
        print('failed to get site name', site, e)
        return
    page = to_soup(resp)
    if not page:
        return
    title = page.find('title')
    result = title.text.strip() if title else ''
    print('success', site, result)
    host = parse_url(site).host
    siteMap[host] = result
    return result


def cache_all_sites():
    c = get_cursor()
    c.execute('select distinct source as site from notice')
    sites = c.fetchall()
    file = site_file
    load_site_map()
    global siteMap

    threads = []
    n = 0
    while sites:
        site = sites.pop()
        site = site['site']
        if site not in siteMap:
            t = Thread(target=get_site_name, args=(site,))
            threads.append(t)
            t.start()
        else:
            siteMap[site] = siteMap[site].strip()
        if len(threads) == 5 or not sites:
            for t in threads:
                t.join(5)
                n += 1
            threads = []

            with open(file, 'w', encoding='utf8') as f:
                json.dump(siteMap, f, ensure_ascii=False)
    with open(file, 'w', encoding='utf8') as f:
        json.dump(siteMap, f, ensure_ascii=False)


if __name__ == '__main__':
    cache_all_sites()
