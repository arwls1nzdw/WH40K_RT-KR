from glob import glob

import utils

data = utils.load_json("dist/enGB.json")
for f in glob("patches/**/*-kr.json", recursive=True):
    d = utils.load_json(f)

    for k, v in d.items():
        if k not in data['strings']:
            continue
        data['strings'][k]['Text'] = v

utils.write_json(data, "dist/koKR.json")

# 영문 병기
enGB = utils.load_json("dist/enGB.json")
for f in [*glob("patches/World/Dialogs/**/*-kr.json", recursive=True), "patches/World/Dialogs-kr.json"]:
    d = utils.load_json(f)
    for k, v in d.items():
        if k not in data['strings']:
            continue
        en = enGB['strings'][k]['Text']
        data['strings'][k]['Text'] = f"{v}\n<size=95%>{en}</size>"

utils.write_json(data, "dist/koKR_영문병기.json")
