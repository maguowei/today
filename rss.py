import os
from datetime import datetime, timezone, timedelta
from time import mktime
import yaml
import feedparser
import requests

from today import Today, DEFAULT_HEADERS
from utils.time import get_beijing_time


RSSHUB_DEFAULT_ADDR = 'https://rsshub.app'
RSSHUB_CUSTOM_ADDR = os.getenv('RSSHUB_CUSTOM_ADDR', 'http://82.157.186.108:1200')


class RSS(Today):
    def __init__(self, name, desc, icon, url, **kwargs):
        self.name = name
        self.desc = desc
        self.icon = icon
        self.url = url
        self.kwargs = kwargs
        super().__init__()

    def _get_proxy_url(self):
        source_need_proxy = self.kwargs.get('proxy', None)
        if source_need_proxy and RSSHUB_CUSTOM_ADDR:
            url = self.url.replace(RSSHUB_DEFAULT_ADDR, RSSHUB_CUSTOM_ADDR)
            print(f'use rsshub proxy addr: {url}')
            return url
        else:
            return self.url

    def crawler(self):
        url = self._get_proxy_url()
        r = requests.get(url, headers=DEFAULT_HEADERS)
        news = feedparser.parse(r.content).entries

        data = []
        for new in list(reversed(news)):
            published_parsed = new.get('published_parsed') or new.get('updated_parsed') or new.get('created_parsed')
            utc_time = datetime.fromtimestamp(mktime(published_parsed)).replace(tzinfo=timezone.utc)
            bj_time = utc_time.astimezone(timezone(timedelta(hours=8)))
            publish_time = bj_time.strftime('%Y-%m-%d %H:%M:%S')
            if bj_time.date() == get_beijing_time().date():
                item = {'title': new.title, 'url': new.link, 'summary': new.summary, 'publish_time': publish_time}
                data.append(item)
            else:
                pass
                # print(self.name, new.title, publish_time)
        return data


if __name__ == '__main__':
    with open('rss.yml') as f:
        data = yaml.safe_load(f)
        for source in data['sources']:
            RSS(**source).export()
