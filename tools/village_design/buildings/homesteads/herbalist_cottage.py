"""The herbalist's cottage: a hedge-herbalist living alone at the edge of the woods.

A crooked little cottage of mud brick and dark oak under a steep, mossy roof, with a potting
lean-to behind. Inside, a cauldron bubbles over a fire in the corner, herbs and roots hang from
the rafters, a spore blossom drifts by the bed and the alchemical press waits for the night's
callers. Outside: a fenced herb garden, sweet berries, a beehive heavy with honey, a fairy ring
of mushrooms and an old oak hung with vines.
"""
import math
import random

from ...kit import Build
from ... import parts
from ...parts import Body, Style, ROOFS
from .common import start, dweller, path, fence_ring, tufts

STYLE = Style(frame='stripped_dark_oak_log', fill='mud_bricks', floor='spruce_planks', roof='dark_oak',
              base='mossy_cobblestone', trim='spruce', door='spruce', upper_fill='mud_bricks')
HERBS = ('allium', 'azure_bluet', 'cornflower', 'lily_of_the_valley', 'oxeye_daisy', 'poppy', 'dandelion', 'fern')


def herbalist_cottage():
    rng = random.Random(4242)
    b = Build('homesteads/herbalist_cottage', (21, 16, 21))

    # The cottage: mud brick between dark oak, a steep dark oak roof along X with moss creeping over it.
    body = Body(b, 5, 6, 12, 12, STYLE, heights=(3,), spacing=3).build()
    body.roof(axis='x', pitch=2, gable='mud_bricks', trim=ROOFS['spruce'])
    for (x, y, z), state in list(b.grid.items()):
        if state[0] == 'minecraft:dark_oak_stairs' and y > 5 and rng.random() < .22:
            b.set(x, y, z, ('minecraft:mossy_cobblestone_stairs', state[1]))
    b.door(8, 2, 6, facing='south', wood='spruce')
    b.set(8, 1, 5, 'mossy_cobblestone_stairs', facing='south', half='bottom')
    for x in (7, 9):
        b.set(x, 2, 5, 'spruce_fence')
        b.set(x, 3, 5, 'spruce_fence')
    for x in (7, 8, 9):
        b.set(x, 4, 5, 'spruce_slab', type='bottom')
    body.windows(0, 'north', [1, 6], height=1, box='flowering_azalea_leaves')
    body.windows(0, 'west', [3], height=1, box='azalea_leaves')
    body.windows(0, 'south', [2], height=1)
    b.set(12, 3, 7, 'glass_pane')
    body.gable_window('west')

    # The chimney climbs the east gable and leans at the top.
    for y in range(1, 9):
        b.set(13, y, 9, 'mossy_cobblestone' if rng.random() < .5 else 'cobblestone')
    for y in range(9, body.ridge + 2):
        b.set(13, y, 10, 'mossy_cobblestone' if rng.random() < .5 else 'cobblestone')
    b.set(13, 9, 9, 'cobblestone_stairs', facing='north', half='top')
    b.set(13, body.ridge + 2, 10, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)

    # Inside: the cauldron over a fire, the press, the brewing stand, a bed, hanging herbs.
    b.set(6, 2, 11, 'campfire', lit=True, signal_fire=False, facing='east', waterlogged=False)
    b.set(6, 3, 11, 'water_cauldron', level=3)
    b.set(7, 2, 11, 'cobblestone')
    b.custom(11, 2, 8, 'alchemical_press', facing='west')
    b.set(11, 2, 10, 'brewing_stand', has_bottle_0=True, has_bottle_1=False, has_bottle_2=True)
    b.bed(10, 2, 11, 'west', 'green')
    b.chest(11, 2, 11, 'west', loot='minecraft:chests/village/village_plains_house')
    for z in (7, 8):
        b.set(6, 2, z, 'bookshelf')
    b.set(6, 3, 7, 'potted_red_mushroom')
    b.set(6, 3, 8, 'potted_fern')
    b.set(11, 3, 11, 'potted_azure_bluet')
    b.set(7, 2, 7, 'decorated_pot', facing='south', cracked=False, waterlogged=False)
    parts.table(b, 8, 2, 9)
    b.set(8, 3, 9, 'candle', candles=3, lit=True, waterlogged=False)
    parts.chair(b, 8, 2, 10, 'south')
    for x, z in ((7, 9), (9, 7), (10, 10), (7, 8)):
        b.set(x, 4, z, 'hanging_roots', waterlogged=False)
    b.set(9, 4, 11, 'spore_blossom')
    parts.lantern(b, 10, 4, 8)
    parts.rug(b, 9, 8, 10, 9, 2, 'green', None)
    b.room('cottage', (9, 3, 9))

    # The potting lean-to behind, with its tools and pots.
    for x in (6, 9):
        for y in (1, 2):
            b.set(x, y, 14, parts.log('stripped_dark_oak_log'))
    for x in range(5, 11):
        b.set(x, 3, 13, 'spruce_slab', type='top')
        b.set(x, 3, 14, 'spruce_stairs', facing='north', half='bottom')
    b.barrel(7, 1, 13, 'up')
    b.set(8, 1, 13, 'flower_pot')
    b.set(8, 1, 14, 'potted_dead_bush')
    b.set(7, 1, 14, 'decorated_pot', facing='north', cracked=True, waterlogged=False)

    # The herb garden, fenced against rabbits.
    fence_ring(b, 0, 6, 3, 14, gates=((3, 10, 'east'),))
    for x in (1, 2):
        for z in range(7, 14):
            b.set(x, 0, z, 'rooted_dirt' if (x + z) % 3 else 'grass_block')
            b.set(x, 1, z, HERBS[(x * 3 + z) % len(HERBS)])
    for z in (8, 11):
        b.set(4, 1, z, 'sweet_berry_bush', age=3)

    # A beehive on a post, the fairy ring, the old oak with its vines.
    b.set(15, 1, 5, 'spruce_fence')
    b.set(15, 2, 5, 'beehive', facing='west', honey_level=5)
    # The fairy ring: a patchy circle of mushrooms in the grass round a holed stone.
    cx, cz = 16, 15
    for x in range(cx - 4, cx + 5):
        for z in range(cz - 4, cz + 5):
            if 2.6 <= math.hypot(x - cx, z - cz) <= 3.4 and rng.random() < .8:
                b.set(x, 1, z, 'red_mushroom' if rng.random() < .45 else 'brown_mushroom')
    b.set(cx, 1, cz, 'mossy_cobblestone')
    parts.oak_tree(b, 2, 1, 18, rng, height=6, radius=3)
    for y in range(2, 5):
        b.set(3, y, 18, 'vine', west=True, north=False, south=False, east=False, up=False)
        b.set(2, y, 19, 'vine', north=True, south=False, east=False, west=False, up=False)
    for (x, y, z) in ((18, 1, 2), (19, 1, 2), (18, 1, 3), (18, 2, 2)):
        b.set(x, y, z, rng.choice(['mossy_cobblestone', 'cobblestone', 'moss_block']))

    b.set(10, 1, 2, 'spruce_fence')
    b.sign(10, 2, 2, ['Remedies', '', 'Knock twice,', 'after dark.'], facing='north', wall=False)
    path(b, [(8, z) for z in range(0, 5)] + [(x, 4) for x in range(4, 8)] + [(4, z) for z in range(5, 11)],
         rng, mats=('dirt_path', 'coarse_dirt', 'moss_block', 'dirt_path'))
    start(b, 10, 10, 'spruce_planks')
    dweller(b, 9, 2, 8, 'herbalist', job='apothecary')
    tufts(b, rng, 0, 0, 20, 20, chance=.16)
    b.natural_ground()
    return b


DESIGNS = {'homesteads/herbalist_cottage': herbalist_cottage}
