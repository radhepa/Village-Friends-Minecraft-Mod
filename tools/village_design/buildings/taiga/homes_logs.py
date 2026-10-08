"""Shared drawing helpers for the taiga homes, workshops, farms and decorations.

Taiga buildings are true log construction: horizontal spruce logs laid in
courses, saddle-notched corners whose log ends stick out on alternate courses,
rubble foundations of mossy cobblestone, steep roofs with moss creeping over
them and stone hearths with tall chimneys. Nothing here owns a design; the
design modules combine these parts in their own way.
"""
from ...kit import DIRS, OPPOSITE, CLOCKWISE, is_air, block
from ... import parts
from ...parts import log, gable_roof
from .palette import ROOFS, LOOT

LEAVES = dict(persistent=True, distance=1, waterlogged=False)


# ----------------------------------------------------------------- foundations
def rubble(b, x0, z0, x1, z1, rng, top=1, floor='spruce_planks', y0=0, mix=None):
    """Mossy rubble plinth from ``y0`` to ``top`` with the floor laid at ``top``."""
    mix = mix or ['mossy_cobblestone', 'mossy_cobblestone', 'cobblestone', 'cobblestone', 'stone', 'andesite']
    for y in range(y0, top + 1):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if x in (x0, x1) or z in (z0, z1):
                    b.set(x, y, z, rng.choice(mix))
                else:
                    b.set(x, y, z, floor if y == top else 'dirt')


def stone_skirt(b, x0, z0, x1, z1, y, rng, chance=.35, skip=()):
    """Loose mossy stones and stair 'rocks' leaning on the foundation."""
    for x, z, facing, corner in parts.ring(x0 - 1, z0 - 1, x1 + 1, z1 + 1):
        if (x, z) in skip or not b.inside(x, y, z) or not is_air(b.get(x, y, z)) or rng.random() > chance:
            continue
        if corner:
            b.set(x, y, z, 'mossy_cobblestone')
        else:
            b.set(x, y, z, 'mossy_cobblestone_stairs', facing=OPPOSITE[facing], half='bottom')


# ----------------------------------------------------------------- log walls
def log_walls(b, x0, z0, x1, z1, y0, y1, wood='spruce_log', chink=None, notch=True, sides=None):
    """Horizontal log walls with saddle-notched, crossed corners.

    On even courses the north/south logs run through the corners and stick
    out one block east and west; on odd courses the east/west logs do. The
    result is the staggered log-end pattern of a real cabin corner.
    ``chink`` swaps every other course for a lighter log (chinking stripes).
    ``sides`` limits the walls drawn (subset of north/south/east/west).
    """
    sides = set(sides or ('north', 'south', 'east', 'west'))
    for i, y in enumerate(range(y0, y1 + 1)):
        through_x = i % 2 == 0
        mat = chink if chink and i % 2 == 1 else wood
        for x in range(x0, x1 + 1):
            for z, side in ((z0, 'north'), (z1, 'south')):
                if side in sides:
                    b.set(x, y, z, log(mat, 'x'))
        for z in range(z0 + 1, z1):
            for x, side in ((x0, 'west'), (x1, 'east')):
                if side in sides:
                    b.set(x, y, z, log(mat, 'z'))
        for x in (x0, x1):
            for z in (z0, z1):
                ns = 'north' if z == z0 else 'south'
                ew = 'west' if x == x0 else 'east'
                if ns not in sides and ew not in sides:
                    continue
                b.set(x, y, z, log(wood, 'x' if through_x else 'z'))
                if not notch:
                    continue
                if through_x and ns in sides:
                    b.set(x + (-1 if x == x0 else 1), y, z, log(wood, 'x'), clip=True)
                elif not through_x and ew in sides:
                    b.set(x, y, z + (-1 if z == z0 else 1), log(wood, 'z'), clip=True)


def ceiling(b, x0, z0, x1, z1, y, mat='spruce_planks'):
    b.fill(x0, y, z0, x1, y, z1, mat)


def partition_x(b, x, z0, z1, y0, y1, mat='spruce_planks'):
    for z in range(z0, z1 + 1):
        for y in range(y0, y1 + 1):
            b.set(x, y, z, mat)


def partition_z(b, z, x0, x1, y0, y1, mat='spruce_planks'):
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            b.set(x, y, z, mat)


def seal_up(b, cells, y0, mat='spruce_planks', limit=40):
    """Fill each (x, z) column from ``y0`` upward until something solid (the roof) is met."""
    for x, z in cells:
        y = y0
        while y < y0 + limit and b.inside(x, y, z) and is_air(b.get(x, y, z)):
            b.set(x, y, z, mat)
            y += 1


# ----------------------------------------------------------------- openings
def window(b, x, y, z, out, height=1, width=1, shutters=True, box=None, trim='spruce'):
    parts.window(b, x, y, z, out, height=height, width=width, trim=trim, shutters=shutters, box=box)


def door(b, x, y, z, out, wood='spruce', step='spruce_stairs', hinge='left', lamp=True):
    """Front door in a wall facing ``out`` with a plank step and a lantern bracket beside it."""
    dx, dz = DIRS[out]
    b.door(x, y, z, facing=OPPOSITE[out], wood=wood, hinge=hinge)
    if step:
        b.set(x + dx, y - 1, z + dz, step, facing=OPPOSITE[out], half='bottom', lock=True)
    if lamp:
        lx, lz = DIRS[CLOCKWISE[out]]
        for side in (1, -1):
            px, pz = x + dx + lx * side, z + dz + lz * side
            if b.inside(px, y + 1, pz) and is_air(b.get(px, y + 1, pz)) \
                    and not is_air(b.get(x + lx * side, y + 1, z + lz * side)):
                b.set(px, y + 1, pz, 'wall_torch', facing=out)
                break


# ----------------------------------------------------------------- roofs
def roof(b, x0, z0, x1, z1, y, kind='dark_oak', axis='x', pitch=1, overhang=1, rake=1, gable='spruce_planks',
         trim=None):
    """Gable roof whose eaves start at the top wall course ``y``. Returns the ridge Y."""
    r = ROOFS[kind] if isinstance(kind, str) else kind
    ridge = gable_roof(b, x0, z0, x1, z1, y, r, axis=axis, overhang=overhang, rake=rake, gable=gable,
                       pitch=pitch)
    if trim:
        _trim_rakes(b, x0, z0, x1, z1, y, r, ROOFS[trim], axis, rake)
    return ridge


def _trim_rakes(b, x0, z0, x1, z1, y, r, t, axis, rake):
    ra, rb = rake if isinstance(rake, tuple) else (rake, rake)
    swap = {'minecraft:' + r.stairs: 'minecraft:' + t.stairs, 'minecraft:' + r.slab: 'minecraft:' + t.slab,
            'minecraft:' + r.full: 'minecraft:' + t.full}
    if axis == 'x':
        cols = [(x, z) for x in (x0 - ra, x1 + rb) for z in range(z0 - 3, z1 + 4)]
    else:
        cols = [(x, z) for z in (z0 - ra, z1 + rb) for x in range(x0 - 3, x1 + 4)]
    for x, z in cols:
        for yy in range(y, y + 24):
            if b.inside(x, yy, z) and b.get(x, yy, z)[0] in swap:
                s = b.get(x, yy, z)
                b.set(x, yy, z, (swap[s[0]], s[1]))


def moss_roof(b, rng, chance=.12, kinds=('dark_oak', 'spruce'), y_min=3):
    """Moss carpet creeping over roof stairs that face the sky."""
    ids = {'minecraft:' + ROOFS[k].stairs for k in kinds}
    for (x, y, z), s in list(b.grid.items()):
        if y < y_min or s[0] not in ids or dict(s[1]).get('half') != 'bottom':
            continue
        if b.inside(x, y + 1, z) and is_air(b.get(x, y + 1, z)) and rng.random() < chance:
            b.set(x, y + 1, z, 'moss_carpet')


def ridge_horns(b, x, y, z, wood='spruce'):
    """Crossed gable horns: a fence finial with a pair of trapdoor 'antlers'."""
    b.set(x, y, z, f'{wood}_fence', clip=True)


# ----------------------------------------------------------------- hearth
def chimney(b, x, z, y0, y1, rng, smoke=True, base=None):
    """Rubble chimney column; ``base`` (x0, z0, x1, z1) widens the bottom courses into a breast."""
    if base:
        bx0, bz0, bx1, bz1 = base
        for y in range(y0, y0 + 3):
            for bx in range(bx0, bx1 + 1):
                for bz in range(bz0, bz1 + 1):
                    b.set(bx, y, bz, rng.choice(['cobblestone', 'mossy_cobblestone', 'cobblestone']))
    for y in range(y0, y1 + 1):
        b.set(x, y, z, rng.choice(['cobblestone', 'mossy_cobblestone', 'cobblestone', 'stone_bricks']))
    if smoke:
        b.set(x, y1 + 1, z, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)


def hearth(b, x, z, y, inward, rng, top, mantle=True):
    """A stone fireplace set into a wall at (x, z): fire in the wall, chimney stack outside.

    ``inward`` is the direction from the wall into the room. The chimney rises
    behind the wall to ``top`` with a smoking campfire cap.
    """
    dx, dz = DIRS[inward]
    ox, oz = x - dx, z - dz  # chimney stack outside
    lx, lz = DIRS[CLOCKWISE[inward]]
    for side in (-1, 0, 1):
        for yy in (y, y + 1, y + 2):
            b.set(x + lx * side, yy, z + lz * side, rng.choice(['cobblestone', 'mossy_cobblestone', 'stone_bricks']))
        for yy in range(y - 1, y + 2):
            b.set(ox + lx * side, yy, oz + lz * side, rng.choice(['cobblestone', 'mossy_cobblestone']), clip=True)
    b.set(x, y, z, 'campfire', lit=True, signal_fire=False, facing=inward, waterlogged=False)
    b.set(ox, y + 2, oz, 'cobblestone')
    for side in (-1, 1):
        b.set(ox + lx * side, y + 2, oz + lz * side, 'cobblestone_stairs', facing=OPPOSITE[CLOCKWISE[inward]]
              if side == 1 else CLOCKWISE[inward], half='bottom', clip=True)
    for yy in range(y + 1, top + 1):
        b.set(ox, yy, oz, rng.choice(['cobblestone', 'mossy_cobblestone', 'cobblestone']), clip=True)
    b.set(ox, top + 1, oz, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False, clip=True)
    if mantle:
        b.set(x + dx, y + 2, z + dz, 'stone_brick_stairs', facing=OPPOSITE[inward], half='top', lock=True)


# ----------------------------------------------------------------- furniture
def bedroom_lamp(b, x, y, z):
    b.set(x, y, z, 'lantern', hanging=True, waterlogged=False)


def table(b, x, y, z, wood='spruce'):
    parts.table(b, x, y, z, wood=wood)


def chair(b, x, y, z, back, wood='spruce'):
    parts.chair(b, x, y, z, back, wood=wood)


def rug(b, x0, z0, x1, z1, y, color='brown', border='green'):
    parts.rug(b, x0, z0, x1, z1, y, color, border)


def loot_chest(b, x, y, z, facing='south'):
    b.chest(x, y, z, facing, loot=LOOT)


def pot(b, x, y, z, rng):
    b.set(x, y, z, rng.choice(['potted_fern', 'potted_spruce_sapling', 'potted_brown_mushroom',
                               'potted_red_mushroom', 'potted_fern']))


def wall_hide(b, x, y, z, out, color='brown'):
    """A hide pinned to a wall: a wall banner facing ``out`` (away from the wall)."""
    b.set(x, y, z, f'{color}_wall_banner', facing=out)


# ----------------------------------------------------------------- yard
def path(b, x, z0, z1, rng, y=0):
    for z in range(z0, z1 + 1):
        b.set(x, y, z, rng.choice(['dirt_path', 'dirt_path', 'dirt_path', 'coarse_dirt', 'podzol']))


def path_cells(b, cells, rng, y=0):
    for x, z in cells:
        b.set(x, y, z, rng.choice(['dirt_path', 'dirt_path', 'coarse_dirt', 'podzol']))


def berry_bush(b, x, z, rng, y=1):
    b.set(x, y - 1, z, rng.choice(['podzol', 'grass_block']))
    b.set(x, y, z, 'sweet_berry_bush', age=rng.choice([1, 2, 3, 3]))


def fern(b, x, z, rng, y=1, large=False):
    b.set(x, y - 1, z, rng.choice(['podzol', 'grass_block', 'podzol']))
    if large:
        b.set(x, y, z, 'large_fern', half='lower')
        b.set(x, y + 1, z, 'large_fern', half='upper')
    else:
        b.set(x, y, z, rng.choice(['fern', 'fern', 'short_grass', 'brown_mushroom']))


def undergrowth(b, cells, rng, chance=.35, y=1):
    """Ferns, berry bushes and mushrooms on the free yard cells (sets podzol/grass under each)."""
    for x, z in cells:
        if not b.inside(x, y, z) or not is_air(b.get(x, y, z)) or (x, y - 1, z) in b.grid:
            continue
        r = rng.random()
        if r > chance:
            continue
        if r < chance * .18:
            berry_bush(b, x, z, rng, y)
        elif r < chance * .3 and b.inside(x, y + 1, z) and is_air(b.get(x, y + 1, z)):
            fern(b, x, z, rng, y, large=True)
        else:
            fern(b, x, z, rng, y)


def woodpile(b, x, y, z, axis='x', length=3, height=2, roofed=True):
    """Split logs stacked end-out under a slab roof."""
    parts.woodpile(b, x, y, z, along_axis=axis, length=length, wood='spruce', height=height)
    if roofed:
        dx, dz = (1, 0) if axis == 'x' else (0, 1)
        for i in range(length):
            b.set(x + dx * i, y + height, z + dz * i, 'spruce_slab', type='bottom', waterlogged=False)


def chopping_block(b, x, y, z, rng):
    b.set(x, y, z, 'stripped_spruce_log', axis='y')
    b.set(x + 1, y, z, 'spruce_log', axis='x', clip=True) if rng.random() < .5 else None


def drying_rack(b, x0, z, y, length=3, hides=('brown', 'white', 'brown'), axis='x'):
    """Two posts and a rail with hides (carpets) hung over it."""
    dx, dz = (1, 0) if axis == 'x' else (0, 1)
    for i in range(length + 2):
        cx, cz = x0 + dx * i, z + dz * i
        if i in (0, length + 1):
            b.set(cx, y, cz, 'spruce_fence')
            b.set(cx, y + 1, cz, 'spruce_fence')
        else:
            b.set(cx, y + 1, cz, 'spruce_fence')
            b.set(cx, y + 2, cz, f'{hides[(i - 1) % len(hides)]}_carpet')


def spruce(b, x, y, z, height=9, shape=None, clip=True):
    """Hand-drawn spruce: a straight trunk under tiered rings of persistent needles."""
    for i in range(height):
        b.set(x, y + i, z, log('spruce_log'), clip=clip)
    top = y + height
    shape = shape or [0, 1, 1, 2, 1, 2, 3, 2, 3, 2]
    b.set(x, top, z, 'spruce_leaves', clip=clip, **LEAVES)
    b.set(x, top + 1, z, 'spruce_leaves', clip=clip, **LEAVES)
    for j, r in enumerate(shape):
        yy = top - j
        if yy < y + 2:
            break
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if dx * dx + dz * dz > r * r + (1 if r >= 2 else 0):
                    continue
                px, pz = x + dx, z + dz
                if b.inside(px, yy, pz) and is_air(b.get(px, yy, pz)):
                    b.set(px, yy, pz, 'spruce_leaves', **LEAVES)


def lantern_post(b, x, y, z, height=2, base='mossy_cobblestone'):
    parts.lamp_post(b, x, y, z, height=height, fence='spruce_fence', top='lantern', base=base)


def fence_line(b, cells, y=1, wood='spruce'):
    for x, z in cells:
        b.set(x, y, z, f'{wood}_fence')


def gate(b, x, y, z, facing='north', wood='spruce'):
    b.set(x, y, z, f'{wood}_fence_gate', facing=facing, open=False, in_wall=False, powered=False)
