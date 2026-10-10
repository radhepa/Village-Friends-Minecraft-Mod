"""Compiles Tall Tales Fishing's data table into the mod: the fish table the game reads at start-up (with the
biome regions it uses to tell a desert river from a taiga one), item tags, crafting and cooking recipes for the
gear and Grilled Fish, the fisherman's trades (he is the village fishmonger) and the language file.

Source (tab separated, '#' lines are comments):

  tools/fishing/fish.tsv     every fish: where and when it bites, its size, rarity and how it fights

Outputs:

  src/main/resources/villagefriends/fishing/fish.json            fish, regions, gear (read by dev.villagefriends.fishing.FishTable)
  data/villagefriends/recipe/<gear>.json                         rods, bait, tackle, the journal, the trophy mount, grilled fish
  data/villagefriends/loot_table/blocks/trophy_mount.json         the mount drops itself
  data/villagefriends/villager_trade/fisherman/*.json            fishmonger trades, listed in the vanilla fisherman level tags;
  data/minecraft/trade_set/fisherman/level_<n>.json              and three offers a level instead of two, so the gear shows up
  data/{c,minecraft,villagefriends}/tags/item/...                fish, edible, grillable, treats, legendary, trout, rods, bait,
                                                                 tackle, minecraft:fishes/cat_food/wolf_food, c:foods/raw_fish...
  assets/villagefriends/lang/en_us.json                          merged: names for everything here, other keys untouched

    python tools/fishing/fishing.py            # write everything
    python tools/fishing/fishing.py --check    # exit 1 if anything is out of date or the table is inconsistent
    python tools/fishing/fishing.py --stats    # counts by rarity, water and region

Art comes from tools/fishing/sprites.py (the fish and their silhouettes) and tools/fishing/art.py (gear, the
trophy mount, the minigame and journal screens). The fish join Hearth & Harvest's cooking tag through
villagefriends:fishing/edible (tools/hearth/hearth.py writes cooking/fish).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
RES = PROJECT / 'src/main/resources'
ASSETS = RES / 'assets/villagefriends'
DATA = RES / 'data'
NS = 'villagefriends'

RARITIES = ('common', 'uncommon', 'rare', 'epic', 'legendary')
WATERS = {'river', 'lake', 'swamp', 'ocean', 'warm', 'cold', 'deep', 'cave', 'deepcave'}
TIMES = {'dawn', 'day', 'noon', 'dusk', 'night'}
WEATHERS = {'any', 'clear', 'rain', 'thunder'}
SEASONS = {'spring', 'summer', 'autumn', 'winter'}
BEHAVIORS = {'smooth', 'mixed', 'dart', 'sinker', 'floater'}
FLAGS = {'existing', 'shellfish', 'inedible', 'poison', 'notreat'}

# The land around the water: which biomes count as which region. A river or ocean biome belongs to no region;
# the region of a bit of water is the most common region among the biomes around it.
REGIONS = {
    'plains': ['minecraft:plains', 'minecraft:sunflower_plains', 'minecraft:meadow'],
    'forest': ['minecraft:forest', 'minecraft:flower_forest', 'minecraft:birch_forest', 'minecraft:old_growth_birch_forest',
               'minecraft:dark_forest', 'minecraft:pale_garden'],
    'cherry': ['minecraft:cherry_grove'],
    'desert': ['minecraft:desert'],
    'badlands': ['minecraft:badlands', 'minecraft:eroded_badlands', 'minecraft:wooded_badlands'],
    'savanna': ['minecraft:savanna', 'minecraft:savanna_plateau', 'minecraft:windswept_savanna'],
    'jungle': ['minecraft:jungle', 'minecraft:sparse_jungle', 'minecraft:bamboo_jungle'],
    'swamp': ['minecraft:swamp', 'minecraft:mangrove_swamp'],
    'snowy': ['minecraft:snowy_plains', 'minecraft:ice_spikes', 'minecraft:snowy_slopes', 'minecraft:frozen_peaks',
              'minecraft:snowy_beach'],
    'taiga': ['minecraft:taiga', 'minecraft:old_growth_pine_taiga', 'minecraft:old_growth_spruce_taiga', 'minecraft:snowy_taiga'],
    'mountain': ['minecraft:windswept_hills', 'minecraft:windswept_gravelly_hills', 'minecraft:windswept_forest',
                 'minecraft:stony_peaks', 'minecraft:jagged_peaks', 'minecraft:stony_shore', 'minecraft:grove'],
    'mushroom': ['minecraft:mushroom_fields'],
}
# The words residents use for a region in tall tales ("the rivers and lakes of the plains").
REGION_WORDS = {'plains': 'the plains', 'forest': 'the forests', 'cherry': 'the cherry groves', 'desert': 'the desert',
                'badlands': 'the badlands', 'savanna': 'the savanna', 'jungle': 'the jungle', 'swamp': 'the swamps',
                'snowy': 'the snowy north', 'taiga': 'the taiga', 'mountain': 'the mountains', 'mushroom': 'the mushroom isles'}

# Fishing gear: (id, name, kind, recipe or None). Effects live in dev.villagefriends.fishing.Gear.
GEAR = [
    ('reinforced_rod', 'Reinforced Rod', 'rod', {'shapeless': ['minecraft:fishing_rod', 'minecraft:iron_ingot', 'minecraft:iron_ingot', 'minecraft:string']}),
    ('anglers_rod', "Angler's Rod", 'rod', {'shapeless': [f'{NS}:reinforced_rod', 'minecraft:gold_ingot', 'minecraft:gold_ingot', 'minecraft:prismarine_shard']}),
    ('bait_worms', 'Bait Worms', 'bait', {'shapeless': ['minecraft:dirt', 'minecraft:bone_meal'], 'count': 6}),
    ('chum', 'Chum', 'bait', {'shapeless': [f'#{NS}:fishing/edible', 'minecraft:bone_meal'], 'count': 4}),
    ('glow_bait', 'Glow Bait', 'bait', {'shapeless': ['minecraft:glow_berries', f'{NS}:bait_worms', f'{NS}:bait_worms'], 'count': 2}),
    ('legend_lure', 'Legend Lure', 'bait', {'shapeless': ['minecraft:gold_ingot', 'minecraft:gold_ingot', 'minecraft:feather', 'minecraft:emerald', f'{NS}:glow_bait']}),
    ('cork_bobber', 'Cork Bobber', 'tackle', {'shapeless': ['#minecraft:wooden_buttons', 'minecraft:red_dye', 'minecraft:string']}),
    ('lead_sinker', 'Lead Sinker', 'tackle', {'shapeless': ['minecraft:iron_nugget', 'minecraft:iron_nugget', 'minecraft:iron_nugget', 'minecraft:string']}),
    ('barbed_hook', 'Barbed Hook', 'tackle', {'shapeless': ['minecraft:iron_nugget', 'minecraft:iron_nugget', 'minecraft:flint']}),
    ('treasure_hook', 'Treasure Hook', 'tackle', {'shapeless': ['minecraft:iron_nugget', 'minecraft:iron_nugget', 'minecraft:gold_ingot', 'minecraft:redstone']}),
    ('spinner', 'Spinner', 'tackle', {'shapeless': ['minecraft:iron_nugget', 'minecraft:copper_ingot', 'minecraft:string']}),
    ('anglers_journal', "Angler's Journal", 'item', {'shapeless': ['minecraft:book', f'#{NS}:fishing/fish']}),
    ('message_in_a_bottle', 'Message in a Bottle', 'item', None),
    ('grilled_fish', 'Grilled Fish', 'item', None),
    ('trophy_mount', 'Trophy Mount', 'block', {'shapeless': ['minecraft:item_frame', '#minecraft:planks', '#minecraft:planks']}),
]
# The fishmonger (the vanilla fisherman): what he sells at each level, and which fish he buys.
SELLS = {1: [('bait_worms', 16, 1), ('anglers_journal', 1, 3)],
         2: [('chum', 8, 1), ('cork_bobber', 1, 4), ('lead_sinker', 1, 4)],
         3: [('reinforced_rod', 1, 8), ('glow_bait', 8, 3), ('barbed_hook', 1, 6), ('spinner', 1, 6)],
         4: [('treasure_hook', 1, 10), ('trophy_mount', 1, 3)],
         5: [('anglers_rod', 1, 24), ('legend_lure', 1, 12)]}
BUYS = {1: ['minnow', 'perch', 'roach', 'herring', 'sardine', 'carp'],
        2: ['pike', 'brown_trout', 'river_eel', 'sea_bass', 'flounder', 'lobster'],
        3: ['catfish', 'zander', 'halibut', 'tuna'],
        4: ['sturgeon', 'swordfish']}
# How many of a fish buy one emerald (or, below one, emeralds for one fish).
PRICES = {'common': (8, 1), 'uncommon': (3, 1), 'rare': (1, 2), 'epic': (1, 5)}
OFFERS = {1: 3, 2: 3, 3: 3, 4: 3, 5: 2}


def fail(message):
    raise SystemExit(f'fish.tsv: {message}')


def read():
    rows, header = [], None
    for n, raw in enumerate((HERE / 'fish.tsv').read_text(encoding='utf-8').splitlines(), 1):
        if not raw.strip() or raw.startswith('#'):
            continue
        cells = raw.split('\t')
        if header is None:
            header = cells
            continue
        if len(cells) != len(header):
            fail(f'line {n}: {len(cells)} columns, expected {len(header)}')
        row = dict(zip(header, cells))
        row['_where'] = f'line {n} ({row["id"]})'
        rows.append(row)
    return rows


def listed(cell, allowed, where, what, any_ok=True):
    if cell == 'any' and any_ok:
        return []
    values = [v for v in cell.split(',') if v]
    bad = [v for v in values if v not in allowed]
    if bad or not values:
        fail(f'{where}: unknown {what} {bad or cell!r}')
    return values


def flags(f):
    return {x for x in f['flags'].split(',') if x and x != '-'}


def size(f):
    m = re.fullmatch(r'(\d+)-(\d+)', f['size'])
    if not m or int(m.group(1)) >= int(m.group(2)):
        fail(f'{f["_where"]}: size must be min-max centimetres')
    return int(m.group(1)), int(m.group(2))


def validate(fish):
    seen = set()
    for f in fish:
        w = f['_where']
        if not re.fullmatch(r'[a-z][a-z0-9_]*', f['id']) or f['id'] in seen:
            fail(f'{w}: bad or repeated id')
        seen.add(f['id'])
        if f['rarity'] not in RARITIES:
            fail(f'{w}: unknown rarity {f["rarity"]!r}')
        listed(f['water'], WATERS, w, 'water')
        listed(f['region'], set(REGIONS), w, 'region')
        listed(f['time'], TIMES, w, 'time')
        if f['weather'] not in WEATHERS:
            fail(f'{w}: unknown weather {f["weather"]!r}')
        listed(f['season'], SEASONS, w, 'season')
        size(f)
        if f['behavior'] not in BEHAVIORS:
            fail(f'{w}: unknown behavior {f["behavior"]!r}')
        if not 0 <= int(f['difficulty']) <= 100:
            fail(f'{w}: difficulty is 0 to 100')
        bad = flags(f) - FLAGS
        if bad:
            fail(f'{w}: unknown flags {sorted(bad)}')
        if f['rarity'] == 'legendary' and (f['region'] == 'any' and 'deep' not in f['water'] and 'deepcave' not in f['water']):
            fail(f'{w}: a legendary fish needs a region (or deep sea / deep caves) for its tall tale')
    ids = {f['id'] for f in fish}
    for level, names in BUYS.items():
        for name in names:
            if name not in ids:
                fail(f'BUYS level {level}: no fish {name!r}')
    if len(fish) < 60:
        fail(f'only {len(fish)} fish')


def item(f):
    return f'minecraft:{f["id"]}' if 'existing' in flags(f) else f'{NS}:{f["id"]}'


def edible(f):
    return f['rarity'] != 'legendary' and 'inedible' not in flags(f)


def food(f):
    """Raw nutrition from size: small fry 1, a good fish 2, a big one 3; shellfish are a little richer."""
    lo, hi = size(f)
    avg = (lo + hi) / 2
    n = 1 if avg < 20 else 2 if avg < 60 else 3
    if 'shellfish' in flags(f):
        n = max(2, n)
    return n, 0.2 if 'shellfish' in flags(f) else 0.1


def dump(data):
    return (json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def tag(values, replace=False):
    return dump({'replace': replace, 'values': values})


def runtime(fish):
    out = {'version': 1, 'regions': REGIONS, 'region_words': REGION_WORDS, 'fish': [],
           'gear': [{'id': g[0], 'kind': g[2]} for g in GEAR]}
    for f in fish:
        lo, hi = size(f)
        n, sat = food(f)
        out['fish'].append({
            'id': f['id'], 'item': item(f), 'name': f['name'], 'rarity': f['rarity'],
            'water': listed(f['water'], WATERS, '', ''), 'region': listed(f['region'], set(REGIONS), '', ''),
            'time': listed(f['time'], TIMES, '', ''), 'weather': f['weather'], 'season': listed(f['season'], SEASONS, '', ''),
            'size': [lo, hi], 'behavior': f['behavior'], 'difficulty': int(f['difficulty']),
            'food': 0 if not edible(f) else n, 'saturation': 0 if not edible(f) else sat,
            'flags': sorted(flags(f)), 'text': f['text']})
    return out


def shapeless(name, spec):
    ingredients = spec['shapeless']
    return dump({'type': 'minecraft:crafting_shapeless', 'category': 'equipment' if name.endswith('rod') else 'misc',
                 'ingredients': ingredients, 'result': {'id': f'{NS}:{name}', 'count': spec.get('count', 1)}})


def cooking(kind, time, xp):
    return dump({'type': f'minecraft:{kind}', 'category': 'food', 'cookingtime': time, 'experience': xp,
                 'ingredient': f'#{NS}:fishing/grillable', 'result': {'id': f'{NS}:grilled_fish'}})


def recipes():
    files = {}
    for name, _, _, spec in GEAR:
        if spec:
            files[DATA / f'{NS}/recipe/{name}.json'] = shapeless(name, spec)
    files[DATA / f'{NS}/loot_table/blocks/trophy_mount.json'] = dump({
        'type': 'minecraft:block', 'random_sequence': f'{NS}:blocks/trophy_mount',
        'pools': [{'rolls': 1, 'bonus_rolls': 0, 'entries': [{'type': 'minecraft:item', 'name': f'{NS}:trophy_mount'}],
                   'conditions': [{'condition': 'minecraft:survives_explosion'}]}]})
    files[DATA / f'{NS}/recipe/grilled_fish.json'] = cooking('smelting', 200, 0.35)
    files[DATA / f'{NS}/recipe/grilled_fish_from_smoking.json'] = cooking('smoking', 100, 0.35)
    files[DATA / f'{NS}/recipe/grilled_fish_from_campfire_cooking.json'] = cooking('campfire_cooking', 600, 0.35)
    return files


def tags(fish):
    files = {}
    ours = [f for f in fish if 'existing' not in flags(f)]
    files[DATA / f'{NS}/tags/item/fishing/fish.json'] = tag([item(f) for f in fish])
    files[DATA / f'{NS}/tags/item/fishing/edible.json'] = tag([item(f) for f in ours if edible(f)])
    files[DATA / f'{NS}/tags/item/fishing/grillable.json'] = tag([item(f) for f in ours if edible(f)
                                                                   and not flags(f) & {'shellfish', 'poison'}])
    files[DATA / f'{NS}/tags/item/fishing/treats.json'] = tag([item(f) for f in fish if edible(f)
                                                                and not flags(f) & {'notreat', 'poison'}])
    files[DATA / f'{NS}/tags/item/fishing/legendary.json'] = tag([item(f) for f in fish if f['rarity'] == 'legendary'])
    files[DATA / f'{NS}/tags/item/fishing/trout.json'] = tag([f'{NS}:brown_trout', f'{NS}:rainbow_trout'])
    rods = [f'{NS}:{g[0]}' for g in GEAR if g[2] == 'rod']
    files[DATA / f'{NS}/tags/item/fishing/rods.json'] = tag(['minecraft:fishing_rod'] + rods)
    files[DATA / f'{NS}/tags/item/fishing/bait.json'] = tag([f'{NS}:{g[0]}' for g in GEAR if g[2] == 'bait'])
    files[DATA / f'{NS}/tags/item/fishing/tackle.json'] = tag([f'{NS}:{g[0]}' for g in GEAR if g[2] == 'tackle'])
    files[DATA / 'minecraft/tags/item/fishes.json'] = tag([item(f) for f in ours])
    files[DATA / 'minecraft/tags/item/cat_food.json'] = tag([f'#{NS}:fishing/treats'])
    files[DATA / 'minecraft/tags/item/wolf_food.json'] = tag([f'#{NS}:fishing/treats'])
    files[DATA / 'minecraft/tags/item/enchantable/fishing.json'] = tag(rods)
    files[DATA / 'minecraft/tags/item/enchantable/durability.json'] = tag(rods)
    files[DATA / 'c/tags/item/tools/fishing_rod.json'] = tag(rods)
    files[DATA / 'c/tags/item/foods/raw_fish.json'] = tag([item(f) for f in ours if edible(f)])
    files[DATA / 'c/tags/item/foods/cooked_fish.json'] = tag([f'{NS}:grilled_fish'])
    return files


def trades(fish):
    files, levels = {}, {}
    rarity = {f['id']: f['rarity'] for f in fish}
    for level, offers in SELLS.items():
        for name, count, price in offers:
            files[DATA / f'{NS}/villager_trade/fisherman/{name}.json'] = dump({
                'wants': {'id': 'minecraft:emerald', 'count': price}, 'gives': {'id': f'{NS}:{name}', 'count': count},
                'max_uses': 12 if count > 1 else 4, 'xp': 2 + 3 * level, 'reputation_discount': 0.05})
            levels.setdefault(level, []).append(f'{NS}:fisherman/{name}')
    for level, names in BUYS.items():
        for name in names:
            count, emeralds = PRICES[rarity[name]]
            files[DATA / f'{NS}/villager_trade/fisherman/{name}_emerald.json'] = dump({
                'wants': {'id': f'{NS}:{name}', 'count': count}, 'gives': {'id': 'minecraft:emerald', 'count': emeralds},
                'max_uses': 16, 'xp': 2 + 3 * level, 'reputation_discount': 0.05})
            levels.setdefault(level, []).append(f'{NS}:fisherman/{name}_emerald')
    for level, values in levels.items():
        files[DATA / f'minecraft/tags/villager_trade/fisherman/level_{level}.json'] = tag(sorted(values))
    for level, amount in OFFERS.items():
        files[DATA / f'minecraft/trade_set/fisherman/level_{level}.json'] = dump({
            'amount': amount, 'random_sequence': f'minecraft:trade_set/fisherman/level_{level}',
            'trades': f'#minecraft:fisherman/level_{level}'})
    return files


def merged_json(path, update):
    raw = path.read_bytes() if path.exists() else b''
    current = json.loads(raw.decode('utf-8')) if raw else {}
    return raw, dump(update(current))


def lang(fish):
    names = {f'item.{NS}.{f["id"]}': f['name'] for f in fish if 'existing' not in flags(f)}
    for name, label, kind, _ in GEAR:
        names[f'{"block" if kind == "block" else "item"}.{NS}.{name}'] = label
    names[f'item.{NS}.trophy_fish'] = '%s (%s cm)'
    return names


def owned():
    fish = read()
    validate(fish)
    files = {RES / f'{NS}/fishing/fish.json': dump(runtime(fish))}
    files.update(recipes())
    files.update(tags(fish))
    files.update(trades(fish))
    return files, fish


def same(path, data):
    return path.exists() and path.read_bytes().replace(b'\r\n', b'\n') == data.replace(b'\r\n', b'\n')


def main():
    files, fish = owned()
    names = lang(fish)
    merged = {ASSETS / 'lang/en_us.json': merged_json(ASSETS / 'lang/en_us.json', lambda current: {**current, **names})}
    stale = [p for p in (DATA / f'{NS}/villager_trade/fisherman').glob('*.json') if p not in files]
    if '--stats' in sys.argv:
        print(f'{len(fish)} fish ({sum("existing" in flags(f) for f in fish)} vanilla)')
        print('by rarity:', dict(Counter(f['rarity'] for f in fish)))
        print('by water:', dict(Counter(w for f in fish for w in (f['water'].split(',')))))
        print('by region:', dict(Counter(r for f in fish for r in (f['region'].split(',')))))
        print('legendary:', ', '.join(f['name'] for f in fish if f['rarity'] == 'legendary'))
        return
    if '--check' in sys.argv:
        bad = [p for p, data in files.items() if not same(p, data)]
        bad += [p for p, (raw, data) in merged.items() if raw.replace(b'\r\n', b'\n') != data]
        bad += stale
        if bad:
            print('Out of date (run tools/fishing/fishing.py):\n  ' + '\n  '.join(str(p.relative_to(PROJECT)) for p in bad))
            sys.exit(1)
        print(f'Tall Tales Fishing data is up to date ({len(files)} files).')
        return
    for path, data in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    for path, (raw, data) in merged.items():
        if raw.replace(b'\r\n', b'\n') != data:
            path.write_bytes(data)
    for path in stale:
        path.unlink()
    print(f'Tall Tales Fishing: {len(files)} files, {len(fish)} fish.')


if __name__ == '__main__':
    main()
