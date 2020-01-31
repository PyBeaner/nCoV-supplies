import requests
from bs4 import BeautifulSoup


def get_content(resp):
    """

    :type resp: requests.Response
    """
    text = ''
    try:
        text = resp.content.decode('utf8')
    except:
        try:
            text = resp.content.decode('gbk')
        except:
            pass
    return text


def to_soup(resp):
    """

    :type resp: requests.Response
    """
    html = get_content(resp)
    if html:
        return BeautifulSoup(html, features='lxml')
