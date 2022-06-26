import requests
from urllib.parse import urlencode
from today import Today, DEFAULT_HEADERS


class WeiboHot(Today):
    name = 'weibo_hot'
    desc = '微博热搜'
    icon = 'https://raw.githubusercontent.com/maguowei/today/master/imgs/icon/weibo.png'
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=filter_type%3Drealtimehot'

    def crawler(self):
        r = requests.get(self.url, headers=DEFAULT_HEADERS)
        hots = r.json()['data']['cards'][0]['card_group']

        data = []
        for item in hots:
            query = urlencode({'q': f"#{item['desc']}#", 'Refer': 'top'})
            data.append({'title': item['desc'], 'url': f"https://s.weibo.com/weibo?{query}"})
        return data


if __name__ == '__main__':
    WeiboHot(WeiboHot.name, WeiboHot.desc, WeiboHot.icon).export()
