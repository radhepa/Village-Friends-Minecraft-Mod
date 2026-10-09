"""Shared pieces for the homesteads.

A homestead is one rigid template placed on its own, far from any village, by the
``villagefriends:village`` structure type with a small terrain survey. It carries:

- one ``villagefriends:homestead_start`` jigsaw (``up_north``) at Y=1, the anchor the
  structure is placed by; its final state is the block that belongs in that spot;
- its residents, tagged ``villagefriends.dweller.<role>`` (plus ``villagefriends.gender.male``
  or ``.female`` where it matters), which the mod reads when they first load (HOMESTEADS.md).

Y=0 is ground level. Cells left undrawn on Y=0 keep the world's own ground.
"""
from ... import parts
from ...kit import DIRS

ROLES = ('homesteader', 'pariah', 'shepherd', 'herbalist', 'veteran')


def start(b, x, z, final):
    """The anchor the homestead is placed by: a jigsaw at Y=1 that becomes ``final``."""
    b.jigsaw(x, 1, z, 'up_north', 'homestead_start', final=final if ':' in final else 'minecraft:' + final)


def dweller(b, x, y, z, role, job='none', gender=None):
    assert role in ROLES, role
    tags = [f'villagefriends.dweller.{role}']
    if gender:
        tags.append(f'villagefriends.gender.{gender}')
    b.resident(x, y, z, job, tags=tags)


def path(b, cells, rng, mats=('dirt_path', 'dirt_path', 'dirt_path', 'coarse_dirt', 'gravel')):
    for x, z in cells:
        b.set(x, 0, z, rng.choice(mats))


def line(x0, z0, x1, z1):
    """Cells on an L-shaped walk: along X first, then along Z."""
    cells = [(x, z0) for x in range(min(x0, x1), max(x0, x1) + 1)]
    cells += [(x1, z) for z in range(min(z0, z1), max(z0, z1) + 1)]
    return cells


def gate(b, x, y, z, facing, wood='spruce'):
    b.set(x, y, z, f'{wood}_fence_gate', facing=facing, open=False, in_wall=False, powered=False)


def fence_ring(b, x0, z0, x1, z1, y=1, wood='spruce', gates=(), gaps=(), posts=None):
    """A fence round a rectangle. ``gates`` are (x, z, facing); ``gaps`` stay open (a sagging, broken fence)."""
    gate_at = {(gx, gz): f for gx, gz, f in gates}
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        if (x, z) in gaps:
            continue
        if (x, z) in gate_at:
            gate(b, x, y, z, gate_at[(x, z)], wood)
        else:
            b.set(x, y, z, posts if (posts and corner) else f'{wood}_fence')


def well(b, cx, cz, roof='spruce'):
    """A small stone well: a ring of cobblestone round water, two posts and a little slab roof with a bucket chain."""
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            b.set(cx + dx, 0, cz + dz, 'cobblestone')
            if dx or dz:
                b.set(cx + dx, 1, cz + dz, 'mossy_cobblestone' if (dx + dz) % 2 else 'cobblestone')
    b.set(cx, 0, cz, 'water', level=0)
    b.set(cx, 1, cz, 'water', level=0)
    for dx in (-1, 1):
        b.set(cx + dx, 2, cz, f'{roof}_fence')
        b.set(cx + dx, 3, cz, f'{roof}_fence')
    for dx in (-1, 0, 1):
        for dz, f in ((-1, 'south'), (1, 'north')):
            b.set(cx + dx, 4, cz + dz, f'{roof}_stairs', facing=f, half='bottom')
        b.set(cx + dx, 4, cz, f'{roof}_planks' if dx else f'{roof}_slab', **({} if dx else {'type': 'top'}))
    b.set(cx, 3, cz, 'chain', axis='y', waterlogged=False)


def hay_pile(b, cells):
    for x, y, z in cells:
        b.set(x, y, z, 'hay_block', axis='y' if y % 2 else 'x')


def tufts(b, rng, x0, z0, x1, z1, chance=.12, y=1):
    """Grass and the odd flower on open ground so the yard doesn't look swept."""
    cells = [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)
             if (x, 0, z) not in b.grid or b.get(x, 0, z)[0] == 'minecraft:structure_void']
    parts.grass_tufts(b, cells, y, rng, chance)


def mossy_carpet(b, rng, cells, y, chance=.35):
    for x, z in cells:
        if rng.random() < chance and b.inside(x, y, z) and b.get(x, y, z)[0] == 'minecraft:air':
            b.set(x, y, z, 'moss_carpet')


def lantern_post(b, x, z, height=2, fence='spruce_fence', y=1):
    parts.lamp_post(b, x, y, z, height=height, fence=fence)


def side(direction):
    return DIRS[direction]
