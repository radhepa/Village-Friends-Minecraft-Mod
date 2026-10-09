"""The lone farmstead: a husband and wife farming on their own.

A long, low farmhouse of fieldstone and white plaster under a dark oak roof, with a
covered porch, a kitchen and a shared bedroom, a woodshed lean-to, a fenced field of
wheat and carrots with a scarecrow, a hen run and coop, a kitchen garden, a well, a
haystack and an old oak. He farms (the composter by the field gate); she keeps the
house and the hens (the kitchen stove).
"""
import random

from ...kit import Build
from ... import parts
from ...parts import Body, Style, ROOFS
from ..farms import scarecrow
from .common import start, dweller, path, fence_ring, well, hay_pile, tufts

STYLE = Style(frame='stripped_oak_log', fill='calcite', floor='spruce_planks', roof='dark_oak',
              base='cobblestone', trim='spruce', door='spruce', upper_fill='calcite')
LOOT = 'minecraft:chests/village/village_plains_house'


def farmstead():
    rng = random.Random(9101)
    b = Build('homesteads/farmstead', (28, 14, 23))

    # The farmhouse: a fieldstone course under white plaster, a dark oak roof along X.
    body = Body(b, 2, 5, 12, 11, STYLE, heights=(3,), spacing=5).build()
    for x, z, facing, corner in parts.ring(2, 5, 12, 11):
        if not corner:
            b.set(x, 2, z, 'cobblestone')
    body.roof(axis='x', pitch=1, gable='calcite', trim=ROOFS['spruce'])
    body.windows(0, 'north', [1, 8], height=1)
    body.windows(0, 'south', [2, 8], height=1, box='flowering_azalea_leaves')
    body.windows(0, 'east', [3], height=1)
    body.gable_window('east')
    body.gable_window('west')
    b.door(5, 2, 5, facing='south', wood='spruce')
    b.door(6, 2, 11, facing='north', wood='spruce', hinge='right')

    # The porch: a plank deck under a lean-to roof, a bench against the wall.
    for x in range(2, 13):
        for z in (3, 4):
            b.set(x, 0, z, 'cobblestone')
            b.set(x, 1, z, 'spruce_planks')
    for x in (2, 8, 12):
        for y in (2, 3):
            b.set(x, y, 3, parts.log('stripped_oak_log'))
    for x in range(1, 14):
        b.set(x, 4, 2, 'spruce_stairs', facing='south', half='bottom')
        b.set(x, 4, 3, 'spruce_slab', type='top')
        b.set(x, 4, 4, 'spruce_slab', type='top')
    for x in (4, 5, 6):
        b.set(x, 1, 2, 'spruce_stairs', facing='south', half='bottom')
    parts.bench(b, 9, 2, 4, 'south', length=2)
    b.set(11, 2, 4, 'potted_red_tulip')
    b.set(3, 2, 4, 'barrel', facing='up', open=False)
    parts.lantern(b, 6, 3, 3)
    parts.lantern(b, 11, 3, 3)

    # Chimney on the west gable.
    for y in range(1, 5):
        b.set(1, y, 8, 'cobblestone')
    parts.chimney(b, 1, 8, 5, body.ridge + 1, 'cobblestone')
    b.set(1, 1, 7, 'cobblestone_stairs', facing='south', half='bottom')
    b.set(1, 1, 9, 'cobblestone_stairs', facing='north', half='bottom')

    # Inside: the kitchen and table to the west, the bedroom behind a partition to the east.
    for z in range(6, 11):
        for y in (2, 3, 4):
            b.set(8, y, z, 'spruce_planks')
    b.door(8, 2, 8, facing='east', wood='spruce')
    b.custom(3, 2, 6, 'kitchen_stove', facing='east')
    b.set(3, 2, 7, 'smoker', facing='east', lit=True)
    b.barrel(3, 2, 9, 'up')
    b.chest(3, 2, 10, 'east', loot=LOOT)
    b.set(4, 2, 10, 'crafting_table')
    parts.table(b, 5, 2, 8)
    parts.chair(b, 5, 2, 9, 'south')
    parts.chair(b, 6, 2, 8, 'east')
    b.set(7, 2, 10, 'potted_red_tulip')
    b.set(7, 2, 6, 'barrel', facing='up', open=False)
    parts.lantern(b, 5, 4, 8)
    b.bed(9, 2, 10, 'north', 'brown')
    b.bed(11, 2, 10, 'north', 'brown')
    b.chest(10, 2, 10, 'north', loot=LOOT)
    b.set(11, 2, 6, 'flower_pot')
    b.set(9, 2, 6, 'bookshelf')
    parts.rug(b, 10, 7, 11, 8, 2, 'yellow', 'brown')
    parts.lantern(b, 10, 4, 8)
    b.room('bedroom', (10, 3, 7))

    # The woodshed lean-to on the east gable.
    for z in (6, 10):
        for y in (1, 2, 3):
            b.set(14, y, z, parts.log('stripped_oak_log'))
    for z in range(5, 12):
        b.set(13, 4, z, 'spruce_slab', type='top')
        b.set(14, 4, z, 'spruce_stairs', facing='west', half='bottom')
    parts.woodpile(b, 13, 1, 7, along_axis='z', length=3, wood='oak', height=2)
    start(b, 14, 9, 'oak_log')

    # The hen run with its little coop, north-east.
    fence_ring(b, 15, 1, 22, 7, gates=((15, 5, 'east'),))
    for x in range(18, 22):
        for z in range(1, 4):
            b.set(x, 0, z, 'spruce_planks')
            corner = x in (18, 21) and z in (1, 3)
            if x in (18, 21) or z in (1, 3):
                for y in (1, 2):
                    b.set(x, y, z, parts.log('stripped_spruce_log') if corner else 'spruce_planks')
    b.set(19, 1, 3, 'air')
    b.set(20, 1, 2, 'hay_block', axis='x')
    parts.gable_roof(b, 18, 1, 21, 3, 3, ROOFS['spruce'], axis='x', overhang=1, rake=0, gable='spruce_planks')
    b.set(16, 1, 6, 'cauldron')
    b.set(21, 1, 6, 'hay_block', axis='y')
    for x, z in ((17, 5), (19, 5), (20, 6)):
        b.animal(x, 1, z, 'chicken')

    # The field: wheat and carrots either side of a water channel, a scarecrow, the farmer's composter.
    fx0, fz0, fx1, fz1 = 14, 10, 26, 21
    fence_ring(b, fx0, fz0, fx1, fz1, gates=((fx0, 15, 'east'),))
    for x in range(fx0 + 1, fx1):
        for z in range(fz0 + 1, fz1):
            if z == 15:
                b.set(x, 0, z, 'water', level=0)
            elif x == fx0 + 1 and z in (11, 12):
                b.set(x, 0, z, 'coarse_dirt')
            else:
                b.set(x, 0, z, 'farmland', moisture=7)
                b.set(x, 1, z, 'wheat' if z < 15 else 'carrots', age=7 if rng.random() < .7 else 5)
    b.set(fx0 + 1, 1, 11, 'composter', level=4)
    b.set(fx0 + 1, 1, 12, 'barrel', facing='up', open=False)
    for x in (18, 23):
        b.set(x, 0, 15, 'spruce_planks')
    b.set(21, 0, 12, 'dirt')
    b.set(21, 1, 12, 'air')
    scarecrow(b, 21, 12, facing='west')

    # The kitchen garden behind the house.
    for x in range(2, 8):
        for z in range(14, 19):
            edge = x in (2, 7) or z in (14, 18)
            if edge:
                b.set(x, 0, z, parts.log('stripped_spruce_log', 'z' if x in (2, 7) else 'x'))
            elif x == 4:
                b.set(x, 0, z, 'dirt_path')
            else:
                b.set(x, 0, z, 'farmland', moisture=7)
                b.set(x, 1, z, 'beetroots' if x < 4 else 'potatoes', age=3 if x < 4 else 7)
    b.set(4, 0, 18, 'dirt_path')

    # The yard: well, haystack, an old oak, the lane sign.
    well(b, 10, 15)
    hay_pile(b, [(9, 1, 19), (10, 1, 19), (9, 1, 20), (9, 2, 19), (11, 1, 20)])
    b.set(10, 1, 20, 'hay_block', axis='y')
    parts.oak_tree(b, 2, 1, 21, rng, height=5, radius=2)
    b.set(7, 1, 1, 'spruce_fence')
    b.sign(7, 2, 1, ['Fresh eggs', 'and bread', '', 'knock at the door'], facing='north', wall=False)
    lane = [(5, z) for z in range(0, 3)] + [(x, 1) for x in range(6, 15)]
    yard = [(6, z) for z in range(12, 14)] + [(x, 13) for x in range(7, 14)] + [(13, z) for z in range(14, 16)] \
        + [(x, 13) for x in range(3, 6)] + [(4, 13)]
    path(b, lane + yard, rng)
    parts.flower_bed(b, 0, 3, 1, 4, 0, rng, soil='grass_block', density=.9)

    dweller(b, 6, 2, 7, 'homesteader', job='minecraft:farmer', gender='male')
    dweller(b, 4, 2, 8, 'homesteader', job='cook', gender='female')
    b.animal(7, 2, 9, 'cat')
    tufts(b, rng, 0, 0, 27, 22, chance=.10)
    b.natural_ground()
    return b


DESIGNS = {'homesteads/farmstead': farmstead}
