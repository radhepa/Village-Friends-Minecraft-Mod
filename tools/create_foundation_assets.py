"""Reproduce Phase 1 models, original pixel art, recipes, tags, trades and catalog.

Geometry and IDs come from the Java registries so block collision and models agree.
Run from any directory with Python + Pillow. This merges shared language/tag files.
"""
from pathlib import Path
from PIL import Image, ImageDraw
from item_sprites import item_sprite
import json
import re

PROJECT = Path(__file__).resolve().parent.parent
ROOT = PROJECT / 'src/main/resources'
JAVA = PROJECT / 'src/main/java/dev/villagefriends'
NS = 'villagefriends'
COLORS = {
    'knight': '#748698', 'archer': '#456949', 'cook': '#E0D4B4',
    'tavern_keeper': '#9C603C', 'apothecary': '#5F977D', 'painter': '#AD8056',
    'bard': '#8E597C', 'tailor': '#427E92', 'carpenter': '#B08242', 'scholar': '#694C87',
    'rain_cloak': '#356B77', 'hooded_poncho': '#AC883E',
}


def save(path, data):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def merge(path, values):
    dest = ROOT / path
    data = json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else {}
    data.update(values)
    save(path, data)


def tag(path, values):
    dest = ROOT / path
    data = json.loads(dest.read_text(encoding='utf-8')) if dest.exists() else {'replace': False, 'values': []}
    data['values'] = sorted(set(data['values']) | set(values))
    save(path, data)


def png(path, image):
    dest = ROOT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    image.save(dest)


def boxes(text):
    return [list(map(int, row.split(','))) for row in re.findall(r'\{([\d,]+)\}', text)]


source = (JAVA / 'VillageBlocks.java').read_text(encoding='utf-8')
bench = boxes(re.search(r'double\[\]\[\] bench = (.*?);', source).group(1))
blocks = {}
for match in re.finditer(r'(add|station)\("([^"]+)", (true|false), (new double\[\]\[\]\{.*?\}|bench)(?:, FoundationEntityBlock.Kind.([A-Z_]+))?\);', source):
    kind, name, stone, geometry, entity = match.groups()
    blocks[name] = {'boxes': bench if geometry == 'bench' else boxes(geometry), 'stone': stone == 'true',
                    'block_entity': entity is not None or kind == 'station', 'workstation': kind == 'station'}
assert len(blocks) == 17, 'Update the generator when the registry changes.'
jobs = re.findall(r'"([a-z_]+)"', re.search(r'JOBS = List.of\((.*?)\);', (JAVA / 'VillageProfessions.java').read_text()).group(1))
workstations = {
    match[0]: re.findall(r'"([a-z_]+)"', match[1])
    for match in re.findall(r'case "([a-z_]+)" -> List.of\((.*?)\);', (JAVA / 'VillageProfessions.java').read_text())
}
supplies = ['smelling_salts', 'revival_tonic', 'bandage_wrap', 'empty_coffee_mug']
meals = ['steaming_coffee_mug', 'mug_of_cider', 'fresh_village_bread', 'hearty_stew']
tools = ['broom', 'paintbrush', 'lute', 'carpenter_hammer', 'field_journal']
wearables = ['rain_cloak', 'hooded_poncho'] + [job + '_uniform' for job in jobs]
items = supplies + meals + tools + wearables
language = {'itemGroup.villagefriends': 'Village Friends'}


def block_art(name, stone):
    image = Image.new('RGBA', (16, 16), '#73766E' if stone else '#A17B51')
    d = ImageDraw.Draw(image)
    d.rectangle((0, 0, 15, 15), outline='#44382E')
    for y in (3, 7, 11):
        d.line((1, y, 14, y), fill='#62655D' if stone else '#8A653E')
    if name == 'archery_target':
        for rect, color in [((2,2,13,13),'#EBDDBB'),((4,4,11,11),'#AD493E'),((6,6,9,9),'#EBDDBB'),((7,7,8,8),'#AD493E')]: d.ellipse(rect,fill=color)
    elif name == 'training_dummy':
        d.rectangle((5,2,10,5), fill='#DEBF71');d.rectangle((3,7,12,11),fill='#BA9250');d.line((8,3,8,13),fill='#695034')
    elif name == 'kitchen_stove':
        d.rectangle((3,4,12,12),fill='#373C3B');d.rectangle((5,7,10,11),fill='#BB6838');d.line((4,5,11,5),fill='#9DA39B')
    elif name in ('drinks_barrel', 'tap_stand'):
        for y in (2,12): d.rectangle((1,y,14,y+1),fill='#4A4D48')
        d.rectangle((7,6,9,8),fill='#C1A56C');d.line((8,9,8,11),fill='#E5BE68')
    elif name == 'alchemical_press':
        d.rectangle((6,2,9,5),fill='#C7D8B3');d.rectangle((4,6,11,12),fill='#51846B');d.line((6,7,6,10),fill='#94C7A6')
    elif name == 'easel_canvas':
        d.rectangle((2,2,13,13),fill='#E8DCC0');d.rectangle((3,9,12,12),fill='#6E9562');d.ellipse((8,3,11,6),fill='#D7AE4A');d.polygon([(3,10),(7,6),(11,10)],fill='#728C96')
    elif name == 'music_stand':
        d.rectangle((3,2,12,13),fill='#EBDEBE');d.line((9,4,9,10),fill='#604339',width=2);d.ellipse((5,9,9,12),fill='#604339');d.line((9,4,11,5),fill='#604339')
    elif name == 'sewing_table':
        d.rectangle((2,3,13,12),fill='#CBB8A4');d.line((4,5,11,10),fill='#5C8190',width=2);d.line((11,5,4,10),fill='#5C8190',width=2)
    elif name == 'sawmill':
        d.ellipse((3,3,12,12),fill='#B5BBB1');d.line((8,2,8,13),fill='#5D655F');d.line((2,8,13,8),fill='#5D655F');d.ellipse((7,7,9,9),fill='#5D655F')
    elif name == 'archives':
        for i,c in enumerate(['#755384','#547B68','#B86F49','#B7A26A']):d.rectangle((2+i*3,3,3+i*3,12),fill=c);d.point((2+i*3,5),fill='#E7D5A4')
        d.line((1,13,14,13),fill='#4B3528')
    elif name in ('village_bench', 'campfire_bench'):
        for y in (3,7,11):d.line((2,y,13,y),fill='#D5B77B')
        if name == 'campfire_bench':d.polygon([(6,11),(5,7),(8,4),(11,8),(9,11)],fill='#C9763F')
    elif name == 'apothecary_cot':
        d.rectangle((1,2,14,13),fill='#DBDEC6');d.rectangle((7,4,9,11),fill='#567D6B');d.rectangle((4,7,12,9),fill='#567D6B')
    elif name == 'house_plaque':
        d.polygon([(3,7),(8,3),(13,7)],fill='#E2C99A');d.rectangle((4,8,11,13),fill='#E2C99A');d.rectangle((7,10,8,13),fill='#705137')
    elif name == 'notice_board':
        d.rectangle((3,2,10,9),fill='#EEE0BC');d.rectangle((7,6,13,13),fill='#D6CCA3');d.point((6,3),fill='#9E4B3C');d.line((4,5,8,5),fill='#90846E')
    elif name == 'command_desk':
        d.rectangle((2,3,13,12),fill='#DCD5AD');d.line([(3,9),(6,6),(9,8),(12,5)],fill='#748D63',width=2);d.point((8,6),fill='#A74F3D')
    return image


for name, entry in blocks.items():
    language[f'block.{NS}.{name}'] = name.replace('_', ' ').title()
    save(f'data/{NS}/loot_table/blocks/{name}.json', {'type': 'minecraft:block', 'pools': [{'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': f'{NS}:{name}'}], 'conditions': [{'condition': 'minecraft:survives_explosion'}]}]})
    if entry['workstation']:
        continue  # Workstation models and art come from tools/workstations/workstations.py.
    png(f'assets/{NS}/textures/block/{name}.png', block_art(name, entry['stone']))
    model = {'parent': 'minecraft:block/block', 'textures': {'surface': f'{NS}:block/{name}', 'side': 'minecraft:block/polished_andesite' if entry['stone'] else 'minecraft:block/stripped_oak_log', 'particle': f'{NS}:block/{name}'},
             'elements': [{'from': b[:3], 'to': b[3:], 'faces': {face: {'texture': '#surface' if face in ('north','south','up') else '#side', 'uv': [0,0,16,16]} for face in ('down','up','north','south','east','west')}} for b in entry['boxes']]}
    save(f'assets/{NS}/models/block/{name}.json', model)
    save(f'assets/{NS}/blockstates/{name}.json', {'variants': {f'facing={direction}': {'model': f'{NS}:block/{name}', 'y': rotation} for direction,rotation in [('north',0),('east',90),('south',180),('west',270)]}})
    save(f'assets/{NS}/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'{NS}:block/{name}'}})
tag('data/minecraft/tags/block/mineable/axe.json', [f'{NS}:{name}' for name,b in blocks.items() if not b['stone']])
tag('data/minecraft/tags/block/mineable/pickaxe.json', [f'{NS}:{name}' for name,b in blocks.items() if b['stone']])
tag('data/minecraft/tags/point_of_interest_type/acquirable_job_site.json', [f'{NS}:{job}' for job in jobs])


def icon(name):
    return item_sprite(name)


for name in items:
    png(f'assets/{NS}/textures/item/{name}.png', icon(name))
    save(f'assets/{NS}/models/item/{name}.json', {'parent': 'minecraft:item/handheld' if name in tools[:4] else 'minecraft:item/generated', 'textures': {'layer0': f'{NS}:item/{name}'}})
    save(f'assets/{NS}/items/{name}.json', {'model': {'type': 'minecraft:model', 'model': f'{NS}:item/{name}'}})
    language[f'item.{NS}.{name}'] = name.replace('_',' ').title().replace(' Of ', ' of ')
for name in wearables:
    image = Image.new('RGBA',(64,32))
    d = ImageDraw.Draw(image)
    color = COLORS[name.removesuffix('_uniform')]
    for rect in [(16,16,39,31),(40,16,55,31)]:d.rectangle(rect,fill=color)
    d.line((20,27,35,27),fill='#574B3C',width=2);d.rectangle((22,21,23,26),fill='#DACA9F');d.rectangle((27,23,30,25),fill='#DACA9F')
    d.line((44,29,47,29),fill='#DACA9F');d.line((52,29,55,29),fill='#DACA9F')
    png(f'assets/{NS}/textures/entity/equipment/humanoid/{name}.png', image)
    save(f'assets/{NS}/equipment/{name}.json', {'layers': {'humanoid': [{'texture': f'{NS}:{name}'}], 'humanoid_baby': [{'texture': f'{NS}:{name}'}]}})

recipes = {}


def recipe(name, ingredients=None, pattern=None, key=None, count=1, category='misc'):
    data = {'type': 'minecraft:crafting_shaped' if pattern else 'minecraft:crafting_shapeless', 'category': category, 'result': {'id': f'{NS}:{name}', 'count': count}}
    if pattern: data.update(pattern=pattern, key=key)
    else: data['ingredients'] = ingredients
    recipes[name] = data
    save(f'data/{NS}/recipe/{name}.json', data)
    material = 'minecraft:oak_planks' if name in blocks else 'minecraft:paper' if name in tools else 'minecraft:white_wool' if name in wearables else 'minecraft:glass_bottle' if name in ('smelling_salts','revival_tonic') else 'minecraft:wheat' if name in meals else 'minecraft:paper'
    save(f'data/{NS}/advancement/recipes/foundation/{name}.json', {'parent':'minecraft:recipes/root','criteria':{'has_material':{'trigger':'minecraft:inventory_changed','conditions':{'items':[{'items':material}]}},'has_recipe':{'trigger':'minecraft:recipe_unlocked','conditions':{'recipes':f'{NS}:{name}'}}},'requirements':[['has_material','has_recipe']],'rewards':{'recipes':[f'{NS}:{name}']}})


materials = {
    'training_dummy': ('minecraft:hay_block','minecraft:stick'), 'archery_target': ('minecraft:target','minecraft:stick'),
    'kitchen_stove': ('minecraft:furnace','minecraft:cauldron'), 'drinks_barrel': ('minecraft:barrel','minecraft:glass_bottle'),
    'tap_stand': ('minecraft:barrel','minecraft:copper_ingot'), 'alchemical_press': ('minecraft:brewing_stand','minecraft:iron_ingot'),
    'easel_canvas': ('minecraft:paper','minecraft:stick'), 'music_stand': ('minecraft:note_block','minecraft:book'),
    'sewing_table': ('minecraft:loom','minecraft:shears'), 'sawmill': ('minecraft:iron_ingot','minecraft:iron_axe'),
    'archives': ('minecraft:bookshelf','minecraft:book'), 'village_bench': ('minecraft:oak_slab','minecraft:stick'),
    'campfire_bench': ('minecraft:oak_log','minecraft:stick'), 'apothecary_cot': ('minecraft:white_wool','minecraft:stick'),
    'house_plaque': ('minecraft:oak_sign','minecraft:paper'), 'notice_board': ('minecraft:oak_sign','minecraft:book'),
    'command_desk': ('minecraft:map','minecraft:iron_ingot'),
}
for name,(a,b) in materials.items():
    recipe(name, pattern=[' A ','PBP',' P '], key={'A':a,'B':b,'P':'#minecraft:planks'}, category='building')
recipe('smelling_salts', ['minecraft:blaze_powder','minecraft:sugar','minecraft:glass_bottle'])
recipe('revival_tonic', ['minecraft:golden_apple','minecraft:glistering_melon_slice',{'fabric:type':'fabric:components','base':'minecraft:potion','components':{'minecraft:potion_contents':{'potion':'minecraft:awkward'}}}])
recipe('bandage_wrap', ['minecraft:paper','#minecraft:wool'], count=2)
recipe('empty_coffee_mug', pattern=['C C',' C '], key={'C':'minecraft:brick'})
recipe('steaming_coffee_mug', [f'{NS}:empty_coffee_mug','minecraft:cocoa_beans','minecraft:sugar'])
recipe('fresh_village_bread', ['minecraft:wheat','minecraft:wheat','minecraft:wheat','minecraft:honey_bottle'])
recipe('hearty_stew', ['minecraft:bowl','minecraft:baked_potato','minecraft:carrot','minecraft:cooked_beef'])
for name in wearables:
    job = name.removesuffix('_uniform')
    accent = {'knight':'minecraft:iron_ingot','archer':'minecraft:feather','cook':'minecraft:wheat','tavern_keeper':'minecraft:glass_bottle','apothecary':'minecraft:green_dye','painter':'minecraft:blue_dye','bard':'minecraft:amethyst_shard','tailor':'minecraft:string','carpenter':'minecraft:stick','scholar':'minecraft:book','rain_cloak':'minecraft:blue_dye','hooded_poncho':'minecraft:yellow_dye'}[job]
    recipe(name, pattern=['W W','WAW','WWW'],key={'W':'#minecraft:wool','A':accent})
for name,a,b in [('broom','minecraft:hay_block','minecraft:stick'),('paintbrush','minecraft:feather','minecraft:stick'),('lute','minecraft:string','minecraft:oak_planks'),('carpenter_hammer','minecraft:iron_ingot','minecraft:stick'),('field_journal','minecraft:book','minecraft:feather')]:
    recipe(name, [a,b])

# Native data-driven trade sets, two offers per level: sell products and buy supplies.
products = {
    'knight': ['minecraft:stone_sword','minecraft:shield','minecraft:iron_sword',f'{NS}:knight_uniform','minecraft:diamond_sword'],
    'archer': ['minecraft:arrow','minecraft:bow','minecraft:crossbow',f'{NS}:archer_uniform','minecraft:spectral_arrow'],
    'cook': [f'{NS}:fresh_village_bread',f'{NS}:hearty_stew',f'{NS}:steaming_coffee_mug',f'{NS}:cook_uniform','minecraft:golden_carrot'],
    'tavern_keeper': [f'{NS}:steaming_coffee_mug','minecraft:honey_bottle',f'{NS}:hearty_stew',f'{NS}:tavern_keeper_uniform','minecraft:golden_apple'],
    'apothecary': [f'{NS}:bandage_wrap',f'{NS}:smelling_salts',f'{NS}:revival_tonic',f'{NS}:apothecary_uniform','minecraft:golden_apple'],
    'painter': [f'{NS}:paintbrush','minecraft:painting','minecraft:blue_dye',f'{NS}:painter_uniform','minecraft:glow_item_frame'],
    'bard': ['minecraft:note_block',f'{NS}:lute','minecraft:jukebox',f'{NS}:bard_uniform','minecraft:music_disc_cat'],
    'tailor': [f'{NS}:rain_cloak',f'{NS}:hooded_poncho','minecraft:shears',f'{NS}:tailor_uniform','minecraft:lead'],
    'carpenter': [f'{NS}:broom',f'{NS}:carpenter_hammer',f'{NS}:village_bench',f'{NS}:carpenter_uniform',f'{NS}:command_desk'],
    'scholar': [f'{NS}:field_journal','minecraft:book','minecraft:map',f'{NS}:scholar_uniform','minecraft:bookshelf'],
}
buying = {'knight':'minecraft:iron_ingot','archer':'minecraft:feather','cook':'minecraft:wheat','tavern_keeper':'minecraft:cocoa_beans','apothecary':'minecraft:paper','painter':'minecraft:clay_ball','bard':'minecraft:string','tailor':'minecraft:white_wool','carpenter':'minecraft:oak_log','scholar':'minecraft:paper'}
for job in jobs:
    language[f'entity.{NS}.villager.{job}'] = job.replace('_',' ').title()
    for level,product in enumerate(products[job], 1):
        prefix = f'{job}/level_{level}'
        save(f'data/{NS}/villager_trade/{prefix}_sell.json', {'wants': {'id':'minecraft:emerald','count':[2,4,8,12,20][level-1]},'gives':{'id':product,'count':8 if product.endswith(':arrow') or product.endswith(':spectral_arrow') else 1},'max_uses':12,'xp':[2,5,10,15,30][level-1],'reputation_discount':0.05})
        save(f'data/{NS}/villager_trade/{prefix}_buy.json', {'wants':{'id':buying[job],'count':max(4,20-level*3)},'gives':{'id':'minecraft:emerald'},'max_uses':16,'xp':[2,5,10,15,30][level-1],'reputation_discount':0.05})
        save(f'data/{NS}/trade_set/{prefix}.json', {'trades':[f'{NS}:{prefix}_sell',f'{NS}:{prefix}_buy'],'amount':2,'random_sequence':f'{NS}:trade_set/{prefix}'})
merge(f'assets/{NS}/lang/en_us.json', language)
save(f'data/{NS}/villagefriends/foundation-catalog.json', {'phase':1,'professions':workstations,'blocks':blocks,'items':items,'wearables':wearables,'recipes':list(recipes),'trade_levels':5})

# A contact sheet is a development artifact, not included in the mod.
sheet = Image.new('RGB',(8*100,6*74),'#EBE4D2');draw=ImageDraw.Draw(sheet)
for n,name in enumerate(list(blocks)+items):
    x,y=(n%8)*100,(n//8)*74
    part=(block_art(name,blocks[name]['stone']) if name in blocks else icon(name))
    sheet.paste(part.resize((40,40),Image.Resampling.NEAREST),(x+30,y+2),part.resize((40,40),Image.Resampling.NEAREST))
    title=name.replace('_',' ').title()
    for line,text in enumerate([title[:16],title[16:]]):draw.text((x+2,y+44+line*12),text,fill='#443D35')
dest=PROJECT/'build/phase1-assets.png';dest.parent.mkdir(parents=True,exist_ok=True);sheet.save(dest)
item_sheet=Image.new('RGB',(8*144,3*128),'#C6C6C6');item_draw=ImageDraw.Draw(item_sheet)
for n,name in enumerate(items):
    x,y=n%8*144,n//8*128
    sprite=icon(name).resize((80,80),Image.Resampling.NEAREST)
    item_sheet.paste(sprite,(x+32,y+6),sprite)
    words=name.replace('_',' ').title().split();lines=['']
    for word in words:
        if len(lines[-1])+len(word)>20:lines.append(word)
        else:lines[-1]=(lines[-1]+' '+word).strip()
    for line,title in enumerate(lines):item_draw.text((x+8,y+94+line*12),title,fill='#292929')
item_sheet.save(PROJECT/'build/phase1-item-sprites.png')
print(f'Phase 1: {len(jobs)} professions, {len(blocks)} blocks, {len(items)} items, {len(recipes)} recipes, 50 trade sets, 100 offers.')
