import json
from pathlib import Path


def json_dump(filename, data):
    file = Path(filename)
    file.parent.mkdir(exist_ok=True, parents=True)

    with file.open('w+') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
