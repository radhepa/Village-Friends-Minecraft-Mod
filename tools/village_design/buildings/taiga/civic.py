"""Taiga civic buildings that face the town square (one of each per village).

Same roles, residents and workstations as the plains civic buildings, built as
a forest lodge village: horizontal log cabins with crossed corners on mossy
stone plinths, steep mossy roofs, log-post porches, a palisade fort and a stave
church. Large slots are up to 17 wide (8 either side of the entrance), small
slots up to 11 wide (5 either side).
"""
import random

from ...kit import Build
from ... import parts
from ..civic import grave
from ..plazas import stall
from . import core_parts as T
from .palette import ROOFS

LOOT = T.LOOT_HOUSE


def plaque(b, x, z, facing='north', y=1):
    b.custom(x, y, z, 'house_plaque', facing=facing)


def win(b, x, y, z, out, height=1, width=1, shutters=True):
    parts.window(b, x, y, z, out, height=height, width=width, trim='spruce', shutters=shutters)


# -------------------------------------------------------------------- tavern
def tavern():
    """The Antler Lodge: the village's tavern, a steep A-frame log lodge facing the square.

    An open deck with trestle tables on the square; a log great hall with a mossy stone hearth and
    fireside armchairs, two long tables, a square table and an old fence table, the bar along the east
    wall with stools and room to stand, and the bard's dais with its note block; the kitchen wing
    behind; two guest rooms upstairs; a yard with wood, kegs and a hide rack.

    Tavern furniture faces the way its sitter faces; stair chairs face their backrest side.
    """
    rng = random.Random(4301)
    seed = 4301
    b = Build('taiga/tavern', (17, 28, 29))
    # Kitchen wing behind the hall (drawn first so the hall's back wall overwrites the shared wall).
    kx0, kz0, kx1, kz1 = 8, 21, 14, 27
    T.plinth(b, kx0, kz0, kx1, kz1, floor='cobblestone', seed=seed)
    T.log_walls(b, kx0, kz0, kx1, kz1, 2, 5)
    T.ceiling(b, kx0 + 1, kz0 + 1, kx1 - 1, kz1 - 1, 6)
    T.roof(b, kx0, kz0, kx1, kz1, 5, 'dark_oak', axis='z', pitch=1, rake=(0, 1), gable='spruce_planks',
           seed=seed + 1, finials=False)
    # The great hall: log walls x 1..15, z 6..21; common room on Y=1, guest rooms on Y=6.
    x0, z0, x1, z1 = 1, 6, 15, 21
    T.plinth(b, x0, z0, x1, z1, seed=seed)
    T.log_walls(b, x0, z0, x1, z1, 2, 9)
    T.ceiling(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, 6)
    T.ceiling(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, 10)
    ridge = T.roof(b, x0, z0, x1, z1, 9, 'dark_oak', axis='z', pitch=2, gable='stripped_spruce_log[axis=x]',
                   seed=seed, moss=.3)
    _lodge_facade(b, ridge)
    _lodge_deck(b, rng)
    _lodge_hearth(b)
    _lodge_common_room(b)
    _lodge_bar(b)
    _lodge_kitchen(b)
    _lodge_upstairs(b)
    _lodge_yard(b, rng)
    b.entrance(8)
    b.natural_ground()
    return b


def _lodge_facade(b, ridge):
    """Front gable with a tall window and antler horns, windows all round, the stone chimney stack."""
    parts.front_door(b, 8, 2, 6, 'north', wood='spruce', step='mossy_cobblestone_stairs', lamps=False)
    # A log-post canopy over the door only, so the deck's seats stay under open sky.
    for x in (7, 9):
        T.log_post(b, x, 4, 1, 4)
    for x, f in ((6, 'east'), (7, 'east'), (8, None), (9, 'west'), (10, 'west')):
        for z in (3, 4, 5):
            if f:
                b.set(x, 5, z, 'dark_oak_stairs', facing=f, half='bottom')
            else:
                b.set(x, 6, z, 'dark_oak_slab', type='bottom', waterlogged=False)
                b.set(x, 5, z, 'dark_oak_planks')
    b.set(8, 4, 3, 'spruce_hanging_sign', rotation=8, attached=False, waterlogged=False)
    T.hang_lantern(b, 8, 4, 5)
    plaque(b, 10, 5)
    for x in (3, 12):
        win(b, x, 3, 6, 'north', height=2, width=2, shutters=True)
    for x in (3, 5, 11, 13):
        win(b, x, 8, 6, 'north', shutters=True)
    for y in range(11, 16):
        for x in (7, 8, 9):
            if y < 15 or x == 8:
                b.set(x, y, 6, 'glass_pane')
    b.set(8, 10, 5, 'green_wall_banner', facing='north')
    for z in (8, 18):
        win(b, 1, 3, z, 'west', height=2, width=2)
    for z in (9, 18):
        win(b, 1, 8, z, 'west')
    for z in (8, 19):
        win(b, 15, 8, z, 'east')
    win(b, 15, 3, 7, 'east', height=2)
    win(b, 15, 8, 13, 'east', width=2)
    # Antlers over the door: spruce trapdoor tines either side of a log boss.
    b.set(8, 9, 5, 'stripped_spruce_log', axis='z')
    for x, f in ((7, 'west'), (9, 'east')):
        b.set(x, 9, 5, 'spruce_trapdoor', facing=f, half='top', open=True, powered=False, waterlogged=False)
        b.set(x, 10, 5, 'spruce_fence')
    # The hearth's mossy stone chimney climbs the outside of the west wall.
    for z in range(12, 17):
        for y in range(0, 6):
            b.set(0, y, z, 'mossy_cobblestone' if (y + z) % 3 == 0 else 'cobblestone')
    b.set(0, 6, 12, 'cobblestone_stairs', facing='south', half='bottom')
    b.set(0, 6, 16, 'cobblestone_stairs', facing='north', half='bottom')
    for z in range(13, 16):
        for y in range(6, 14):
            b.set(0, y, z, 'cobblestone' if (y + z) % 4 else 'mossy_cobblestone')
    b.set(0, 14, 13, 'cobblestone_wall')
    b.set(0, 14, 14, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    b.set(0, 14, 15, 'cobblestone_wall')


def _lodge_deck(b, rng):
    """Open deck on the square: two trestle tables with benches under the sky, a log rail and lanterns."""
    for x in range(1, 16):
        for z in range(1, 6):
            b.set(x, 0, z, 'spruce_planks' if z > 1 else 'stripped_spruce_log', axis='x')
    for z in range(0, 6):
        b.set(8, 0, z, 'mossy_cobblestone' if z % 2 == 0 else 'gravel')
    for x in (7, 9):
        b.set(x, 0, 0, 'coarse_dirt')
    for x0 in (2, 12):
        for x in (x0, x0 + 1):
            b.custom(x, 1, 3, 'tavern_table')
            b.custom(x, 1, 2, 'village_bench', facing='south')
            b.custom(x, 1, 4, 'village_bench', facing='north')
    for z in range(1, 6):
        for x in (1, 15):
            b.set(x, 1, z, 'spruce_fence')
    for x in (1, 15):
        T.lamp(b, x, 1, height=2)
    for x in (5, 11):
        T.lamp(b, x, 1, height=2)
    # Berry boxes and ferns along the front edge.
    for x in list(range(1, 7)) + list(range(10, 16)):
        if b.get(x, 1, 0)[0] != 'minecraft:air':
            continue
        b.set(x, 0, 0, 'podzol')
        b.set(x, 1, 0, rng.choice(['sweet_berry_bush[age=3]', 'fern', 'fern', 'short_grass']))


def _lodge_hearth(b):
    """The big stone fireplace in the west wall, with armchairs facing the fire and settles either side."""
    for z in range(12, 17):
        for y in range(1, 6):
            b.set(1, y, z, 'mossy_stone_bricks' if (y + z) % 3 else 'cobblestone')
        b.set(2, 1, z, 'cobblestone')
    for z in range(13, 16):
        b.set(1, 2, z, 'air')
        b.set(1, 3, z, 'air')
        b.set(1, 4, z, 'stripped_spruce_log', axis='z')
    b.set(1, 2, 14, 'campfire', lit=True, signal_fire=False, facing='east', waterlogged=False)
    for z in (13, 15):
        b.set(1, 2, z, 'spruce_log', axis='x')
    for z in range(12, 17):
        b.set(2, 4, z, 'spruce_slab', type='top', waterlogged=False)
    b.set(2, 5, 12, 'candle', candles=3, lit=True, waterlogged=False)
    b.set(2, 5, 16, 'candle', candles=2, lit=True, waterlogged=False)
    # Antlers over the mantel.
    for z, f in ((13, 'north'), (15, 'south')):
        b.set(1, 5, z, 'stripped_spruce_log', axis='z')
        b.set(2, 5, z, 'spruce_trapdoor', facing='east', half='top', open=True, powered=False, waterlogged=False)
    # A bear-brown rug laid into the floor (wool, so it stays walkable).
    for x in (3, 4):
        for z in range(12, 17):
            b.set(x, 1, z, 'brown_wool' if x == 3 and 13 <= z <= 15 else 'green_wool')
    for z in (13, 15):
        b.custom(3, 2, z, 'fireside_armchair', facing='west')
    b.barrel(3, 2, 14, 'up')
    b.set(3, 3, 14, 'candle', candles=1, lit=True, waterlogged=False)
    for x in (2, 3):
        b.custom(x, 2, 11, 'village_bench', facing='south')
        b.custom(x, 2, 17, 'village_bench', facing='north')


def _lodge_common_room(b):
    """Long tables, a square table, the fence table, the bard's dais, beams, chandelier and the stairs."""
    for zs in (8, 13):
        for z in range(zs, zs + 3):
            b.custom(6, 2, z, 'tavern_table')
            b.custom(5, 2, z, 'tavern_chair', facing='east')
            b.custom(7, 2, z, 'tavern_chair', facing='west')
    b.custom(3, 2, 19, 'tavern_table')
    for x, z, f in ((2, 19, 'east'), (4, 19, 'west'), (3, 18, 'south'), (3, 20, 'north')):
        b.custom(x, 2, z, 'tavern_chair', facing=f)
    parts.table(b, 6, 2, 18, wood='spruce')
    for x, z, back in ((5, 18, 'west'), (7, 18, 'east'), (6, 17, 'north'), (6, 19, 'south')):
        parts.chair(b, x, 2, z, back, wood='spruce')
    # The bard's dais in the north-west corner, a note block to play beside.
    for x in (2, 3):
        for z in (7, 8):
            b.set(x, 2, z, 'spruce_planks' if (x, z) != (3, 8) else 'green_wool')
        b.set(x, 2, 9, 'spruce_slab', type='bottom', waterlogged=False)
    b.set(2, 3, 7, 'note_block', instrument='bass', note=0, powered=False)
    b.set(3, 5, 7, 'green_wall_banner', facing='south')
    b.set(3, 5, 8, 'lantern', hanging=True, waterlogged=False)
    # Log beams, lanterns and an antler chandelier over the long tables.
    for z in (9, 15, 18):
        for x in range(2, 15):
            if b.get(x, 5, z)[0] == 'minecraft:air':
                b.set(x, 5, z, 'stripped_spruce_log', axis='x')
    for x, z in ((9, 9), (9, 15), (9, 18), (12, 15)):
        b.set(x, 4, z, 'lantern', hanging=True, waterlogged=False)
    for x, z in ((5, 12), (6, 12), (7, 12), (6, 11), (6, 13)):
        b.set(x, 5, z, 'spruce_fence')
    for x, z in ((5, 12), (7, 12), (6, 11), (6, 13)):
        b.set(x, 4, z, 'lantern', hanging=True, waterlogged=False)
    parts.stair_run(b, 7, 20, 2, 5, 'east', wood='spruce')
    b.barrel(4, 2, 7, 'up')
    b.set(4, 3, 7, 'potted_fern')


def _lodge_bar(b):
    """The bar along the east wall: a log counter with five stools, the keeper's well half a step down."""
    for z in range(9, 18):
        b.set(12, 2, z, 'stripped_spruce_log', axis='z')
    b.set(12, 2, 18, 'spruce_log', axis='y')
    b.set(12, 3, 18, 'lantern', hanging=False, waterlogged=False)
    for z in (9, 11, 13, 15, 17):
        b.custom(11, 2, z, 'bar_stool', facing='east')
    for z in range(9, 21):
        b.set(13, 1, z, 'spruce_slab', type='bottom', waterlogged=False)
    b.barrel(13, 2, 8, 'west')
    b.barrel(14, 2, 8, 'west')
    b.barrel(14, 2, 7, 'up')
    b.barrel(13, 2, 7, 'west')
    b.custom(14, 2, 13, 'tap_stand', facing='west')
    b.custom(14, 2, 14, 'drinks_barrel', facing='west')
    for z in (9, 10, 11, 12, 18, 19, 20):
        b.barrel(14, 2, z, 'west')
    for z in (10, 12, 19):
        b.barrel(14, 3, z, 'west')
    b.set(14, 3, 11, 'brewing_stand', has_bottle_0=False, has_bottle_1=False, has_bottle_2=False)
    b.chest(14, 2, 15, 'west')
    b.set(14, 2, 16, 'barrel', facing='up', open=False)
    b.set(14, 2, 17, 'water_cauldron', level=3)
    for z in (10, 11, 12, 19, 20):
        b.set(14, 4, z, 'spruce_trapdoor', facing='west', half='top', open=False, powered=False, waterlogged=False)
    for z, item in ((10, 'candle'), (11, 'potted_fern'), (12, 'candle'), (19, 'potted_red_mushroom'),
                    (20, 'candle')):
        if item == 'candle':
            b.set(14, 5, z, 'candle', candles=3 if z % 2 else 2, lit=True, waterlogged=False)
        else:
            b.set(14, 5, z, item)
    b.set(14, 4, 13, 'green_wall_banner', facing='west')
    b.set(14, 4, 14, 'brown_wall_banner', facing='west')
    for z in (10, 13, 16):
        b.set(13, 5, z, 'hanging_roots', waterlogged=False)
    b.resident(13, 2, 14, 'tavern_keeper')
    # Serving hatch and door to the kitchen at the end of the well.
    b.set(12, 2, 21, 'spruce_stairs', facing='north', half='top', waterlogged=False, lock=True)
    b.set(12, 3, 21, 'air')
    b.door(13, 2, 21, facing='north', wood='spruce')


def _lodge_kitchen(b):
    """The cook's kitchen: stove and smoker under a stone hood, prep table, pantry and water."""
    b.custom(11, 2, 26, 'kitchen_stove', facing='north')
    b.set(12, 2, 26, 'smoker', facing='north', lit=True)
    b.set(10, 2, 26, 'water_cauldron', level=3)
    for x in (11, 12):
        b.set(x, 4, 26, 'mossy_cobblestone')
        b.set(x, 5, 26, 'cobblestone')
    parts.chimney(b, 11, 26, 6, 12, 'cobblestone')
    b.set(9, 2, 22, 'crafting_table')
    b.barrel(9, 2, 23, 'east')
    b.barrel(9, 3, 23, 'east')
    b.barrel(9, 2, 26, 'up')
    b.set(9, 3, 26, 'hay_block', axis='y')
    b.barrel(10, 2, 22, 'south')
    b.set(13, 2, 24, 'smooth_stone_slab', type='double')
    b.set(13, 2, 25, 'smooth_stone_slab', type='double')
    b.set(13, 3, 24, 'potted_brown_mushroom')
    b.set(13, 2, 26, 'composter', level=4)
    for x, z in ((10, 23), (12, 24)):
        b.set(x, 5, z, 'hanging_roots', waterlogged=False)
    T.hang_lantern(b, 11, 5, 24)
    b.resident(11, 2, 24, 'cook')
    parts.front_door(b, 8, 2, 24, 'west', wood='spruce', step='cobblestone_stairs', lamps=False)
    win(b, 14, 3, 24, 'east')
    win(b, 10, 3, 27, 'south')


def _lodge_upstairs(b):
    """Two guest rooms on the west side, a landing and linen store on the east."""
    for z in range(7, 21):
        for y in (7, 8, 9):
            b.set(8, y, z, 'spruce_planks')
    for x in range(2, 8):
        for y in (7, 8, 9):
            b.set(x, y, 14, 'spruce_planks')
    b.door(8, 7, 10, facing='east', wood='spruce')
    b.door(8, 7, 17, facing='east', wood='spruce', hinge='right')
    for x in (9, 10):
        b.set(x, 7, 19, 'spruce_fence')
    b.bed(3, 7, 9, 'west', 'green')
    b.bed(3, 7, 12, 'west', 'brown')
    b.chest(2, 7, 10, 'east', loot=LOOT)
    b.set(2, 7, 11, 'barrel', facing='up', open=False)
    parts.table(b, 6, 7, 8, wood='spruce')
    parts.rug(b, 4, 10, 6, 12, 7, 'brown', border='green')
    T.hang_lantern(b, 5, 9, 10)
    b.room('guest_room_north', (5, 8, 11))
    b.bed(3, 7, 16, 'west', 'brown')
    b.bed(3, 7, 19, 'west', 'green')
    b.chest(2, 7, 17, 'east', loot=LOOT)
    b.set(2, 7, 18, 'barrel', facing='up', open=False)
    parts.table(b, 6, 7, 20, wood='spruce')
    parts.rug(b, 4, 16, 6, 18, 7, 'white', border='brown')
    T.hang_lantern(b, 5, 9, 17)
    b.room('guest_room_south', (5, 8, 17))
    for z in (7, 8):
        b.barrel(14, 7, z, 'west')
    b.set(14, 8, 7, 'white_wool')
    b.chest(13, 7, 7, 'south')
    parts.rug(b, 10, 10, 13, 15, 7, 'green', border='brown')
    T.hang_lantern(b, 11, 9, 9)
    T.hang_lantern(b, 11, 9, 16)


def _lodge_yard(b, rng):
    """Back yard by the kitchen door: woodpile, kegs, hay, a chopping block and a hide rack."""
    for x in range(1, 8):
        for z in range(22, 29):
            if rng.random() < .65:
                b.set(x, 0, z, rng.choice(['coarse_dirt', 'podzol', 'dirt_path', 'gravel']))
    T.woodstack(b, 2, 22, 'x', length=4, height=2)
    T.chopping_block(b, 5, 25)
    for x, z, f in ((1, 26, 'east'), (1, 27, 'east'), (2, 27, 'north')):
        b.barrel(x, 1, z, f)
    b.barrel(1, 2, 27, 'up')
    for x, z in ((6, 27), (6, 28), (5, 28)):
        b.set(x, 1, z, 'hay_block', axis='y')
    for x in range(9, 15):
        if x % 2:
            b.barrel(x, 1, 28, 'up')


# ------------------------------------------------------------------ garrison
def palisade(b, x0, z0, x1, z1, rng, skip=()):
    """Sharpened log palisade on a rubble footing along a straight run."""
    for x, z in parts.along(x0, z0, x1, z1):
        if (x, z) in skip:
            continue
        b.set(x, 0, z, 'mossy_cobblestone' if rng.random() < .5 else 'cobblestone')
        h = 4 if (x + z) % 2 else 5
        for y in range(1, h + 1):
            b.set(x, y, z, 'spruce_log', axis='y')
        b.set(x, h + 1, z, 'spruce_fence')


def garrison():
    """Palisade fort: a jettied log blockhouse, a log watchtower and a fenced training yard."""
    rng = random.Random(4302)
    seed = 4302
    b = Build('taiga/garrison', (17, 22, 22))
    # Training yard ground.
    for x in range(1, 16):
        for z in range(1, 12):
            b.set(x, 0, z, 'gravel' if rng.random() < .4 else rng.choice(['coarse_dirt', 'dirt_path', 'podzol',
                                                                        'coarse_dirt']))
    for z in range(0, 12):
        b.set(8, 0, z, 'dirt_path' if z % 3 else 'gravel')
    # Palisade: front with a gate, both flanks back to the blockhouse.
    gate = {(x, 1) for x in range(7, 10)}
    palisade(b, 0, 1, 16, 1, rng, skip=gate)
    palisade(b, 0, 2, 0, 12, rng)
    palisade(b, 16, 2, 16, 12, rng)
    for x in (1, 2, 14, 15):
        palisade(b, x, 12, x, 12, rng)
    # Gate: tall posts, lintel and a fenced walk.
    for x in (6, 10):
        for y in range(1, 8):
            b.set(x, y, 1, 'spruce_log', axis='y')
        b.set(x, 8, 1, 'spruce_fence')
        b.set(x, 5, 0, 'green_wall_banner', facing='north')
    for x in range(7, 10):
        b.set(x, 5, 1, 'stripped_spruce_log', axis='x')
        b.set(x, 6, 1, 'spruce_fence')
    b.set(7, 4, 1, 'spruce_stairs', facing='east', half='top', lock=True)
    b.set(9, 4, 1, 'spruce_stairs', facing='west', half='top', lock=True)
    T.hang_lantern(b, 8, 4, 1)
    plaque(b, 5, 2)
    # Watchtower in the yard's front corner.
    tx0, tz0, tx1, tz1 = 12, 2, 15, 5
    for x in range(tx0, tx1 + 1):
        for z in range(tz0, tz1 + 1):
            b.set(x, 0, z, 'mossy_cobblestone')
    T.log_walls(b, tx0, tz0, tx1, tz1, 1, 8)
    b.fill(tx0 + 1, 9, tz0 + 1, tx1 - 1, 9, tz1 - 1, 'spruce_planks')
    T.beam_course(b, tx0, tz0, tx1, tz1, 9)
    for y in range(1, 10):
        b.set(14, y, 4, 'ladder', facing='west', waterlogged=False)
    b.door(tx0, 1, 3, facing='east', wood='spruce')
    b.set(11, 0, 3, 'dirt_path')
    for x, z in ((tx0, tz0), (tx1, tz0), (tx0, tz1), (tx1, tz1)):
        for y in (10, 11, 12):
            b.set(x, y, z, 'spruce_log', axis='y')
    for x in range(tx0, tx1 + 1):
        for z in range(tz0, tz1 + 1):
            if (x in (tx0, tx1) or z in (tz0, tz1)) and b.get(x, 10, z)[0] == 'minecraft:air':
                b.set(x, 10, z, 'spruce_fence')
    T.hang_lantern(b, 13, 12, 3)
    T.roof(b, tx0, tz0, tx1, tz1, 13, 'spruce', axis='x', pitch=2, gable='spruce_planks', seed=seed + 5,
           overhang=1, rake=1)
    for y in (5, 6):
        b.set(tx0, y, 4, 'glass_pane')
        b.set(tx1, y, 3, 'glass_pane')
    b.set(13, 7, tz0, 'glass_pane')
    b.set(13, 7, 1, 'green_wall_banner', facing='north')
    # Blockhouse barracks: log ground floor, overhanging upper floor, steep roof.
    x0, z0, x1, z1 = 3, 13, 13, 19
    T.plinth(b, x0, z0, x1, z1, seed=seed)
    T.log_walls(b, x0, z0, x1, z1, 2, 5)
    T.ceiling(b, x0, z0, x1, z1, 6)
    T.beam_course(b, x0 - 1, z0 - 1, x1 + 1, z1 + 1, 6)
    for x in range(x0, x1 + 1, 3):
        b.set(x, 5, z0 - 1, 'spruce_stairs', facing='south', half='top', lock=True)
        b.set(x, 5, z1 + 1, 'spruce_stairs', facing='north', half='top', lock=True)
    for z in range(z0 + 1, z1, 3):
        b.set(x0 - 1, 5, z, 'spruce_stairs', facing='east', half='top', lock=True)
        b.set(x1 + 1, 5, z, 'spruce_stairs', facing='west', half='top', lock=True)
    T.log_walls(b, x0 - 1, z0 - 1, x1 + 1, z1 + 1, 7, 9)
    T.ceiling(b, x0, z0, x1, z1, 10)
    T.roof(b, x0 - 1, z0 - 1, x1 + 1, z1 + 1, 9, 'dark_oak', axis='x', pitch=2,
           gable='stripped_spruce_log[axis=z]', seed=seed)
    parts.front_door(b, 8, 2, z0, 'north', wood='spruce', step='cobblestone_stairs', lamps=True)
    for x in (5, 11):
        win(b, x, 3, z0, 'north', shutters=False)
    win(b, x0, 3, 15, 'west')
    win(b, x1, 3, 16, 'east')
    for x in (4, 7, 10):
        b.set(x, 8, z0 - 1, 'glass_pane')
        b.set(x, 8, z1 + 1, 'glass_pane')
    for z in (14, 17):
        b.set(x0 - 1, 8, z, 'glass_pane')
        b.set(x1 + 1, 8, z, 'glass_pane')
    # Guard office and armoury below.
    b.custom(5, 2, 15, 'command_desk', facing='east')
    parts.chair(b, 4, 2, 15, 'west')
    b.chest(4, 2, 18, 'east', loot='minecraft:chests/village/village_weaponsmith')
    b.set(5, 2, 18, 'anvil', facing='east')
    b.barrel(9, 2, 18, 'up')
    b.barrel(10, 2, 18, 'up')
    b.set(10, 3, 18, 'barrel', facing='up', open=False)
    b.custom(9, 2, 15, 'training_dummy', facing='west')
    T.hang_lantern(b, 6, 5, 16)
    T.hang_lantern(b, 10, 5, 16)
    parts.stair_run(b, 12, 14, 2, 5, 'south', wood='spruce')
    # Bunk room above, behind a partition.
    for z in range(z0, z1 + 1):
        for y in (7, 8, 9):
            b.set(11, y, z, 'spruce_planks')
    b.door(11, 7, 14, facing='west', wood='spruce')
    for x in (3, 5, 7, 9):
        b.bed(x, 7, 18, 'south', 'green' if x % 4 == 1 else 'brown')
    b.chest(4, 7, 13, 'south', loot=LOOT)
    b.set(10, 7, 13, 'crafting_table')
    T.hang_lantern(b, 6, 9, 15)
    b.room('bunk_room', (7, 8, 15))
    # Yard: dummies, targets, a rack and the forge corner.
    for x, z in ((3, 4), (3, 7), (6, 6)):
        b.custom(x, 1, z, 'training_dummy', facing='south')
    for z in (8, 9):
        b.custom(1, 1, z, 'archery_target', facing='east')
    for x, z in ((1, 10), (2, 10), (1, 11)):
        b.set(x, 1, z, 'hay_block', axis='y')
    b.set(13, 1, 9, 'grindstone', face='floor', facing='north')
    b.set(14, 1, 9, 'smithing_table')
    b.barrel(15, 1, 9, 'up')
    for x in (11, 12):
        b.set(x, 1, 7, 'spruce_fence')
    b.set(11, 2, 7, 'spruce_trapdoor', facing='north', half='top', open=True, powered=False, waterlogged=False)
    b.set(10, 1, 8, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    b.custom(10, 1, 9, 'campfire_bench', facing='north')
    b.custom(9, 1, 8, 'campfire_bench', facing='east')
    T.lamp(b, 5, 11)
    b.resident(5, 1, 5, 'knight')
    b.resident(4, 1, 9, 'archer')
    b.entrance(8)
    b.natural_ground()
    return b


# ------------------------------------------------------------------ workshop
def workshop():
    """Loom house and sawmill shed: the tailor's log cabin beside the carpenter's open lumber shed."""
    rng = random.Random(4303)
    seed = 4303
    b = Build('taiga/workshop', (17, 21, 19))
    x0, z0, x1, z1 = 1, 6, 9, 14
    T.plinth(b, x0, z0, x1, z1, seed=seed)
    T.log_walls(b, x0, z0, x1, z1, 2, 9, chink=False)
    T.ceiling(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, 6)
    T.ceiling(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, 10)
    T.roof(b, x0, z0, x1, z1, 9, 'spruce', axis='z', pitch=2, gable='stripped_spruce_log[axis=x]', seed=seed)
    parts.front_door(b, 5, 2, z0, 'north', wood='spruce', step='mossy_cobblestone_stairs', lamps=True)
    win(b, 2, 3, z0, 'north', height=2, width=2)
    win(b, 7, 3, z0, 'north', height=2)
    for x in (3, 4, 6, 7):
        b.set(x, 8, z0, 'glass_pane')
    for z in (12, 13):
        b.set(5, 12, z0, 'glass_pane') if z == 12 else None
    win(b, x0, 3, 8, 'west', height=2, width=2)
    win(b, x0, 3, 12, 'west', height=2)
    win(b, x0, 8, 9, 'west')
    win(b, x0, 8, 12, 'west')
    win(b, 5, 8, z1, 'south')
    # Tailor's shop.
    b.custom(3, 2, 12, 'sewing_table', facing='north')
    b.set(2, 2, 10, 'loom', facing='east')
    for z, c in zip(range(8, 14), ['green', 'brown', 'white', 'light_gray', 'red', 'cyan']):
        b.set(2, 2, z, f'{c}_wool') if z not in (10, 12) else None
    for z, c in ((8, 'green'), (9, 'brown'), (11, 'white'), (13, 'red')):
        b.set(2, 3, z, f'{c}_carpet')
    parts.rug(b, 4, 9, 6, 11, 2, 'brown', border='green')
    b.chest(4, 2, 13, 'north', loot=LOOT)
    T.hang_lantern(b, 5, 5, 10)
    b.resident(5, 2, 12, 'tailor')
    parts.stair_run(b, 8, 7, 2, 5, 'south', wood='spruce')
    # Bedroom upstairs behind a partition that closes the stairwell.
    for z in range(z0 + 1, z1):
        for y in (7, 8, 9):
            b.set(7, y, z, 'spruce_planks')
    b.door(7, 7, 12, facing='west', wood='spruce')
    b.bed(3, 7, 12, 'south', 'green')
    b.bed(5, 7, 12, 'south', 'brown')
    b.chest(2, 7, 7, 'east', loot=LOOT)
    b.set(6, 7, 7, 'barrel', facing='up', open=False)
    T.hang_lantern(b, 4, 9, 10)
    b.room('bedroom', (4, 8, 9))
    # The carpenter's lumber shed, its lean-to roof rising toward the cabin.
    for x, z in ((16, 4), (16, 10), (16, 16), (13, 4), (13, 16), (11, 4), (11, 16)):
        b.set(x, 0, z, 'mossy_cobblestone')
        for y in range(1, 5 + (16 - x)):
            b.set(x, y, z, 'spruce_log', axis='y')
    T.lean_to_x(b, 3, 17, 16, 10, 5 + 0, kind='spruce', seed=seed + 3)
    for x in range(11, 17):
        for z in range(4, 17):
            if b.get(x, 0, z)[0] == 'minecraft:air':
                b.set(x, 0, z, 'spruce_planks' if (x + z) % 3 else 'stripped_spruce_log', axis='x')
    b.custom(13, 1, 9, 'sawmill', facing='west')
    b.set(13, 1, 12, 'crafting_table')
    b.resident(12, 1, 10, 'carpenter')
    T.woodstack(b, 15, 5, 'z', length=4, height=3)
    T.woodstack(b, 15, 12, 'z', length=3, height=2)
    for z in (13, 15):
        b.set(13, 1, z, 'spruce_fence')
    for z in range(13, 16):
        b.set(13, 2, z, 'stripped_spruce_log', axis='z')
    b.set(12, 1, 6, 'spruce_planks')
    b.set(12, 2, 6, 'spruce_slab', type='bottom')
    b.barrel(14, 1, 15, 'up')
    T.chopping_block(b, 12, 14)
    T.hang_lantern(b, 13, 7, 10)
    # Front yard: path, berry boxes and the plaque.
    for z in range(0, 5):
        b.set(8, 0, z, 'dirt_path' if z % 3 else 'coarse_dirt')
    for x in range(5, 9):
        b.set(x, 0, 4, 'dirt_path')
    b.set(5, 0, 5, 'dirt_path')
    for x in range(1, 5):
        for z in range(1, 4):
            b.set(x, 0, z, 'podzol' if rng.random() < .5 else 'grass_block')
            b.set(x, 1, z, rng.choice(['sweet_berry_bush[age=3]', 'fern', 'fern', 'short_grass']))
    plaque(b, 7, 3)
    T.lamp(b, 10, 2)
    b.entrance(8)
    b.natural_ground()
    return b


# -------------------------------------------------------------------- chapel
def chapel():
    """Stave church: an ambulatory skirt roof, a steep staved nave, a belfry spire and a mossy graveyard."""
    rng = random.Random(4304)
    seed = 4304
    b = Build('taiga/chapel', (17, 30, 21))
    gx0, gz0, gx1, gz1 = 3, 5, 13, 17
    T.plinth(b, gx0, gz0, gx1, gz1, floor='dark_oak_planks', seed=seed)
    # Ambulatory walls: plank dado with an arcade of fences between posts.
    for x, z, facing, corner in parts.ring(gx0, gz0, gx1, gz1):
        post = corner or (x - gx0) % 2 == 0 and facing in ('north', 'south') or (z - gz0) % 2 == 0 and \
            facing in ('east', 'west')
        if post:
            for y in (2, 3):
                b.set(x, y, z, 'dark_oak_log', axis='y')
        else:
            b.set(x, 2, z, 'dark_oak_planks')
            b.set(x, 3, z, 'dark_oak_fence')
    # Nave of upright staves.
    nx0, nz0, nx1, nz1 = 5, 7, 11, 15
    T.stave_walls(b, nx0, nz0, nx1, nz1, 2, 9)
    # Skirt roof round the ambulatory.
    for k, y in ((0, 4), (1, 5), (2, 6)):
        lx, hx, lz, hz = gx0 - 1 + k, gx1 + 1 - k, gz0 - 1 + k, gz1 + 1 - k
        for x, z, facing, corner in parts.ring(lx, lz, hx, hz):
            f = {'north': 'south', 'south': 'north', 'west': 'east', 'east': 'west'}[facing]
            if corner:
                f = 'south' if z == lz else 'north'
            b.set(x, y, z, 'dark_oak_stairs', facing=f, half='bottom')
    T.mossify(b, (gx0 - 1, 4, gz0 - 1, gx1 + 1, 6, gz1 + 1), seed + 1, .25)
    ridge = T.roof(b, nx0, nz0, nx1, nz1, 9, 'dark_oak', axis='z', pitch=2, gable='dark_oak_planks', seed=seed,
                   finials=False)
    # Dragon-head finials: upturned stairs at both ends of the ridge.
    for z, f in ((nz0 - 1, 'south'), (nz1 + 1, 'north')):
        b.set(8, ridge + 1, z, 'dark_oak_fence')
        b.set(8, ridge + 2, z, 'dark_oak_stairs', facing=f, half='top', lock=True)
    # Belfry tower rising through the ridge, with a skirt roof and a spire.
    for y in range(10, 20):
        for x in range(7, 10):
            for z in range(10, 13):
                edge = x in (7, 9) or z in (10, 12)
                corner = x in (7, 9) and z in (10, 12)
                if y == 10 and not edge:
                    b.set(x, y, z, 'dark_oak_planks')
                elif y >= 17 and edge and not corner:
                    b.set(x, y, z, 'air')
                elif edge:
                    b.set(x, y, z, 'dark_oak_log' if corner or (x + z) % 2 else 'stripped_dark_oak_log', axis='y')
                else:
                    b.set(x, y, z, 'air')
    for x in range(6, 11):
        for z in range(9, 14):
            if x in (6, 10) or z in (9, 13):
                f = 'south' if z == 9 else 'north' if z == 13 else 'east' if x == 6 else 'west'
                b.set(x, 16, z, 'dark_oak_stairs', facing=f, half='bottom')
    b.fill(7, 20, 10, 9, 20, 12, 'dark_oak_planks')
    b.set(8, 19, 11, 'bell', attachment='ceiling', facing='north', powered=False)
    parts.pyramid_roof(b, 6, 9, 10, 13, 21, 'dark_oak_stairs', 'dark_oak_planks', pitch=2,
                       finial=['dark_oak_fence', 'lightning_rod[facing=up]'])
    T.mossify(b, (6, 21, 9, 10, 26, 13), seed + 2, .2)
    # Front porch with its own steep gable.
    for x in range(7, 10):
        for z in range(2, 5):
            b.set(x, 1, z, 'dark_oak_planks')
            b.set(x, 0, z, 'mossy_cobblestone')
    for x in (7, 9):
        T.log_post(b, x, 2, 2, 4, wood='dark_oak')
    parts.gable_roof(b, 7, 2, 9, 4, 5, ROOFS['dark_oak'], axis='z', overhang=1, rake=(1, 0), pitch=2,
                     gable='dark_oak_planks')
    b.set(8, 7, 2, 'air')
    b.set(8, 6, 2, 'air')
    T.hang_lantern(b, 8, 6, 3)
    b.set(8, 1, 1, 'dark_oak_stairs', facing='south', half='bottom', lock=True)
    b.set(8, 2, gz0, 'air')
    b.set(8, 3, gz0, 'air')
    b.door(8, 2, nz0, facing='south', wood='dark_oak')
    # Interior: pews facing the altar, carpet aisle, candles and a lantern crown.
    for z in (9, 11, 13):
        for x in (6, 7, 9, 10):
            b.set(x, 2, z, 'spruce_stairs', facing='north', half='bottom', lock=True, shape='straight')
    for z in range(8, 15):
        b.set(8, 2, z, 'green_carpet') if z > 8 else None
    for x in (7, 8, 9):
        b.set(x, 2, 14, 'chiseled_stone_bricks' if x == 8 else 'stripped_dark_oak_log', axis='x')
    b.set(7, 3, 14, 'brewing_stand')
    b.set(8, 3, 14, 'candle', candles=3, lit=True, waterlogged=False)
    b.set(9, 3, 14, 'green_candle', candles=2, lit=True, waterlogged=False)
    for y in (5, 6, 7):
        b.set(8, y, nz1, 'yellow_stained_glass_pane' if y < 7 else 'red_stained_glass_pane')
    for z in (9, 13):
        b.set(nx0, 7, z, 'glass_pane')
        b.set(nx1, 7, z, 'glass_pane')
    T.hang_lantern(b, 8, 9, 11, links=2)
    for x, z in ((6, 9), (10, 9), (6, 13), (10, 13)):
        T.hang_lantern(b, x, 9, z)
    # Graveyard on both flanks inside a mossy wall, an old spruce in the corner.
    for z in range(6, 18, 3):
        for x in (1, 15):
            grave(b, x, z, rng)
    for x in range(0, 17):
        b.set(x, 1, 20, 'mossy_cobblestone_wall' if x % 4 else 'mossy_cobblestone')
    for z in range(3, 20):
        for x in (0, 16):
            b.set(x, 1, z, 'mossy_cobblestone_wall' if z % 4 else 'mossy_cobblestone')
    T.spruce(b, 14, 19, height=8)
    b.custom(2, 1, 19, 'village_bench', facing='east')
    # Front path and lanterns.
    for z in range(0, 2):
        b.set(8, 0, z, 'mossy_stone_bricks' if z else 'gravel')
    for x in (5, 11):
        T.lamp(b, x, 2)
    for x in (1, 2, 3, 13, 14, 15):
        for z in (1, 2, 3):
            b.set(x, 0, z, 'podzol' if rng.random() < .4 else 'grass_block')
            if rng.random() < .5:
                b.set(x, 1, z, rng.choice(['fern', 'short_grass', 'lily_of_the_valley']))
    b.entrance(8)
    b.natural_ground()
    return b


# ---------------------------------------------------------------- apothecary
def apothecary():
    """Herb hut: a mossy-roofed log cabin, infirmary below, the apothecary's bedroom above, herb beds in front."""
    rng = random.Random(4305)
    seed = 4305
    b = Build('taiga/apothecary', (11, 21, 16))
    x0, z0, x1, z1 = 1, 5, 9, 12
    T.plinth(b, x0, z0, x1, z1, seed=seed)
    T.log_walls(b, x0, z0, x1, z1, 2, 9)
    T.ceiling(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, 6)
    T.ceiling(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, 10)
    T.roof(b, x0, z0, x1, z1, 9, 'spruce', axis='z', pitch=2, gable='stripped_spruce_log[axis=x]', seed=seed,
           moss=.5)
    parts.front_door(b, 5, 2, z0, 'north', wood='spruce', step='mossy_cobblestone_stairs', lamps=False)
    for x in (4, 5, 6):
        b.set(x, 5, z0 - 1, 'spruce_slab', type='top') if x == 5 else \
            b.set(x, 5, z0 - 1, 'spruce_stairs', facing='south', half='top', lock=True)
    T.hang_lantern(b, 6, 4, z0 - 1)
    win(b, 2, 3, z0, 'north', width=2)
    win(b, 7, 3, z0, 'north')
    for x in (3, 4):
        b.set(x, 8, z0, 'glass_pane')
    win(b, x0, 3, 8, 'west', width=2)
    win(b, x1, 3, 8, 'east', width=2)
    win(b, x0, 8, 8, 'west')
    win(b, 4, 8, z1, 'south')
    # Vines and moss creeping down the west wall.
    for z in range(z0, z1 + 1):
        for y in range(5, 9):
            if rng.random() < .4 and b.get(x0 - 1, y, z)[0] == 'minecraft:air':
                b.set(x0 - 1, y, z, 'vine', east=True)
    # Infirmary and workroom.
    b.custom(2, 2, 6, 'alchemical_press', facing='east')
    b.set(2, 2, 7, 'brewing_stand')
    b.set(2, 2, 8, 'water_cauldron', level=2)
    for z in (9, 11):
        b.custom(6, 2, z, 'apothecary_cot', facing='west')
    b.set(2, 2, 11, 'barrel', facing='up', open=False)
    b.set(2, 3, 11, 'potted_fern')
    b.set(3, 2, 11, 'potted_red_mushroom')
    T.hang_lantern(b, 4, 5, 9)
    parts.stair_run(b, 8, 6, 2, 5, 'south', wood='spruce')
    b.resident(4, 2, 9, 'apothecary')
    # Bedroom upstairs behind a partition that closes the stairwell.
    for z in range(z0 + 1, z1):
        for y in (7, 8, 9):
            b.set(7, y, z, 'spruce_planks')
    b.door(7, 7, 11, facing='west', wood='spruce')
    b.bed(3, 7, 10, 'south', 'green')
    b.chest(2, 7, 7, 'east', loot=LOOT)
    b.set(5, 7, 11, 'potted_azure_bluet')
    b.set(6, 7, 6, 'brewing_stand')
    b.set(5, 7, 6, 'bookshelf')
    T.hang_lantern(b, 4, 9, 8)
    b.room('apothecary_bedroom', (4, 8, 8))
    # Herb beds either side of the path.
    for x in range(1, 10):
        for z in range(1, 4):
            if x in (4, 5, 6):
                continue
            b.set(x, 0, z, 'podzol' if x in (1, 9) else 'rooted_dirt')
            p = rng.choice(['sweet_berry_bush', 'fern', 'short_grass', 'red_mushroom', 'brown_mushroom',
                            'lily_of_the_valley', 'azure_bluet'])
            if p == 'sweet_berry_bush':
                b.set(x, 1, z, p, age=3)
            elif 'mushroom' in p:
                b.set(x, 0, z, 'podzol')
                b.set(x, 1, z, p)
            else:
                b.set(x, 1, z, p)
    for x in (0, 10):
        for z in range(1, 4):
            b.set(x, 1, z, 'spruce_fence')
    for z in range(0, 5):
        b.set(5, 0, z, 'mossy_cobblestone' if z % 2 else 'gravel')
    plaque(b, 4, 4)
    b.entrance(5)
    b.natural_ground()
    return b


# ------------------------------------------------------------------- library
def library():
    """Lore lodge: rubble-stone ground floor lined with books, a log upper floor and a glazed gable."""
    rng = random.Random(4306)
    seed = 4306
    b = Build('taiga/library', (11, 22, 17))
    x0, z0, x1, z1 = 1, 4, 9, 13
    for y in (0, 1):
        for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
            b.set(x, y, z, 'mossy_stone_bricks' if (x + z + y) % 3 else 'stone_bricks')
        b.fill(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, 'dark_oak_planks' if y else 'dirt')
    T.stone_walls(b, x0, z0, x1, z1, 2, 5, seed=seed)
    T.ceiling(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, 6, 'dark_oak_planks')
    T.beam_course(b, x0, z0, x1, z1, 6, 'dark_oak')
    T.log_walls(b, x0, z0, x1, z1, 7, 9)
    T.ceiling(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, 10, 'dark_oak_planks')
    T.roof(b, x0, z0, x1, z1, 9, 'dark_oak', axis='z', pitch=2, gable='spruce_planks', seed=seed)
    for y in range(11, 15):
        for x in (4, 5, 6):
            if b.get(x, y, z0)[0] == 'minecraft:spruce_planks':
                b.set(x, y, z0, 'glass_pane')
    parts.front_door(b, 5, 2, z0, 'north', wood='dark_oak', step='stone_brick_stairs', lamps=False)
    for x in (2, 7):
        parts.window(b, x, 3, z0, 'north', height=2, width=2 if x == 2 else 1, trim='dark_oak', shutters=False,
                     sill='stone_brick')
    for z in (7, 10):
        parts.window(b, x0, 3, z, 'west', height=2, trim='dark_oak', shutters=False)
        parts.window(b, x1, 3, z, 'east', height=2, trim='dark_oak', shutters=False)
    for x in (3, 5, 7):
        b.set(x, 8, z0, 'glass_pane')
    for z in (6, 11):
        win(b, x0, 8, z, 'west')
        win(b, x1, 8, z, 'east')
    # Books line the ground floor.
    for z in range(z0 + 1, z1):
        for x in (2, 8):
            for y in (2, 3, 4):
                if b.get(x - 1 if x == 2 else x + 1, y, z)[0] == 'minecraft:glass_pane':
                    continue
                if x == 8 and z >= 8:
                    continue
                b.set(x, y, z, 'bookshelf' if (y + z) % 3 else 'chiseled_bookshelf',
                      **({'facing': 'east' if x == 2 else 'west'} if (y + z) % 3 == 0 else {}))
    for x in range(2, 8):
        for y in (2, 3, 4):
            b.set(x, y, z1 - 1, 'bookshelf')
    b.custom(5, 2, 11, 'archives', facing='north')
    b.set(4, 2, 8, 'lectern', facing='north', has_book=False, powered=False)
    parts.table(b, 5, 2, 6, wood='dark_oak')
    parts.chair(b, 4, 2, 6, 'west', wood='dark_oak')
    parts.chair(b, 6, 2, 6, 'east', wood='dark_oak')
    T.hang_lantern(b, 5, 5, 7)
    T.hang_lantern(b, 5, 5, 10)
    parts.stair_run(b, 8, 12, 2, 5, 'north', wood='dark_oak')
    b.resident(5, 2, 9, 'scholar')
    # Upper floor: reading gallery in front, the scholar's room behind.
    for x in range(2, 8):
        for y in (7, 8, 9):
            b.set(x, y, 9, 'dark_oak_planks')
    for z in range(10, 13):
        for y in (7, 8, 9):
            b.set(8, y, z, 'dark_oak_planks')
    b.door(4, 7, 9, facing='south', wood='dark_oak')
    b.bed(3, 7, 11, 'west', 'cyan')
    b.chest(2, 7, 12, 'east', loot=LOOT)
    b.set(6, 7, 12, 'bookshelf')
    b.set(7, 7, 12, 'bookshelf')
    b.set(7, 8, 12, 'bookshelf')
    T.hang_lantern(b, 5, 9, 11)
    b.room('scholar_bedroom', (5, 8, 11))
    for x in (2, 3):
        for y in (7, 8):
            b.set(x, y, 5, 'bookshelf')
    parts.table(b, 5, 7, 6, wood='dark_oak')
    T.hang_lantern(b, 5, 9, 7)
    # Front: flagged path, lantern posts, ferns.
    for z in range(0, 4):
        b.set(5, 0, z, 'mossy_stone_bricks' if z % 2 else 'cobblestone')
    for x in (3, 7):
        T.lamp(b, x, 2)
    for x in (1, 2, 8, 9):
        for z in (1, 2, 3):
            b.set(x, 0, z, 'podzol' if rng.random() < .5 else 'grass_block')
            if rng.random() < .5:
                b.set(x, 1, z, rng.choice(['fern', 'short_grass', 'sweet_berry_bush[age=2]']))
    plaque(b, 4, 3)
    b.entrance(5)
    b.natural_ground()
    return b


# ------------------------------------------------------------------- markets
def market_furs():
    """Fur trading post: two stalls, a hide-drying rack and a stack of barrels."""
    rng = random.Random(4307)
    b = Build('taiga/market_furs', (11, 7, 11))
    for x in range(11):
        for z in range(11):
            if rng.random() < .85:
                b.set(x, 0, z, rng.choice(['coarse_dirt', 'podzol', 'dirt_path', 'gravel', 'mossy_cobblestone']))
    for z in range(0, 11):
        b.set(5, 0, z, 'dirt_path' if z % 3 else 'gravel')
    stall(b, 1, 9, 'north', 'brown', ['white_wool', 'brown_wool', 'barrel[facing=up]'], wood='spruce')
    stall(b, 9, 7, 'west', 'green', ['barrel[facing=up]', 'sweet_berry_bush[age=3]', 'hay_block[axis=y]'],
          wood='spruce')
    T.drying_rack(b, 0, 3, length=3, hides=('brown', 'white', 'brown'))
    T.chopping_block(b, 2, 5)
    T.lamp(b, 5, 6, height=2)
    for x, z in ((8, 1), (9, 1), (8, 2)):
        b.barrel(x, 1, z, 'up')
    b.set(9, 1, 2, 'hay_block', axis='y')
    b.entrance(5)
    b.natural_ground()
    return b


def market_smokehouse():
    """Smokehouse: an open log shed over a fire pit, fish barrels and a salting table."""
    rng = random.Random(4308)
    seed = 4308
    b = Build('taiga/market_smokehouse', (11, 11, 11))
    for x in range(11):
        for z in range(11):
            b.set(x, 0, z, rng.choice(['coarse_dirt', 'podzol', 'gravel', 'coarse_dirt']))
    for z in range(0, 3):
        b.set(5, 0, z, 'dirt_path')
    sx0, sz0, sx1, sz1 = 2, 3, 8, 8
    for x in range(sx0, sx1 + 1):
        for z in range(sz0, sz1 + 1):
            b.set(x, 0, z, 'mossy_cobblestone' if (x + z) % 3 == 0 else 'cobblestone')
    for x, z in ((sx0, sz0), (sx1, sz0), (sx0, sz1), (sx1, sz1)):
        T.log_post(b, x, z, 1, 3)
    T.log_walls(b, sx0, sz1, sx1, sz1, 1, 3, stubs=False)
    for x in range(sx0, sx1 + 1):
        for z in (sz0, sz1):
            b.set(x, 4, z, 'stripped_spruce_log', axis='x')
    for z in range(sz0, sz1 + 1):
        for x in (sx0, sx1):
            b.set(x, 4, z, 'stripped_spruce_log', axis='z')
    T.roof(b, sx0, sz0, sx1, sz1, 4, 'spruce', axis='z', pitch=1, gable='stripped_spruce_log[axis=x]',
           seed=seed, moss=.35)
    b.set(5, 1, 6, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    for x in (4, 6):
        b.set(x, 1, 6, 'cobblestone_wall')
    for x in range(sx0 + 1, sx1):
        b.set(x, 3, 5, 'spruce_fence') if x != 5 else b.set(x, 3, 5, 'stripped_spruce_log', axis='x')
    b.set(5, 3, 5, 'stripped_spruce_log', axis='x')
    b.set(3, 1, 7, 'smoker', facing='north', lit=True)
    b.barrel(7, 1, 7, 'up')
    b.barrel(7, 2, 7, 'up')
    b.set(7, 1, 4, 'spruce_fence')
    b.set(7, 2, 4, 'spruce_pressure_plate', powered=False)
    for x, z in ((0, 9), (1, 9), (0, 8), (9, 9), (10, 9)):
        b.barrel(x, 1, z, rng.choice(['up', 'north']))
    b.set(10, 1, 8, 'hay_block', axis='y')
    T.woodstack(b, 9, 2, 'z', length=4, height=2)
    T.lamp(b, 1, 2, height=2)
    b.custom(3, 1, 1, 'village_bench', facing='south')
    b.entrance(5)
    b.natural_ground()
    return b


def market_berries():
    """Berry yard: sweet berry beds round a log-roofed well, with benches and baskets."""
    rng = random.Random(4309)
    seed = 4309
    b = Build('taiga/market_berries', (11, 9, 11))
    for x in range(11):
        for z in range(11):
            b.set(x, 0, z, 'grass_block')
    for z in range(0, 11):
        b.set(5, 0, z, 'dirt_path' if z % 3 else 'coarse_dirt')
    for x in range(1, 10):
        b.set(x, 0, 5, 'dirt_path' if x % 3 else 'coarse_dirt')
    for bx, bz in ((1, 1), (7, 1), (1, 7), (7, 7)):
        for x in range(bx, bx + 3):
            for z in range(bz, bz + 3):
                b.set(x, 0, z, 'podzol')
                if rng.random() < .75:
                    b.set(x, 1, z, 'sweet_berry_bush', age=rng.choice([2, 3]))
                elif rng.random() < .5:
                    b.set(x, 1, z, 'fern')
    for x in range(4, 7):
        for z in range(4, 7):
            b.set(x, 0, z, 'mossy_cobblestone')
            if (x, z) == (5, 5):
                b.set(x, 1, z, 'water', level=0)
            elif abs(x - 5) == 1 and abs(z - 5) == 1:
                b.set(x, 1, z, 'mossy_cobblestone')
                b.set(x, 2, z, 'spruce_fence')
                b.set(x, 3, z, 'spruce_fence')
            else:
                b.set(x, 1, z, 'mossy_cobblestone_wall')
    parts.gable_roof(b, 4, 4, 6, 6, 4, ROOFS['dark_oak'], axis='x', overhang=1, rake=0)
    T.mossify(b, (3, 4, 3, 7, 6, 7), seed, .35)
    T.chain(b, 5, 4, 5)
    b.set(5, 3, 5, 'lantern', hanging=True, waterlogged=False)
    for x, z, f in ((4, 2, 'east'), (6, 8, 'west')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    b.barrel(4, 1, 8, 'up')
    b.set(6, 1, 2, 'composter', level=5)
    b.entrance(5)
    b.natural_ground()
    return b


DESIGNS = {'taiga/tavern': tavern, 'taiga/garrison': garrison, 'taiga/workshop': workshop,
           'taiga/chapel': chapel, 'taiga/apothecary': apothecary, 'taiga/library': library,
           'taiga/market_furs': market_furs, 'taiga/market_smokehouse': market_smokehouse,
           'taiga/market_berries': market_berries}
