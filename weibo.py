import datetime
import json
import requests


URL = 'https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=filter_type%3Drealtimehot%26mi_cid%3D100103%26pos%3D0_0%26c_type%3D30%26display_time%3D1540538388&luicode=10000011&lfid=231583'


class Weibo:
    @classmethod
    def get_weibo_hots(cls):
        r = requests.get(URL)
        hots = r.json()['data']['cards'][0]['card_group']
        data = [{'title': hot['desc'], 'url': hot['scheme']} for hot in hots]
        return data

    @classmethod
    def get_latest_hot_data(cls, filename):
        try:
            with open(filename) as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return []

    @classmethod
    def export_hots(cls):
        today = datetime.date.today()
        data = cls.get_weibo_hots()

        raw_filename = f'data/raw/{today}.json'
        md_filename = f'data/md/{today}.md'

        old_data = cls.get_latest_hot_data(raw_filename)

        data = cls.merge_hots(old_data, data)

        cls.dump_hots_json(raw_filename, data)
        cls.dump_hots_md(md_filename, data)

    @classmethod
    def merge_hots(cls, old_data, new_data):
        titles = [hot['title'] for hot in old_data]
        new_count = 0
        for hot in new_data:
            if hot['title'] not in titles:
                old_data.append(hot)
                new_count += 1

        print(f'热搜总计: {len(old_data)}, 新增: {new_count}')
        return old_data

    @classmethod
    def dump_hots_json(cls, filename, data):
        with open(filename, 'w+') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @classmethod
    def dump_hots_md(cls, filename, data):
        with open(filename, 'w+') as f:
            mds = [f"{i+1}. [{hot['title']}]({hot['url']})\n" for i, hot in enumerate(data)]
            f.writelines(mds)


if __name__ == '__main__':
    Weibo.export_hots()
