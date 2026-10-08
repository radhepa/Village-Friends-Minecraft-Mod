"""Savanna drawing helpers shared by the savanna homes, workshops, farms and decor.

Round mud huts with conical thatch, low hipped roofs with deep eaves, verandas on
posts, woven acacia fences, drying racks and hand-shaped acacia trees. Every
helper only draws into a ``Build``.
"""
import math

from ...kit import DIRS, OPPOSITE, CLOCKWISE, is_air
from ... import parts
from .palette import LOOT

LEAF = dict(persistent=True, distance=1, waterlogged=False)
DRY = ('short_dry_grass', 'short_dry_grass', 'tall_dry_grass', 'short_grass', 'dead_bush')


# ------------------------------------------------------------------ ground
def ground(b, x0, z0, x1, z1, rng, mix=None, y=0, tufts=0.0, skip=None):
    """Sun-baked yard: coarse dirt, packed earth and patches of grass with dry tufts."""
    mix = mix or ['coarse_dirt', 'coarse_dirt', 'grass_block', 'dirt', 'grass_block']
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if skip and (x, z) in skip:
                continue
            if b.get(x, y, z)[0] not in ('minecraft:air', 'minecraft:structure_void'):
                continue
            g = rng.choice(mix)
            b.set(x, y, z, g)
            if tufts and g in ('grass_block', 'coarse_dirt', 'dirt') and is_air(b.get(x, y + 1, z)) \
                    and rng.random() < tufts:
                b.set(x, y + 1, z, rng.choice(DRY) if g != 'grass_block' else rng.choice(DRY + ('short_grass',)))


def yard(b, cells, rng, mix=None, y=0, tufts=0.0):
    """Like ``ground`` but over an arbitrary set of (x, z) cells (an organic, rounded yard)."""
    mix = mix or ['coarse_dirt', 'coarse_dirt', 'grass_block', 'dirt', 'grass_block']
    for x, z in sorted(cells):
        if not b.inside(x, y, z) or b.get(x, y, z)[0] not in ('minecraft:air', 'minecraft:structure_void'):
            continue
        g = rng.choice(mix)
        b.set(x, y, z, g)
        if tufts and is_air(b.get(x, y + 1, z)) and rng.random() < tufts:
            b.set(x, y + 1, z, rng.choice(DRY))


def path(b, x, z0, z1, rng, y=0, width=1):
    for z in range(min(z0, z1), max(z0, z1) + 1):
        for i in range(width):
            b.set(x + i, y, z, rng.choice(['dirt_path', 'dirt_path', 'packed_mud', 'coarse_dirt']))


def tufts(b, cells, rng, chance=0.3, y=1):
    for x, z in cells:
        if b.inside(x, y, z) and is_air(b.get(x, y, z)) and rng.random() < chance:
            b.set(x, y, z, rng.choice(DRY))


# ------------------------------------------------------------------ lights
def lantern(b, x, y, z, chain=0, hanging=True):
    """Lantern hung from ``chain`` iron chain links (26.x renamed ``chain`` to ``iron_chain``)."""
    for i in range(chain):
        b.set(x, y - i, z, 'iron_chain', axis='y', waterlogged=False)
    b.set(x, y - chain, z, 'lantern', hanging=hanging, waterlogged=False)


def post_lantern(b, x, y, z, height=2, fence='acacia_fence', base=None):
    if base:
        b.set(x, y, z, base)
        y += 1
    for i in range(height):
        b.set(x, y + i, z, fence)
    b.set(x, y + height, z, 'lantern', hanging=False, waterlogged=False)


def torch(b, x, y, z, facing):
    b.set(x, y, z, 'wall_torch', facing=facing)


# ------------------------------------------------------------------ round huts
def disk(cx, cz, r):
    """Cells whose centre lies within ``r`` of (cx, cz); centres may be half-integers."""
    out = set()
    for x in range(math.floor(cx - r - 1), math.ceil(cx + r + 2)):
        for z in range(math.floor(cz - r - 1), math.ceil(cz + r + 2)):
            if (x - cx) ** 2 + (z - cz) ** 2 <= r * r + 0.3:
                out.add((x, z))
    return out


def outline(cells):
    """Cells of ``cells`` that touch a cell outside it (4-neighbourhood)."""
    return {(x, z) for x, z in cells if any((x + dx, z + dz) not in cells for dx, dz in DIRS.values())}


def round_hut(b, cx, cz, r, y0, wall_h, wall='packed_mud', base='mud_bricks', floor='packed_mud', band=None,
              ground_floor=True, pattern=None):
    """Round hut: a mud-brick footing at ``y0``, a floor, ``wall_h`` courses of wall and an optional band.

    Returns ``(inside, ring, top)`` where ``top`` is the Y of the first roof course.
    """
    cells = disk(cx, cz, r)
    ring = outline(cells)
    inside = cells - ring
    for x, z in cells:
        for yy in range(0, y0 + 1 if ground_floor else y0):
            b.set(x, yy, z, base if (x, z) in ring else 'dirt')
        b.set(x, y0, z, base if (x, z) in ring else floor)
    for yy in range(y0 + 1, y0 + wall_h + 1):
        for x, z in ring:
            b.set(x, yy, z, band if band and yy == y0 + wall_h else wall)
    if pattern:
        # Painted band: colours alternate around the hut in angle order.
        py, colours = pattern
        order = sorted(ring, key=lambda c: math.atan2(c[1] - cz, c[0] - cx))
        for i, (x, z) in enumerate(order):
            b.set(x, py, z, colours[i % len(colours)])
    return inside, ring, y0 + wall_h + 1


def cone_roof(b, cx, cz, r, y, inside, eave=1.4, mat='hay_block', fringe='acacia_trapdoor', peak='acacia_fence',
              step=1.0, ceiling=None):
    """Stepped conical thatch roof over a round hut whose wall interior is ``inside``.

    Course ``i`` is solid everywhere in its disk except over the hollow it shares with
    the course above, so the cone is sealed from within (rooms under it stay
    enclosed). ``ceiling`` closes the first course completely (keeps big rooms small).
    ``fringe`` hangs open trapdoors under the eave rim like a straw skirt. Returns the
    top course's Y.
    """
    radii = []
    rr = r + eave
    while rr > 0.4:
        radii.append(rr)
        # Steeper near the tip, like a real thatched cone.
        rr -= step if rr > 2.2 else step * 0.5
    radii.append(0.0)
    disks = [disk(cx, cz, q) for q in radii]
    hollow = set() if ceiling else set(inside)
    top = y
    for i, cells in enumerate(disks):
        nxt = disks[i + 1] if i + 1 < len(disks) else set()
        # Open only where this course surrounds the cell and the next course covers it.
        hollow = hollow & nxt & (cells - outline(cells))
        for x, z in cells:
            if (x, z) in hollow or not b.inside(x, y + i, z):
                continue
            spec = ceiling if (ceiling and i == 0 and (x, z) in inside) else mat
            b.set(x, y + i, z, spec, **({'axis': 'y'} if spec == 'hay_block' else {}))
        top = y + i
    if fringe:
        rim = outline(disks[0])
        for x, z in rim:
            if not b.inside(x, y - 1, z) or not is_air(b.get(x, y - 1, z)):
                continue
            for d, (dx, dz) in DIRS.items():
                if (x + dx, z + dz) not in disks[0]:
                    b.set(x, y - 1, z, fringe, facing=OPPOSITE[d], half='bottom', open=True, powered=False,
                          waterlogged=False)
                    break
    if peak:
        b.set(round(cx), top + 1, round(cz), peak, clip=True)
    return top


# ------------------------------------------------------------------ rectangular roofs
def hip_roof(b, x0, z0, x1, z1, y, roof, overhang=1, eave=None, ridge_full=False, low=False):
    """Low hipped roof over the wall rectangle; corners take outer stair shapes.

    ``eave`` adds an outer ring of bottom slabs one block beyond the stairs (a deep,
    flared savanna eave). Returns the ridge Y.
    """
    if eave:
        ex0, ez0, ex1, ez1 = x0 - overhang - 1, z0 - overhang - 1, x1 + overhang + 1, z1 + overhang + 1
        for x, z, _, _ in parts.ring(ex0, ez0, ex1, ez1):
            if b.inside(x, y - 1, z) and is_air(b.get(x, y - 1, z)):
                b.set(x, y - 1, z, eave, type='top', waterlogged=False)
    lx, lz, hx, hz = x0 - overhang, z0 - overhang, x1 + overhang, z1 + overhang
    k, top = 0, y
    if low:
        # Half pitch: alternating bottom and top slab courses, eave course of stairs.
        while lx + k <= hx - k and lz + k <= hz - k:
            ax, az, bx, bz = lx + k, lz + k, hx - k, hz - k
            yy = y + k // 2
            top = yy
            last = ax + 1 > bx - 1 or az + 1 > bz - 1
            for x in range(ax, bx + 1):
                for z in range(az, bz + 1):
                    if not (last or x in (ax, bx) or z in (az, bz)):
                        continue
                    b.set(x, yy, z, roof.slab, type='bottom' if k % 2 == 0 else 'top', waterlogged=False, clip=True)
            if last:
                if k % 2 == 1:
                    for x in range(ax, bx + 1):
                        for z in range(az, bz + 1):
                            b.set(x, yy + 1, z, roof.slab, type='bottom', waterlogged=False, clip=True)
                    top = yy + 1
                break
            k += 1
        return top
    while lx + k <= hx - k and lz + k <= hz - k:
        ax, az, bx, bz = lx + k, lz + k, hx - k, hz - k
        yy = y + k
        top = yy
        if ax == bx or az == bz:
            for x in range(ax, bx + 1):
                for z in range(az, bz + 1):
                    if ridge_full:
                        b.set(x, yy, z, roof.full, clip=True)
                    else:
                        b.set(x, yy, z, roof.slab, type='bottom', waterlogged=False, clip=True)
            break
        for x, z, facing, corner in parts.ring(ax, az, bx, bz):
            inward = OPPOSITE[facing]
            if corner:
                inward = 'south' if z == az else 'north'
            b.set(x, yy, z, roof.stairs, facing=inward, half='bottom', clip=True)
        k += 1
    return top


def thatch_hip(b, x0, z0, x1, z1, y, overhang=1, mat='hay_block', fringe='acacia_trapdoor', cap='acacia_slab'):
    """Stepped hay-bale hip roof (each course one block in) with a straw fringe."""
    lx, lz, hx, hz = x0 - overhang, z0 - overhang, x1 + overhang, z1 + overhang
    k, top = 0, y
    while lx + k <= hx - k and lz + k <= hz - k:
        ax, az, bx, bz = lx + k, lz + k, hx - k, hz - k
        yy = y + k
        top = yy
        last = ax + 1 > bx - 1 or az + 1 > bz - 1
        for x in range(ax, bx + 1):
            for z in range(az, bz + 1):
                if last or x in (ax, bx) or z in (az, bz):
                    b.set(x, yy, z, mat, axis='y', clip=True)
        if last:
            if cap:
                for x in range(ax, bx + 1):
                    for z in range(az, bz + 1):
                        b.set(x, yy + 1, z, cap, type='bottom', waterlogged=False, clip=True)
            break
        k += 1
    if fringe:
        for x, z, facing, corner in parts.ring(lx - 1, lz - 1, hx + 1, hz + 1):
            if corner:
                continue
            if b.inside(x, y, z) and is_air(b.get(x, y, z)):
                b.set(x, y, z, fringe, facing=facing, half='top', open=True, powered=False, waterlogged=False)
    return top


# ------------------------------------------------------------------ walls and openings
def slit(b, x, y, z, height=1, mat='acacia_fence'):
    """A barred window: acacia fence in the wall opening (keeps rooms sealed, lets light in)."""
    for j in range(height):
        b.set(x, y + j, z, mat)


def glazed(b, x, y, z, out, height=1, sill=True, shutters='acacia_trapdoor'):
    b.set(x, y, z, 'glass_pane')
    if height > 1:
        b.set(x, y + 1, z, 'glass_pane')
    dx, dz = DIRS[out]
    if sill and b.inside(x + dx, y - 1, z + dz) and is_air(b.get(x + dx, y - 1, z + dz)):
        b.set(x + dx, y - 1, z + dz, 'acacia_trapdoor', facing=out, half='top', open=False, powered=False,
              waterlogged=False)
    if shutters:
        lx, lz = DIRS[CLOCKWISE[out]]
        for s in (-1, 1):
            sx, sz = x + dx + lx * s, z + dz + lz * s
            for j in range(height):
                if b.inside(sx, y + j, sz) and is_air(b.get(sx, y + j, sz)):
                    b.set(sx, y + j, sz, shutters, facing=out, half='bottom', open=True, powered=False,
                          waterlogged=False)


def door(b, x, y, z, out, wood='acacia', step=None, hinge='left'):
    """Door in a wall facing ``out``, with an optional mud-brick step outside."""
    dx, dz = DIRS[out]
    b.door(x, y, z, facing=OPPOSITE[out], wood=wood, hinge=hinge)
    if step:
        b.set(x + dx, y - 1, z + dz, step, facing=OPPOSITE[out], half='bottom', lock=True)


def mud_wall(b, cells, y0, height, mat='mud_bricks', cap='mud_brick_wall', base=None):
    """Compound wall: ``height`` courses with a wall-block coping."""
    for x, z in cells:
        if base:
            b.set(x, 0, z, base)
        for yy in range(y0, y0 + height):
            b.set(x, yy, z, mat)
        if cap:
            b.set(x, y0 + height, z, cap)


def woven_fence(b, cells, y=1, gate=None, gate_facing='north', fence='acacia_fence'):
    for x, z in cells:
        if gate and (x, z) == gate:
            b.set(x, y, z, f'{fence}_gate', facing=gate_facing, open=False, in_wall=False, powered=False)
        else:
            b.set(x, y, z, fence)


def verandah(b, x0, z0, x1, z1, y_floor, posts, roof_y, deck='acacia_planks', post='stripped_acacia_log',
             roof=None, roof_facing='south', slab='acacia_slab'):
    """Raised deck with log posts and a lean-to roof of stairs (``roof_facing`` = high side)."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            for yy in range(0, y_floor):
                if is_air(b.get(x, yy, z)) or b.get(x, yy, z)[0] == 'minecraft:structure_void':
                    b.set(x, yy, z, 'packed_mud' if yy < y_floor - 1 else 'mud_bricks')
            b.set(x, y_floor, z, deck)
    for px, pz in posts:
        for yy in range(y_floor + 1, roof_y):
            b.set(px, yy, pz, post, axis='y')
    if roof:
        for x in range(x0 - 1, x1 + 2):
            for z in range(z0 - 1 if roof_facing in ('east', 'west') else z0, z1 + 2 if roof_facing in ('east', 'west') else z1 + 1):
                if b.inside(x, roof_y, z) and is_air(b.get(x, roof_y, z)):
                    b.set(x, roof_y, z, roof.stairs, facing=roof_facing, half='bottom')


# ------------------------------------------------------------------ furniture
def bed_nook(b, x, y, z, facing, color, chest_at=None, chest_facing='south'):
    b.bed(x, y, z, facing, color)
    if chest_at:
        b.chest(*chest_at, chest_facing, loot=LOOT)


def stool(b, x, y, z, wood='acacia'):
    b.set(x, y, z, f'{wood}_slab', type='bottom', waterlogged=False)


def low_table(b, x, y, z, wood='acacia', top='acacia_pressure_plate'):
    b.set(x, y, z, f'{wood}_fence')
    b.set(x, y + 1, z, top, **({'powered': False} if top.endswith('pressure_plate') else {}))


def pot(b, x, y, z, rng=None, plant=None):
    if plant:
        b.set(x, y, z, plant)
    else:
        b.set(x, y, z, 'decorated_pot', facing='north', waterlogged=False, cracked=False,
              nbt={'id': 'minecraft:decorated_pot'})


def hearth(b, x, y, z, lit=False):
    """Indoor cook-fire ring: a campfire (unlit indoors) in a ring of mud-brick slabs is too fussy; keep a
    single campfire on a packed-mud floor."""
    b.set(x, y, z, 'campfire', lit=lit, signal_fire=False, facing='north', waterlogged=False)


def firepit(b, x, y, z, ring='mud_brick_slab', lit=True, benches=()):
    """Cook-fire with campfire benches on the ``benches`` sides (each faces the fire) and slabs elsewhere."""
    b.set(x, y, z, 'campfire', lit=lit, signal_fire=False, facing='north', waterlogged=False)
    for side, (dx, dz) in DIRS.items():
        if not b.inside(x + dx, y, z + dz) or not is_air(b.get(x + dx, y, z + dz)):
            continue
        if side in benches:
            b.custom(x + dx, y, z + dz, 'campfire_bench', facing=OPPOSITE[side])
        else:
            b.set(x + dx, y, z + dz, ring, type='bottom', waterlogged=False)


def drying_rack(b, x, z, axis='x', length=3, y=1, hides=('brown', 'orange', 'white'), face='north'):
    """Two posts and a rail with hides (wall banners) hanging from it."""
    dx, dz = (1, 0) if axis == 'x' else (0, 1)
    for i in (0, length - 1):
        for yy in (y, y + 1):
            b.set(x + dx * i, yy, z + dz * i, 'acacia_fence')
    for i in range(length):
        b.set(x + dx * i, y + 2, z + dz * i, 'acacia_fence')
    for n, i in enumerate(range(1, length - 1)):
        color = hides[n % len(hides)]
        b.set(x + dx * i, y + 1, z + dz * i, f'{color}_wall_banner', facing=face)


def hay_pile(b, cells, rng, high=()):
    for x, z in cells:
        b.set(x, 1, z, 'hay_block', axis=rng.choice(['x', 'y', 'z']))
    for x, z in high:
        b.set(x, 2, z, 'hay_block', axis='y')


# ------------------------------------------------------------------ trees
def acacia_tree(b, x, y, z, rng, height=4, lean='east', lean_len=2, canopy=2.6, second=None, clip=True):
    """Savanna acacia: a trunk that kinks to one side under a flat, wide crown.

    ``second`` = (direction, length, radius) grows a second, lower crown on a branch.
    """
    for i in range(height):
        b.set(x, y + i, z, 'acacia_log', axis='y')
    dx, dz = DIRS[lean]
    tx, ty, tz = x, y + height - 1, z
    for i in range(lean_len):
        tx, ty, tz = tx + dx, ty + 1, tz + dz
        b.set(tx, ty, tz, 'acacia_wood', clip=clip)
    crown(b, tx, ty + 1, tz, canopy, rng, clip)
    if second:
        d2, l2, r2 = second
        ex, ez = DIRS[d2]
        sx, sy, sz = x, y + height - 2, z
        for i in range(l2):
            sx, sy, sz = sx + ex, sy + (1 if i else 0), sz + ez
            b.set(sx, sy, sz, 'acacia_wood', clip=clip)
        crown(b, sx, sy + 1, sz, r2, rng, clip)
    return ty


def crown(b, x, y, z, r, rng, clip=True):
    """Flat acacia crown: a wide leaf layer with a smaller one on top."""
    b.set(x, y - 1, z, 'acacia_wood', clip=clip) if is_air(b.get(x, y - 1, z)) else None
    for cx, cz in disk(x, z, r):
        if (cx - x) ** 2 + (cz - z) ** 2 > (r - 0.6) ** 2 and rng.random() < .25:
            continue
        if b.inside(cx, y, cz) and is_air(b.get(cx, y, cz)):
            b.set(cx, y, cz, 'acacia_leaves', **LEAF)
    for cx, cz in disk(x, z, max(1.0, r - 1.2)):
        if b.inside(cx, y + 1, cz) and is_air(b.get(cx, y + 1, cz)):
            b.set(cx, y + 1, cz, 'acacia_leaves', **LEAF)
