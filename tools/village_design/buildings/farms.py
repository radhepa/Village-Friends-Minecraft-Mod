"""Fields, paddocks and gardens. These favour the outer streets (``plains/lots_outer``)."""
import random

from ..kit import Build
from .. import parts

CROPS = {'wheat': 7, 'carrots': 7, 'potatoes': 7, 'beetroots': 3}


def field(b, x0, z0, x1, z1, crop, rng, water_x=None, border='stripped_oak_log'):
    """Log-bordered field with a water channel down the middle."""
    mid = water_x if water_x is not None else (x0 + x1) // 2
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                b.set(x, 0, z, border, axis='z' if x in (x0, x1) else 'x')
            elif x == mid:
                b.set(x, 0, z, 'water', level=0)
            else:
                b.set(x, 0, z, 'farmland', moisture=7)
                ripe = CROPS[crop]
                b.set(x, 1, z, crop, age=ripe if rng.random() < .7 else max(1, ripe - 2))


def scarecrow(b, x, z, facing='north'):
    b.set(x, 1, z, 'spruce_fence')
    b.set(x, 2, z, 'hay_block', axis='y')
    b.set(x, 3, z, 'carved_pumpkin', facing=facing)


def farm_wheat():
    rng = random.Random(601)
    b = Build('farm_wheat', (13, 6, 12))
    field(b, 1, 2, 11, 11, 'wheat', rng)
    scarecrow(b, 0, 1)
    b.set(12, 1, 1, 'composter', level=5)
    b.set(11, 1, 0, 'hay_block', axis='x')
    b.set(12, 1, 0, 'hay_block', axis='z')
    b.set(12, 2, 0, 'hay_block', axis='y')
    b.set(6, 0, 1, 'dirt_path')
    b.set(6, 0, 0, 'dirt_path')
    b.entrance(6)
    b.natural_ground()
    return b


def farm_mixed():
    rng = random.Random(602)
    b = Build('farm_mixed', (15, 6, 11))
    field(b, 0, 2, 6, 10, 'carrots', rng, water_x=3)
    field(b, 8, 2, 14, 10, 'potatoes', rng, water_x=11)
    for z in range(0, 11):
        b.set(7, 0, z, 'dirt_path' if z % 3 else 'coarse_dirt')
    b.set(7, 1, 10, 'composter', level=3)
    b.set(14, 1, 1, 'barrel', facing='up', open=False)
    b.set(0, 1, 1, 'hay_block', axis='y')
    b.entrance(7)
    b.natural_ground()
    return b


def farm_beets():
    rng = random.Random(603)
    b = Build('farm_beets', (9, 6, 10))
    field(b, 0, 1, 8, 9, 'beetroots', rng)
    scarecrow(b, 8, 0, 'north')
    b.set(0, 1, 0, 'composter', level=6)
    b.entrance(4)
    b.set(4, 0, 0, 'dirt_path')
    b.natural_ground()
    return b


def pumpkin_patch():
    rng = random.Random(604)
    b = Build('pumpkin_patch', (11, 6, 10))
    for x in range(0, 11):
        for z in range(1, 10):
            if x in (0, 10) or z in (1, 9):
                b.set(x, 1, z, 'oak_fence') if not (x == 5 and z == 1) else None
                continue
            if x == 5:
                b.set(x, 0, z, 'water', level=0)
                continue
            b.set(x, 0, z, 'farmland', moisture=7)
            if z % 2 == 0:
                fruit = 'pumpkin' if x < 5 else 'melon'
                b.set(x, 1, z, fruit) if rng.random() < .5 else b.set(x, 1, z, f'{fruit}_stem', age=7)
            else:
                b.set(x, 1, z, f'{"pumpkin" if x < 5 else "melon"}_stem', age=rng.randrange(4, 8))
    b.set(5, 1, 1, 'oak_fence_gate', facing='north', open=False, in_wall=False, powered=False)
    b.set(5, 0, 0, 'dirt_path')
    b.set(5, 0, 1, 'dirt_path')
    b.set(1, 1, 0, 'carved_pumpkin', facing='north')
    b.set(9, 1, 0, 'hay_block', axis='y')
    b.entrance(5)
    b.natural_ground()
    return b


def paddock():
    """Fenced paddock with a field shelter, trough, hay and livestock."""
    rng = random.Random(605)
    b = Build('paddock', (15, 8, 13))
    for x in range(0, 15):
        for z in range(1, 13):
            edge = x in (0, 14) or z in (1, 12)
            if edge:
                if x == 7 and z == 1:
                    b.set(x, 1, z, 'spruce_fence_gate', facing='north', open=False, in_wall=False, powered=False)
                else:
                    b.set(x, 1, z, 'spruce_fence')
            else:
                b.set(x, 0, z, 'grass_block')
                if rng.random() < .1:
                    b.set(x, 1, z, 'short_grass')
    # Field shelter in the back corner.
    for x, z in ((9, 8), (13, 8), (9, 11), (13, 11)):
        for y in (1, 2, 3):
            b.set(x, y, z, 'spruce_fence')
    for x in range(8, 15):
        for z in range(7, 13):
            b.set(x, 4, z, 'spruce_slab', type='bottom')
    for x in (10, 11, 12):
        b.set(x, 1, 11, 'hay_block', axis='x')
    b.set(12, 2, 11, 'hay_block', axis='y')
    for x in (2, 3):
        b.set(x, 1, 11, 'water_cauldron', level=3)
    b.set(7, 0, 0, 'dirt_path')
    b.set(7, 0, 1, 'dirt_path')
    for x, z, kind in ((4, 5, 'cow'), (10, 4, 'cow'), (5, 8, 'sheep'), (3, 3, 'chicken'), (11, 6, 'chicken'),
                       (6, 9, 'pig')):
        b.animal(x, 1, z, kind)
    b.entrance(7)
    b.natural_ground()
    return b


def apiary():
    """Beehives among wildflowers."""
    rng = random.Random(606)
    b = Build('apiary', (9, 6, 9))
    for x in range(0, 9):
        for z in range(1, 9):
            b.set(x, 0, z, 'grass_block')
            if rng.random() < .55:
                b.set(x, 1, z, parts.flowers(rng))
    for x, z in ((2, 3), (6, 3), (2, 6), (6, 6)):
        b.set(x, 1, z, 'spruce_fence')
        b.set(x, 2, z, 'beehive', facing='north', honey_level=rng.randrange(0, 4))
    b.set(4, 0, 0, 'dirt_path')
    b.set(4, 0, 1, 'dirt_path')
    b.set(4, 1, 1, 'air')
    b.entrance(4)
    b.natural_ground()
    return b


DESIGNS = {'farm_wheat': farm_wheat, 'farm_mixed': farm_mixed, 'farm_beets': farm_beets,
           'pumpkin_patch': pumpkin_patch, 'paddock': paddock, 'apiary': apiary}
