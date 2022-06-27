import json
import yaml
import feedparser


def get_config() -> dict:
    data = None

    with open('feedme.yaml') as f:
        data = yaml.safe_load(f)

    return data


config = get_config()

title = config['title']
sources = config['sources']

data = []

for source in sources:
    d = feedparser.parse(source['href'])

    items = []
    for entrie in d.entries:
        items.append(
            {
                'title': entrie.title,
                'link': entrie.link,
                # 'published': entrie.published,
            }
        )

    source_data = {
        'title': d.feed.title,
        'link': d.feed.link,
        'items': items,
    }

    data.append(source_data)

print(json.dumps(data, ensure_ascii=False))