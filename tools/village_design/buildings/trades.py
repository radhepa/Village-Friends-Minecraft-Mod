"""Workplaces for the vanilla professions, scattered along the streets.

Each holds the vanilla job site block, so unemployed residents of nearby homes
can take up the trade. Lots follow the drop-in contract.
"""
import random

from ..kit import Build
from .. import parts
from ..parts import Body, Style, ROOFS

STONE = Style(frame='stripped_spruce_log', fill='cobblestone', floor='stone_bricks', roof='dark_oak',
              base='cobblestone', trim='spruce', door='spruce', upper_fill='spruce_planks')
TIMBER = Style(frame='stripped_spruce_log', fill='oak_planks', floor='spruce_planks', roof='spruce',
               base='cobblestone', trim='spruce', door='spruce', upper_fill='calcite')
BIRCH = Style(frame='stripped_dark_oak_log', fill='birch_planks', floor='oak_planks', roof='dark_oak',
              base='stone_bricks', trim='dark_oak', door='dark_oak', upper_fill='birch_planks')


def lot_path(b, x, z0, z1, rng):
    for z in range(z0, z1 + 1):
        b.set(x, 0, z, rng.choice(['dirt_path', 'dirt_path', 'gravel', 'coarse_dirt']))


def smithy():
    """Open-fronted forge: blast furnace, smithing table, grindstone, anvil and a lava cauldron."""
    rng = random.Random(501)
    b = Build('smithy', (13, 16, 13))
    body = Body(b, 1, 4, 11, 10, STONE, heights=(3,), spacing=5).build()
    body.roof(axis='x', pitch=1, gable='spruce_planks', trim=ROOFS['spruce'])
    # Open the forge front between stout posts.
    for x in range(2, 11):
        for y in (2, 3, 4):
            if x not in (1, 6, 11):
                b.set(x, y, 4, 'air')
    for x in (1, 6, 11):
        for y in (2, 3, 4):
            b.set(x, y, 4, 'stripped_spruce_log', axis='y')
    for x in range(1, 12):
        b.set(x, 5, 4, 'stripped_spruce_log', axis='x')
    for x in range(2, 11):
        b.set(x, 1, 4, 'stone_bricks')
    # Back room wall with a door.
    for x in range(2, 11):
        for y in (2, 3, 4):
            b.set(x, y, 7, 'spruce_planks')
    b.door(8, 2, 7, facing='north', wood='spruce')
    body.windows(0, 'south', [(2, 2), (7, 2)], height=1)
    body.windows(0, 'west', [4], height=1)
    # Forge: stone hearth with a lava cauldron and a tall chimney.
    for x in (2, 3, 4):
        b.set(x, 2, 6, 'bricks')
    b.set(3, 2, 6, 'lava_cauldron')
    b.set(2, 2, 5, 'blast_furnace', facing='east', lit=True)
    for x in (2, 3, 4):
        b.set(x, 3, 6, 'brick_stairs', facing='south', half='top', lock=True)
        b.set(x, 4, 6, 'bricks')
    parts.chimney(b, 3, 6, 5, body.ridge + 1, 'bricks')
    b.set(5, 2, 5, 'anvil', facing='east')
    b.set(9, 2, 5, 'smithing_table')
    b.set(10, 2, 6, 'grindstone', face='floor', facing='north')
    b.barrel(10, 2, 5, 'up', loot='minecraft:chests/village/village_toolsmith')
    b.chest(3, 2, 9, 'north', loot='minecraft:chests/village/village_armorer')
    b.set(10, 2, 9, 'crafting_table')
    parts.lantern(b, 7, 4, 5)
    parts.lantern(b, 6, 4, 8)
    # Yard: coal, ore cart and a lamp.
    lot_path(b, 6, 0, 3, rng)
    for x in range(3, 10):
        b.set(x, 0, 3, rng.choice(['gravel', 'cobblestone', 'coarse_dirt']))
    b.set(1, 1, 2, 'coal_block')
    b.set(2, 1, 2, 'barrel', facing='up', open=False)
    b.set(10, 1, 2, 'cobblestone')
    parts.lamp_post(b, 11, 1, 2, height=2)
    b.entrance(6)
    b.natural_ground()
    return b


def butcher():
    """Butcher's shop with a smoker, a hanging rack and a stocked cold store."""
    rng = random.Random(502)
    b = Build('butcher', (11, 15, 12))
    body = Body(b, 1, 4, 9, 9, BIRCH, heights=(3,), spacing=4).build()
    body.roof(axis='x', pitch=1, gable='birch_planks', trim=ROOFS['spruce'])
    parts.front_door(b, 5, 2, 4, 'north', wood='dark_oak', step='stone_brick_stairs')
    body.windows(0, 'north', [(1, 2), (6, 2)], height=1, box='azalea_leaves')
    body.windows(0, 'east', [2], height=1)
    b.set(2, 2, 8, 'smoker', facing='east', lit=True)
    b.set(3, 2, 8, 'smoker', facing='north', lit=False)
    for x in (6, 7, 8):
        b.set(x, 2, 7, 'stripped_birch_log', axis='x')
    b.barrel(8, 2, 8, 'up', loot='minecraft:chests/village/village_butcher')
    b.set(2, 2, 5, 'crafting_table')
    b.set(4, 4, 7, 'chain', axis='y')
    parts.lantern(b, 5, 4, 6)
    parts.chimney(b, 2, 8, 5, body.ridge + 1, 'cobblestone')
    for z in range(5, 8):
        b.set(0, 1, z, 'hay_block', axis='y') if z != 6 else b.set(0, 1, z, 'barrel', facing='up', open=False)
    lot_path(b, 5, 0, 3, rng)
    b.set(8, 1, 2, 'stripped_oak_log', axis='y')
    b.set(2, 1, 2, 'spruce_fence')
    b.set(2, 2, 2, 'lantern')
    b.entrance(5)
    b.natural_ground()
    return b


def fletcher():
    """Fletcher's hut with archery butts out back."""
    rng = random.Random(503)
    b = Build('fletcher', (11, 14, 14))
    body = Body(b, 2, 3, 8, 8, TIMBER, heights=(3,), spacing=3).build()
    body.roof(axis='z', pitch=2, gable='calcite', trim=ROOFS['dark_oak'])
    parts.front_door(b, 5, 2, 3, 'north', wood='spruce', step='cobblestone_stairs')
    body.windows(0, 'north', [1, 5], height=1, box='flowering_azalea_leaves')
    body.windows(0, 'west', [(2, 2)], height=1)
    body.gable_window('north')
    b.set(3, 2, 7, 'fletching_table')
    b.barrel(7, 2, 7, 'up', loot='minecraft:chests/village/village_fletcher')
    b.set(7, 2, 4, 'crafting_table')
    parts.lantern(b, 5, 4, 5)
    for x in (2, 5, 8):
        b.set(x, 1, 12, 'hay_block', axis='y')
        b.set(x, 2, 12, 'target', power=0)
    for x in range(1, 10):
        b.set(x, 0, 11, 'coarse_dirt' if x % 2 else 'dirt_path')
    lot_path(b, 5, 0, 2, rng)
    b.set(9, 1, 1, 'barrel', facing='up', open=False)
    b.entrance(5)
    b.natural_ground()
    return b


def shepherd():
    """Shepherd's barn with a loom and a fenced sheep pen."""
    rng = random.Random(504)
    b = Build('shepherd', (15, 15, 15))
    body = Body(b, 1, 3, 7, 10, TIMBER, heights=(4,), spacing=4).build()
    body.roof(axis='z', pitch=1, gable='oak_planks', trim=ROOFS['dark_oak'])
    for z in range(5, 9):
        for y in (2, 3, 4):
            b.set(7, y, z, 'air')
    for z in (4, 9):
        for y in (2, 3, 4, 5):
            b.set(7, y, z, 'stripped_spruce_log', axis='y')
    parts.front_door(b, 4, 2, 3, 'north', wood='spruce', step='cobblestone_stairs')
    body.windows(0, 'west', [(2, 2), (5, 1)], height=1)
    body.gable_window('north')
    b.set(2, 2, 9, 'loom', facing='north')
    for z, c in zip((5, 6, 7), ('white', 'light_gray', 'brown')):
        b.set(2, 2, z, f'{c}_wool')
    b.set(5, 2, 9, 'hay_block', axis='y')
    b.set(4, 2, 9, 'barrel', facing='up', open=False)
    parts.lantern(b, 4, 5, 6)
    # Sheep pen on the open east side.
    for x in range(8, 15):
        for z in range(3, 14):
            edge = x in (8, 14) or z in (3, 13)
            if edge and not (x == 8 and 5 <= z <= 8):
                b.set(x, 1, z, 'spruce_fence')
            if not edge:
                b.set(x, 0, z, 'grass_block')
                if rng.random() < .12:
                    b.set(x, 1, z, 'short_grass')
    b.set(13, 1, 12, 'hay_block', axis='y')
    b.set(12, 1, 12, 'water_cauldron', level=3)
    for x, z in ((10, 6), (12, 8), (11, 10)):
        b.animal(x, 1, z, 'sheep')
    lot_path(b, 4, 0, 2, rng)
    b.entrance(4)
    b.natural_ground()
    return b


def fisher():
    """Fisher's hut on a little pond with a jetty."""
    rng = random.Random(505)
    b = Build('fisher', (13, 13, 14))
    body = Body(b, 1, 3, 6, 8, Style(frame='stripped_spruce_log', fill='spruce_planks', floor='spruce_planks',
                                       roof='oak', base='cobblestone', trim='spruce', upper_fill='spruce_planks'),
                heights=(3,), spacing=5).build()
    body.roof(axis='x', pitch=1, gable='spruce_planks', trim=ROOFS['spruce'])
    parts.front_door(b, 3, 2, 3, 'north', wood='spruce', step='cobblestone_stairs')
    body.windows(0, 'east', [(2, 2)], height=1)
    body.windows(0, 'north', [5], height=1)
    b.barrel(5, 2, 7, 'up', loot='minecraft:chests/village/village_fisher')
    b.set(2, 2, 7, 'crafting_table')
    parts.lantern(b, 3, 4, 5)
    # Pond lined with clay and sand, a jetty over it.
    for x in range(3, 13):
        for z in range(9, 14):
            dx, dz = (x - 7.5) / 5, (z - 11) / 2.6
            if dx * dx + dz * dz <= 1:
                b.set(x, 0, z, 'water', level=0)
                b.set(x, 1, z, 'air')
            elif dx * dx + dz * dz <= 1.5:
                b.set(x, 0, z, rng.choice(['sand', 'gravel', 'grass_block', 'clay']))
    for z in range(8, 12):
        b.set(7, 1, z, 'spruce_slab', type='bottom', waterlogged=False)
    b.set(8, 1, 11, 'spruce_fence')
    b.set(8, 2, 11, 'lantern')
    for x, z in ((10, 10), (5, 11)):
        if b.get(x, 0, z)[0] == 'minecraft:water':
            b.set(x, 1, z, 'lily_pad')
    for x, z in ((3, 9), (12, 11)):
        b.set(x, 0, z, 'grass_block')
        b.set(x, 1, z, 'sugar_cane', age=0)
        b.set(x, 2, z, 'sugar_cane', age=0)
    lot_path(b, 3, 0, 2, rng)
    b.set(9, 1, 2, 'barrel', facing='up', open=False)
    b.set(10, 1, 2, 'barrel', facing='north', open=False)
    b.entrance(3)
    b.natural_ground()
    return b


def cartographer():
    """A slim three-storey map tower with a lookout."""
    rng = random.Random(506)
    b = Build('cartographer', (9, 22, 11))
    body = Body(b, 1, 3, 7, 9, BIRCH, heights=(3, 3, 3), jetty=(), stone_ground=True).build()
    body.roof(axis='x', pitch=2, gable='birch_planks', trim=ROOFS['spruce'])
    parts.front_door(b, 4, 2, 3, 'north', wood='dark_oak', step='stone_brick_stairs')
    body.windows(0, 'north', [1, 5], height=1)
    for lvl in (1, 2):
        body.windows(lvl, 'north', [(2, 3)], height=2, shutters=True)
        body.windows(lvl, 'south', [3], height=2)
        body.windows(lvl, 'west', [3], height=2)
        body.windows(lvl, 'east', [3], height=2)
    b.set(2, 2, 8, 'cartography_table')
    b.set(6, 2, 8, 'bookshelf')
    b.chest(6, 2, 7, 'west', loot='minecraft:chests/village/village_cartographer')
    parts.lantern(b, 4, 4, 6)
    for lvl in (0, 1):
        y0 = body.floor_y[lvl] + 1
        parts.stair_run(b, 2, 4 + 4 * 0, y0, 4, 'south', wood='dark_oak') if lvl == 0 else \
            parts.stair_run(b, 6, 8, y0, 4, 'north', wood='dark_oak')
    parts.lantern(b, 4, body.floor_y[1] + 3, 6)
    parts.lantern(b, 4, body.floor_y[2] + 3, 6)
    parts.table(b, 4, body.floor_y[2] + 1, 6, wood='dark_oak')
    lot_path(b, 4, 0, 2, rng)
    b.entrance(4)
    b.natural_ground()
    return b


def mason():
    """Mason's yard: stonecutter under a lean-to, stacked stone and a half-built wall."""
    rng = random.Random(507)
    b = Build('mason', (11, 10, 11))
    for x in range(1, 10):
        for z in range(2, 10):
            b.set(x, 0, z, rng.choice(['gravel', 'cobblestone', 'andesite', 'coarse_dirt', 'stone']))
    for x, z in ((1, 6), (5, 6), (1, 9), (5, 9)):
        for y in (1, 2, 3):
            b.set(x, y, z, 'stripped_spruce_log', axis='y')
    for z in range(5, 11):
        for i, x in enumerate(range(0, 7)):
            b.set(x, 4, z, 'spruce_slab', type='bottom')
    b.set(3, 1, 8, 'stonecutter', facing='north')
    b.chest(2, 1, 9, 'north', loot='minecraft:chests/village/village_mason')
    for x in range(7, 10):
        for y in range(1, 3 if x < 9 else 2):
            b.set(x, y, 8, rng.choice(['stone_bricks', 'cobblestone', 'mossy_stone_bricks']))
    for x, z in ((7, 3), (8, 3), (7, 4)):
        b.set(x, 1, z, rng.choice(['stone_bricks', 'cobblestone', 'polished_andesite']))
    b.set(8, 2, 3, 'stone_brick_slab', type='bottom')
    b.set(2, 1, 3, 'cobblestone_wall')
    b.set(2, 2, 3, 'lantern')
    lot_path(b, 5, 0, 1, rng)
    b.entrance(5)
    b.natural_ground()
    return b


def tannery():
    """Leatherworker's tannery: vats, drying racks and a little workshop."""
    rng = random.Random(508)
    b = Build('tannery', (11, 13, 12))
    body = Body(b, 1, 5, 6, 10, TIMBER, heights=(3,), spacing=5).build()
    body.roof(axis='z', pitch=1, gable='oak_planks', trim=ROOFS['dark_oak'])
    parts.front_door(b, 3, 2, 5, 'north', wood='spruce', step='cobblestone_stairs')
    body.windows(0, 'east', [(2, 2)], height=1)
    b.set(2, 2, 9, 'cauldron')
    b.set(5, 2, 9, 'barrel', facing='up', open=False)
    b.chest(2, 2, 6, 'east', loot='minecraft:chests/village/village_tannery')
    parts.lantern(b, 3, 4, 7)
    # Outdoor vats and drying racks.
    for x in (8, 9):
        b.set(x, 1, 6, 'water_cauldron', level=2)
    b.set(8, 1, 8, 'cauldron')
    for z in (2, 3, 4):
        b.set(7, 1, z, 'spruce_fence')
        b.set(10, 1, z, 'spruce_fence')
    for x in range(7, 11):
        b.set(x, 2, 3, 'spruce_fence')
    for x in (8, 9):
        b.set(x, 2, 2, 'brown_carpet')
        b.set(x, 1, 4, 'brown_wool')
    lot_path(b, 3, 0, 4, rng)
    b.entrance(3)
    b.natural_ground()
    return b


DESIGNS = {'smithy': smithy, 'butcher': butcher, 'fletcher': fletcher, 'shepherd': shepherd, 'fisher': fisher,
           'cartographer': cartographer, 'mason': mason, 'tannery': tannery}
