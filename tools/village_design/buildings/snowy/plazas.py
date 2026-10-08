"""Snowy town centres: 33x33 squares on the shared plaza frame (same slots and exits as plains).

Packed-snow lawns, frost-grey paving and a warm centrepiece each: a bonfire hearth ring, a frozen
pond turned skating rink with its hut, or a great midwinter spruce hung with lanterns beside a
covered well-house. Every square has the town start, notice board, painter's easel, bard's music
stand, a bell on a spruce-and-stone frame, benches and plenty of lantern light. No open water:
the only water here is ice.
"""
import math
import random

from ...roads import noise, smooth
from ... import parts
from .. import plazas
from ..plazas import C, SIZE
from . import palette
from . import core_parts as cp

R = palette.ROOFS


def paving(x, z, seed):
    n = smooth(x, z, seed, 2.5) * .6 + noise(x, z, seed + 5) * .4
    if n < .12:
        return 'cracked_stone_bricks'
    if n < .4:
        return 'stone_bricks'
    if n < .56:
        return 'cobblestone'
    if n < .68:
        return 'polished_andesite'
    if n < .78:
        return 'gravel'
    if n < .9:
        return 'snow_block'
    return 'andesite'


def frame(name, roles, seed, ring=9.5, height=14):
    b, rng = plazas.base(name, roles, seed, ring=ring, height=height, prefix='snowy/', paving=paving,
                         lawn='snow_block', ring_block='polished_deepslate', plants=False)
    # Frost-bitten grass shows through the snow here and there.
    for x in range(SIZE):
        for z in range(SIZE):
            if b.get(x, 0, z)[0] == 'minecraft:snow_block' and smooth(x, z, seed + 9, 3) < .25:
                b.set(x, 0, z, 'grass_block', snowy=True)
                b.set(x, 1, z, 'snow', layers=1)
    return b, rng


def lawn_cells(b):
    return [(x, z) for x in range(SIZE) for z in range(SIZE)
            if b.get(x, 0, z)[0] in ('minecraft:snow_block', 'minecraft:grass_block')]


def lamp_ring(b, radius, count, offset=0.0, skip=()):
    plazas.lamp_ring(b, radius, count, offset=offset, skip=skip, base='cobblestone', fence='spruce_fence')


def bell(b, x, z, along='x'):
    plazas.bell_frame(b, x, z, along=along, log='stripped_spruce_log', stone='cobblestone', slab='spruce_slab')
    # A little roof over the bell keeps the snow off.
    dx, dz = (1, 0) if along == 'x' else (0, 1)
    for s in (-1, 0, 1):
        f1, f2 = ('south', 'north') if along == 'x' else ('east', 'west')
        b.set(x + dx * s + (0 if along == 'x' else -1), 6, z + dz * s + (-1 if along == 'x' else 0), 'spruce_stairs',
              facing=f1, half='bottom')
        b.set(x + dx * s + (0 if along == 'x' else 1), 6, z + dz * s + (1 if along == 'x' else 0), 'spruce_stairs',
              facing=f2, half='bottom')
        b.set(x + dx * s, 6, z + dz * s, 'spruce_planks')
        b.set(x + dx * s, 7, z + dz * s, 'spruce_slab', type='bottom')
    b.set(x, 1, z, 'cobblestone')


def stage(b, x0, z0, x1, z1, stand, bard, facing, roof=True):
    """Bard's stage: a plank platform with corner posts, lanterns and a snow roof."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, 1, z, 'spruce_slab', type='top')
    for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        for y in (2, 3, 4):
            b.set(x, y, z, 'spruce_fence')
    if roof:
        for x in range(x0 - 1, x1 + 2):
            for z in range(z0 - 1, z1 + 2):
                edge = x in (x0 - 1, x1 + 1) or z in (z0 - 1, z1 + 1)
                b.set(x, 5, z, 'spruce_slab' if edge else 'spruce_planks', **({'type': 'bottom'} if edge else {}))
        cx, cz = (x0 + x1) // 2, (z0 + z1) // 2
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if (x, z) != (cx, cz):
                    b.set(x, 6, z, 'dark_oak_slab', type='bottom')
        b.set(cx, 6, cz, 'dark_oak_planks')
        b.set(cx, 7, cz, 'dark_oak_slab', type='bottom')
        cp.hang(b, cx, 4, cz)
    b.custom(stand[0], 2, stand[1], 'music_stand', facing=facing)
    b.resident(bard[0], 2, bard[1], 'bard')


def snowman(b, x, z, facing='north'):
    b.set(x, 1, z, 'snow_block')
    b.set(x, 2, z, 'snow_block')
    b.set(x, 3, z, 'carved_pumpkin', facing=facing)


def easel(b, x, z, facing, painter):
    b.custom(x, 1, z, 'easel_canvas', facing=facing)
    b.resident(painter[0], 1, painter[1], 'painter')


# ------------------------------------------------------------------ bonfire square
def plaza_hearth():
    """Bonfire square: a great fire in a stone ring, log seats round it, lamps all about."""
    roles = {'north': ('tavern', 'apothecary'), 'east': ('garrison', 'market'),
             'south': ('workshop', 'library'), 'west': ('chapel', 'market')}
    b, rng = frame('snowy/plaza_hearth', roles, seed=3201)
    # The bonfire: nine campfires on a stone hearth inside a wall kerb.
    for x in range(C - 4, C + 5):
        for z in range(C - 4, C + 5):
            r = math.hypot(x - C, z - C)
            if r <= 3.6:
                b.set(x, 0, z, 'stone_bricks' if r > 2.6 else 'cobblestone')
            if r <= 1.5 and (x, z) != (C, C):
                b.set(x, 1, z, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
            elif 1.5 < r <= 2.6:
                b.set(x, 1, z, 'cobblestone_wall')
    b.jigsaw(C, 1, C, 'up_north', 'town_start', final='minecraft:campfire')
    # Log seats round the fire.
    for x, z, f in ((C, C - 4, 'south'), (C, C + 4, 'north'), (C - 4, C, 'east'), (C + 4, C, 'west'),
                    (C - 3, C - 3, 'south'), (C + 3, C + 3, 'north'), (C - 3, C + 3, 'east'), (C + 3, C - 3, 'west')):
        b.custom(x, 1, z, 'campfire_bench', facing=f)
    # Firewood racks between the seats.
    for x, z, axis in ((C - 2, C - 4, 'x'), (C + 2, C + 4, 'x'), (C - 4, C + 2, 'z'), (C + 4, C - 2, 'z')):
        b.set(x, 1, z, 'spruce_log', axis=axis)
    lamp_ring(b, 7.2, 8, offset=math.pi / 8)
    # Painter's corner (north-west) among spruces.
    easel(b, 7, 7, 'south', (8, 8))
    cp.spruce(b, 5, 1, 9, height=7)
    cp.spruce(b, 10, 1, 5, height=6)
    b.custom(6, 1, 5, 'village_bench', facing='east')
    # The bard's stage (south-east).
    stage(b, 23, 23, 27, 26, (25, 25), (25, 26), 'north')
    for x in (24, 26):
        b.custom(x, 1, 21, 'village_bench', facing='south')
    cp.spruce(b, 28, 1, 21, height=6)
    # Hot cider and roast chestnut stalls (north-east).
    plazas.stall(b, 23, 7, 'west', 'light_blue', ['barrel[facing=up]', 'smoker[facing=west,lit=true]', 'barrel[facing=up]'])
    plazas.stall(b, 23, 11, 'west', 'white', ['white_wool', 'brown_wool', 'light_gray_wool'])
    parts.woodpile(b, 27, 1, 5, 'z', length=4, height=2)
    cp.spruce(b, 27, 1, 13, height=6)
    # Notice board by the tavern and the bell (south-west) with a sledge beside it.
    b.custom(13, 1, 4, 'notice_board', facing='south')
    bell(b, 9, 23, along='x')
    cp.sledge(b, 6, 27, 'north', load=('barrel', 'white_wool'))
    snowman(b, 5, 19, 'east')
    cp.spruce(b, 9, 1, 28, height=5)
    for x, z, f in ((16, 9, 'south'), (9, 16, 'east'), (23, 16, 'west')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    return b


# ------------------------------------------------------------------ frozen pond
def skating_hut(b, x0, z0, x1, z1):
    """Little log hut where skaters warm up: benches, a stove, a smoking chimney and a snow roof."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, 0, z, 'cobblestone' if x in (x0, x1) or z in (z0, z1) else 'spruce_planks')
            for y in range(1, 9):
                b.set(x, y, z, 'air')
    cp.log_walls(b, x0, z0, x1, z1, 1, 3)
    parts.beam_ring(b, x0, z0, x1, z1, 4, 'stripped_spruce_log')
    b.fill(x0 + 1, 4, z0 + 1, x1 - 1, 4, z1 - 1, 'spruce_planks')
    ridge = cp.steep_roof(b, x0, z0, x1, z1, 4, R['dark_oak'], axis='x', gable='spruce_planks')
    door = (x0 + 2, z0)
    b.door(door[0], 1, z0, facing='south', wood='spruce')
    b.set(x0 + 1, 2, z0, 'glass_pane')
    b.set(x1 - 1, 2, z0, 'glass_pane')
    b.set(x0, 2, z0 + 2, 'glass_pane')
    for x in range(x0 + 1, x1):
        if x != door[0]:
            b.custom(x, 1, z1 - 1, 'village_bench', facing='north')
    b.set(x1 - 1, 1, z0 + 1, 'furnace', facing='west', lit=True)
    cp.chimney(b, [(x1, z0 + 1)], 1, ridge)
    cp.hang(b, door[0], 3, z0 + 2)
    return ridge


def plaza_rink():
    """Frozen pond: a packed-ice skating rink inside low boards, an ice carving at its heart,
    spectators' benches round the edge and a warm skating hut on the bank."""
    roles = {'north': ('garrison', 'library'), 'east': ('tavern', 'market'),
             'south': ('chapel', 'apothecary'), 'west': ('workshop', 'market')}
    b, rng = frame('snowy/plaza_rink', roles, seed=3202, ring=10.5)
    gaps = {(C, C - 9), (C, C + 9), (C - 9, C), (C + 9, C)}
    for x in range(C - 10, C + 11):
        for z in range(C - 10, C + 11):
            r = math.hypot(x - C, z - C)
            if r <= 8.2:
                b.set(x, 0, z, 'blue_ice' if r > 7.4 or (r < 1.6) else 'packed_ice')
                b.set(x, 1, z, 'air')
            elif r <= 9.3:
                b.set(x, 0, z, 'stripped_spruce_log', axis='y')
                near_gap = any(abs(x - gx) + abs(z - gz) <= 1 for gx, gz in gaps)
                b.set(x, 1, z, 'air' if near_gap else 'spruce_fence')
    # Ice carving at the heart of the rink.
    b.jigsaw(C, 1, C, 'up_north', 'town_start', final='minecraft:packed_ice')
    b.set(C, 2, C, 'blue_ice')
    b.set(C, 3, C, 'packed_ice')
    b.set(C, 4, C, 'lantern', hanging=False, waterlogged=False)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        b.set(C + dx, 1, C + dz, 'packed_ice')
    for dx, dz in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        b.set(C + dx, 1, C + dz, 'snow', layers=2)
    # Lanterns on posts round the boards, spectators' benches between them.
    for i in range(8):
        a = math.pi / 8 + i * math.pi / 4
        x, z = round(C + 9.8 * math.cos(a)), round(C + 9.8 * math.sin(a))
        cp.lamp_post(b, x, z, height=3, base='cobblestone')
    for x, z, f in ((C - 3, C - 10, 'south'), (C + 3, C + 10, 'north'), (C - 10, C + 3, 'east'),
                    (C + 10, C - 3, 'west')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    # The skating hut on the south-east bank.
    skating_hut(b, 23, 23, 28, 27)
    for x, z in ((21, 23), (22, 28)):
        b.barrel(x, 1, z, 'up')
    # The bard plays on the north-west bank; the painter paints the rink from the north-east.
    stage(b, 4, 5, 7, 7, (6, 6), (6, 7), 'south', roof=True)
    for x in (5, 6):
        b.custom(x, 1, 9, 'village_bench', facing='north')
    easel(b, 26, 9, 'west', (27, 10))
    cp.spruce(b, 27, 1, 5, height=7)
    cp.spruce(b, 23, 1, 4, height=5)
    snowman(b, 25, 13, 'west')
    b.custom(13, 1, 4, 'notice_board', facing='south')
    bell(b, 7, 24, along='z')
    cp.spruce(b, 4, 1, 28, height=6)
    snowman(b, 9, 28, 'north')
    parts.woodpile(b, 4, 1, 19, 'z', length=3, height=2)
    return b


# ------------------------------------------------------------------ midwinter tree
def midwinter_tree(b, cx, cz, rng, y=1, height=17):
    """A great spruce in tiers, hung with lanterns, a shroomlight star on top."""
    for yy in range(y + 1, y + height):
        b.set(cx, yy, cz, 'spruce_log', axis='y')
    tiers = []
    top = y + height
    for yy in range(y + 3, top + 1):
        t = (top - yy) / (top - y - 3)
        r = 0.6 + t * 4.4
        if (yy - y) % 3 == 0:
            r -= 0.9
        tiers.append((yy, r))
    lantern_spots = []
    for yy, r in tiers:
        for x in range(cx - 5, cx + 6):
            for z in range(cz - 5, cz + 6):
                d = math.hypot(x - cx, z - cz)
                if d <= r and (x, z) != (cx, cz) and b.get(x, yy, z)[0] == 'minecraft:air':
                    b.set(x, yy, z, 'spruce_leaves', persistent=True, distance=1, waterlogged=False)
                    if r - 1 < d <= r and yy < top - 2:
                        lantern_spots.append((x, yy, z))
    rng.shuffle(lantern_spots)
    hung = 0
    for x, yy, z in lantern_spots:
        if hung >= 18:
            break
        if b.get(x, yy - 1, z)[0] == 'minecraft:air' and yy - 1 > y + 1:
            b.set(x, yy - 1, z, 'lantern', hanging=True, waterlogged=False)
            hung += 1
    b.set(cx, top + 1, cz, 'shroomlight')
    return top + 1


def well_house(b, x0, z0):
    """Covered well-house: a stone curb over a frozen shaft, four posts and a steep slate cap."""
    cx, cz = x0 + 2, z0 + 2
    for x in range(x0, x0 + 5):
        for z in range(z0, z0 + 5):
            b.set(x, 0, z, 'stone_bricks')
    for x in range(cx - 1, cx + 2):
        for z in range(cz - 1, cz + 2):
            if (x, z) == (cx, cz):
                b.set(x, 0, z, 'blue_ice')
            else:
                b.set(x, 1, z, 'cobblestone_wall' if (x + z) % 2 else 'stone_bricks')
    for x, z in ((x0, z0), (x0 + 4, z0), (x0, z0 + 4), (x0 + 4, z0 + 4)):
        for y in (1, 2, 3):
            b.set(x, y, z, 'stripped_spruce_log', axis='y')
    parts.beam_ring(b, x0, z0, x0 + 4, z0 + 4, 4, 'spruce_log')
    parts.pyramid_roof(b, x0 - 1, z0 - 1, x0 + 5, z0 + 5, 5, 'deepslate_tile_stairs', 'deepslate_tiles', pitch=2,
                       finial=['spruce_fence'])
    b.fill(x0 + 1, 4, z0 + 1, x0 + 3, 4, z0 + 3, 'spruce_planks')
    b.set(cx, 3, cz, 'iron_chain', axis='y')
    b.set(cx, 2, cz, 'cauldron')
    cp.hang(b, x0 + 1, 3, z0 + 1)
    cp.hang(b, x0 + 3, 3, z0 + 3)


def plaza_midwinter():
    """Midwinter square: a great lantern-hung spruce ringed by gifts and benches, a covered
    well-house, a Yule market and the bard's stage."""
    roles = {'north': ('workshop', 'apothecary'), 'east': ('chapel', 'market'),
             'south': ('tavern', 'library'), 'west': ('garrison', 'market')}
    b, rng = frame('snowy/plaza_midwinter', roles, seed=3203, ring=9.5, height=22)
    for x in range(C - 6, C + 7):
        for z in range(C - 6, C + 7):
            r = math.hypot(x - C, z - C)
            if r <= 5.6:
                b.set(x, 0, z, 'snow_block' if r <= 2.2 else 'podzol' if r <= 3.2 else 'stone_bricks')
                b.set(x, 1, z, 'air')
    b.jigsaw(C, 1, C, 'up_north', 'town_start', final='minecraft:spruce_log')
    midwinter_tree(b, C, C, rng)
    # Gifts under the tree.
    for (x, z), wool in zip(((C - 2, C - 1), (C + 2, C + 1), (C + 1, C - 2), (C - 1, C + 2), (C + 2, C - 2),
                             (C - 2, C + 2)), ('red_wool', 'green_wool', 'white_wool', 'red_wool', 'light_blue_wool',
                                               'green_wool')):
        b.set(x, 1, z, wool)
    # Low ring of spruce fence with four gaps, benches facing the tree.
    for x in range(C - 6, C + 7):
        for z in range(C - 6, C + 7):
            r = math.hypot(x - C, z - C)
            if 4.6 < r <= 5.4 and abs(x - C) > 1 and abs(z - C) > 1:
                b.set(x, 1, z, 'spruce_fence')
    for x, z, f in ((C - 1, C - 7, 'south'), (C + 1, C + 7, 'north'), (C - 7, C + 1, 'east'), (C + 7, C - 1, 'west')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    lamp_ring(b, 8.4, 8, offset=math.pi / 8)
    # Covered well-house on the north-east lawn.
    well_house(b, 23, 5)
    # Yule market on the south-west lawn.
    plazas.stall(b, 5, 20, 'east', 'red', ['barrel[facing=up]', 'white_wool', 'pumpkin'])
    plazas.stall(b, 5, 25, 'east', 'green', ['brown_wool', 'barrel[facing=up]', 'hay_block[axis=y]'])
    cp.sledge(b, 9, 28, 'east', load=('barrel', 'spruce_slab'))
    # Stage (south-east), easel (north-west), bell, notice board.
    stage(b, 23, 24, 27, 27, (25, 26), (25, 27), 'north')
    for x in (24, 26):
        b.custom(x, 1, 22, 'village_bench', facing='south')
    easel(b, 7, 7, 'south', (8, 8))
    cp.spruce(b, 5, 1, 5, height=6)
    snowman(b, 10, 6, 'south')
    b.custom(13, 1, 4, 'notice_board', facing='south')
    bell(b, 26, 13, along='z')
    cp.spruce(b, 28, 1, 28, height=5)
    cp.spruce(b, 4, 1, 28, height=5)
    return b


DESIGNS = {
    'snowy/plaza_hearth': plaza_hearth,
    'snowy/plaza_rink': plaza_rink,
    'snowy/plaza_midwinter': plaza_midwinter,
}
