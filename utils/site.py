from utils.response import to_soup


# TODO:cache
def get_title(host):
    import requests
    resp = requests.get(host)
    page = to_soup(resp)
    return page.find('title').text


if __name__ == '__main__':
    print(get_title('http://www.nxyn.gov.cn'))
