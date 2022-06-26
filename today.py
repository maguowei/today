import json
from pathlib import Path
from datetime import datetime, timedelta, timezone
from abc import ABC, abstractmethod
from utils.dump import json_dump


DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}


class Today(ABC):
    def __init__(self, name, desc, icon):
        self.name = name
        self.desc = desc
        self.icon = icon
        self.latest_data = self.get_latest_data()

    def get_latest_data(self):
        filename = self.get_filename_by_ext('json')
        try:
            with open(filename) as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return []

    @classmethod
    def get_bj_time_now(cls):
        utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        # 转换为北京时间
        bj_time = utc_time.astimezone(timezone(timedelta(hours=8)))
        return bj_time

    def get_filename_by_ext(self, ext):
        today = self.get_bj_time_now().today().strftime('%Y-%m-%d')
        filename = f'data/{self.name}/{ext}/{today}.{ext}'
        return filename

    @abstractmethod
    def crawler(self) -> list[dict]:
        pass

    def export(self):
        data = self.crawler()
        self.merge_data(data)
        self.dump_json()
        self.dump_md()

    def merge_data(self, data):
        titles = [item['title'] for item in self.latest_data]
        new_count = 0
        for item in data:
            if item['title'] not in titles:
                self.latest_data.append(item)
                new_count += 1

        print(f'merge data, count: {len(self.latest_data)}, new: {new_count}')
        return self.latest_data

    def dump_json(self):
        filename = self.get_filename_by_ext('json')
        json_dump(filename, self.latest_data)

    def dump_md(self):
        time = self.get_bj_time_now().strftime('%Y-%m-%d %H:%M:%S')
        filename = self.get_filename_by_ext('md')
        file = Path(filename)
        file.parent.mkdir(exist_ok=True, parents=True)
        with file.open('w+') as f:
            f.writelines(f'# {self.desc}\n\n')
            f.writelines(f'最近更新时间: {time}\n\n')
            f.writelines(f'--- \n')
            mds = [f"{i + 1}. [{hot['title']}]({hot['url']})\n" for i, hot in enumerate(self.latest_data)]
            f.writelines(mds)

    @property
    def source_meta_info(self):
        return {
            'name': self.name,
            'desc': self.desc,
            'icon': self.icon,
        }
