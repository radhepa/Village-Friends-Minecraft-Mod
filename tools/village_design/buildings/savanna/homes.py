"""Savanna homes: round mud-and-thatch huts, verandah bungalows, an acacia lodge and walled compounds.

Every home is a drop-in lot: north-facing ``building_entrance`` at [x,1,0], a path
to a real front door, at least one enclosed bedroom with paired beds, a loot chest,
lights and one or two unemployed residents.
"""
import random

from ...kit import Build
from ... import parts
from ...parts import Body, Style
from . import homes_parts as hp
from .palette import LOOT, ROOFS, STYLES

BANDS = {
    'ochre': ['orange_terracotta', 'orange_terracotta', 'white_terracotta'],
    'chevron': ['white_terracotta', 'brown_terracotta', 'white_terracotta', 'orange_terracotta'],
    'earth': ['brown_terracotta', 'terracotta', 'brown_terracotta', 'white_terracotta'],
}
LODGE = Style(frame='acacia_log', fill='packed_mud', floor='acacia_planks', roof=ROOFS['acacia'],
              base='mud_bricks', base_stairs='mud_brick_stairs', trim='acacia', door='acacia',
              upper_fill='white_terracotta', ceiling='acacia_planks', accent='dark_oak')
BUNGALOW = Style(frame='acacia_log', fill='white_terracotta', floor='acacia_planks', roof=ROOFS['acacia'],
                 base='mud_bricks', base_stairs='mud_brick_stairs', trim='acacia', door='acacia',
                 upper_fill='white_terracotta', ceiling='acacia_planks', accent='dark_oak')


def door_frame(b, x, y, z, axis='x', wood='stripped_acacia_log'):
    """Log jambs and lintel around a door at (x, y, z) in a wall running along ``axis``."""
    dx, dz = (1, 0) if axis == 'x' else (0, 1)
    for yy in (y, y + 1, y + 2):
        b.set(x - dx, yy, z - dz, wood, axis='y')
        b.set(x + dx, yy, z + dz, wood, axis='y')
    b.set(x, y + 2, z, wood, axis=axis)


def kitchen(b, cells, y, facing, rng):
    """Cooking corner along a wall: smoker, barrel, crafting table, a pot."""
    items = ['smoker', 'barrel', 'crafting_table', 'pot', 'furnace']
    for (x, z), item in zip(cells, items):
        if item == 'smoker':
            b.set(x, y, z, 'smoker', facing=facing, lit=False)
        elif item == 'furnace':
            b.set(x, y, z, 'furnace', facing=facing, lit=False)
        elif item == 'barrel':
            b.barrel(x, y, z, 'up')
        elif item == 'pot':
            hp.pot(b, x, y, z)
        else:
            b.set(x, y, z, item)


# ------------------------------------------------------------------ round huts
def hut_round():
    """A single round mud hut under a stepped thatch cone, with a cooking yard."""
    rng = random.Random(3101)
    b = Build('savanna/hut_round', (13, 14, 15))
    cx, cz, r = 6, 7, 3.5
    inside, ring, top = hp.round_hut(b, cx, cz, r, 1, 3, pattern=(2, BANDS['ochre']))
    door_frame(b, 6, 2, 4)
    hp.door(b, 6, 2, 4, 'north', step='mud_brick_stairs')
    for x, z in ((3, 7), (9, 7), (6, 10)):
        hp.slit(b, x, 3, z)
    hp.cone_roof(b, cx, cz, r, top, inside)
    # Inside: bed and chest on the east, stores on the west, a hanging lantern.
    b.bed(8, 2, 7, 'south', 'orange')
    b.chest(8, 2, 6, 'west', loot=LOOT)
    b.barrel(4, 2, 7, 'up')
    hp.pot(b, 4, 2, 8)
    b.set(6, 2, 9, 'crafting_table')
    b.set(5, 2, 9, 'brown_carpet')
    b.set(7, 2, 9, 'brown_carpet')
    hp.lantern(b, 6, 8, 7, chain=2)
    b.room('hut', (6, 3, 6))
    b.resident(5, 2, 7)
    # Yard: path, cooking fire, drying rack, water pot and a hay pile behind.
    hp.path(b, 6, 0, 3, rng)
    b.entrance(6)
    b.custom(5, 1, 1, 'house_plaque', facing='north')
    hp.firepit(b, 10, 1, 3, benches=('west',))
    hp.pot(b, 1, 1, 4)
    b.set(2, 1, 3, 'water_cauldron', level=3)
    hp.drying_rack(b, 2, 13, 'x', length=4, face='north')
    hp.hay_pile(b, [(10, 12), (11, 12), (11, 11)], rng, high=[(11, 12)])
    hp.yard(b, hp.disk(6, 7, 6.6), rng, tufts=.15)
    b.natural_ground()
    return b


def homestead():
    """Two round huts, a sleeping hut and a kitchen hut, joined by a walled cooking yard."""
    rng = random.Random(3102)
    b = Build('savanna/homestead', (20, 14, 17))
    # Sleeping hut (west) and kitchen hut (east).
    a_in, _, a_top = hp.round_hut(b, 5, 9, 3.5, 1, 3, pattern=(2, BANDS['chevron']))
    k_in, _, k_top = hp.round_hut(b, 14, 9, 3, 1, 3, pattern=(2, BANDS['earth']))
    door_frame(b, 5, 2, 6)
    hp.door(b, 5, 2, 6, 'north')
    door_frame(b, 14, 2, 6)
    hp.door(b, 14, 2, 6, 'north')
    hp.cone_roof(b, 5, 9, 3.5, a_top, a_in)
    hp.cone_roof(b, 14, 9, 3, k_top, k_in, eave=1.3)
    for x, z in ((2, 9), (5, 12)):
        hp.slit(b, x, 3, z)
    for x, z in ((17, 9), (14, 12)):
        hp.slit(b, x, 3, z)
    # Cooking yard: a low mud wall from hut to hut with a gate on the street.
    wall = [(x, 3) for x in range(1, 19) if x != 9] + [(1, z) for z in range(4, 9)] + \
           [(18, z) for z in range(4, 9)] + [(9, z) for z in range(8, 11)] + [(10, z) for z in range(8, 11)]
    hp.mud_wall(b, wall, 1, 1, mat='mud_bricks', cap='mud_brick_wall')
    b.set(9, 1, 3, 'acacia_fence_gate', facing='north', open=False, in_wall=True, powered=False)
    for x in (8, 10):
        b.set(x, 2, 3, 'stripped_acacia_log', axis='y')
        b.set(x, 3, 3, 'lantern', hanging=False, waterlogged=False)
    for x in range(2, 18):
        for z in range(4, 8):
            if b.get(x, 0, z)[0] == 'minecraft:air':
                b.set(x, 0, z, rng.choice(['packed_mud', 'coarse_dirt', 'packed_mud', 'dirt_path']))
    hp.firepit(b, 9, 1, 6, benches=('west', 'east'))
    hp.pot(b, 2, 1, 4)
    hp.pot(b, 17, 1, 4)
    b.set(16, 1, 4, 'water_cauldron', level=3)
    # Sleeping hut: bed, chest, rug, lantern.
    b.bed(7, 2, 9, 'south', 'red')
    b.chest(7, 2, 8, 'west', loot=LOOT)
    b.set(3, 2, 9, 'barrel', facing='up', open=False)
    hp.pot(b, 3, 2, 10)
    for x, z in ((4, 9), (5, 9), (4, 10), (5, 10), (6, 10)):
        b.set(x, 2, z, 'red_carpet' if (x + z) % 2 else 'orange_carpet')
    hp.lantern(b, 5, 8, 9, chain=2)
    b.room('sleeping_hut', (5, 3, 8))
    # Kitchen hut: hearth stores and the child's bed.
    kitchen(b, [(13, 10), (12, 9), (16, 9), (14, 11)], 2, 'north', rng)
    b.bed(15, 2, 9, 'south', 'yellow')
    hp.lantern(b, 14, 7, 9, chain=1)
    b.room('kitchen_hut', (14, 3, 8))
    b.resident(5, 2, 10)
    b.resident(13, 2, 9, child=True)
    # Street side: path, plaque, a lone young acacia behind.
    hp.path(b, 9, 0, 2, rng)
    b.entrance(9)
    b.custom(8, 1, 1, 'house_plaque', facing='north')
    hp.drying_rack(b, 8, 15, 'x', length=4, hides=('orange', 'brown'), face='north')
    hp.yard(b, {(x, z) for x in range(0, 20) for z in range(0, 17) if (x - 9.5) ** 2 / 110 + (z - 9) ** 2 / 64 <= 1},
            rng, tufts=.12)
    b.natural_ground()
    return b


def hut_family():
    """A large rondavel whose thatch sweeps out over a ring of posts: a shaded verandah all round."""
    rng = random.Random(3103)
    b = Build('savanna/hut_family', (19, 16, 19))
    cx, cz, r = 9, 9, 4.5
    inside, ring, top = hp.round_hut(b, cx, cz, r, 1, 3, pattern=(3, BANDS['chevron']))
    # Raised verandah plinth with posts on its rim; the thatch sweeps out over it.
    deck = hp.disk(cx, cz, 6.8) - hp.disk(cx, cz, r)
    for x, z in deck:
        b.set(x, 0, z, 'mud_bricks')
        b.set(x, 1, z, 'packed_mud')
    rim = hp.outline(hp.disk(cx, cz, 6.8))
    posts = [(x, z) for x, z in rim if (x - cx) * (z - cz) == 0 or abs(x - cx) == abs(z - cz)]
    for x, z in posts:
        if (x, z) == (9, 3):
            continue
        for yy in (2, 3, 4):
            b.set(x, yy, z, 'stripped_acacia_log', axis='y')
    hp.cone_roof(b, cx, cz, r, top, inside, eave=2.5, ceiling='acacia_planks', fringe='acacia_trapdoor')
    for x in (8, 9, 10):
        b.set(x, 1, 2, 'mud_brick_stairs', facing='south', half='bottom')
    # Openings.
    door_frame(b, 9, 2, 5)
    b.door(9, 2, 5, facing='south', wood='acacia')
    for x, z in ((5, 8), (5, 10), (13, 8), (13, 10), (9, 13)):
        hp.slit(b, x, 3, z)
    # Interior: hearth room in front, bedroom behind a mud partition with its own door.
    for x in range(5, 14):
        for yy in (2, 3, 4):
            if (x, 10) in inside:
                b.set(x, yy, 10, 'mud_bricks')
    b.door(9, 2, 10, facing='south', wood='acacia')
    b.bed(7, 2, 11, 'west', 'orange')
    b.bed(11, 2, 11, 'east', 'white')
    b.chest(8, 2, 12, 'north', loot=LOOT)
    hp.pot(b, 10, 2, 12)
    b.set(9, 2, 12, 'orange_carpet')
    hp.lantern(b, 9, 4, 12)
    b.room('bedroom', (8, 3, 11))
    kitchen(b, [(6, 8), (6, 7), (7, 6), (12, 7), (12, 8)], 2, 'east', rng)
    hp.low_table(b, 9, 2, 8)
    hp.stool(b, 8, 2, 8)
    hp.stool(b, 10, 2, 8)
    hp.lantern(b, 9, 4, 7)
    b.resident(7, 2, 9)
    b.resident(11, 2, 9, child=True)
    # Verandah life: benches, water pots, lanterns under the eave; path to the street.
    b.custom(5, 2, 4, 'village_bench', facing='north')
    b.custom(13, 2, 4, 'village_bench', facing='north')
    hp.pot(b, 3, 2, 6)
    b.set(15, 2, 6, 'water_cauldron', level=3)
    for x in (7, 11):
        b.set(x, 4, 3, 'lantern', hanging=True, waterlogged=False)
    hp.path(b, 9, 0, 1, rng)
    b.entrance(9)
    b.custom(7, 1, 1, 'house_plaque', facing='north')
    hp.hay_pile(b, [(16, 16), (17, 16), (17, 15)], rng, high=[(17, 16)])
    hp.yard(b, hp.disk(cx, cz, 8.6), rng, tufts=.12)
    b.natural_ground()
    return b


# ------------------------------------------------------------------ rectangular houses
def bungalow_verandah():
    """Acacia-framed bungalow with ochre walls, a deep front verandah and a low slab hip roof."""
    rng = random.Random(3104)
    st = BUNGALOW
    b = Build('savanna/bungalow_verandah', (17, 11, 18))
    body = Body(b, 2, 6, 14, 13, st, heights=(3,), spacing=4).build()
    # Ochre dado under white-washed walls.
    b.replace(2, 2, 6, 14, 2, 13, 'white_terracotta', 'orange_terracotta')
    # Verandah: raised deck, posts, rail and its own ceiling under the main roof.
    hp.verandah(b, 2, 3, 14, 5, 1, [(2, 3), (5, 3), (11, 3), (14, 3)], 5)
    for x in range(2, 15):
        b.set(x, 5, 3, 'stripped_acacia_log', axis='x')
        for z in (4, 5):
            b.set(x, 5, z, 'acacia_planks')
    for z in (4, 5):
        b.set(2, 5, z, 'stripped_acacia_log', axis='z')
        b.set(14, 5, z, 'stripped_acacia_log', axis='z')
    for x in list(range(3, 5)) + list(range(6, 7)) + list(range(10, 11)) + list(range(12, 14)):
        b.set(x, 2, 3, 'acacia_fence')
    for z in (4, 5):
        b.set(2, 2, z, 'acacia_fence')
        b.set(14, 2, z, 'acacia_fence')
    for x in (7, 8, 9):
        b.set(x, 1, 2, 'mud_brick_stairs', facing='south', half='bottom')
    hp.hip_roof(b, 2, 3, 14, 13, 6, ROOFS['acacia'], overhang=1, low=True, eave='dark_oak_slab')
    # Openings.
    door_frame(b, 8, 2, 6)
    b.door(8, 2, 6, facing='south', wood='acacia')
    for x in (4, 12):
        hp.glazed(b, x, 3, 6, 'north', sill=False)
    for x in (5, 11):
        hp.glazed(b, x, 3, 13, 'south')
    for z in (9, 10):
        hp.glazed(b, 2, 3, z, 'west', shutters=None)
        hp.glazed(b, 14, 3, z, 'east', shutters=None)
    # Bedroom (east) behind a partition with a door.
    for z in range(7, 13):
        for yy in (2, 3, 4):
            b.set(10, yy, z, 'acacia_planks')
    b.door(10, 2, 10, facing='east', wood='acacia')
    b.bed(13, 2, 8, 'north', 'orange')
    b.bed(13, 2, 11, 'south', 'orange')
    b.chest(13, 2, 9, 'west', loot=LOOT)
    hp.pot(b, 11, 2, 7)
    parts.rug(b, 11, 11, 12, 12, 2, 'white', border='orange')
    hp.lantern(b, 12, 4, 10)
    b.room('bedroom', (11, 3, 10))
    # Living room: table, stools, kitchen corner, rug.
    kitchen(b, [(3, 12), (4, 12), (5, 12), (3, 7), (3, 11)], 2, 'north', rng)
    b.custom(6, 2, 9, 'tavern_table')
    b.custom(5, 2, 9, 'tavern_chair', facing='east')
    b.custom(7, 2, 9, 'tavern_chair', facing='west')
    b.custom(6, 2, 10, 'tavern_chair', facing='north')
    b.set(9, 2, 12, 'barrel', facing='up', open=False)
    hp.lantern(b, 6, 4, 10)
    hp.lantern(b, 8, 4, 4)
    b.resident(5, 2, 10)
    b.resident(12, 2, 10, child=True)
    # Front: steps, path, plaque, bench on the verandah; a woodpile behind.
    hp.path(b, 8, 0, 2, rng)
    b.entrance(8)
    b.custom(6, 1, 1, 'house_plaque', facing='north')
    b.custom(4, 2, 5, 'village_bench', facing='north')
    hp.pot(b, 13, 2, 4)
    parts.woodpile(b, 4, 1, 15, 'x', length=4, wood='acacia')
    b.set(11, 1, 15, 'water_cauldron', level=3)
    hp.yard(b, {(x, z) for x in range(0, 17) for z in range(0, 18)}, rng, tufts=.1,
            mix=['coarse_dirt', 'grass_block', 'grass_block', 'dirt'])
    b.natural_ground()
    return b


def bungalow_clay():
    """Small white-washed clay house with a terracotta hip roof and a shaded porch."""
    rng = random.Random(3105)
    st = STYLES['clay']
    b = Build('savanna/bungalow_clay', (13, 11, 15))
    body = Body(b, 2, 5, 10, 11, st, heights=(3,), spacing=4).build()
    hp.hip_roof(b, 2, 5, 10, 11, 5, ROOFS['terracotta'], overhang=1)
    # Porch over the door.
    for x, z in ((4, 2), (8, 2)):
        b.set(x, 0, z, 'mud_bricks')
        for yy in (1, 2, 3):
            b.set(x, yy, z, 'acacia_fence')
    for x in range(3, 10):
        for z in (2, 3):
            b.set(x, 4, z, 'acacia_slab', type='bottom', waterlogged=False)
        b.set(x, 4, 4, 'acacia_planks')
    for x in range(4, 9):
        for z in (2, 3, 4):
            b.set(x, 0, z, 'packed_mud')
    hp.door(b, 6, 2, 5, 'north', step='mud_brick_stairs')
    b.set(6, 3, 3, 'lantern', hanging=True, waterlogged=False)
    for x in (3, 9):
        hp.glazed(b, x, 3, 5, 'north')
    hp.glazed(b, 4, 3, 11, 'south')
    hp.glazed(b, 10, 3, 8, 'east')
    hp.glazed(b, 2, 3, 8, 'west')
    # Bedroom on the east behind a partition.
    for z in range(6, 11):
        for yy in (2, 3, 4):
            b.set(7, yy, z, 'white_terracotta')
    b.door(7, 2, 8, facing='east', wood='acacia')
    b.bed(9, 2, 9, 'south', 'light_blue')
    b.chest(9, 2, 6, 'south', loot=LOOT)
    b.set(9, 2, 7, 'brown_carpet')
    hp.lantern(b, 8, 4, 8)
    b.room('bedroom', (8, 3, 7))
    kitchen(b, [(3, 10), (4, 10), (3, 9), (5, 10)], 2, 'north', rng)
    hp.low_table(b, 4, 2, 7)
    hp.stool(b, 3, 2, 7)
    hp.lantern(b, 5, 4, 8)
    b.resident(5, 2, 8)
    hp.path(b, 6, 0, 1, rng)
    b.entrance(6)
    b.custom(3, 1, 1, 'house_plaque', facing='north')
    hp.pot(b, 9, 1, 3)
    hp.pot(b, 10, 1, 3, plant='potted_cactus')
    hp.firepit(b, 10, 1, 13, lit=False)
    hp.yard(b, hp.disk(6, 8, 7.4), rng, tufts=.12)
    b.natural_ground()
    return b


def lodge():
    """Two-storey acacia lodge: mud ground floor, ochre upper storey and a full-width gallery."""
    rng = random.Random(3106)
    st = LODGE
    b = Build('savanna/lodge', (17, 15, 17))
    body = Body(b, 3, 6, 13, 13, st, heights=(3, 3), spacing=5).build()
    top = body.top  # 9
    # Ground-floor shade and the upstairs gallery on six posts.
    for x in range(3, 14):
        for z in (3, 4, 5):
            b.set(x, 0, z, 'mud_bricks')
            b.set(x, 1, z, 'packed_mud')
            b.set(x, 5, z, 'acacia_planks')
    for x in (3, 7, 9, 13):
        for yy in range(2, top):
            b.set(x, yy, 3, 'stripped_acacia_log', axis='y')
    for x in range(3, 14):
        b.set(x, top, 3, 'stripped_acacia_log', axis='x')
        b.set(x, top, 4, 'acacia_planks')
        b.set(x, top, 5, 'acacia_planks')
        if x not in (3, 7, 9, 13):
            b.set(x, 6, 3, 'acacia_fence')
    for z in (4, 5):
        b.set(3, 6, z, 'acacia_fence')
        b.set(13, 6, z, 'acacia_fence')
        b.set(3, top, z, 'stripped_acacia_log', axis='z')
        b.set(13, top, z, 'stripped_acacia_log', axis='z')
    for x in (3, 13):
        b.set(x, 5, 4, 'stripped_acacia_log', axis='z')
    for x in (7, 8, 9):
        b.set(x, 1, 2, 'mud_brick_stairs', facing='south', half='bottom')
    b.set(8, 1, 2, 'mud_brick_stairs', facing='south', half='bottom')
    b.replace(3, 6, 6, 13, 6, 13, 'white_terracotta', 'orange_terracotta')
    hp.hip_roof(b, 3, 3, 13, 13, top + 1, ROOFS['acacia'], overhang=1, low=True, eave='dark_oak_slab')
    # Ground floor.
    door_frame(b, 8, 2, 6)
    b.door(8, 2, 6, facing='south', wood='acacia')
    for x in (5, 11):
        hp.glazed(b, x, 3, 6, 'north', sill=False, shutters=None)
    for z in (8, 11):
        hp.glazed(b, 3, 3, z, 'west')
    hp.glazed(b, 13, 3, 8, 'east')
    for x in (6, 10):
        hp.glazed(b, x, 3, 13, 'south')
    parts.stair_run(b, 12, 12, 2, 4, 'north', wood='acacia')
    kitchen(b, [(4, 12), (5, 12), (6, 12), (4, 7), (4, 11)], 2, 'north', rng)
    parts.rug(b, 6, 8, 10, 10, 2, 'orange', border='brown')
    b.custom(8, 2, 9, 'tavern_table')
    b.custom(7, 2, 9, 'tavern_chair', facing='east')
    b.custom(9, 2, 9, 'tavern_chair', facing='west')
    hp.lantern(b, 8, 4, 10)
    hp.lantern(b, 8, 4, 4)
    # Upstairs: a hall along the stairs and two bedrooms off it.
    uy = 6
    for z in range(7, 13):
        for yy in (6, 7, 8):
            b.set(10, yy, z, 'acacia_planks')
    for x in range(4, 10):
        for yy in (6, 7, 8):
            b.set(x, yy, 10, 'acacia_planks')
    b.door(10, uy, 8, facing='east', wood='acacia')
    b.door(10, uy, 11, facing='east', wood='acacia')
    b.door(6, uy, 6, facing='south', wood='acacia')
    b.bed(5, uy, 8, 'west', 'orange')
    b.chest(4, uy, 7, 'east', loot=LOOT)
    hp.pot(b, 9, uy, 7)
    hp.lantern(b, 7, 8, 8)
    b.room('bedroom_gallery', (8, 7, 8))
    b.bed(5, uy, 11, 'west', 'red')
    b.bed(5, uy, 12, 'west', 'yellow')
    b.chest(9, uy, 12, 'west', loot=LOOT)
    b.custom(8, uy, 12, 'fireside_armchair', facing='west')
    hp.lantern(b, 7, 8, 11)
    b.room('bedroom_back', (7, 7, 12))
    for z in (8, 11):
        hp.glazed(b, 3, 7, z, 'west', shutters=None)
    hp.glazed(b, 13, 7, 10, 'east', shutters=None)
    for x in (5, 8):
        hp.glazed(b, x, 7, 13, 'south', sill=False, shutters=None)
    hp.lantern(b, 11, 8, 8)
    hp.lantern(b, 8, 8, 4)
    b.custom(11, uy, 4, 'village_bench', facing='north')
    hp.pot(b, 4, uy, 4, plant='potted_acacia_sapling')
    b.resident(6, 2, 8)
    b.resident(10, 2, 11, child=True)
    # Yard.
    hp.path(b, 8, 0, 2, rng)
    b.entrance(8)
    b.custom(6, 1, 1, 'house_plaque', facing='north')
    hp.post_lantern(b, 11, 1, 1)
    hp.drying_rack(b, 1, 15, 'x', length=4, face='north')
    parts.woodpile(b, 11, 1, 15, 'x', length=4, wood='acacia')
    hp.yard(b, {(x, z) for x in range(0, 17) for z in range(0, 17)}, rng, tufts=.1)
    b.natural_ground()
    return b


def compound():
    """Walled family compound: a thatched mud house, a granary on stilts and a shaded court."""
    rng = random.Random(3107)
    b = Build('savanna/compound', (19, 13, 20))
    # Outer wall with a timber gateway.
    wall = [(x, z) for x, z, _, _ in parts.ring(0, 2, 18, 19) if not (z == 2 and 8 <= x <= 10)]
    hp.mud_wall(b, wall, 1, 2, mat='mud_bricks', cap='mud_brick_wall')
    for x in (7, 11):
        for yy in range(1, 5):
            b.set(x, yy, 2, 'stripped_acacia_log', axis='y')
    for x in range(7, 12):
        b.set(x, 4, 2, 'stripped_acacia_log', axis='x')
        b.set(x, 5, 2, 'acacia_slab', type='bottom', waterlogged=False)
    b.set(9, 3, 2, 'lantern', hanging=True, waterlogged=False)
    for x in (6, 12):
        b.set(x, 4, 2, 'acacia_slab', type='bottom', waterlogged=False)
    # Court floor.
    for x in range(1, 18):
        for z in range(3, 19):
            b.set(x, 0, z, rng.choice(['packed_mud', 'coarse_dirt', 'coarse_dirt', 'dirt_path', 'packed_mud']))
    # Main house along the back wall, thatched.
    st = STYLES['mud']
    body = Body(b, 2, 12, 12, 18, st, heights=(3,), spacing=5).build()
    hp.thatch_hip(b, 2, 12, 12, 18, 5, overhang=1, fringe='acacia_trapdoor', cap='acacia_slab')
    door_frame(b, 6, 2, 12)
    b.door(6, 2, 12, facing='south', wood='acacia')
    for x in (4, 9):
        hp.slit(b, x, 3, 12)
    hp.slit(b, 2, 3, 15)
    for z in range(13, 18):
        for yy in (2, 3, 4):
            b.set(8, yy, z, 'mud_bricks')
    b.door(8, 2, 15, facing='east', wood='acacia')
    b.bed(11, 2, 14, 'north', 'red')
    b.bed(11, 2, 16, 'south', 'orange')
    b.chest(9, 2, 17, 'north', loot=LOOT)
    hp.slit(b, 12, 3, 15)
    hp.lantern(b, 10, 4, 15)
    b.room('bedroom', (10, 3, 15))
    kitchen(b, [(3, 17), (4, 17), (5, 17), (3, 13), (3, 16)], 2, 'north', rng)
    hp.low_table(b, 5, 2, 15)
    hp.stool(b, 6, 2, 15)
    hp.lantern(b, 5, 4, 14)
    # Granary on stilts in the front-east corner.
    gx, gz = 15, 7
    for x, z in ((14, 6), (16, 6), (14, 8), (16, 8)):
        b.set(x, 1, z, 'acacia_fence')
    gran = hp.disk(gx, gz, 1.5)
    for x, z in gran:
        b.set(x, 2, z, 'acacia_planks')
        for yy in (3, 4):
            b.set(x, yy, z, 'packed_mud' if (x, z) != (15, 7) else 'hay_block', **({'axis': 'y'} if (x, z) == (15, 7) else {}))
    b.set(15, 3, 6, 'acacia_trapdoor', facing='north', half='bottom', open=False, powered=False, waterlogged=False)
    hp.cone_roof(b, gx, gz, 1.5, 5, set(), eave=1.2, fringe=None)
    b.set(13, 1, 7, 'acacia_slab', type='bottom', waterlogged=False)
    # Court: shade tree, fire, water, grinding stone and a goat corner.
    hp.acacia_tree(b, 3, 1, 6, rng, height=3, lean='east', lean_len=1, canopy=2.6)
    b.custom(4, 1, 8, 'village_bench', facing='north')
    hp.firepit(b, 9, 1, 8, benches=('west', 'east', 'south'))
    b.set(16, 1, 11, 'water_cauldron', level=3)
    hp.pot(b, 17, 1, 11)
    hp.pot(b, 13, 1, 17)
    hp.drying_rack(b, 14, 15, 'x', length=4, face='north')
    hp.post_lantern(b, 12, 1, 9)
    b.resident(5, 2, 14)
    b.resident(10, 2, 15, child=True)
    # Street.
    hp.path(b, 9, 0, 3, rng)
    b.entrance(9)
    b.custom(5, 1, 1, 'house_plaque', facing='north')
    b.natural_ground()
    return b


def longhouse():
    """Long mud house with a dark timber roof and a shaded side workshop."""
    rng = random.Random(3108)
    st = STYLES['mud']
    b = Build('savanna/longhouse', (18, 11, 14))
    body = Body(b, 1, 4, 13, 9, st, heights=(3,), spacing=4).build()
    hp.hip_roof(b, 1, 4, 13, 9, 5, ROOFS['dark'], overhang=1)
    # Lean-to on the east end.
    for z in (4, 9):
        for yy in (1, 2, 3):
            b.set(16, yy, z, 'acacia_fence')
    for z in range(3, 11):
        b.set(15, 4, z, 'acacia_slab', type='bottom', waterlogged=False)
        b.set(16, 4, z, 'acacia_slab', type='bottom', waterlogged=False)
    parts.woodpile(b, 15, 1, 6, 'z', length=3, wood='acacia')
    b.set(16, 1, 6, 'hay_block', axis='y')
    hp.pot(b, 16, 1, 8)
    # Openings.
    door_frame(b, 9, 2, 4)
    hp.door(b, 9, 2, 4, 'north', step='mud_brick_stairs')
    for x in (3, 6, 12):
        hp.glazed(b, x, 3, 4, 'north')
    for x in (4, 10):
        hp.glazed(b, x, 3, 9, 'south')
    hp.glazed(b, 1, 3, 6, 'west', shutters=None)
    # Bedroom on the west behind a partition.
    for z in range(5, 9):
        for yy in (2, 3, 4):
            b.set(6, yy, z, 'dark_oak_planks')
    b.door(6, 2, 7, facing='east', wood='acacia')
    b.bed(3, 2, 5, 'west', 'brown')
    b.bed(3, 2, 8, 'west', 'orange')
    b.chest(5, 2, 5, 'south', loot=LOOT)
    hp.lantern(b, 4, 4, 6)
    b.room('bedroom', (4, 3, 7))
    # Living room and kitchen.
    kitchen(b, [(12, 8), (11, 8), (12, 5), (7, 8), (12, 6)], 2, 'west', rng)
    b.custom(9, 2, 7, 'tavern_table')
    b.custom(8, 2, 7, 'tavern_chair', facing='east')
    b.custom(10, 2, 7, 'tavern_chair', facing='west')
    hp.lantern(b, 9, 4, 6)
    b.resident(9, 2, 6)
    b.resident(4, 2, 6)
    # Street side.
    hp.path(b, 9, 0, 3, rng)
    b.entrance(9)
    b.custom(7, 1, 2, 'house_plaque', facing='north')
    hp.firepit(b, 3, 1, 1, benches=('east',))
    hp.pot(b, 13, 1, 2)
    hp.post_lantern(b, 11, 1, 2)
    hp.drying_rack(b, 2, 12, 'x', length=5, face='north')
    hp.yard(b, {(x, z) for x in range(0, 18) for z in range(0, 14)}, rng, tufts=.1)
    b.natural_ground()
    return b


DESIGNS = {
    'savanna/hut_round': hut_round,
    'savanna/homestead': homestead,
    'savanna/hut_family': hut_family,
    'savanna/bungalow_verandah': bungalow_verandah,
    'savanna/bungalow_clay': bungalow_clay,
    'savanna/lodge': lodge,
    'savanna/compound': compound,
    'savanna/longhouse': longhouse,
}
