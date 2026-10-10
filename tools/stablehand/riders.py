"""Riders: the villagefriends:challengers entity tag.

Not-So-Vanilla Mobs' challenger bosses spook every horse nearby (low-bond horses bolt or throw their rider,
steadier ones rear). Village Friends never depends on that mod: every entry is `"required": false`, so without
it the tag simply loads empty, and the spook code only looks at the tag when `nsvmobs` is loaded.

The ids are the ten challengers registered in Not-So-Vanilla-Mobs' NsvEntities. Never hand-edit the JSON;
change the list here and rerun tools/stablehand/stablehand.py.
"""
from kit import DATA, dump

MOD = 'nsvmobs'
CHALLENGERS = ['broodmother', 'sandmaw', 'cinderhulk', 'crag_troll', 'prowler',
               'stormcaller', 'brineclaw', 'rimewraith', 'riftstalker', 'oregorger']
TAG = DATA / 'villagefriends/tags/entity_type/challengers.json'


def tag():
    return {'replace': False, 'values': [{'id': f'{MOD}:{name}', 'required': False} for name in CHALLENGERS]}


def outputs():
    return {TAG: dump(tag())}


def preview():
    print(f'riders: villagefriends:challengers holds {len(CHALLENGERS)} optional ids:')
    for entry in tag()['values']:
        print(f"  {entry['id']}")
