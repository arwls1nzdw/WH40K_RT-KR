import json
from pathlib import Path


def load_json(path):
    with open(path, 'rt', encoding='utf-8') as fp:
        return json.load(fp)


def write_json(data, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wt', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)
