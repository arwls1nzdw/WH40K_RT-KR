"""
    Blueprint 파일

    SteamLibrary/steamapps/common/Warhammer 40,000 Rogue Trader/Modding/WhRtModificationTemplate-release.rar
"""

from collections import defaultdict
from glob import glob
from pathlib import Path

import utils


def isDummy(text: str):
    if len(text) == 0:
        return True
    if "[draft]" in text.lower():
        return True
    return False


if __name__ == "__main__":
    files = glob(f"blueprints/**/*.json", recursive=True)
    files = map(lambda x: x.replace("\\", "/"), files)
    files = sorted(files)

    enGB = utils.load_json("dist/enGB.json")['strings']
    koKR = utils.load_json("dist/koKR.json")['strings']

    dummyKeys = [k for k in enGB if isDummy(enGB[k]['Text'])]
    for k in dummyKeys:
        del enGB[k]
        del koKR[k]

    groupNames = set()
    for f in glob("blueprints/*"):
        f = f.replace("\\", "/")
        groupNames.add(f.split("/")[-1])

    def getSubGroups(rootGroup, depth):
        if depth == 0:
            return set([rootGroup])

        subGroups = set()
        for f in glob(f"blueprints/{rootGroup}/**/*", recursive=True):
            if Path(f).is_file():
                f = Path(f).parent

            f = str(f).replace("\\", "/")
            if f.count('/') == depth + rootGroup.count('/') + 1:
                groupKey = '/'.join(f.split("/")[1:])
                subGroups.add(groupKey)

        return subGroups

    groupNames.update(getSubGroups("Classes", 1))
    groupNames.update(getSubGroups("Consumables", 1))
    groupNames.update(getSubGroups("Root", 0))
    groupNames.update(getSubGroups("Equipment", 1))
    groupNames.update(getSubGroups("GlobalMaps", 1))
    groupNames.update(getSubGroups("Units", 0))
    groupNames.update(getSubGroups("Spacecombat", 1))
    groupNames.update(getSubGroups("TutorialWindows", 1))
    groupNames.update(getSubGroups("Weapons", 1))
    groupNames.update(getSubGroups("World/Areas", 1))
    groupNames.update(getSubGroups("World/Dialogs", 2))
    groupNames.update(getSubGroups("World/Quests", 1))
    groupNames.update(getSubGroups("World", 1))
    groupNames = sorted(groupNames)

    grouped = defaultdict(set)
    current = defaultdict(lambda: None)
    for f in files:
        for g in groupNames:
            if f.startswith(f"blueprints/{g}"):
                grouped[g].add(f)
                if current[f]:
                    grouped[current[f]].remove(f)
                current[f] = g

    keyFound = set()
    for g in grouped:
        output = defaultdict(dict)
        for f in grouped[g]:
            bp = utils.load_json(f)
            key = bp.get('key', bp.get('String', {}).get('m_Key'))
            if key not in enGB or key in keyFound:
                continue
            output['en'][key] = enGB[key]['Text']
            output['kr'][key] = koKR[key]['Text']
            keyFound.add(key)

        if len(output['en']) == 0:
            continue

        output['en'] = dict(sorted(output['en'].items()))
        output['kr'] = dict(sorted(output['kr'].items(),
                            key=lambda x: (enGB[x[0]]['Text'], x[0])))
        utils.write_json(output['en'], f"patches/{g}-en.json")
        utils.write_json(output['kr'], f"patches/{g}-kr.json")

    missingKeys = [k for k in enGB if k not in keyFound]
    missingData = defaultdict(dict)
    for k in missingKeys:
        missingData['en'][k] = enGB[k]['Text']
        missingData['kr'][k] = koKR[k]['Text']

    missingData['en'] = dict(sorted(missingData['en'].items()))
    missingData['kr'] = dict(
        sorted(missingData['kr'].items(), key=lambda x: (enGB[x[0]]['Text'], x[0])))
    utils.write_json(missingData['en'], "patches/missing-en.json")
    utils.write_json(missingData['kr'], "patches/missing-kr.json")
