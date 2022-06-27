import json
from pathlib import Path
from abc import ABC, abstractmethod
from utils.dump import json_dump, json_append_dump
from utils.time import get_beijing_time


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
        self.latest_source_data = self.get_latest_data('sources')
        self.add_source_data = []
        self.latest_feeds_data = self.get_latest_feeds_data()

    @abstractmethod
    def crawler(self) -> list[dict]:
        pass

    def get_latest_data(self, module) -> list:
        filename = self.get_filename(module, 'json')
        try:
            with open(filename) as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return []

    def get_latest_feeds_data(self) -> list:
        data = self.get_latest_data('feeds')
        return data

    def get_filename(self, module, ext):
        today = get_beijing_time().strftime('%Y-%m-%d')
        if module == 'sources':
            filename = f'data/{module}/{self.name}/{ext}/{today}.{ext}'
        else:
            filename = f'data/{module}/{ext}/{today}.{ext}'
        return filename

    def merge_source_data(self, data):
        titles = [item['title'] for item in self.latest_source_data]
        for item in data:
            if item['title'] not in titles:
                self.latest_source_data.append(item)
                self.add_source_data.append(item)
        return self.latest_source_data

    def dump_json(self, module):
        filename = self.get_filename(module, 'json')
        if module == 'sources':
            json_dump(filename, self.latest_source_data)
        else:
            data = self.latest_feeds_data
            data.extend(self.get_feeds(self.add_source_data))
            json_dump(filename, data)
        print(f'dump_json: {filename}')

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
            data.extend(self.get_feeds(self.add_source_data))

        with file.open('w+') as f:
            f.writelines(f'# {title}\n\n')
            f.writelines(f'最近更新时间: {time}\n\n')
            f.writelines(f'--- \n')
            mds = [f"{i + 1}. [{hot['title']}]({hot['url']})\n" for i, hot in enumerate(data)]
            f.writelines(mds)
        print(f'dump_md: {filename}')

    @property
    def source_meta_info(self):
        return {
            'name': self.name,
            'desc': self.desc,
            'icon': self.icon,
        }

    def export(self):
        data = self.crawler()
        self.merge_source_data(data)
        if self.add_source_data:
            self.dump_json('sources')
            self.dump_md('sources')
            self.dump_json('feeds')
            self.dump_md('feeds')
        print(f'export data, name: {self.name}, desc: {self.desc}, count: {len(self.latest_source_data)}, new: {len(self.add_source_data)}')

    def get_feeds(self, data):
        feeds = []
        for item in data:
            item['source'] = self.source_meta_info
            feeds.append(item)
        return feeds
