import os
from urllib.parse import quote_plus

import requests

STATUS_INIT = 'init'
STATUS_FAILED = 'failed'
STATUS_IGNORED = 'ignored'
STATUS_DOWNLOADED = 'downloaded'


class NoticeHandler:
    def __init__(self, url, title, source):
        self.url = url
        self.title = title
        self.source = source
        # TODO:notice updated?
        self.log_path = 'data/logs/%s/%s' % (source, title)

    # handle-status of this notice
    def get_status(self):
        p = self.log_path
        try:
            with open(p, 'r') as f:
                return f.readline().strip()
        except Exception:
            return STATUS_INIT

    # update status
    def update_status(self, status):
        p = self.log_path
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w') as f:
            return f.write(status)

    # download the notice content
    def download(self):
        status = self.get_status()
        if status in (STATUS_DOWNLOADED, STATUS_IGNORED):
            return
        print('downloading...', self.url, status)
        try:
            resp = requests.get(self.url, timeout=3)
        except requests.exceptions.Timeout:
            print('Timeout occurred...', self.url)
            return

        if resp.status_code != 200:
            print("Error occurred when crawling", self.url)
            if resp.status_code == 404:
                self.update_status(STATUS_IGNORED)
            return
        url = resp.url
        save_as = 'data/notices/' + quote_plus(url)
        if not save_as.endswith('.html'):
            save_as += '.html'
        with open(save_as, 'w', encoding='utf8') as f:
            try:
                text = resp.content.decode('utf8')
            except:
                text = resp.content.decode('gbk')
            f.write(text)
        self.update_status(STATUS_DOWNLOADED)
