"""Desert street kit: the shared street pieces drawn in the desert THEME.

The terrain-matching streets come straight from ``streets.kit``. The two rigid
pieces are redrawn as desert architecture: the neighbourhood square gets a
domed well kiosk, and the street end gate is a sandstone gate with two
crenellated towers and wall wings.
"""
from .. import streets
from ...kit import Build
from ...roads import Street
from . import core_parts as dp
from .palette import THEME

T = THEME


def _iron_chains(b):
    """26.3 renamed ``chain`` to ``iron_chain``; fix any the shared kit draws."""
    for pos, state in list(b.grid.items()):
        if state[0] == 'minecraft:chain':
            b.grid[pos] = ('minecraft:iron_chain', state[1])
    return b


def square():
    """Neighbourhood square with a domed well kiosk on four sandstone piers (a rigid piece)."""
    b = streets.square(T)
    cx, cz = 7, 7
    b.clear(cx - 2, 1, cz - 2, cx + 2, b.h - 1, cz + 2)
    for x in range(cx - 1, cx + 2):
        for z in range(cz - 1, cz + 2):
            corner = abs(x - cx) == 1 and abs(z - cz) == 1
            b.set(x, 0, z, 'cut_sandstone')
            if (x, z) == (cx, cz):
                b.set(x, 0, z, 'water', level=0)
                b.set(x, 1, z, 'water', level=0)
            elif corner:
                for y in range(1, 4):
                    b.set(x, y, z, 'cut_sandstone' if y != 2 else 'smooth_sandstone')
            else:
                b.set(x, 1, z, 'sandstone_wall')
            b.set(x, 4, z, 'cut_sandstone' if corner else 'smooth_sandstone')
    dp.dome(b, cx, cz, 5, 1, mat='smooth_sandstone')
    b.set(cx, 7, cz, 'cut_sandstone_slab', type='bottom')
    dp.lantern(b, cx, 3, cz)
    return b


def end_gate():
    """Sandstone town gate: a pointed arch between two crenellated towers, with wall wings (a rigid piece)."""
    b = Build(T.name('end_gate'), (17, 11, 7), kind='street', background='structure_void')
    s = Street(T.name('end_gate'), 17, 7, h=11, seed=114, theme=T)
    s.b = b
    s.rect(6, 0, 10, 6)
    s.ragged([(x, z) for x in (5, 11) for z in range(7)], 0.6)
    s.street_in(8)
    s.paint()
    # Wall wings with merlons.
    for x in list(range(0, 3)) + list(range(14, 17)):
        b.set(x, 0, 3, 'sandstone')
        for y in range(1, 4):
            b.set(x, y, 3, 'smooth_sandstone' if y < 3 else 'cut_sandstone')
        if x % 2 == 0:
            b.set(x, 4, 3, 'cut_sandstone')
        else:
            b.set(x, 4, 3, 'smooth_sandstone_slab', type='bottom')
    # Two towers with a band, lattice slits and corner horns.
    for x0 in (3, 11):
        for x in range(x0, x0 + 3):
            for z in range(2, 5):
                for y in range(0, 7):
                    b.set(x, y, z, 'cut_sandstone' if y in (0, 3, 6) else 'smooth_sandstone')
        for x, z, _, corner in dp.parts.ring(x0, 2, x0 + 2, 4):
            if corner:
                b.set(x, 7, z, 'cut_sandstone')
                b.set(x, 8, z, 'sandstone_wall')
            elif (x + z) % 2:
                b.set(x, 7, z, 'smooth_sandstone_slab', type='bottom')
        b.set(x0 + 1, 7, 3, 'lantern', hanging=False, waterlogged=False)
        for z, out in ((2, 'north'), (4, 'south')):
            dp.lattice(b, x0 + 1, 4, z, out, height=1)
            b.set(x0 + 1, 3, z - 1 if out == 'north' else z + 1, 'orange_wall_banner', facing=out)
    # The arch over the road, a lintel and merlons.
    for z in (2, 3, 4):
        dp.arch(b, 6, z, 10, z, 4)
        for x in range(6, 11):
            b.set(x, 5, z, 'cut_sandstone' if z == 3 else 'smooth_sandstone')
            if z == 3:
                b.set(x, 6, z, 'cut_sandstone' if x % 2 == 0 else 'smooth_sandstone_slab',
                      **({} if x % 2 == 0 else {'type': 'bottom'}))
    b.set(8, 5, 2, 'chiseled_sandstone')
    b.set(8, 5, 4, 'chiseled_sandstone')
    for x, z in ((5, 1), (11, 1), (5, 5), (11, 5)):
        dp.wall_post(b, x, 0, z, height=1)
    return b


DESIGNS = {name: (lambda f=f: _iron_chains(f())) for name, f in streets.kit(T).items()}
DESIGNS[T.name('street_square')] = square
DESIGNS[T.name('end_gate')] = end_gate
