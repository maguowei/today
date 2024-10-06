from pathlib import Path
from abc import ABC, abstractmethod
from utils.dump import json_dump
from utils.time import get_beijing_time
from utils.logger import logger
from sql_import import history_data_import, insert_feeds, get_today_feed, get_today_feed_by_source


DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}


class Today(ABC):
    name = None
    desc = None
    icon = None
    url = None

    def __init__(self):
        fields = [self.name, self.desc, self.icon, self.url]
        if not all(f is not None for f in fields):
            raise TypeError(f"init error: fields has None value")

        self.latest_source_data = []
        self.latest_feeds_data = []
    @abstractmethod
    def crawler(self) -> list[dict]:
        pass

    def get_filename(self, module, ext):
        today = get_beijing_time().strftime('%Y-%m-%d')
        if module == 'sources':
            filename = f'data/{module}/{self.name}/{ext}/{today}.{ext}'
        else:
            filename = f'data/{module}/{ext}/{today}.{ext}'
        return filename

    def dump_json(self, module):
        filename = self.get_filename(module, 'json')
        if module == 'sources':
            json_dump(filename, self.latest_source_data)
        else:
            json_dump(filename, self.latest_feeds_data)
        logger.info(f'dump_json: {filename}')

    def dump_md(self, module):
        time = get_beijing_time().strftime('%Y-%m-%d %H:%M:%S')
        filename = self.get_filename(module, 'md')
        file = Path(filename)
        file.parent.mkdir(exist_ok=True, parents=True)

        if module == 'sources':
            title = self.desc
            data = self.latest_source_data
        else:
            title = 'Today'
            data = self.latest_feeds_data

        with file.open('w+') as f:
            f.writelines(f'# {title}\n\n')
            f.writelines(f'最近更新时间: {time}\n\n')
            f.writelines(f'--- \n')
            mds = [f"{i + 1}. [{item['title']}]({item['url']}) {item['source']['desc'] if module == 'feeds' else ''}\n" for i, item in enumerate(data)]
            f.writelines(mds)
        logger.info(f'dump_md: {filename}')

    @property
    def source_meta_info(self):
        return {
            'name': self.name,
            'desc': self.desc,
            'icon': self.icon,
        }

    def export(self):
        data = self.crawler()
        history_data_import(limit=1)
        feeds = self.get_feeds(data)
        insert_feeds(feeds)

        self.latest_source_data = get_today_feed_by_source(self.name)
        self.latest_feeds_data = get_today_feed()

        self.dump_json('sources')
        self.dump_md('sources')
        self.dump_json('feeds')
        self.dump_md('feeds')
        logger.info(f'export data, name: {self.name}, desc: {self.desc}, count: {len(self.latest_source_data)}')

    def get_feeds(self, data):
        feeds = []
        for item in data:
            item['source'] = self.source_meta_info
            feeds.append(item)
        return feeds
