"""Plains street kit: terrain-matching road pieces, junctions and street ends.

Every piece enters from the north through ``street_in`` at Y=1. Streets offer
``lot`` jigsaws on their outer edges so houses, workshops, farms and small
decorations attach outside the road's bounding box. Left/right variants are
mirror images.
"""
import math

from ..kit import Build, DIRS
from ..roads import Street
from .. import parts


def avenue():
    """First street out of the plaza: runs between two civic buildings, then opens up."""
    s = Street('avenue', 5, 26, seed=101)
    s.rect(1, 0, 3, 25)
    s.ragged([(x, z) for x in (0, 4) for z in range(26)], 0.75)
    s.street_in(2)
    s.street_out(2, 25, 'south')
    for z in range(8, 24, 4):
        s.lot(0, z, 'west')
        s.lot(4, z + 2, 'east')
    s.lamp(0, 2)
    s.lamp(4, 2)
    s.lamp(4, 13, arm='west')
    return s.paint()


def avenue_bend():
    s = Street('avenue_bend', 8, 26, seed=102)
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
    parts.bush(b, 6, 1, 3)
    parts.bush(b, 6, 1, 4, 'flowering_azalea_leaves')
    b.set(6, 0, 3, 'grass_block')
    b.set(6, 0, 4, 'grass_block')
    return b


def straight_short():
    s = Street('street_straight_short', 5, 10, seed=103)
    s.rect(1, 0, 3, 9)
    s.ragged([(x, z) for x in (0, 4) for z in range(10)], 0.7)
    s.street_in(2)
    s.street_out(2, 9, 'south')
    for z in (2, 6):
        s.lot(0, z + 1, 'west')
        s.lot(4, z, 'east')
    return s.paint()


def straight_long(name='street_straight_long', lamp=False, seed=104):
    s = Street(name, 5, 17, seed=seed)
    s.rect(1, 0, 3, 16)
    s.ragged([(x, z) for x in (0, 4) for z in range(17)], 0.7)
    s.street_in(2)
    s.street_out(2, 16, 'south')
    for z in range(2, 16, 4):
        s.lot(0, z + 1, 'west')
        if not (lamp and z == 6):
            s.lot(4, z, 'east')
    if lamp:
        s.lamp(4, 8, arm='west')
    return s.paint()


def straight_lamp():
    return straight_long('street_straight_lamp', lamp=True, seed=105)


def bend_right():
    """Gentle S-bend that shifts the road three blocks east."""
    s = Street('street_bend_right', 8, 14, seed=106)
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
    b.set(6, 0, 1, 'grass_block')
    parts.bush(b, 6, 1, 1)
    return b


def bend_left():
    return bend_right().mirrored('street_bend_left')


def turn_right():
    """Quarter-circle turn toward the east (seen from the incoming road)."""
    s = Street('street_turn_right', 10, 10, seed=107)
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
    for x, z in ((7, 1), (8, 2)):
        b.set(x, 0, z, 'grass_block')
    parts.lamp_post(b, 6, 1, 2, height=3)
    b.set(6, 0, 2, 'cobblestone')
    parts.bush(b, 8, 1, 2, 'flowering_azalea_leaves')
    b.set(7, 1, 1, 'short_grass')
    return b


def turn_left():
    return turn_right().mirrored('street_turn_left')


def tee_right():
    """Straight street with a branch to the east."""
    s = Street('street_tee_right', 10, 13, seed=108)
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
    parts.lamp_post(b, 4, 1, 3, height=3)
    b.set(4, 0, 3, 'cobblestone')
    return b


def tee_left():
    return tee_right().mirrored('street_tee_left')


def fork():
    """The road splits east and west."""
    s = Street('street_fork', 15, 8, seed=109)
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
    b.set(7, 0, 7, 'cobblestone')
    parts.lamp_post(b, 7, 1, 7, height=3)
    b.set(10, 0, 1, 'grass_block')
    parts.bush(b, 10, 1, 1)
    return b


def crossroads():
    s = Street('street_crossroads', 13, 13, seed=110)
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
        b.set(x, 0, z, 'cobblestone')
        parts.lamp_post(b, x, 1, z, height=3)
    return b


def square():
    """A small neighbourhood square with a covered well."""
    s = Street('street_square', 15, 15, h=8, seed=111)
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
    # Well: cobble ring, water, spruce roof on posts.
    for x in range(6, 9):
        for z in range(6, 9):
            b.set(x, 0, z, 'cobblestone')
            if (x, z) == (7, 7):
                b.set(x, 1, z, 'water', level=0)
                b.set(x, 0, z, 'cobblestone')
            else:
                b.set(x, 1, z, 'mossy_cobblestone' if (x + z) % 3 == 0 else 'cobblestone_wall')
    for x, z in ((6, 6), (8, 6), (6, 8), (8, 8)):
        b.set(x, 1, z, 'cobblestone')
        b.set(x, 2, z, 'spruce_fence')
        b.set(x, 3, z, 'spruce_fence')
    parts.gable_roof(b, 6, 6, 8, 8, 3, parts.ROOFS['spruce'], axis='x')
    b.set(7, 4, 7, 'chain', axis='y')
    b.set(7, 3, 7, 'lantern', hanging=True)
    for x, z, f in ((3, 3, 'east'), (11, 11, 'west')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    for x, z in ((2, 11), (12, 3)):
        b.set(x, 0, z, 'grass_block')
        parts.bush(b, x, 1, z, 'flowering_azalea_leaves')
    return b


# ------------------------------------------------------------------ street ends
def end_fade():
    s = Street('end_fade', 5, 5, seed=112)
    s.rect(1, 0, 3, 1)
    s.rect(2, 2, 3, 2)
    s.ragged([(x, z) for x in range(5) for z in range(5)], 0.35)
    s.street_in(2)
    return s.paint()


def end_lamp():
    s = Street('end_lamp', 7, 5, seed=113)
    s.rect(2, 0, 4, 3)
    s.ragged([(x, z) for x in range(7) for z in range(5)], 0.4)
    s.street_in(3)
    b = s.paint()
    b.set(3, 0, 4, 'cobblestone')
    parts.lamp_post(b, 3, 1, 4, height=3)
    b.custom(2, 1, 3, 'village_bench', facing='north')
    b.custom(4, 1, 3, 'village_bench', facing='north')
    for x in (1, 5):
        b.set(x, 0, 4, 'grass_block')
        parts.bush(b, x, 1, 4, 'flowering_azalea_leaves' if x == 1 else 'azalea_leaves')
    return b


def end_gate():
    """Timber gatehouse with palisade wings where a street leaves the village."""
    b = Build('end_gate', (17, 12, 7), kind='street', background='structure_void')
    s = Street('end_gate', 17, 7, h=12, seed=114)
    s.b = b
    s.rect(6, 0, 10, 6)
    s.ragged([(x, z) for x in (5, 11) for z in range(7)], 0.6)
    s.street_in(8)
    s.paint()
    # Palisade wings: sharpened logs on a stone footing.
    for x in list(range(0, 3)) + list(range(14, 17)):
        b.set(x, 0, 3, 'cobblestone')
        h = 4 if x % 2 else 5
        for y in range(1, h + 1):
            b.set(x, y, 3, 'spruce_log', axis='y')
        b.set(x, h + 1, 3, 'spruce_fence')
    # Two timber towers on stone bases, each capped with a little pyramid roof.
    for x0 in (3, 11):
        for x in range(x0, x0 + 3):
            for z in range(2, 5):
                corner = x in (x0, x0 + 2) and z in (2, 4)
                for y in range(0, 7):
                    if y <= 1:
                        b.set(x, y, z, 'cobblestone')
                    elif corner:
                        b.set(x, y, z, 'stripped_spruce_log', axis='y')
                    elif y == 6:
                        b.set(x, y, z, 'stripped_spruce_log', axis='x' if z != 3 else 'z')
                    else:
                        b.set(x, y, z, 'spruce_planks' if (x, z) != (x0 + 1, 3) else 'air')
        for z in (2, 4):
            b.set(x0 + 1, 4, z, 'glass_pane')
        parts.pyramid_roof(b, x0 - 1, 1, x0 + 3, 5, 7, parts.ROOFS['spruce'].stairs, 'spruce_planks', pitch=1,
                           finial=['spruce_fence'])
        for z, f in ((1, 'north'), (5, 'south')):
            b.set(x0 + 1, 5, z, 'red_wall_banner', facing=f)
    # Lintel beam and a small roof over the passage, with a lantern.
    for x in range(6, 11):
        b.set(x, 6, 3, 'stripped_spruce_log', axis='x')
    parts.gable_roof(b, 6, 3, 10, 3, 6, parts.ROOFS['spruce'], axis='x', overhang=1, rake=0)
    b.set(8, 5, 3, 'chain', axis='y')
    b.set(8, 4, 3, 'lantern', hanging=True)
    for x, z in ((5, 1), (11, 1), (5, 5), (11, 5)):
        b.set(x, 0, z, 'cobblestone')
        b.set(x, 1, z, 'spruce_fence')
        b.set(x, 2, z, 'lantern')
    return b


DESIGNS = {
    'avenue': avenue, 'avenue_bend': avenue_bend,
    'street_straight_short': straight_short, 'street_straight_long': straight_long,
    'street_straight_lamp': straight_lamp, 'street_bend_right': bend_right, 'street_bend_left': bend_left,
    'street_turn_right': turn_right, 'street_turn_left': turn_left, 'street_tee_right': tee_right,
    'street_tee_left': tee_left, 'street_fork': fork, 'street_crossroads': crossroads, 'street_square': square,
    'end_fade': end_fade, 'end_lamp': end_lamp, 'end_gate': end_gate,
}
