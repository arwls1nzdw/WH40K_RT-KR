from glob import glob

import utils
import translator

# added

added = utils.load_json(".tmp/added.json")
for k, v in added.items():
    if v[1] == "":
        v[1] = translator.translate_local_tokenized(v[0])
utils.write_json(added, ".tmp/added.json")

for f in glob("patches/**/*-kr.json", recursive=True):
    data = utils.load_json(f)
    for k, v in data.items():
        if k in added:
            data[k] = added[k][1]
    utils.write_json(data, f)

# removed
removed = utils.load_json(".tmp/removed.json")
for f in glob("patches/**/*-kr.json", recursive=True):
    data = utils.load_json(f)
    for k in removed:
        if k in data:
            del data[k]
    utils.write_json(data, f)

# changed
changed = utils.load_json(".tmp/changed.json")
for k, v in changed.items():
    if v[3] == "":
        v[3] = translator.translate_local_tokenized(v[1])
utils.write_json(changed, ".tmp/changed.json")

for f in glob("patches/**/*-kr.json", recursive=True):
    data = utils.load_json(f)
    for k, v in changed.items():
        if k in data:
            data[k] = v[3]
    utils.write_json(data, f)
