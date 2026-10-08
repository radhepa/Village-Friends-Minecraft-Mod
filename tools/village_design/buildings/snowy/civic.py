"""Snowy civic buildings that face the town square (one of each per village).

Northern architecture rather than a reskin of the plains set: saddle-notched log
cabins on stone plinths, steep pitch-2 roofs that hold the snow, stone chimneys
that smoke all winter, enclosed storm porches, small shuttered windows and warm
hearths inside. Each keeps the plains building's residents, workstations, plaque
and enclosed bedrooms. Large slots are at most 17 wide (8 either side of the
entrance), small ones 11 (5 either side).
"""
import random

from ...kit import Build
from ... import parts
from . import palette
from . import core_parts as cp

R = palette.ROOFS
LOOT = palette.LOOT


def plaque(b, x, z, facing='north', y=1):
    b.custom(x, y, z, 'house_plaque', facing=facing)


def storm_porch(b, x0, z0, x1, z1, door_x, roof, log='spruce_log', y_floor=1, wall_top=4, gable='spruce_planks',
                rake=(1, 1), door_wood='spruce'):
    """Enclosed entry porch (x0..x1, z0..z1) with an outer door on its north wall."""
    cp.plinth(b, x0, z0, x1, z1, top=y_floor, skirt=None)
    cp.log_walls(b, x0, z0, x1, z1, y_floor + 1, wall_top, log=log, notch=False)
    parts.beam_ring(b, x0, z0, x1, z1, wall_top + 1, 'stripped_spruce_log')
    b.fill(x0 + 1, wall_top + 1, z0 + 1, x1 - 1, wall_top + 1, z1 - 1, 'spruce_planks')
    ridge = cp.steep_roof(b, x0, z0, x1, z1, wall_top + 1, roof, axis='z', rake=rake, gable=gable)
    b.door(door_x, y_floor + 1, z0, facing='south', wood=door_wood)
    b.set(door_x, y_floor, z0 - 1, 'cobblestone_stairs', facing='south', half='bottom', lock=True)
    return ridge


# ----------------------------------------------------------------------------- tavern
def tavern():
    """The Frost Hearth: a mead hall for the long winter.

    A gable-fronted log hall under a great slate roof, entered through a storm porch. Inside, a
    hooded central fire with fireside armchairs and settles, long trestle tables, a bar with stools
    and standing room, and the bard's dais; the keeper's well behind the bar, the kitchen wing
    behind the hall, and two guest rooms in the roof. 33 seats, 10 of them at the fire.

    Tavern furniture faces the way its sitter faces; stair chairs face their backrest side.
    """
    rng = random.Random(3301)
    b = Build('snowy/tavern', (17, 27, 29))
    storm_porch(b, 6, 2, 10, 5, 8, R['slate'], rake=(1, 0))
    # The hall: walls x 1..15, z 5..21, Y 2..6; floor at Y=1, attic floor at Y=7.
    cp.plinth(b, 1, 5, 15, 21)
    cp.log_walls(b, 1, 5, 15, 21, 2, 6)
    parts.beam_ring(b, 1, 5, 15, 21, 7, 'stripped_spruce_log')
    b.fill(2, 7, 6, 14, 7, 20, 'spruce_planks')
    ridge = cp.steep_roof(b, 1, 5, 15, 21, 7, R['slate'], axis='z', rake=(1, 0), gable='spruce_planks',
                          trim=R['dark_oak'])
    cp.clear(b, 2, 2, 6, 14, 6, 20)
    b.door(8, 2, 5, facing='south', wood='spruce')
    # Kitchen wing behind, its gable tucked against the hall's back wall.
    cp.plinth(b, 7, 21, 15, 27, skirt=None)
    cp.log_walls(b, 7, 21, 15, 27, 2, 5, skip={(x, 21) for x in range(8, 15)})
    parts.beam_ring(b, 7, 21, 15, 27, 6, 'stripped_spruce_log')
    b.fill(8, 6, 22, 14, 6, 26, 'spruce_planks')
    wing_ridge = cp.steep_roof(b, 7, 21, 15, 27, 6, R['slate'], axis='z', rake=(0, 1), gable='spruce_planks')
    cp.clear(b, 8, 2, 22, 14, 5, 26)
    _snow_tavern_hearth(b, ridge)
    _snow_tavern_tables(b)
    _snow_tavern_bar(b)
    _snow_tavern_kitchen(b, wing_ridge)
    _snow_tavern_attic(b)
    _snow_tavern_outside(b, rng)
    b.entrance(8)
    b.natural_ground()
    return b


def _snow_tavern_hearth(b, ridge):
    """A long fire in the middle of the floor under a hanging stone hood, armchairs and settles round it."""
    for x in range(6, 9):
        for z in range(10, 14):
            b.set(x, 1, z, 'stone_bricks' if (x + z) % 2 else 'polished_andesite')
    for z in (11, 12):
        b.set(7, 2, z, 'campfire', lit=True, signal_fire=False, facing='south', waterlogged=False)
        b.set(6, 4, z, 'cobblestone_stairs', facing='east', half='top', lock=True)
        b.set(8, 4, z, 'cobblestone_stairs', facing='west', half='top', lock=True)
    for z, f in ((10, 'south'), (13, 'north')):
        b.set(7, 4, z, 'cobblestone_stairs', facing=f, half='top', lock=True)
    cp.chimney(b, [(7, 11), (7, 12)], 4, ridge + 1)
    for z in (11, 12):
        b.custom(5, 2, z, 'fireside_armchair', facing='east')
        b.custom(9, 2, z, 'fireside_armchair', facing='west')
    for x in (6, 7, 8):
        b.custom(x, 2, 9, 'village_bench', facing='south')
        b.custom(x, 2, 14, 'village_bench', facing='north')
    # Firewood and a kettle by the fire.
    b.set(6, 2, 10, 'spruce_log', axis='z')
    b.set(8, 2, 13, 'cauldron')
    b.set(6, 2, 13, 'spruce_log', axis='x')
    b.set(8, 2, 10, 'spruce_log', axis='x')


def _snow_tavern_tables(b):
    """Long trestle tables, the bard's dais by the door, beams, lanterns and the stair to the attic."""
    # West long table of four, chairs down both sides.
    for z in range(10, 14):
        b.custom(3, 2, z, 'tavern_table')
        b.custom(2, 2, z, 'tavern_chair', facing='east')
        b.custom(4, 2, z, 'tavern_chair', facing='west')
    # Back long table of five across the hall.
    for x in range(3, 8):
        b.custom(x, 2, 17, 'tavern_table')
        b.custom(x, 2, 16, 'tavern_chair', facing='south')
        b.custom(x, 2, 18, 'tavern_chair', facing='north')
    # The bard's dais in the front west corner with its note block.
    for x in (2, 3, 4):
        for z in (6, 7):
            b.set(x, 2, z, 'dark_oak_planks' if (x, z) != (3, 7) else 'red_wool')
    for x in (2, 3, 4):
        b.set(x, 2, 8, 'spruce_slab', type='bottom', waterlogged=False)
    b.set(2, 3, 6, 'note_block', instrument='bass', note=0, powered=False)
    cp.banner(b, 3, 5, 6, 'south', 'light_blue')
    cp.banner(b, 2, 5, 7, 'east', 'white')
    # Beams across the hall with lanterns, and a hanging ring of lanterns over the back table.
    for z in (8, 15, 19):
        for x in range(2, 15):
            if b.get(x, 6, z)[0] == 'minecraft:air':
                b.set(x, 6, z, 'stripped_spruce_log', axis='x')
    for x, z in ((3, 8), (10, 8), (3, 15), (10, 15), (5, 19), (10, 19)):
        cp.hang(b, x, 5, z)
    for x in (4, 6):
        cp.hang(b, x, 5, 17)
    for x, z, f in ((1, 9, 'east'), (1, 15, 'east')):
        cp.banner(b, x + 1, 5, z, f, 'blue')
    # Stair to the guest attic along the back wall, kegs beneath.
    parts.stair_run(b, 3, 20, 2, 6, 'east', wood='spruce')
    b.barrel(9, 2, 20, 'north')
    b.barrel(10, 2, 20, 'up')
    b.barrel(9, 3, 20, 'north')


def _snow_tavern_bar(b):
    """The bar down the east side: counter, five stools with room to stand between, the keeper's well."""
    for z in range(7, 17):
        b.set(12, 2, z, 'stripped_spruce_log', axis='z')
    b.set(12, 2, 17, 'stripped_spruce_log', axis='y')
    b.set(12, 3, 17, 'lantern', hanging=False, waterlogged=False)
    for z in (8, 10, 12, 14, 16):
        b.custom(11, 2, z, 'bar_stool', facing='east')
    for z in range(6, 21):
        b.set(13, 1, z, 'spruce_slab', type='bottom', waterlogged=False)
    b.custom(14, 2, 11, 'tap_stand', facing='west')
    b.custom(14, 2, 12, 'drinks_barrel', facing='west')
    b.resident(13, 2, 12, 'tavern_keeper')
    for z in (6, 7, 8, 9, 10, 16, 17, 18, 19, 20):
        b.barrel(14, 2, z, 'west')
    for z in (7, 9, 17, 19):
        b.barrel(14, 3, z, 'west')
    b.set(14, 2, 13, 'brewing_stand', has_bottle_0=False, has_bottle_1=False, has_bottle_2=False)
    b.chest(14, 2, 14, 'west')
    b.set(14, 2, 15, 'water_cauldron', level=3)
    for z in (8, 10, 18):
        b.set(14, 4, z, 'spruce_trapdoor', facing='west', half='top', open=False, powered=False, waterlogged=False)
        b.set(14, 5, z, 'candle', candles=3, lit=True, waterlogged=False)
    cp.banner(b, 14, 4, 11, 'west', 'light_blue')
    cp.banner(b, 14, 4, 12, 'west', 'white')
    cp.hang(b, 13, 5, 10)
    cp.hang(b, 13, 5, 15)
    # Serving hatch and door to the kitchen at the end of the well.
    b.set(12, 2, 21, 'spruce_stairs', facing='north', half='top', waterlogged=False, lock=True)
    b.set(12, 3, 21, 'air')
    b.door(13, 2, 21, facing='north', wood='spruce')
    for x in (8, 9, 10, 11, 14):
        for y in range(2, 6):
            b.set(x, y, 21, 'spruce_log', axis='x')
    b.set(12, 4, 21, 'spruce_log', axis='x')
    b.set(12, 5, 21, 'spruce_log', axis='x')


def _snow_tavern_kitchen(b, wing_ridge):
    """The cook's kitchen: stove and smoker against a stone chimney breast, pantry, water and a back door."""
    b.custom(11, 2, 26, 'kitchen_stove', facing='north')
    b.set(12, 2, 26, 'smoker', facing='north', lit=True)
    b.set(10, 2, 26, 'water_cauldron', level=3)
    cp.chimney(b, [(11, 27), (12, 27)], 1, wing_ridge + 1)
    for x in (11, 12):
        b.set(x, 4, 26, 'cobblestone')
        b.set(x, 5, 26, 'cobblestone')
    b.set(8, 2, 22, 'crafting_table')
    b.barrel(8, 2, 23, 'east')
    b.barrel(8, 3, 23, 'east')
    b.barrel(8, 2, 26, 'up')
    b.set(8, 3, 26, 'hay_block', axis='y')
    b.barrel(14, 2, 22, 'west')
    b.set(14, 2, 23, 'smooth_stone_slab', type='double')
    b.set(14, 2, 24, 'smooth_stone_slab', type='double')
    b.set(14, 3, 23, 'potted_red_mushroom')
    b.set(13, 2, 26, 'barrel', facing='up', open=False)
    b.set(14, 2, 26, 'composter', level=4)
    cp.hang(b, 11, 5, 24)
    b.resident(11, 2, 24, 'cook')
    parts.front_door(b, 7, 2, 24, 'west', wood='spruce', step='cobblestone_stairs', lamps=False)
    cp.window(b, 15, 3, 24, 'east')
    cp.window(b, 9, 3, 27, 'south')


def _snow_tavern_attic(b):
    """Guest attic under the roof: two rooms at the front, a landing over the back of the hall."""
    for x in range(2, 15):
        for z in range(6, 21):
            if b.get(x, 11, z)[0] == 'minecraft:air':
                b.set(x, 11, z, 'spruce_planks')
    for z in range(6, 14):
        cp.fill_up(b, [(7, z), (10, z)], 8, 'spruce_planks')
    for x in list(range(2, 7)) + list(range(11, 15)):
        cp.fill_up(b, [(x, 13)], 8, 'spruce_planks')
    b.door(7, 8, 9, facing='east', wood='spruce')
    b.door(10, 8, 9, facing='east', wood='spruce', hinge='right')
    b.bed(3, 8, 8, 'north', 'red')
    b.bed(5, 8, 8, 'north', 'white')
    b.chest(4, 8, 6, 'south', loot=LOOT)
    b.set(4, 8, 11, 'barrel', facing='up', open=False)
    parts.rug(b, 3, 10, 5, 12, 8, 'red', border='white')
    cp.hang(b, 4, 10, 9)
    b.room('guest_room_west', (5, 9, 10))
    b.bed(11, 8, 8, 'north', 'light_blue')
    b.bed(13, 8, 8, 'north', 'white')
    b.chest(12, 8, 6, 'south', loot=LOOT)
    parts.rug(b, 11, 10, 13, 12, 8, 'light_blue', border='white')
    cp.hang(b, 12, 10, 10)
    b.room('guest_room_east', (12, 9, 10))
    cp.window(b, 3, 9, 5, 'north', shutters=False)
    cp.window(b, 12, 9, 5, 'north', shutters=False)
    for z in range(14, 20, 2):
        b.barrel(13, 8, z, 'west')
    b.set(12, 8, 16, 'white_wool')
    cp.hang(b, 9, 10, 16)
    cp.hang(b, 5, 10, 16)


def _snow_tavern_outside(b, rng):
    """Small shuttered windows, lamps, woodpiles under the eaves, the sign, plaque and a back yard."""
    for z in (8, 16):
        cp.window(b, 1, 3, z, 'west', width=2)
    cp.window(b, 15, 4, 8, 'east', width=2, shutters=False)
    cp.window(b, 15, 4, 18, 'east', width=2, shutters=False)
    for x in (3, 12):
        cp.window(b, x, 3, 5, 'north', width=2)
    cp.window(b, 7, 3, 2, 'north', shutters=False)
    cp.window(b, 9, 3, 2, 'north', shutters=False)
    for y in range(14, 17):
        b.set(8, y, 5, 'glass_pane')
    for x in (5, 11):
        cp.lamp_post(b, x, 1, height=3)
    parts.woodpile(b, 0, 1, 7, 'z', length=6, height=3)
    parts.woodpile(b, 16, 1, 7, 'z', length=5, height=2)
    b.set(13, 0, 1, 'cobblestone')
    for y in range(1, 6):
        b.set(13, y, 1, 'spruce_fence')
    b.set(12, 5, 1, 'spruce_fence')
    b.set(12, 4, 1, 'spruce_hanging_sign', rotation=8, attached=False, waterlogged=False)
    for x in (2, 14):
        b.custom(x, 1, 2, 'village_bench', facing='north')
    plaque(b, 10, 1)
    for x, z in ((3, 2), (13, 2)):
        b.barrel(x, 1, z, 'up')
    for z in range(0, 2):
        b.set(8, 0, z, 'cobblestone' if z else 'gravel')
    for x in range(0, 17):
        for z in range(0, 5):
            if (x, 0, z) not in b.grid and rng.random() < .55:
                b.set(x, 0, z, rng.choice(['snow_block', 'snow_block', 'gravel', 'cobblestone']))
    # Back yard by the kitchen door.
    parts.woodpile(b, 1, 1, 23, 'x', length=4, height=2)
    b.set(4, 1, 26, 'stripped_spruce_log', axis='y')
    for x, z in ((1, 26), (1, 27), (2, 27)):
        b.barrel(x, 1, z, 'up')
    cp.sledge(b, 5, 27, 'east', load=('barrel', 'white_wool'))
    for x in range(0, 7):
        for z in range(22, 29):
            if (x, 0, z) not in b.grid and rng.random() < .5:
                b.set(x, 0, z, rng.choice(['snow_block', 'gravel', 'coarse_dirt']))


# --------------------------------------------------------------------------- garrison
def garrison():
    """Frost Watch: a stone-and-log blockhouse with a jettied bunk floor, a lookout tower
    with a covered gallery, and a palisaded training yard."""
    rng = random.Random(3302)
    b = Build('snowy/garrison', (17, 27, 21))
    st = parts.Style(frame='stripped_spruce_log', fill='cobblestone', floor='spruce_planks', roof=R['slate'],
                     base='cobblestone', trim='spruce', door='spruce', upper_fill='spruce_planks')
    house = parts.Body(b, 1, 11, 15, 18, st, heights=(4, 3), jetty=('north',), stone_ground=True).build()
    cp.log_walls(b, 1, 10, 15, 18, 7, 9, notch=True)
    parts.beam_ring(b, 1, 10, 15, 18, 10, 'stripped_spruce_log')
    ridge = cp.steep_roof(b, 1, 10, 15, 18, 10, R['slate'], axis='x', gable='spruce_planks', trim=R['dark_oak'])
    for z in range(12, 18):
        b.set(1, 1, z, 'cobblestone')
    parts.front_door(b, 7, 2, 11, 'north', wood='spruce', step='cobblestone_stairs', lamps=False)
    for x in (6, 8):
        cp.hang(b, x, 5, 10)
    # Lookout tower: stone shaft, log watch room, a railed gallery and a steep spire.
    tx0, tz0, tx1, tz1 = 11, 1, 15, 5
    for y in range(0, 13):
        for x in range(tx0, tx1 + 1):
            for z in range(tz0, tz1 + 1):
                edge = x in (tx0, tx1) or z in (tz0, tz1)
                corner = x in (tx0, tx1) and z in (tz0, tz1)
                if y <= 1:
                    b.set(x, y, z, 'cobblestone')
                elif edge and y <= 7:
                    b.set(x, y, z, 'stone_bricks' if corner else 'cobblestone')
                elif not edge and y == 7:
                    b.set(x, y, z, 'spruce_planks')
    cp.log_walls(b, tx0, tz0, tx1, tz1, 8, 12, notch=False)
    for x in range(tx0 - 1, tx1 + 2):
        for z in range(tz0 - 1, tz1 + 2):
            edge = x in (tx0 - 1, tx1 + 1) or z in (tz0 - 1, tz1 + 1)
            b.set(x, 13, z, 'stripped_spruce_log' if edge else 'spruce_planks',
                  axis='x' if z in (tz0 - 1, tz1 + 1) else 'z')
            if edge:
                b.set(x, 14, z, 'spruce_fence')
    for x, z in ((tx0 - 1, tz0 - 1), (tx1 + 1, tz0 - 1), (tx0 - 1, tz1 + 1), (tx1 + 1, tz1 + 1)):
        for y in (14, 15, 16):
            b.set(x, y, z, 'spruce_log', axis='y')
    for x in range(tx0 - 1, tx1 + 2):
        for z in (tz0 - 1, tz1 + 1):
            b.set(x, 12, z, 'spruce_stairs', facing='south' if z == tz0 - 1 else 'north', half='top', lock=True,
                  shape='straight')
    for z in range(tz0, tz1 + 1):
        for x in (tx0 - 1, tx1 + 1):
            b.set(x, 12, z, 'spruce_stairs', facing='east' if x == tx0 - 1 else 'west', half='top', lock=True,
                  shape='straight')
    parts.pyramid_roof(b, tx0 - 1, tz0 - 1, tx1 + 1, tz1 + 1, 17, 'deepslate_tile_stairs', 'deepslate_tiles', pitch=2,
                       finial=['spruce_fence', 'lightning_rod'])
    cp.hang(b, 13, 16, 3)
    for y in range(2, 14):
        b.set(tx0 + 1, y, tz0 + 1, 'ladder', facing='south')
    b.set(tx0 + 1, 13, tz0 + 1, 'spruce_trapdoor', facing='south', half='top', open=False, powered=False,
          waterlogged=False)
    b.door(tx0 + 2, 2, tz1, facing='north', wood='spruce')
    b.set(tx0 + 2, 1, tz1, 'cobblestone')
    b.set(tx0 + 2, 1, tz1 + 1, 'cobblestone_stairs', facing='north', half='bottom', lock=True)
    for y in (4, 10):
        for x, z, out in ((tx0, tz0 + 2, 'west'), (tx1, tz0 + 2, 'east'), (tx0 + 2, tz0, 'north')):
            b.set(x, y, z, 'glass_pane')
    cp.banner(b, tx0 + 2, 10, tz0 - 1, 'north', 'blue')
    cp.banner(b, tx0 - 1, 10, tz0 + 2, 'west', 'blue')
    b.set(tx0 + 2, 8, tz0 + 2, 'barrel', facing='up', open=False)
    cp.hang(b, tx0 + 3, 6, tz0 + 3)
    # Palisade around the yard with a gate toward the square.
    stakes = [(x, 0) for x in range(0, 17) if not 6 <= x <= 10]
    stakes += [(0, z) for z in range(1, 11)] + [(16, z) for z in range(6, 11)]
    cp.palisade(b, stakes)
    for x in (6, 10):
        b.set(x, 0, 0, 'cobblestone')
        for y in range(1, 5):
            b.set(x, y, 0, 'stripped_spruce_log', axis='y')
        cp.standing_lantern(b, x, 5, 0)
    # Training yard.
    for x in range(1, 16):
        for z in range(1, 10):
            if not (tx0 <= x <= tx1 and tz0 <= z <= tz1) and (x, 0, z) not in b.grid:
                b.set(x, 0, z, rng.choice(['gravel', 'gravel', 'snow_block', 'coarse_dirt', 'cobblestone']))
    for z in range(0, 11):
        b.set(7 + (z % 2), 0, z, 'cobblestone')
        b.set(8 - (z % 2), 0, z, 'stone_bricks')
    for x, z in ((3, 3), (3, 6), (6, 5)):
        b.custom(x, 1, z, 'training_dummy', facing='south')
    b.custom(1, 1, 8, 'archery_target', facing='east')
    b.custom(1, 1, 9, 'archery_target', facing='east')
    for x, z in ((14, 8), (15, 8), (15, 9)):
        b.set(x, 1, z, 'hay_block', axis='y')
    b.set(10, 1, 9, 'grindstone', face='floor', facing='north')
    b.barrel(11, 1, 9, 'up')
    b.set(12, 1, 9, 'smithing_table')
    # A warming brazier for the sentries.
    b.set(5, 0, 8, 'cobblestone')
    b.set(5, 1, 8, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    for x, z, f in ((4, 8, 'east'), (6, 8, 'west')):
        b.custom(x, 1, z, 'campfire_bench', facing=f)
    parts.woodpile(b, 2, 1, 10, 'x', length=4, height=2)
    plaque(b, 9, 10)
    b.resident(5, 1, 6, 'knight')
    b.resident(3, 1, 8, 'archer')
    # Ground floor: guard room with the command desk, hearth and armoury.
    cp.fireplace(b, 2, 2, 15, 'east', ridge + 1)
    cp.chimney(b, [(2, 15), (2, 16)], 17, ridge + 1)
    b.custom(5, 2, 16, 'command_desk', facing='north')
    parts.chair(b, 5, 2, 17, 'south')
    b.set(4, 2, 17, 'bookshelf')
    b.set(4, 3, 17, 'lantern', hanging=False, waterlogged=False)
    b.chest(12, 2, 17, 'north', loot='minecraft:chests/village/village_weaponsmith')
    b.set(11, 2, 17, 'anvil', facing='east')
    b.barrel(10, 2, 17, 'up')
    b.custom(10, 2, 13, 'training_dummy', facing='west')
    parts.rug(b, 4, 13, 7, 14, 2, 'blue', border='light_gray')
    for x in (5, 10):
        cp.hang(b, x, 5, 14)
    parts.stair_run(b, 14, 12, 2, 5, 'south', wood='spruce')
    # Upper floor: bunk room behind a partition, the stair landing beside it.
    for z in range(11, 18):
        for y in (7, 8, 9):
            b.set(12, y, z, 'spruce_planks')
    b.door(12, 7, 15, facing='west', wood='spruce')
    for x, c in ((3, 'blue'), (5, 'light_blue'), (7, 'blue'), (9, 'light_blue')):
        b.bed(x, 7, 16, 'south', c)
    b.chest(10, 7, 17, 'north', loot=LOOT)
    b.set(2, 7, 11, 'crafting_table')
    b.barrel(2, 7, 12, 'up')
    parts.rug(b, 4, 12, 8, 13, 7, 'light_gray')
    cp.hang(b, 6, 9, 14)
    cp.hang(b, 13, 9, 13)
    b.room('bunk_room', (6, 8, 14))
    # Windows: arrow-slit narrow below, small shuttered ones on the log floor.
    for x in (3, 11):
        b.set(x, 3, 11, 'glass_pane')
        b.set(x, 4, 11, 'glass_pane')
    for z in (13, 16):
        b.set(15, 3, z, 'glass_pane')
    for x in (3, 6, 9):
        cp.window(b, x, 8, 10, 'north')
    cp.window(b, 13, 8, 10, 'north', shutters=False)
    for x in (4, 7, 10):
        cp.window(b, x, 8, 18, 'south')
    cp.window(b, 1, 13, 14, 'west')
    cp.window(b, 15, 13, 14, 'east')
    b.entrance(8)
    b.natural_ground()
    return b


# --------------------------------------------------------------------------- workshop
def workshop():
    """Sled & Loom: a gable-fronted log workshop (tailor below, bedroom in the roof) with the
    carpenter's lean-to lumber shed along its east wall."""
    rng = random.Random(3303)
    b = Build('snowy/workshop', (15, 19, 19))
    storm_porch(b, 4, 2, 8, 5, 6, R['spruce'], wall_top=3, rake=(1, 0))
    cp.plinth(b, 1, 5, 10, 13)
    cp.log_walls(b, 1, 5, 10, 13, 2, 5)
    parts.beam_ring(b, 1, 5, 10, 13, 6, 'stripped_spruce_log')
    b.fill(2, 6, 6, 9, 6, 12, 'spruce_planks')
    ridge = cp.steep_roof(b, 1, 5, 10, 13, 6, R['spruce'], axis='z', gable='stripped_spruce_log',
                          trim=R['dark_oak'])
    cp.clear(b, 2, 2, 6, 9, 5, 12)
    b.door(6, 2, 5, facing='south', wood='spruce')
    # Carpenter's lean-to.
    parts.shed_roof(b, 11, 4, 14, 14, 4, R['spruce'], slope='east', overhang=0)
    for z in (5, 9, 13):
        b.set(14, 0, z, 'cobblestone')
        for y in (1, 2, 3):
            b.set(14, y, z, 'stripped_spruce_log', axis='y')
    for x in range(11, 15):
        for z in range(4, 15):
            if (x, 0, z) not in b.grid:
                b.set(x, 0, z, 'spruce_planks' if (x + z) % 3 else 'stripped_spruce_log', axis='x')
    b.custom(12, 1, 8, 'sawmill', facing='west')
    b.set(12, 1, 12, 'crafting_table')
    b.set(11, 1, 12, 'stonecutter', facing='west')
    parts.woodpile(b, 13, 1, 10, 'z', length=3, height=3)
    parts.woodpile(b, 11, 1, 5, 'z', length=2, height=2, wood='birch')
    b.set(13, 1, 6, 'spruce_planks')
    b.set(13, 2, 6, 'spruce_slab', type='bottom')
    cp.hang(b, 12, 4, 9)
    cp.hang(b, 12, 4, 13)
    b.resident(12, 1, 10, 'carpenter')
    # A sledge on blocks, half built.
    b.set(12, 1, 15, 'stripped_spruce_log', axis='x')
    b.set(13, 1, 16, 'spruce_stairs', facing='west', half='bottom', lock=True, shape='straight')
    b.set(12, 1, 16, 'spruce_slab', type='bottom')
    b.set(11, 1, 16, 'spruce_slab', type='bottom')
    b.set(12, 1, 17, 'stripped_spruce_log', axis='x')
    # Tailor's shop: hearth, loom, sewing table and a wall of dyed wool.
    cp.fireplace(b, 2, 2, 8, 'east', ridge - 2)
    b.custom(4, 2, 10, 'sewing_table', facing='north')
    b.set(2, 2, 11, 'loom', facing='east')
    for z, c in zip(range(6, 12), ['white', 'light_blue', 'red', 'gray', 'brown', 'cyan']):
        b.set(9, 2, z, f'{c}_wool')
        b.set(9, 3, z, f'{c}_carpet')
    parts.rug(b, 5, 7, 7, 9, 2, 'white', border='light_blue')
    b.chest(8, 2, 6, 'west', loot=LOOT)
    cp.hang(b, 5, 5, 8)
    cp.hang(b, 7, 5, 11)
    b.resident(5, 2, 9, 'tailor')
    parts.stair_run(b, 3, 12, 2, 5, 'east', wood='spruce')
    # Bedroom in the roof, the stair landing behind a partition.
    for x in range(2, 10):
        cp.fill_up(b, [(x, 10)], 7, 'spruce_planks')
    b.door(5, 7, 10, facing='south', wood='spruce')
    b.bed(3, 7, 7, 'north', 'light_blue')
    b.bed(8, 7, 7, 'north', 'white')
    b.chest(5, 7, 6, 'south', loot=LOOT)
    b.barrel(6, 7, 6, 'up')
    cp.hang(b, 5, 11, 8, chain=2)
    cp.hang(b, 7, 10, 12)
    b.room('bedroom', (5, 8, 8))
    # Windows.
    cp.window(b, 2, 3, 5, 'north')
    cp.window(b, 9, 3, 5, 'north')
    cp.window(b, 3, 8, 5, 'north', shutters=False)
    cp.window(b, 8, 8, 5, 'north', shutters=False)
    cp.window(b, 1, 3, 11, 'west')
    cp.window(b, 10, 3, 7, 'east', shutters=False)
    cp.window(b, 5, 3, 13, 'south', width=2)
    cp.window(b, 5, 9, 13, 'south', width=2, shutters=False)
    # Front yard: lamps, path, plaque, a woodpile by the porch.
    for x in (3, 9):
        cp.lamp_post(b, x, 1, height=2)
    plaque(b, 2, 2)
    parts.woodpile(b, 9, 1, 3, 'z', length=2, height=2)
    for z in range(0, 2):
        b.set(6, 0, z, 'cobblestone' if z else 'gravel')
    for x in range(0, 15):
        for z in range(0, 4):
            if (x, 0, z) not in b.grid and rng.random() < .5:
                b.set(x, 0, z, rng.choice(['snow_block', 'snow_block', 'gravel', 'coarse_dirt']))
    parts.woodpile(b, 2, 1, 15, 'x', length=4, height=2)
    b.set(7, 1, 16, 'stripped_spruce_log', axis='y')
    b.barrel(8, 1, 15, 'up')
    b.entrance(6)
    b.natural_ground()
    return b


# ----------------------------------------------------------------------------- chapel
def stave_walls(b, x0, z0, x1, z1, y0, y1):
    """Upright staves: vertical spruce logs with stripped corner posts."""
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        for y in range(y0, y1 + 1):
            b.set(x, y, z, 'stripped_spruce_log' if corner else 'spruce_log', axis='y')


def gallery_roof(b, x0, z0, x1, z1, top, depth=3, stairs='dark_oak_stairs'):
    """Skirt roof around a rectangle: rings stepping down and out from the wall top."""
    for d in range(1, depth + 1):
        y = top - d
        for x, z, facing, corner in parts.ring(x0 - d, z0 - d, x1 + d, z1 + d):
            if not b.inside(x, y, z):
                continue
            if corner:
                f = 'south' if z == z0 - d else 'north'
            else:
                f = OPPOSITE_OUT[facing]
            b.set(x, y, z, stairs, facing=f, half='bottom')


OPPOSITE_OUT = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}


def grave(b, x, z, rng):
    b.set(x, 0, z + 1, rng.choice(['snow_block', 'coarse_dirt', 'podzol']))
    kind = rng.random()
    if kind < .45:
        b.set(x, 1, z, rng.choice(['cobblestone_wall', 'stone_brick_wall']))
        if rng.random() < .5:
            b.set(x, 2, z, 'spruce_fence')
    elif kind < .8:
        b.set(x, 1, z, 'stone_brick_stairs', facing='south', half='bottom', lock=True)
    else:
        b.set(x, 1, z, 'chiseled_stone_bricks')
    if rng.random() < .3:
        b.set(x, 1, z + 1, 'candle', candles=1, lit=True, waterlogged=False)


def chapel():
    """Stave chapel: upright-log nave in a covered gallery, tiered dark roofs, a belfry
    turret with a spire, dragon-head gable crests and a snowy churchyard."""
    rng = random.Random(3304)
    b = Build('snowy/chapel', (17, 30, 26))
    nx0, nz0, nx1, nz1 = 4, 7, 12, 17
    # Gallery (svalgang) floor and posts.
    for x in range(nx0 - 2, nx1 + 3):
        for z in range(nz0 - 2, nz1 + 3):
            b.set(x, 0, z, 'cobblestone')
            b.set(x, 1, z, 'spruce_planks' if not (nx0 <= x <= nx1 and nz0 <= z <= nz1) else 'cobblestone')
    for x, z, facing, corner in parts.ring(nx0 - 2, nz0 - 2, nx1 + 2, nz1 + 2):
        post = corner or (facing in ('north', 'south') and (x - nx0) % 3 == 0) or \
            (facing in ('east', 'west') and (z - nz0) % 3 == 1)
        if post:
            for y in (2, 3, 4):
                b.set(x, y, z, 'stripped_spruce_log', axis='y')
        else:
            b.set(x, 2, z, 'spruce_fence')
        b.set(x, 5, z, 'stripped_spruce_log', axis='x' if facing in ('north', 'south') else 'z')
    gallery_roof(b, nx0, nz0, nx1, nz1, 8, depth=3)
    for x, z, facing, corner in parts.ring(nx0 - 2, nz0 - 2, nx1 + 2, nz1 + 2):
        b.set(x, 5, z, 'stripped_spruce_log', axis='x' if facing in ('north', 'south') else 'z')
    # Nave of upright staves on a stone sill, open to its steep roof.
    for x in range(nx0, nx1 + 1):
        for z in range(nz0, nz1 + 1):
            b.set(x, 1, z, 'spruce_planks' if nx0 < x < nx1 and nz0 < z < nz1 else 'cobblestone')
    stave_walls(b, nx0, nz0, nx1, nz1, 2, 7)
    parts.beam_ring(b, nx0, nz0, nx1, nz1, 8, 'stripped_spruce_log')
    ridge = cp.steep_roof(b, nx0, nz0, nx1, nz1, 8, R['dark_oak'], axis='z', gable='spruce_log', trim=R['spruce'])
    for x in range(nx0 + 1, nx1):
        for z in range(nz0 + 1, nz1):
            for y in range(2, 9):
                b.set(x, y, z, 'air')
    # Entrance porch with its own steep gable.
    porch_ridge = storm_porch(b, 6, 2, 10, 6, 8, R['dark_oak'], log='spruce_log', rake=(1, 0))
    b.door(8, 2, nz0, facing='south', wood='dark_oak')
    b.set(8, 1, nz0 - 1, 'spruce_planks')
    cp.clear(b, 7, 2, 3, 9, 4, 6)
    b.door(8, 2, 2, facing='south', wood='dark_oak')
    cp.hang(b, 8, 4, 4)
    # Belfry turret on the ridge and its spire.
    tx0, tz0, tx1, tz1 = 7, 11, 9, 13
    for y in range(ridge - 1, ridge + 4):
        for x, z, facing, corner in parts.ring(tx0, tz0, tx1, tz1):
            mid = not corner
            if mid and y in (ridge + 1, ridge + 2):
                b.set(x, y, z, 'spruce_fence' if y == ridge + 1 else 'air')
            else:
                b.set(x, y, z, 'spruce_log' if not corner else 'stripped_spruce_log', axis='y')
    b.fill(tx0, ridge + 3, tz0, tx1, ridge + 3, tz1, 'dark_oak_planks')
    b.set(8, ridge + 2, 12, 'bell', attachment='ceiling', facing='north', powered=False)
    parts.pyramid_roof(b, tx0 - 1, tz0 - 1, tx1 + 1, tz1 + 1, ridge + 4, 'dark_oak_stairs', 'dark_oak_planks',
                       pitch=2, finial=['dark_oak_fence', 'lightning_rod'])
    # Dragon-head crests on the gable peaks.
    for z, f in ((nz0 - 1, 'north'), (nz1 + 1, 'south')):
        b.set(8, ridge + 1, z, 'dark_oak_stairs', facing=OPPOSITE_OUT[f], half='bottom', lock=True)
    b.set(8, porch_ridge + 1, 1, 'dark_oak_stairs', facing='south', half='bottom', lock=True)
    # Interior: pews, aisle, altar (the cleric's brewing stand), candles and lanterns.
    for z in (10, 12, 14):
        for x in (5, 6, 7, 9, 10, 11):
            b.set(x, 2, z, 'spruce_stairs', facing='north', half='bottom', lock=True, shape='straight')
    for z in range(nz0 + 2, 16):
        b.set(8, 2, z, 'red_carpet')
    for x in range(5, 12):
        b.set(x, 1, 16, 'dark_oak_planks')
    for x in (7, 8, 9):
        b.set(x, 2, 16, 'chiseled_stone_bricks' if x == 8 else 'stone_brick_slab', **({} if x == 8 else {'type': 'top'}))
    b.set(7, 3, 16, 'brewing_stand')
    b.set(8, 3, 16, 'candle', candles=3, lit=True, waterlogged=False)
    b.set(9, 3, 16, 'candle', candles=2, lit=True, waterlogged=False)
    for x in (5, 11):
        b.set(x, 2, 16, 'candle', candles=4, lit=True, waterlogged=False)
    for z in (9, 12, 15):
        cp.hang(b, 8, 11, z, chain=ridge - 13)
    for z in (9, 15):
        for x in (5, 11):
            cp.hang(b, x, 7, z)
    # Small high windows and a cross window in the front gable.
    for z in (9, 12, 15):
        for x in (nx0, nx1):
            b.set(x, 6, z, 'yellow_stained_glass_pane')
    for y, xs in ((10, (8,)), (11, (7, 8, 9)), (12, (8,))):
        for x in xs:
            b.set(x, y, nz1, 'orange_stained_glass_pane')
    b.set(8, 13, nz0, 'yellow_stained_glass_pane')
    # Churchyard behind, inside a low stone wall, with a spruce.
    for x in range(0, 17):
        b.set(x, 1, 25, 'cobblestone_wall' if x % 4 else 'stone_bricks')
    for z in range(21, 25):
        b.set(0, 1, z, 'cobblestone_wall' if z % 4 else 'stone_bricks')
        b.set(16, 1, z, 'cobblestone_wall' if z % 4 else 'stone_bricks')
    for x in (2, 5, 11, 14):
        grave(b, x, 22, rng)
    cp.spruce(b, 8, 1, 23, height=7)
    b.set(8, 0, 23, 'podzol')
    b.custom(1, 1, 22, 'village_bench', facing='east')
    # Front: lamp posts and a stone path through the snow.
    for z in range(0, 2):
        b.set(8, 0, z, 'stone_bricks' if z % 2 else 'cobblestone')
    for x in (4, 12):
        cp.lamp_post(b, x, 2, height=2, fence='dark_oak_fence')
    for x in list(range(0, 4)) + list(range(13, 17)):
        for z in range(0, 5):
            if (x, 0, z) not in b.grid:
                b.set(x, 0, z, 'snow_block' if rng.random() < .7 else 'gravel')
    cp.spruce(b, 1, 1, 2, height=5)
    cp.spruce(b, 15, 1, 2, height=5)
    b.entrance(8)
    b.natural_ground()
    return b


# ------------------------------------------------------------------------- apothecary
def apothecary():
    """Herbalist's stone cottage: infirmary by the hearth, bedroom in the roof, and a glass
    winter garden on the sunny back wall where herbs grow through the cold."""
    rng = random.Random(3305)
    b = Build('snowy/apothecary', (11, 19, 19))
    storm_porch(b, 3, 2, 7, 5, 5, R['dark_oak'], log='spruce_log', wall_top=3, rake=(1, 0),
                gable='stripped_spruce_log')
    cp.plinth(b, 1, 5, 9, 12, mat='cobblestone')
    cp.stone_walls(b, 1, 5, 9, 12, 2, 5, mat='cobblestone', quoin='stone_bricks')
    parts.beam_ring(b, 1, 5, 9, 12, 6, 'stripped_spruce_log')
    b.fill(2, 6, 6, 8, 6, 11, 'spruce_planks')
    ridge = cp.steep_roof(b, 1, 5, 9, 12, 6, R['dark_oak'], axis='z', gable='spruce_log', trim=R['spruce'])
    cp.clear(b, 2, 2, 6, 8, 5, 11)
    b.door(5, 2, 5, facing='south', wood='spruce')
    # Infirmary: press, brewing stand and cauldron along the front, two cots by the east wall.
    b.custom(3, 2, 6, 'alchemical_press', facing='south')
    b.set(4, 2, 6, 'brewing_stand')
    b.set(6, 2, 6, 'water_cauldron', level=2)
    b.barrel(7, 2, 6, 'up')
    b.set(8, 2, 6, 'spruce_planks')
    b.set(8, 3, 6, 'potted_fern')
    for z in (8, 10):
        b.custom(8, 2, z, 'apothecary_cot', facing='west')
    b.set(8, 2, 9, 'spruce_slab', type='bottom')
    b.set(8, 3, 9, 'candle', candles=2, lit=True, waterlogged=False)
    cp.fireplace(b, 2, 2, 9, 'east', ridge - 4)
    parts.rug(b, 4, 8, 6, 9, 2, 'green', border='white')
    cp.hang(b, 5, 5, 8)
    cp.hang(b, 7, 5, 10)
    b.resident(5, 2, 8, 'apothecary')
    parts.stair_run(b, 2, 11, 2, 5, 'east', wood='spruce')
    # Bedroom in the roof.
    for x in range(2, 9):
        cp.fill_up(b, [(x, 10)], 7, 'spruce_planks')
    b.door(7, 7, 10, facing='south', wood='spruce')
    b.bed(4, 7, 8, 'north', 'green')
    b.chest(4, 7, 9, 'north', loot=LOOT)
    b.set(6, 7, 6, 'brewing_stand')
    b.set(7, 7, 6, 'bookshelf')
    cp.hang(b, 5, 11, 8, chain=2)
    cp.hang(b, 5, 11, 11, chain=2)
    b.room('apothecary_bedroom', (5, 8, 7))
    # Winter garden behind, under glass.
    b.door(7, 2, 12, facing='north', wood='spruce')
    gx0, gz0, gx1, gz1 = 1, 12, 9, 17
    for x in range(gx0, gx1 + 1):
        for z in range(gz0 + 1, gz1 + 1):
            edge = x in (gx0, gx1) or z == gz1
            corner = x in (gx0, gx1) and z == gz1
            b.set(x, 0, z, 'cobblestone')
            b.set(x, 1, z, 'cobblestone' if edge else ('rooted_dirt' if x in (2, 3, 5) else 'spruce_planks'))
            for y in (2, 3, 4):
                if corner or (edge and z == gz0 + 1):
                    b.set(x, y, z, 'stripped_spruce_log', axis='y')
                elif edge:
                    b.set(x, y, z, 'glass_pane')
            b.set(x, 5, z, 'stripped_spruce_log' if edge else 'glass', axis='x')
    for z in range(gz0 + 1, gz1):
        b.set(2, 2, z, rng.choice(['sweet_berry_bush[age=2]', 'fern', 'fern']))
        b.set(3, 2, z, rng.choice(['brown_mushroom', 'fern', 'lily_of_the_valley']))
        b.set(5, 2, z, rng.choice(['sweet_berry_bush[age=3]', 'azure_bluet', 'fern']))
    b.set(8, 2, 16, 'composter', level=4)
    b.set(8, 2, 14, 'potted_spruce_sapling')
    b.set(8, 2, 15, 'flower_pot')
    cp.hang(b, 6, 4, 15)
    # Front: lamps, plaque, a drying rack with herbs and a bench.
    for x in (1, 9):
        cp.lamp_post(b, x, 2, height=2)
    plaque(b, 8, 3)
    for x in (1, 2):
        b.set(x, 1, 4, 'spruce_fence')
        b.set(x, 2, 4, 'spruce_fence')
    b.set(1, 3, 4, 'spruce_slab', type='bottom')
    b.set(2, 3, 4, 'spruce_slab', type='bottom')
    b.custom(8, 1, 1, 'village_bench', facing='north')
    for z in range(0, 1):
        b.set(5, 0, z, 'cobblestone')
    for x in range(0, 11):
        for z in range(0, 5):
            if (x, 0, z) not in b.grid and rng.random() < .6:
                b.set(x, 0, z, rng.choice(['snow_block', 'snow_block', 'podzol', 'gravel']))
    cp.window(b, 2, 3, 5, 'north')
    cp.window(b, 8, 3, 5, 'north', shutters=False)
    cp.window(b, 9, 3, 7, 'east')
    cp.window(b, 1, 3, 7, 'west')
    cp.window(b, 3, 8, 5, 'north', shutters=False)
    cp.window(b, 7, 8, 5, 'north', shutters=False)
    b.entrance(5)
    b.natural_ground()
    return b


# ---------------------------------------------------------------------------- library
def crow_steps(b, x0, x1, z, top, cap='stone_brick_slab', mat='stone_bricks'):
    """Turn a flush gable into a crow-stepped one: the wall rises one block above each roof step."""
    for x in range(x0, x1 + 1):
        for y in range(b.h - 1, top - 1, -1):
            s = b.get(x, y, z)
            if s[0].endswith(('_stairs', '_slab')) or s[0] == 'minecraft:deepslate_tiles':
                b.set(x, y, z, mat)
                b.set(x, y + 1, z, mat, clip=True)
                b.set(x, y + 2, z, cap, type='bottom', clip=True)
                break


def library():
    """Scholar's stone house: crow-stepped gables, a slate roof, tall narrow windows, books to
    the rafters and the scholar's room upstairs."""
    rng = random.Random(3306)
    b = Build('snowy/library', (11, 25, 17))
    st = parts.Style(frame='stone_bricks', fill='stone_bricks', floor='dark_oak_planks', roof=R['slate'],
                     base='cobblestone', trim='dark_oak', door='dark_oak', upper_fill='stone_bricks')
    body = parts.Body(b, 1, 4, 9, 14, st, heights=(4, 3), stone_ground=True).build()
    for x, z, facing, corner in parts.ring(1, 4, 9, 14):
        if corner:
            for y in range(2, 10):
                b.set(x, y, z, 'polished_andesite' if y % 2 else 'stone_bricks')
    parts.beam_ring(b, 1, 4, 9, 14, 6, 'stripped_dark_oak_log')
    b.fill(2, 6, 5, 8, 6, 13, 'dark_oak_planks')
    ridge = cp.steep_roof(b, 1, 4, 9, 14, 10, R['slate'], axis='z', rake=0, gable='stone_bricks')
    crow_steps(b, 0, 10, 4, 10)
    crow_steps(b, 0, 10, 14, 10)
    parts.front_door(b, 5, 2, 4, 'north', wood='dark_oak', step='stone_brick_stairs', lamps=False)
    # Bookshelves line the ground floor.
    for z in range(5, 14):
        for x in (2, 8):
            if (x == 2 and z == 7) or (x == 8 and z in (7, 8, 9, 11)):
                continue
            for y in (2, 3, 4):
                b.set(x, y, z, 'bookshelf')
    for x in range(3, 8):
        for y in (2, 3, 4):
            b.set(x, y, 13, 'bookshelf')
    b.set(5, 4, 13, 'chiseled_bookshelf', facing='north')
    b.custom(5, 2, 12, 'archives', facing='north')
    b.set(4, 2, 9, 'lectern', facing='north', has_book=False, powered=False)
    parts.table(b, 5, 2, 7, wood='dark_oak')
    parts.chair(b, 4, 2, 7, 'west', wood='dark_oak')
    parts.chair(b, 6, 2, 7, 'east', wood='dark_oak')
    cp.fireplace(b, 8, 2, 8, 'west', ridge - 3)
    parts.rug(b, 3, 8, 6, 11, 2, 'blue', border='light_blue')
    cp.hang(b, 5, 5, 8)
    cp.hang(b, 4, 5, 11)
    parts.stair_run(b, 7, 12, 2, 5, 'north', wood='dark_oak')
    b.resident(5, 2, 10, 'scholar')
    # Upper floor: reading gallery and the scholar's room.
    for x in range(2, 9):
        for y in (7, 8, 9):
            if x != 7:
                b.set(x, y, 10, 'dark_oak_planks')
    for z in range(11, 14):
        for y in (7, 8, 9):
            b.set(7, y, z, 'dark_oak_planks')
    b.door(4, 7, 10, facing='south', wood='dark_oak')
    b.bed(3, 7, 13, 'north', 'blue')
    b.chest(5, 7, 13, 'north', loot=LOOT)
    b.set(6, 7, 13, 'bookshelf')
    b.set(6, 8, 13, 'bookshelf')
    b.set(2, 7, 11, 'candle', candles=3, lit=True, waterlogged=False)
    cp.hang(b, 4, 9, 12)
    b.room('scholar_bedroom', (5, 8, 12))
    for x in (2, 3):
        for y in (7, 8):
            b.set(x, y, 5, 'bookshelf')
    parts.table(b, 5, 7, 6, wood='dark_oak')
    b.set(5, 8, 6, 'candle', candles=2, lit=True, waterlogged=False)
    cp.hang(b, 5, 9, 8)
    b.set(2, 7, 8, 'lectern', facing='east', has_book=False, powered=False)
    # Tall narrow windows.
    for x in (3, 7):
        cp.window(b, x, 2, 4, 'north', height=2, shutters=False, sill='stone_brick')
        cp.window(b, x, 7, 4, 'north', height=2, shutters=False)
    for z in (6, 10):
        cp.window(b, 1, 2, z, 'west', height=2, shutters=False)
        cp.window(b, 9, 7, z + 1, 'east', height=2, shutters=False)
    cp.window(b, 1, 7, 8, 'west', height=2, shutters=False)
    for y in range(11, 14):
        b.set(5, y, 4, 'glass_pane')
    b.set(5, 12, 14, 'glass_pane')
    # Front steps, lamps and a snowy yard with spruce bushes.
    for z in range(0, 3):
        b.set(5, 0, z, 'stone_bricks' if z % 2 else 'polished_andesite')
    for x in (3, 7):
        cp.lamp_post(b, x, 2, height=2, fence='dark_oak_fence', base='stone_bricks')
    plaque(b, 4, 3)
    for x, z in ((1, 2), (9, 2), (0, 5), (10, 9)):
        b.set(x, 0, z, 'podzol')
        cp.bush(b, x, 1, z)
    for x in range(0, 11):
        for z in range(0, 4):
            if (x, 0, z) not in b.grid and rng.random() < .6:
                b.set(x, 0, z, 'snow_block' if rng.random() < .7 else 'gravel')
    b.entrance(5)
    b.natural_ground()
    return b


DESIGNS = {
    'snowy/tavern': tavern,
    'snowy/garrison': garrison,
    'snowy/workshop': workshop,
    'snowy/chapel': chapel,
    'snowy/apothecary': apothecary,
    'snowy/library': library,
}
