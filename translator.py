import requests
import json


import utils


def translate_local(text: str):
    url = "http://127.0.0.1:8000/t"
    data = {"text": text}
    headers = {"Content-Type": "application/json"}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()["text"]


def translate_local_tokenized(text: str):
    tagMap = {}
    for t in utils.tokenize(text):
        t2 = utils.replace_tags(t, tagMap)
        t2 = translate_local(t2)
        t2 = utils.recover_tags(t2, tagMap)
        text = text.replace(t, t2, 1)

    return text
