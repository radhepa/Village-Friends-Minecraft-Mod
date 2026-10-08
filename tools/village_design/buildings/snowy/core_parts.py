"""Northern building parts for the snowy town centres and civic buildings.

Local helpers only (the shared kit and parts stay untouched): log-course walls
with notched corners, steep snow roofs, big stone chimneys with smoke, hearths,
enclosed storm porches, sledges and lanterns on 26.3 ``iron_chain``.
"""
from ...kit import DIRS, OPPOSITE, CLOCKWISE, is_air
from ... import parts

CHAIN = 'iron_chain'


def log_walls(b, x0, z0, x1, z1, y0, y1, log='spruce_log', notch=True, skip=()):
    """Horizontal log courses (a log cabin). Corners alternate axis per course and,
    with ``notch``, the log ends stick out one block like saddle-notched corners."""
    for y in range(y0, y1 + 1):
        even = (y - y0) % 2 == 0
        for x in range(x0, x1 + 1):
            for z in (z0, z1):
                if (x, z) not in skip:
                    b.set(x, y, z, log, axis='x')
        for z in range(z0 + 1, z1):
            for x in (x0, x1):
                if (x, z) not in skip:
                    b.set(x, y, z, log, axis='z')
        for x in (x0, x1):
            for z in (z0, z1):
                b.set(x, y, z, log, axis='x' if even else 'z')
                if not notch:
                    continue
                if even:
                    px, pz, axis = x + (-1 if x == x0 else 1), z, 'x'
                else:
                    px, pz, axis = x, z + (-1 if z == z0 else 1), 'z'
                if b.inside(px, y, pz) and is_air(b.get(px, y, pz)):
                    b.set(px, y, pz, log, axis=axis)


def stone_walls(b, x0, z0, x1, z1, y0, y1, mat='cobblestone', quoin='stone_bricks'):
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        for y in range(y0, y1 + 1):
            b.set(x, y, z, quoin if corner else mat)


def plinth(b, x0, z0, x1, z1, top=1, mat='cobblestone', floor='spruce_planks', skirt='cobblestone_stairs'):
    """Stone plinth up to ``top`` with the floor inside; a sloped stone skirt around it."""
    for y in range(0, top + 1):
        for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
            b.set(x, y, z, mat)
        b.fill(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, floor if y == top else 'dirt')
    if skirt and top >= 1:
        parts.plinth_skirt(b, x0, z0, x1, z1, 0, skirt)


def steep_roof(b, x0, z0, x1, z1, y, roof, axis='x', overhang=1, rake=1, gable='spruce_planks', trim=None):
    """Pitch-2 gable roof that collects snow; ``trim`` (a Roof) edges the rakes."""
    ridge = parts.gable_roof(b, x0, z0, x1, z1, y, roof, axis=axis, overhang=overhang, rake=rake, gable=gable,
                             pitch=2)
    if trim:
        ra, rb = rake if isinstance(rake, tuple) else (rake, rake)
        if axis == 'x':
            edges = [(x, z) for x in (x0 - ra, x1 + rb) for z in range(z0 - overhang, z1 + overhang + 1)]
        else:
            edges = [(x, z) for z in (z0 - ra, z1 + rb) for x in range(x0 - overhang, x1 + overhang + 1)]
        swap = {'minecraft:' + roof.stairs: 'minecraft:' + trim.stairs, 'minecraft:' + roof.slab: 'minecraft:' + trim.slab,
                'minecraft:' + roof.full: 'minecraft:' + trim.full}
        for x, z in edges:
            for yy in range(y, min(b.h, ridge + 2)):
                if not b.inside(x, yy, z):
                    continue
                s = b.get(x, yy, z)
                if s[0] in swap:
                    b.set(x, yy, z, (swap[s[0]], s[1]))
    return ridge


def chimney(b, cells, y0, y1, mat='cobblestone', band='stone_bricks', smoke=True):
    """Big stone stack over ``cells``; a band course near the top and a lit campfire for smoke."""
    for x, z in cells:
        for y in range(y0, y1 + 1):
            b.set(x, y, z, band if y == y1 - 1 else mat, clip=True)
    if smoke:
        x, z = cells[0]
        b.set(x, y1 + 1, z, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False, clip=True)
        for x, z in cells[1:]:
            b.set(x, y1 + 1, z, 'stone_brick_slab', type='bottom', waterlogged=False, clip=True)


def fireplace(b, x, y, z, facing, flue_top, mat='cobblestone', mantel='stone_brick'):
    """Hearth niche against a wall: campfire with stone cheeks, a stair mantel and a flue.

    ``facing`` points into the room. The flue rises from the block above the fire to
    ``flue_top`` with a smoking campfire on top."""
    lx, lz = DIRS[CLOCKWISE[facing]]
    b.set(x, y, z, 'campfire', lit=True, signal_fire=False, facing=facing, waterlogged=False)
    for s in (-1, 1):
        for dy in (0, 1):
            b.set(x + lx * s, y + dy, z + lz * s, mat)
    for s in (-1, 0, 1):
        b.set(x + lx * s, y + 2, z + lz * s, f'{mantel}_stairs', facing=OPPOSITE[facing], half='top', lock=True)
    for yy in range(y + 1, flue_top + 1):
        if yy != y + 2:
            b.set(x, yy, z, mat)
    b.set(x, y + 2, z, mat)
    b.set(x, flue_top + 1, z, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False, clip=True)
    # A hearth stone and two candles on the mantel.
    fx, fz = x + DIRS[facing][0], z + DIRS[facing][1]
    for s in (-1, 1):
        if b.inside(x + lx * s, y + 3, z + lz * s) and is_air(b.get(x + lx * s, y + 3, z + lz * s)):
            b.set(x + lx * s, y + 3, z + lz * s, 'candle', candles=2, lit=True, waterlogged=False)
    return fx, fz


def hang(b, x, y, z, chain=0, soul=False):
    """Hanging lantern at ``y`` with ``chain`` links of 26.3 iron chain above it."""
    for i in range(chain):
        b.set(x, y + 1 + i, z, CHAIN, axis='y', waterlogged=False)
    b.set(x, y, z, 'soul_lantern' if soul else 'lantern', hanging=True, waterlogged=False)


def standing_lantern(b, x, y, z):
    b.set(x, y, z, 'lantern', hanging=False, waterlogged=False)


def lamp_post(b, x, z, y=1, height=3, fence='spruce_fence', base='cobblestone'):
    if base:
        b.set(x, y - 1, z, base)
    for i in range(height):
        b.set(x, y + i, z, fence)
    standing_lantern(b, x, y + height, z)


def arm_lamp(b, x, z, arm, y=1, height=4, fence='spruce_fence', base='cobblestone'):
    """Post with an arm and a hanging lantern (rigid pieces only)."""
    if base:
        b.set(x, y - 1, z, base)
    for i in range(height + 1):
        b.set(x, y + i, z, fence)
    dx, dz = DIRS[arm]
    b.set(x + dx, y + height, z + dz, fence)
    hang(b, x + dx, y + height - 1, z + dz)


def fill_up(b, cells, y0, mat, limit=None):
    """Fill each column upward from ``y0`` until the first solid block (a partition up to the roof)."""
    top = limit if limit is not None else b.h - 1
    for x, z in cells:
        y = y0
        while y <= top and b.inside(x, y, z) and is_air(b.get(x, y, z)):
            b.set(x, y, z, mat)
            y += 1


def clear(b, x0, y0, z0, x1, y1, z1):
    for x in range(min(x0, x1), max(x0, x1) + 1):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for z in range(min(z0, z1), max(z0, z1) + 1):
                if b.inside(x, y, z):
                    b.set(x, y, z, 'air')


def window(b, x, y, z, out, height=1, width=1, trim='spruce', shutters=True, sill=None, pane='glass_pane'):
    parts.window(b, x, y, z, out, height=height, width=width, trim=trim, shutters=shutters, sill=sill, pane=pane)


def sledge(b, x, z, facing, y=1, wood='spruce', load=('barrel', 'white_wool')):
    """Two-block sledge: a curled stair prow and a slab bed with its load."""
    dx, dz = DIRS[facing]
    b.set(x, y, z, f'{wood}_stairs', facing=OPPOSITE[facing], half='bottom', lock=True, shape='straight',
          waterlogged=False)
    bx, bz = x - dx, z - dz
    if load:
        item = load[0]
        if item == 'barrel':
            b.set(bx, y, bz, 'barrel', facing='up', open=False)
        else:
            b.set(bx, y, bz, item)
        if len(load) > 1:
            b.set(x - 2 * dx, y, z - 2 * dz, load[1] if not load[1].endswith('_slab') else load[1],
                  **({'type': 'bottom'} if load[1].endswith('_slab') else {}))
    else:
        b.set(bx, y, bz, f'{wood}_slab', type='bottom', waterlogged=False)
    b.set(x + dx, y, z + dz, f'{wood}_fence_gate', facing=facing, open=False, powered=False, in_wall=False)


def snow(b, cells, y, rng, chance=0.35, layers=(1, 1, 2)):
    """Drifts of snow layers where the ground below is a full block and the cell is free."""
    for x, z in cells:
        if not b.inside(x, y, z) or not is_air(b.get(x, y, z)) or (x, y, z) in b.grid:
            continue
        below = b.get(x, y - 1, z)
        if below[0] in ('minecraft:snow_block', 'minecraft:grass_block', 'minecraft:dirt', 'minecraft:podzol',
                        'minecraft:coarse_dirt', 'minecraft:stone_bricks', 'minecraft:cobblestone') \
                and rng.random() < chance:
            b.set(x, y, z, 'snow', layers=rng.choice(layers))


def spruce(b, x, y, z, height=8, rng=None):
    """A tall, layered spruce (wider skirts than the shared one)."""
    for i in range(height):
        b.set(x, y + i, z, 'spruce_log', axis='y')
    radii = []
    level = height
    r = 0
    while level >= 2:
        radii.append((level, r))
        r = r + 1 if r < 2 else (1 if r == 3 else r + 1)
        level -= 1
    pattern = [0, 1, 1, 2, 1, 2, 3, 2, 3]
    for i, dy in enumerate(range(height, 1, -1)):
        rr = pattern[min(i, len(pattern) - 1)]
        for dx in range(-rr, rr + 1):
            for dz in range(-rr, rr + 1):
                if abs(dx) + abs(dz) > rr + (1 if rr >= 2 else 0):
                    continue
                if dx == 0 and dz == 0 and dy < height:
                    continue
                px, py, pz = x + dx, y + dy, z + dz
                if b.inside(px, py, pz) and is_air(b.get(px, py, pz)):
                    b.set(px, py, pz, 'spruce_leaves', persistent=True, distance=1, waterlogged=False)
    b.set(x, y + height, z, 'spruce_leaves', persistent=True, distance=1, waterlogged=False, clip=True)
    b.set(x, y + height + 1, z, 'spruce_leaves', persistent=True, distance=1, waterlogged=False, clip=True)


def palisade(b, cells, rng=None, low=3, high=4, footing='cobblestone'):
    """Sharpened spruce stakes on a stone footing: alternating heights, a fence point on each."""
    for i, (x, z) in enumerate(cells):
        b.set(x, 0, z, footing)
        h = high if (x + z) % 2 else low
        for y in range(1, h + 1):
            b.set(x, y, z, 'spruce_log', axis='y')
        b.set(x, h + 1, z, 'spruce_fence')


def bush(b, x, y, z):
    b.set(x, y, z, 'spruce_leaves', persistent=True, distance=1, waterlogged=False)


def banner(b, x, y, z, facing, color='light_blue'):
    b.set(x, y, z, f'{color}_wall_banner', facing=facing)
