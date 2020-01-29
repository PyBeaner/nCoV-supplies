import os
import sqlite3

DEFAULT_DB = os.path.abspath(os.path.dirname(__file__) + './notice.db')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_cursor(db=DEFAULT_DB):
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    conn.isolation_level = None
    return conn.cursor()


def _create_tables():
    c = get_cursor()
    # 公告表
    c.execute(
        'CREATE TABLE if not exists notice (id integer primary key autoincrement,title varchar,published_at timestamp,source varchar,url text,status varchar,created_at timestamp,updated_at timestamp)')
    # 公告详情表
    c.execute(
        'CREATE TABLE if not exists notice_detail (id integer primary key autoincrement,notice_id integer, raw_html text, content text)')
    # 物资需求表（暂时没有用到）
    c.execute(
        'CREATE TABLE if not exists notice_demand (id integer primary key autoincrement,notice_id integer, item_name varchar,remark text)')


if __name__ == '__main__':
    _create_tables()
