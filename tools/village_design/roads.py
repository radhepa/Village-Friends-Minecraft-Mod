"""Road painting shared by the plaza and the street kit.

Streets are terrain-matching pieces: every column follows the ground, so a
road is just its Y=0 surface plus clear air above it. Cells nobody paints are
``structure_void`` and keep the natural ground and grass.

Because each column of a terrain-matching piece is placed on its own, anything
taller than one block that spans several columns (a roofed well, a lamp arm, a
gatehouse) shears apart on slopes. Keep street decor to single columns; put
anything wider in a rigid piece (a square or a street end).

A ``Theme`` holds the materials of one village type's streets, so every type can
reuse the street kit in ``buildings/streets.py`` with its own surface, edges,
lamps and pools.
"""
import random

from .kit import Build


def noise(x, z, seed):
    """Small deterministic value noise in [0, 1)."""
    h = (x * 374761393 + z * 668265263 + seed * 2147483647) & 0xFFFFFFFF
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return (h ^ (h >> 16)) / 2 ** 32


def smooth(x, z, seed, scale=3.0):
    """Blocky blended noise so materials form patches rather than salt and pepper."""
    gx, gz = int(x // scale), int(z // scale)
    fx, fz = x / scale - gx, z / scale - gz
    a, b = noise(gx, gz, seed), noise(gx + 1, gz, seed)
    c, d = noise(gx, gz + 1, seed), noise(gx + 1, gz + 1, seed)
    top, bottom = a + (b - a) * fx, c + (d - c) * fx
    return top + (bottom - top) * fz


def road_block(x, z, seed, centrality):
    """Plains: worn gravel and cobble near the middle, packed path toward the edges."""
    n = smooth(x, z, seed) * 0.7 + noise(x, z, seed + 7) * 0.3
    v = n + centrality * 0.25
    if v > 0.86:
        return 'cobblestone'
    if v > 0.74:
        return 'gravel'
    if v > 0.70:
        return 'andesite'
    if v < 0.16:
        return 'coarse_dirt'
    if noise(x, z, seed + 3) < 0.05:
        return 'mossy_cobblestone'
    return 'dirt_path'


def edge_block(r):
    """Plains verge for a ragged-edge cell; ``r`` is noise in [0, 1)."""
    return 'dirt_path' if r < .45 else 'coarse_dirt' if r < .6 else 'grass_block'


class Theme:
    """Street materials and pool names for one village type.

    ``prefix`` is prepended to every street template name ('' for plains,
    'desert/' for the desert). ``road(x, z, seed, centrality)`` and ``edge(r)``
    choose surface blocks. ``post`` is the lamp post (a fence) standing on
    ``post_base``; ``light`` sits on top. ``planter`` is the soil under a
    ``bush``/``bush_alt`` decoration. ``bench`` is a single-block seat.
    """

    def __init__(self, prefix='', streets='plains/streets', ends='plains/street_ends', lots='plains/lots',
                 road=road_block, edge=edge_block, post='spruce_fence', post_base='cobblestone', light='lantern',
                 planter='grass_block', bush='azalea_leaves', bush_alt='flowering_azalea_leaves',
                 bench='villagefriends:village_bench', wood='spruce', stone='cobblestone', seed_offset=0):
        self.prefix, self.streets, self.ends, self.lots = prefix, streets, ends, lots
        self.road, self.edge = road, edge
        self.post, self.post_base, self.light = post, post_base, light
        self.planter, self.bush, self.bush_alt, self.bench = planter, bush, bush_alt, bench
        self.wood, self.stone, self.seed_offset = wood, stone, seed_offset

    def name(self, base):
        return self.prefix + base


PLAINS = Theme()
STREET_IN = dict(name='street_in', target='street_out')


class Street:
    """A terrain-matching street template."""

    def __init__(self, name, w, d, h=6, seed=1, theme=PLAINS):
        self.theme = theme
        self.b = Build(name, (w, h, d), kind='street', background='structure_void')
        self.seed = seed + theme.seed_offset
        self.rng = random.Random(self.seed)
        self.core = {}
        self.edge = set()

    def road(self, cells, centre_fn=None):
        for (x, z) in cells:
            c = centre_fn(x, z) if centre_fn else 0.5
            self.core[(x, z)] = max(self.core.get((x, z), 0), c)

    def rect(self, x0, z0, x1, z1, axis='z'):
        """Road rectangle; ``axis`` is the travel direction (for centre weighting)."""
        cells = [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]
        if axis == 'z':
            mid, half = (x0 + x1) / 2, max(1, (x1 - x0) / 2)
            self.road(cells, lambda x, z: 1 - abs(x - mid) / half)
        else:
            mid, half = (z0 + z1) / 2, max(1, (z1 - z0) / 2)
            self.road(cells, lambda x, z: 1 - abs(z - mid) / half)

    def disc(self, cx, cz, r):
        cells = [(x, z) for x in range(int(cx - r), int(cx + r) + 1) for z in range(int(cz - r), int(cz + r) + 1)
                 if (x - cx) ** 2 + (z - cz) ** 2 <= r * r + 0.5]
        self.road(cells, lambda x, z: 1 - ((x - cx) ** 2 + (z - cz) ** 2) ** .5 / max(r, 1))

    def ragged(self, cells, chance=0.6):
        for c in cells:
            if c not in self.core and self.rng.random() < chance:
                self.edge.add(c)

    def paint(self):
        b = self.b
        for (x, z), c in self.core.items():
            b.set(x, 0, z, self.theme.road(x, z, self.seed, c))
            for y in range(1, b.h):
                if b.get(x, y, z)[0] == 'minecraft:air' and (x, y, z) not in b.grid:
                    b.set(x, y, z, 'air')
        for (x, z) in self.edge:
            if (x, z) in self.core or not b.inside(x, 0, z):
                continue
            b.set(x, 0, z, self.theme.edge(noise(x, z, self.seed + 11)))
            for y in range(1, b.h):
                if (x, y, z) not in b.grid:
                    b.set(x, y, z, 'air')
        return b

    # connectors -----------------------------------------------------------
    def street_in(self, x, z=0):
        self.b.jigsaw(x, 1, z, 'north_up', **STREET_IN)

    def street_out(self, x, z, facing, pool=None, selection=1):
        self.b.jigsaw(x, 1, z, f'{facing}_up', 'street_out', target='street_in', pool=pool or self.theme.streets,
                      selection=selection)

    def lot(self, x, z, facing, pool=None):
        self.b.jigsaw(x, 1, z, f'{facing}_up', 'lot', target='building_entrance', pool=pool or self.theme.lots)

    def lamp(self, x, z, height=3):
        """A single-column lamp post, which stays upright on any slope."""
        b, t = self.b, self.theme
        b.set(x, 0, z, t.post_base)
        for y in range(1, 1 + height):
            b.set(x, y, z, t.post)
        b.set(x, 1 + height, z, t.light, hanging=False, waterlogged=False) if t.light == 'lantern' \
            else b.set(x, 1 + height, z, t.light)

    def planter(self, x, z, alt=False):
        """A bush on its own patch of soil."""
        b, t = self.b, self.theme
        b.set(x, 0, z, t.planter)
        plant = t.bush_alt if alt else t.bush
        if plant.endswith('_leaves'):
            b.set(x, 1, z, plant, persistent=True, distance=1, waterlogged=False)
        else:
            b.set(x, 1, z, plant)

    def bench(self, x, z, facing):
        b, t = self.b, self.theme
        if t.bench.startswith('villagefriends:'):
            b.custom(x, 1, z, t.bench.split(':')[1], facing=facing)
        else:
            b.set(x, 1, z, t.bench, facing=facing, half='bottom', shape='straight', waterlogged=False, lock=True)
