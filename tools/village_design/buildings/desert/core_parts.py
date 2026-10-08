"""Desert architecture helpers for the town centres, civic buildings and streets.

Flat roofs with parapets, domes, arcades, lattice (trapdoor) windows, striped
awnings and palms. Everything only draws into a ``Build``; the shared kit stays
untouched. 26.3 renamed ``chain`` to ``iron_chain``, so these helpers use the
new id.
"""
import math

from ...kit import DIRS, OPPOSITE, CLOCKWISE, is_air
from ... import parts

CHAIN = 'iron_chain'
STRIPES = ('orange', 'white', 'red', 'white', 'yellow', 'white', 'cyan', 'white')
FACE = {(1, 0): 'west', (-1, 0): 'east', (0, 1): 'north', (0, -1): 'south'}


def lantern(b, x, y, z, hanging=True, chain=0):
    """Lantern; ``chain`` iron chain links above it when hanging."""
    for i in range(chain):
        b.set(x, y - i, z, CHAIN, axis='y', waterlogged=False)
    b.set(x, y - chain, z, 'lantern', hanging=hanging, waterlogged=False)


def leaves(b, x, y, z, kind='jungle_leaves'):
    if b.inside(x, y, z) and is_air(b.get(x, y, z)):
        b.set(x, y, z, kind, persistent=True, distance=1, waterlogged=False)


# ------------------------------------------------------------------ volumes
def walls(b, x0, z0, x1, z1, y0, y1, fill='smooth_sandstone', corner='cut_sandstone', bands=(), band='cut_sandstone'):
    """Solid wall ring; corner pilasters and horizontal bands in ``band``."""
    for x, z, facing, is_corner in parts.ring(x0, z0, x1, z1):
        for y in range(y0, y1 + 1):
            if is_corner and corner:
                b.set(x, y, z, corner)
            elif y in bands:
                b.set(x, y, z, band)
            else:
                b.set(x, y, z, fill)


def slab(b, x0, z0, x1, z1, y, mat):
    b.fill(x0, y, z0, x1, y, z1, mat)


def plinth(b, x0, z0, x1, z1, top=1, base='sandstone', floor='smooth_sandstone'):
    """Base course from Y=0 to ``top`` with the floor at ``top``."""
    for y in range(0, top + 1):
        for x, z, _, _ in parts.ring(x0, z0, x1, z1):
            b.set(x, y, z, base)
        b.fill(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, floor if y == top else 'sandstone')


def parapet(b, x0, z0, x1, z1, y, style='merlon', mat='cut_sandstone', low='smooth_sandstone_slab',
            wall='sandstone_wall', skip=()):
    """Roof-edge parapet at ``y`` around the rectangle.

    ``merlon``: stepped blocks every other cell with slabs between (crenels);
    ``wall``: a continuous sandstone wall with block posts at the corners;
    ``solid``: a continuous block course with slab caps on the corners.
    """
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        if (x, z) in skip:
            continue
        if style == 'merlon':
            if corner or (x + z) % 2 == 0:
                b.set(x, y, z, mat)
                if corner:
                    b.set(x, y + 1, z, low, type='bottom')
            else:
                b.set(x, y, z, low, type='bottom')
        elif style == 'wall':
            b.set(x, y, z, mat if corner else wall)
            if corner:
                b.set(x, y + 1, z, low, type='bottom')
        else:
            b.set(x, y, z, mat)
            if corner:
                b.set(x, y + 1, z, low, type='bottom')


def cornice(b, x0, z0, x1, z1, y, stairs='sandstone_stairs'):
    """Upside-down stairs projecting one block out of the wall rectangle at ``y``."""
    for x in range(x0, x1 + 1):
        for z, f in ((z0 - 1, 'south'), (z1 + 1, 'north')):
            if b.inside(x, y, z) and is_air(b.get(x, y, z)):
                b.set(x, y, z, stairs, facing=f, half='top', shape='straight', waterlogged=False, lock=True)
    for z in range(z0, z1 + 1):
        for x, f in ((x0 - 1, 'east'), (x1 + 1, 'west')):
            if b.inside(x, y, z) and is_air(b.get(x, y, z)):
                b.set(x, y, z, stairs, facing=f, half='top', shape='straight', waterlogged=False, lock=True)


def dome(b, cx, cz, y, r, mat='smooth_sandstone', stairs=None, finial=None, hollow=True, rise=1.1, band=None):
    """Stepped voxel dome of radius ``r`` (footprint 2r+1) standing on ``y``; returns the crown's Y.

    Each column rises to round(sqrt(R^2 - d^2) * rise). With ``stairs`` the top
    block of every column that steps down toward the rim becomes a stair facing the
    crown; full blocks read cleaner at small radii. ``band`` paints the lowest course
    (a drum ring). A hollow dome stays open underneath.
    """
    R = r + 0.5
    heights = {}
    for x in range(cx - r, cx + r + 1):
        for z in range(cz - r, cz + r + 1):
            d = math.hypot(x - cx, z - cz)
            if d <= R:
                heights[(x, z)] = max(1, int(math.sqrt(max(R * R - d * d, 0)) * rise + 0.5))
    top_y = y
    for (x, z), h in heights.items():
        dx, dz = x - cx, z - cz
        nbs = [heights.get((x + ox, z + oz), 0) for ox, oz in DIRS.values()]
        low = min(nbs)
        for i in range(h):
            if hollow and i < low - 1:
                continue
            spec = band if (band and i == 0) else mat
            b.set(x, y + i, z, spec)
        top_y = max(top_y, y + h - 1)
        if (dx, dz) == (0, 0) or not stairs:
            continue
        step = (1 if dx > 0 else -1, 0) if abs(dx) >= abs(dz) else (0, 1 if dz > 0 else -1)
        outward = heights.get((x + step[0], z + step[1]), 0)
        if outward < h and not (band and h == 1):
            b.set(x, y + h - 1, z, stairs, facing=FACE[step], half='bottom')
    if finial:
        for i, spec in enumerate(finial):
            b.set(cx, top_y + 1 + i, cz, spec)
    return top_y


# ----------------------------------------------------------------- openings
def lattice(b, x, y, z, out, height=2, width=1, wood='jungle', sill=None, head=None):
    """Mashrabiya window: the wall opening is screened by trapdoors flush with the outer face."""
    lx, lz = DIRS[CLOCKWISE[out]]
    dx, dz = DIRS[out]
    for i in range(width):
        for j in range(height):
            b.set(x + lx * i, y + j, z + lz * i, f'{wood}_trapdoor', facing=OPPOSITE[out], half='bottom', open=True,
                  powered=False, waterlogged=False)
        if sill:
            sx, sz = x + lx * i + dx, z + lz * i + dz
            if b.inside(sx, y - 1, sz) and is_air(b.get(sx, y - 1, sz)):
                b.set(sx, y - 1, sz, sill, facing=OPPOSITE[out], half='top', shape='straight', waterlogged=False,
                      lock=True)
        if head:
            b.set(x + lx * i, y + height, z + lz * i, head)


def glass(b, x, y, z, out, height=2, width=1, pane='glass_pane'):
    lx, lz = DIRS[CLOCKWISE[out]]
    for i in range(width):
        for j in range(height):
            b.set(x + lx * i, y + j, z + lz * i, pane)


def arch(b, x0, z0, x1, z1, y, stairs='sandstone_stairs', key='cut_sandstone_slab'):
    """Arch head spanning the open cells between two piers (a straight run).

    Upside-down stairs spring from the piers and a top slab closes the crown.
    ``y`` is the springing course.
    """
    cells = parts.along(x0, z0, x1, z1)
    n = len(cells)
    if n == 1:
        b.set(cells[0][0], y, cells[0][1], key, type='top')
        return
    first, last = cells[0], cells[-1]
    if x0 == x1:
        fa, fb = 'north', 'south'
    else:
        fa, fb = 'west', 'east'
    b.set(first[0], y, first[1], stairs, facing=fa, half='top', shape='straight', waterlogged=False, lock=True)
    b.set(last[0], y, last[1], stairs, facing=fb, half='top', shape='straight', waterlogged=False, lock=True)
    for (x, z) in cells[1:-1]:
        b.set(x, y, z, key, type='top')


def arcade(b, x0, z0, x1, z1, y0, height, pier='cut_sandstone', spacing=3, stairs='sandstone_stairs',
           key='cut_sandstone_slab', lintel='smooth_sandstone', cap=None, base=None):
    """Row of piers with arches between them along a straight run; the lintel course sits above the arches."""
    cells = parts.along(x0, z0, x1, z1)
    piers = [i for i in range(len(cells)) if i % spacing == 0 or i == len(cells) - 1]
    for i in piers:
        x, z = cells[i]
        if base:
            b.set(x, y0 - 1, z, base)
        for y in range(y0, y0 + height):
            b.set(x, y, z, pier)
    for a, c in zip(piers, piers[1:]):
        if c - a > 1:
            (ax, az), (cx, cz) = cells[a + 1], cells[c - 1]
            arch(b, ax, az, cx, cz, y0 + height - 1, stairs, key)
    for x, z in cells:
        b.set(x, y0 + height, z, lintel)
        if cap:
            b.set(x, y0 + height + 1, z, cap)


def door(b, x, y, z, out, wood='acacia', step='sandstone_stairs', head='chiseled_sandstone', hinge='left',
         lamps=False):
    """Door in a wall facing ``out`` with a step and a carved head stone."""
    dx, dz = DIRS[out]
    b.door(x, y, z, facing=OPPOSITE[out], wood=wood, hinge=hinge)
    if step:
        b.set(x + dx, y - 1, z + dz, step, facing=OPPOSITE[out], half='bottom', shape='straight', lock=True)
    if head:
        b.set(x, y + 2, z, head)
    if lamps:
        lx, lz = DIRS[CLOCKWISE[out]]
        for s in (-1, 1):
            px, pz = x + dx + lx * s, z + dz + lz * s
            if b.inside(px, y + 1, pz) and is_air(b.get(px, y + 1, pz)):
                b.set(px, y + 1, pz, 'wall_torch', facing=out)


def awning(b, cells, y, out, colors=STRIPES, start=0, valance='acacia'):
    """Striped cloth awning: one wool cell outward of each wall cell, with a trapdoor valance."""
    dx, dz = DIRS[out]
    for i, (x, z) in enumerate(cells):
        ax, az = x + dx, z + dz
        if not b.inside(ax, y, az):
            continue
        b.set(ax, y, az, f'{colors[(i + start) % len(colors)]}_wool')
        vx, vz = ax + dx, az + dz
        if valance and b.inside(vx, y, vz) and is_air(b.get(vx, y, vz)):
            b.set(vx, y, vz, f'{valance}_trapdoor', facing=out, half='top', open=True, powered=False,
                  waterlogged=False)


def canopy(b, x0, z0, x1, z1, y, colors=STRIPES, along='x', posts=None, post='acacia_fence', start=0):
    """Flat striped cloth canopy on posts (stripes run perpendicular to ``along``)."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            i = (x - x0) if along == 'x' else (z - z0)
            b.set(x, y, z, f'{colors[(i + start) % len(colors)]}_wool')
    for (x, z) in posts or ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        for yy in range(1, y):
            if is_air(b.get(x, yy, z)):
                b.set(x, yy, z, post)


# --------------------------------------------------------------- furniture
def cushion(b, x, y, z, color='red'):
    """Floor cushion: a carpet."""
    b.set(x, y, z, f'{color}_carpet')


def pot(b, x, y, z, plant=None):
    b.set(x, y, z, f'potted_{plant}' if plant else 'decorated_pot', **({} if plant else {'facing': 'north'}))


def low_table(b, x, y, z, wood='acacia'):
    b.set(x, y, z, f'{wood}_slab', type='bottom')


def brazier(b, x, y, z, base='cut_sandstone'):
    b.set(x, y, z, base)
    b.set(x, y + 1, z, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)


def wall_post(b, x, y, z, height=2, base='cut_sandstone', post='sandstone_wall'):
    """Sandstone lamp post with a lantern on top."""
    if base:
        b.set(x, y, z, base)
        y += 1
    for i in range(height):
        b.set(x, y + i, z, post)
    b.set(x, y + height, z, 'lantern', hanging=False, waterlogged=False)


# ------------------------------------------------------------------ nature
def palm(b, x, y, z, rng, height=6, lean=None, dates=True):
    """Date palm: a jungle-log trunk that may lean, and a crown of drooping fronds."""
    cx, cz = x, z
    lean = lean if lean is not None else rng.choice(['north', 'south', 'east', 'west', None])
    for i in range(height):
        if lean and i == height // 2 + 1:
            dx, dz = DIRS[lean]
            cx, cz = cx + dx, cz + dz
        b.set(cx, y + i, cz, 'jungle_log', axis='y', clip=True)
    top = y + height
    leaves(b, cx, top, cz)
    for dx, dz in DIRS.values():
        leaves(b, cx + dx, top, cz + dz)
        leaves(b, cx + 2 * dx, top, cz + 2 * dz)
        leaves(b, cx + 3 * dx, top - 1, cz + 3 * dz)
        if rng.random() < .6:
            leaves(b, cx + 3 * dx, top - 2, cz + 3 * dz)
    for dx, dz in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        leaves(b, cx + dx, top, cz + dz)
        leaves(b, cx + 2 * dx, top - 1, cz + 2 * dz)
    leaves(b, cx, top + 1, cz)
    if dates:
        for (dx, dz), f in (((1, 0), 'west'), ((-1, 0), 'east')):
            px, pz = cx + dx, cz + dz
            if b.inside(px, top - 1, pz) and is_air(b.get(px, top - 1, pz)) and rng.random() < .7:
                b.set(px, top - 1, pz, 'cocoa', facing=f, age=2)
    return cx, top, cz


def desert_plants(b, cells, y, rng, chance=0.12):
    for x, z in cells:
        if b.inside(x, y, z) and is_air(b.get(x, y, z)) and rng.random() < chance:
            b.set(x, y, z, rng.choice(['dead_bush', 'short_dry_grass', 'short_dry_grass', 'tall_dry_grass']))


def cactus(b, x, y, z, height=2):
    for i in range(height):
        b.set(x, y + i, z, 'cactus', age=0)
