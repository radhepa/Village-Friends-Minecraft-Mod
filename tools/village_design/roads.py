"""Road painting shared by the plaza and the street kit.

Streets are terrain-matching pieces: every column follows the ground, so a
road is just its Y=0 surface plus clear air above it. Cells nobody paints are
``structure_void`` and keep the natural ground and grass.
"""
import random

from .kit import Build

STREET_IN = dict(name='street_in', target='street_out')
LOT = dict(name='lot', target='building_entrance', pool='plains/lots')


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
    """Pick a surface block: worn gravel and cobble near the middle, packed path toward the edges."""
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


class Street:
    """A terrain-matching street template."""

    def __init__(self, name, w, d, h=6, seed=1):
        self.b = Build(name, (w, h, d), kind='street', background='structure_void')
        self.seed = seed
        self.rng = random.Random(seed)
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
            b.set(x, 0, z, road_block(x, z, self.seed, c))
            for y in range(1, b.h):
                if b.get(x, y, z)[0] == 'minecraft:air' and (x, y, z) not in b.grid:
                    b.set(x, y, z, 'air')
        for (x, z) in self.edge:
            if (x, z) in self.core or not b.inside(x, 0, z):
                continue
            r = noise(x, z, self.seed + 11)
            b.set(x, 0, z, 'dirt_path' if r < .45 else 'coarse_dirt' if r < .6 else 'grass_block')
            for y in range(1, b.h):
                if (x, y, z) not in b.grid:
                    b.set(x, y, z, 'air')
        return b

    # connectors -----------------------------------------------------------
    def street_in(self, x, z=0):
        self.b.jigsaw(x, 1, z, 'north_up', **STREET_IN)

    def street_out(self, x, z, facing, pool='plains/streets', selection=1):
        self.b.jigsaw(x, 1, z, f'{facing}_up', 'street_out', target='street_in', pool=pool, selection=selection)

    def lot(self, x, z, facing, pool='plains/lots'):
        self.b.jigsaw(x, 1, z, f'{facing}_up', 'lot', target='building_entrance', pool=pool)

    def lamp(self, x, z, arm=None, height=3):
        b = self.b
        b.set(x, 0, z, 'cobblestone')
        for y in range(1, 1 + height):
            b.set(x, y, z, 'spruce_fence')
        if arm:
            from .kit import DIRS
            dx, dz = DIRS[arm]
            b.set(x, 1 + height, z, 'spruce_fence')
            b.set(x + dx, 1 + height, z + dz, 'spruce_fence')
            b.set(x + dx, height, z + dz, 'lantern', hanging=True, waterlogged=False)
        else:
            b.set(x, 1 + height, z, 'lantern', hanging=False, waterlogged=False)
