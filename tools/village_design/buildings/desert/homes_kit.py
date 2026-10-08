"""Drawing helpers for the desert homes, workshops, farms and decorations.

Desert buildings are solid masonry boxes with flat roofs, so they share a small
vocabulary: plinths and walls, roof decks with crenellated parapets, projecting
beam ends, lattice (trapdoor) windows, arched openings, striped wool awnings,
domes, date palms and a handful of furniture pieces. Everything here only draws
into a ``Build``; each design stays an independent program.
"""
import math

from ...kit import DIRS, OPPOSITE, CLOCKWISE, is_air
from ... import parts
from .palette import LOOT, AWNINGS

__all__ = ['LOOT', 'AWNINGS']

PAVING = ('smooth_sandstone', 'smooth_sandstone', 'cut_sandstone', 'sandstone')


# ------------------------------------------------------------------ masonry
def plinth(b, x0, z0, x1, z1, top=1, mat='sandstone', floor='smooth_sandstone', under='sandstone', rim='cut_sandstone'):
    """Solid base from Y=0 to ``top`` with the interior floor on ``top``; ``rim`` is
    the visible top course of the base."""
    for y in range(0, top + 1):
        for x, z, _, _ in parts.ring(x0, z0, x1, z1):
            b.set(x, y, z, rim if (rim and y == top) else mat)
        b.fill(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, floor if y == top else under)


def walls(b, x0, z0, x1, z1, y0, y1, fill, corner=None, band=None, base=None):
    """Masonry walls on a rectangle: corner pilasters, an optional base course at
    ``y0`` and a band course at ``y1``."""
    for x, z, _, is_corner in parts.ring(x0, z0, x1, z1):
        for y in range(y0, y1 + 1):
            if is_corner and corner:
                mat = corner
            elif y == y1 and band:
                mat = band
            elif y == y0 and base:
                mat = base
            else:
                mat = fill
            b.set(x, y, z, mat)


def frieze(b, x0, z0, x1, z1, y, mats=('orange_terracotta',), corners=False, only=None):
    """A painted band (or checker of ``mats``) around a wall ring at ``y``; ``only``
    limits it to some sides."""
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        if corner and not corners:
            continue
        if only and facing not in only and not corner:
            continue
        b.set(x, y, z, mats[(x + z) % len(mats)])


def wall_run(b, x0, z0, x1, z1, y0, y1, mat):
    """Straight wall (one block thick) between two cells."""
    for x, z in parts.along(x0, z0, x1, z1):
        for y in range(y0, y1 + 1):
            b.set(x, y, z, mat)


def deck(b, x0, z0, x1, z1, y, mat='smooth_sandstone', edge='cut_sandstone'):
    """Flat roof (or upper floor) slab with a contrasting cornice course on its rim."""
    b.fill(x0, y, z0, x1, y, z1, mat)
    if edge:
        for x, z, _, _ in parts.ring(x0, z0, x1, z1):
            b.set(x, y, z, edge)


def parapet(b, x0, z0, x1, z1, y, mat='cut_sandstone', cap='cut_sandstone_slab', style='crenel', skip=()):
    """Parapet ring standing on the roof at ``y``.

    ``crenel``: a full course with slab merlons on alternate cells and taller corners;
    ``solid``: one full course; ``low``: a single course of slabs.
    """
    for x, z, _, corner in parts.ring(x0, z0, x1, z1):
        if (x, z) in skip:
            continue
        if style == 'low':
            b.set(x, y, z, cap, type='bottom', waterlogged=False)
            continue
        b.set(x, y, z, mat)
        if style == 'crenel':
            if corner:
                b.set(x, y + 1, z, mat)
            elif (x + z) % 2 == 0:
                b.set(x, y + 1, z, cap, type='bottom', waterlogged=False)


def flat_roof(b, x0, z0, x1, z1, y, deck_mat='smooth_sandstone', edge='cut_sandstone', parapet_mat='cut_sandstone',
              cap='cut_sandstone_slab', style='crenel', skip=()):
    deck(b, x0, z0, x1, z1, y, deck_mat, edge)
    if style:
        parapet(b, x0, z0, x1, z1, y + 1, parapet_mat, cap, style, skip)


def beam_ends(b, x0, z0, x1, z1, y, every=2, wood='stripped_acacia_log', sides=('north', 'south', 'east', 'west')):
    """Projecting roof beams (vigas): logs poking one block out of the walls at ``y``."""
    for side in sides:
        if side in ('north', 'south'):
            z = z0 - 1 if side == 'north' else z1 + 1
            for x in range(x0 + 1, x1, every):
                if b.inside(x, y, z) and is_air(b.get(x, y, z)):
                    b.set(x, y, z, wood, axis='z')
        else:
            x = x0 - 1 if side == 'west' else x1 + 1
            for z in range(z0 + 1, z1, every):
                if b.inside(x, y, z) and is_air(b.get(x, y, z)):
                    b.set(x, y, z, wood, axis='x')


def spouts(b, cells, y, mat='cut_sandstone_slab'):
    """Rain spouts: top slabs poking out of the parapet line."""
    for x, z in cells:
        if b.inside(x, y, z) and is_air(b.get(x, y, z)):
            b.set(x, y, z, mat, type='top', waterlogged=False)


# ------------------------------------------------------------------ openings
def lattice(b, x, y, z, out, wood='jungle', height=1):
    """Lattice window: closed screens of open trapdoors set into a wall facing ``out``."""
    for j in range(height):
        b.set(x, y + j, z, f'{wood}_trapdoor', facing=out, half='bottom', open=True, powered=False,
              waterlogged=False)


def lattice_row(b, cells, y, out, wood='jungle', height=1, sill=None):
    for x, z in cells:
        lattice(b, x, y, z, out, wood, height)
        if sill:
            dx, dz = DIRS[out]
            if b.inside(x + dx, y - 1, z + dz) and is_air(b.get(x + dx, y - 1, z + dz)):
                b.set(x + dx, y - 1, z + dz, sill, type='top', waterlogged=False)


def arch(b, first, last, y, axis, mat='sandstone_stairs'):
    """Round the two top corners of an opening; ``first``/``last`` are its end
    cells (x, z) along ``axis`` ('x' or 'z') at the top row ``y``."""
    (ax, az), (cx, cz) = first, last
    if axis == 'x':
        b.set(ax, y, az, mat, facing='west', half='top', shape='straight', waterlogged=False, lock=True)
        b.set(cx, y, cz, mat, facing='east', half='top', shape='straight', waterlogged=False, lock=True)
    else:
        b.set(ax, y, az, mat, facing='north', half='top', shape='straight', waterlogged=False, lock=True)
        b.set(cx, y, cz, mat, facing='south', half='top', shape='straight', waterlogged=False, lock=True)


def door(b, x, y, z, out, wood='acacia', step='sandstone_stairs', hinge='left', lamp=True, frame=None):
    """A door in a wall facing ``out`` with a step outside, a painted ``frame`` and a
    lantern beside it."""
    dx, dz = DIRS[out]
    b.door(x, y, z, facing=OPPOSITE[out], wood=wood, hinge=hinge)
    if frame:
        lx, lz = DIRS[CLOCKWISE[out]]
        for s in (-1, 1):
            for j in (0, 1, 2):
                b.set(x + lx * s, y + j, z + lz * s, frame)
        b.set(x, y + 2, z, frame)
    if step:
        b.set(x + dx, y - 1, z + dz, step, facing=OPPOSITE[out], half='bottom', shape='straight',
              waterlogged=False, lock=True)
    if not frame:
        b.set(x, y + 2, z, 'chiseled_sandstone')
    if lamp:
        lx, lz = DIRS[CLOCKWISE[out]]
        cx, cz = x + dx + lx, z + dz + lz
        if b.inside(cx, y + 1, cz) and is_air(b.get(cx, y + 1, cz)) and not is_air(b.get(x + lx, y + 1, z + lz)):
            b.set(cx, y + 1, cz, 'wall_torch', facing=out)


# ------------------------------------------------------------------ shade
def awning(b, x0, z0, x1, z1, y, colors=('orange', 'white'), stripe='x', posts=(), post='acacia_fence'):
    """Flat striped wool canopy over a rectangle at ``y``; ``posts`` are (x, z) cells
    holding it up from the ground."""
    for x in range(min(x0, x1), max(x0, x1) + 1):
        for z in range(min(z0, z1), max(z0, z1) + 1):
            i = x if stripe == 'x' else z
            b.set(x, y, z, f'{colors[i % len(colors)]}_wool')
    for px, pz in posts:
        for yy in range(1, y):
            if is_air(b.get(px, yy, pz)):
                b.set(px, yy, pz, post)


def canopy_edge(b, x0, z0, x1, z1, y, colors=('orange', 'white'), stripe='x'):
    """Carpet valance: a row of striped carpets laid on top of a canopy edge."""
    for x in range(min(x0, x1), max(x0, x1) + 1):
        for z in range(min(z0, z1), max(z0, z1) + 1):
            i = x if stripe == 'x' else z
            b.set(x, y, z, f'{colors[i % len(colors)]}_carpet')


def pergola(b, x0, z0, x1, z1, y, wood='acacia', axis='x'):
    """Slatted shade: alternate rows of beams and open gaps."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if (z if axis == 'x' else x) % 2 == 0:
                b.set(x, y, z, f'stripped_{wood}_log', axis=axis)


# ------------------------------------------------------------------ domes
def dome(b, cx, cz, y0, r, mat='smooth_sandstone', finial='sandstone_wall', ry=None):
    """Hemispherical shell centred on (cx, cz) (half-block centres allowed) rising from ``y0``."""
    ry = ry or r
    top = None
    for dy in range(0, int(ry + 1)):
        for x in range(int(math.floor(cx - r - 1)), int(math.ceil(cx + r + 1)) + 1):
            for z in range(int(math.floor(cz - r - 1)), int(math.ceil(cz + r + 1)) + 1):
                d = math.sqrt(((x - cx) / r) ** 2 + ((z - cz) / r) ** 2 + (dy / ry) ** 2)
                inner = math.sqrt(((x - cx) / max(r - 1, .5)) ** 2 + ((z - cz) / max(r - 1, .5)) ** 2
                                  + (dy / max(ry - 1, .5)) ** 2)
                if d <= 1.0 + .5 / r and inner > 1.0 + .5 / r - .02:
                    b.set(x, y0 + dy, z, mat, clip=True)
                    if top is None or y0 + dy > top[1]:
                        top = (x, y0 + dy, z)
    if finial:
        fx, fz = int(math.floor(cx)), int(math.floor(cz))
        yy = max(y for (x, y, z) in b.grid if (x, z) == (fx, fz) and y >= y0) + 1
        b.set(fx, yy, fz, finial)
        if finial.endswith('_wall'):
            b.set(fx, yy + 1, fz, 'lantern', hanging=False, waterlogged=False)
    return top


# ------------------------------------------------------------------ greenery
def leaf(b, x, y, z, kind='jungle_leaves'):
    if b.inside(x, y, z) and is_air(b.get(x, y, z)):
        b.set(x, y, z, kind, persistent=True, distance=1, waterlogged=False)


def palm(b, x, y, z, height=6, lean=None, dates=True, crown='jungle_leaves', wood='jungle_log'):
    """Date palm: a slim jungle-log trunk (optionally kinked toward ``lean``), a
    drooping crown of persistent leaves and cocoa 'dates' under it.  Returns the crown top."""
    tx, tz = x, z
    kink = height // 2 if lean else None
    for i in range(height):
        if kink is not None and i == kink:
            dx, dz = DIRS[lean]
            b.set(tx, y + i, tz, wood, axis='y')
            tx, tz = tx + dx, tz + dz
        b.set(tx, y + i, tz, wood, axis='y')
    ty = y + height - 1
    leaf(b, tx, ty + 1, tz, crown)
    for d, (dx, dz) in DIRS.items():
        leaf(b, tx + dx, ty + 1, tz + dz, crown)
        leaf(b, tx + 2 * dx, ty + 1, tz + 2 * dz, crown)
        leaf(b, tx + 3 * dx, ty, tz + 3 * dz, crown)
        leaf(b, tx + 3 * dx, ty - 1, tz + 3 * dz, crown)
        leaf(b, tx + dx, ty, tz + dz, crown)
    for dx, dz in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        leaf(b, tx + dx, ty + 1, tz + dz, crown)
        leaf(b, tx + 2 * dx, ty, tz + 2 * dz, crown)
    if dates:
        for d in ('north', 'east', 'south', 'west')[:3]:
            dx, dz = DIRS[d]
            if b.inside(tx + dx, ty - 1, tz + dz) and is_air(b.get(tx + dx, ty - 1, tz + dz)):
                b.set(tx + dx, ty - 1, tz + dz, 'cocoa', facing=OPPOSITE[d], age=2)
    return ty + 1


def cactus(b, x, z, height=2, flower=False):
    """Cactus on its own sand cell; keeps the sides clear so it survives."""
    b.set(x, 0, z, 'sand')
    for i in range(height):
        b.set(x, 1 + i, z, 'cactus', age=0)
    if flower:
        b.set(x, 1 + height, z, 'cactus_flower')


def dry_tuft(b, x, z, rng, y=1):
    if b.inside(x, y, z) and is_air(b.get(x, y, z)):
        b.set(x, y, z, rng.choice(['dead_bush', 'short_dry_grass', 'short_dry_grass', 'tall_dry_grass']))


def sand_patch(b, cells, rng, tufts=.25):
    for x, z in cells:
        b.set(x, 0, z, 'sand')
        if rng.random() < tufts:
            dry_tuft(b, x, z, rng)


# ------------------------------------------------------------------ ground
def path(b, cells, rng, mats=PAVING):
    for x, z in cells:
        b.set(x, 0, z, rng.choice(mats))


def path_line(b, x, z0, z1, rng, width=1, mats=PAVING):
    path(b, [(x + i, z) for z in range(z0, z1 + 1) for i in range(width)], rng, mats)


def paving(b, x0, z0, x1, z1, rng, y=0, mats=('smooth_sandstone', 'cut_sandstone')):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, y, z, mats[(x + z) % 2] if len(mats) == 2 else rng.choice(mats))


# ------------------------------------------------------------------ furniture
def hang(b, x, y, z):
    b.set(x, y, z, 'lantern', hanging=True, waterlogged=False)


def stand_lamp(b, x, y, z):
    b.set(x, y, z, 'lantern', hanging=False, waterlogged=False)


def candle(b, x, y, z, n=3, color=None):
    b.set(x, y, z, f'{color}_candle' if color else 'candle', candles=n, lit=True, waterlogged=False)


def pot(b, x, y, z, facing='north'):
    b.set(x, y, z, 'decorated_pot', facing=facing, cracked=False, waterlogged=False)


def shelf(b, x, y, z, facing, wood='acacia'):
    b.set(x, y, z, f'{wood}_shelf', facing=facing, powered=False, side_chain='unconnected', waterlogged=False)


def table(b, x, y, z, wood='acacia', cloth=None):
    parts.table(b, x, y, z, wood, cloth)


def chair(b, x, y, z, back, wood='acacia'):
    parts.chair(b, x, y, z, back, wood)


def rug(b, x0, z0, x1, z1, y, color, border=None):
    parts.rug(b, x0, z0, x1, z1, y, color, border)


def ladder(b, x, y0, y1, z, facing):
    """Ladder from ``y0`` to ``y1``; ``facing`` points away from the wall it hangs on."""
    for y in range(y0, y1 + 1):
        b.set(x, y, z, 'ladder', facing=facing, waterlogged=False)


def water_jar(b, x, y, z):
    b.set(x, y, z, 'water_cauldron', level=3)


def plant(b, x, y, z, rng):
    b.set(x, y, z, rng.choice(['potted_cactus', 'potted_dead_bush', 'potted_cactus', 'potted_acacia_sapling',
                               'potted_jungle_sapling']))


def bed_with_chest(b, x, y, z, facing, color, chest_at, chest_facing):
    b.bed(x, y, z, facing, color)
    b.chest(*chest_at, chest_facing, loot=LOOT)
