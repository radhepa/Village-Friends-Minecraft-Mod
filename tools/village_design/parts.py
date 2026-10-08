"""Architectural parts shared by the plains buildings.

Every helper only *draws* into a ``Build``; buildings stay independent files
that combine these parts in their own way.
"""
import random

from .kit import DIRS, OPPOSITE, CLOCKWISE, COUNTER, is_air, block

WOODS = ('oak', 'spruce', 'birch', 'dark_oak', 'jungle', 'acacia', 'mangrove', 'cherry', 'pale_oak')


class Roof:
    def __init__(self, stairs, slab, full):
        self.stairs, self.slab, self.full = stairs, slab, full


ROOFS = {
    'spruce': Roof('spruce_stairs', 'spruce_slab', 'spruce_planks'),
    'dark_oak': Roof('dark_oak_stairs', 'dark_oak_slab', 'dark_oak_planks'),
    'oak': Roof('oak_stairs', 'oak_slab', 'oak_planks'),
    'birch': Roof('birch_stairs', 'birch_slab', 'birch_planks'),
    'slate': Roof('deepslate_tile_stairs', 'deepslate_tile_slab', 'deepslate_tiles'),
    'brick': Roof('brick_stairs', 'brick_slab', 'bricks'),
    'mud': Roof('mud_brick_stairs', 'mud_brick_slab', 'mud_bricks'),
    'mangrove': Roof('mangrove_stairs', 'mangrove_slab', 'mangrove_planks'),
    'stone': Roof('stone_brick_stairs', 'stone_brick_slab', 'stone_bricks'),
    'cobble': Roof('cobblestone_stairs', 'cobblestone_slab', 'cobblestone'),
}


class Style:
    """Material set for one building."""

    def __init__(self, frame='stripped_spruce_log', fill='calcite', floor='spruce_planks', roof='spruce',
                 base='cobblestone', base_stairs='cobblestone_stairs', trim='spruce', door='spruce',
                 upper_fill=None, ceiling=None, accent='oak'):
        self.frame, self.fill, self.floor = frame, fill, floor
        self.roof = ROOFS[roof] if isinstance(roof, str) else roof
        self.base, self.base_stairs, self.trim, self.door = base, base_stairs, trim, door
        self.upper_fill = upper_fill or fill
        self.ceiling = ceiling or floor
        self.accent = accent


PILLAR_ENDINGS = ('_log', '_wood', '_stem', '_hyphae', '_pillar', 'froglight')
PILLARS = {'hay_block', 'basalt', 'polished_basalt', 'bone_block', 'iron_chain', 'chain', 'bamboo_block',
           'stripped_bamboo_block', 'muddy_mangrove_roots', 'deepslate'}


def log(name, axis='y'):
    """A pillar block turned along ``axis``; blocks without an axis (cut sandstone, planks...) stay plain."""
    base = name.split('[')[0].split(':')[-1]
    return block(name, axis=axis) if base.endswith(PILLAR_ENDINGS) or base in PILLARS else block(name)


def along(x0, z0, x1, z1):
    """Positions on a straight horizontal run (inclusive)."""
    if x0 == x1:
        return [(x0, z) for z in range(min(z0, z1), max(z0, z1) + 1)]
    return [(x, z0) for x in range(min(x0, x1), max(x0, x1) + 1)]


# ------------------------------------------------------------------- volumes
def ring(x0, z0, x1, z1):
    """Perimeter cells of a rectangle, as (x, z, outward facing, is_corner)."""
    cells = []
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            corner = x in (x0, x1)
            cells.append((x, z, 'north' if z == z0 else 'south', corner))
    for z in range(z0 + 1, z1):
        for x in (x0, x1):
            cells.append((x, z, 'west' if x == x0 else 'east', False))
    return cells


def posts_for(length, spacing=4):
    """Evenly spread post offsets along a wall of ``length`` cells (corners included)."""
    last = length - 1
    if last <= spacing:
        return {0, last}
    parts = max(1, round(last / spacing))
    return {round(i * last / parts) for i in range(parts + 1)}


def timber_walls(b, x0, z0, x1, z1, y0, y1, frame, fill, spacing=4, beam_top=True, posts=True):
    """Timber-framed walls: corner and intermediate posts, a top beam course, plaster infill."""
    px = posts_for(x1 - x0 + 1, spacing) if posts else {0, x1 - x0}
    pz = posts_for(z1 - z0 + 1, spacing) if posts else {0, z1 - z0}
    for x, z, facing, corner in ring(x0, z0, x1, z1):
        is_post = corner or (facing in ('north', 'south') and (x - x0) in px) or \
            (facing in ('west', 'east') and (z - z0) in pz)
        for y in range(y0, y1 + 1):
            if is_post:
                b.set(x, y, z, log(frame, 'y'))
            elif beam_top and y == y1:
                b.set(x, y, z, log(frame, 'x' if facing in ('north', 'south') else 'z'))
            else:
                b.set(x, y, z, fill)


def solid_walls(b, x0, z0, x1, z1, y0, y1, mat, corners=None):
    for x, z, facing, corner in ring(x0, z0, x1, z1):
        for y in range(y0, y1 + 1):
            b.set(x, y, z, log(corners, 'y') if corners and corner else mat)


def beam_ring(b, x0, z0, x1, z1, y, frame):
    for x, z, facing, corner in ring(x0, z0, x1, z1):
        b.set(x, y, z, log(frame, 'y') if corner else log(frame, 'x' if facing in ('north', 'south') else 'z'))


def floor(b, x0, z0, x1, z1, y, mat):
    b.fill(x0, y, z0, x1, y, z1, mat)


def foundation(b, x0, z0, x1, z1, style, top=1, interior=None):
    """Stone plinth from Y=0 to ``top``; interior floor at ``top``."""
    for y in range(0, top + 1):
        for x, z, facing, corner in ring(x0, z0, x1, z1):
            b.set(x, y, z, style.base)
        b.fill(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, interior or style.floor if y == top else 'dirt')


def plinth_skirt(b, x0, z0, x1, z1, y, mat_stairs, skip=()):
    """Sloped stone skirt around a foundation (stairs leaning against the walls)."""
    for x in range(x0, x1 + 1):
        for z, f in ((z0 - 1, 'south'), (z1 + 1, 'north')):
            if (x, z) not in skip and b.inside(x, y, z) and is_air(b.get(x, y, z)):
                b.set(x, y, z, mat_stairs, facing=f, half='bottom')
    for z in range(z0, z1 + 1):
        for x, f in ((x0 - 1, 'east'), (x1 + 1, 'west')):
            if (x, z) not in skip and b.inside(x, y, z) and is_air(b.get(x, y, z)):
                b.set(x, y, z, mat_stairs, facing=f, half='bottom')


# --------------------------------------------------------------------- roofs
def gable_roof(b, x0, z0, x1, z1, y, roof, axis='x', overhang=1, rake=1, gable=None, pitch=1,
               eave_trim=None, clip=True):
    """Gable roof over the wall rectangle (x0..x1, z0..z1) whose top course is at ``y``.

    ``axis`` is the ridge direction; ``gable`` fills the triangular end walls.
    ``pitch`` 2 makes a steep roof (two blocks of rise per step). Returns the ridge Y.
    """
    ra, rb = rake if isinstance(rake, tuple) else (rake, rake)
    if axis == 'x':
        lo, hi, wl, wh = z0 - overhang, z1 + overhang, z0, z1
        run, ends = range(x0 - ra, x1 + rb + 1), (x0, x1)
        near, far = 'south', 'north'
    else:
        lo, hi, wl, wh = x0 - overhang, x1 + overhang, x0, x1
        run, ends = range(z0 - ra, z1 + rb + 1), (z0, z1)
        near, far = 'east', 'west'

    def put(u, yy, v, spec, only_air=False, **kw):
        x, z = (v, u) if axis == 'x' else (u, v)
        if not b.inside(x, yy, z):
            assert clip and 0 <= yy < b.h, f'{b.name}: roof does not fit the template at {(x, yy, z)}'
            return
        if only_air and not is_air(b.get(x, yy, z)):
            return
        b.set(x, yy, z, spec, **kw)

    k, ridge = 0, y
    while lo + k <= hi - k:
        a, c, top = lo + k, hi - k, y + pitch * k
        for v in run:
            if a == c:
                if pitch == 2:
                    put(a, top - 1, v, roof.full)
                put(a, top, v, roof.slab, type='bottom', waterlogged=False)
            else:
                put(a, top, v, roof.stairs, facing=near, half='bottom')
                put(c, top, v, roof.stairs, facing=far, half='bottom')
                if pitch == 2 and k > 0:
                    put(a, top - 1, v, roof.full)
                    put(c, top - 1, v, roof.full)
        ridge = top
        if gable and k > 0:
            for e in ends:
                for yy in range(top - pitch + 1, top + 1):
                    for u in range(max(a + 1, wl + 1), min(c, wh)):
                        put(u, yy, e, gable, only_air=True)
        k += 1
    if eave_trim:
        for v in run:
            for u, f in ((lo, near), (hi, far)):
                put(u, y - 1, v, eave_trim, only_air=True, facing=OPPOSITE[f], half='top')
    return ridge


def shed_roof(b, x0, z0, x1, z1, y, roof, slope='south', overhang=1):
    """Single-pitch roof falling toward ``slope``."""
    dx, dz = DIRS[slope]
    up = OPPOSITE[slope]
    if dz:
        rows = range(z0 - overhang, z1 + overhang + 1)
        rows = list(rows) if dz > 0 else list(reversed(rows))
        for i, z in enumerate(reversed(rows)):
            for x in range(x0 - overhang, x1 + overhang + 1):
                b.set(x, y + i, z, roof.stairs, facing=up, half='bottom', clip=True)
    else:
        cols = list(range(x0 - overhang, x1 + overhang + 1))
        cols = cols if dx > 0 else list(reversed(cols))
        for i, x in enumerate(reversed(cols)):
            for z in range(z0 - overhang, z1 + overhang + 1):
                b.set(x, y + i, z, roof.stairs, facing=up, half='bottom', clip=True)


# ------------------------------------------------------------- openings
def window(b, x, y, z, out, height=2, width=1, trim='spruce', shutters=True, box=None, sill=None,
           pane='glass_pane'):
    """Glass window cut into a wall that faces ``out`` (outward direction).

    ``shutters`` adds open trapdoor shutters; ``box`` a flower box (leaves) below;
    ``sill`` a stair sill under the window.
    """
    dx, dz = DIRS[out]
    lateral = CLOCKWISE[out]
    lx, lz = DIRS[lateral]
    for i in range(width):
        for j in range(height):
            b.set(x + lx * i, y + j, z + lz * i, pane)
    ox, oz = x + dx, z + dz
    if shutters:
        for j in range(height):
            for side, sign in ((-1, -1), (width, 1)):
                sx, sz = ox + lx * side, oz + lz * side
                if b.inside(sx, y + j, sz) and is_air(b.get(sx, y + j, sz)):
                    b.set(sx, y + j, sz, f'{trim}_trapdoor', facing=out, half='bottom', open=True,
                          powered=False, waterlogged=False)
    for i in range(width):
        bx, bz = ox + lx * i, oz + lz * i
        if box and b.inside(bx, y - 1, bz) and is_air(b.get(bx, y - 1, bz)):
            b.set(bx, y - 1, bz, box, persistent=True, distance=1, waterlogged=False)
        elif sill and b.inside(bx, y - 1, bz) and is_air(b.get(bx, y - 1, bz)):
            b.set(bx, y - 1, bz, f'{sill}_stairs', facing=OPPOSITE[out], half='top', lock=True)


def front_door(b, x, y, z, out, wood='spruce', step=None, awning=None, lamps=True, hinge='left'):
    """Door in a wall facing ``out``; optional step (stairs) and awning (slab roof) outside."""
    dx, dz = DIRS[out]
    b.door(x, y, z, facing=OPPOSITE[out], wood=wood, hinge=hinge)
    if step:
        b.set(x + dx, y - 1, z + dz, step, facing=OPPOSITE[out], half='bottom', lock=True)
    if awning:
        lateral = CLOCKWISE[out]
        lx, lz = DIRS[lateral]
        for i in (-1, 0, 1):
            ax, az = x + dx + lx * i, z + dz + lz * i
            if b.inside(ax, y + 2, az) and is_air(b.get(ax, y + 2, az)):
                if i == 0:
                    b.set(ax, y + 2, az, awning, type='top')
                else:
                    b.set(ax, y + 2, az, awning.replace('_slab', '_stairs'), facing=OPPOSITE[out], half='top',
                          lock=True)
    if lamps:
        lateral = CLOCKWISE[out]
        lx, lz = DIRS[lateral]
        for i in (-1, 1):
            lx2, lz2 = x + dx + lx * i, z + dz + lz * i
            if b.inside(lx2, y + 1, lz2) and is_air(b.get(lx2, y + 1, lz2)) and not is_air(b.get(x + lx * i, y + 1, z + lz * i)):
                b.set(lx2, y + 1, lz2, 'wall_torch', facing=out)
                break


def lantern(b, x, y, z, hanging=True, chain=0):
    for i in range(chain):
        b.set(x, y - i, z, 'chain', axis='y', waterlogged=False)
    b.set(x, y - chain, z, 'lantern', hanging=hanging, waterlogged=False)


def chimney(b, x, z, y0, y1, mat='bricks', smoke=True, cap=None):
    """Chimney column from ``y0`` to ``y1``; a lit campfire on top makes smoke."""
    for y in range(y0, y1 + 1):
        b.set(x, y, z, mat)
    if smoke:
        b.set(x, y1 + 1, z, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    elif cap:
        b.set(x, y1 + 1, z, cap)


def lamp_post(b, x, y, z, height=3, fence='spruce_fence', top='lantern', base=None):
    if base:
        b.set(x, y, z, base)
        y += 1
    for i in range(height):
        b.set(x, y + i, z, fence)
    b.set(x, y + height, z, top, hanging=False, waterlogged=False) if top == 'lantern' else b.set(x, y + height, z, top)


def hanging_lamp_post(b, x, y, z, arm, height=4, fence='spruce_fence'):
    """Post with an arm toward ``arm`` and a hanging lantern."""
    for i in range(height):
        b.set(x, y + i, z, fence)
    dx, dz = DIRS[arm]
    b.set(x, y + height, z, fence)
    b.set(x + dx, y + height, z + dz, fence)
    b.set(x + dx, y + height - 1, z + dz, 'lantern', hanging=True, waterlogged=False)


# --------------------------------------------------------------- furniture
def table(b, x, y, z, wood='spruce', cloth=None):
    b.set(x, y, z, f'{wood}_fence')
    b.set(x, y + 1, z, cloth or f'{wood}_pressure_plate', **({} if cloth else {'powered': False}))


def chair(b, x, y, z, facing, wood='spruce'):
    """Stair chair; ``facing`` is the side of its backrest."""
    b.set(x, y, z, f'{wood}_stairs', facing=facing, half='bottom', shape='straight', waterlogged=False, lock=True)


def bench(b, x, y, z, facing, length=2, wood='spruce'):
    """Stair bench with trapdoor arms; ``facing`` is the backrest side."""
    lateral = CLOCKWISE[facing]
    lx, lz = DIRS[lateral]
    for i in range(length):
        chair(b, x + lx * i, y, z + lz * i, facing, wood)


def rug(b, x0, z0, x1, z1, y, color, border=None):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            b.set(x, y, z, f'{border if (border and edge) else color}_carpet')


def shelf(b, x, y, z, facing, items=('potted_red_tulip', 'flower_pot'), wood='spruce'):
    b.set(x, y, z, f'{wood}_trapdoor', facing=facing, half='top', open=False, powered=False, waterlogged=False)


def bookshelf_wall(b, x0, z0, x1, z1, y0, y1):
    b.fill(x0, y0, z0, x1, y1, z1, 'bookshelf')


# ------------------------------------------------------------------ nature
def flowers(rng):
    return rng.choice(['poppy', 'dandelion', 'cornflower', 'azure_bluet', 'oxeye_daisy', 'allium',
                       'red_tulip', 'orange_tulip', 'white_tulip', 'pink_tulip', 'lily_of_the_valley'])


def flower_bed(b, x0, z0, x1, z1, y, rng, border='spruce_trapdoor', soil='rooted_dirt', density=0.8,
               ground_y=None):
    """Planted bed: soil at ``y`` with flowers above."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, y, z, soil if soil != 'grass_block' else 'grass_block')
            if rng.random() < density:
                b.set(x, y + 1, z, flowers(rng))


def bush(b, x, y, z, kind='azalea_leaves'):
    b.set(x, y, z, kind, persistent=True, distance=1, waterlogged=False)


def oak_tree(b, x, y, z, rng, height=5, wood='oak', leaves='oak_leaves', radius=2):
    """Hand-shaped round tree (trunk base at ``y``)."""
    for i in range(height):
        b.set(x, y + i, z, log(f'{wood}_log'))
    top = y + height
    for dy in range(-2, 2):
        r = radius if dy in (-1, 0) else radius - 1
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if abs(dx) == r and abs(dz) == r and (dy != -1 or rng.random() < .5):
                    continue
                px, py, pz = x + dx, top + dy, z + dz
                if b.inside(px, py, pz) and is_air(b.get(px, py, pz)):
                    b.set(px, py, pz, leaves, persistent=True, distance=1, waterlogged=False)
    b.set(x, top + 2, z, leaves, persistent=True, distance=1, waterlogged=False, clip=True)


def spruce_tree(b, x, y, z, height=7):
    for i in range(height):
        b.set(x, y + i, z, log('spruce_log'))
    layers = [(height - 1, 0), (height - 2, 1), (height - 3, 1), (height - 4, 2), (height - 5, 1), (height - 6, 2)]
    for dy, r in layers:
        if dy < 1:
            continue
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if abs(dx) + abs(dz) > r + (1 if r == 2 else 0):
                    continue
                px, py, pz = x + dx, y + dy, z + dz
                if b.inside(px, py, pz) and is_air(b.get(px, py, pz)):
                    b.set(px, py, pz, 'spruce_leaves', persistent=True, distance=1, waterlogged=False)
    b.set(x, y + height, z, 'spruce_leaves', persistent=True, distance=1, waterlogged=False, clip=True)


def birch_tree(b, x, y, z, rng, height=6):
    oak_tree(b, x, y, z, rng, height=height, wood='birch', leaves='birch_leaves', radius=2)


def woodpile(b, x, y, z, along_axis='x', length=3, wood='spruce', height=2):
    dx, dz = (1, 0) if along_axis == 'x' else (0, 1)
    cross = 'z' if along_axis == 'x' else 'x'
    for i in range(length):
        for j in range(height if i not in (0, length - 1) else max(1, height - 1)):
            b.set(x + dx * i, y + j, z + dz * i, log(f'{wood}_log', cross))


def crate_stack(b, x, y, z, rng):
    b.set(x, y, z, 'barrel', facing=rng.choice(['up', 'north', 'east']), open=False)
    if rng.random() < .5:
        b.set(x, y + 1, z, 'hay_block', axis='y')


def grass_tufts(b, cells, y, rng, chance=0.25):
    for x, z in cells:
        if b.inside(x, y, z) and is_air(b.get(x, y, z)) and rng.random() < chance:
            b.set(x, y, z, rng.choice(['short_grass', 'short_grass', 'fern', flowers(rng)]))


# ------------------------------------------------------------------ house bodies
class Body:
    """A rectangular building volume: plinth, floors, framed walls and a roof.

    ``x0..x1, z0..z1`` is the ground-floor wall rectangle. ``heights`` lists the
    wall height of each storey. Floor ``i`` stands on ``self.floor_y[i]`` and its
    walls occupy ``floor_y[i]+1 .. floor_y[i]+heights[i]``; a beam course sits
    on top. ``jetty`` names sides where upper storeys overhang by one block.
    """

    def __init__(self, b, x0, z0, x1, z1, style, heights=(3,), base=1, jetty=(), stone_ground=False,
                 spacing=4):
        self.b, self.style = b, style
        self.x0, self.z0, self.x1, self.z1 = x0, z0, x1, z1
        self.heights, self.base, self.jetty = list(heights), base, set(jetty)
        self.stone_ground, self.spacing = stone_ground, spacing
        self.floor_y = []
        y = base
        for h in self.heights:
            self.floor_y.append(y)
            y += h + 1
        self.top = y  # beam course and ceiling above the last storey

    def rect(self, level):
        x0, z0, x1, z1 = self.x0, self.z0, self.x1, self.z1
        if level > 0:
            x0 -= 'west' in self.jetty
            x1 += 'east' in self.jetty
            z0 -= 'north' in self.jetty
            z1 += 'south' in self.jetty
        return x0, z0, x1, z1

    def walls_y(self, level):
        f = self.floor_y[level]
        return f + 1, f + self.heights[level]

    def build(self, ceiling=True):
        b, st = self.b, self.style
        foundation(b, self.x0, self.z0, self.x1, self.z1, st, top=self.base)
        for level, h in enumerate(self.heights):
            x0, z0, x1, z1 = self.rect(level)
            fy = self.floor_y[level]
            y0, y1 = fy + 1, fy + h
            if level > 0:
                # Floor platform and its beam ring (which is the jetty sill when overhanging).
                floor(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, fy, st.floor)
                beam_ring(b, x0, z0, x1, z1, fy, st.frame)
                self._corbels(level)
            if level == 0 and self.stone_ground:
                solid_walls(b, x0, z0, x1, z1, y0, y1, st.base, corners=None)
                for x, z, facing, corner in ring(x0, z0, x1, z1):
                    if corner:
                        for y in range(y0, y1 + 1):
                            b.set(x, y, z, 'stone_bricks' if st.base == 'cobblestone' else st.base)
            else:
                timber_walls(b, x0, z0, x1, z1, y0, y1, st.frame, st.fill if level == 0 else st.upper_fill,
                             spacing=self.spacing, beam_top=False)
        x0, z0, x1, z1 = self.rect(len(self.heights) - 1)
        beam_ring(b, x0, z0, x1, z1, self.top, st.frame)
        if ceiling:
            floor(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, self.top, st.ceiling)
        return self

    def _corbels(self, level):
        b, st = self.b, self.style
        fy = self.floor_y[level]
        x0, z0, x1, z1 = self.x0, self.z0, self.x1, self.z1
        stairs = f'{st.trim}_stairs'
        for side in self.jetty:
            if side in ('north', 'south'):
                z = z0 - 1 if side == 'north' else z1 + 1
                for x in sorted(posts_for(x1 - x0 + 1, self.spacing)):
                    b.set(x0 + x, fy - 1, z, stairs, facing=OPPOSITE[side], half='top', lock=True)
            else:
                x = x0 - 1 if side == 'west' else x1 + 1
                for z in sorted(posts_for(z1 - z0 + 1, self.spacing)):
                    b.set(x, fy - 1, z0 + z, stairs, facing=OPPOSITE[side], half='top', lock=True)

    def roof(self, axis='x', pitch=1, overhang=1, rake=1, gable=None, trim=None, ends=True):
        """Gable roof. ``trim`` (a Roof) edges the rakes and ridge in a contrasting material."""
        x0, z0, x1, z1 = self.rect(len(self.heights) - 1)
        st = self.style
        ridge = gable_roof(self.b, x0, z0, x1, z1, self.top, st.roof, axis=axis, overhang=overhang, rake=rake,
                           gable=gable or st.upper_fill, pitch=pitch)
        if trim:
            self.trim_rakes(axis, trim, overhang, rake if isinstance(rake, int) else max(rake), pitch)
        self.ridge = ridge
        return ridge

    def trim_rakes(self, axis, trim, overhang=1, rake=1, pitch=1):
        """Swap the outermost rake stairs (gable edges) for a contrasting material."""
        b = self.b
        x0, z0, x1, z1 = self.rect(len(self.heights) - 1)
        if axis == 'x':
            edges = (x0 - rake, x1 + rake)
            for x in edges:
                for z in range(z0 - overhang, z1 + overhang + 1):
                    for y in range(self.top, self.top + 20):
                        s = b.get(x, y, z) if b.inside(x, y, z) else None
                        if s and s[0].endswith('_stairs') and s[0] == 'minecraft:' + self.style.roof.stairs:
                            b.set(x, y, z, (f'minecraft:{trim.stairs}', s[1]))
                        elif s and s[0] == 'minecraft:' + self.style.roof.slab:
                            b.set(x, y, z, (f'minecraft:{trim.slab}', s[1]))
                        elif s and s[0] == 'minecraft:' + self.style.roof.full:
                            b.set(x, y, z, trim.full)
        else:
            edges = (z0 - rake, z1 + rake)
            for z in edges:
                for x in range(x0 - overhang, x1 + overhang + 1):
                    for y in range(self.top, self.top + 20):
                        s = b.get(x, y, z) if b.inside(x, y, z) else None
                        if s and s[0] == 'minecraft:' + self.style.roof.stairs:
                            b.set(x, y, z, (f'minecraft:{trim.stairs}', s[1]))
                        elif s and s[0] == 'minecraft:' + self.style.roof.slab:
                            b.set(x, y, z, (f'minecraft:{trim.slab}', s[1]))
                        elif s and s[0] == 'minecraft:' + self.style.roof.full:
                            b.set(x, y, z, trim.full)

    def windows(self, level, side, offsets, height=2, box=None, shutters=True, sill=None, y=None):
        """Windows on one wall of a storey at offsets measured from the wall's west/north corner."""
        x0, z0, x1, z1 = self.rect(level)
        wy = y if y is not None else self.floor_y[level] + 2
        for o in offsets:
            o, width = (o, 1) if isinstance(o, int) else o
            if side in ('north', 'south'):
                x, z = x0 + o, (z0 if side == 'north' else z1)
            else:
                x, z = (x0 if side == 'west' else x1), z0 + o
            # ``window`` widens toward the outward direction's clockwise side.
            if side in ('south', 'west'):
                x, z = (x + width - 1, z) if side == 'south' else (x, z + width - 1)
            window(self.b, x, wy, z, side, height=height, width=width, trim=self.style.trim, shutters=shutters,
                   box=box, sill=sill)

    def gable_window(self, side, height=1, pane='glass_pane'):
        """Small window in a gable end (the end walls of the ridge axis)."""
        x0, z0, x1, z1 = self.rect(len(self.heights) - 1)
        y = self.top + 2
        if side in ('west', 'east'):
            x, z = (x0 if side == 'west' else x1), (z0 + z1) // 2
        else:
            x, z = (x0 + x1) // 2, (z0 if side == 'north' else z1)
        for j in range(height):
            self.b.set(x, y + j, z, pane)
            if (z0 + z1) % 2 == 1 and side in ('west', 'east'):
                self.b.set(x, y + j, z + 1, pane)
            if (x0 + x1) % 2 == 1 and side in ('north', 'south'):
                self.b.set(x + 1, y + j, z, pane)

    def interior_walls(self, level, cells, mat=None):
        b = self.b
        y0, y1 = self.walls_y(level)
        for x, z in cells:
            for y in range(y0, y1 + 1):
                b.set(x, y, z, mat or self.style.floor)


def stair_run(b, x, z, y0, steps, direction, wood='spruce', hole=True):
    """Straight staircase climbing toward ``direction``; clears headroom through the floor above."""
    dx, dz = DIRS[direction]
    for i in range(steps):
        sx, sz, sy = x + dx * i, z + dz * i, y0 + i
        b.set(sx, sy, sz, f'{wood}_stairs', facing=direction, half='bottom', shape='straight', lock=True)
        for h in (1, 2):
            if hole or h == 1:
                b.set(sx, sy + h, sz, 'air')
        # Fill below the run so it reads as solid.
        for yy in range(y0, sy):
            b.set(sx, yy, sz, f'{wood}_planks')


def door_cells(x, z, facing):
    """The two walking cells on either side of a door, for keeping them clear."""
    dx, dz = DIRS[facing]
    return [(x + dx, z + dz), (x - dx, z - dz)]


def pyramid_roof(b, x0, z0, x1, z1, y, stairs, full, pitch=2, finial=None):
    """Hipped pyramid/spire over a square; corner stairs take outer shapes automatically."""
    k = 0
    while x0 + k <= x1 - k and z0 + k <= z1 - k:
        lx, hx, lz, hz = x0 + k, x1 - k, z0 + k, z1 - k
        top = y + pitch * k
        if lx == hx and lz == hz:
            for i in range(pitch):
                b.set(lx, top - i, lz, full)
            y_end = top
            break
        for x in range(lx, hx + 1):
            for z in range(lz, hz + 1):
                if x in (lx, hx) or z in (lz, hz):
                    for i in range(1, pitch if k > 0 else 1):
                        b.set(x, top - i, z, full)
                    f = 'south' if z == lz else 'north' if z == hz else 'east' if x == lx else 'west'
                    b.set(x, top, z, stairs, facing=f, half='bottom')
                else:
                    b.set(x, top, z, full)
        y_end = top
        k += 1
    if finial:
        for i, spec in enumerate(finial):
            b.set((x0 + x1) // 2, y_end + 1 + i, (z0 + z1) // 2, spec)
    return y_end
