"""Savanna core helpers shared by the town centres, civic buildings and streets.

Acacia trees with flat umbrella canopies, low hipped roofs in acacia or thatch,
deep verandas on posts, sharpened stockades, mud-brick lamps, thatched stalls,
water troughs and the plaza paving. Every helper only draws into a ``Build``.
"""
import math

from ...kit import DIRS, OPPOSITE, CLOCKWISE, is_air
from ...parts import Roof, Style
from ...roads import noise, smooth
from ... import parts
from .palette import ROOFS

# Thatch: woven straw (bamboo mosaic) over hay-bale ridges.
THATCH = Roof('bamboo_mosaic_stairs', 'bamboo_mosaic_slab', 'hay_block')
ACACIA = ROOFS['acacia']
LOOT = 'minecraft:chests/village/village_savanna_house'

# Materials for civic walls; a Style keeps parts.Body happy.
MUD = Style(frame='acacia_log', fill='packed_mud', floor='acacia_planks', roof=ACACIA, base='mud_bricks',
            base_stairs='mud_brick_stairs', trim='acacia', door='acacia', upper_fill='packed_mud',
            ceiling='acacia_planks', accent='dark_oak')
CLAY = Style(frame='stripped_acacia_log', fill='orange_terracotta', floor='acacia_planks', roof=ACACIA,
             base='mud_bricks', base_stairs='mud_brick_stairs', trim='acacia', door='acacia',
             upper_fill='white_terracotta', ceiling='acacia_planks', accent='dark_oak')
WHITE = Style(frame='stripped_acacia_log', fill='white_terracotta', floor='acacia_planks', roof=ACACIA,
              base='brown_terracotta', base_stairs='mud_brick_stairs', trim='acacia', door='acacia',
              upper_fill='white_terracotta', ceiling='acacia_planks', accent='dark_oak')


def leaves(b, x, y, z, kind='acacia_leaves'):
    if b.inside(x, y, z) and is_air(b.get(x, y, z)):
        b.set(x, y, z, kind, persistent=True, distance=1, waterlogged=False)


def canopy(b, cx, cy, cz, r, rng=None, top=None):
    """Flat umbrella canopy: a wide disc of leaves and a smaller cap above."""
    for dx in range(-r - 1, r + 2):
        for dz in range(-r - 1, r + 2):
            d = math.hypot(dx, dz)
            ragged = rng.random() * .6 if rng else .3
            if d <= r + .35 - ragged:
                leaves(b, cx + dx, cy, cz + dz)
    rt = top if top is not None else max(1, r - 2)
    for dx in range(-rt, rt + 1):
        for dz in range(-rt, rt + 1):
            if math.hypot(dx, dz) <= rt + .3:
                leaves(b, cx + dx, cy + 1, cz + dz)


def acacia_tree(b, x, z, rng, y=1, height=3, lean=None, bend=2, radius=2, fork=False):
    """A savanna acacia: short trunk, a diagonal lean, then a flat crown.

    ``fork`` adds a second, lower crown leaning the other way.
    """
    for i in range(height):
        b.set(x, y + i, z, 'acacia_log', axis='y')
    lean = lean or rng.choice(list(DIRS))
    ends = []
    for direction, steps in ((lean, bend),) + (((OPPOSITE[lean], max(1, bend - 1)),) if fork else ()):
        dx, dz = DIRS[direction]
        cx, cy, cz = x, y + height - 1, z
        for _ in range(steps):
            cx, cy, cz = cx + dx, cy + 1, cz + dz
            if b.inside(cx, cy, cz):
                b.set(cx, cy, cz, 'acacia_log', axis='y')
        ends.append((cx, cy, cz))
    for i, (cx, cy, cz) in enumerate(ends):
        canopy(b, cx, cy + 1, cz, radius if i == 0 else max(1, radius - 1), rng)
        if b.inside(cx, cy + 1, cz):
            b.set(cx, cy + 1, cz, 'acacia_log', axis='y')
    return ends


def great_acacia(b, cx, cz, rng, y=1):
    """The meeting tree: a 2x2 trunk with roots and three long limbs under wide flat crowns."""
    for x in (cx, cx + 1):
        for z in (cz, cz + 1):
            for yy in range(y, y + 6):
                b.set(x, yy, z, 'acacia_log', axis='y')
    for dx, dz, axis in ((-1, 0, 'x'), (2, 1, 'x'), (1, -1, 'z'), (0, 2, 'z'), (-1, 1, 'x'), (2, 0, 'x')):
        b.set(cx + dx, y, cz + dz, 'acacia_wood', axis=axis)
    # (start corner, direction, rising steps, level steps, crown radius)
    limbs = (((1, -1), (1, -1), 3, 2, 4), ((-1, 1), (-1, 0), 2, 3, 4), ((0, 1), (1, 1), 4, 1, 4),
             ((-1, -1), (-1, -1), 3, 0, 2))
    for (sx, sz), (dx, dz), rise, run, radius in limbs:
        x, yy, z = cx + (1 if sx > 0 else 0), y + 5, cz + (1 if sz > 0 else 0)
        for i in range(rise):
            x, z, yy = x + dx, z + dz, yy + 1
            b.set(x, yy, z, 'acacia_log', axis='y')
        for i in range(run):
            x, z = x + dx, z + dz
            b.set(x, yy, z, 'acacia_wood', axis='y')
        canopy(b, x, yy + 1, z, radius, rng, top=max(1, radius - 2))
        b.set(x, yy + 1, z, 'acacia_wood', axis='y')


# --------------------------------------------------------------------- roofs
def hip_roof(b, x0, z0, x1, z1, y, roof=THATCH, overhang=2, lip=True, low=False, ridge_full=True):
    """Hipped roof over the wall rectangle; its first course sits at ``y``.

    ``lip`` starts with a flat slab eave (a deep, shady overhang). ``low`` halves the
    pitch with alternating slabs for the long, low savanna silhouette.
    Returns the top Y.
    """
    lx, lz, hx, hz = x0 - overhang, z0 - overhang, x1 + overhang, z1 + overhang
    i, top = 0, y
    while lx + i <= hx - i and lz + i <= hz - i:
        ax, az, bx, bz = lx + i, lz + i, hx - i, hz - i
        k = i - (1 if lip else 0)
        if low:
            level, half = y + max(0, k) // 2, ('bottom' if max(0, k) % 2 == 0 else 'top')
        else:
            level = y + max(0, k)
        for x in range(ax, bx + 1):
            for z in range(az, bz + 1):
                if not (x in (ax, bx) or z in (az, bz)):
                    continue
                if not b.inside(x, level, z):
                    continue
                if i == 0 and lip:
                    b.set(x, level, z, roof.slab, type='bottom', waterlogged=False)
                elif ax == bx or az == bz:
                    if ridge_full:
                        b.set(x, level, z, roof.full, **({'axis': 'x' if ax != bx else 'z'} if roof.full.endswith(('hay_block', '_log')) else {}))
                        b.set(x, level + 1, z, roof.slab, type='bottom', waterlogged=False)
                    else:
                        b.set(x, level, z, roof.slab, type='bottom' if not low or half == 'bottom' else 'top', waterlogged=False)
                elif low:
                    b.set(x, level, z, roof.slab, type=half, waterlogged=False)
                else:
                    f = 'south' if z == az else 'north' if z == bz else 'east' if x == ax else 'west'
                    b.set(x, level, z, roof.stairs, facing=f, half='bottom')
        top = level
        i += 1
    return top + 1


def flat_roof(b, x0, z0, x1, z1, y, mat='mud_bricks', parapet='mud_brick_wall', floor='packed_mud'):
    """Flat mud roof with a low parapet (for terraces)."""
    b.fill(x0, y, z0, x1, y, z1, floor)
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        b.set(x, y, z, mat)
        b.set(x, y + 1, z, mat if corner else parapet)


def cone_roof(b, cx, cz, y, r, mat='hay_block', cap='bamboo_mosaic_slab'):
    """Stepped conical thatch over a round hut of radius ``r``."""
    level, rr = y, r + 1.2
    while rr > 0.4:
        for dx in range(-int(rr) - 1, int(rr) + 2):
            for dz in range(-int(rr) - 1, int(rr) + 2):
                d = math.hypot(dx, dz)
                if d <= rr and (d > rr - 1.3 or rr < 1.5):
                    b.set(cx + dx, level, cz + dz, mat, axis='y')
                    if d > rr - .75 and is_air(b.get(cx + dx, level + 1, cz + dz)):
                        b.set(cx + dx, level + 1, cz + dz, cap, type='bottom', waterlogged=False)
        level += 1
        rr -= 1.0
    b.set(cx, level, cz, mat, axis='y')
    b.set(cx, level + 1, cz, 'lightning_rod', facing='up', powered=False)
    return level


# ------------------------------------------------------------ walls and porches
def toron(b, x0, z0, x1, z1, y, every=2, wood='acacia_fence', corners=False):
    """Beam ends poking out of mud walls (Sahel style) one row at ``y``."""
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        if corner and not corners:
            continue
        u = x - x0 if facing in ('north', 'south') else z - z0
        if u % every:
            continue
        dx, dz = DIRS[facing]
        if b.inside(x + dx, y, z + dz) and is_air(b.get(x + dx, y, z + dz)):
            b.set(x + dx, y, z + dz, wood)


def veranda(b, x0, x1, z0, z1, y_floor, y_roof, roof=ACACIA, posts=3, side='north', floor='acacia_planks',
            rail=False, slope=True):
    """Open porch on posts over (x0..x1, z0..z1) on the ``side`` of a building.

    The roof is a shed of stairs falling outward, or flat slabs (``slope=False``).
    """
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, y_floor, z, floor)
    outer = z0 if side == 'north' else z1 if side == 'south' else None
    xs = sorted(parts.posts_for(x1 - x0 + 1, posts)) if side in ('north', 'south') else [0, x1 - x0]
    zs = sorted(parts.posts_for(z1 - z0 + 1, posts)) if side in ('east', 'west') else [0, z1 - z0]
    cells = []
    if side in ('north', 'south'):
        cells = [(x0 + o, outer) for o in xs]
    else:
        ox = x0 if side == 'west' else x1
        cells = [(ox, z0 + o) for o in zs]
    for x, z in cells:
        for y in range(y_floor + 1, y_roof):
            b.set(x, y, z, 'stripped_acacia_log', axis='y')
    if rail:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                edge = (side in ('north', 'south') and z == outer) or (side == 'west' and x == x0) or \
                       (side == 'east' and x == x1)
                if edge and is_air(b.get(x, y_floor + 1, z)):
                    b.set(x, y_floor + 1, z, 'acacia_fence')
    # Roof: a beam over the posts, then the covering.
    for x in range(x0 - 1, x1 + 2):
        for z in range(z0 - 1 if side == 'north' else z0, z1 + 2 if side == 'south' else z1 + 1):
            if not b.inside(x, y_roof, z):
                continue
            if slope:
                b.set(x, y_roof, z, roof.stairs, facing=OPPOSITE[side], half='bottom')
            else:
                b.set(x, y_roof, z, roof.slab, type='bottom', waterlogged=False)
    return cells


def stockade(b, cells, y=1, h=4, base='packed_mud', wood='acacia_log', tips=True):
    """Sharpened log palisade: alternate heights and fence tips."""
    for i, (x, z) in enumerate(cells):
        b.set(x, 0, z, base)
        top = h - (i % 2)
        for yy in range(y, y + top):
            b.set(x, yy, z, wood, axis='y')
        if tips:
            b.set(x, y + top, z, 'acacia_fence')


def woven_fence(b, cells, y=1):
    for x, z in cells:
        b.set(x, y, z, 'acacia_fence')


# ------------------------------------------------------------------ furniture
def lamp(b, x, z, y=1, height=2, base='mud_bricks'):
    """A mud-brick footed lantern post."""
    b.set(x, y, z, base)
    for i in range(height):
        b.set(x, y + 1 + i, z, 'acacia_fence')
    b.set(x, y + 1 + height, z, 'lantern', hanging=False, waterlogged=False)


def brazier(b, x, z, y=1):
    """A mud-brick pillar crowned with a lantern behind a low wall."""
    b.set(x, y, z, 'mud_bricks')
    b.set(x, y + 1, z, 'mud_brick_wall')
    b.set(x, y + 2, z, 'lantern', hanging=False, waterlogged=False)


def stool(b, x, y, z):
    b.set(x, y, z, 'acacia_slab', type='bottom', waterlogged=False)


def log_seat(b, x, y, z, axis='x'):
    b.set(x, y, z, 'stripped_acacia_log', axis=axis)


def trough(b, x0, z0, length, axis='x', y=1):
    """Drinking trough: water held between split acacia logs."""
    dx, dz = (1, 0) if axis == 'x' else (0, 1)
    cross = 'z' if axis == 'x' else 'x'
    cx, cz = (0, 1) if axis == 'x' else (1, 0)
    for i in range(-1, length + 1):
        x, z = x0 + dx * i, z0 + dz * i
        b.set(x, y - 1, z, 'mud_bricks')
        if i in (-1, length):
            b.set(x, y, z, 'stripped_acacia_log', axis=axis)
            continue
        b.set(x, y, z, 'water', level=0)
        for s in (-1, 1):
            b.set(x + cx * s, y, z + cz * s, 'stripped_acacia_log', axis=axis)
            b.set(x + cx * s, y - 1, z + cz * s, 'mud_bricks')


def thatched_stall(b, x0, z0, facing, goods, cloth='orange', counter='acacia_planks'):
    """Market stall 3 wide x 2 deep under a hay-and-straw roof; the counter faces ``facing``."""
    dx, dz = DIRS[facing]
    lx, lz = DIRS[CLOCKWISE[facing]]
    front = [(x0 + lx * i, z0 + lz * i) for i in range(3)]
    back = [(x - dx, z - dz) for x, z in front]
    for i, (x, z) in enumerate(front):
        if i == 1:
            b.set(x, 1, z, 'barrel', facing='up', open=False)
        else:
            b.set(x, 1, z, counter)
        g = goods[i % len(goods)]
        if g:
            b.set(x, 2, z, g)
    for x, z in (back[0], back[2]):
        for y in (1, 2, 3):
            b.set(x, y, z, 'acacia_fence')
    for x, z in (front[0], front[2]):
        b.set(x, 3, z, 'acacia_fence')
    for x, z in front + back:
        b.set(x, 4, z, 'hay_block', axis='y')
    for x, z in front:
        b.set(x + dx, 4, z + dz, THATCH.slab, type='bottom', waterlogged=False)
    for x, z in back:
        b.set(x - dx, 4, z - dz, THATCH.slab, type='bottom', waterlogged=False)
    for (x, z), side in ((front[0], -1), (front[2], 1)):
        ex, ez = x + lx * side, z + lz * side
        b.set(ex, 4, ez, THATCH.slab, type='bottom', waterlogged=False)
        ex2, ez2 = ex - dx, ez - dz
        b.set(ex2, 4, ez2, THATCH.slab, type='bottom', waterlogged=False)
    # A cloth bolt on the counter end shows the stall's colour.
    b.set(back[0][0], 4, back[0][1], f'{cloth}_wool')
    bx, bz = back[1]
    b.set(bx, 1, bz, 'decorated_pot', facing=OPPOSITE[facing], waterlogged=False, cracked=False)


def drying_rack(b, x, z, along='x', length=3, y=1, hides=('brown', 'white', 'orange')):
    """Hide-drying frame: two posts, a rail and hides (carpets) slung over a slab bar."""
    dx, dz = (1, 0) if along == 'x' else (0, 1)
    for i in (0, length - 1):
        for yy in range(y, y + 2):
            b.set(x + dx * i, yy, z + dz * i, 'acacia_fence')
    for i in range(length):
        b.set(x + dx * i, y + 2, z + dz * i, 'stripped_acacia_log', axis=along)
    for i in range(1, length - 1):
        b.set(x + dx * i, y + 3, z + dz * i, f'{hides[i % len(hides)]}_carpet')


def pot_cluster(b, cells, y=1):
    for i, (x, z) in enumerate(cells):
        b.set(x, y, z, 'decorated_pot', facing=('north', 'east', 'south', 'west')[i % 4], waterlogged=False,
              cracked=False)


# ---------------------------------------------------------------- the ground
def paving(x, z, seed):
    """Plaza ground: packed mud and mud brick worn into dirt, gravel and red sand."""
    n = smooth(x, z, seed, 2.5) * .65 + noise(x, z, seed + 5) * .35
    if n < .12:
        return 'coarse_dirt'
    if n < .28:
        return 'dirt_path'
    if n < .56:
        return 'packed_mud'
    if n < .66:
        return 'mud_bricks'
    if n < .76:
        return 'packed_mud'
    if n < .84:
        return 'coarse_dirt'
    if n < .9:
        return 'gravel'
    return 'red_sand' if noise(x, z, seed + 9) < .5 else 'terracotta'


def market_paving(x, z, seed):
    """Busier ground for the market square: more brick and terracotta."""
    n = smooth(x, z, seed, 2.0) * .6 + noise(x, z, seed + 5) * .4
    if n < .14:
        return 'dirt_path'
    if n < .4:
        return 'mud_bricks'
    if n < .62:
        return 'packed_mud'
    if n < .72:
        return 'terracotta'
    if n < .8:
        return 'coarse_dirt'
    if n < .88:
        return 'brown_terracotta'
    return 'red_sand'


def savanna_plants(b, cells, rng, chance=.3, y=1):
    """Sow tufts of savanna grass on lawn cells."""
    for x, z in cells:
        if not (b.inside(x, y, z) and is_air(b.get(x, y, z))):
            continue
        r = rng.random()
        if r < chance * .6:
            b.set(x, y, z, 'short_grass')
        elif r < chance * .8:
            b.set(x, y, z, 'short_dry_grass')
        elif r < chance * .9:
            b.set(x, y, z, 'bush')
        elif r < chance:
            b.set(x, y, z, rng.choice(['dandelion', 'orange_tulip', 'red_tulip', 'oxeye_daisy']))


def tall_grass(b, x, z, y=1):
    if is_air(b.get(x, y, z)) and is_air(b.get(x, y + 1, z)):
        b.set(x, y, z, 'tall_grass', half='lower')
        b.set(x, y + 1, z, 'tall_grass', half='upper')
