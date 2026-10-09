"""The shepherd's fold: a hill shepherd living alone with the flock.

A small dry-stone hut under a steep spruce roof with a hay ridge, a loom and a hearth
inside; a round dry-stone sheepfold with a handful of sheep, hay and a water trough; a
lookout rock with a seat and a lantern, a lone spruce.
"""
import math
import random

from ...kit import Build
from ... import parts
from ...parts import ROOFS
from .common import start, dweller, path, gate, hay_pile, tufts

SHEEP_COLORS = (0, 8, 7, 12, 15, 0)  # white, light grey, grey, brown, black, white


def shepherd_fold():
    rng = random.Random(5150)
    b = Build('homesteads/shepherd_fold', (24, 13, 22))

    # The hut: dry-stone walls with spruce corner posts, a steep roof along Z.
    x0, z0, x1, z1 = 2, 4, 8, 11
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, 0, z, 'cobblestone')
            b.set(x, 1, z, 'spruce_planks' if x0 < x < x1 and z0 < z < z1 else 'cobblestone')
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        for y in range(2, 5):
            if corner:
                b.set(x, y, z, parts.log('spruce_log'))
            else:
                b.set(x, y, z, 'mossy_cobblestone' if rng.random() < .4 else 'cobblestone')
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        b.set(x, 5, z, parts.log('stripped_spruce_log', 'y' if corner else ('x' if facing in ('north', 'south') else 'z')))
    b.fill(x0 + 1, 5, z0 + 1, x1 - 1, 5, z1 - 1, 'spruce_planks')
    ridge = parts.gable_roof(b, x0, z0, x1, z1, 5, ROOFS['spruce'], axis='z', overhang=1, rake=1, gable='spruce_planks', pitch=1)
    for z in range(z0 - 1, z1 + 2):
        b.set(5, ridge, z, 'hay_block', axis='z')
    b.door(5, 2, z0, facing='south', wood='spruce')
    b.set(5, 1, z0 - 1, 'cobblestone_stairs', facing='south', half='bottom')
    parts.window(b, 2, 3, 7, 'west', height=1, trim='spruce')
    parts.window(b, 8, 3, 6, 'east', height=1, trim='spruce')
    parts.window(b, 8, 3, 9, 'east', height=1, trim='spruce')
    b.set(3, 3, 4, 'glass_pane')
    b.set(7, 3, 4, 'glass_pane')

    # Inside: hearth in the back wall, bed, loom, chest, a wool rug.
    b.set(5, 2, z1, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    for y in range(3, ridge + 2):
        b.set(5, y, z1, 'cobblestone')
    b.set(5, ridge + 2, z1, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    b.set(4, 2, z1, 'cobblestone')
    b.set(6, 2, z1, 'cobblestone')
    b.bed(3, 2, 10, 'north', 'light_gray')
    b.chest(3, 2, 7, 'east', loot='minecraft:chests/village/village_shepherd')
    b.set(7, 2, 5, 'loom', facing='west')
    b.barrel(7, 2, 10, 'up')
    b.set(7, 2, 9, 'white_wool')
    parts.rug(b, 4, 6, 6, 9, 2, 'white', 'brown')
    parts.lantern(b, 5, 4, 7)
    b.room('hut', (4, 3, 6))

    # The sheepfold: a ring of dry-stone wall round grass, hay and a water trough.
    cx, cz, r = 16, 12, 5.6
    ring = {(x, z) for x in range(cx - 7, cx + 8) for z in range(cz - 7, cz + 8) if r - .5 <= math.hypot(x - cx, z - cz) <= r + .5}
    # Close every diagonal step with the outer of its two corner cells, so the wall runs unbroken.
    for x, z in list(ring):
        for dx, dz in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            if (x + dx, z + dz) in ring and (x + dx, z) not in ring and (x, z + dz) not in ring:
                ring.add(max(((x + dx, z), (x, z + dz)), key=lambda c: math.hypot(c[0] - cx, c[1] - cz)))
    for x, z in sorted(ring):
        b.set(x, 1, z, 'mossy_cobblestone_wall' if rng.random() < .45 else 'cobblestone_wall')
        if rng.random() < .25:
            b.set(x, 0, z, 'cobblestone')
    gate(b, cx - 6, 1, cz, 'east')
    hay_pile(b, [(cx + 2, 1, cz - 3), (cx + 3, 1, cz - 3), (cx + 3, 1, cz - 2), (cx + 3, 2, cz - 3)])
    for x in (cx + 1, cx + 2):
        b.set(x, 0, cz + 3, 'stone_bricks')
    for x, z in ((cx, cz + 3), (cx + 3, cz + 3), (cx + 1, cz + 4), (cx + 2, cz + 4), (cx + 1, cz + 2), (cx + 2, cz + 2)):
        b.set(x, 1, z, 'stone_brick_slab', type='bottom')
    for x in (cx + 1, cx + 2):
        b.set(x, 1, cz + 3, 'water', level=0)
    start(b, cx - 1, cz - 1, 'hay_block')
    for (sx, sz), color in zip(((14, 12), (15, 10), (17, 11), (15, 14), (13, 13)), SHEEP_COLORS):
        b.animal(sx, 1, sz, 'sheep', Color=color)
    b.animal(16, 1, 13, 'sheep', baby=True, Color=0)

    # The lookout rock with a stump seat and a lantern, a lone spruce, a wool line by the hut.
    for (x, y, z) in ((3, 1, 16), (4, 1, 16), (3, 1, 17), (4, 1, 17), (5, 1, 17), (3, 2, 17), (4, 2, 17), (2, 1, 17), (4, 1, 18)):
        b.set(x, y, z, rng.choice(['mossy_cobblestone', 'cobblestone', 'andesite', 'stone']))
    b.set(3, 3, 17, 'spruce_slab', type='bottom')
    parts.lamp_post(b, 6, 1, 17, height=2)
    parts.spruce_tree(b, 21, 1, 3, height=7)
    for x in (10, 13):
        for y in (1, 2):
            b.set(x, y, 5, 'spruce_fence')
    for x in range(10, 14):
        b.set(x, 3, 5, 'spruce_fence')
    b.set(11, 1, 6, 'white_wool')
    b.set(12, 1, 6, 'light_gray_wool')
    b.set(12, 2, 6, 'white_wool')

    path(b, [(5, z) for z in range(0, 3)] + [(x, 2) for x in range(5, 9)] + [(9, z) for z in range(2, 13)]
         + [(x, 12) for x in range(9, 11)], rng, mats=('dirt_path', 'coarse_dirt', 'dirt_path', 'gravel'))
    dweller(b, 5, 2, 7, 'shepherd', job='minecraft:shepherd')
    tufts(b, rng, 0, 0, 23, 21, chance=.14)
    b.natural_ground()
    return b


DESIGNS = {'homesteads/shepherd_fold': shepherd_fold}
