"""Drawing helpers shared by the snowy homes, workshops, farms and decorations.

Only draws into a ``Build``; holds no designs of its own. Materials come from
``palette.py`` (read-only), so every frost-hamlet building shares one look:
spruce logs and planks on cobblestone, steep roofs loaded with snow, stone
chimneys with smoke, small windows, warm lantern light and woodpiles.
"""
import math

from ...kit import DIRS, CLOCKWISE, OPPOSITE, is_air, bid, props, block
from ... import parts
from .palette import ROOFS, LOOT

ROOF_PARTS = {}
for _roof in ROOFS.values():
    for _name in (_roof.stairs, _roof.slab, _roof.full):
        ROOF_PARTS[_name] = _roof

PATH = ('dirt_path', 'dirt_path', 'dirt_path', 'gravel', 'coarse_dirt')


def leaf(b, x, y, z, kind='spruce_leaves', clip=True):
    if b.inside(x, y, z) and is_air(b.get(x, y, z)):
        b.set(x, y, z, kind, persistent=True, distance=1, waterlogged=False)


def snow(b, x, y, z, layers=1):
    """A snow layer on top of whatever is below (only into air)."""
    if b.inside(x, y, z) and is_air(b.get(x, y, z)):
        b.set(x, y, z, 'snow', layers=layers)


def chain(b, x, y, z):
    b.set(x, y, z, 'iron_chain', axis='y', waterlogged=False)


def hang(b, x, y, z, links=0):
    """Hanging lantern at ``y`` below ``links`` chain links (26.3 calls the chain ``iron_chain``)."""
    for i in range(links):
        chain(b, x, y + links - i, z)
    b.set(x, y, z, 'lantern', hanging=True, waterlogged=False)


def stand_lantern(b, x, y, z):
    b.set(x, y, z, 'lantern', hanging=False, waterlogged=False)


def path(b, cells, rng, y=0, mix=PATH):
    for x, z in cells:
        b.set(x, y, z, rng.choice(mix))


def path_line(b, x, z0, z1, rng, y=0, mix=PATH):
    path(b, [(x, z) for z in range(min(z0, z1), max(z0, z1) + 1)], rng, y, mix)


def snow_roof(b, x0, z0, x1, z1, rng, ymin, eave_y=None, cover=0.85, depth=(1, 2, 2, 3)):
    """Load a finished roof with snow.

    Stairs and slabs only hold snow in the world when their top face is full,
    so each snowed roof cell becomes the roof's full block with a snow layer on
    top; eaves at ``eave_y`` and uncovered cells keep their stair profile.
    """
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            top = None
            for y in range(b.h - 2, ymin - 1, -1):
                if not is_air(b.get(x, y, z)):
                    top = y
                    break
            if top is None:
                continue
            s = b.get(x, top, z)
            roof = ROOF_PARTS.get(bid(s))
            if roof is None or rng.random() > cover:
                continue
            p = props(s)
            if bid(s) == roof.stairs:
                if p.get('half') == 'top' or (eave_y is not None and top <= eave_y):
                    continue
            elif bid(s) == roof.slab and p.get('type') == 'top':
                pass
            b.set(x, top, z, roof.full)
            snow(b, x, top + 1, z, rng.choice(depth))


def log_walls(b, x0, z0, x1, z1, y0, y1, wood='spruce', notch=True):
    """Horizontal log walls with saddle-notched corners that cross and stick out."""
    for y in range(y0, y1 + 1):
        odd = (y - y0) % 2
        for x in range(x0, x1 + 1):
            for z in (z0, z1):
                b.set(x, y, z, f'{wood}_log', axis='x')
        for z in range(z0 + 1, z1):
            for x in (x0, x1):
                b.set(x, y, z, f'{wood}_log', axis='z')
        for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
            b.set(x, y, z, f'{wood}_log', axis='z' if odd else 'x')
        if notch:
            for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
                if odd:
                    oz = z - 1 if z == z0 else z + 1
                    if b.inside(x, y, oz) and is_air(b.get(x, y, oz)):
                        b.set(x, y, oz, f'{wood}_log', axis='z')
                else:
                    ox = x - 1 if x == x0 else x + 1
                    if b.inside(ox, y, z) and is_air(b.get(ox, y, z)):
                        b.set(ox, y, z, f'{wood}_log', axis='x')


def fireplace(b, x, z, out, fy, top, mantel=True, breast='cobblestone', stack='stone_bricks', smoke=True):
    """Hearth set into the wall cell (x, z) of a wall facing ``out``.

    ``fy`` is the floor block's Y. A three-wide stone breast stands outside the
    wall and a chimney rises from it to ``top``, capped with a smoking campfire.
    Inside there is a lit campfire in the firebox, a stone hearth and a mantel.
    """
    dx, dz = DIRS[out]
    lx, lz = DIRS[CLOCKWISE[out]]
    for i in (-1, 0, 1):
        wx, wz = x + lx * i, z + lz * i
        for y in range(fy + 1, fy + 4):
            b.set(wx, y, wz, 'stone_bricks' if i or y > fy + 1 else 'cobblestone')
        for y in range(0, fy + 4):
            b.set(wx + dx, y, wz + dz, breast)
    b.set(x, fy + 1, z, 'campfire', lit=True, signal_fire=False, facing=OPPOSITE[out], waterlogged=False)
    b.set(x, fy + 2, z, 'chiseled_stone_bricks')
    for i in (-1, 1):
        b.set(x + dx + lx * i, fy + 4, z + dz + lz * i, 'stone_brick_stairs', facing=OPPOSITE[CLOCKWISE[out]] if i > 0
              else CLOCKWISE[out], half='bottom')
    for y in range(fy + 4, top + 1):
        b.set(x + dx, y, z + dz, stack)
    if smoke:
        b.set(x + dx, top + 1, z + dz, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    # Hearthstone and mantel inside.
    b.set(x - dx, fy, z - dz, 'stone_bricks')
    if mantel:
        b.set(x - dx, fy + 3, z - dz, 'stone_brick_slab', type='top', waterlogged=False)


def stove_chimney(b, x, z, y0, top, mat='cobblestone', cap='stone_bricks'):
    """Free chimney column (e.g. through a roof) with a smoking campfire."""
    for y in range(y0, top + 1):
        b.set(x, y, z, mat if y < top - 1 else cap)
    b.set(x, top + 1, z, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)


def vestibule(b, x, z, fy, wood='spruce', walls='spruce_planks', frame='stripped_spruce_log', roof=None,
              step='cobblestone_stairs', base='cobblestone'):
    """Enclosed cold porch in front of a north door at (x, fy+1, z).

    Outer door at z-2, a one-block airlock at z-1. Returns the outer door's Z.
    """
    zo = z - 2
    for zz in (zo, z - 1):
        for xx in (x - 1, x, x + 1):
            b.set(xx, fy, zz, base if xx != x else f'{wood}_planks')
        for y in range(1, fy):
            for xx in (x - 1, x, x + 1):
                b.set(xx, y, zz, base)
        for y in range(fy + 1, fy + 4):
            for xx in (x - 1, x + 1):
                b.set(xx, y, zz, frame if zz == zo else walls, **({'axis': 'y'} if zz == zo else {}))
        for xx in (x - 1, x + 1):
            b.set(xx, fy + 4, zz, frame, axis='z')
    for y in (fy + 1, fy + 2):
        b.set(x, y, z - 1, 'air')
    b.set(x, fy + 3, zo, frame, axis='x')
    b.set(x, fy + 4, zo, frame, axis='x')
    b.set(x, fy + 3, z - 1, walls)
    b.set(x, fy + 4, z - 1, walls)
    b.door(x, fy + 1, zo, facing='south', wood=wood, hinge='right')
    b.door(x, fy + 1, z, facing='south', wood=wood, hinge='left')
    if step:
        b.set(x, fy, zo - 1, step, facing='south', half='bottom', lock=True)
    # Window slit on each side of the airlock and a lamp by the outer door.
    b.set(x - 1, fy + 2, z - 1, 'glass_pane')
    b.set(x + 1, fy + 2, z - 1, 'glass_pane')
    if roof:
        parts.gable_roof(b, x - 1, zo, x + 1, z - 1, fy + 4, roof, axis='z', overhang=1, rake=(1, 0),
                         gable=walls)
    return zo


def window(b, x, y, z, out, height=1, width=1, trim='spruce', shutters=True, pane='glass_pane'):
    parts.window(b, x, y, z, out, height=height, width=width, trim=trim, shutters=shutters, pane=pane)


def kitchen(b, rng, cells, y, facing='east', loot=False):
    """Cooking corner: smoker, barrel, crafting table, furnace, cauldron of water."""
    items = ['smoker', 'barrel', 'crafting_table', 'furnace', 'water_cauldron', 'barrel']
    for (x, z), item in zip(cells, items):
        if item in ('smoker', 'furnace'):
            b.set(x, y, z, item, facing=facing, lit=item == 'smoker')
        elif item == 'barrel':
            b.barrel(x, y, z, 'up', loot=LOOT if loot else None)
        elif item == 'water_cauldron':
            b.set(x, y, z, 'water_cauldron', level=3)
        else:
            b.set(x, y, z, item)


def fur_rug(b, x0, z0, x1, z1, y, inner='white', border='brown'):
    parts.rug(b, x0, z0, x1, z1, y, inner, border)


def woodpile(b, x, y, z, along='x', length=3, height=2, wood='spruce'):
    """Split firewood stacked crosswise, tapering at the ends."""
    parts.woodpile(b, x, y, z, along_axis=along, length=length, wood=wood, height=height)


def chopping_block(b, x, y, z):
    b.set(x, y, z, 'stripped_spruce_log', axis='y')
    b.set(x, y + 1, z, 'spruce_pressure_plate', powered=False)


def spruce(b, x, y, z, rng, height=8, radius=3, sparse=0.0, snowy=True):
    """Tall, layered spruce with drooping tiers, persistent leaves and snow on the tiers."""
    for i in range(height):
        b.set(x, y + i, z, 'spruce_log', axis='y', clip=True)
    top = y + height
    n = height - 1
    zigzag = [0, 1, 1, 2, 1, 2, 3, 2, 3, 4, 3, 4]
    tiers = [(top - i, min(radius, zigzag[min(i, len(zigzag) - 1)])) for i in range(n)]
    for ty, tr in tiers:
        for dx in range(-tr, tr + 1):
            for dz in range(-tr, tr + 1):
                d = math.hypot(dx, dz)
                if d > tr + (0.25 if tr < 2 else 0.3) or (tr > 1 and d > tr - 0.4 and rng.random() < sparse):
                    continue
                leaf(b, x + dx, ty, z + dz)
    leaf(b, x, top + 1, z)
    if snowy:
        dust_tree(b, x, z, radius, rng, y)


def dust_tree(b, cx, cz, radius, rng, ymin, chance=0.55):
    """Snow layers on exposed leaves (leaves hold snow in the world)."""
    for x in range(cx - radius - 1, cx + radius + 2):
        for z in range(cz - radius - 1, cz + radius + 2):
            for y in range(b.h - 2, ymin, -1):
                s = b.get(x, y, z) if b.inside(x, y, z) else None
                if s is None or is_air(s):
                    continue
                if bid(s).endswith('_leaves') and rng.random() < chance:
                    snow(b, x, y + 1, z, 1 if rng.random() < .7 else 2)
                break


def plaque(b, x, z, facing='north'):
    b.custom(x, 1, z, 'house_plaque', facing=facing)


def fence_run(b, cells, y=1, fence='spruce_fence'):
    for x, z in cells:
        b.set(x, y, z, fence)


def gate(b, x, y, z, facing='north', wood='spruce'):
    b.set(x, y, z, f'{wood}_fence_gate', facing=facing, open=False, in_wall=False, powered=False)


def seal_gable(b, z, y0, y1, x0, x1, mat, axis_x=True):
    """Fill the air inside a roof cross-section (between the two slopes) at ``z``.

    With ``axis_x`` False, ``z`` is an X and the section runs along Z instead.
    """
    for y in range(y0, y1 + 1):
        cells = [(xx, z) if axis_x else (z, xx) for xx in range(x0, x1 + 1)]
        solid = [i for i, (cx, cz) in enumerate(cells) if not is_air(b.get(cx, y, cz))]
        if len(solid) < 2:
            continue
        for i in range(solid[0] + 1, solid[-1]):
            cx, cz = cells[i]
            if is_air(b.get(cx, y, cz)):
                b.set(cx, y, cz, mat)


def lamp_post(b, x, y, z, height=3, fence='spruce_fence', base='cobblestone'):
    parts.lamp_post(b, x, y, z, height=height, fence=fence, top='lantern', base=base)


def sled(b, x, y, z, along='z', load=True):
    """Small cargo sledge: slab bed on trapdoor runners with a curled front."""
    ax, az = (0, 1) if along == 'z' else (1, 0)
    for i in range(3):
        cx, cz = x + ax * i, z + az * i
        b.set(cx, y, cz, 'spruce_slab', type='top', waterlogged=False)
    front = (x - ax, z - az)
    b.set(front[0], y, front[1], 'spruce_trapdoor', facing='north' if along == 'z' else 'west', half='bottom',
          open=True, powered=False, waterlogged=False)
    if load:
        b.set(x + ax, y + 1, z + az, 'barrel', facing='up', open=False)
        b.set(x + 2 * ax, y + 1, z + 2 * az, 'spruce_log', axis='x' if along == 'z' else 'z')


def room_lamp(b, x, ceiling_y, z):
    """Hanging lantern under a ceiling block at ``ceiling_y``."""
    b.set(x, ceiling_y - 1, z, 'lantern', hanging=True, waterlogged=False)


def bed_pair(b, x, y, z, facing, color, step):
    """Two matching beds side by side, ``step`` = (dx, dz) between them."""
    b.bed(x, y, z, facing, color)
    b.bed(x + step[0], y, z + step[1], facing, color)


def facing_of(state):
    return props(state).get('facing')


def blk(spec, **kw):
    return block(spec, **kw)
