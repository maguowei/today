import requests
from today import Today, DEFAULT_HEADERS


class ZhihuHot(Today):
    name = 'zhihu_hot'
    desc = '知乎热榜'
    icon = 'https://raw.githubusercontent.com/maguowei/today/master/imgs/icon/zhihu.png'
    url = 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=100'

    def crawler(self) -> list[dict]:
        r = requests.get(self.url, headers=DEFAULT_HEADERS)
        hots = r.json()['data']

        data = [{'title': item['target']['title'], 'url': f"https://www.zhihu.com/question/{item['target']['id']}"} for item in hots]
        return data


if __name__ == '__main__':
    ZhihuHot(ZhihuHot.name, ZhihuHot.desc, ZhihuHot.icon).export()
