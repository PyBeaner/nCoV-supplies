from downloader import download_new_notices
from parse import generate_csv


def run():
    import os
    os.system('scrapy runspider crawler.py')
    download_new_notices()
    generate_csv()


if __name__ == '__main__':
    run()
