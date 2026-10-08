"""Snowy street kit: the shared kit drawn in the frost-hamlet theme, plus a stone-and-log watch-gate.

The shared well and gatehouse use the old ``chain`` id and an open-water well; here chains become
26.3 ``iron_chain`` and the neighbourhood well is frozen over (blue ice), since the square and its
streets keep water out. Decor on terrain-matching pieces stays one column wide.
"""
from ...kit import Build
from ...roads import Street
from ... import parts
from .. import streets
from . import palette
from . import core_parts as cp

T = palette.THEME
R = palette.ROOFS


def _wintered(make):
    def build():
        b = make()
        for pos, state in list(b.grid.items()):
            if state[0] == 'minecraft:chain':
                b.grid[pos] = ('minecraft:iron_chain', state[1])
            elif state[0] == 'minecraft:water':
                b.set(*pos, 'blue_ice')
        return b
    return build


def watch_gate():
    """Watch-gate where a street leaves the village: two stone towers with log lookouts and slate
    spires, a roofed log bridge over the passage, and palisade wings of sharpened stakes."""
    name = T.name('end_gate')
    b = Build(name, (17, 16, 7), kind='street', background='structure_void')
    s = Street(name, 17, 7, h=16, seed=3114, theme=T)
    s.b = b
    s.rect(6, 0, 10, 6)
    s.ragged([(x, z) for x in (5, 11) for z in range(7)], 0.6)
    s.street_in(8)
    s.paint()
    # Palisade wings.
    cp.palisade(b, [(x, 3) for x in (0, 1, 2, 14, 15, 16)])
    # Towers: a stone shaft, a log lookout and a steep slate spire.
    for x0 in (2, 11):
        x1 = x0 + 3
        for y in range(0, 9):
            for x in range(x0, x1 + 1):
                for z in range(1, 6):
                    if not (x0 <= x <= x1 and 2 <= z <= 4):
                        continue
                    edge = x in (x0, x1) or z in (2, 4)
                    corner = x in (x0, x1) and z in (2, 4)
                    if y <= 1:
                        b.set(x, y, z, 'cobblestone')
                    elif y <= 5:
                        b.set(x, y, z, ('stone_bricks' if corner else 'cobblestone') if edge else 'air')
                    else:
                        b.set(x, y, z, 'air')
        cp.log_walls(b, x0, 2, x1, 4, 6, 8, notch=False)
        for y in (6, 7, 8):
            for x in range(x0 + 1, x1):
                b.set(x, y, 3, 'air')
        b.fill(x0, 9, 2, x1, 9, 4, 'spruce_planks')
        parts.pyramid_roof(b, x0 - 1, 1, x1 + 1, 5, 9, R['slate'].stairs, R['slate'].full, pitch=2,
                           finial=['spruce_fence'])
        for z, out in ((2, 'north'), (4, 'south')):
            b.set(x0 + 1, 7, z, 'glass_pane')
            b.set(x0 + 2, 7, z, 'glass_pane')
            b.set(x0 + 1, 4, z, 'glass_pane')
        for z, f in ((1, 'north'), (5, 'south')):
            b.set(x0 + 2 if x0 == 2 else x0 + 1, 5, z, 'light_blue_wall_banner', facing=f)
        cp.hang(b, x0 + 1, 8, 3)
    # Log bridge over the passage with its own steep roof.
    for x in range(6, 11):
        b.set(x, 6, 2, 'stripped_spruce_log', axis='x')
        b.set(x, 6, 4, 'stripped_spruce_log', axis='x')
        b.set(x, 6, 3, 'spruce_planks')
        for y in (7, 8):
            for z in (2, 4):
                b.set(x, y, z, 'spruce_log', axis='x')
    for z in (2, 4):
        b.set(8, 7, z, 'glass_pane')
    parts.gable_roof(b, 6, 2, 10, 4, 9, R['dark_oak'], axis='x', overhang=1, rake=0, gable='spruce_planks', pitch=2)
    b.fill(6, 9, 3, 10, 9, 3, 'spruce_planks')
    for z in (2, 4):
        b.set(6, 5, z, 'spruce_stairs', facing='east', half='top', lock=True)
        b.set(10, 5, z, 'spruce_stairs', facing='west', half='top', lock=True)
    b.set(8, 5, 3, 'iron_chain', axis='y')
    b.set(8, 4, 3, 'lantern', hanging=True, waterlogged=False)
    # Lanterns on posts either side of the road, outside and in.
    for x, z in ((5, 0), (11, 0), (5, 6), (11, 6)):
        b.set(x, 0, z, T.stone)
        b.set(x, 1, z, 'spruce_fence')
        b.set(x, 2, z, 'lantern', hanging=False, waterlogged=False)
    return b


DESIGNS = {name: _wintered(make) for name, make in streets.kit(T).items()}
DESIGNS[T.name('end_gate')] = watch_gate
