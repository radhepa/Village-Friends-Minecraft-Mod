"""The pariah's house: a once-fine house, gone to seed, where someone cast out of their village lives alone.

Built for someone who mattered: a stone ground floor, a jettied timber upper storey, a slate roof,
a walled yard with an ornamental basin. Now the basin is dry and its statue gone, the yard wall
has fallen in places, the slate has holes, a window is broken and another boarded up, and a sign
on the gate tells visitors to turn back. Inside there is one armchair by the fire and a long table
set for six with a single chair.
"""
import random

from ...kit import Build
from ... import parts
from ...parts import Body, Style
from .common import start, dweller, path, gate, tufts

STYLE = Style(frame='stripped_dark_oak_log', fill='calcite', floor='dark_oak_planks', roof='slate',
              base='stone_bricks', trim='dark_oak', door='dark_oak', upper_fill='calcite')


def _overgrow(b, rng, cells):
    """Tall grass, ferns and dead bushes where a garden used to be."""
    for x, z in cells:
        if not b.inside(x, 2, z) or b.get(x, 1, z)[0] != 'minecraft:air':
            continue
        roll = rng.random()
        if roll < .16 and b.get(x, 2, z)[0] == 'minecraft:air':
            kind = rng.choice(['tall_grass', 'large_fern'])
            b.set(x, 1, z, kind, half='lower')
            b.set(x, 2, z, kind, half='upper')
        elif roll < .38:
            b.set(x, 1, z, rng.choice(['short_grass', 'short_grass', 'fern']))
        elif roll < .44:
            b.set(x, 1, z, 'dead_bush')
            b.set(x, 0, z, 'coarse_dirt')


def pariah_house():
    rng = random.Random(6606)
    b = Build('homesteads/pariah_house', (21, 17, 21))

    # The house: stone below, jettied timber above, a slate roof along X.
    body = Body(b, 5, 7, 15, 14, STYLE, heights=(3, 3), jetty=('north',), stone_ground=True).build()
    body.roof(axis='x', pitch=1, gable='calcite')
    # Plaster has fallen away in patches, showing the tuff beneath.
    for (x, y, z), state in list(b.grid.items()):
        if state[0] == 'minecraft:calcite' and rng.random() < .18:
            b.set(x, y, z, 'tuff')
    # Holes in the slate, a few patched with whatever was to hand.
    roof = [(p, s) for p, s in b.grid.items() if s[0] == 'minecraft:deepslate_tile_stairs' and p[1] >= 10]
    rng.shuffle(roof)
    for (x, y, z), state in roof[:4]:
        b.set(x, y, z, 'air')
    for (x, y, z), state in roof[4:9]:
        b.set(x, y, z, ('minecraft:cobblestone_stairs', state[1]))

    # Front: the old stone steps, a dark oak door, a lantern on a chain, windows (one broken, one boarded).
    b.door(10, 2, 7, facing='south', wood='dark_oak')
    for x in (9, 10, 11):
        b.set(x, 1, 6, 'stone_brick_stairs', facing='south', half='bottom')
    parts.lantern(b, 12, 4, 6)
    body.windows(0, 'north', [2, 8], height=2, shutters=True)
    b.set(13, 3, 7, 'air')                      # a broken pane
    b.set(14, 3, 6, 'air')                      # and a shutter gone with it
    body.windows(1, 'north', [2, 5, 8], height=2, shutters=False)
    for y in (7, 8):
        b.set(13, y, 5, 'dark_oak_trapdoor', facing='north', half='bottom', open=True, powered=False, waterlogged=False)
    body.windows(0, 'south', [3, 7], height=2)
    body.windows(1, 'south', [2, 7], height=2, shutters=False)
    body.windows(1, 'east', [3], height=2, shutters=False)
    body.gable_window('east')
    body.gable_window('west')

    # The hearth in the west wall; its chimney stack climbs outside.
    for z in (9, 10, 11):
        for y in range(1, 5):
            b.set(4, y, z, 'stone_bricks')
    for y in range(5, body.ridge + 1):
        b.set(4, y, 10, 'stone_bricks')
    b.set(4, body.ridge + 1, 10, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    b.set(5, 2, 10, 'campfire', lit=True, signal_fire=False, facing='east', waterlogged=False)
    b.set(5, 3, 10, 'chiseled_stone_bricks')
    b.set(5, 4, 10, 'stone_bricks')

    # Ground floor: one good armchair by the fire, a long table set for six with a single chair.
    parts.rug(b, 6, 9, 8, 11, 2, 'red', 'black')
    b.custom(7, 2, 10, 'fireside_armchair', facing='west')
    for x in range(9, 13):
        parts.table(b, x, 2, 12, wood='dark_oak')
    parts.chair(b, 13, 2, 12, 'east', wood='dark_oak')
    b.set(10, 3, 12, 'candle', candles=2, lit=False, waterlogged=False)
    for x in (6, 7):
        for y in (2, 3):
            b.set(x, y, 8, 'bookshelf')
    b.set(6, 2, 13, 'lectern', facing='east', has_book=False, powered=False)
    b.barrel(6, 2, 12, 'up')
    b.set(8, 4, 8, 'cobweb')
    b.set(14, 4, 13, 'cobweb')
    parts.lantern(b, 10, 4, 10)
    b.set(6, 4, 12, 'black_wall_banner', facing='east')
    parts.stair_run(b, 14, 13, 2, 4, 'north', wood='dark_oak')

    # Upstairs: a bedroom behind a partition, the landing with a rail round the stairwell.
    for z in range(7, 14):
        for y in (6, 7, 8):
            b.set(12, y, z, 'dark_oak_planks')
    b.door(12, 6, 8, facing='east', wood='dark_oak')
    b.bed(7, 6, 12, 'north', 'gray')
    b.chest(6, 6, 13, 'north', loot='minecraft:chests/village/village_plains_house')
    b.set(9, 6, 13, 'dark_oak_stairs', facing='south', half='bottom')
    b.set(10, 6, 13, 'dark_oak_slab', type='top')
    b.set(10, 7, 13, 'candle', candles=1, lit=False, waterlogged=False)
    b.set(11, 6, 7, 'barrel', facing='up', open=False)
    b.set(6, 8, 7, 'cobweb')
    b.set(11, 8, 13, 'cobweb')
    parts.lantern(b, 9, 8, 10)
    b.room('bedroom', (9, 7, 10))
    for z in (11, 12):
        b.set(13, 6, z, 'dark_oak_fence')
    b.set(13, 6, 13, 'barrel', facing='up', open=False)
    b.set(14, 8, 7, 'cobweb')

    # The yard wall: low stone, fallen in places, rubble where it fell.
    for x, z, facing, corner in parts.ring(1, 1, 19, 19):
        if (x, z) in ((9, 1), (10, 1), (11, 1)):
            continue
        if rng.random() < .14 and not corner:
            if rng.random() < .6:
                b.set(x, 1, z, rng.choice(['cobblestone_slab', 'mossy_cobblestone_slab']), type='bottom')
            continue
        b.set(x, 1, z, 'mossy_cobblestone_wall' if rng.random() < .45 else 'cobblestone_wall')
    # The gate between two pillars, one lantern still lit, and the sign.
    for x in (9, 11):
        b.set(x, 1, 1, 'stone_bricks')
        b.set(x, 2, 1, 'chiseled_stone_bricks')
    b.set(9, 3, 1, 'lantern', hanging=False, waterlogged=False)
    b.set(11, 3, 1, 'stone_brick_slab', type='bottom')
    gate(b, 10, 1, 1, 'north', wood='dark_oak')
    b.sign(9, 2, 0, ['Turn back.', '', 'No visitors.', 'No pity.'], facing='north', wood='dark_oak')

    # The front walk, cracked and grown over.
    for z in range(2, 6):
        for x in (9, 10, 11):
            b.set(x, 0, z, rng.choice(['stone_bricks', 'cracked_stone_bricks', 'mossy_stone_bricks', 'gravel', 'coarse_dirt']))

    # The ornamental basin: dry, its statue gone, only the pedestal left.
    cx, cz = 5, 4
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            b.set(cx + dx, 0, cz + dz, 'stone_bricks')
            if dx or dz:
                b.set(cx + dx, 1, cz + dz, 'stone_brick_slab', type='bottom')
    b.set(cx, 1, cz, 'chiseled_stone_bricks')
    b.set(cx - 1, 1, cz + 1, 'mossy_stone_brick_slab', type='bottom')
    b.set(cx + 1, 1, cz - 1, 'air')

    # A dead tree in the corner, branches bare.
    tx, tz = 16, 4
    for y in range(1, 7):
        b.set(tx, y, tz, parts.log('dark_oak_log'))
    for (dx, dy, dz) in ((1, 4, 0), (2, 5, 0), (-1, 5, 0), (-2, 6, 0), (0, 5, 1), (0, 6, 2), (0, 4, -1), (1, 7, -1)):
        b.set(tx + dx, dy, tz + dz, 'dark_oak_fence')
    b.set(tx, 7, tz, 'dark_oak_fence')

    # Round the back: firewood against the wall, a stump, a vegetable patch gone to weeds.
    parts.woodpile(b, 6, 1, 15, along_axis='x', length=4, wood='dark_oak', height=2)
    b.set(12, 1, 16, 'oak_log', axis='y')
    for x in range(13, 18):
        for z in range(16, 19):
            roll = rng.random()
            if roll < .2:
                b.set(x, 0, z, 'farmland', moisture=0)
                b.set(x, 1, z, 'potatoes', age=2)
            else:
                b.set(x, 0, z, 'coarse_dirt' if rng.random() < .5 else 'rooted_dirt')
                if roll < .45:
                    b.set(x, 1, z, rng.choice(['dead_bush', 'short_grass']))
    b.set(16, 1, 15, 'cauldron')

    path(b, [(10, z) for z in range(15, 17)] + [(x, 17) for x in range(8, 12)], rng,
         mats=('coarse_dirt', 'gravel', 'dirt_path'))
    b.door(10, 2, 14, facing='north', wood='dark_oak')

    cells = [(x, z) for x in range(2, 19) for z in range(2, 19)]
    _overgrow(b, rng, cells)
    start(b, 10, 10, 'dark_oak_planks')
    dweller(b, 8, 2, 11, 'pariah')
    b.natural_ground()
    return b


DESIGNS = {'homesteads/pariah_house': pariah_house}
