"""The old watchtower: a veteran keeps a watch nobody ordered.

A square stone tower of three storeys on a battered plinth, corbelled out at the top into a
crenellated fighting deck with a brazier and a flagpole. The veteran lives on the ground floor
(bed, chest, table, stove); the floor above holds the old kit, the top room looks out every way,
and stairs climb all the way to the deck. Around it: fallen stretches of the old curtain wall,
rubble, the archery target and hay-bale butts in the yard, a woodpile and a sign at the approach.
"""
import random

from ...kit import Build
from ... import parts
from .common import start, dweller, path, tufts

X0, Z0, X1, Z1 = 6, 6, 12, 12          # the tower's outer walls
FLOORS = (1, 6, 11)                     # floor levels; walls run up to the next floor
DECK = 16


def _stone(rng):
    roll = rng.random()
    return 'mossy_stone_bricks' if roll < .16 else 'cracked_stone_bricks' if roll < .26 else 'stone_bricks'


def watchtower():
    rng = random.Random(1212)
    b = Build('homesteads/watchtower', (19, 24, 19))

    # Plinth, walls and floors.
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            b.set(x, 0, z, 'cobblestone')
    for x, z, facing, corner in parts.ring(X0, Z0, X1, Z1):
        for y in range(1, DECK):
            b.set(x, y, z, 'polished_andesite' if corner and y < 3 else _stone(rng))
    parts.plinth_skirt(b, X0, Z0, X1, Z1, 1, 'stone_brick_stairs')
    for fy in FLOORS:
        b.fill(X0 + 1, fy, Z0 + 1, X1 - 1, fy, Z1 - 1, 'spruce_planks')
    # String courses where the floors are, corbels under the deck.
    for x, z, facing, corner in parts.ring(X0 - 1, Z0 - 1, X1 + 1, Z1 + 1):
        if not corner:
            b.set(x, 15, z, 'stone_brick_stairs', facing={'north': 'south', 'south': 'north', 'west': 'east', 'east': 'west'}[facing], half='top')
            b.set(x, 11, z, 'stone_brick_slab', type='top')
    for x, z in ((X0 - 1, Z0 - 1), (X1 + 1, Z0 - 1), (X0 - 1, Z1 + 1), (X1 + 1, Z1 + 1)):
        b.set(x, 15, z, 'stone_bricks')
        b.set(x, 14, z, 'stone_brick_wall')

    # The fighting deck: wider than the tower, a parapet with crenels, the brazier and the flagpole.
    b.fill(X0 - 1, DECK, Z0 - 1, X1 + 1, DECK, Z1 + 1, 'stone_bricks')
    b.fill(X0, DECK, Z0, X1, DECK, Z1, 'spruce_planks')
    for i, (x, z, facing, corner) in enumerate(parts.ring(X0 - 1, Z0 - 1, X1 + 1, Z1 + 1)):
        b.set(x, DECK + 1, z, _stone(rng))
        if corner or (x + z) % 2 == 0:
            b.set(x, DECK + 2, z, _stone(rng))
    b.set(9, DECK + 1, 9, 'chiseled_stone_bricks')
    b.set(9, DECK + 2, 9, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    for y in range(DECK + 1, DECK + 6):
        b.set(X0, y, Z1, 'spruce_fence')
    b.set(X0, DECK + 6, Z1, 'yellow_banner', rotation=8)
    b.set(X1 - 1, DECK + 1, Z1 - 1, 'barrel', facing='up', open=False)
    b.set(X0 + 1, DECK + 1, Z0 + 1, 'spruce_stairs', facing='west', half='bottom')

    # The ground floor: the veteran's quarters.
    b.door(9, 2, Z0, facing='south', wood='spruce')
    b.set(9, 4, Z0, 'iron_bars')
    b.set(9, 1, Z0 - 1, 'stone_brick_stairs', facing='south', half='bottom')
    b.set(10, 3, Z0 - 1, 'wall_torch', facing='north')
    b.bed(7, 2, 11, 'north', 'red')
    b.chest(8, 2, 11, 'north', loot='minecraft:chests/village/village_fletcher')
    b.set(7, 2, 7, 'furnace', facing='east', lit=True)
    b.barrel(8, 2, 7, 'up')
    parts.table(b, 9, 2, 10)
    parts.chair(b, 9, 2, 9, 'north')
    b.set(10, 2, 11, 'potted_fern')
    parts.lantern(b, 8, 5, 9)
    parts.stair_run(b, 11, 11, 2, 5, 'north')
    for z in (8, 9):
        b.set(10, 7, z, 'spruce_fence')

    # The middle floor: the old kit.
    parts.stair_run(b, 7, 7, 7, 5, 'south')
    for z in (9, 10):
        b.set(8, 12, z, 'spruce_fence')
    b.set(10, 7, 11, 'barrel', facing='up', open=False)
    b.set(11, 7, 11, 'barrel', facing='north', open=False)
    b.set(9, 7, 11, 'hay_block', axis='y')
    b.chest(11, 7, 10, 'west')
    b.set(9, 10, 9, 'lantern', hanging=True, waterlogged=False)

    # The top room: windows every way, a bench to sit the watch.
    parts.stair_run(b, 11, 11, 12, 5, 'north')
    for z in (8, 9):
        b.set(10, DECK + 1, z, 'spruce_fence')
    parts.bench(b, 10, 12, 11, 'south', length=2)
    b.set(9, 15, 9, 'lantern', hanging=True, waterlogged=False)

    # Windows and arrow slits.
    for y0 in (3, 8):
        for (x, z) in ((X0, 9), (X1, 9), (9, Z1)):
            for y in (y0, y0 + 1):
                b.set(x, y, z, 'glass_pane')
    for y in (8, 9):
        b.set(9, y, Z0, 'glass_pane')
    for (x, z) in ((X0, 8), (X0, 10), (X1, 8), (X1, 10), (8, Z0), (10, Z0), (8, Z1), (10, Z1)):
        for y in (13, 14):
            b.set(x, y, z, 'glass_pane')
    b.set(10, 10, Z0 - 1, 'yellow_wall_banner', facing='north')

    # The yard: what's left of the curtain wall, rubble, the target and the butts.
    wall = [(x, 1) for x in range(1, 8)] + [(1, z) for z in range(1, 9)] + [(17, z) for z in range(10, 18)] \
        + [(x, 17) for x in range(11, 18)] + [(x, 1) for x in range(13, 16)]
    for x, z in wall:
        height = rng.choice([1, 1, 2, 2, 3])
        for y in range(1, height + 1):
            b.set(x, y, z, _stone(rng))
    for (x, y, z) in ((2, 1, 11), (3, 1, 12), (2, 1, 12), (9, 1, 1), (10, 1, 2), (16, 1, 8), (15, 1, 17), (16, 1, 16)):
        b.set(x, y, z, rng.choice(['cobblestone', 'mossy_cobblestone', 'stone_brick_slab', 'andesite']))
    b.set(3, 1, 15, 'mossy_stone_bricks')
    b.set(3, 2, 15, 'mossy_stone_brick_slab', type='bottom')
    b.custom(15, 1, 5, 'archery_target', facing='west')
    for z in (3, 4):
        b.set(15, 1, z, 'hay_block', axis='y')
    b.set(15, 2, 4, 'hay_block', axis='x')
    parts.woodpile(b, 3, 1, 5, along_axis='z', length=3, wood='spruce', height=2)
    b.set(4, 1, 9, 'cauldron')
    b.set(12, 1, 2, 'spruce_fence')
    b.sign(12, 2, 2, ['Halt.', '', 'State your', 'business.'], facing='north', wall=False)
    path(b, [(9, z) for z in range(0, 5)] + [(x, 4) for x in range(10, 15)], rng,
         mats=('gravel', 'dirt_path', 'coarse_dirt', 'cobblestone'))
    start(b, 9, 9, 'spruce_planks')
    dweller(b, 9, 2, 8, 'veteran', job='archer')
    tufts(b, rng, 0, 0, 18, 18, chance=.12)
    b.natural_ground()
    return b


DESIGNS = {'homesteads/watchtower': watchtower}
