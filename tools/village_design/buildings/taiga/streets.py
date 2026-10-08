"""Taiga street kit: the shared street pieces drawn in the taiga palette.

Everything comes from ``streets.kit(palette.THEME)`` (podzol and mossy cobble roads,
spruce lamp posts on mossy stone, spruce and sweet berry planters). The village
gate is replaced by a log palisade gate, a rigid piece. Decor on the
terrain-matching pieces stays one column wide.
"""
from ...kit import Build
from ...roads import Street
from .. import streets
from . import core_parts as T
from .palette import THEME


def end_gate(t=THEME):
    """Palisade gate where a street leaves the village: sharpened log wings and a roofed log gateway."""
    b = Build(t.name('end_gate'), (17, 12, 7), kind='street', background='structure_void')
    s = Street(t.name('end_gate'), 17, 7, h=12, seed=414, theme=t)
    s.b = b
    s.rect(6, 0, 10, 6)
    s.ragged([(x, z) for x in (5, 11) for z in range(7)], 0.6)
    s.street_in(8)
    s.paint()
    # Palisade wings: sharpened spruce logs on a mossy footing, a stake tip on each.
    for x in list(range(0, 5)) + list(range(12, 17)):
        b.set(x, 0, 3, 'mossy_cobblestone' if x % 3 else 'cobblestone')
        h = 4 if x % 2 else 5
        for y in range(1, h + 1):
            b.set(x, y, 3, 'spruce_log', axis='y')
        b.set(x, h + 1, 3, 'spruce_fence')
    # Raking braces behind the wings.
    for x in (1, 15):
        b.set(x, 1, 4, 'spruce_stairs', facing='north', half='bottom', lock=True)
    # Gateposts: paired logs on rubble bases, a lintel and a little mossy gable roof.
    for x0 in (4, 11):
        for x in (x0, x0 + 1):
            for z in (3,):
                b.set(x, 0, z, 'mossy_cobblestone')
                for y in range(1, 8):
                    b.set(x, y, z, 'spruce_log', axis='y')
    for x in range(6, 11):
        b.set(x, 6, 3, 'stripped_spruce_log', axis='x')
        b.set(x, 7, 3, 'spruce_planks')
    for x, f in ((6, 'east'), (10, 'west')):
        b.set(x, 5, 3, 'spruce_stairs', facing=f, half='top', lock=True)
    T.roof(b, 4, 3, 12, 3, 8, 'spruce', axis='x', pitch=1, overhang=1, rake=0, gable='spruce_planks', seed=414,
           moss=.35, finials=False)
    for x in (4, 12):
        b.set(x, 9, 3, 'spruce_fence')
    T.hang_lantern(b, 8, 5, 3, links=1)
    for x in (5, 11):
        b.set(x, 5, 2, 'green_wall_banner', facing='north')
        b.set(x, 5, 4, 'green_wall_banner', facing='south')
    # Fire baskets outside the gate.
    for x in (3, 13):
        b.set(x, 0, 1, 'mossy_cobblestone')
        b.set(x, 1, 1, 'mossy_cobblestone_wall')
        b.set(x, 2, 1, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    return b


def _fixed(design):
    return lambda: T.fix_ids(design())


DESIGNS = {name: _fixed(design) for name, design in streets.kit(THEME).items()}
DESIGNS[THEME.name('end_gate')] = end_gate
