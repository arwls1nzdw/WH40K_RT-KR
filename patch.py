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
