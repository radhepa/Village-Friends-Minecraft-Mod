"""Town centres: a 33x33 square ringed by the guaranteed civic buildings.

Each side has, in pinwheel order, a large slot (up to 17 wide), a street exit
and a small slot (up to 11 wide). Slots are jigsaws into the role pools, so
every village gets the tavern, garrison, workshop, chapel, apothecary and
library facing the square. Slots have a higher selection priority than the
exits, so civic buildings are placed before the street network grows. The
whole start piece rotates randomly in the world.
"""
import math
import random

from ..kit import Build, DIRS
from ..roads import noise, smooth
from .. import parts

SIZE = 33
C = 16
# (side facing, big slot, exit, small slot) in plaza coordinates, pinwheel order.
SIDES = {
    'north': ((8, 0), (19, 0), (27, 0)),
    'east': ((32, 8), (32, 19), (32, 27)),
    'south': ((24, 32), (13, 32), (5, 32)),
    'west': ((0, 24), (0, 13), (0, 5)),
}
EXIT_SPAN = {'north': ('x', 17, 21), 'east': ('z', 17, 21), 'south': ('x', 11, 15), 'west': ('z', 11, 15)}


def stone(x, z, seed):
    n = smooth(x, z, seed, 2.5) * .6 + noise(x, z, seed + 5) * .4
    if n < .14:
        return 'mossy_stone_bricks'
    if n < .22:
        return 'cracked_stone_bricks'
    if n < .55:
        return 'stone_bricks'
    if n < .7:
        return 'cobblestone'
    if n < .82:
        return 'andesite'
    if n < .9:
        return 'polished_andesite'
    return 'gravel'


def base(name, roles, seed, ring=9.5, height=14):
    """Paving, lawns, slots and exits shared by every town centre."""
    b = Build(name, (SIZE, height, SIZE))
    rng = random.Random(seed)
    for x in range(SIZE):
        for z in range(SIZE):
            r = math.hypot(x - C, z - C)
            edge = min(x, z, SIZE - 1 - x, SIZE - 1 - z)
            road = False
            for side, (axis, lo, hi) in EXIT_SPAN.items():
                u = x if axis == 'x' else z
                if lo <= u <= hi:
                    v = z if axis == 'x' else x
                    if (side in ('north', 'west') and v <= C) or (side in ('south', 'east') and v >= C):
                        road = True
            if r <= ring + .5 or edge <= 2 or road:
                block = stone(x, z, seed)
                if abs(r - ring) < .55:
                    block = 'polished_andesite'
                b.set(x, 0, z, block)
            else:
                b.set(x, 0, z, 'grass_block')
                roll = rng.random()
                if roll < .16:
                    b.set(x, 1, z, 'short_grass')
                elif roll < .22:
                    b.set(x, 1, z, parts.flowers(rng))
    for side, (big, exit_, small) in SIDES.items():
        b.jigsaw(big[0], 1, big[1], f'{side}_up', 'slot', target='building_entrance',
                 pool=f'buildings/{roles[side][0]}', selection=5)
        b.jigsaw(small[0], 1, small[1], f'{side}_up', 'slot', target='building_entrance',
                 pool=f'buildings/{roles[side][1]}', selection=5)
        b.jigsaw(exit_[0], 1, exit_[1], f'{side}_up', 'plaza_exit', target='street_in', pool='plains/avenues')
    return b, rng


def lamp_ring(b, radius, count, offset=0.0, skip=()):
    for i in range(count):
        a = offset + i * 2 * math.pi / count
        x, z = round(C + radius * math.cos(a)), round(C + radius * math.sin(a))
        if (x, z) in skip:
            continue
        b.set(x, 1, z, 'stone_bricks')
        parts.lamp_post(b, x, 2, z, height=2, fence='spruce_fence')


def stall(b, x0, z0, facing, wool, goods, wood='spruce'):
    """Market stall 3 wide x 2 deep with a striped awning; counter faces ``facing``."""
    dx, dz = DIRS[facing]
    lx, lz = DIRS[{'north': 'east', 'east': 'south', 'south': 'west', 'west': 'north'}[facing]]
    front = [(x0 + lx * i, z0 + lz * i) for i in range(3)]
    back = [(x - dx, z - dz) for x, z in front]
    for i, (x, z) in enumerate(front):
        b.set(x, 1, z, f'{wood}_planks' if i != 1 else 'barrel', **({} if i != 1 else {'facing': 'up', 'open': False}))
        b.set(x, 2, z, goods[i % len(goods)])
    for (x, z) in (front[0], front[2], back[0], back[2]):
        for y in range(1 if (x, z) in back else 3, 4):
            b.set(x, y, z, f'{wood}_fence')
    for i, (x, z) in enumerate(front + back):
        color = wool if (i % 3) != 1 else 'white'
        b.set(x, 4, z, f'{color}_wool')
    for x, z in front:
        b.set(x + dx, 4, z + dz, f'{wood}_trapdoor', facing=facing, half='top',
              open=True, powered=False, waterlogged=False)
    bx, bz = back[1]
    b.set(bx, 1, bz, 'barrel', facing='up', open=False)


def bell_frame(b, x, z, along='x'):
    dx, dz = (1, 0) if along == 'x' else (0, 1)
    for s in (-1, 1):
        px, pz = x + dx * s, z + dz * s
        b.set(px, 1, pz, 'cobblestone')
        for y in (2, 3, 4):
            b.set(px, y, pz, 'stripped_spruce_log', axis='y')
    for s in (-1, 0, 1):
        b.set(x + dx * s, 5, z + dz * s, 'stripped_spruce_log', axis=along)
    b.set(x, 6, z, 'spruce_slab', type='bottom')
    b.set(x, 4, z, 'bell', attachment='ceiling', facing='north' if along == 'x' else 'east', powered=False)
    b.set(x, 1, z, 'cobblestone')


def fountain(b, cx=C, cz=C):
    for x in range(cx - 5, cx + 6):
        for z in range(cz - 5, cz + 6):
            r = math.hypot(x - cx, z - cz)
            if r <= 4.6:
                b.set(x, 0, z, 'stone_bricks')
            if 3.6 < r <= 4.6:
                b.set(x, 1, z, 'stone_bricks')
                b.set(x, 2, z, 'stone_brick_slab', type='bottom')
            elif r <= 3.6:
                b.set(x, 1, z, 'water', level=0)
            if 4.6 < r <= 5.3:
                b.set(x, 1, z, 'stone_brick_stairs', facing={(1, 0): 'west', (-1, 0): 'east', (0, 1): 'north',
                                                             (0, -1): 'south'}[_dir(x - cx, z - cz)], half='bottom')
    # Tiered centre: pedestal, bowl and a spout that spills into the basin.
    b.jigsaw(cx, 1, cz, 'up_north', 'town_start', final='minecraft:chiseled_stone_bricks')
    b.set(cx, 2, cz, 'stone_brick_wall')
    b.set(cx, 3, cz, 'chiseled_stone_bricks')
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        f = {(1, 0): 'west', (-1, 0): 'east', (0, 1): 'north', (0, -1): 'south'}.get((dx, dz))
        if f:
            b.set(cx + dx, 3, cz + dz, 'stone_brick_stairs', facing=f, half='top')
        else:
            b.set(cx + dx, 3, cz + dz, 'stone_brick_slab', type='top')
    b.set(cx, 4, cz, 'water', level=0)


def _dir(dx, dz):
    if abs(dx) >= abs(dz):
        return (1 if dx > 0 else -1, 0)
    return (0, 1 if dz > 0 else -1)


def fountain_square():
    roles = {'north': ('tavern', 'apothecary'), 'east': ('garrison', 'market'),
             'south': ('workshop', 'library'), 'west': ('chapel', 'market')}
    b, rng = base('central_plaza', roles, seed=201)
    fountain(b)
    lamp_ring(b, 7.2, 8, offset=math.pi / 8)
    # Benches facing the fountain.
    for x, z, f in ((16, 9, 'south'), (16, 23, 'north'), (9, 16, 'east'), (23, 16, 'west')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    # Painter's corner (north-west lawn) and the bard's stage (south-east lawn).
    b.custom(7, 1, 7, 'easel_canvas', facing='south')
    b.resident(8, 1, 8, 'painter')
    parts.flower_bed(b, 5, 5, 6, 6, 0, rng, soil='grass_block', density=1)
    parts.oak_tree(b, 6, 1, 10, rng, height=5)
    for x in range(23, 28):
        for z in range(23, 27):
            b.set(x, 1, z, 'spruce_slab', type='bottom')
    b.custom(25, 1, 25, 'music_stand', facing='north')
    b.resident(25, 1, 26, 'bard')
    b.set(23, 2, 26, 'spruce_fence')
    b.set(27, 2, 26, 'spruce_fence')
    parts.lantern(b, 23, 3, 26, hanging=False)
    parts.lantern(b, 27, 3, 26, hanging=False)
    for x in (24, 26):
        b.custom(x, 1, 21, 'village_bench', facing='south')
    parts.oak_tree(b, 28, 1, 21, rng, height=5, wood='birch', leaves='birch_leaves')
    # Market stalls on the north-east lawn and the notice board by the tavern.
    stall(b, 23, 7, 'west', 'yellow', ['pumpkin', 'melon', 'hay_block'])
    stall(b, 23, 11, 'west', 'red', ['barrel[facing=up]', 'composter', 'bee_nest[facing=west]'])
    b.custom(13, 1, 4, 'notice_board', facing='south')
    # Bell (the vanilla meeting point) and a fire pit on the south-west lawn.
    bell_frame(b, 9, 23, along='x')
    b.set(6, 1, 26, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    for (x, z, f) in ((5, 26, 'east'), (7, 26, 'west'), (6, 25, 'south'), (6, 27, 'north')):
        b.custom(x, 1, z, 'campfire_bench', facing=f)
    parts.oak_tree(b, 26, 1, 5, rng, height=6)
    return b


def big_oak(b, cx, cz, rng, y=1):
    """A broad old oak with a 2x2 trunk, buttress roots and branches."""
    for x in (cx, cx + 1):
        for z in (cz, cz + 1):
            for yy in range(y, y + 7):
                b.set(x, yy, z, 'oak_log', axis='y')
    for dx, dz, axis in ((-1, 0, 'x'), (2, 1, 'x'), (0, 2, 'z'), (1, -1, 'z')):
        b.set(cx + dx, y, cz + dz, 'oak_log', axis=axis)
    for dx, dz, axis in ((-1, 0, 'x'), (-2, 0, 'x'), (2, 1, 'x'), (3, 1, 'x'), (1, 2, 'z'), (1, 3, 'z'), (0, -1, 'z'),
                         (0, -2, 'z')):
        b.set(cx + dx, y + 6, cz + dz, 'oak_log', axis=axis)
    centre = (cx + .5, y + 8, cz + .5)
    for xx in range(cx - 6, cx + 8):
        for zz in range(cz - 6, cz + 8):
            for yy in range(y + 5, y + 12):
                dx, dy, dz = xx - centre[0], (yy - centre[1]) * 1.6, zz - centre[2]
                r = (dx * dx + dy * dy + dz * dz) ** .5
                if r <= 5.6 - rng.random() * .9 and b.get(xx, yy, zz)[0] == 'minecraft:air':
                    b.set(xx, yy, zz, 'oak_leaves', persistent=True, distance=1, waterlogged=False)


def gazebo(b, x0, z0, wood='spruce', roof='dark_oak'):
    """5x5 bandstand: raised floor, corner posts, railings and a pyramid roof."""
    for x in range(x0, x0 + 5):
        for z in range(z0, z0 + 5):
            b.set(x, 1, z, f'{wood}_planks' if (x + z) % 2 else 'stripped_spruce_log', axis='x')
            corner = x in (x0, x0 + 4) and z in (z0, z0 + 4)
            edge = x in (x0, x0 + 4) or z in (z0, z0 + 4)
            if corner:
                for y in (2, 3, 4):
                    b.set(x, y, z, f'{wood}_fence')
            elif edge and z != z0:
                b.set(x, 2, z, f'{wood}_fence')
    for i, y in enumerate((5, 6, 7)):
        for x in range(x0 - 1 + i, x0 + 6 - i):
            for z in range(z0 - 1 + i, z0 + 6 - i):
                if x in (x0 - 1 + i, x0 + 5 - i) or z in (z0 - 1 + i, z0 + 5 - i):
                    f = 'south' if z == z0 - 1 + i else 'north' if z == z0 + 5 - i else 'east' if x == x0 - 1 + i else 'west'
                    b.set(x, y, z, f'{roof}_stairs', facing=f, half='bottom')
    b.set(x0 + 2, 8, z0 + 2, f'{roof}_slab', type='bottom')
    b.set(x0 + 2, 7, z0 + 2, f'{roof}_planks')
    b.set(x0 + 2, 6, z0 + 2, 'chain', axis='y')
    b.set(x0 + 2, 5, z0 + 2, 'lantern', hanging=True)
    b.set(x0 + 2, 1, z0 - 1, f'{wood}_stairs', facing='south', half='bottom', lock=True)


def village_green():
    roles = {'north': ('garrison', 'library'), 'east': ('tavern', 'market'),
             'south': ('chapel', 'apothecary'), 'west': ('workshop', 'market')}
    b, rng = base('plaza_green', roles, seed=202, ring=4.5)
    # Grass green in the middle, a ring path, the great oak and a ring bench.
    for x in range(SIZE):
        for z in range(SIZE):
            r = math.hypot(x - C, z - C)
            if 4.5 < r <= 10.5:
                b.set(x, 0, z, 'grass_block')
                b.set(x, 1, z, 'air')
                if rng.random() < .1:
                    b.set(x, 1, z, parts.flowers(rng))
            elif 10.5 < r <= 12 and min(x, z, SIZE - 1 - x, SIZE - 1 - z) > 2:
                b.set(x, 0, z, 'dirt_path' if rng.random() < .7 else 'gravel')
                b.set(x, 1, z, 'air')
            if r <= 4.5:
                b.set(x, 0, z, 'grass_block')
                b.set(x, 1, z, 'air')
    big_oak(b, C, C, rng)
    b.jigsaw(C, 1, C, 'up_north', 'town_start', final='minecraft:oak_log')
    for x in range(C - 3, C + 5):
        for z in range(C - 3, C + 5):
            r = math.hypot(x - C - .5, z - C - .5)
            if 3.1 <= r < 4.1:
                f = 'north' if z < C - 1 else 'south' if z > C + 2 else 'west' if x < C else 'east'
                b.set(x, 1, z, 'spruce_stairs', facing=f, half='bottom', lock=True, shape='straight')
    gazebo(b, 22, 22)
    b.custom(24, 2, 24, 'music_stand', facing='north')
    b.resident(24, 2, 25, 'bard')
    for x in (23, 25):
        b.custom(x, 1, 20, 'village_bench', facing='south')
    b.custom(8, 1, 8, 'easel_canvas', facing='south')
    b.resident(9, 1, 9, 'painter')
    parts.flower_bed(b, 5, 7, 6, 8, 0, rng, soil='grass_block', density=1)
    bell_frame(b, 24, 9, along='z')
    b.custom(13, 1, 4, 'notice_board', facing='south')
    for x, z, f in ((19, 4, 'south'), (4, 19, 'east')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    # Well and a market stall.
    for x in range(6, 9):
        for z in range(23, 26):
            b.set(x, 1, z, 'water' if (x, z) == (7, 24) else 'cobblestone_wall' if (x + z) % 2 else 'mossy_cobblestone',
                  **({'level': 0} if (x, z) == (7, 24) else {}))
    for x, z in ((6, 23), (8, 25)):
        b.set(x, 2, z, 'spruce_fence')
        b.set(x, 3, z, 'spruce_fence')
    for x in range(6, 9):
        for z in range(23, 26):
            b.set(x, 4, z, 'spruce_slab', type='bottom')
    stall(b, 4, 12, 'east', 'orange', ['pumpkin', 'hay_block[axis=y]', 'melon'])
    for x, z in ((6, 26), (26, 6)):
        parts.oak_tree(b, x, 1, z, rng, height=4, wood='birch', leaves='birch_leaves')
    lamp_ring(b, 12.5, 8, offset=math.pi / 8)
    return b


def market_hall(b, x0, z0, x1, z1, y0=1):
    """Open market hall: a timber-framed upper room on stone arches."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            pillar = edge and (x - x0) % 3 == 0 and (z - z0) % 3 == 0 or (x in (x0, x1) and z in (z0, z1))
            if pillar:
                for y in range(y0, y0 + 3):
                    b.set(x, y, z, 'stone_bricks' if y > y0 else 'cobblestone')
            elif edge:
                b.set(x, y0 + 2, z, 'stone_brick_stairs', facing='north' if z == z0 else 'south' if z == z1 else
                      'west' if x == x0 else 'east', half='top', lock=True)
            b.set(x, y0 + 3, z, 'spruce_planks' if not edge else 'stripped_dark_oak_log', axis='x' if z in (z0, z1) else 'z')
    body = parts.Body(b, x0, z0, x1, z1, parts.Style(frame='stripped_dark_oak_log', fill='calcite',
                                                       floor='spruce_planks', roof='slate', trim='dark_oak'),
                      heights=(3,), base=y0 + 3)
    parts.timber_walls(b, x0, z0, x1, z1, y0 + 4, y0 + 6, 'stripped_dark_oak_log', 'calcite', spacing=3)
    parts.beam_ring(b, x0, z0, x1, z1, y0 + 7, 'stripped_dark_oak_log')
    b.fill(x0 + 1, y0 + 7, z0 + 1, x1 - 1, y0 + 7, z1 - 1, 'spruce_planks')
    body.top = y0 + 7
    ridge = parts.gable_roof(b, x0, z0, x1, z1, y0 + 7, parts.ROOFS['slate'], axis='z', gable='calcite')
    for z in range(z0 + 1, z1, 2):
        for x in (x0, x1):
            b.set(x, y0 + 5, z, 'glass_pane')
    for y in range(y0 + 8, y0 + 10):
        b.set((x0 + x1) // 2, y, z0, 'glass_pane')
    b.set((x0 + x1) // 2, ridge + 1, (z0 + z1) // 2, 'lightning_rod', facing='up', powered=False)
    return ridge


def market_square():
    roles = {'north': ('workshop', 'apothecary'), 'east': ('chapel', 'market'),
             'south': ('tavern', 'library'), 'west': ('garrison', 'market')}
    b, rng = base('plaza_market', roles, seed=203, ring=12.5, height=18)
    b.jigsaw(C, 1, C, 'up_north', 'town_start', final='minecraft:cobblestone')
    ridge = market_hall(b, C - 3, C - 4, C + 3, C + 4)
    # Stalls under and around the hall.
    stall(b, C - 2, C - 1, 'east', 'red', ['pumpkin', 'melon', 'hay_block[axis=y]'])
    stall(b, C + 2, C + 1, 'west', 'blue', ['barrel[facing=up]', 'bee_nest[facing=west]', 'composter[level=7]'])
    for (x, z) in ((C - 1, C - 3), (C + 1, C + 3)):
        b.barrel(x, 1, z, 'up')
    stall(b, 8, 9, 'south', 'yellow', ['hay_block[axis=y]', 'pumpkin', 'barrel[facing=up]'])
    stall(b, 24, 23, 'north', 'green', ['melon', 'barrel[facing=up]', 'hay_block[axis=y]'])
    # Small fountain, bell, painter and bard spots.
    for x in range(22, 27):
        for z in range(7, 12):
            r = math.hypot(x - 24, z - 9)
            if 1.5 < r <= 2.6:
                b.set(x, 1, z, 'stone_brick_wall' if (x + z) % 2 else 'stone_bricks')
            elif r <= 1.5:
                b.set(x, 1, z, 'water', level=0)
    b.set(24, 1, 9, 'chiseled_stone_bricks')
    b.set(24, 2, 9, 'water', level=0)
    bell_frame(b, 9, 24, along='x')
    b.custom(6, 1, 18, 'easel_canvas', facing='east')
    b.resident(7, 1, 18, 'painter')
    b.custom(26, 1, 18, 'music_stand', facing='west')
    b.resident(27, 1, 18, 'bard')
    for z in (16, 20):
        b.custom(24, 1, z, 'village_bench', facing='east')
    b.custom(13, 1, 4, 'notice_board', facing='south')
    for x, z, f in ((10, 16, 'east'), (22, 16, 'west')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    for x, z in ((4, 4), (28, 28), (4, 28)):
        b.set(x, 0, z, 'grass_block')
        parts.oak_tree(b, x, 1, z, rng, height=5)
    lamp_ring(b, 9.5, 8, offset=0.3)
    return b


DESIGNS = {'central_plaza': fountain_square, 'plaza_green': village_green, 'plaza_market': market_square}
