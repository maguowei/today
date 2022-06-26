import json
from weibo import WeiboHot
from zhihu import ZhihuHot
from utils.dump import json_dump


source = [WeiboHot, ZhihuHot]


def dump_json():
    data = {s.name: s(s.name, s.desc, s.icon).source_meta_info for s in source}
    json_dump('data/sources.json', data)


if __name__ == '__main__':
    dump_json()
