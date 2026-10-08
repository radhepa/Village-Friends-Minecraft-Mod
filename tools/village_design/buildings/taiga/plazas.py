"""Taiga town centres: 33x33 squares with the plains slot and exit layout.

Each centre is built on ``plazas.base`` with the ``taiga/`` prefix, so the civic
slots, exits and their priorities match plains exactly. Centrepieces:

* ``plaza_hearth``  - a mossy stone fire pit under a great log pavilion with a smoke louvre.
* ``plaza_millpond`` - a spring-fed pond with a mossy spring boulder, a log mill and its wheel.
* ``plaza_elder``   - an ancient mega spruce in a mossy grove ringed by benches and lanterns.
"""
import math
import random

from ..plazas import base, bell_frame, stall, C, SIZE
from ... import parts
from ...roads import noise, smooth
from . import core_parts as T


def paving(x, z, seed):
    """Worn flagstones: cobble and mossy stone with gravel and trodden earth."""
    n = smooth(x, z, seed, 2.5) * .6 + noise(x, z, seed + 5) * .4
    if n < .15:
        return 'mossy_cobblestone'
    if n < .27:
        return 'mossy_stone_bricks'
    if n < .5:
        return 'cobblestone'
    if n < .6:
        return 'stone_bricks'
    if n < .7:
        return 'gravel'
    if n < .8:
        return 'coarse_dirt'
    if n < .9:
        return 'andesite'
    return 'cracked_stone_bricks'


def square(name, roles, seed, ring=9.5, height=18):
    return base(name, roles, seed, ring=ring, height=height, prefix='taiga/', paving=paving, lawn='grass_block',
                ring_block='mossy_stone_bricks', plants=False)


def facing_to(x, z, tx, tz):
    dx, dz = tx - x, tz - z
    if abs(dx) >= abs(dz):
        return 'east' if dx > 0 else 'west'
    return 'south' if dz > 0 else 'north'


def hip_roof(b, x0, z0, x1, z1, y, kind='dark_oak', levels=None, hole=0, seed=0, moss=.3):
    """Hipped roof stepping in one block per level; ``hole`` leaves the top levels open."""
    stairs = {'dark_oak': 'dark_oak_stairs', 'spruce': 'spruce_stairs'}[kind]
    k = 0
    while x0 + k <= x1 - k and z0 + k <= z1 - k:
        lx, hx, lz, hz = x0 + k, x1 - k, z0 + k, z1 - k
        if levels is not None and k >= levels:
            break
        if hole and (hx - lx) < hole * 2 + 1:
            break
        for x in range(lx, hx + 1):
            for z in range(lz, hz + 1):
                if x in (lx, hx) or z in (lz, hz):
                    f = 'south' if z == lz else 'north' if z == hz else 'east' if x == lx else 'west'
                    b.set(x, y + k, z, stairs, facing=f, half='bottom')
                elif lx == hx or lz == hz:
                    b.set(x, y + k, z, f'{kind}_slab', type='bottom')
        k += 1
    T.mossify(b, (x0, y, z0, x1, y + k + 1, z1), seed, moss)
    return y + k - 1


def stage(b, x0, z0, x1, z1, y=1):
    """Low log stage: stripped log rim, plank boards."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            rim = x in (x0, x1) or z in (z0, z1)
            b.set(x, y, z, 'stripped_spruce_log' if rim else 'spruce_planks',
                  **({'axis': 'x' if z in (z0, z1) else 'z'} if rim else {}))


def market_stall(b, x0, z0, facing, wool, goods):
    stall(b, x0, z0, facing, wool, goods, wood='spruce')


# -------------------------------------------------------------- plaza_hearth
def hearth_square():
    roles = {'north': ('tavern', 'apothecary'), 'east': ('garrison', 'market'),
             'south': ('workshop', 'library'), 'west': ('chapel', 'market')}
    seed = 4201
    b, rng = square('taiga/plaza_hearth', roles, seed, ring=9.5, height=19)
    # Fire pit: a low ring of mossy stone round the town fire.
    for x in range(C - 3, C + 4):
        for z in range(C - 3, C + 4):
            r = math.hypot(x - C, z - C)
            if r <= 1.5:
                b.set(x, 0, z, 'coarse_dirt' if (x + z) % 2 else 'gravel')
            elif r <= 2.5:
                b.set(x, 0, z, 'mossy_cobblestone')
                b.set(x, 1, z, 'mossy_cobblestone_wall' if (x * 3 + z) % 4 else 'mossy_cobblestone')
            elif r <= 3.3:
                b.set(x, 0, z, 'mossy_stone_bricks' if (x + z) % 3 else 'cobblestone')
    b.jigsaw(C, 1, C, 'up_north', 'town_start', final='minecraft:campfire')
    # Benches round the fire.
    for dx, dz in ((0, -4), (0, 4), (-4, 0), (4, 0), (-3, -3), (3, -3), (-3, 3), (3, 3)):
        b.custom(C + dx, 1, C + dz, 'campfire_bench', facing=facing_to(C + dx, C + dz, C, C))
    for x, z, axis in ((C - 1, C - 5, 'x'), (C - 1, C + 5, 'x'), (C - 5, C - 1, 'z'), (C + 5, C - 1, 'z')):
        T.log_bench(b, x, z, axis, length=3)
    # The great log pavilion: four log posts, braced beams and a hipped roof with a smoke louvre.
    lo, hi = C - 6, C + 6
    for x, z in ((lo, lo), (hi, lo), (lo, hi), (hi, hi)):
        b.set(x, 1, z, 'mossy_cobblestone')
        for y in range(2, 8):
            b.set(x, y, z, 'spruce_log', axis='y')
    for i in range(lo, hi + 1):
        for (x, z, axis) in ((i, lo, 'x'), (i, hi, 'x'), (lo, i, 'z'), (hi, i, 'z')):
            if b.get(x, 7, z)[0] == 'minecraft:air':
                b.set(x, 7, z, 'stripped_spruce_log', axis=axis)
    for x, z in ((lo, lo), (hi, lo), (lo, hi), (hi, hi)):
        sx, sz = (1 if x == lo else -1), (1 if z == lo else -1)
        b.set(x + sx, 6, z, 'spruce_stairs', facing='west' if sx > 0 else 'east', half='top', lock=True)
        b.set(x, 6, z + sz, 'spruce_stairs', facing='north' if sz > 0 else 'south', half='top', lock=True)
    # Cross beams with hanging lanterns.
    for i in range(lo + 1, hi):
        b.set(i, 7, C, 'stripped_spruce_log', axis='x')
    for x in (C - 3, C + 3):
        T.hang_lantern(b, x, 6, C, links=1)
    for x, z in ((C, lo), (C, hi), (lo, C), (hi, C)):
        T.hang_lantern(b, x, 6, z)
    top = hip_roof(b, lo - 1, lo - 1, hi + 1, hi + 1, 8, 'dark_oak', hole=1, seed=seed)
    # Raised louvre over the smoke hole.
    k = top - 8
    hl, hh = lo - 1 + k, hi + 1 - k
    for x, z in ((hl, hl), (hh, hl), (hl, hh), (hh, hh)):
        b.set(x, top + 1, z, 'spruce_fence')
    hip_roof(b, hl - 1, hl - 1, hh + 1, hh + 1, top + 2, 'spruce', seed=seed + 1, moss=.2)
    # Painter's corner (north-west) and the bard's stage (south-east).
    b.custom(6, 1, 7, 'easel_canvas', facing='south')
    b.resident(7, 1, 8, 'painter')
    b.barrel(5, 1, 6, 'up')
    stage(b, 23, 23, 27, 26)
    b.custom(25, 2, 25, 'music_stand', facing='north')
    b.resident(25, 2, 26, 'bard')
    for x in (23, 27):
        b.set(x, 2, 26, 'spruce_fence')
        b.set(x, 3, 26, 'spruce_fence')
        T.stand_lantern(b, x, 4, 26)
    b.set(25, 2, 27, 'spruce_log', axis='y') if b.inside(25, 2, 27) else None
    for x in (24, 26):
        b.custom(x, 1, 21, 'village_bench', facing='south')
    # Notice board on its own log frame by the tavern.
    b.custom(13, 1, 4, 'notice_board', facing='south')
    for x in (12, 14):
        b.set(x, 1, 4, 'spruce_fence')
        b.set(x, 2, 4, 'spruce_fence')
    b.set(13, 3, 4, 'spruce_slab', type='bottom')
    b.set(12, 3, 4, 'spruce_stairs', facing='east', half='bottom')
    b.set(14, 3, 4, 'spruce_stairs', facing='west', half='bottom')
    # Bell in the south-west and a carved totem in the north-east.
    bell_frame(b, 7, 25, along='x', log='stripped_spruce_log', stone='mossy_cobblestone', slab='spruce_slab')
    T.totem(b, 26, 9, facing='west')
    T.totem(b, 4, 20, facing='east', height=6)
    # Fur and berry stalls on the north-east lawn.
    market_stall(b, 24, 13, 'west', 'brown', ['sweet_berry_bush[age=3]', 'barrel[facing=up]', 'pumpkin'])
    T.drying_rack(b, 23, 5, length=3)
    # Woodpile and chopping block by the bell.
    T.woodstack(b, 4, 27, 'x', length=4, height=2)
    T.chopping_block(b, 9, 28)
    # Lanterns round the square.
    for x, z in ((9, 9), (23, 9), (9, 23), (23, 23), (16, 25), (25, 16), (16, 7), (7, 16)):
        if b.get(x, 1, z)[0] == 'minecraft:air':
            T.lamp(b, x, z)
    # Spruces in the corners, then the forest floor.
    for x, z, h in ((4, 4, 8), (28, 4, 9), (28, 28, 8), (4, 23, 7)):
        if b.get(x, 1, z)[0] == 'minecraft:air':
            T.spruce(b, x, z, height=h)
    T.forest_floor(b, rng, seed)
    return b


# ------------------------------------------------------------ plaza_millpond
def water(b, x, z):
    b.set(x, 0, z, 'water', level=0)
    for y in range(1, 3):
        if b.get(x, y, z)[0] != 'minecraft:air':
            b.set(x, y, z, 'air')


def millpond_square():
    roles = {'north': ('workshop', 'library'), 'east': ('tavern', 'market'),
             'south': ('chapel', 'apothecary'), 'west': ('garrison', 'market')}
    seed = 4202
    b, rng = square('taiga/plaza_millpond', roles, seed, ring=11.5, height=18)
    lobe = (15.0, 9.0, 2.2)
    pond = set()
    for x in range(SIZE):
        for z in range(SIZE):
            r = math.hypot(x - C, z - C) + (noise(x, z, seed) - .5) * .6
            if r <= 6.3 or math.hypot(x - lobe[0], z - lobe[1]) <= lobe[2] + .3:
                pond.add((x, z))
    for x, z in pond:
        water(b, x, z)
    # Shore: mud, gravel and moss, with reeds where they can grow.
    for x in range(SIZE):
        for z in range(SIZE):
            if (x, z) in pond:
                continue
            near = any((x + dx, z + dz) in pond for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if not near:
                continue
            n = noise(x, z, seed + 9)
            b.set(x, 0, z, 'mud' if n < .2 else 'gravel' if n < .4 else 'mossy_cobblestone' if n < .55 else
                  'grass_block' if n < .8 else 'coarse_dirt')
            if b.get(x, 0, z)[0] == 'minecraft:grass_block' and rng.random() < .5:
                for y in range(1, 1 + rng.randint(1, 2)):
                    b.set(x, y, z, 'sugar_cane', age=0)
    for x, z in sorted(pond):
        if rng.random() < .1 and math.hypot(x - C, z - C) > 2.5 and abs(x - 14) > 1:
            b.set(x, 1, z, 'lily_pad')
    # The spring boulder in the middle.
    for x in range(C - 1, C + 2):
        for z in range(C - 1, C + 2):
            b.set(x, 0, z, 'mossy_cobblestone')
            b.set(x, 1, z, 'mossy_cobblestone' if (x + z) % 2 == 0 else rng.choice(['cobblestone', 'andesite']))
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        b.set(C + dx, 2, C + dz, 'mossy_cobblestone')
    b.set(C - 1, 3, C, 'mossy_cobblestone_wall')
    b.set(C, 3, C + 1, 'moss_carpet')
    b.set(C + 1, 2, C + 1, 'fern')
    b.set(C - 1, 2, C - 1, 'moss_carpet')
    b.jigsaw(C, 1, C, 'up_north', 'town_start', final='minecraft:mossy_cobblestone')
    b.set(C, 2, C, 'water', level=0)
    # The log mill on the north-west bank, its wheel turning in the pond.
    mx0, mz0, mx1, mz1 = 6, 3, 12, 9
    for x in range(mx0, mx1 + 1):
        for z in range(mz0, mz1 + 1):
            b.set(x, 0, z, 'mossy_cobblestone' if x in (mx0, mx1) or z in (mz0, mz1) else 'spruce_planks')
            for y in range(1, 4):
                b.set(x, y, z, 'air')
    T.log_walls(b, mx0, mz0, mx1, mz1, 1, 4, stubs=True)
    T.ceiling(b, mx0 + 1, mz0 + 1, mx1 - 1, mz1 - 1, 5, 'spruce_planks')
    ridge = T.roof(b, mx0, mz0, mx1, mz1, 4, 'dark_oak', axis='x', pitch=2, gable='spruce_planks', seed=seed)
    b.door(10, 1, mz1, facing='north', wood='spruce')
    b.set(10, 0, mz1 + 1, 'spruce_planks')
    b.set(mx0, 2, 6, 'glass_pane')
    b.set(mx0, 2, 7, 'glass_pane')
    parts.chimney(b, mx0 + 1, mz0, ridge - 2, ridge + 1, 'cobblestone', smoke=False)
    b.set(8, 1, 5, 'grindstone', face='floor', facing='east')
    b.set(11, 1, 5, 'smooth_stone')
    b.set(11, 2, 5, 'smooth_stone_slab', type='bottom')
    b.barrel(7, 1, 7, 'up')
    b.barrel(7, 1, 8, 'up')
    b.set(11, 1, 7, 'hay_block', axis='y')
    b.set(11, 1, 8, 'composter', level=4)
    T.hang_lantern(b, 9, 4, 6)
    # Axle through the east wall and a spoked wheel standing in the water.
    wx, wy, wz = 14, 2, 8
    b.set(mx1, wy, wz, 'stripped_spruce_log', axis='x')
    b.set(mx1 + 1, wy, wz, 'stripped_spruce_log', axis='x')
    b.set(wx, wy, wz, 'spruce_log', axis='x')
    wx += 1
    b.set(wx, wy, wz, 'spruce_log', axis='x')
    for y in range(0, 6):
        for z in range(wz - 4, wz + 5):
            d = math.hypot(y - wy, z - wz)
            if 2.5 <= d <= 3.4:
                b.set(wx, y, z, 'spruce_planks' if (y + z) % 2 else 'stripped_spruce_log', axis='x')
            elif d < 2.5 and (y, z) != (wy, wz) and (y == wy or z == wz):
                b.set(wx, y, z, 'spruce_fence')
    # Woodpile and sacks by the mill, a cart path to the door.
    T.woodstack(b, 4, 4, 'z', length=4, height=2)
    T.chopping_block(b, 3, 9)
    b.barrel(4, 1, 9, 'up')
    # Painter on the north-east bank, painting the mill.
    b.custom(23, 1, 6, 'easel_canvas', facing='west')
    b.resident(24, 1, 6, 'painter')
    # The bard plays from a jetty on the east shore.
    for x in range(20, 24):
        for z in range(14, 17):
            b.set(x, 0, z, 'spruce_planks' if x < 23 else 'stripped_spruce_log', axis='z')
            if b.get(x, 1, z)[0] == 'minecraft:sugar_cane':
                b.set(x, 1, z, 'air')
                b.set(x, 2, z, 'air')
    for x, z in ((20, 14), (20, 16)):
        b.set(x, 1, z, 'spruce_fence')
        T.stand_lantern(b, x, 2, z)
    b.custom(21, 1, 15, 'music_stand', facing='east')
    b.resident(22, 1, 15, 'bard')
    for z in (14, 16):
        b.custom(25, 1, z, 'village_bench', facing='west')
    # Notice board and benches on the west bank.
    b.custom(5, 1, 18, 'notice_board', facing='east')
    for x, z in ((5, 17), (5, 19)):
        b.set(x, 1, z, 'spruce_fence')
    b.custom(9, 1, 21, 'village_bench', facing='east')
    b.custom(23, 1, 22, 'village_bench', facing='north')
    # Bell in the south-east, a stall and drying rack on the south-west lawn.
    bell_frame(b, 25, 26, along='x', log='stripped_spruce_log', stone='mossy_cobblestone', slab='spruce_slab')
    market_stall(b, 4, 22, 'east', 'green', ['barrel[facing=up]', 'sweet_berry_bush[age=3]', 'hay_block[axis=y]'])
    T.totem(b, 27, 21, facing='west', height=6)
    T.drying_rack(b, 4, 27, length=3, hides=('white', 'brown', 'white'))
    # Lanterns on the bank.
    for x, z in ((9, 11), (23, 11), (9, 23), (23, 24), (16, 26), (26, 16), (16, 6), (5, 14)):
        if b.get(x, 1, z)[0] == 'minecraft:air' and (x, z) not in pond:
            T.lamp(b, x, z)
    for x, z, h in ((28, 4, 9), (4, 9, 7), (28, 28, 8), (19, 28, 7)):
        if b.get(x, 1, z)[0] == 'minecraft:air' and b.get(x, 0, z)[0] == 'minecraft:grass_block':
            T.spruce(b, x, z, height=h)
    T.forest_floor(b, rng, seed)
    return b


# --------------------------------------------------------------- plaza_elder
def gazebo(b, x0, z0, seed):
    """Log bandstand: raised plank floor, log posts, rails and a steep mossy hip roof."""
    x1, z1 = x0 + 4, z0 + 4
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            b.set(x, 1, z, 'stripped_spruce_log' if edge else 'spruce_planks',
                  **({'axis': 'x' if z in (z0, z1) else 'z'} if edge else {}))
            if x in (x0, x1) and z in (z0, z1):
                for y in range(2, 6):
                    b.set(x, y, z, 'spruce_log', axis='y')
            elif edge and z != z0:
                b.set(x, 2, z, 'spruce_fence')
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if (x in (x0, x1) or z in (z0, z1)) and b.get(x, 5, z)[0] == 'minecraft:air':
                b.set(x, 5, z, 'stripped_spruce_log', axis='x' if z in (z0, z1) else 'z')
    top = hip_roof(b, x0 - 1, z0 - 1, x1 + 1, z1 + 1, 6, 'dark_oak', seed=seed, moss=.35)
    b.set(x0 + 2, top + 1, z0 + 2, 'spruce_fence')
    b.set(x0 + 2, top + 2, z0 + 2, 'lightning_rod', facing='up', powered=False)
    T.hang_lantern(b, x0 + 2, 4, z0 + 2)
    b.set(x0 + 2, 1, z0 - 1, 'spruce_stairs', facing='south', half='bottom', lock=True)


def elder_square():
    roles = {'north': ('garrison', 'market'), 'east': ('chapel', 'library'),
             'south': ('tavern', 'market'), 'west': ('workshop', 'apothecary')}
    seed = 4203
    b, rng = square('taiga/plaza_elder', roles, seed, ring=4.5, height=30)
    # A grove of moss and podzol round the tree, with a beaten path ring outside it.
    for x in range(SIZE):
        for z in range(SIZE):
            r = math.hypot(x - C - .5, z - C - .5)
            edge = min(x, z, SIZE - 1 - x, SIZE - 1 - z)
            if r <= 3.2:
                b.set(x, 0, z, 'podzol' if noise(x, z, seed) < .5 else 'moss_block')
            elif r <= 4.2:
                b.set(x, 0, z, 'mossy_cobblestone')
                b.set(x, 1, z, 'mossy_cobblestone_wall' if (x + z) % 3 else 'mossy_cobblestone')
            elif r <= 9.6:
                b.set(x, 0, z, 'grass_block')
            elif r <= 11.4 and edge > 2:
                b.set(x, 0, z, 'dirt_path' if noise(x, z, seed + 2) < .6 else
                      'coarse_dirt' if noise(x, z, seed + 3) < .5 else 'gravel')
            if r <= 11.4 and edge > 2 and r > 4.2:
                b.set(x, 1, z, 'air')
    # Gaps in the low wall where the four paths meet the tree.
    for dx, dz in ((0, -4), (1, -4), (0, 5), (1, 5), (-4, 0), (-4, 1), (5, 0), (5, 1)):
        b.set(C + dx, 1, C + dz, 'air')
        b.set(C + dx, 0, C + dz, 'mossy_stone_bricks')
    T.mega_spruce(b, C, C, height=20, rng=rng, crown=7.2)
    b.jigsaw(C, 1, C, 'up_north', 'town_start', final='minecraft:spruce_log')
    for x, z in ((C - 2, C - 2), (C + 3, C - 2), (C - 2, C + 3), (C + 3, C + 3)):
        b.set(x, 1, z, 'fern')
    # Benches facing the tree, between the paths.
    for dx, dz in ((-6, -3), (-3, -6), (7, -3), (4, -6), (-6, 4), (-3, 7), (7, 4), (4, 7)):
        x, z = C + dx, C + dz
        b.custom(x, 1, z, 'village_bench', facing=facing_to(x, z, C + .5, C + .5))
    # Bandstand for the bard on the south-east lawn, painter on the north-west lawn.
    gazebo(b, 22, 22, seed)
    b.custom(24, 2, 24, 'music_stand', facing='north')
    b.resident(24, 2, 25, 'bard')
    b.custom(7, 1, 7, 'easel_canvas', facing='south')
    b.resident(8, 1, 8, 'painter')
    b.barrel(6, 1, 6, 'up')
    # Notice board, bell, totems, a stall and woodcraft corners.
    b.custom(13, 1, 4, 'notice_board', facing='south')
    for x in (12, 14):
        b.set(x, 1, 4, 'spruce_fence')
        b.set(x, 2, 4, 'spruce_fence')
    b.set(13, 3, 4, 'spruce_slab', type='bottom')
    bell_frame(b, 25, 8, along='z', log='stripped_spruce_log', stone='mossy_cobblestone', slab='spruce_slab')
    T.totem(b, 27, 13, facing='west')
    T.totem(b, 5, 19, facing='east', height=6)
    market_stall(b, 5, 26, 'north', 'brown', ['barrel[facing=up]', 'pumpkin', 'sweet_berry_bush[age=3]'])
    T.drying_rack(b, 22, 4, length=3)
    T.woodstack(b, 4, 22, 'z', length=3, height=2)
    T.chopping_block(b, 6, 23)
    # Lanterns round the path ring.
    for i in range(8):
        a = math.pi / 8 + i * math.pi / 4
        x, z = round(C + .5 + 12.4 * math.cos(a)), round(C + .5 + 12.4 * math.sin(a))
        if b.get(x, 1, z)[0] == 'minecraft:air':
            T.lamp(b, x, z, height=2)
    for x, z, h in ((4, 4, 8), (28, 4, 8), (4, 28, 7)):
        if b.get(x, 1, z)[0] == 'minecraft:air':
            T.spruce(b, x, z, height=h)
    T.forest_floor(b, rng, seed, rich=.8)
    return b


DESIGNS = {'taiga/plaza_hearth': hearth_square, 'taiga/plaza_millpond': millpond_square,
           'taiga/plaza_elder': elder_square}
