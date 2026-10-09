"""Compiles Hearth & Harvest's data tables into the mod: the dish table the game reads at start-up, one
station recipe per dish, the crops' block models and loot, tags, farmer trades, the language file and
the farm processors that sow Hearth crops in village and homestead fields.

Sources (tab separated, '#' lines are comments):

  tools/hearth/dishes.tsv        every dish and kitchen ingredient, with its station recipe
  tools/hearth/crops.tsv         the six crops, their seeds and which village types grow them
  tools/hearth/ingredients.tsv   ingredients that drop from mobs (Not-So-Vanilla Mobs only)

Outputs:

  src/main/resources/villagefriends/hearth/dishes.json           items, food, Well Fed tiers, meals, likes
  data/villagefriends/hearth_recipe/<id>.json                    station recipes (fabric:load_conditions for other mods)
  data/villagefriends/loot_table/blocks/<crop>_crop.json         crop harvests; and the stations drop themselves
  data/villagefriends/recipe/<station>.json                      crafting recipes for the three stations
  data/villagefriends/villager_trade/farmer/*.json + vanilla farmer trade tags   farmers sell seeds and buy produce
  data/{c,minecraft,villagefriends}/tags/...                     c:crops, c:seeds, villager seeds, cooking/fish...
  assets/villagefriends/blockstates|models/block/<crop>_crop*    crop growth stages (textures: tools/hearth/sprites.py)
  assets/villagefriends/lang/en_us.json                          merged: names for everything here, other keys untouched
  tools/village_layouts/<type>.hearth.json                       '<base>_fields' processor lists, and the farm
                                                                 elements of every layout pointed at them

    python tools/hearth/hearth.py            # write everything
    python tools/hearth/hearth.py --check    # exit 1 if anything is out of date or the tables are inconsistent
    python tools/hearth/hearth.py --stats    # counts by station and tier

After changing farm processors run python tools/create_village_structures.py to compile the pools.
Art comes from tools/hearth/sprites.py (items, crop stages) and tools/hearth/stations.py (stations, GUI).
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
LAYOUTS = PROJECT / 'tools/village_layouts'
BLUEPRINTS = PROJECT / 'tools/village_blueprints'
NS = 'villagefriends'
FISH_TAG = f'{NS}:cooking/fish'

STATIONS = {'pot', 'oven', 'prep'}
SLOTS = 6
SERVES = {'stew', 'pie', 'bread', 'platter', 'tart', 'cider', '-'}
MEALS = {'breakfast', 'lunch', 'supper', 'tavern', 'picnic', 'party', 'winter'}
PERSONALITIES = {'warmhearted', 'thoughtful', 'playful', 'adventurous', 'meticulous', 'steadfast', 'reserved',
                 'imaginative', 'pragmatic', 'curious', 'protective', 'gentle'}
JOBS = {'farmer', 'fisherman', 'shepherd', 'fletcher', 'librarian', 'cartographer', 'cleric', 'armorer', 'weaponsmith',
        'toolsmith', 'butcher', 'leatherworker', 'mason', 'knight', 'archer', 'cook', 'tavern_keeper', 'apothecary',
        'painter', 'bard', 'tailor', 'carpenter', 'scholar'}
VESSELS = {'bowl': 'minecraft:bowl', 'bottle': 'minecraft:glass_bottle', '-': None}
# Every Minecraft item the recipes may use, so a typo fails here instead of in the game.
VANILLA = {'wheat', 'milk_bucket', 'carrot', 'potato', 'beetroot', 'brown_mushroom', 'red_mushroom', 'rabbit', 'beef',
           'mutton', 'chicken', 'porkchop', 'cod', 'salmon', 'egg', 'sugar', 'apple', 'honey_bottle', 'sweet_berries',
           'cocoa_beans', 'bread', 'cooked_beef', 'cooked_porkchop', 'cooked_chicken', 'cooked_mutton', 'cooked_cod',
           'cooked_salmon', 'baked_potato', 'bowl', 'glass_bottle', 'pumpkin', 'melon_slice', 'kelp', 'dried_kelp'}
# Village types whose farm templates are re-sown, and the stand-ins for crops the homesteads grow.
TYPES = ('plains', 'desert', 'savanna', 'snowy', 'taiga')
VANILLA_CROPS = ('minecraft:wheat', 'minecraft:carrots', 'minecraft:potatoes', 'minecraft:beetroots')
FIELD_SHARE = 0.32
# Farmers' trades: (level, crop or seed id, wants, gives).
SEED_TRADES = {'onion_seeds': 1, 'cabbage_seeds': 1, 'herb_seeds': 1, 'barley_seeds': 2, 'leek_seeds': 2, 'garlic_clove': 2}
PRODUCE_TRADES = {'onion': (2, 18), 'cabbage': (2, 12), 'garlic': (3, 16), 'leek': (3, 14), 'barley': (3, 20), 'herbs': (2, 20)}
STATION_BLOCKS = ('cooking_pot', 'clay_oven', 'prep_table')
STATION_NAMES = {'cooking_pot': 'Cooking Pot', 'clay_oven': 'Clay Oven', 'prep_table': 'Prep Table'}


def fail(message):
    raise SystemExit(f'hearth: {message}')


def table(name):
    rows, header = [], None
    for n, raw in enumerate((HERE / name).read_text(encoding='utf-8').splitlines(), 1):
        if not raw.strip() or raw.startswith('#'):
            continue
        cells = raw.split('\t')
        if header is None:
            header = cells
            continue
        if len(cells) != len(header):
            fail(f'{name}:{n}: {len(cells)} columns, the header has {len(header)}')
        rows.append(dict(zip(header, [c.strip() for c in cells])) | {'_where': f'{name}:{n}'})
    return rows


def read():
    crops, ingredients, dishes = table('crops.tsv'), table('ingredients.tsv'), table('dishes.tsv')
    ours = {c['id'] for c in crops} | {c['seed'] for c in crops} | {i['id'] for i in ingredients} | {d['id'] for d in dishes}
    seen = Counter([c['id'] for c in crops] + [c['seed'] for c in crops] + [i['id'] for i in ingredients] + [d['id'] for d in dishes])
    twice = [k for k, n in seen.items() if n > 1]
    if twice:
        fail(f'ids used twice: {twice}')
    return crops, ingredients, dishes, ours


def item_id(token, ours, where):
    if token.startswith('#'):
        tag = token[1:]
        if tag == 'fish':
            return '#' + FISH_TAG
        if ':' not in tag:
            fail(f'{where}: write tags as #namespace:path ({token})')
        return token
    if ':' in token:
        return token
    if token in ours:
        return f'{NS}:{token}'
    if token not in VANILLA:
        fail(f'{where}: unknown ingredient {token!r} (add it to VANILLA if it is a real Minecraft item)')
    return f'minecraft:{token}'


def ingredients_of(d, ours):
    out = []
    for token in [t.strip() for t in d['ingredients'].split(';') if t.strip()]:
        name, _, times = token.partition('*')
        out += [item_id(name, ours, d['_where'])] * (int(times) if times else 1)
    return out


def flags(d):
    return {f for f in d['flags'].split(',') if f and f != '-'}


def needs(d):
    return next((f.split(':', 1)[1] for f in flags(d) if f.startswith('needs:')), None)


def listed(cell, allowed, where, what):
    values = [v for v in cell.split(',') if v and v != '-']
    bad = [v for v in values if v not in allowed]
    if bad:
        fail(f'{where}: unknown {what} {bad}')
    return values


def validate(crops, ingredients, dishes, ours):
    signatures = {}
    for d in dishes:
        w, f = d['_where'], flags(d)
        if d['station'] not in STATIONS:
            fail(f'{w}: station must be one of {sorted(STATIONS)}')
        if d['vessel'] not in VESSELS:
            fail(f'{w}: vessel must be bowl, bottle or -')
        if d['serve'] not in SERVES:
            fail(f'{w}: serve must be one of {sorted(SERVES)}')
        listed(d['meals'], MEALS, w, 'meals')
        listed(d['likes'], PERSONALITIES | JOBS | {'child'}, w, 'likes')
        unknown = {x for x in f if not x.startswith('needs:')} - {'ingredient', 'existing', 'secret'}
        if unknown:
            fail(f'{w}: unknown flags {sorted(unknown)}')
        parts = ingredients_of(d, ours)
        grid = parts + ([VESSELS[d['vessel']]] if d['vessel'] != '-' and d['station'] != 'pot' else [])
        if not 1 <= len(grid) <= SLOTS:
            fail(f'{w}: {len(grid)} grid slots (1..{SLOTS})')
        tier = int(d['tier'])
        if 'ingredient' in f:
            if tier:
                fail(f'{w}: kitchen ingredients have tier 0')
        elif not 1 <= tier <= 3 or int(d['buff']) < 30:
            fail(f'{w}: dishes have tier 1-3 and a Well Fed time')
        if int(d['buff']) > 300:
            fail(f'{w}: Well Fed stays short (5 minutes at most)')
        key = (d['station'], d['vessel'] if d['station'] == 'pot' else '-', tuple(sorted(grid)))
        if key in signatures:
            fail(f'{w}: same recipe as {signatures[key]}')
        signatures[key] = d['id']
    for c in crops:
        listed(c['biomes'], set(TYPES) | {'homestead'}, c['_where'], 'biomes')


# -- outputs ---------------------------------------------------------------------------------------

def dump(data):
    return (json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def runtime(crops, ingredients, dishes, ours):
    out = {'version': 1, 'crops': [], 'ingredients': [], 'dishes': []}
    for c in crops:
        out['crops'].append({'id': c['id'], 'seed': c['seed'], 'food': int(c['food']), 'saturation': float(c['sat']),
                             'biomes': [b for b in c['biomes'].split(',') if b]})
    for i in ingredients:
        effect = None
        if i['raw_effect'] != '-':
            ns, path, seconds = i['raw_effect'].split(':')
            effect = {'effect': f'{ns}:{path}', 'seconds': int(seconds)}
        mod = i['source'].split(':')[0] if ':' in i['source'] else None
        lo, hi = (int(x) for x in i['drops'].split('-'))
        out['ingredients'].append({'id': i['id'], 'food': int(i['food']), 'saturation': float(i['sat']),
                                   'raw_effect': effect, 'needs': mod, 'source': i['source'], 'drops': [lo, hi]})
    for d in dishes:
        f = flags(d)
        out['dishes'].append({
            'id': d['id'], 'station': d['station'], 'existing': 'existing' in f, 'ingredient': 'ingredient' in f,
            'secret': 'secret' in f, 'needs': needs(d), 'food': int(d['food']), 'saturation': float(d['sat']),
            'tier': int(d['tier']), 'buff': int(d['buff']), 'serve': d['serve'], 'vessel': d['vessel'],
            'meals': listed(d['meals'], MEALS, d['_where'], 'meals'),
            'likes': listed(d['likes'], PERSONALITIES | JOBS | {'child'}, d['_where'], 'likes')})
    return out


def recipe(d, ours):
    grid = ingredients_of(d, ours)
    vessel = VESSELS[d['vessel']]
    data = {}
    mod = needs(d)
    if mod:
        data['fabric:load_conditions'] = [{'condition': 'fabric:all_mods_loaded', 'values': [mod]}]
    data |= {'station': d['station']}
    if vessel and d['station'] != 'pot':
        grid.append(vessel)
    data['ingredients'] = grid
    if vessel and d['station'] == 'pot':
        data['vessel'] = vessel
    data['result'] = {'id': f'{NS}:{d["id"]}', 'count': int(d['makes'])}
    data['time'] = int(float(d['time']) * 20)
    if 'secret' in flags(d):
        data['secret'] = True
    return data


def crop_assets(c):
    files, block = {}, f'{c["id"]}_crop'
    # Eight vanilla ages over four drawn stages, the way carrots and potatoes do it.
    stage = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3}
    files[ASSETS / f'blockstates/{block}.json'] = dump({'variants': {f'age={a}': {'model': f'{NS}:block/{block}_stage{s}'} for a, s in stage.items()}})
    for s in range(4):
        files[ASSETS / f'models/block/{block}_stage{s}.json'] = dump(
            {'parent': 'minecraft:block/crop', 'textures': {'crop': f'{NS}:block/{c["id"]}_stage{s}'}})
    lo, hi = (int(x) for x in c['drops'].split('-'))
    ripe = [{'condition': 'minecraft:block_state_property', 'block': f'{NS}:{block}', 'properties': {'age': '7'}}]
    files[DATA / f'{NS}/loot_table/blocks/{block}.json'] = dump({
        'type': 'minecraft:block',
        'functions': [{'function': 'minecraft:explosion_decay'}],
        'pools': [
            {'rolls': 1.0, 'bonus_rolls': 0.0, 'entries': [{'type': 'minecraft:alternatives', 'children': [
                {'type': 'minecraft:item', 'name': f'{NS}:{c["id"]}', 'conditions': ripe,
                 'functions': [{'function': 'minecraft:set_count', 'count': {'type': 'minecraft:uniform', 'min': lo, 'max': hi}, 'add': False}]},
                {'type': 'minecraft:item', 'name': f'{NS}:{c["seed"]}'}]}]},
            {'rolls': 1.0, 'bonus_rolls': 0.0, 'conditions': ripe, 'entries': [{'type': 'minecraft:item', 'name': f'{NS}:{c["seed"]}',
                'functions': [{'function': 'minecraft:apply_bonus', 'enchantment': 'minecraft:fortune',
                               'formula': 'minecraft:binomial_with_bonus_count', 'parameters': {'extra': 2, 'probability': 0.5714286}}]}]}],
        'random_sequence': f'{NS}:blocks/{block}'})
    return files


def station_loot(name):
    return dump({'type': 'minecraft:block', 'pools': [{'rolls': 1.0, 'bonus_rolls': 0.0,
        'entries': [{'type': 'minecraft:item', 'name': f'{NS}:{name}'}], 'conditions': [{'condition': 'minecraft:survives_explosion'}]}],
        'random_sequence': f'{NS}:blocks/{name}'})


# Crafting recipes for the stations: an iron pot with nugget handles, a brick-and-clay dome on a stone
# hearth, and a slab-topped table with a knife.
STATION_CRAFTING = {
    'cooking_pot': (['N N', 'I I', ' I '], {'N': 'minecraft:iron_nugget', 'I': 'minecraft:iron_ingot'}),
    'clay_oven': (['CBC', 'B B', 'SSS'], {'C': 'minecraft:clay_ball', 'B': 'minecraft:brick', 'S': '#minecraft:stone_crafting_materials'}),
    'prep_table': (['I  ', 'SSS', 'F F'], {'I': 'minecraft:iron_ingot', 'S': '#minecraft:wooden_slabs', 'F': '#minecraft:wooden_fences'}),
}


def station_recipe(name):
    pattern, key = STATION_CRAFTING[name]
    return dump({'type': 'minecraft:crafting_shaped', 'category': 'misc', 'result': {'id': f'{NS}:{name}', 'count': 1},
                 'pattern': pattern, 'key': key})


def tag(values, replace=False):
    return dump({'replace': replace, 'values': values})


def tags(crops, dishes):
    files = {}
    produce = [f'{NS}:{c["id"]}' for c in crops]
    seeds = [f'{NS}:{c["seed"]}' for c in crops]
    blocks = [f'{NS}:{c["id"]}_crop' for c in crops]
    files[DATA / 'c/tags/item/crops.json'] = tag(produce)
    files[DATA / 'c/tags/item/seeds.json'] = tag(seeds)
    for c in crops:
        files[DATA / f'c/tags/item/crops/{c["id"]}.json'] = tag([f'{NS}:{c["id"]}'])
        files[DATA / f'c/tags/item/seeds/{c["id"]}.json'] = tag([f'{NS}:{c["seed"]}'])
    meals = [d for d in dishes if 'ingredient' not in flags(d)]
    files[DATA / 'c/tags/item/foods.json'] = tag([f'{NS}:{d["id"]}' for d in meals if 'existing' not in flags(d)])
    files[DATA / 'c/tags/item/foods/soup.json'] = tag([f'{NS}:{d["id"]}' for d in meals if d['vessel'] == 'bowl' and 'existing' not in flags(d)])
    files[DATA / 'c/tags/item/foods/bread.json'] = tag([f'{NS}:{d["id"]}' for d in meals if d['serve'] == 'bread' and 'existing' not in flags(d)])
    files[DATA / 'c/tags/item/foods/pie.json'] = tag([f'{NS}:{d["id"]}' for d in meals if d['serve'] == 'pie' and 'existing' not in flags(d)])
    files[DATA / 'minecraft/tags/item/villager_plantable_seeds.json'] = tag(seeds)
    files[DATA / 'minecraft/tags/block/crops.json'] = tag(blocks)
    files[DATA / 'minecraft/tags/block/bee_growables.json'] = tag(blocks)
    files[DATA / 'minecraft/tags/block/maintains_farmland.json'] = tag(blocks)
    files[DATA / f'{NS}/tags/block/hearth/crops.json'] = tag(blocks)
    files[DATA / f'{NS}/tags/block/hearth/heat_sources.json'] = tag(['minecraft:campfire', 'minecraft:soul_campfire', 'minecraft:fire',
                                                                     'minecraft:soul_fire', 'minecraft:lava', 'minecraft:magma_block'])
    files[DATA / f'{NS}/tags/item/cooking/fish.json'] = tag(['minecraft:cod', 'minecraft:salmon', 'minecraft:cooked_cod', 'minecraft:cooked_salmon'])
    files[DATA / f'{NS}/tags/item/hearth/crops.json'] = tag(produce)
    files[DATA / f'{NS}/tags/item/hearth/seeds.json'] = tag(seeds)
    files[DATA / f'{NS}/tags/item/hearth/dishes.json'] = tag([f'{NS}:{d["id"]}' for d in meals])
    for meal in ('party', 'picnic', 'winter'):
        name = {'party': 'cakes', 'picnic': 'picnic', 'winter': 'preserved'}[meal]
        files[DATA / f'{NS}/tags/item/hearth/{name}.json'] = tag([f'{NS}:{d["id"]}' for d in meals if meal in d['meals'].split(',')
                                                                   and (meal != 'party' or d['serve'] == 'tart')])
    return files


def trades(crops):
    files, levels = {}, {}
    for c in crops:
        seed = c['seed']
        files[DATA / f'{NS}/villager_trade/farmer/{seed}.json'] = dump({'wants': {'id': 'minecraft:emerald'}, 'gives': {'id': f'{NS}:{seed}', 'count': 6},
                                                                       'max_uses': 12, 'xp': 1, 'reputation_discount': 0.05})
        levels.setdefault(SEED_TRADES[seed], []).append(f'{NS}:farmer/{seed}')
        level, count = PRODUCE_TRADES[c['id']]
        files[DATA / f'{NS}/villager_trade/farmer/{c["id"]}_emerald.json'] = dump({'wants': {'id': f'{NS}:{c["id"]}', 'count': count},
                                                                                 'gives': {'id': 'minecraft:emerald'}, 'max_uses': 16, 'xp': 2 * level,
                                                                                 'reputation_discount': 0.05})
        levels.setdefault(level, []).append(f'{NS}:farmer/{c["id"]}_emerald')
    for level, values in levels.items():
        files[DATA / f'minecraft/tags/villager_trade/farmer/level_{level}.json'] = tag(sorted(values))
    return files


# -- merged files (other tools own the rest of them) ----------------------------------------------

def merged_json(path, update):
    raw = path.read_bytes() if path.exists() else b''
    current = json.loads(raw.decode('utf-8')) if raw else {}
    return raw, dump(update(current))


def lang(crops, ingredients, dishes):
    names = {}
    for c in crops:
        names[f'item.{NS}.{c["id"]}'] = c['name']
        names[f'item.{NS}.{c["seed"]}'] = c['seed_name']
        names[f'block.{NS}.{c["id"]}_crop'] = {'onion': 'Onions', 'cabbage': 'Cabbages', 'barley': 'Barley', 'garlic': 'Garlic',
                                               'leek': 'Leeks', 'herbs': 'Kitchen Herbs'}.get(c['id'], c['name'])
    for i in ingredients:
        names[f'item.{NS}.{i["id"]}'] = i['name']
    for d in dishes:
        if 'existing' not in flags(d):
            names[f'item.{NS}.{d["id"]}'] = d['name']
    for block, name in STATION_NAMES.items():
        names[f'block.{NS}.{block}'] = name
        names[f'container.{NS}.{block}'] = name
    names[f'item.{NS}.recipe_card'] = 'Recipe Card'
    names[f'item.{NS}.recipe_card.named'] = 'Recipe Card: %s'
    names[f'item.{NS}.fine_dish'] = 'Fine %s'
    names[f'effect.{NS}.well_fed'] = 'Well Fed'
    return names


def merged_files(crops, ingredients, dishes):
    out = {}
    names = lang(crops, ingredients, dishes)
    out[ASSETS / 'lang/en_us.json'] = merged_json(ASSETS / 'lang/en_us.json', lambda current: {**current, **names})

    def add(values):
        def update(current):
            have = list(current.get('values', []))
            return {'replace': current.get('replace', False), 'values': sorted(set(have) | set(values))}
        return update
    out[DATA / 'minecraft/tags/block/mineable/axe.json'] = merged_json(DATA / 'minecraft/tags/block/mineable/axe.json', add([f'{NS}:prep_table']))
    out[DATA / 'minecraft/tags/block/mineable/pickaxe.json'] = merged_json(DATA / 'minecraft/tags/block/mineable/pickaxe.json',
                                                                            add([f'{NS}:cooking_pot', f'{NS}:clay_oven']))
    return out


# -- farm processors ------------------------------------------------------------------------------

def crop_templates():
    """Templates whose blueprint plants a vanilla crop: village fields, kitchen gardens, greenhouses."""
    names = set()
    for path in BLUEPRINTS.rglob('*.json'):
        text = path.read_text(encoding='utf-8')
        if any(re.search(r'"(minecraft:)?' + c.split(':')[1] + r'"', text) for c in VANILLA_CROPS):
            names.add(path.relative_to(BLUEPRINTS).with_suffix('').as_posix())
    return names


def field_rules(crop_ids):
    """A rule processor that swaps about a third of a field's vanilla crops for this village's Hearth crops."""
    share = 1 - (1 - FIELD_SHARE) ** (1 / len(crop_ids))
    rules = []
    for vanilla in VANILLA_CROPS:
        for n, crop in enumerate(crop_ids):
            rules.append({'input_predicate': {'predicate_type': 'minecraft:random_block_match', 'block': vanilla, 'probability': round(share, 4)},
                          'location_predicate': {'predicate_type': 'minecraft:always_true'},
                          'output_state': {'Name': f'{NS}:{crop}_crop', 'Properties': {'age': '7' if (n + len(vanilla)) % 3 else '5'}}})
    return {'processor_type': 'minecraft:rule', 'rules': rules}


def fields(crops):
    """The <type>.hearth.json fragments, and every layout file with its crop-bearing elements re-pointed."""
    grown = {t: [c['id'] for c in crops if t in c['biomes'].split(',')] for t in TYPES + ('homestead',)}
    templates = crop_templates()
    layouts = {p: json.loads(p.read_text(encoding='utf-8')) for p in sorted(LAYOUTS.glob('*.json')) if '.hearth.' not in p.name}
    defined = {}
    for data in layouts.values():
        defined.update(data.get('processor_lists', {}))
    defined.setdefault('village', [])
    out, made = {}, {t: {} for t in TYPES}
    for path, data in layouts.items():
        kind = data['type']
        changed = False
        for pool in data.get('pools', {}).values():
            for element in pool.get('elements', []) if isinstance(pool, dict) else []:
                if element.get('template') not in templates:
                    continue
                current = element.get('processors', 'village')
                base = re.sub(rf'^{kind}_(.+)_fields$', r'\1', current)
                name = f'{kind}_{base}_fields'
                made[kind][name] = defined[base] + [field_rules(grown[kind])]
                if current != name:
                    element['processors'] = name
                    changed = True
        out[path] = dump(data) if changed else None
    for kind in TYPES:
        lists = dict(sorted(made[kind].items()))
        if kind == 'plains':
            # Homesteads (tools/homesteads.json) sow their fields with the homestead crops.
            lists['homestead_fields'] = defined['village'] + [field_rules(grown['homestead'])]
        out[LAYOUTS / f'{kind}.hearth.json'] = dump({'format': 3, 'type': kind,
            'part': 'Hearth & Harvest: farm processors written by tools/hearth/hearth.py (never edit by hand)',
            'processor_lists': lists})
    return out


# -- driver ---------------------------------------------------------------------------------------

def owned():
    crops, ingredients, dishes, ours = read()
    validate(crops, ingredients, dishes, ours)
    files = {RES / f'{NS}/hearth/dishes.json': dump(runtime(crops, ingredients, dishes, ours))}
    for d in dishes:
        files[DATA / f'{NS}/hearth_recipe/{d["id"]}.json'] = dump(recipe(d, ours))
    for c in crops:
        files.update(crop_assets(c))
    for block in STATION_BLOCKS:
        files[DATA / f'{NS}/loot_table/blocks/{block}.json'] = station_loot(block)
        files[DATA / f'{NS}/recipe/{block}.json'] = station_recipe(block)
    files.update(tags(crops, dishes))
    files.update(trades(crops))
    return files, (crops, ingredients, dishes)


def same(path, data):
    return path.exists() and path.read_bytes().replace(b'\r\n', b'\n') == data.replace(b'\r\n', b'\n')


def main():
    files, (crops, ingredients, dishes) = owned()
    merged = merged_files(crops, ingredients, dishes)
    layouts = fields(crops)
    stale_recipes = [p for p in (DATA / f'{NS}/hearth_recipe').glob('*.json') if p not in files]
    if '--stats' in sys.argv:
        meals = [d for d in dishes if 'ingredient' not in flags(d)]
        print(f'{len(meals)} dishes ({sum("existing" in flags(d) for d in meals)} already in the mod), '
              f'{len(dishes) - len(meals)} kitchen ingredients, {len(crops)} crops, {len(ingredients)} mob ingredients')
        print('by station:', dict(Counter(d['station'] for d in meals)))
        print('by tier:', dict(Counter(d['tier'] for d in meals)))
        print('secret:', sum('secret' in flags(d) for d in meals), ' needs another mod:', sum(bool(needs(d)) for d in meals))
        return
    if '--check' in sys.argv:
        bad = [p for p, data in files.items() if not same(p, data)]
        bad += [p for p, (raw, data) in merged.items() if raw.replace(b'\r\n', b'\n') != data]
        bad += [p for p, data in layouts.items() if data is not None and not same(p, data)]
        bad += stale_recipes
        if bad:
            print('Out of date (run tools/hearth/hearth.py):\n  ' + '\n  '.join(str(p.relative_to(PROJECT)) for p in bad))
            sys.exit(1)
        print(f'Hearth & Harvest data is up to date ({len(files)} files).')
        return
    for path, data in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    for path, (raw, data) in merged.items():
        if raw.replace(b'\r\n', b'\n') != data:
            path.write_bytes(data)
    for path, data in layouts.items():
        if data is not None:
            path.write_bytes(data)
    for path in stale_recipes:
        path.unlink()
    print(f'Hearth & Harvest: {len(files)} files, {len(dishes)} recipes, {len(crops)} crops.')


if __name__ == '__main__':
    main()
