"""Snowy trade workshops: each holds a vanilla job site block and no residents.

Unemployed residents of nearby homes take up the trade. Every workshop is a
drop-in lot with a north-facing ``building_entrance`` at [x,1,0] and a path
to its door or open front.
"""
import random

from ...kit import Build
from ... import parts
from .palette import STYLES, ROOFS
from . import homes_kit as k

LOOT = 'minecraft:chests/village/village_'


def log_shell(b, x0, z0, x1, z1, roof, axis, pitch=2, gable='spruce_planks', ceiling=True):
    """Log-walled hut on a cobblestone plinth (floor at Y=1, walls Y=2..4); returns the ridge Y."""
    parts.foundation(b, x0, z0, x1, z1, STYLES['cabin'], top=1)
    k.log_walls(b, x0, z0, x1, z1, 2, 4)
    parts.beam_ring(b, x0, z0, x1, z1, 5, 'spruce_log')
    if ceiling:
        parts.floor(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, 5, 'spruce_planks')
    return parts.gable_roof(b, x0, z0, x1, z1, 5, roof, axis=axis, pitch=pitch, gable=gable)


def yard(b, cells, rng, mix=('gravel', 'cobblestone', 'coarse_dirt', 'gravel')):
    for x, z in cells:
        b.set(x, 0, z, rng.choice(mix))


def smithy():
    """Open-fronted stone forge: blast furnace, lava hearth, anvil, smithing table and grindstone."""
    rng = random.Random(7201)
    b = Build('snowy/smithy', (13, 17, 13))
    body = parts.Body(b, 1, 4, 11, 10, STYLES['stone'], heights=(3,), spacing=5).build()
    ridge = body.roof(axis='x', pitch=2, gable='spruce_planks')
    for x in range(2, 11):
        for y in (2, 3, 4):
            b.set(x, y, 4, 'air')
    for x in (1, 6, 11):
        for y in (2, 3, 4):
            b.set(x, y, 4, 'spruce_log', axis='y')
    # Forge against the back wall with a hood and a tall chimney.
    b.set(2, 2, 9, 'blast_furnace', facing='north', lit=True)
    b.set(3, 2, 9, 'lava_cauldron')
    b.set(4, 2, 9, 'bricks')
    for x in (2, 3, 4):
        b.set(x, 3, 9, 'brick_stairs', facing='south', half='top', lock=True)
        b.set(x, 4, 9, 'bricks')
    k.stove_chimney(b, 3, 9, 5, ridge + 1, mat='bricks', cap='stone_bricks')
    b.set(2, 1, 8, 'stone_bricks')
    b.set(3, 1, 8, 'stone_bricks')
    b.set(5, 2, 8, 'anvil', facing='east')
    b.set(6, 2, 9, 'water_cauldron', level=3)
    b.set(8, 2, 9, 'smithing_table')
    b.set(9, 2, 9, 'grindstone', face='floor', facing='north')
    b.barrel(10, 2, 9, 'up', loot=LOOT + 'toolsmith')
    b.chest(10, 2, 7, 'west', loot=LOOT + 'armorer')
    b.chest(10, 2, 6, 'west', loot=LOOT + 'weaponsmith')
    b.set(2, 2, 6, 'crafting_table')
    k.window(b, 1, 3, 7, 'west')
    k.window(b, 7, 3, 10, 'south', width=2)
    k.room_lamp(b, 7, 5, 6)
    k.room_lamp(b, 4, 5, 6)
    # Yard: coal, iron, a quenching trough and a lamp.
    yard(b, [(x, z) for x in range(2, 11) for z in (1, 2, 3)], rng)
    k.path_line(b, 6, 0, 0, rng)
    b.set(1, 1, 2, 'coal_block')
    b.set(1, 1, 1, 'coal_block')
    b.set(1, 2, 2, 'coal_block')
    b.barrel(2, 1, 1, 'up')
    b.set(10, 1, 2, 'raw_iron_block')
    b.set(9, 1, 2, 'cobblestone_slab', type='bottom', waterlogged=False)
    k.lamp_post(b, 11, 1, 1, height=2)
    k.woodpile(b, 12, 1, 5, along='z', length=5)
    b.entrance(6)
    k.snow_roof(b, 0, 0, 12, 12, rng, 5, eave_y=5)
    b.natural_ground()
    return b


def smokehouse():
    """Butcher's smokehouse: log walls, smokers, a meat hearth and an outdoor smoking rack."""
    rng = random.Random(7202)
    b = Build('snowy/smokehouse', (12, 17, 12))
    x0, z0, x1, z1 = 3, 3, 9, 8
    ridge = log_shell(b, x0, z0, x1, z1, ROOFS['dark_oak'], 'z')
    parts.front_door(b, 6, 2, z0, 'north', wood='spruce', step='cobblestone_stairs', lamps=False)
    k.fireplace(b, 6, z1, 'south', 1, ridge + 1)
    b.set(4, 2, 7, 'smoker', facing='east', lit=True)
    b.set(4, 2, 6, 'smoker', facing='east', lit=True)
    b.barrel(8, 2, 7, 'up', loot=LOOT + 'butcher')
    k.chopping_block(b, 8, 2, 5)
    b.set(4, 2, 4, 'crafting_table')
    # Hams curing on chains from the ceiling.
    for x in (5, 7):
        k.chain(b, x, 4, 6)
        k.chain(b, x, 3, 6)
    k.room_lamp(b, 6, 5, 5)
    k.window(b, x1, 3, 5, 'east')
    k.window(b, 8, 3, z0, 'north')
    # Smoking rack: a fire under a fence frame hung with fish.
    for z in (4, 6):
        for y in (1, 2):
            b.set(0, y, z, 'spruce_fence')
    for z in (4, 5, 6):
        b.set(0, 3, z, 'spruce_fence')
    b.set(0, 1, 5, 'campfire', lit=True, signal_fire=False, facing='east', waterlogged=False)
    b.set(1, 1, 5, 'cobblestone_slab', type='bottom', waterlogged=False)
    b.set(1, 1, 7, 'hay_block', axis='y')
    b.barrel(1, 1, 8, 'up')
    k.path_line(b, 6, 0, 2, rng)
    k.lamp_post(b, 9, 1, 1, height=2)
    k.woodpile(b, 10, 1, 4, along='z', length=4)
    b.entrance(6)
    k.snow_roof(b, 0, 0, 11, 11, rng, 5, eave_y=5)
    b.natural_ground()
    return b


def fletcher():
    """Fletcher's log hut with a stove, and straw targets out back on the snow."""
    rng = random.Random(7203)
    b = Build('snowy/fletcher', (11, 15, 15))
    x0, z0, x1, z1 = 2, 3, 8, 8
    ridge = log_shell(b, x0, z0, x1, z1, ROOFS['spruce'], 'z')
    parts.front_door(b, 5, 2, z0, 'north', wood='spruce', step='cobblestone_stairs', lamps=False)
    k.fireplace(b, x0, 6, 'west', 1, ridge - 1)
    b.set(4, 2, 7, 'fletching_table')
    b.barrel(7, 2, 7, 'up', loot=LOOT + 'fletcher')
    b.set(7, 2, 4, 'crafting_table')
    b.set(7, 2, 5, 'spruce_fence')
    b.set(7, 3, 5, 'spruce_trapdoor', facing='west', half='bottom', open=False, powered=False, waterlogged=False)
    b.set(5, 2, 7, 'white_carpet')
    k.room_lamp(b, 5, 5, 5)
    k.window(b, x1, 3, 6, 'east')
    k.window(b, 3, 3, z0, 'north')
    b.set(5, 9, z1, 'glass_pane')
    # Archery range: straw butts with targets.
    for x in (2, 5, 8):
        b.set(x, 1, 13, 'hay_block', axis='y')
        b.set(x, 2, 13, 'target', power=0)
    for x in range(1, 10):
        b.set(x, 1, 14, 'spruce_fence')
    b.set(9, 1, 10, 'spruce_fence')
    b.set(9, 2, 10, 'lantern', hanging=False, waterlogged=False)
    k.path_line(b, 5, 0, 2, rng)
    b.barrel(8, 1, 1, 'up')
    b.set(8, 2, 1, 'hay_block', axis='y')
    b.entrance(5)
    k.snow_roof(b, 0, 0, 10, 12, rng, 5, eave_y=5)
    b.natural_ground()
    return b


def shepherd():
    """Wool barn with a loom and a fenced sheep pen with a hay feeder."""
    rng = random.Random(7204)
    b = Build('snowy/shepherd', (16, 15, 15))
    body = parts.Body(b, 1, 3, 7, 10, STYLES['cabin'], heights=(3,), spacing=4).build()
    ridge = body.roof(axis='z', pitch=2, gable='spruce_planks')
    parts.front_door(b, 4, 2, 3, 'north', wood='spruce', step='cobblestone_stairs', lamps=False)
    # Wide barn door to the pen on the east side.
    for z in (6, 7):
        for y in (2, 3):
            b.set(7, y, z, 'air')
        b.set(8, 1, z, 'cobblestone_slab', type='bottom', waterlogged=False)
    b.set(2, 2, 9, 'loom', facing='east')
    for z, c in ((5, 'white'), (6, 'light_gray'), (7, 'light_blue')):
        b.set(2, 2, z, f'{c}_wool')
    b.set(2, 3, 5, 'white_wool')
    b.barrel(5, 2, 9, 'up', loot=LOOT + 'shepherd')
    b.set(6, 2, 9, 'hay_block', axis='y')
    b.set(6, 3, 9, 'hay_block', axis='x')
    k.room_lamp(b, 4, 5, 6)
    k.window(b, 1, 3, 7, 'west')
    body.gable_window('north')
    # Sheep pen.
    for x in range(8, 16):
        for z in range(3, 14):
            edge = x in (8, 15) or z in (3, 13)
            if not edge:
                continue
            if x == 8 and z in (6, 7):
                continue
            if (x, z) == (11, 3):
                k.gate(b, x, 1, z, 'north')
            else:
                b.set(x, 1, z, 'spruce_fence')
    for z in (12,):
        b.set(14, 1, z, 'hay_block', axis='y')
        b.set(13, 1, z, 'hay_block', axis='x')
    b.set(14, 1, 4, 'water_cauldron', level=3)
    b.set(9, 1, 12, 'spruce_fence')
    b.set(9, 2, 12, 'lantern', hanging=False, waterlogged=False)
    for x, z in ((10, 6), (12, 9), (13, 5)):
        b.animal(x, 1, z, 'sheep')
    k.path_line(b, 4, 0, 2, rng)
    k.path_line(b, 11, 0, 2, rng)
    b.entrance(4)
    k.snow_roof(b, 0, 0, 15, 14, rng, 5, eave_y=5)
    b.natural_ground()
    return b


def ice_fishing():
    """Ice-fishing shack on a frozen pond: a hole in the floor, the fisher's barrel and a fire outside."""
    rng = random.Random(7205)
    b = Build('snowy/ice_fishing', (12, 10, 14))
    for x in range(b.w):
        for z in range(3, b.d):
            dx, dz = (x - 5.5) / 5.6, (z - 8.5) / 5.4
            r = dx * dx + dz * dz
            if r <= 1:
                b.set(x, 0, z, 'blue_ice' if rng.random() < .18 else 'packed_ice')
    # The shack on skids.
    x0, z0, x1, z1 = 3, 5, 7, 9
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, 0, z, 'spruce_planks')
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        for y in (1, 2, 3):
            b.set(x, y, z, 'spruce_log' if corner else 'spruce_planks', **({'axis': 'y'} if corner else {}))
    parts.beam_ring(b, x0, z0, x1, z1, 4, 'stripped_spruce_log')
    parts.floor(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, 4, 'spruce_planks')
    parts.gable_roof(b, x0, z0, x1, z1, 4, ROOFS['spruce'], axis='z', pitch=1, gable='spruce_planks')
    b.door(5, 1, z0, facing='south', wood='spruce')
    b.set(5, 0, 8, 'water', level=0)
    b.set(4, 1, 8, 'spruce_stairs', facing='west', half='bottom', lock=True)
    b.barrel(6, 1, 8, 'up', loot=LOOT + 'fisher')
    b.barrel(6, 1, 7, 'up')
    b.set(4, 1, 6, 'spruce_trapdoor', facing='north', half='top', open=False, powered=False, waterlogged=False)
    k.room_lamp(b, 5, 4, 7)
    b.set(x1, 2, 7, 'glass_pane')
    b.set(x0, 2, 7, 'glass_pane')
    # Outside: a second hole with a rod rack, a fire with a bench, a sledge.
    b.set(9, 0, 11, 'water', level=0)
    b.set(10, 1, 11, 'spruce_fence')
    b.set(10, 2, 11, 'lantern', hanging=False, waterlogged=False)
    b.set(2, 1, 12, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    b.custom(3, 1, 12, 'campfire_bench', facing='west')
    k.sled(b, 9, 1, 5, along='z')
    for z in range(0, 5):
        b.set(5, 0, z, 'spruce_planks' if z >= 3 else rng.choice(k.PATH))
    b.entrance(5)
    k.snow_roof(b, 0, 0, 11, 13, rng, 4, eave_y=4)
    b.natural_ground()
    return b


def cartographer():
    """A slim three-storey lookout tower of stone and timber; ladders inside, maps at the bottom."""
    rng = random.Random(7206)
    b = Build('snowy/cartographer', (9, 24, 11))
    body = parts.Body(b, 1, 3, 7, 9, STYLES['stone'], heights=(3, 3, 3), stone_ground=True).build()
    body.roof(axis='x', pitch=2, gable='spruce_planks')
    parts.front_door(b, 3, 2, 3, 'north', wood='spruce', step='cobblestone_stairs', lamps=False)
    body.windows(0, 'north', [5], height=1)
    body.windows(0, 'west', [3], height=1)
    for lvl in (1, 2):
        body.windows(lvl, 'north', [(2, 3)], height=2, shutters=lvl == 1)
        body.windows(lvl, 'south', [3], height=2)
        body.windows(lvl, 'west', [3], height=2)
        body.windows(lvl, 'east', [2], height=1)
    body.gable_window('west')
    body.gable_window('east')
    # Ladder up the east wall through both floors.
    for y in range(2, body.top):
        b.set(6, y, 8, 'ladder', facing='west', waterlogged=False)
    b.set(2, 2, 8, 'cartography_table')
    b.chest(2, 2, 6, 'east', loot=LOOT + 'cartographer')
    b.set(4, 2, 8, 'bookshelf')
    b.set(3, 2, 8, 'spruce_stairs', facing='south', half='bottom', lock=True)
    k.room_lamp(b, 4, 5, 6)
    fy1, fy2 = body.floor_y[1], body.floor_y[2]
    parts.table(b, 3, fy1 + 1, 6, cloth='white_carpet')
    b.set(2, fy1 + 1, 8, 'barrel', facing='up', open=False)
    k.room_lamp(b, 4, fy2, 6)
    b.custom(4, fy2 + 1, 4, 'village_bench', facing='north')
    parts.table(b, 3, fy2 + 1, 7)
    k.room_lamp(b, 4, body.top, 6)
    k.path_line(b, 3, 0, 2, rng)
    k.lamp_post(b, 6, 1, 1, height=2)
    b.entrance(3)
    k.snow_roof(b, 0, 0, 8, 10, rng, body.top, eave_y=body.top)
    b.natural_ground()
    return b


def mason():
    """Mason's yard: a stonecutter under a slate lean-to, block stacks and a half-built wall."""
    rng = random.Random(7207)
    b = Build('snowy/mason', (12, 9, 12))
    yard(b, [(x, z) for x in range(1, 11) for z in range(2, 11)], rng,
         ('gravel', 'cobblestone', 'andesite', 'cobbled_deepslate', 'gravel'))
    for x, z in ((1, 6), (5, 6), (1, 10), (5, 10)):
        for y in (1, 2, 3):
            b.set(x, y, z, 'spruce_log', axis='y')
    for x in range(0, 7):
        b.set(x, 4, 6, 'deepslate_tile_stairs', facing='south', half='bottom')
        for z in range(7, 11):
            b.set(x, 4, z, 'deepslate_tile_slab', type='bottom', waterlogged=False)
        b.set(x, 4, 11, 'deepslate_tile_stairs', facing='north', half='bottom')
    b.set(3, 1, 8, 'stonecutter', facing='north')
    b.chest(2, 1, 9, 'north', loot=LOOT + 'mason')
    b.barrel(4, 1, 9, 'up')
    k.hang(b, 3, 3, 8)
    for x in range(7, 11):
        for y in range(1, 3 if x < 10 else 2):
            b.set(x, y, 9, rng.choice(['stone_bricks', 'cobblestone', 'deepslate_bricks']))
    b.set(10, 2, 9, 'stone_brick_slab', type='bottom', waterlogged=False)
    for x, z, h in ((7, 3, 2), (8, 3, 1), (7, 4, 1), (9, 4, 1)):
        for y in range(1, h + 1):
            b.set(x, y, z, rng.choice(['stone_bricks', 'polished_andesite', 'cobbled_deepslate']))
    b.set(8, 2, 3, 'stone_brick_slab', type='bottom', waterlogged=False)
    b.set(2, 1, 3, 'cobblestone_wall')
    b.set(2, 2, 3, 'lantern', hanging=False, waterlogged=False)
    k.sled(b, 9, 1, 6, along='z', load=False)
    b.set(9, 2, 6, 'stone_bricks')
    b.set(9, 2, 7, 'cobblestone')
    k.path_line(b, 5, 0, 1, rng)
    b.entrance(5)
    k.snow_roof(b, 0, 0, 11, 11, rng, 1, cover=.6)
    b.natural_ground()
    return b


def furrier():
    """Furrier's lodge (leatherworker): soaking vats, a pelt-drying frame and a sledge of furs."""
    rng = random.Random(7208)
    b = Build('snowy/furrier', (13, 14, 13))
    x0, z0, x1, z1 = 1, 4, 7, 9
    ridge = log_shell(b, x0, z0, x1, z1, ROOFS['dark_oak'], 'x')
    parts.front_door(b, 4, 2, z0, 'north', wood='spruce', step='cobblestone_stairs', lamps=False)
    k.fireplace(b, 4, z1, 'south', 1, ridge + 1)
    b.set(2, 2, 8, 'cauldron')
    b.chest(6, 2, 8, 'west', loot=LOOT + 'tannery')
    b.set(6, 2, 5, 'crafting_table')
    k.fur_rug(b, 2, 5, 3, 6, 2, 'white', 'brown')
    k.room_lamp(b, 4, 5, 6)
    k.window(b, x1, 3, 6, 'east', width=2)
    k.window(b, 2, 3, z0, 'north')
    # Outdoor vats and a drying frame hung with pelts.
    for z in (5, 6):
        b.set(9, 1, z, 'water_cauldron', level=2)
    b.set(9, 1, 7, 'cauldron')
    for z in (9, 11):
        for y in (1, 2, 3):
            b.set(9, y, z, 'spruce_fence')
            b.set(12, y, z, 'spruce_fence')
    for x in range(9, 13):
        b.set(x, 3, 10, 'spruce_fence')
    for x, c in ((10, 'brown'), (11, 'white')):
        b.set(x, 2, 10, f'{c}_wool')
    k.sled(b, 10, 1, 2, along='x')
    b.set(11, 2, 2, 'white_carpet')
    b.set(12, 2, 2, 'brown_carpet')
    k.path_line(b, 4, 0, 2, rng)
    b.entrance(4)
    k.snow_roof(b, 0, 0, 12, 12, rng, 5, eave_y=5)
    b.natural_ground()
    return b


def herbalist():
    """Herbalist's study (cleric and librarian): brewing stand, lectern, books and a berry bed."""
    rng = random.Random(7209)
    st = STYLES['white']
    b = Build('snowy/herbalist', (13, 16, 13))
    body = parts.Body(b, 2, 4, 10, 9, st, heights=(3,), spacing=4).build()
    ridge = body.roof(axis='x', pitch=2, gable='white_terracotta')
    parts.front_door(b, 5, 2, 4, 'north', wood='dark_oak', step='stone_brick_stairs', lamps=False)
    k.fireplace(b, 10, 6, 'east', 1, ridge + 1)
    body.windows(0, 'north', [1, (5, 2)], height=1)
    body.windows(0, 'south', [2, 5], height=1)
    body.gable_window('west')
    # Brewing corner.
    b.set(3, 2, 8, 'spruce_planks')
    b.set(3, 3, 8, 'brewing_stand', has_bottle_0=False, has_bottle_1=False, has_bottle_2=False)
    b.set(4, 2, 8, 'water_cauldron', level=3)
    b.set(3, 2, 7, 'barrel', facing='up', open=False)
    b.set(3, 3, 7, 'potted_fern')
    # Study corner.
    b.set(7, 2, 8, 'lectern', facing='north', has_book=False, powered=False)
    for x in (8, 9):
        b.set(x, 2, 8, 'bookshelf')
        b.set(x, 3, 8, 'bookshelf')
    b.chest(9, 2, 5, 'west', loot=LOOT + 'temple')
    b.custom(7, 2, 6, 'fireside_armchair', facing='east')
    k.room_lamp(b, 5, 5, 6)
    k.room_lamp(b, 8, 5, 6)
    # Berry bed beside the house.
    for x in range(2, 6):
        for z in (11, 12):
            b.set(x, 0, z, 'podzol')
            b.set(x, 1, z, 'sweet_berry_bush', age=rng.choice([2, 3]))
    for x in (1, 6):
        for z in (11, 12):
            b.set(x, 1, z, 'spruce_fence')
    k.path_line(b, 5, 0, 2, rng)
    k.lamp_post(b, 8, 1, 2, height=2)
    b.set(3, 1, 2, 'spruce_leaves', persistent=True, distance=1, waterlogged=False)
    b.entrance(5)
    k.snow_roof(b, 0, 0, 12, 12, rng, 5, eave_y=5)
    b.natural_ground()
    return b


DESIGNS = {
    'snowy/smithy': smithy,
    'snowy/smokehouse': smokehouse,
    'snowy/fletcher': fletcher,
    'snowy/shepherd': shepherd,
    'snowy/ice_fishing': ice_fishing,
    'snowy/cartographer': cartographer,
    'snowy/mason': mason,
    'snowy/furrier': furrier,
    'snowy/herbalist': herbalist,
}
