"""Street kit: terrain-matching road pieces, junctions and street ends.

Every piece enters from the north through ``street_in`` at Y=1. Streets offer
``lot`` jigsaws on their outer edges so houses, workshops, farms and small
decorations attach outside the road's bounding box. Left/right variants are
mirror images.

The kit is drawn for a ``roads.Theme``: ``kit(theme)`` returns every street of
one village type, named with the theme's prefix. Plains uses ``roads.PLAINS``.
Decor on terrain-matching pieces stays one column wide (lamp posts, bushes,
benches); the square and the gatehouse are rigid pieces in the layout.
"""
import math

from ..kit import Build
from ..roads import Street, PLAINS
from .. import parts


def _roof(wood):
    return parts.ROOFS.get(wood) or parts.Roof(f'{wood}_stairs', f'{wood}_slab', f'{wood}_planks')


def avenue(t=PLAINS):
    """First street out of the plaza: runs between two civic buildings, then opens up."""
    s = Street(t.name('avenue'), 5, 26, seed=101, theme=t)
    s.rect(1, 0, 3, 25)
    s.ragged([(x, z) for x in (0, 4) for z in range(26)], 0.75)
    s.street_in(2)
    s.street_out(2, 25, 'south')
    for z in range(8, 24, 4):
        s.lot(0, z, 'west')
        s.lot(4, z + 2, 'east')
    s.lamp(0, 2)
    s.lamp(4, 2)
    s.lamp(4, 13)
    return s.paint()


def avenue_bend(t=PLAINS):
    s = Street(t.name('avenue_bend'), 8, 26, seed=102, theme=t)
    s.rect(1, 0, 3, 13)
    for z in range(13, 19):
        off = round((z - 13) * 3 / 5)
        s.rect(1 + off, z, 3 + off, z)
    s.rect(4, 19, 6, 25)
    s.ragged([(x, z) for x in range(8) for z in range(26)], 0.18)
    s.street_in(2)
    s.street_out(5, 25, 'south')
    for z in (8, 11, 14):
        s.lot(0, z, 'west')
    for z in (19, 22):
        s.lot(0, z, 'west')
    for z in (8, 11, 14, 17, 20, 23):
        s.lot(7, z, 'east')
    s.lamp(0, 2)
    s.lamp(4, 2)
    b = s.paint()
    s.planter(6, 3)
    s.planter(6, 4, alt=True)
    return b


def straight_short(t=PLAINS):
    s = Street(t.name('street_straight_short'), 5, 10, seed=103, theme=t)
    s.rect(1, 0, 3, 9)
    s.ragged([(x, z) for x in (0, 4) for z in range(10)], 0.7)
    s.street_in(2)
    s.street_out(2, 9, 'south')
    for z in (2, 6):
        s.lot(0, z + 1, 'west')
        s.lot(4, z, 'east')
    return s.paint()


def straight_long(t=PLAINS, name='street_straight_long', lamp=False, seed=104):
    s = Street(t.name(name), 5, 17, seed=seed, theme=t)
    s.rect(1, 0, 3, 16)
    s.ragged([(x, z) for x in (0, 4) for z in range(17)], 0.7)
    s.street_in(2)
    s.street_out(2, 16, 'south')
    for z in range(2, 16, 4):
        s.lot(0, z + 1, 'west')
        if not (lamp and z == 6):
            s.lot(4, z, 'east')
    if lamp:
        s.lamp(4, 8)
    return s.paint()


def straight_lamp(t=PLAINS):
    return straight_long(t, 'street_straight_lamp', lamp=True, seed=105)


def bend_right(t=PLAINS):
    """Gentle S-bend that shifts the road three blocks east."""
    s = Street(t.name('street_bend_right'), 8, 14, seed=106, theme=t)
    s.rect(1, 0, 3, 4)
    for z in range(5, 9):
        off = round((z - 4) * 3 / 5)
        s.rect(1 + off, z, 3 + off, z)
    s.rect(4, 9, 6, 13)
    s.ragged([(x, z) for x in range(8) for z in range(14)], 0.2)
    s.street_in(2)
    s.street_out(5, 13, 'south')
    for z in (3, 6, 9, 12):
        s.lot(0, z, 'west')
    for z in (1, 4, 7, 10):
        s.lot(7, z, 'east')
    b = s.paint()
    s.planter(6, 1)
    return b


def bend_left(t=PLAINS):
    return bend_right(t).mirrored(t.name('street_bend_left'))


def turn_right(t=PLAINS):
    """Quarter-circle turn toward the east (seen from the incoming road)."""
    s = Street(t.name('street_turn_right'), 10, 10, seed=107, theme=t)
    cx, cz = 9.5, -0.5
    cells = []
    for x in range(10):
        for z in range(10):
            r = math.hypot(x - cx, z - cz)
            if 5.6 <= r <= 8.6:
                cells.append((x, z))
    s.road(cells, lambda x, z: 1 - abs(math.hypot(x - cx, z - cz) - 7.1) / 1.5)
    s.rect(1, 0, 3, 1)
    s.rect(8, 6, 9, 8, axis='x')
    ring = [(x, z) for x in range(10) for z in range(10) if 4.6 <= math.hypot(x - cx, z - cz) <= 9.6]
    s.ragged(ring, 0.55)
    s.street_in(2)
    s.street_out(9, 7, 'east')
    s.lot(0, 5, 'west')
    s.lot(3, 9, 'south')
    s.lot(6, 9, 'south')
    s.lot(9, 1, 'east')
    b = s.paint()
    b.set(7, 0, 1, t.planter)
    s.lamp(6, 2)
    s.planter(8, 2, alt=True)
    b.set(7, 1, 1, 'short_grass' if t.planter == 'grass_block' else 'air')
    return b


def turn_left(t=PLAINS):
    return turn_right(t).mirrored(t.name('street_turn_left'))


def tee_right(t=PLAINS):
    """Straight street with a branch to the east."""
    s = Street(t.name('street_tee_right'), 10, 13, seed=108, theme=t)
    s.rect(1, 0, 3, 12)
    s.rect(4, 5, 9, 7, axis='x')
    s.disc(3, 6, 2.2)
    s.ragged([(0, z) for z in range(13)] + [(4, z) for z in range(13)] +
             [(x, z) for x in range(4, 10) for z in (4, 8)], 0.65)
    s.street_in(2)
    s.street_out(2, 12, 'south')
    s.street_out(9, 6, 'east')
    for z in (2, 6, 10):
        s.lot(0, z, 'west')
    s.lot(9, 2, 'east')
    s.lot(9, 10, 'east')
    s.lot(7, 12, 'south')
    b = s.paint()
    s.lamp(4, 3)
    return b


def tee_left(t=PLAINS):
    return tee_right(t).mirrored(t.name('street_tee_left'))


def fork(t=PLAINS):
    """The road splits east and west."""
    s = Street(t.name('street_fork'), 15, 8, seed=109, theme=t)
    s.rect(6, 0, 8, 3)
    s.rect(0, 3, 14, 5, axis='x')
    s.disc(7, 4, 2.4)
    s.ragged([(x, z) for x in range(15) for z in (2, 6)] + [(5, z) for z in range(3)] + [(9, z) for z in range(3)], 0.6)
    s.street_in(7)
    s.street_out(0, 4, 'west')
    s.street_out(14, 4, 'east')
    for x in (2, 6, 10):
        s.lot(x + 1, 7, 'south')
    s.lot(1, 0, 'north')
    s.lot(13, 0, 'north')
    b = s.paint()
    s.lamp(7, 7)
    s.planter(10, 1)
    return b


def crossroads(t=PLAINS):
    s = Street(t.name('street_crossroads'), 13, 13, seed=110, theme=t)
    s.rect(5, 0, 7, 12)
    s.rect(0, 5, 12, 7, axis='x')
    s.disc(6, 6, 3.1)
    s.ragged([(x, z) for x in range(13) for z in range(13) if 4 <= x <= 8 or 4 <= z <= 8], 0.45)
    s.street_in(6)
    s.street_out(0, 6, 'west')
    s.street_out(12, 6, 'east')
    s.street_out(6, 12, 'south')
    for a in (1, 3):
        s.lot(a, 0, 'north')
        s.lot(12 - a, 12, 'south')
        s.lot(0, 12 - a, 'west')
        s.lot(12, a, 'east')
    b = s.paint()
    for x, z in ((3, 3), (9, 9)):
        s.lamp(x, z)
    return b


def well(b, t, cx, cz):
    """Covered well on a 3x3 curb (for rigid pieces only)."""
    for x in range(cx - 1, cx + 2):
        for z in range(cz - 1, cz + 2):
            b.set(x, 0, z, t.stone)
            if (x, z) == (cx, cz):
                b.set(x, 1, z, 'water', level=0)
            elif abs(x - cx) == 1 and abs(z - cz) == 1:
                b.set(x, 1, z, t.stone)
                b.set(x, 2, z, f'{t.wood}_fence')
                b.set(x, 3, z, f'{t.wood}_fence')
            else:
                b.set(x, 1, z, f'mossy_{t.stone}' if t.stone == 'cobblestone' and (x + z) % 3 == 0 else f'{t.stone}_wall')
    parts.gable_roof(b, cx - 1, cz - 1, cx + 1, cz + 1, 3, _roof(t.wood), axis='x')
    b.set(cx, 4, cz, 'chain', axis='y')
    b.set(cx, 3, cz, 'lantern', hanging=True)


def square(t=PLAINS):
    """A small neighbourhood square with a covered well (a rigid piece)."""
    s = Street(t.name('street_square'), 15, 15, h=8, seed=111, theme=t)
    s.rect(6, 0, 8, 14)
    s.rect(0, 6, 14, 8, axis='x')
    s.disc(7, 7, 5.3)
    s.ragged([(x, z) for x in range(15) for z in range(15) if math.hypot(x - 7, z - 7) <= 6.6], 0.6)
    s.street_in(7)
    s.street_out(0, 7, 'west')
    s.street_out(14, 7, 'east')
    s.street_out(7, 14, 'south')
    for a in (1, 3):
        s.lot(a, 0, 'north')
        s.lot(14 - a, 14, 'south')
        s.lot(0, 14 - a, 'west')
        s.lot(14, a, 'east')
    b = s.paint()
    well(b, t, 7, 7)
    for x, z, f in ((3, 3, 'east'), (11, 11, 'west')):
        s.bench(x, z, f)
    for x, z in ((2, 11), (12, 3)):
        s.planter(x, z, alt=True)
    return b


# ------------------------------------------------------------------ street ends
def end_fade(t=PLAINS):
    s = Street(t.name('end_fade'), 5, 5, seed=112, theme=t)
    s.rect(1, 0, 3, 1)
    s.rect(2, 2, 3, 2)
    s.ragged([(x, z) for x in range(5) for z in range(5)], 0.35)
    s.street_in(2)
    return s.paint()


def end_lamp(t=PLAINS):
    s = Street(t.name('end_lamp'), 7, 5, seed=113, theme=t)
    s.rect(2, 0, 4, 3)
    s.ragged([(x, z) for x in range(7) for z in range(5)], 0.4)
    s.street_in(3)
    b = s.paint()
    s.lamp(3, 4)
    s.bench(2, 3, 'north')
    s.bench(4, 3, 'north')
    s.planter(1, 4, alt=True)
    s.planter(5, 4)
    return b


def end_gate(t=PLAINS):
    """Timber gatehouse with palisade wings where a street leaves the village (a rigid piece)."""
    b = Build(t.name('end_gate'), (17, 12, 7), kind='street', background='structure_void')
    s = Street(t.name('end_gate'), 17, 7, h=12, seed=114, theme=t)
    s.b = b
    s.rect(6, 0, 10, 6)
    s.ragged([(x, z) for x in (5, 11) for z in range(7)], 0.6)
    s.street_in(8)
    s.paint()
    log, stripped = f'{t.wood}_log', f'stripped_{t.wood}_log'
    # Palisade wings: sharpened logs on a stone footing.
    for x in list(range(0, 3)) + list(range(14, 17)):
        b.set(x, 0, 3, t.stone)
        h = 4 if x % 2 else 5
        for y in range(1, h + 1):
            b.set(x, y, 3, log, axis='y')
        b.set(x, h + 1, 3, f'{t.wood}_fence')
    # Two timber towers on stone bases, each capped with a little pyramid roof.
    for x0 in (3, 11):
        for x in range(x0, x0 + 3):
            for z in range(2, 5):
                corner = x in (x0, x0 + 2) and z in (2, 4)
                for y in range(0, 7):
                    if y <= 1:
                        b.set(x, y, z, t.stone)
                    elif corner:
                        b.set(x, y, z, stripped, axis='y')
                    elif y == 6:
                        b.set(x, y, z, stripped, axis='x' if z != 3 else 'z')
                    else:
                        b.set(x, y, z, f'{t.wood}_planks' if (x, z) != (x0 + 1, 3) else 'air')
        for z in (2, 4):
            b.set(x0 + 1, 4, z, 'glass_pane')
        parts.pyramid_roof(b, x0 - 1, 1, x0 + 3, 5, 7, _roof(t.wood).stairs, f'{t.wood}_planks', pitch=1,
                           finial=[f'{t.wood}_fence'])
        for z, f in ((1, 'north'), (5, 'south')):
            b.set(x0 + 1, 5, z, 'red_wall_banner', facing=f)
    # Lintel beam and a small roof over the passage, with a lantern.
    for x in range(6, 11):
        b.set(x, 6, 3, stripped, axis='x')
    parts.gable_roof(b, 6, 3, 10, 3, 6, _roof(t.wood), axis='x', overhang=1, rake=0)
    b.set(8, 5, 3, 'chain', axis='y')
    b.set(8, 4, 3, 'lantern', hanging=True)
    for x, z in ((5, 1), (11, 1), (5, 5), (11, 5)):
        b.set(x, 0, z, t.stone)
        b.set(x, 1, z, f'{t.wood}_fence')
        b.set(x, 2, z, 'lantern')
    return b


def kit(t):
    """Every street piece for theme ``t``, as ``{name: design}``."""
    pieces = [avenue, avenue_bend, straight_short, straight_long, straight_lamp, bend_right, bend_left, turn_right,
              turn_left, tee_right, tee_left, fork, crossroads, square, end_fade, end_lamp, end_gate]
    names = ['avenue', 'avenue_bend', 'street_straight_short', 'street_straight_long', 'street_straight_lamp',
             'street_bend_right', 'street_bend_left', 'street_turn_right', 'street_turn_left', 'street_tee_right',
             'street_tee_left', 'street_fork', 'street_crossroads', 'street_square', 'end_fade', 'end_lamp', 'end_gate']
    return {t.name(n): (lambda f=f: f(t)) for n, f in zip(names, pieces)}


DESIGNS = kit(PLAINS)
