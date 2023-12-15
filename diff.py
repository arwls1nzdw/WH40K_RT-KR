from glob import glob

import deep_translator
from tqdm import tqdm

import utils

translator = deep_translator.GoogleTranslator(source='ja', target='ko')

enGB_prev = utils.load_json("dist/enGB.prev.json")['strings']
enGB_curr = utils.load_json("dist/enGB.json")['strings']
koKR = utils.load_json("dist/koKR.json")['strings']
jaJP = utils.load_json("dist/jaJP.json")['strings']

dummy_keys = []
for k, v in enGB_curr.items():
    if v['Text'] == jaJP[k]['Text']:
        dummy_keys.append(k)

keys_removed = []
keys_added = []
keys_changed = []
for k, v in enGB_curr.items():
    if k not in enGB_prev:
        keys_added.append(k)
    elif v['Text'] != enGB_prev[k]['Text']:
        keys_changed.append(k)

for k, v in enGB_prev.items():
    if k not in enGB_curr:
        keys_removed.append(k)


for f in glob("patches/**/*.json", recursive=True):
    patch = utils.load_json(f)
    for k in keys_removed:
        if k in patch:
            del patch[k]

    if '-en' in f:
        for k in keys_changed:
            if k in patch:
                patch[k] = enGB_curr[k]


print("Keys removed: {}".format(len(keys_removed)))
data_removed = {}
for k in keys_removed:
    data_removed[k] = enGB_prev[k]['Text']
utils.write_json(data_removed, ".tmp/removed.json")

print("Keys added: {}".format(len(keys_added)))
keys_added = list(filter(lambda x: x not in dummy_keys, keys_added))
data_added = {}
for k in keys_added:
    data_added[k] = (
        enGB_curr[k]['Text'],
        "",
    )
utils.write_json(data_added, ".tmp/added.json")

print("Keys changed: {}".format(len(keys_changed)))
keys_changed = list(filter(lambda x: x not in dummy_keys, keys_changed))
data_changed = {}
for k in tqdm(keys_changed):
    data_changed[k] = (
        enGB_prev[k]['Text'],
        enGB_curr[k]['Text'],
        koKR[k]['Text'],
        "",
    )
utils.write_json(data_changed, ".tmp/changed.json")
