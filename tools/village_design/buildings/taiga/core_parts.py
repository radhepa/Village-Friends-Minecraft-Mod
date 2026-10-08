"""Shared drawing helpers for the taiga town centres, civic buildings and streets.

Only draws into a ``Build``; no designs live here. Everything follows the
palette's art direction: horizontal log walls with crossed corners, mossy
stone plinths, steep shingle roofs with moss patches, log-post porches,
lanterns and forest-floor yards.
"""
import math

from ...kit import is_air
from ...roads import noise, smooth
from ... import parts
from .palette import ROOFS

LOOT_HOUSE = 'minecraft:chests/village/village_taiga_house'
LEAVES = dict(persistent=True, distance=1, waterlogged=False)
# 26.3 renamed the chain block; the shared kit still writes the old id.
RENAMED = {'minecraft:chain': 'minecraft:iron_chain'}


def fix_ids(b):
    """Swap ids the shared helpers write under their pre-26.3 names."""
    for pos, state in list(b.grid.items()):
        if state[0] in RENAMED:
            b.grid[pos] = (RENAMED[state[0]], state[1])
    return b


def chain(b, x, y, z):
    b.set(x, y, z, 'iron_chain', axis='y', waterlogged=False)


def hang_lantern(b, x, y, z, links=0):
    """Lantern hanging at ``y - links`` from the block above ``y``."""
    for i in range(links):
        chain(b, x, y - i, z)
    b.set(x, y - links, z, 'lantern', hanging=True, waterlogged=False)


def stand_lantern(b, x, y, z):
    b.set(x, y, z, 'lantern', hanging=False, waterlogged=False)


# ------------------------------------------------------------------ log walls
def log_walls(b, x0, z0, x1, z1, y0, y1, wood='spruce', stubs=True, chink=False):
    """Horizontal log walls whose courses cross at the corners.

    Courses alternate which wall runs through the corner, and the through-log
    sticks out one block past the corner, so corners read as notched joints.
    ``chink`` swaps every other course on the long walls for stripped logs
    (light chinking between the logs).
    """
    log, light = f'{wood}_log', f'stripped_{wood}_log'
    for y in range(y0, y1 + 1):
        p = (y - y0) % 2
        mat = light if chink and p else log
        for x in range(x0, x1 + 1):
            for z in (z0, z1):
                corner = x in (x0, x1)
                b.set(x, y, z, log if corner else mat, axis=('x' if p == 0 else 'z') if corner else 'x')
        for z in range(z0 + 1, z1):
            for x in (x0, x1):
                b.set(x, y, z, mat, axis='z')
        if not stubs:
            continue
        ends = (((x0 - 1, z0), (x1 + 1, z0), (x0 - 1, z1), (x1 + 1, z1)), 'x') if p == 0 else \
            (((x0, z0 - 1), (x0, z1 + 1), (x1, z0 - 1), (x1, z1 + 1)), 'z')
        for x, z in ends[0]:
            if b.inside(x, y, z) and is_air(b.get(x, y, z)):
                b.set(x, y, z, log, axis=ends[1])


def stave_walls(b, x0, z0, x1, z1, y0, y1, a='dark_oak_log', c='stripped_dark_oak_log'):
    """Vertical stave walls: upright logs alternating dark and light."""
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        mat = a if corner or (x + z) % 2 == 0 else c
        for y in range(y0, y1 + 1):
            b.set(x, y, z, mat, axis='y')


def plinth(b, x0, z0, x1, z1, top=1, floor='spruce_planks', seed=0):
    """Mossy rubble-stone plinth from Y=0 to ``top``; floor at ``top``."""
    for y in range(0, top + 1):
        for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
            n = noise(x * 3 + y, z, seed)
            b.set(x, y, z, 'mossy_cobblestone' if n < .45 else 'cobblestone' if n < .8 else 'mossy_stone_bricks')
        b.fill(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, floor if y == top else 'dirt')


def stone_walls(b, x0, z0, x1, z1, y0, y1, seed=0, corners='stripped_dark_oak_log'):
    """Rubble-stone walls with timber corner posts."""
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        for y in range(y0, y1 + 1):
            if corner and corners:
                b.set(x, y, z, corners, axis='y')
                continue
            n = smooth(x + z, y, seed, 2.0) * .6 + noise(x, y * 7 + z, seed) * .4
            b.set(x, y, z, 'mossy_cobblestone' if n < .3 else 'cobblestone' if n < .62 else
                  'stone_bricks' if n < .85 else 'mossy_stone_bricks')


def beam_course(b, x0, z0, x1, z1, y, wood='spruce'):
    parts.beam_ring(b, x0, z0, x1, z1, y, f'stripped_{wood}_log')


def ceiling(b, x0, z0, x1, z1, y, mat='spruce_planks'):
    b.fill(x0, y, z0, x1, y, z1, mat)


# --------------------------------------------------------------------- roofs
MOSS = {
    'minecraft:dark_oak_stairs': 'minecraft:mossy_cobblestone_stairs',
    'minecraft:spruce_stairs': 'minecraft:mossy_cobblestone_stairs',
    'minecraft:dark_oak_slab': 'minecraft:mossy_cobblestone_slab',
    'minecraft:spruce_slab': 'minecraft:mossy_cobblestone_slab',
}


def mossify(b, box, seed, amount=0.3):
    """Patches of moss on exposed roof stairs and slabs inside ``box``."""
    x0, y0, z0, x1, y1, z1 = box
    for (x, y, z), state in list(b.grid.items()):
        if not (x0 <= x <= x1 and y0 <= y <= y1 and z0 <= z <= z1) or state[0] not in MOSS:
            continue
        above = b.get(x, y + 1, z) if b.inside(x, y + 1, z) else None
        if above is not None and not is_air(above):
            continue
        if smooth(x + y * .5, z - y * .5, seed, 2.2) * .75 + noise(x, z * 5 + y, seed) * .25 < amount:
            b.grid[(x, y, z)] = (MOSS[state[0]], state[1])


def roof(b, x0, z0, x1, z1, y, kind='dark_oak', axis='x', pitch=2, gable='spruce_planks', moss=0.28, seed=0,
         overhang=1, rake=1, finials=True):
    """Steep gable roof with moss patches; returns the ridge Y."""
    r = ROOFS[kind]
    ridge = parts.gable_roof(b, x0, z0, x1, z1, y, r, axis=axis, overhang=overhang, rake=rake, gable=gable,
                             pitch=pitch)
    ra, rb = rake if isinstance(rake, tuple) else (rake, rake)
    if moss:
        mossify(b, (x0 - ra - 1, y, z0 - overhang - 1, x1 + rb + 1, ridge + 1, z1 + overhang + 1) if axis == 'x'
                else (x0 - overhang - 1, y, z0 - ra - 1, x1 + overhang + 1, ridge + 1, z1 + rb + 1), seed, moss)
    if finials:
        # Crossed bargeboard horns over each gable.
        if axis == 'x':
            mid = (z0 + z1) / 2
            for x in (x0 - ra, x1 + rb):
                for z in {math.floor(mid), math.ceil(mid)}:
                    if b.inside(x, ridge + 1, z) and is_air(b.get(x, ridge + 1, z)):
                        b.set(x, ridge + 1, z, f'{"spruce" if kind != "spruce" else "dark_oak"}_fence')
        else:
            mid = (x0 + x1) / 2
            for z in (z0 - ra, z1 + rb):
                for x in {math.floor(mid), math.ceil(mid)}:
                    if b.inside(x, ridge + 1, z) and is_air(b.get(x, ridge + 1, z)):
                        b.set(x, ridge + 1, z, f'{"spruce" if kind != "spruce" else "dark_oak"}_fence')
    return ridge


def lean_to(b, x0, x1, z_out, z_in, y, kind='spruce', side='north', moss=0.25, seed=0):
    """Lean-to roof rows from the outer edge ``z_out`` rising toward ``z_in`` (one step per row).

    ``side`` is the direction the roof faces (its low edge); works for north/south.
    """
    r = ROOFS[kind]
    step = 1 if z_in > z_out else -1
    facing = 'south' if step > 0 else 'north'
    for i, z in enumerate(range(z_out, z_in + step, step)):
        for x in range(x0, x1 + 1):
            if b.inside(x, y + i, z):
                b.set(x, y + i, z, r.stairs, facing=facing, half='bottom')
    if moss:
        mossify(b, (x0, y, min(z_out, z_in), x1, y + abs(z_in - z_out) + 1, max(z_out, z_in)), seed, moss)


def lean_to_x(b, z0, z1, x_out, x_in, y, kind='spruce', moss=0.25, seed=0):
    """Lean-to roof whose low edge runs along Z at ``x_out``, rising toward ``x_in``."""
    r = ROOFS[kind]
    step = 1 if x_in > x_out else -1
    facing = 'east' if step > 0 else 'west'
    for i, x in enumerate(range(x_out, x_in + step, step)):
        for z in range(z0, z1 + 1):
            if b.inside(x, y + i, z):
                b.set(x, y + i, z, r.stairs, facing=facing, half='bottom')
    if moss:
        mossify(b, (min(x_out, x_in), y, z0, max(x_out, x_in), y + abs(x_in - x_out) + 1, z1), seed, moss)


def gable_glass(b, x, y, z, along='x', width=1, height=1):
    for i in range(width):
        for j in range(height):
            b.set(x + (i if along == 'x' else 0), y + j, z + (i if along == 'z' else 0), 'glass_pane')


# ---------------------------------------------------------------- outdoors
def log_post(b, x, z, y0, y1, wood='spruce', base=None):
    if base:
        b.set(x, y0 - 1, z, base)
    for y in range(y0, y1 + 1):
        b.set(x, y, z, f'{wood}_log', axis='y')


def lamp(b, x, z, y=1, height=2, base='mossy_cobblestone'):
    """Lantern on a spruce post with a mossy stone foot."""
    parts.lamp_post(b, x, y, z, height=height, fence='spruce_fence', base=base)


def arm_lamp(b, x, z, arm, y=1, height=3):
    """Log post with a short arm and a hanging lantern (rigid pieces only)."""
    b.set(x, y, z, 'mossy_cobblestone')
    for i in range(1, height + 1):
        b.set(x, y + i, z, 'spruce_log', axis='y')
    dx, dz = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}[arm]
    b.set(x + dx, y + height, z + dz, 'spruce_fence')
    hang_lantern(b, x + dx, y + height - 1, z + dz)


def totem(b, x, z, facing='south', y=1, height=7):
    """Carved spruce totem: banded wood, a carved face with trapdoor wings and a lantern crown."""
    wings = {'south': ((1, 0), (-1, 0)), 'north': ((1, 0), (-1, 0)), 'east': ((0, 1), (0, -1)),
             'west': ((0, 1), (0, -1))}[facing]
    seq = ['mossy_cobblestone', 'stripped_spruce_log', 'dark_oak_log', 'stripped_spruce_log',
           'carved_pumpkin', 'dark_oak_log', 'stripped_spruce_log', 'spruce_log']
    seq = seq[:height]
    for i, mat in enumerate(seq):
        if mat == 'carved_pumpkin':
            b.set(x, y + i, z, mat, facing=facing)
            for dx, dz in wings:
                b.set(x + dx, y + i, z + dz, 'spruce_trapdoor', facing=facing, half='top', open=True,
                      powered=False, waterlogged=False)
        elif mat.endswith('_log'):
            b.set(x, y + i, z, mat, axis='y')
        else:
            b.set(x, y + i, z, mat)
    top = y + len(seq)
    b.set(x, top, z, 'dark_oak_slab', type='bottom', waterlogged=False)
    for dx, dz in wings:
        b.set(x + dx, top - 2, z + dz, 'spruce_fence')


def drying_rack(b, x0, z, y=1, length=3, hides=('brown', 'white', 'brown')):
    """Two posts, a beam and hanging hides (wall banners under the beam)."""
    for x in (x0, x0 + length + 1):
        b.set(x, y, z, 'spruce_fence')
        b.set(x, y + 1, z, 'spruce_fence')
        b.set(x, y + 2, z, 'spruce_log', axis='y')
    for i in range(length):
        b.set(x0 + 1 + i, y + 2, z, 'stripped_spruce_log', axis='x')
        b.set(x0 + 1 + i, y + 1, z, f'{hides[i % len(hides)]}_wall_banner', facing='south')


def chopping_block(b, x, z, y=1):
    b.set(x, y, z, 'stripped_spruce_log', axis='y')
    b.set(x, y + 1, z, 'spruce_pressure_plate', powered=False)


def log_bench(b, x, z, axis='x', length=3, y=1):
    """A split-log bench: a horizontal log on two stumps (decorative seating)."""
    dx, dz = (1, 0) if axis == 'x' else (0, 1)
    for i in range(length):
        b.set(x + dx * i, y, z + dz * i, 'stripped_spruce_log', axis=axis)


def boulder(b, x, z, rng, size=1):
    cells = [(x, z)] + ([(x + 1, z), (x, z + 1)] if size > 1 else [])
    for cx, cz in cells:
        b.set(cx, 1, cz, rng.choice(['mossy_cobblestone', 'cobblestone', 'mossy_cobblestone', 'andesite']))
        if rng.random() < .5:
            b.set(cx, 2, cz, 'moss_carpet')


def woodstack(b, x, z, axis='x', length=3, height=2, y=1):
    parts.woodpile(b, x, y, z, axis, length=length, wood='spruce', height=height)


# ------------------------------------------------------------------- nature
def ground_cover(x, z, seed):
    n = smooth(x, z, seed, 3.2) * .7 + noise(x, z, seed + 1) * .3
    if n < .28:
        return 'podzol'
    if n < .34:
        return 'coarse_dirt'
    if n > .86:
        return 'moss_block'
    return 'grass_block'


def plant(b, x, z, rng, ground, rich=1.0):
    """Taiga understorey on top of ``ground``."""
    if not (b.inside(x, 2, z) and is_air(b.get(x, 1, z))):
        return
    r = rng.random() / rich
    if ground == 'podzol':
        if r < .05:
            b.set(x, 1, z, rng.choice(['brown_mushroom', 'red_mushroom']))
        elif r < .14:
            b.set(x, 1, z, 'fern')
        elif r < .2:
            b.set(x, 1, z, 'leaf_litter', facing=rng.choice(['north', 'east', 'south', 'west']),
                  segment_amount=rng.randint(1, 4))
        return
    if ground == 'moss_block':
        if r < .3:
            b.set(x, 1, z, 'moss_carpet')
        return
    if r < .08:
        b.set(x, 1, z, 'fern')
    elif r < .16:
        b.set(x, 1, z, 'short_grass')
    elif r < .19 and is_air(b.get(x, 2, z)):
        b.set(x, 1, z, 'large_fern', half='lower')
        b.set(x, 2, z, 'large_fern', half='upper')
    elif r < .215:
        b.set(x, 1, z, 'sweet_berry_bush', age=3)
    elif r < .23:
        b.set(x, 1, z, rng.choice(['lily_of_the_valley', 'cornflower'])
              if rng.random() < .4 else 'bush')


def forest_floor(b, rng, seed, lawn='grass_block', rich=1.0, skip=()):
    """Turn a plain lawn at Y=0 into podzol, moss and ferns."""
    for (x, y, z), state in list(b.grid.items()):
        if y != 0 or state[0] != 'minecraft:' + lawn or (x, z) in skip:
            continue
        g = ground_cover(x, z, seed)
        b.set(x, 0, z, g)
        plant(b, x, z, rng, g, rich)


def spruce(b, x, z, y=1, height=8, ground=True):
    """A shapely spruce with tiered branches (trunk base at ``y``)."""
    if ground:
        b.set(x, y - 1, z, 'podzol')
    for i in range(height):
        b.set(x, y + i, z, 'spruce_log', axis='y')
    top = y + height
    radius = {0: 0, 1: 1, 2: 1, 3: 2, 4: 1, 5: 2, 6: 3, 7: 2}
    for d in range(0, height - 1):
        ly = top - d
        r = radius.get(d, 3 if d % 2 == 0 else 2)
        r = min(r, 3)
        for dx in range(-r, r + 1):
            for dz in range(-r, r + 1):
                if abs(dx) + abs(dz) > r + (1 if r >= 2 else 0) or (dx == 0 and dz == 0 and d > 0):
                    continue
                px, pz = x + dx, z + dz
                if b.inside(px, ly, pz) and is_air(b.get(px, ly, pz)):
                    b.set(px, ly, pz, 'spruce_leaves', **LEAVES)
    if b.inside(x, top + 1, z):
        b.set(x, top + 1, z, 'spruce_leaves', **LEAVES)


def mega_spruce(b, cx, cz, y=1, height=22, rng=None, crown=6.2):
    """Ancient 2x2 spruce with tiered skirts, buttress roots and a spire."""
    for x in (cx, cx + 1):
        for z in (cz, cz + 1):
            for yy in range(y, y + height):
                b.set(x, yy, z, 'spruce_log', axis='y')
    # Buttress roots and a mossy root bed.
    for dx, dz, axis in ((-1, 0, 'x'), (-1, 1, 'x'), (2, 0, 'x'), (2, 1, 'x'), (0, -1, 'z'), (1, -1, 'z'),
                         (0, 2, 'z'), (1, 2, 'z')):
        if (dx + dz) % 2 == 0:
            b.set(cx + dx, y, cz + dz, 'spruce_log', axis=axis)
        else:
            b.set(cx + dx, y, cz + dz, 'spruce_wood', axis='y')
            b.set(cx + dx, y + 1, cz + dz, 'moss_carpet')
    for dx, dz in ((-2, 0), (3, 1), (1, -2), (0, 3)):
        b.set(cx + dx, y, cz + dz, 'spruce_log', axis='x' if dz in (0, 1) else 'z')
    ox, oz = cx + .5, cz + .5
    start, top = y + 7, y + height + 2
    for ly in range(start, top + 1):
        t = (ly - start) / max(1, top - start)
        r = crown * (1 - t) ** .9 + .6
        tier = (ly - start) % 3
        if tier == 2:
            r = r * .45
        elif tier == 1:
            r -= .9
        for xx in range(int(ox - r) - 1, int(ox + r) + 2):
            for zz in range(int(oz - r) - 1, int(oz + r) + 2):
                d = math.hypot(xx - ox, zz - oz)
                jitter = noise(xx, zz * 3 + ly, 77) * .9
                if d <= r - jitter + .4 and b.inside(xx, ly, zz) and is_air(b.get(xx, ly, zz)):
                    b.set(xx, ly, zz, 'spruce_leaves', **LEAVES)
    for ly in range(y + height, top + 2):
        if b.inside(cx, ly, cz) and is_air(b.get(cx, ly, cz)):
            b.set(cx, ly, cz, 'spruce_leaves', **LEAVES)
