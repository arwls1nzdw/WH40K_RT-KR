import json
import csv
from pathlib import Path


def load_json(path):
    with open(path, 'rt', encoding='utf-8') as fp:
        return json.load(fp)


def load_csv(csvFile, delimiter=','):
    with open(csvFile, 'r', encoding='utf-8') as fp:
        return list(csv.reader(fp, delimiter=delimiter))


def write_json(data, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'wt', encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)


def flatten(arr):
    return [item for sublist in arr for item in sublist]


def tokenize(text: str):
    text = text.split("{n}")
    text = (t.split("{/n}") for t in text)
    text = flatten(text)
    text = (t.split('\n') for t in text)
    text = flatten(text)
    text = map(lambda x: x.strip(), text)
    text = filter(lambda x: x != "", text)
    text = map(lambda x: x[1:-1] if x[0] == '"' and x[-1] == '"' else x, text)
    text = map(lambda x: x[1:] if x[0] == '"' else x, text)
    text = map(lambda x: x[:-1] if x[-1] == '"' else x, text)
    text = filter(lambda x: x != "", text)

    return list(text)


def replace_tags(text: str, tagDict: dict):
    index = len(tagDict)
    si = text.find('{')
    while si != -1:
        ei = text.find('}', si)
        tag = text[si:ei + 1]

        if 'g|' in tag:
            text = text[:si] + f"<T{index}>" + text[ei + 1:]
            text = text.replace('{/g}', f"</T{index}>", 1)
        else:
            text = text[:si] + f"<T{index}/>" + text[ei + 1:]
        tagDict[index] = tag
        index += 1
        si = text.find('{', si + 1)

    return text


def recover_tags(text: str, tagDict: dict):
    si = text.find('<T')
    while si != -1:
        ei = text.find('>', si)
        tag = text[si:ei + 1]
        tagIndex = tag[2:-1] if '/' not in tag else tag[2:-2]
        tagIndex = int(tagIndex)
        text = text[:si] + tagDict[tagIndex] + text[ei + 1:]
        text = text.replace(f"</T{tagIndex}>", '{/g}', 1)
        si = text.find('<T', si + 1)

    return text
