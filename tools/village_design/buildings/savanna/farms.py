"""Savanna fields, kraals, paddocks and a chicken coop. These favour the outer streets
(``savanna/lots_outer``)."""
import math
import random

from ...kit import Build
from ... import parts
from . import homes_parts as hp

CROPS = {'wheat': 7, 'carrots': 7, 'potatoes': 7, 'beetroots': 3}


def field(b, x0, z0, x1, z1, crop, rng, water_x=None, border='stripped_acacia_log'):
    """Log-bordered field on farmland with a water channel down the middle."""
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
    b.set(x, 1, z, 'acacia_fence')
    b.set(x, 2, z, 'hay_block', axis='y')
    b.set(x, 3, z, 'carved_pumpkin', facing=facing)
    b.set(x, 4, z, 'orange_carpet')


def farm_wheat():
    """Wheat field behind a woven fence, with a scarecrow, a thatched hay stack and a composter."""
    rng = random.Random(6101)
    b = Build('savanna/farm_wheat', (15, 7, 13))
    field(b, 1, 2, 13, 12, 'wheat', rng)
    for x in range(0, 15):
        if x not in (6, 7, 8):
            b.set(x, 1, 1, 'acacia_fence')
    scarecrow(b, 4, 7)
    b.set(14, 1, 2, 'composter', level=5)
    hp.hay_pile(b, [(12, 0), (13, 0), (14, 0), (13, 1)], rng, high=[(13, 0)])
    b.set(13, 3, 0, 'acacia_slab', type='bottom', waterlogged=False)
    hp.path(b, 7, 0, 1, rng)
    b.entrance(7)
    b.natural_ground()
    return b


def farm_beets_melon():
    """Beetroot beds and a melon patch either side of a shared water channel."""
    rng = random.Random(6102)
    b = Build('savanna/farm_beets_melon', (15, 6, 12))
    field(b, 0, 2, 7, 11, 'beetroots', rng, water_x=3)
    # Melons: stems on farmland beside the channel, fruit on dirt beside them.
    for x in range(7, 15):
        for z in range(2, 12):
            if x in (14,) or z in (2, 11):
                b.set(x, 0, z, 'stripped_acacia_log', axis='z' if x == 14 else 'x')
            elif x == 7:
                b.set(x, 0, z, 'water', level=0)
            elif x in (8, 11):
                b.set(x, 0, z, 'farmland', moisture=7)
                b.set(x, 1, z, 'melon_stem', age=7)
            else:
                b.set(x, 0, z, 'coarse_dirt' if x in (9, 12) else 'dirt')
                if x in (9, 12) and z % 2 == 0:
                    b.set(x, 1, z, 'melon')
                elif x == 10 and z % 3 == 0:
                    b.set(x, 1, z, 'short_dry_grass')
    for z in range(2, 12):
        b.set(7, 0, z, 'water', level=0)
    b.set(7, 0, 2, 'stripped_acacia_log', axis='x')
    b.set(7, 0, 11, 'stripped_acacia_log', axis='x')
    b.set(0, 1, 1, 'composter', level=3)
    b.set(14, 1, 1, 'barrel', facing='up', open=False)
    hp.pot(b, 13, 1, 1)
    hp.path(b, 7, 0, 1, rng)
    b.entrance(7)
    b.natural_ground()
    return b


def farm_roots():
    """Carrot and potato plots with a drying rack and a water pot at the head of the rows."""
    rng = random.Random(6103)
    b = Build('savanna/farm_roots', (15, 6, 11))
    field(b, 0, 2, 6, 10, 'carrots', rng, water_x=3)
    field(b, 8, 2, 14, 10, 'potatoes', rng, water_x=11)
    for z in range(0, 11):
        b.set(7, 0, z, rng.choice(['dirt_path', 'dirt_path', 'coarse_dirt', 'packed_mud']))
    b.set(7, 1, 10, 'composter', level=4)
    hp.drying_rack(b, 0, 0, 'x', length=4, hides=('brown',), face='north')
    b.set(14, 1, 1, 'water_cauldron', level=3)
    hp.pot(b, 13, 1, 1)
    b.entrance(7)
    b.natural_ground()
    return b


def kraal():
    """Round cattle kraal: a woven acacia ring hedged with dead brush, hay and a trough in the middle."""
    rng = random.Random(6104)
    b = Build('savanna/kraal', (17, 6, 18))
    cx, cz, r = 8, 9.5, 7.0
    ring = hp.outline(hp.disk(cx, cz, r))
    gate = (8, 3)
    for x, z in ring:
        if (x, z) == gate:
            b.set(x, 1, z, 'acacia_fence_gate', facing='north', open=False, in_wall=False, powered=False)
        else:
            b.set(x, 1, z, 'acacia_fence')
    # Thorn brush piled against the outside of the ring.
    outer = hp.outline(hp.disk(cx, cz, r + 1)) - hp.disk(cx, cz, r)
    for x, z in sorted(outer):
        if b.inside(x, 1, z) and abs(x - gate[0]) > 1 and rng.random() < .55:
            b.set(x, 0, z, 'coarse_dirt')
            b.set(x, 1, z, rng.choice(['dead_bush', 'dead_bush', 'tall_dry_grass', 'bush']))
    # Trampled floor, hay and trough.
    for x, z in hp.disk(cx, cz, r - 1):
        if rng.random() < .35:
            b.set(x, 0, z, rng.choice(['coarse_dirt', 'dirt', 'coarse_dirt', 'packed_mud']))
    hp.hay_pile(b, [(8, 10), (9, 10), (8, 11)], rng, high=[(8, 10)])
    for x in (5, 6):
        b.set(x, 1, 13, 'water_cauldron', level=3)
    for x, z in ((5, 7), (11, 7), (11, 12), (6, 10)):
        b.animal(x, 1, z, 'cow')
    b.animal(10, 1, 9, 'cow', baby=True)
    b.set(8, 0, 2, 'dirt_path')
    b.set(8, 0, 1, 'dirt_path')
    b.set(8, 0, 0, 'dirt_path')
    b.set(8, 0, 3, 'dirt_path')
    hp.post_lantern(b, 6, 1, 1)
    b.entrance(8)
    b.natural_ground()
    return b


def paddock():
    """Horse and goat paddock with a thatched field shelter, hay rack and trough."""
    rng = random.Random(6105)
    b = Build('savanna/paddock', (17, 8, 14))
    pen = [(x, z) for x, z, _, _ in parts.ring(0, 1, 16, 13)]
    hp.woven_fence(b, pen, gate=(8, 1), gate_facing='north')
    # Shelter in the back-east corner.
    for x, z in ((11, 9), (15, 9), (11, 12), (15, 12)):
        for yy in (1, 2, 3):
            b.set(x, yy, z, 'stripped_acacia_log', axis='y')
    for x in range(11, 16):
        for z in range(9, 13):
            b.set(x, 4, z, 'acacia_planks' if x in (11, 15) or z in (9, 12) else 'acacia_slab',
                  **({} if x in (11, 15) or z in (9, 12) else {'type': 'top', 'waterlogged': False}))
    hp.thatch_hip(b, 11, 9, 15, 12, 5, overhang=1, fringe=None)
    for x in (12, 13, 14):
        b.set(x, 1, 12, 'hay_block', axis='x')
    b.set(14, 2, 12, 'hay_block', axis='y')
    for x in (2, 3, 4):
        b.set(x, 1, 12, 'water_cauldron', level=3)
    b.set(2, 1, 3, 'hay_block', axis='y')
    for x, z in ((4, 6), (12, 4)):
        b.animal(x, 1, z, 'horse')
    for x, z in ((7, 9), (9, 10)):
        b.animal(x, 1, z, 'goat')
    b.animal(6, 1, 4, 'goat', baby=True)
    hp.tufts(b, [(x, z) for x in range(1, 16) for z in range(2, 13)], rng, .1)
    b.set(8, 0, 0, 'dirt_path')
    b.set(8, 0, 1, 'dirt_path')
    b.entrance(8)
    b.natural_ground()
    return b


def coop():
    """Raised chicken coop of mud and acacia on stilts, with a fenced run."""
    rng = random.Random(6106)
    b = Build('savanna/coop', (12, 10, 12))
    run = [(x, z) for x, z, _, _ in parts.ring(0, 2, 11, 11)]
    hp.woven_fence(b, run, gate=(5, 2), gate_facing='north')
    # Coop house on stilts in the back.
    for x, z in ((6, 7), (10, 7), (6, 10), (10, 10)):
        b.set(x, 1, z, 'acacia_fence')
    b.fill(6, 2, 7, 10, 2, 10, 'acacia_planks')
    for x, z, facing, corner in parts.ring(6, 7, 10, 10):
        for yy in (3, 4):
            b.set(x, yy, z, 'stripped_acacia_log' if corner else 'packed_mud', **({'axis': 'y'} if corner else {}))
    b.set(8, 3, 7, 'air')
    b.set(8, 4, 7, 'air')
    hp.slit(b, 10, 4, 8)
    for x in (7, 9):
        b.set(x, 3, 9, 'hay_block', axis='y')
    b.set(8, 3, 9, 'composter', level=7)
    hp.thatch_hip(b, 6, 7, 10, 10, 5, overhang=1, fringe=None)
    # Ramp up to the coop door.
    b.set(8, 1, 6, 'acacia_slab', type='bottom', waterlogged=False)
    b.set(8, 2, 6, 'acacia_slab', type='bottom', waterlogged=False)
    b.set(8, 1, 6, 'acacia_slab', type='top', waterlogged=False)
    b.set(8, 1, 5, 'acacia_slab', type='bottom', waterlogged=False)
    for x, z in ((2, 5), (4, 8), (3, 10), (8, 4), (10, 4)):
        b.animal(x, 1, z, 'chicken')
    b.animal(2, 1, 8, 'chicken', baby=True)
    b.set(1, 1, 10, 'water_cauldron', level=3)
    hp.tufts(b, [(x, z) for x in range(1, 11) for z in range(3, 11)], rng, .12)
    hp.path(b, 5, 0, 2, rng)
    b.entrance(5)
    b.natural_ground()
    return b


DESIGNS = {
    'savanna/farm_wheat': farm_wheat,
    'savanna/farm_beets_melon': farm_beets_melon,
    'savanna/farm_roots': farm_roots,
    'savanna/kraal': kraal,
    'savanna/paddock': paddock,
    'savanna/coop': coop,
}
