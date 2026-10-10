"""Horse breeds: the data table Java reads (stablehand/breeds.json), and later the painted coats, the brush
and whistle sprites and their recipes.

Each row: stat ranges (vanilla wild horses: health 15-30, speed 0.1125-0.3375 where x42.16 is blocks per
second, jump 0.4-1.0), where the breed is picked (biome keyword and weight; `any` matches every biome),
extra biome spawns for places vanilla has no horses (keyword, weight, group size), vanilla markings drawn on
top of the coat, how many painted coats it has, and which village types keep it in their stables.

Biome keywords: plains (path has "plains", not "snowy"), meadow, forest, savanna, desert, badlands, taiga,
snowy (cold farm-animal biomes), windswept (path starts with "windswept"), any.

Never hand-edit breeds.json; change the rows here and rerun tools/stablehand/stablehand.py.
"""
from kit import TABLES, dump

BREEDS = [
    {'id': 'destrier', 'name': 'Destrier', 'health': [26, 34], 'speed': [0.20, 0.26], 'jump': [0.55, 0.75],
     'spawns': [('plains', 1)], 'extra_spawns': [], 'markings': ['none', 'white'], 'coats': 1, 'village': ['plains']},
    {'id': 'palfrey', 'name': 'Palfrey', 'health': [20, 26], 'speed': [0.24, 0.30], 'jump': [0.60, 0.80],
     'spawns': [('plains', 4), ('meadow', 3), ('forest', 2)], 'extra_spawns': [], 'markings': ['white', 'white_field'],
     'coats': 1, 'village': ['plains']},
    {'id': 'courser', 'name': 'Courser', 'health': [16, 22], 'speed': [0.29, 0.3375], 'jump': [0.70, 0.95],
     'spawns': [('plains', 2), ('savanna', 2)], 'extra_spawns': [], 'markings': ['none', 'white_dots'],
     'coats': 1, 'village': ['plains', 'savanna']},
    {'id': 'rouncey', 'name': 'Rouncey', 'health': [18, 26], 'speed': [0.20, 0.27], 'jump': [0.55, 0.80],
     'spawns': [('plains', 5), ('forest', 3), ('any', 3)], 'extra_spawns': [],
     'markings': ['none', 'white', 'white_field', 'white_dots', 'black_dots'], 'coats': 1, 'village': ['plains', 'taiga']},
    {'id': 'draft', 'name': 'Draft Horse', 'health': [28, 36], 'speed': [0.15, 0.20], 'jump': [0.40, 0.55],
     'spawns': [('plains', 1), ('forest', 1), ('taiga', 1)], 'extra_spawns': [], 'markings': ['none', 'white'],
     'coats': 1, 'village': ['plains', 'taiga', 'snowy']},
    {'id': 'desert', 'name': 'Desert Horse', 'health': [16, 22], 'speed': [0.28, 0.34], 'jump': [0.65, 0.90],
     'spawns': [('desert', 5), ('badlands', 3)], 'extra_spawns': [('desert', 2, 2, 3), ('badlands', 1, 2, 3)],
     'markings': ['none'], 'coats': 1, 'village': ['desert']},
    {'id': 'steppe_pony', 'name': 'Steppe Pony', 'health': [20, 26], 'speed': [0.22, 0.28], 'jump': [0.75, 1.00],
     'spawns': [('savanna', 4), ('windswept', 4)], 'extra_spawns': [('windswept', 2, 2, 4)], 'markings': ['none', 'black_dots'],
     'coats': 1, 'village': ['savanna']},
    {'id': 'fjord', 'name': 'Fjord Horse', 'health': [22, 28], 'speed': [0.18, 0.24], 'jump': [0.60, 0.80],
     'spawns': [('taiga', 4), ('snowy', 4)], 'extra_spawns': [('taiga', 2, 2, 4), ('snowy', 1, 2, 3)], 'markings': ['none'],
     'coats': 1, 'village': ['taiga', 'snowy']},
]
KEYWORDS = ['plains', 'meadow', 'forest', 'savanna', 'desert', 'badlands', 'taiga', 'snowy', 'windswept', 'any']
MARKINGS = ['none', 'white', 'white_field', 'white_dots', 'black_dots']


def table():
    rows = []
    for b in BREEDS:
        assert all(k in KEYWORDS for k, _ in b['spawns']) and all(s[0] in KEYWORDS for s in b['extra_spawns']), b['id']
        assert all(m in MARKINGS for m in b['markings']), b['id']
        rows.append({'id': b['id'], 'name': b['name'], 'health': b['health'], 'speed': b['speed'], 'jump': b['jump'],
                     'spawns': [{'biome': k, 'weight': w} for k, w in b['spawns']],
                     'extra_spawns': [{'biome': k, 'weight': w, 'min': lo, 'max': hi} for k, w, lo, hi in b['extra_spawns']],
                     'markings': b['markings'], 'coats': b['coats'], 'village': b['village']})
    return {'breeds': rows}


def outputs():
    # Coat art, brush and whistle sprites and recipes are added here by the breeds package.
    return {TABLES / 'breeds.json': dump(table())}


def preview():
    print('breeds: no art to preview yet.')
