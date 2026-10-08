"""Savanna workshops for the vanilla professions (no residents).

Each holds the vanilla job site block, so unemployed residents of nearby homes can
take up the trade. Open-sided sheds on acacia posts, thatched huts and mud-walled
workrooms; every lot follows the drop-in contract.
"""
import random

from ...kit import Build
from ... import parts
from ...parts import Body
from . import homes_parts as hp
from .palette import ROOFS, STYLES

VILLAGE = 'minecraft:chests/village/village_'


def posts(b, cells, y0, y1, wood='stripped_acacia_log'):
    for x, z in cells:
        for yy in range(y0, y1 + 1):
            b.set(x, yy, z, wood, axis='y')


def beam_ring(b, x0, z0, x1, z1, y, wood='stripped_acacia_log'):
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        b.set(x, y, z, wood, axis='y' if corner else ('x' if facing in ('north', 'south') else 'z'))


def floor(b, x0, z0, x1, z1, rng, y=0, mix=('packed_mud', 'packed_mud', 'coarse_dirt', 'mud_bricks')):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, y, z, rng.choice(mix))


def smithy():
    """Open forge under a dark timber roof: blast furnace, smithing table, grindstone, anvil and lava."""
    rng = random.Random(5101)
    b = Build('savanna/smithy', (15, 13, 14))
    floor(b, 1, 3, 13, 11, rng, mix=('packed_mud', 'coarse_dirt', 'mud_bricks', 'gravel'))
    # Back and side walls of mud brick, open front on posts.
    for x in range(1, 14):
        for yy in (1, 2, 3):
            b.set(x, yy, 11, 'mud_bricks')
    for z in range(8, 12):
        for yy in (1, 2, 3):
            b.set(1, yy, z, 'mud_bricks')
            b.set(13, yy, z, 'mud_bricks')
    posts(b, [(1, 3), (5, 3), (9, 3), (13, 3), (1, 7), (13, 7)], 1, 3)
    for x in (1, 13):
        b.set(x, 2, 5, 'acacia_fence')
        b.set(x, 1, 5, 'acacia_fence')
    beam_ring(b, 1, 3, 13, 11, 4)
    for x in range(2, 13):
        b.set(x, 4, 7, 'stripped_acacia_log', axis='x')
    hp.hip_roof(b, 1, 3, 13, 11, 5, ROOFS['dark'], overhang=1)
    # Forge hearth with a lava cauldron and a mud-brick hood and chimney.
    b.set(2, 1, 10, 'mud_bricks')
    b.set(3, 1, 10, 'lava_cauldron')
    b.set(4, 1, 10, 'mud_bricks')
    for x in (2, 3, 4):
        b.set(x, 2, 10, 'mud_brick_stairs', facing='south', half='top', lock=True)
        b.set(x, 3, 10, 'mud_bricks')
    for yy in range(4, 11):
        b.set(3, yy, 10, 'mud_bricks')
    b.set(3, 11, 10, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    b.set(2, 1, 8, 'blast_furnace', facing='east', lit=True)
    b.set(5, 1, 9, 'anvil', facing='east')
    b.set(6, 1, 10, 'water_cauldron', level=3)
    b.set(10, 1, 9, 'smithing_table')
    b.set(11, 1, 9, 'grindstone', face='floor', facing='north')
    b.barrel(12, 1, 10, 'up', loot=VILLAGE + 'toolsmith')
    b.barrel(11, 1, 10, 'north', loot=VILLAGE + 'weaponsmith')
    b.chest(12, 1, 8, 'west', loot=VILLAGE + 'armorer')
    b.set(2, 1, 9, 'coal_block')
    for x in (5, 9):
        hp.lantern(b, x, 3, 7)
    # Front apron with an ore cart and a lamp.
    hp.path(b, 7, 0, 2, rng)
    for x in range(4, 11):
        if x != 7:
            b.set(x, 0, 2, rng.choice(['coarse_dirt', 'gravel', 'packed_mud']))
    b.set(11, 1, 1, 'barrel', facing='up', open=False)
    b.set(12, 1, 1, 'iron_ore')
    hp.post_lantern(b, 3, 1, 1)
    b.entrance(7)
    hp.tufts(b, [(x, z) for x in range(15) for z in range(14)], rng, .05)
    b.natural_ground()
    return b


def butcher():
    """White clay butchery with smokers inside and biltong drying on a rack outside."""
    rng = random.Random(5102)
    b = Build('savanna/butcher', (14, 11, 14))
    body = Body(b, 2, 4, 10, 9, STYLES['clay'], heights=(3,), spacing=4).build()
    hp.hip_roof(b, 2, 4, 10, 9, 5, ROOFS['terracotta'], overhang=1)
    hp.door(b, 6, 2, 4, 'north', step='mud_brick_stairs')
    for x in (3, 9):
        hp.glazed(b, x, 3, 4, 'north')
    hp.glazed(b, 10, 3, 7, 'east', shutters=None)
    hp.glazed(b, 6, 3, 9, 'south', shutters=None)
    b.set(3, 2, 8, 'smoker', facing='east', lit=True)
    b.set(4, 2, 8, 'smoker', facing='north', lit=False)
    b.barrel(9, 2, 8, 'up', loot=VILLAGE + 'butcher')
    b.set(9, 2, 5, 'crafting_table')
    b.set(8, 2, 8, 'stripped_acacia_log', axis='x')
    b.set(3, 2, 5, 'barrel', facing='up', open=False)
    hp.lantern(b, 6, 4, 7)
    parts.chimney(b, 3, 8, 5, 8, 'mud_bricks')
    # Biltong rack and chopping block.
    hp.drying_rack(b, 11, 3, 'z', length=4, hides=('red', 'brown'), face='east')
    b.set(12, 1, 8, 'stripped_acacia_log', axis='y')
    b.set(12, 1, 9, 'hay_block', axis='y')
    # Pig pen behind.
    pen = [(x, z) for x, z, _, _ in parts.ring(1, 10, 9, 13)]
    hp.woven_fence(b, pen)
    b.set(8, 1, 12, 'water_cauldron', level=3)
    b.set(2, 1, 12, 'hay_block', axis='y')
    b.animal(4, 1, 12, 'pig')
    b.animal(6, 1, 11, 'pig')
    hp.path(b, 6, 0, 2, rng)
    b.entrance(6)
    hp.yard(b, hp.disk(6, 6, 6.8), rng, tufts=.1)
    b.natural_ground()
    return b


def fletcher():
    """Round fletcher's hut with an archery range of hay-backed targets behind."""
    rng = random.Random(5103)
    b = Build('savanna/fletcher', (13, 13, 16))
    inside, ring, top = hp.round_hut(b, 6, 7, 3.5, 1, 3, pattern=(3, ['white_terracotta', 'brown_terracotta']))
    for yy in (2, 3, 4):
        b.set(5, yy, 4, 'stripped_acacia_log', axis='y')
        b.set(7, yy, 4, 'stripped_acacia_log', axis='y')
    hp.door(b, 6, 2, 4, 'north', step='mud_brick_stairs')
    hp.cone_roof(b, 6, 7, 3.5, top, inside, eave=1.3)
    for x, z in ((3, 7), (9, 7)):
        hp.slit(b, x, 3, z)
    b.set(8, 2, 8, 'fletching_table')
    b.barrel(4, 2, 8, 'up', loot=VILLAGE + 'fletcher')
    b.set(6, 2, 9, 'crafting_table')
    b.set(8, 2, 6, 'barrel', facing='west', open=False)
    hp.lantern(b, 6, 6, 7, chain=1)
    # Range behind: dirt lane and targets on hay bales.
    for x in range(1, 12):
        b.set(x, 0, 14, rng.choice(['coarse_dirt', 'dirt_path', 'coarse_dirt']))
    for x in (2, 6, 10):
        b.set(x, 1, 15, 'hay_block', axis='y')
        b.set(x, 2, 15, 'target', power=0)
    hp.woven_fence(b, [(0, z) for z in range(12, 16)] + [(12, z) for z in range(12, 16)])
    b.set(11, 1, 12, 'hay_block', axis='x')
    # Front: path, chicken coop for feathers.
    hp.path(b, 6, 0, 3, rng)
    b.entrance(6)
    for x, z in ((10, 1), (11, 1), (10, 2), (11, 2)):
        b.set(x, 0, z, 'coarse_dirt')
    hp.woven_fence(b, [(9, 1), (9, 2), (9, 3), (10, 3), (11, 3), (12, 3), (12, 2), (12, 1), (12, 0), (11, 0), (10, 0), (9, 0)])
    b.animal(10, 1, 1, 'chicken')
    b.animal(11, 1, 2, 'chicken')
    hp.yard(b, hp.disk(6, 7, 5.6), rng, tufts=.12)
    b.natural_ground()
    return b


def shepherd():
    """Thatched loom shelter beside a woven sheep pen with hay and a water trough."""
    rng = random.Random(5104)
    b = Build('savanna/shepherd', (16, 10, 15))
    floor(b, 1, 3, 6, 8, rng)
    posts(b, [(1, 3), (6, 3), (1, 8), (6, 8)], 1, 3)
    beam_ring(b, 1, 3, 6, 8, 4)
    for z in range(4, 8):
        for yy in (1, 2, 3):
            b.set(1, yy, z, 'mud_bricks')
    hp.thatch_hip(b, 1, 3, 6, 8, 5, overhang=1)
    b.set(2, 1, 6, 'loom', facing='east')
    b.barrel(2, 1, 7, 'up', loot=VILLAGE + 'shepherd')
    for x, y, z, c in ((5, 1, 7, 'white'), (4, 1, 7, 'orange'), (5, 1, 6, 'brown'), (5, 2, 7, 'white')):
        b.set(x, y, z, f'{c}_wool')
    b.set(2, 1, 4, 'red_wool')
    b.set(2, 2, 4, 'orange_carpet')
    hp.lantern(b, 3, 3, 5)
    # Woven sheep pen.
    pen = [(x, z) for x, z, _, _ in parts.ring(7, 2, 15, 13)]
    hp.woven_fence(b, pen, gate=(7, 5), gate_facing='east')
    for x in range(8, 15):
        for z in range(3, 13):
            if rng.random() < .1:
                b.set(x, 1, z, rng.choice(['short_grass', 'short_dry_grass', 'tall_dry_grass']))
    hp.hay_pile(b, [(13, 11), (14, 11), (14, 12), (13, 12)], rng, high=[(14, 12)])
    for x in (9, 10):
        b.set(x, 1, 12, 'water_cauldron', level=3)
    for x, z in ((10, 5), (12, 8), (11, 10), (9, 7)):
        b.animal(x, 1, z, 'sheep')
    b.animal(13, 1, 6, 'sheep', baby=True)
    hp.path(b, 4, 0, 2, rng)
    b.entrance(4)
    b.natural_ground()
    return b


def fisher():
    """Fisher's shade by a reed-fringed waterhole, with a dugout canoe and fish barrels."""
    rng = random.Random(5105)
    b = Build('savanna/fisher', (15, 8, 16))
    # Waterhole.
    for x in range(1, 15):
        for z in range(6, 16):
            dx, dz = (x - 8) / 5.6, (z - 10.5) / 4.0
            d = dx * dx + dz * dz
            if d <= 1:
                b.set(x, 0, z, 'water', level=0)
            elif d <= 1.45:
                b.set(x, 0, z, rng.choice(['mud', 'coarse_dirt', 'sand', 'grass_block', 'mud']))
    for x, z in ((3, 8), (3, 9), (13, 12), (12, 14), (4, 13)):
        if b.get(x, 0, z)[0] != 'minecraft:water':
            b.set(x, 0, z, 'grass_block')
            b.set(x, 1, z, 'sugar_cane', age=0)
            b.set(x, 2, z, 'sugar_cane', age=0)
    for x, z in ((10, 9), (6, 12), (11, 12)):
        if b.get(x, 0, z)[0] == 'minecraft:water':
            b.set(x, 1, z, 'lily_pad')
    # Shade on four posts.
    floor(b, 2, 2, 7, 5, rng, mix=('packed_mud', 'coarse_dirt'))
    posts(b, [(2, 2), (7, 2), (2, 5), (7, 5)], 1, 3, wood='acacia_log')
    beam_ring(b, 2, 2, 7, 5, 4, wood='acacia_log')
    b.fill(3, 4, 3, 6, 4, 4, 'acacia_planks')
    hp.thatch_hip(b, 2, 2, 7, 5, 5, overhang=1)
    b.barrel(3, 1, 5, 'up', loot=VILLAGE + 'fisher')
    b.set(4, 1, 5, 'barrel', facing='up', open=False)
    b.set(6, 1, 5, 'crafting_table')
    hp.lantern(b, 4, 3, 3)
    hp.drying_rack(b, 9, 2, 'x', length=4, hides=('light_gray', 'white'), face='north')
    # Dugout canoe on the bank (the water's edge at the west).
    b.set(10, 1, 6, 'acacia_stairs', facing='west', half='bottom', shape='straight', lock=True)
    b.set(11, 1, 6, 'acacia_slab', type='bottom', waterlogged=False)
    b.set(12, 1, 6, 'acacia_stairs', facing='east', half='bottom', shape='straight', lock=True)
    hp.path(b, 4, 0, 1, rng)
    b.entrance(4)
    hp.tufts(b, [(x, z) for x in range(15) for z in range(16)], rng, .05)
    b.natural_ground()
    return b


def mason():
    """Potter-mason's yard: stonecutter under a shade, a mud kiln and stacks of terracotta and pots."""
    rng = random.Random(5106)
    b = Build('savanna/mason', (14, 9, 13))
    floor(b, 1, 2, 12, 11, rng, mix=('coarse_dirt', 'packed_mud', 'red_sand', 'coarse_dirt', 'gravel'))
    posts(b, [(1, 6), (6, 6), (1, 10), (6, 10)], 1, 3)
    for x in range(0, 8):
        for z in range(5, 12):
            b.set(x, 4, z, 'acacia_slab', type='bottom', waterlogged=False)
    b.set(3, 1, 8, 'stonecutter', facing='north')
    b.chest(2, 1, 10, 'north', loot=VILLAGE + 'mason')
    b.set(5, 1, 10, 'crafting_table')
    hp.lantern(b, 3, 3, 7)
    # Kiln: a mud-brick dome with a fire inside.
    for x in range(8, 12):
        for z in range(7, 11):
            edge = x in (8, 11) or z in (7, 10)
            for yy in (1, 2):
                if edge:
                    b.set(x, yy, z, 'mud_bricks')
            if not edge:
                b.set(x, 1, z, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
                b.set(x, 2, z, 'air')
                b.set(x, 3, z, 'mud_bricks')
    b.set(9, 1, 7, 'furnace', facing='north', lit=True)
    b.set(10, 1, 7, 'mud_bricks')
    for x, z in ((8, 7), (11, 7), (8, 10), (11, 10)):
        b.set(x, 3, z, 'mud_brick_slab', type='bottom', waterlogged=False)
    b.set(9, 4, 9, 'mud_brick_wall')
    # Stacks of fired terracotta and pots.
    for x, z, h in ((8, 3, 2), (9, 3, 1), (10, 3, 2), (11, 3, 1)):
        for yy in range(1, h + 1):
            b.set(x, yy, z, rng.choice(['orange_terracotta', 'white_terracotta', 'terracotta', 'brown_terracotta']))
    for x in (2, 3, 4):
        hp.pot(b, x, 1, 3)
    b.set(5, 1, 3, 'clay')
    b.set(12, 1, 11, 'mud_bricks')
    b.set(12, 2, 11, 'mud_brick_slab', type='bottom', waterlogged=False)
    hp.path(b, 6, 0, 1, rng)
    b.entrance(6)
    b.natural_ground()
    return b


def tannery():
    """Leatherworker's yard: vats, hide racks and a small thatched store."""
    rng = random.Random(5107)
    b = Build('savanna/tannery', (15, 12, 14))
    inside, ring, top = hp.round_hut(b, 4, 9, 2.5, 1, 3, pattern=(3, ['brown_terracotta', 'white_terracotta']))
    for yy in (2, 3, 4):
        b.set(3, yy, 7, 'stripped_acacia_log', axis='y')
        b.set(5, yy, 7, 'stripped_acacia_log', axis='y')
    hp.door(b, 4, 2, 7, 'north', step='mud_brick_stairs')
    hp.cone_roof(b, 4, 9, 2.5, top, inside, eave=1.3)
    b.chest(5, 2, 10, 'west', loot=VILLAGE + 'tannery')
    b.set(3, 2, 10, 'barrel', facing='up', open=False)
    hp.lantern(b, 4, 5, 9)
    # Vats and racks.
    floor(b, 7, 3, 13, 12, rng, mix=('coarse_dirt', 'packed_mud', 'mud', 'coarse_dirt'))
    b.set(8, 1, 5, 'cauldron')
    b.set(9, 1, 5, 'water_cauldron', level=3)
    b.set(10, 1, 5, 'water_cauldron', level=2)
    b.set(11, 1, 5, 'cauldron')
    hp.drying_rack(b, 8, 8, 'x', length=5, hides=('brown', 'orange', 'white'), face='north')
    hp.drying_rack(b, 8, 11, 'x', length=5, hides=('white', 'brown', 'orange'), face='north')
    b.set(13, 1, 4, 'hay_block', axis='y')
    b.set(13, 1, 3, 'barrel', facing='up', open=False)
    hp.path(b, 4, 0, 5, rng)
    b.entrance(4)
    hp.yard(b, hp.disk(4, 9, 4.6), rng, tufts=.1)
    hp.tufts(b, [(x, z) for x in range(15) for z in range(14)], rng, .04)
    b.natural_ground()
    return b


def cartographer():
    """Mud-brick lookout tower: map room below, a thatched lookout on top reached by ladder."""
    rng = random.Random(5108)
    st = STYLES['mud']
    b = Build('savanna/cartographer', (11, 20, 12))
    body = Body(b, 3, 4, 7, 8, st, heights=(3, 3), spacing=4).build()
    # Lookout deck on the roof with a railing and a little thatched cap on posts.
    for x, z, _, corner in parts.ring(2, 3, 8, 9):
        b.set(x, 9, z, 'acacia_slab', type='top', waterlogged=False)
        b.set(x, 10, z, 'acacia_fence')
    for x, z in ((2, 3), (8, 3), (2, 9), (8, 9)):
        for yy in (10, 11, 12):
            b.set(x, yy, z, 'stripped_acacia_log', axis='y')
    b.fill(3, 13, 4, 7, 13, 8, 'acacia_planks')
    hp.thatch_hip(b, 2, 3, 8, 9, 13, overhang=1, fringe=None)
    hp.door(b, 5, 2, 4, 'north', step='mud_brick_stairs')
    for side, cells in (('west', [(3, 6)]), ('east', [(7, 6)]), ('south', [(5, 8)])):
        for x, z in cells:
            hp.glazed(b, x, 3, z, side, shutters=None)
            hp.glazed(b, x, 7, z, side, shutters=None)
    hp.glazed(b, 4, 7, 4, 'north', shutters=None)
    # Ladder up the back wall through both floors.
    for yy in range(2, 10):
        b.set(6, yy, 7, 'ladder', facing='north', waterlogged=False)
    b.set(4, 2, 7, 'cartography_table')
    b.chest(4, 2, 5, 'east', loot=VILLAGE + 'cartographer')
    hp.lantern(b, 5, 4, 6)
    hp.low_table(b, 4, 6, 6)
    b.set(4, 6, 7, 'barrel', facing='up', open=False)
    b.set(6, 6, 5, 'white_carpet')
    hp.lantern(b, 5, 8, 6)
    hp.lantern(b, 5, 12, 6)
    hp.path(b, 5, 0, 2, rng)
    b.entrance(5)
    hp.yard(b, hp.disk(5, 6, 5.2), rng, tufts=.12)
    b.natural_ground()
    return b


DESIGNS = {
    'savanna/smithy': smithy,
    'savanna/butcher': butcher,
    'savanna/fletcher': fletcher,
    'savanna/shepherd': shepherd,
    'savanna/fisher': fisher,
    'savanna/mason': mason,
    'savanna/tannery': tannery,
    'savanna/cartographer': cartographer,
}
