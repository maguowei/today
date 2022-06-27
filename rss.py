from datetime import datetime, timezone, timedelta
from time import mktime
import yaml
import feedparser
import requests

from today import Today, DEFAULT_HEADERS


class RSS(Today):
    def __init__(self, name, desc, icon, url):
        self.name = name
        self.desc = desc
        self.icon = icon
        self.url = url
        super().__init__()

    def crawler(self):
        r = requests.get(self.url, headers=DEFAULT_HEADERS)
        news = feedparser.parse(r.content).entries

        data = []
        for new in news:
            published_parsed = new.published_parsed
            utc_time = datetime.fromtimestamp(mktime(published_parsed)).replace(tzinfo=timezone.utc)
            bj_time = utc_time.astimezone(timezone(timedelta(hours=8)))
            publish_time = bj_time.strftime('%Y-%m-%d %H:%M:%S')
            if bj_time.date() == datetime.today().date():
                item = {'title': new.title, 'url': new.link, 'summary': new.summary, 'publish_time': publish_time}
                data.append(item)
        return data


if __name__ == '__main__':
    with open('rss.yml') as f:
        data = yaml.safe_load(f)
        for source in data['sources']:
            RSS(**source).export()
