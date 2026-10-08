"""Savanna street kit: the shared kit drawn in the savanna theme, with a stockade gate.

Straights, bends, turns, junctions and the well square come from
``streets.kit(THEME)`` (packed-mud and red-sand roads, acacia lamp posts on mud
footings, acacia-leaf and tall-grass planters). The gate where a street leaves the
village is replaced by a rigid savanna one: two mud bastions with beam ends and
white pinnacles, a thatched lintel over the road and sharpened acacia stockade wings.
"""
from ...kit import Build
from ...roads import Street
from .. import streets
from . import core_parts as cp
from .palette import THEME


def end_gate(t=THEME):
    """Stockade gate (a rigid piece): mud bastions, a thatched passage and palisade wings."""
    b = Build(t.name('end_gate'), (17, 11, 7), kind='street', background='structure_void')
    s = Street(t.name('end_gate'), 17, 7, h=11, seed=2114, theme=t)
    s.b = b
    s.rect(6, 0, 10, 6)
    s.ragged([(x, z) for x in (5, 11) for z in range(7)], 0.6)
    s.street_in(8)
    s.paint()
    # Palisade wings of sharpened acacia logs.
    cp.stockade(b, [(x, 3) for x in range(0, 3)] + [(x, 3) for x in range(14, 17)], h=4)
    # Two mud bastions with a crenellated top, beam ends and white pinnacles.
    for x0 in (3, 11):
        x1 = x0 + 2
        for y in range(0, 6):
            for x in range(x0, x1 + 1):
                for z in range(2, 5):
                    b.set(x, y, z, 'mud_bricks' if y <= 1 or (x in (x0, x1) and z in (2, 4)) else 'packed_mud')
        for x in range(x0, x1 + 1):
            for z in range(2, 5):
                edge = x in (x0, x1) or z in (2, 4)
                corner = x in (x0, x1) and z in (2, 4)
                if corner:
                    b.set(x, 6, z, 'mud_bricks')
                    b.set(x, 7, z, 'white_terracotta')
                elif edge:
                    b.set(x, 6, z, 'mud_brick_wall')
        for z, f in ((1, 'north'), (5, 'south')):
            b.set(x0 + 1, 4, z, 'red_wall_banner', facing=f)
            b.set(x0 + 1, 2, z, 'acacia_fence')
        for x in (x0 - 1, x1 + 1):
            if 0 <= x < 17 and b.get(x, 3, 3)[0] in ('minecraft:air', 'minecraft:structure_void'):
                b.set(x, 3, 3, 'acacia_fence')
        b.set(x0 + 1, 5, 1, 'acacia_fence')
        b.set(x0 + 1, 5, 5, 'acacia_fence')
    # Lintel and a thatched canopy over the road, with a lantern.
    for x in range(6, 11):
        b.set(x, 5, 3, 'stripped_acacia_log', axis='x')
    for x in range(5, 12):
        for z in (2, 4):
            b.set(x, 6, z, cp.THATCH.slab, type='bottom', waterlogged=False)
    for x in range(6, 11):
        b.set(x, 6, 3, 'hay_block', axis='x')
        b.set(x, 7, 3, cp.THATCH.slab, type='bottom', waterlogged=False)
    b.set(8, 4, 3, 'lantern', hanging=True, waterlogged=False)
    # Lantern posts outside the gate.
    for x, z in ((5, 0), (11, 0), (5, 6), (11, 6)):
        cp.lamp(b, x, z, y=0, height=2, base='mud_bricks')
    return b


def square(t=THEME):
    """The kit's well square, with the well's lantern on an iron chain (26.3 renamed ``chain``)."""
    b = streets.square(t)
    b.replace(0, 0, 0, b.w - 1, b.h - 1, b.d - 1, 'chain', 'iron_chain[axis=y]')
    return b


DESIGNS = streets.kit(THEME)
DESIGNS[THEME.name('end_gate')] = end_gate
DESIGNS[THEME.name('street_square')] = square
