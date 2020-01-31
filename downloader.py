import datetime

import requests

from database import get_cursor
from utils.response import get_content

STATUS_INIT = 'init'
STATUS_FAILED = 'failed'
STATUS_IGNORED = 'ignored'
STATUS_DOWNLOADED = 'downloaded'


class NoticeDownloader:
    def __init__(self, url, title, source):
        self.init(url, title, source)
        # TODO:notice updated?

    def init(self, url, title, source):
        self.url = url
        self.title = title
        self.source = source

        c = get_cursor()
        c.execute('select id,status from notice where title=? and source=?', (self.title, self.source))
        row = c.fetchone()
        if not row:
            now = datetime.datetime.now()
            c = get_cursor()
            c.execute(
                'insert into notice (title, source, url, status, created_at, updated_at) '
                'values (?,?,?,?,?,?)', (self.title, self.source, self.url, STATUS_INIT, now, now))
            self._id = c.lastrowid
        else:
            self._id = row['id']

    # status of this notice
    def get_status(self):
        c = get_cursor()
        c.execute('select id,status from notice where title=? and source=?', (self.title, self.source))
        row = c.fetchone()
        return row['status'] if row else None

    # update status
    def update_status(self, status):
        c = get_cursor()
        now = datetime.datetime.now()
        c.execute('update notice set status=?,updated_at=? where id=?',
                  (status, now, self._id))

    # download the notice content
    def download(self):
        status = self.get_status()
        if status in (STATUS_DOWNLOADED, STATUS_IGNORED):
            return

        print('downloading...', self.url)
        try:
            resp = requests.get(self.url, timeout=10)
        except Exception as e:
            if type(e) is requests.exceptions.Timeout:
                print('Timeout occurred...', self.url)
            else:
                print("Error occurred when crawling", self.url, e)
            return

        if resp.status_code != 200:
            print("Error occurred when crawling", self.url, resp.status_code)
            if resp.status_code in (404, 403, 400):
                self.update_status(STATUS_IGNORED)
            return
        url = resp.url
        text = get_content(resp)
        if not text:
            return  # TODO
        c = get_cursor()
        now = datetime.datetime.now()
        with c.connection as conn:
            conn.execute('update notice set url=?,status=?,updated_at=? where id=?',
                         (url, STATUS_DOWNLOADED, now, self._id))
            conn.execute('insert into notice_detail (notice_id, raw_html) VALUES (?,?)',
                         (self._id, text))


# 下载最新获取的公告列表
def download_new_notices():
    print('Downloading Notices...')
    c = get_cursor()
    c.execute('select url,title,source from notice where status=? order by id desc', (STATUS_INIT,))
    rows = c.fetchall()
    from threading import Thread

    def download(row):
        import time, random
        time.sleep(random.randint(0, 3))
        NoticeDownloader(row['url'], row['title'], row['source']).download()

    threads = []
    n = 0
    while rows:
        row = rows.pop()
        t = Thread(target=download, args=(row,))
        threads.append(t)
        t.start()
        if len(threads) == 5:
            for t in threads:
                t.join(5)
                n += 1
            threads = []
    print('Downloading Finished!', n, ' new notices downloaded...')


if __name__ == '__main__':
    download_new_notices()
