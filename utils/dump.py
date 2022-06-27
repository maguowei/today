import json
from pathlib import Path


def json_dump(filename, data):
    file = Path(filename)
    file.parent.mkdir(exist_ok=True, parents=True)

    with file.open('w+') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def json_append_dump(filename, data):
    file = Path(filename)
    file.parent.mkdir(exist_ok=True, parents=True)

    with file.open('a+') as f:
        try:
            store = json.load(f)
        except json.JSONDecodeError:
            store = []
        store.extend(data)
        json.dump(store, f, ensure_ascii=False, indent=2)
