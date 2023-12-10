"""
    Blueprint 파일

    SteamLibrary/steamapps/common/Warhammer 40,000 Rogue Trader/Modding/WhRtModificationTemplate-release.rar
"""

from collections import defaultdict
from glob import glob

import utils

files = glob(f"blueprints/**/*.json", recursive=True)
files = map(lambda x: x.replace("\\", "/"), files)
files = sorted(files)

metadata = defaultdict(lambda: defaultdict(dict))
for f in files:
    bp = utils.load_json(f)
    key = bp.get('key', bp.get('String', {}).get('m_Key'))

    metadata[key]['path'] = f
    if 'speaker' in bp:
        metadata[key]['speaker'] = bp['speaker']
    if 'speakerGender' in bp:
        metadata[key]['speakerGender'] = bp['speakerGender']

utils.write_json(metadata, "patches/_metadata.json")
