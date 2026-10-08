"""Taiga homes: log huts, an A-frame, porch and dogtrot cabins, a two-storey lodge,
an L-plan cabin, a stone cottage and a stone-based longhouse.

Every home is a drop-in lot: north-facing ``building_entrance`` at [x,1,0], a
path to a real front door, at least one enclosed bedroom with paired beds, a
stone hearth, a loot chest and unemployed residents. Walls are true log
construction (``homes_logs.log_walls``) on mossy rubble foundations.
"""
import random

from ...kit import Build
from ... import parts
from ...parts import log
from . import homes_logs as H


def plaque(b, x, z, y=2, facing='north'):
    """The House Plaque on the front wall beside the door, at eye height: it names the house and who lives there."""
    b.custom(x, y, z, 'house_plaque', facing=facing)


def trapper_hut():
    """A one-room trapper's hut with a back sleeping room, hide racks and a woodpile."""
    rng = random.Random(4101)
    b = Build('taiga/trapper_hut', (11, 14, 13))
    H.rubble(b, 2, 3, 8, 10, rng)
    H.log_walls(b, 2, 3, 8, 10, 2, 4)
    H.partition_z(b, 7, 3, 7, 2, 4)
    H.ceiling(b, 3, 4, 7, 9, 5)
    ridge = H.roof(b, 2, 3, 8, 10, 4, 'dark_oak', axis='z', pitch=1, gable=log('stripped_spruce_log', 'x'), trim='spruce')
    H.door(b, 5, 2, 3, 'north')
    H.window(b, 3, 3, 3, 'north')
    H.window(b, 7, 3, 3, 'north')
    H.window(b, 8, 3, 8, 'east')
    H.window(b, 5, 3, 10, 'south', shutters=False)
    b.set(5, 7, 3, 'glass_pane')
    H.hearth(b, 2, 5, 2, 'east', rng, top=ridge + 1)
    # Front room: fire, a table by it and the trapper's stores.
    H.table(b, 6, 2, 5)
    H.chair(b, 7, 2, 5, 'east')
    b.set(7, 2, 4, 'crafting_table')
    b.barrel(7, 2, 6, 'up')
    b.set(3, 2, 6, 'brown_carpet')
    b.set(4, 2, 6, 'brown_carpet')
    H.wall_hide(b, 4, 3, 6, 'north')
    b.custom(3, 2, 4, 'fireside_armchair', facing='west')
    b.set(6, 4, 4, 'lantern', hanging=True, waterlogged=False)
    # Back room behind a plank partition.
    b.door(5, 2, 7, facing='south', wood='spruce')
    b.bed(3, 2, 8, 'south', 'brown')
    H.loot_chest(b, 7, 2, 9, 'west')
    b.barrel(7, 2, 8, 'up')
    b.set(4, 2, 9, 'white_carpet')
    H.bedroom_lamp(b, 5, 4, 9)
    b.room('bedroom', (5, 3, 8))
    plaque(b, 6, 2)
    H.moss_roof(b, rng, .14)
    # Yard: hide racks, woodpile, chopping block.
    H.path(b, 5, 0, 2, rng)
    b.entrance(5)
    H.drying_rack(b, 10, 4, 1, length=3, axis='z', hides=('brown', 'white', 'brown'))
    H.woodpile(b, 0, 1, 7, 'z', length=3)
    H.chopping_block(b, 1, 1, 1, rng)
    H.lantern_post(b, 8, 1, 1, height=2)
    H.undergrowth(b, [(x, z) for x in range(11) for z in list(range(0, 3)) + [11, 12]], rng, .3)
    b.resident(4, 2, 5)
    b.natural_ground()
    return b


def aframe_cabin():
    """A steep A-frame whose roof runs to the ground; log gable with a tall window and a deck."""
    rng = random.Random(4102)
    b = Build('taiga/aframe_cabin', (13, 14, 19))
    H.rubble(b, 2, 4, 10, 16, rng)
    H.roof(b, 2, 4, 10, 16, 1, 'dark_oak', axis='z', pitch=2, rake=(2, 1),
           gable=log('stripped_spruce_log', 'x'), trim='spruce')
    # Bedroom partition right up to the roof.
    H.seal_up(b, [(x, 10) for x in range(3, 10)], 2)
    b.door(6, 2, 10, facing='south', wood='spruce')
    # Front gable: door, side windows and a tall window up to the apex.
    H.door(b, 6, 2, 4, 'north', step=None)
    H.window(b, 4, 3, 4, 'north', shutters=False)
    H.window(b, 8, 3, 4, 'north', shutters=False)
    for x in (5, 6, 7):
        b.set(x, 6, 4, 'glass_pane')
        b.set(x, 7, 4, 'glass_pane')
    b.set(6, 8, 4, 'glass_pane')
    for x, y in ((6, 5), (6, 9)):
        b.set(x, y, 4, log('stripped_spruce_log', 'x'))
    b.set(6, 6, 16, 'glass_pane')
    b.set(6, 7, 16, 'glass_pane')
    # Deck and steps under the deep front overhang.
    for x in range(3, 10):
        for z in (2, 3):
            b.set(x, 1, z, 'spruce_planks')
    for x in (3, 4, 8, 9):
        b.set(x, 2, 2, 'spruce_fence')
    b.set(5, 2, 2, 'spruce_fence')
    b.set(7, 2, 2, 'spruce_fence')
    b.set(3, 3, 2, 'lantern', waterlogged=False)
    b.set(9, 3, 2, 'lantern', waterlogged=False)
    b.set(6, 1, 1, 'spruce_stairs', facing='south', half='bottom', lock=True)
    b.custom(4, 2, 3, 'village_bench', facing='north')
    # Living room: stone stove with a flue through the roof.
    b.set(8, 2, 7, 'campfire', lit=True, signal_fire=False, facing='west', waterlogged=False)
    for x, z in ((9, 7), (8, 6), (8, 8)):
        b.set(x, 2, z, 'mossy_cobblestone' if (x + z) % 2 else 'cobblestone')
    b.set(9, 3, 7, 'cobblestone')
    H.chimney(b, 8, 7, 3, 8, rng)
    H.table(b, 4, 2, 7)
    H.chair(b, 4, 2, 6, 'north')
    H.chair(b, 4, 2, 8, 'south')
    b.set(3, 2, 5, 'crafting_table')
    b.barrel(3, 2, 9, 'up')
    b.set(3, 2, 8, 'furnace', facing='east', lit=False)
    H.rug(b, 5, 6, 7, 8, 2, 'green', 'brown')
    parts.lantern(b, 6, 9, 7)
    b.set(4, 3, 7, 'lantern', hanging=False, waterlogged=False)
    b.custom(7, 2, 6, 'fireside_armchair', facing='east')
    # Bedroom at the back.
    b.bed(4, 2, 14, 'south', 'green')
    b.bed(8, 2, 14, 'south', 'brown')
    H.loot_chest(b, 6, 2, 15, 'north')
    b.barrel(3, 2, 11, 'up')
    H.pot(b, 9, 2, 11, rng)
    H.rug(b, 5, 12, 7, 13, 2, 'white', 'white')
    parts.lantern(b, 6, 9, 13)
    b.set(3, 2, 15, 'lantern', hanging=False, waterlogged=False)
    b.room('bedroom', (6, 3, 12))
    plaque(b, 7, 3)
    H.moss_roof(b, rng, .1, kinds=('dark_oak',), y_min=1)
    H.path(b, 6, 0, 0, rng)
    b.set(6, 0, 1, 'dirt_path')
    b.entrance(6)
    H.woodpile(b, 12, 1, 7, 'z', length=4)
    H.undergrowth(b, [(x, z) for x in range(13) for z in (0, 1, 17, 18)] + [(0, z) for z in range(19)], rng, .3)
    b.resident(7, 2, 8)
    b.resident(5, 2, 12)
    b.natural_ground()
    return b


def porch_cabin():
    """Log cabin with a full-width porch under a catslide roof."""
    rng = random.Random(4103)
    b = Build('taiga/porch_cabin', (15, 15, 16))
    H.rubble(b, 2, 6, 12, 12, rng)
    H.log_walls(b, 2, 6, 12, 12, 2, 6, chink='stripped_spruce_log')
    H.partition_x(b, 8, 7, 11, 2, 4)
    H.ceiling(b, 3, 7, 11, 11, 5)
    ridge = H.roof(b, 2, 6, 12, 12, 6, 'dark_oak', axis='x', pitch=1, gable=log('spruce_log', 'z'), trim='spruce')
    # Porch: plank deck, log posts, fence rail and a catslide roof.
    for x in range(2, 13):
        for z in (3, 4, 5):
            b.set(x, 1, z, 'spruce_planks')
    for x in range(1, 14):
        b.set(x, 5, 4, 'dark_oak_stairs', facing='south', half='bottom')
        b.set(x, 4, 3, 'dark_oak_stairs', facing='south', half='bottom')
    for x in (2, 5, 9, 12):
        b.set(x, 2, 3, 'spruce_log', axis='y')
        b.set(x, 3, 3, 'spruce_log', axis='y')
    for x in (3, 4, 6, 8, 10, 11):
        b.set(x, 2, 3, 'spruce_fence')
    for z in (4, 5):
        b.set(2, 2, z, 'spruce_fence')
        b.set(12, 2, z, 'spruce_fence')
    b.set(7, 1, 2, 'spruce_stairs', facing='south', half='bottom', lock=True)
    H.door(b, 7, 2, 6, 'north', step=None)
    b.custom(4, 2, 5, 'village_bench', facing='south')
    b.barrel(11, 2, 5, 'up')
    b.set(10, 2, 5, 'hay_block', axis='y')
    b.set(4, 4, 4, 'lantern', hanging=True, waterlogged=False)
    b.set(10, 4, 4, 'lantern', hanging=True, waterlogged=False)
    H.window(b, 3, 3, 6, 'north', height=2, width=2, shutters=False)
    H.window(b, 10, 3, 6, 'north', height=2, width=1, shutters=False)
    H.window(b, 12, 3, 9, 'east')
    H.window(b, 4, 3, 12, 'south')
    H.window(b, 10, 3, 12, 'south')
    b.set(12, 8, 9, 'glass_pane')
    b.set(2, 8, 10, 'glass_pane')
    H.hearth(b, 2, 9, 2, 'east', rng, top=ridge + 1)
    # Living room.
    H.rug(b, 4, 8, 6, 10, 2, 'brown', 'green')
    H.table(b, 5, 2, 9)
    H.chair(b, 5, 2, 8, 'north')
    H.chair(b, 5, 2, 10, 'south')
    b.set(3, 2, 11, 'smoker', facing='east', lit=False)
    b.set(4, 2, 11, 'crafting_table')
    b.barrel(6, 2, 11, 'up')
    H.loot_chest(b, 3, 2, 7, 'east')
    H.pot(b, 7, 2, 11, rng)
    b.set(5, 4, 9, 'lantern', hanging=True, waterlogged=False)
    b.custom(3, 2, 10, 'fireside_armchair', facing='west')
    H.wall_hide(b, 6, 3, 7, 'south')
    # Bedroom behind the partition.
    b.door(8, 2, 9, facing='east', wood='spruce')
    b.bed(11, 2, 8, 'north', 'green')
    b.bed(11, 2, 10, 'south', 'cyan')
    b.barrel(9, 2, 7, 'up')
    b.set(9, 2, 11, 'lantern', hanging=False, waterlogged=False)
    b.set(10, 2, 9, 'green_carpet')
    H.bedroom_lamp(b, 10, 4, 9)
    b.room('bedroom', (10, 3, 9))
    plaque(b, 8, 5)
    H.moss_roof(b, rng, .12)
    # Yard.
    H.path(b, 7, 0, 1, rng)
    b.entrance(7)
    H.woodpile(b, 3, 1, 14, 'x', length=4)
    H.chopping_block(b, 9, 1, 14, rng)
    H.undergrowth(b, [(x, z) for x in range(15) for z in (0, 1, 2, 15)] + [(0, z) for z in range(16)]
                  + [(14, z) for z in range(16)], rng, .3)
    b.resident(6, 2, 8)
    b.resident(9, 2, 10, child=True)
    b.natural_ground()
    return b


def log_lodge():
    """Two-storey log lodge: gable to the street, balcony over the door, bedrooms upstairs."""
    rng = random.Random(4104)
    b = Build('taiga/log_lodge', (15, 18, 17))
    H.rubble(b, 2, 4, 12, 12, rng)
    H.log_walls(b, 2, 4, 12, 12, 2, 9)
    H.ceiling(b, 3, 5, 11, 11, 6)
    H.ceiling(b, 3, 5, 11, 11, 10)
    parts.stair_run(b, 11, 11, 2, 5, 'north', wood='spruce')
    # Upstairs: corridor along the stairs, two bedrooms.
    H.partition_x(b, 9, 5, 11, 7, 9)
    H.partition_z(b, 8, 3, 8, 7, 9)
    ridge = H.roof(b, 2, 4, 12, 12, 9, 'dark_oak', axis='z', pitch=1, rake=(2, 1),
                   gable=log('spruce_log', 'x'), trim='spruce')
    # Balcony on log posts.
    for x in range(2, 13):
        for z in (2, 3):
            b.set(x, 6, z, 'spruce_planks')
        b.set(x, 7, 2, 'spruce_fence')
    for z in (2, 3):
        b.set(2, 7, z, 'spruce_fence')
        b.set(12, 7, z, 'spruce_fence')
    for x in (2, 12):
        for y in range(1, 6):
            b.set(x, y, 2, 'spruce_log', axis='y')
        b.set(x, 0, 2, 'mossy_cobblestone')
    for x in range(3, 12):
        b.set(x, 5, 2, 'spruce_stairs', facing='north', half='top', lock=True)
    b.door(10, 7, 4, facing='north', wood='spruce')
    H.window(b, 5, 7, 4, 'north', height=2, width=2, shutters=False)
    b.set(7, 11, 4, 'glass_pane')
    b.set(7, 12, 4, 'glass_pane')
    H.door(b, 7, 2, 4, 'north')
    H.window(b, 4, 3, 4, 'north', height=2, width=2, shutters=False)
    H.window(b, 9, 3, 4, 'north', height=2, width=1, shutters=False)
    H.window(b, 2, 3, 11, 'west', height=2)
    H.window(b, 12, 3, 5, 'east', height=2)
    H.window(b, 4, 7, 12, 'south', height=2, width=2)
    H.window(b, 2, 7, 6, 'west')
    H.window(b, 2, 7, 10, 'west')
    H.window(b, 12, 8, 9, 'east')
    H.hearth(b, 2, 8, 2, 'east', rng, top=ridge - 1)
    # Ground floor hall.
    H.rug(b, 5, 6, 7, 10, 2, 'brown', 'green')
    H.table(b, 6, 2, 8)
    H.chair(b, 5, 2, 8, 'west')
    H.chair(b, 7, 2, 8, 'east')
    H.chair(b, 6, 2, 9, 'south')
    b.set(3, 2, 11, 'smoker', facing='north', lit=False)
    b.barrel(4, 2, 11, 'up')
    b.set(5, 2, 11, 'crafting_table')
    b.set(6, 2, 11, 'furnace', facing='north', lit=False)
    b.set(3, 2, 5, 'bookshelf')
    b.set(4, 2, 5, 'bookshelf')
    H.pot(b, 3, 3, 5, rng)
    b.set(6, 5, 8, 'lantern', hanging=True, waterlogged=False)
    b.custom(3, 2, 7, 'fireside_armchair', facing='west')
    b.custom(3, 2, 9, 'fireside_armchair', facing='west')
    b.set(9, 5, 10, 'lantern', hanging=True, waterlogged=False)
    H.wall_hide(b, 3, 4, 10, 'east')
    # Bedroom north (front, window to the balcony side).
    b.door(9, 7, 6, facing='east', wood='spruce')
    b.bed(4, 7, 5, 'west', 'green')
    b.bed(4, 7, 7, 'west', 'green')
    H.loot_chest(b, 7, 7, 7, 'north')
    H.bedroom_lamp(b, 6, 9, 6)
    b.room('bedroom_north', (7, 8, 6))
    # Bedroom south (the child's).
    b.door(9, 7, 10, facing='east', wood='spruce')
    b.bed(4, 7, 10, 'west', 'brown')
    b.barrel(8, 7, 11, 'up')
    b.set(3, 7, 9, 'white_carpet')
    H.bedroom_lamp(b, 6, 9, 10)
    b.room('bedroom_south', (7, 8, 10))
    plaque(b, 8, 3)
    H.bedroom_lamp(b, 10, 9, 6)
    H.moss_roof(b, rng, .1)
    # Yard.
    H.path(b, 7, 0, 3, rng)
    b.set(7, 1, 3, 'spruce_stairs', facing='south', half='bottom', lock=True)
    b.entrance(7)
    H.woodpile(b, 0, 1, 6, 'z', length=4)
    H.chopping_block(b, 13, 1, 14, rng)
    H.drying_rack(b, 3, 15, 1, length=3, hides=('brown', 'brown', 'white'))
    H.undergrowth(b, [(x, z) for x in range(15) for z in (0, 1, 14, 15, 16)] + [(14, z) for z in range(17)],
                  rng, .3)
    b.resident(4, 2, 8)
    b.resident(8, 2, 6)
    b.resident(9, 2, 9, child=True)
    b.natural_ground()
    return b


def longhouse():
    """A long stone-based hall: rubble lower walls, dark logs above, a fire pit and a back sleeping room."""
    rng = random.Random(4105)
    b = Build('taiga/longhouse', (13, 17, 27))
    H.rubble(b, 2, 4, 10, 23, rng)
    stones = ['mossy_stone_bricks', 'stone_bricks', 'mossy_cobblestone', 'cobblestone', 'cracked_stone_bricks',
              'mossy_stone_bricks']
    for x, z, facing, corner in parts.ring(2, 4, 10, 23):
        for y in (2, 3):
            b.set(x, y, z, 'stone_bricks' if corner else rng.choice(stones))
    H.log_walls(b, 2, 4, 10, 23, 4, 5, wood='dark_oak_log')
    H.stone_skirt(b, 2, 4, 10, 23, 1, rng, .3, skip={(6, 3)})
    # Sleeping room at the back with a storage loft above it.
    H.partition_z(b, 18, 3, 9, 2, 4)
    H.ceiling(b, 3, 19, 9, 22, 5)
    H.roof(b, 2, 4, 10, 23, 5, 'spruce', axis='z', pitch=2, gable=log('dark_oak_log', 'x'), trim='dark_oak')
    for z in (3, 24):
        b.set(6, 16, z, 'dark_oak_fence')
    H.door(b, 6, 2, 4, 'north', step='mossy_cobblestone_stairs')
    H.window(b, 4, 3, 4, 'north')
    H.window(b, 8, 3, 4, 'north')
    for y in (7, 8, 9):
        b.set(6, y, 4, 'glass_pane')
    b.set(6, 7, 23, 'glass_pane')
    b.set(6, 8, 23, 'glass_pane')
    for z in (7, 12, 16, 21):
        H.window(b, 2, 3, z, 'west')
        H.window(b, 10, 3, z, 'east')
    # Fire pit with a smoke hood rising through the ridge.
    for x in (5, 6, 7):
        for z in (10, 11, 12):
            b.set(x, 1, z, rng.choice(['stone_bricks', 'mossy_stone_bricks', 'cobblestone']))
    b.set(6, 2, 11, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    for x, z in ((5, 10), (6, 10), (7, 10), (5, 11), (7, 11), (5, 12), (6, 12), (7, 12)):
        b.set(x, 2, z, 'mossy_cobblestone_slab', type='bottom', waterlogged=False)
    b.set(6, 9, 11, 'cobblestone_wall')
    b.custom(4, 2, 11, 'campfire_bench', facing='east')
    b.custom(8, 2, 11, 'campfire_bench', facing='west')
    H.chimney(b, 6, 11, 10, 15, rng)
    # Long table with benches, kitchen along the east wall.
    for z in range(6, 10):
        H.table(b, 4, 2, z, wood='dark_oak')
        H.chair(b, 3, 2, z, 'west', wood='spruce')
    b.set(4, 3, 7, 'lantern', hanging=False, waterlogged=False)
    b.set(9, 2, 14, 'smoker', facing='west', lit=False)
    b.set(9, 2, 15, 'crafting_table')
    b.barrel(9, 2, 16, 'up')
    b.barrel(9, 2, 17, 'west')
    b.set(9, 2, 13, 'furnace', facing='west', lit=False)
    b.set(3, 2, 17, 'bookshelf')
    b.set(3, 2, 16, 'chiseled_bookshelf', facing='east')
    for z in (8, 15):
        for y in (4, 5, 6):
            b.set(6, y + 3, z, 'iron_chain', axis='y', waterlogged=False)
        b.set(6, 6, z, 'lantern', hanging=True, waterlogged=False)
    H.wall_hide(b, 3, 4, 13, 'east')
    H.wall_hide(b, 9, 4, 9, 'west', 'green')
    # Loft over the sleeping room.
    for x in (3, 4, 8, 9):
        b.set(x, 6, 19, 'spruce_fence')
    b.set(5, 6, 21, 'hay_block', axis='x')
    b.barrel(8, 6, 21, 'up')
    b.barrel(4, 6, 22, 'up')
    # Sleeping room.
    b.door(6, 2, 18, facing='south', wood='spruce')
    b.bed(3, 2, 21, 'south', 'brown')
    b.bed(9, 2, 21, 'south', 'brown')
    b.bed(8, 2, 19, 'east', 'white')
    H.loot_chest(b, 6, 2, 22, 'north')
    H.rug(b, 4, 20, 8, 21, 2, 'brown', 'green')
    H.bedroom_lamp(b, 6, 4, 20)
    b.room('bedroom', (6, 3, 20))
    plaque(b, 7, 3)
    H.moss_roof(b, rng, .1, kinds=('spruce', 'dark_oak'))
    H.path(b, 6, 0, 2, rng)
    b.entrance(6)
    H.woodpile(b, 12, 1, 9, 'z', length=4)
    H.woodpile(b, 0, 1, 14, 'z', length=3)
    H.drying_rack(b, 3, 25, 1, length=3, hides=('brown', 'white', 'brown'))
    H.undergrowth(b, [(x, z) for x in range(13) for z in (0, 1, 2, 25, 26)] + [(x, z) for x in (0, 12)
                                                                              for z in range(27)], rng, .3)
    b.resident(5, 2, 8)
    b.resident(8, 2, 13)
    b.resident(7, 2, 15, child=True)
    b.natural_ground()
    return b


def dogtrot_cabin():
    """Two log pens under one roof with an open breezeway between them."""
    rng = random.Random(4106)
    b = Build('taiga/dogtrot_cabin', (17, 13, 14))
    H.rubble(b, 1, 4, 15, 10, rng)
    H.log_walls(b, 1, 4, 6, 10, 2, 4)
    H.log_walls(b, 10, 4, 15, 10, 2, 4)
    H.ceiling(b, 2, 5, 5, 9, 5)
    H.ceiling(b, 11, 5, 14, 9, 5)
    for x in (6, 10):
        b.set(x, 5, 4, log('spruce_log', 'x'))
        b.set(x, 5, 10, log('spruce_log', 'x'))
    ridge = H.roof(b, 1, 4, 15, 10, 4, 'dark_oak', axis='x', pitch=1, gable=log('spruce_log', 'z'), trim='spruce')
    b.set(7, 1, 3, 'spruce_stairs', facing='south', half='bottom', lock=True)
    b.set(8, 1, 3, 'spruce_stairs', facing='south', half='bottom', lock=True)
    b.set(9, 1, 3, 'spruce_stairs', facing='south', half='bottom', lock=True)
    # Living pen (west).
    b.door(6, 2, 7, facing='east', wood='spruce')
    H.hearth(b, 1, 7, 2, 'east', rng, top=ridge + 1)
    H.window(b, 3, 3, 4, 'north', width=2)
    H.window(b, 3, 3, 10, 'south', width=2)
    H.table(b, 4, 2, 6)
    H.chair(b, 4, 2, 5, 'north')
    H.chair(b, 3, 2, 6, 'west')
    b.set(2, 2, 9, 'smoker', facing='east', lit=False)
    b.set(3, 2, 9, 'crafting_table')
    b.barrel(5, 2, 9, 'up')
    b.set(5, 2, 5, 'lantern', hanging=False, waterlogged=False)
    H.loot_chest(b, 2, 2, 5, 'east')
    b.set(4, 4, 7, 'lantern', hanging=True, waterlogged=False)
    b.custom(2, 2, 8, 'fireside_armchair', facing='west')
    # Sleeping pen (east).
    b.door(10, 2, 7, facing='west', wood='spruce')
    H.window(b, 12, 3, 4, 'north', width=2)
    H.window(b, 12, 3, 10, 'south', width=2)
    H.window(b, 15, 3, 7, 'east')
    b.bed(13, 2, 5, 'east', 'brown')
    b.bed(13, 2, 9, 'east', 'green')
    b.barrel(14, 2, 7, 'up')
    b.set(11, 2, 9, 'lantern', hanging=False, waterlogged=False)
    H.rug(b, 12, 6, 13, 8, 2, 'brown', 'brown')
    H.bedroom_lamp(b, 12, 4, 7)
    b.room('bedroom', (12, 3, 7))
    plaque(b, 5, 3)
    # Breezeway: bench, saddle-bag barrels, hides and a chained lantern.
    b.custom(8, 2, 9, 'village_bench', facing='south')
    b.barrel(7, 2, 9, 'up')
    b.set(9, 2, 9, 'hay_block', axis='y')
    H.wall_hide(b, 7, 3, 5, 'east')
    H.wall_hide(b, 9, 3, 5, 'west', 'white')
    for y in (5, 6, 7):
        b.set(8, y, 7, 'iron_chain', axis='y', waterlogged=False)
    b.set(8, 4, 7, 'lantern', hanging=True, waterlogged=False)
    H.moss_roof(b, rng, .12)
    H.path(b, 8, 0, 2, rng)
    b.entrance(8)
    H.woodpile(b, 11, 1, 12, 'x', length=4)
    H.chopping_block(b, 3, 1, 12, rng)
    H.undergrowth(b, [(x, z) for x in range(17) for z in (0, 1, 2, 12, 13)], rng, .3)
    b.resident(4, 2, 8)
    b.resident(8, 2, 6)
    b.natural_ground()
    return b


def stone_cottage():
    """Rubble-stone cottage with dark log corners and a spruce roof."""
    rng = random.Random(4107)
    b = Build('taiga/stone_cottage', (13, 15, 13))
    H.rubble(b, 2, 4, 10, 10, rng, mix=['mossy_stone_bricks', 'stone_bricks', 'mossy_cobblestone',
                                         'cracked_stone_bricks'])
    for x, z, facing, corner in parts.ring(2, 4, 10, 10):
        for y in (2, 3, 4):
            b.set(x, y, z, log('stripped_dark_oak_log') if corner else
                  rng.choice(['cobblestone', 'cobblestone', 'mossy_cobblestone', 'cobblestone', 'tuff']))
    parts.beam_ring(b, 2, 4, 10, 10, 5, 'stripped_spruce_log')
    H.partition_x(b, 7, 5, 9, 2, 4)
    H.ceiling(b, 3, 5, 9, 9, 5)
    ridge = H.roof(b, 2, 4, 10, 10, 5, 'spruce', axis='x', pitch=2, gable=log('stripped_spruce_log', 'z'),
                   trim='dark_oak')
    H.door(b, 5, 2, 4, 'north', step='mossy_cobblestone_stairs')
    H.window(b, 3, 3, 4, 'north', box='spruce_leaves')
    H.window(b, 8, 3, 4, 'north', box='spruce_leaves')
    H.window(b, 10, 3, 7, 'east')
    H.window(b, 4, 3, 10, 'south')
    H.window(b, 8, 3, 10, 'south')
    b.set(10, 7, 7, 'glass_pane')
    H.hearth(b, 2, 7, 2, 'east', rng, top=ridge)
    # Living room.
    H.table(b, 4, 2, 9)
    H.chair(b, 5, 2, 9, 'east')
    H.chair(b, 4, 2, 8, 'north')
    b.set(3, 2, 5, 'smoker', facing='east', lit=False)
    b.set(4, 2, 5, 'crafting_table')
    b.barrel(6, 2, 9, 'up')
    b.set(3, 2, 9, 'lantern', hanging=False, waterlogged=False)
    b.set(4, 4, 7, 'lantern', hanging=True, waterlogged=False)
    b.custom(3, 2, 6, 'fireside_armchair', facing='west')
    # Bedroom.
    b.door(7, 2, 7, facing='east', wood='spruce')
    b.bed(9, 2, 6, 'north', 'brown')
    b.bed(9, 2, 8, 'south', 'white')
    H.loot_chest(b, 8, 2, 5, 'south')
    b.set(8, 2, 9, 'lantern', hanging=False, waterlogged=False)
    H.bedroom_lamp(b, 8, 4, 7)
    b.room('bedroom', (8, 3, 8))
    plaque(b, 6, 3)
    H.moss_roof(b, rng, .12, kinds=('spruce', 'dark_oak'))
    # Front garden behind a low mossy wall.
    H.path(b, 5, 0, 3, rng)
    b.entrance(5)
    for x in list(range(1, 5)) + list(range(6, 12)):
        b.set(x, 1, 1, 'mossy_cobblestone_wall' if x % 3 else 'cobblestone_wall')
    for z in (2, 3):
        b.set(1, 1, z, 'mossy_cobblestone_wall')
        b.set(11, 1, z, 'mossy_cobblestone_wall')
    for x in (2, 3, 7, 8, 9):
        H.berry_bush(b, x, 2, rng)
    b.set(11, 2, 1, 'lantern', waterlogged=False)
    H.woodpile(b, 11, 1, 7, 'z', length=3)
    H.undergrowth(b, [(x, z) for x in range(13) for z in (11, 12)] + [(0, z) for z in range(13)], rng, .35)
    b.resident(5, 2, 7)
    b.resident(8, 2, 7, child=True)
    b.natural_ground()
    return b


def cabin_ell():
    """L-plan log cabin: hall and kitchen at the front, sleeping wing behind."""
    rng = random.Random(4108)
    b = Build('taiga/cabin_ell', (16, 15, 18))
    H.rubble(b, 7, 9, 12, 15, rng)
    H.rubble(b, 2, 4, 12, 9, rng)
    H.log_walls(b, 7, 9, 12, 15, 2, 4)
    H.log_walls(b, 2, 4, 12, 9, 2, 4, chink='stripped_spruce_log')
    b.clear(3, 2, 5, 11, 4, 8)
    b.clear(8, 2, 10, 11, 4, 14)
    H.ceiling(b, 3, 5, 11, 8, 5)
    H.ceiling(b, 8, 10, 11, 14, 5)
    H.roof(b, 7, 9, 12, 15, 4, 'dark_oak', axis='z', pitch=1, rake=(0, 1), gable=log('spruce_log', 'x'),
           trim='spruce')
    ridge = H.roof(b, 2, 4, 12, 9, 4, 'dark_oak', axis='x', pitch=1, gable=log('spruce_log', 'z'), trim='spruce')
    H.door(b, 5, 2, 4, 'north')
    H.window(b, 3, 3, 4, 'north')
    H.window(b, 8, 3, 4, 'north', width=2)
    H.window(b, 11, 3, 4, 'north')
    H.window(b, 4, 3, 9, 'south', width=2)
    H.window(b, 12, 3, 12, 'east')
    H.window(b, 9, 3, 15, 'south', width=2)
    H.window(b, 7, 3, 12, 'west')
    b.set(12, 6, 6, 'glass_pane')
    b.set(12, 6, 7, 'glass_pane')
    H.hearth(b, 2, 6, 2, 'east', rng, top=ridge + 1)
    # Hall and kitchen.
    H.table(b, 6, 2, 7)
    H.chair(b, 6, 2, 8, 'south')
    H.chair(b, 7, 2, 7, 'east')
    b.set(11, 2, 5, 'smoker', facing='west', lit=False)
    b.set(11, 2, 6, 'crafting_table')
    b.barrel(11, 2, 7, 'up')
    b.set(11, 2, 8, 'furnace', facing='west', lit=False)
    b.set(3, 2, 8, 'bookshelf')
    H.loot_chest(b, 4, 2, 8, 'north')
    H.rug(b, 6, 5, 8, 6, 2, 'green', 'brown')
    b.set(6, 4, 6, 'lantern', hanging=True, waterlogged=False)
    b.set(9, 4, 6, 'lantern', hanging=True, waterlogged=False)
    b.custom(3, 2, 5, 'fireside_armchair', facing='west')
    # Sleeping wing.
    b.door(9, 2, 9, facing='south', wood='spruce')
    b.bed(8, 2, 13, 'south', 'green')
    b.bed(11, 2, 13, 'south', 'brown')
    b.barrel(10, 2, 14, 'up')
    b.set(11, 2, 10, 'lantern', hanging=False, waterlogged=False)
    H.wall_hide(b, 8, 3, 10, 'east')
    H.bedroom_lamp(b, 10, 4, 11)
    b.room('bedroom', (10, 3, 11))
    plaque(b, 6, 3)
    H.moss_roof(b, rng, .12)
    # Yard tucked into the L: berry patch, woodpile, a young spruce.
    H.path(b, 5, 0, 2, rng)
    b.entrance(5)
    for x in (2, 3, 4):
        for z in (12, 13):
            H.berry_bush(b, x, z, rng)
    H.woodpile(b, 1, 1, 11, 'x', length=4)
    H.chopping_block(b, 5, 1, 11, rng)
    H.spruce(b, 3, 1, 15, height=6, shape=[0, 1, 1, 2, 1])
    H.lantern_post(b, 14, 1, 2, height=2)
    H.undergrowth(b, [(x, z) for x in range(16) for z in (0, 1, 2, 16, 17)] + [(x, z) for x in (14, 15)
                                                                              for z in range(18)], rng, .3)
    b.resident(5, 2, 6)
    b.resident(9, 2, 7)
    b.natural_ground()
    return b


DESIGNS = {
    'taiga/trapper_hut': trapper_hut,
    'taiga/aframe_cabin': aframe_cabin,
    'taiga/porch_cabin': porch_cabin,
    'taiga/log_lodge': log_lodge,
    'taiga/longhouse': longhouse,
    'taiga/dogtrot_cabin': dogtrot_cabin,
    'taiga/stone_cottage': stone_cottage,
    'taiga/cabin_ell': cabin_ell,
}
