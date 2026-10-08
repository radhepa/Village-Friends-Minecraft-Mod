"""Snowy farms and pens: a greenhouse, a root cellar, a frost field and pens for goats, rabbits and sled dogs.

These favour the outer streets (``snowy/lots_outer``). Outdoor water may freeze,
so the crops that matter grow under glass; the cellar and fields still hold a
composter for the farmer's trade.
"""
import random

from ...kit import Build
from ... import parts
from . import homes_kit as k

CROPS = {'wheat': 7, 'carrots': 7, 'potatoes': 7, 'beetroots': 3}


def crop(b, x, z, kind, rng):
    b.set(x, 0, z, 'farmland', moisture=7)
    ripe = CROPS[kind]
    b.set(x, 1, z, kind, age=ripe if rng.random() < .65 else max(1, ripe - 2))


def greenhouse():
    """Glass-roofed greenhouse on a log frame: crop beds on farmland with water channels and a composter."""
    rng = random.Random(7301)
    b = Build('snowy/greenhouse', (13, 11, 14))
    x0, z0, x1, z1 = 1, 3, 11, 12
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        b.set(x, 0, z, 'cobblestone')
        post = corner or (facing in ('north', 'south') and (x - x0) % 5 == 0) or \
            (facing in ('west', 'east') and (z - z0) % 3 == 0)
        b.set(x, 1, z, 'cobblestone' if not post else 'spruce_log', **({'axis': 'y'} if post else {}))
        for y in (2, 3):
            b.set(x, y, z, 'spruce_log' if post else 'glass_pane', **({'axis': 'y'} if post else {}))
        b.set(x, 4, z, 'stripped_spruce_log', axis='y' if corner else ('x' if facing in ('north', 'south') else 'z'))
    # Glass gable roof with spruce rafters at each end and down the middle.
    ridge = 4
    for kk in range(0, 6):
        lo, hi, y = x0 + kk, x1 - kk, 4 + kk
        for z in range(z0, z1 + 1):
            rafter = z in (z0, z1, (z0 + z1) // 2)
            for x in {lo, hi}:
                if kk == 0:
                    continue
                b.set(x, y, z, 'spruce_planks' if rafter else 'glass')
        ridge = y
    for z in range(z0, z1 + 1):
        b.set(6, ridge + 1, z, 'spruce_slab', type='bottom', waterlogged=False)
    for z in (z0, z1):
        k.seal_gable(b, z, 5, ridge, x0, x1, 'glass_pane')
    # Beds, channels and an aisle.
    for z in range(z0 + 1, z1):
        b.set(6, 0, z, 'dirt_path')
        for x in (3, 9):
            b.set(x, 0, z, 'water', level=0)
        for x, kind in ((2, 'carrots'), (4, 'potatoes'), (5, 'beetroots'), (7, 'wheat'), (8, 'carrots'),
                        (10, 'potatoes')):
            crop(b, x, z, kind, rng)
    for x in (3, 9):
        b.set(x, 0, z1 - 1, 'cobblestone')
        b.set(x, 1, z1 - 1, 'composter' if x == 3 else 'barrel', **({'level': 5} if x == 3 else
                                                                  {'facing': 'up', 'open': False}))
    b.door(6, 1, z0, facing='south', wood='spruce')
    b.set(6, 0, z0, 'cobblestone')
    for z in (5, 8, 10):
        k.hang(b, 6, ridge - 1, z, links=1)
    k.path_line(b, 6, 0, 2, rng)
    b.entrance(6)
    b.set(9, 1, 1, 'spruce_fence')
    b.set(9, 2, 1, 'lantern', hanging=False, waterlogged=False)
    b.natural_ground()
    return b


def root_cellar():
    """Sod-roofed root cellar with a stone portal, beside a potato and carrot field."""
    rng = random.Random(7302)
    b = Build('snowy/root_cellar', (15, 8, 14))
    x0, z0, x1, z1 = 1, 5, 7, 11
    # Stone vault with an earth mound heaped over it.
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, 0, z, 'cobblestone' if x in (x0, x1) or z in (z0, z1) else 'packed_mud')
            edge = min(x - x0, x1 - x, z - z0, z1 - z)
            h = min(5, 3 + edge)
            for y in range(1, h + 1):
                b.set(x, y, z, rng.choice(['dirt', 'dirt', 'coarse_dirt']))
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 + 1, z1 + 2):
            if x in (x0 - 1, x1 + 1) or z == z1 + 1:
                for y in range(1, 3 if z0 + 2 < z < z1 else 2):
                    b.set(x, y, z, rng.choice(['dirt', 'coarse_dirt']))
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            for y in (1, 2, 3):
                b.set(x, y, z, 'air')
            b.set(x, 4, z, 'spruce_planks')
    for x in range(x0, x1 + 1):
        for y in range(1, 5):
            b.set(x, y, z0, 'stone_bricks' if y < 4 else 'stone_brick_slab', **({'type': 'bottom',
                                                                               'waterlogged': False} if y == 4 else {}))
    b.set(4, 3, z0, 'chiseled_stone_bricks')
    b.door(4, 1, z0, facing='south', wood='spruce')
    for z in (z0 - 1,):
        b.set(3, 1, z, 'spruce_fence')
        b.set(3, 2, z, 'lantern', hanging=False, waterlogged=False)
    # Stores inside.
    for x, z in ((2, 10), (3, 10), (6, 10), (6, 9)):
        b.barrel(x, 1, z, 'up')
    b.barrel(2, 2, 10, 'up')
    b.set(2, 1, 6, 'hay_block', axis='y')
    b.set(6, 1, 6, 'composter', level=6)
    b.set(5, 1, 10, 'pumpkin')
    k.hang(b, 4, 3, 8)
    # Snow on the mound.
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 + 1, z1 + 2):
            top = max(y for y in range(b.h) if b.get(x, y, z)[0] != 'minecraft:air')
            k.snow(b, x, top + 1, z, rng.choice([1, 2, 2, 3]))
    k.leaf(b, 6, 6, 9)
    # The field.
    for x in range(9, 14):
        for z in range(2, 13):
            if x in (9, 13) or z in (2, 12):
                b.set(x, 0, z, 'stripped_spruce_log', axis='z' if x in (9, 13) else 'x')
            elif x == 11:
                b.set(x, 0, z, 'water', level=0)
            else:
                crop(b, x, z, 'potatoes' if x < 11 else 'carrots', rng)
    k.path_line(b, 4, 0, 4, rng)
    b.entrance(4)
    b.natural_ground()
    return b


def goat_pen():
    """Stone-and-fence pen with a lean-to shelter, hay racks and a goat herd."""
    rng = random.Random(7303)
    b = Build('snowy/goat_pen', (15, 9, 14))
    x0, z0, x1, z1 = 0, 2, 14, 13
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if not (x in (x0, x1) or z in (z0, z1)):
                continue
            if (x, z) == (7, z0):
                k.gate(b, x, 1, z, 'north')
                b.set(x, 2, z, 'air')
                continue
            b.set(x, 1, z, 'cobblestone_wall')
            b.set(x, 2, z, 'spruce_fence')
    # Shelter along the back.
    for x in (1, 5, 9, 13):
        for y in (1, 2, 3):
            b.set(x, y, 9, 'spruce_log', axis='y')
    for x in range(0, 15):
        b.set(x, 4, 9, 'spruce_stairs', facing='south', half='bottom')
        for z in (10, 11, 12):
            b.set(x, 4, z, 'spruce_slab', type='top', waterlogged=False)
        b.set(x, 5, 13, 'spruce_slab', type='bottom', waterlogged=False)
        for y in (1, 2, 3, 4):
            if x not in (x0, x1):
                b.set(x, y, 13, 'spruce_planks' if y > 2 else b.get(x, y, 13))
    for x in range(1, 14):
        for y in (3,):
            b.set(x, y, 13, 'spruce_planks')
    for x in (2, 3, 11):
        b.set(x, 1, 12, 'hay_block', axis='x')
    b.set(3, 2, 12, 'hay_block', axis='y')
    b.set(12, 1, 12, 'water_cauldron', level=3)
    k.hang(b, 7, 3, 11)
    # A rocky hump for climbing.
    for x, z, h in ((4, 5, 1), (5, 5, 2), (5, 6, 1), (10, 6, 1)):
        for y in range(1, h + 1):
            b.set(x, y, z, rng.choice(['cobblestone', 'stone', 'andesite']))
    for x, z in ((3, 7), (8, 5), (11, 7)):
        b.animal(x, 1, z, 'goat')
    b.animal(7, 1, 11, 'goat', baby=True)
    k.path_line(b, 7, 0, 1, rng)
    b.entrance(7)
    k.snow_roof(b, 0, 9, 14, 13, rng, 4, cover=.9)
    b.natural_ground()
    return b


def rabbit_hutch():
    """Raised rabbit hutches under a slab roof, with a fenced run and a carrot patch."""
    rng = random.Random(7304)
    b = Build('snowy/rabbit_hutch', (11, 6, 10))
    for x in range(1, 10):
        for z in (6, 7, 8):
            b.set(x, 1, z, 'spruce_planks')
            b.set(x, 3, z, 'spruce_slab', type='top', waterlogged=False)
        b.set(x, 4, 9, 'spruce_slab', type='bottom', waterlogged=False)
        b.set(x, 2, 8, 'spruce_planks')
        b.set(x, 2, 6, 'spruce_fence' if x not in (1, 5, 9) else 'spruce_log', **({} if x not in (1, 5, 9)
                                                                                   else {'axis': 'y'}))
        b.set(x, 4, 6, 'spruce_stairs', facing='south', half='bottom')
        b.set(x, 4, 7, 'spruce_slab', type='bottom', waterlogged=False)
        b.set(x, 4, 8, 'spruce_slab', type='bottom', waterlogged=False)
    for x in (1, 5, 9):
        b.set(x, 2, 7, 'spruce_planks')
        b.set(x, 0, 6, 'cobblestone')
        b.set(x, 0, 8, 'cobblestone')
    for x in (2, 3, 4, 6, 7, 8):
        b.set(x, 2, 7, 'hay_block', axis='x') if x in (2, 8) else None
    b.animal(3, 2, 7, 'rabbit')
    b.animal(7, 2, 7, 'rabbit')
    # Run in front.
    for x in range(0, 11):
        for z in range(1, 6):
            edge = x in (0, 10) or z == 1
            if edge:
                if (x, z) == (5, 1):
                    k.gate(b, x, 1, z, 'north')
                else:
                    b.set(x, 1, z, 'spruce_fence')
    for x in (2, 3, 7, 8):
        for z in (3, 4):
            crop(b, x, z, 'carrots', rng)
    b.animal(5, 1, 3, 'rabbit')
    b.animal(4, 1, 4, 'rabbit', baby=True)
    b.set(9, 1, 2, 'water_cauldron', level=2)
    k.path_line(b, 5, 0, 0, rng)
    b.entrance(5)
    for x in range(1, 10):
        for z in (6, 7, 8, 9):
            s = b.get(x, 4, z)
            if s[0].endswith('_slab'):
                b.set(x, 4, z, 'spruce_planks')
                k.snow(b, x, 5, z, rng.choice([1, 2]))
    b.natural_ground()
    return b


def kennel():
    """Sled-dog kennel: three dog houses in a fenced yard, a parked dog sled and water."""
    rng = random.Random(7305)
    b = Build('snowy/kennel', (13, 7, 12))
    for x in range(0, 13):
        for z in range(1, 12):
            if x in (0, 12) or z in (1, 11):
                if (x, z) == (6, 1):
                    k.gate(b, x, 1, z, 'north')
                else:
                    b.set(x, 1, z, 'spruce_fence')
                    if z == 11 or x in (0, 12):
                        b.set(x, 2, z, 'spruce_fence')
    for i, x0 in enumerate((1, 5, 9)):
        # Dog house: 3x3 box, opening north, peaked plank roof.
        for x in range(x0, x0 + 3):
            for z in (8, 9, 10):
                b.set(x, 0, z, 'spruce_planks')
                edge = x in (x0, x0 + 2) or z == 10
                if edge:
                    b.set(x, 1, z, 'spruce_planks')
                    b.set(x, 2, z, 'spruce_planks' if x == x0 + 1 or z == 10 else 'stripped_spruce_log', axis='y')
            b.set(x, 1, 8, 'air') if x == x0 + 1 else b.set(x, 1, 8, 'spruce_planks')
        for z in range(7, 11):
            b.set(x0, 3, z, 'dark_oak_stairs', facing='east', half='bottom')
            b.set(x0 + 2, 3, z, 'dark_oak_stairs', facing='west', half='bottom')
            b.set(x0 + 1, 3, z, 'dark_oak_planks')
            k.snow(b, x0 + 1, 4, z, 2)
        b.set(x0 + 1, 2, 8, 'spruce_planks')
        b.set(x0 + 1, 1, 9, 'white_carpet' if i != 1 else 'light_gray_carpet')
    for x, z in ((3, 4), (7, 6), (10, 4)):
        b.animal(x, 1, z, 'wolf')
    b.set(2, 1, 3, 'water_cauldron', level=3)
    b.set(11, 1, 2, 'bone_block', axis='y')
    k.sled(b, 6, 1, 3, along='z', load=False)
    b.set(6, 2, 4, 'white_carpet')
    b.set(6, 2, 5, 'barrel', facing='up', open=False)
    k.path_line(b, 6, 0, 0, rng)
    b.entrance(6)
    b.set(4, 1, 0, 'spruce_fence')
    b.set(4, 2, 0, 'lantern', hanging=False, waterlogged=False)
    b.natural_ground()
    return b


def frost_field():
    """Hardy beets and potatoes behind a wattle windbreak, watched by a snowman scarecrow."""
    rng = random.Random(7306)
    b = Build('snowy/frost_field', (13, 6, 13))
    for x in range(0, 13):
        for z in range(2, 13):
            if x in (0, 12) or z in (2, 12):
                b.set(x, 0, z, 'stripped_spruce_log', axis='z' if x in (0, 12) else 'x')
            elif x == 6:
                b.set(x, 0, z, 'water', level=0)
            else:
                crop(b, x, z, 'beetroots' if x < 6 else 'potatoes', rng)
    # Windbreak along the back and west edge.
    for x in range(0, 13):
        b.set(x, 1, 12, 'spruce_fence')
        b.set(x, 2, 12, 'spruce_fence') if x % 3 else b.set(x, 2, 12, 'spruce_log', axis='y')
    for z in range(3, 12):
        b.set(0, 1, z, 'spruce_fence')
    b.set(6, 1, 12, 'composter', level=4)
    # Snowman scarecrow.
    b.set(11, 1, 1, 'snow_block')
    b.set(11, 2, 1, 'snow_block')
    b.set(11, 3, 1, 'carved_pumpkin', facing='north')
    b.set(10, 2, 1, 'spruce_fence')
    b.set(12, 2, 1, 'spruce_fence')
    b.set(6, 0, 0, 'dirt_path')
    b.set(6, 0, 1, 'dirt_path')
    b.set(1, 1, 1, 'hay_block', axis='y')
    b.set(2, 1, 1, 'barrel', facing='up', open=False)
    b.entrance(6)
    b.natural_ground()
    return b


DESIGNS = {
    'snowy/greenhouse': greenhouse,
    'snowy/root_cellar': root_cellar,
    'snowy/goat_pen': goat_pen,
    'snowy/rabbit_hutch': rabbit_hutch,
    'snowy/kennel': kennel,
    'snowy/frost_field': frost_field,
}
