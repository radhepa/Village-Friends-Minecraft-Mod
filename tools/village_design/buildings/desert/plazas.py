"""Desert town centres: 33x33 squares built on the shared ``plazas.base``.

Slots and exits sit exactly where the plains squares have them; only the
paving, the centrepiece and the furniture are desert. Each square keeps the
``town_start`` jigsaw, the notice board, the painter's easel, the bard's music
stand, a bell, benches and lighting.
"""
import math
import random

from .. import plazas
from ..plazas import C, SIZE
from ...roads import noise, smooth
from ...kit import DIRS
from ... import parts
from . import core_parts as dp

ROLES_A = {'north': ('tavern', 'apothecary'), 'east': ('garrison', 'market'),
           'south': ('workshop', 'library'), 'west': ('chapel', 'market')}
ROLES_B = {'north': ('garrison', 'library'), 'east': ('tavern', 'market'),
           'south': ('chapel', 'apothecary'), 'west': ('workshop', 'market')}
ROLES_C = {'north': ('workshop', 'apothecary'), 'east': ('chapel', 'market'),
           'south': ('tavern', 'library'), 'west': ('garrison', 'market')}


def flagstones(x, z, seed):
    """Sun-bleached flagstones: mostly smooth sandstone with sandstone and cut slabs, sand in the joints."""
    n = smooth(x, z, seed, 2.5) * .6 + noise(x, z, seed + 5) * .4
    if n < .12:
        return 'sand'
    if n < .3:
        return 'sandstone'
    if n < .72:
        return 'smooth_sandstone'
    if n < .9:
        return 'cut_sandstone'
    return 'sandstone'


def terracotta_flags(x, z, seed):
    """Warmer paving with orange and white terracotta tiles mixed in."""
    n = smooth(x, z, seed, 2.0) * .55 + noise(x, z, seed + 9) * .45
    if n < .1:
        return 'sand'
    if n < .26:
        return 'sandstone'
    if n < .58:
        return 'smooth_sandstone'
    if n < .7:
        return 'cut_sandstone'
    if n < .8:
        return 'orange_terracotta'
    if n < .9:
        return 'white_terracotta'
    return 'smooth_sandstone'


def lawn_cells(b):
    return [(x, z) for x in range(SIZE) for z in range(SIZE) if b.get(x, 0, z)[0] == 'minecraft:sand']


def scrub(b, rng, chance=.1):
    """Dry grass and dead bushes on the open sand."""
    dp.desert_plants(b, lawn_cells(b), 1, rng, chance)


def stall(b, x0, z0, facing, wool, goods):
    plazas.stall(b, x0, z0, facing, wool, goods, wood='acacia')


def rug_stall(b, x0, z0, rng):
    """Carpet seller: rugs laid out on the ground under a striped canopy (3x3 from x0,z0)."""
    for x in range(x0, x0 + 3):
        for z in range(z0, z0 + 3):
            b.set(x, 1, z, f'{rng.choice(["red", "orange", "cyan", "yellow", "magenta"])}_carpet')
    dp.canopy(b, x0, z0, x0 + 2, z0 + 2, 4, along='x', start=rng.randrange(4))
    b.set(x0 + 1, 1, z0 + 1, 'decorated_pot', facing='north')


def stage(b, x0, z0, x1, z1, rng, colors=('red', 'white', 'orange', 'white')):
    """Bard's platform: a raised sandstone dais with a striped canopy."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            b.set(x, 1, z, 'smooth_sandstone_slab' if edge else 'cut_sandstone_slab', type='bottom')
    dp.canopy(b, x0, z0 + 1, x1, z1, 5, colors=colors, along='x',
              posts=((x0, z0 + 1), (x1, z0 + 1), (x0, z1), (x1, z1)))
    for x, z in ((x0, z0), (x1, z0)):
        dp.pot(b, x, 1, z, 'cactus')


def painter_corner(b, x, z, facing, rng):
    dx, dz = DIRS[facing]
    b.custom(x, 1, z, 'easel_canvas', facing=facing)
    b.resident(x + dx, 1, z + dz, 'painter')
    lx, lz = DIRS[{'north': 'east', 'east': 'south', 'south': 'west', 'west': 'north'}[facing]]
    b.set(x - dx + lx, 1, z - dz + lz, 'decorated_pot', facing=facing)


def lamp_ring(b, radius, count, offset=0.0, skip=(), height=2):
    for i in range(count):
        a = offset + i * 2 * math.pi / count
        x, z = round(C + radius * math.cos(a)), round(C + radius * math.sin(a))
        if (x, z) in skip:
            continue
        dp.wall_post(b, x, 1, z, height=height)


# ------------------------------------------------------------------ oasis
def oasis():
    """Oasis: a spring-fed pool with a palm island, sugar cane banks and a shaded promenade."""
    b, rng = plazas.base('desert/plaza_oasis', ROLES_A, seed=211, ring=10.5, height=16, prefix='desert/',
                         paving=flagstones, lawn='sand', ring_block='cut_sandstone', plants=False)
    pool, bank = set(), set()
    for x in range(SIZE):
        for z in range(SIZE):
            dx, dz = x - C, z - C
            a = math.atan2(dz, dx)
            r = math.hypot(dx, dz) * (1 + .1 * math.sin(3 * a + 1.3) + .05 * math.sin(5 * a))
            if r <= 5.6:
                pool.add((x, z))
            elif r <= 7.4:
                bank.add((x, z))
    island = {(C + dx, C + dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1) if abs(dx) + abs(dz) <= 1}
    for x, z in pool:
        b.set(x, 0, z, 'sand' if (x, z) in island else 'water', **({} if (x, z) in island else {'level': 0}))
        b.set(x, 1, z, 'air')
    for x, z in bank:
        b.set(x, 0, z, 'sand' if noise(x, z, 5) < .7 else 'sandstone')
        b.set(x, 1, z, 'air')
    # Reeds and lily pads where the water meets the bank.
    for x, z in sorted(bank):
        wet = any((x + dx, z + dz) in pool and (x + dx, z + dz) not in island for dx, dz in DIRS.values())
        if wet and rng.random() < .45:
            for y in range(1, 2 + rng.randrange(2)):
                b.set(x, y, z, 'sugar_cane', age=0)
        elif not wet and rng.random() < .12:
            b.set(x, 1, z, rng.choice(['short_dry_grass', 'dead_bush', 'fern']))
    for x, z in sorted(pool - island):
        if rng.random() < .08 and math.hypot(x - C, z - C) > 2:
            b.set(x, 1, z, 'lily_pad')
    # The palm island carries the town_start jigsaw at the foot of its trunk.
    b.jigsaw(C, 1, C, 'up_north', 'town_start', final='minecraft:jungle_log')
    dp.palm(b, C, 2, C, rng, height=7, lean='east')
    for (x, z), h, lean in (((C - 6, C + 2), 6, 'west'), ((C + 5, C + 5), 7, 'south'), ((C + 2, C - 7), 5, 'north'),
                            ((C - 4, C - 5), 6, 'north'), ((C + 7, C - 2), 5, 'east')):
        b.set(x, 0, z, 'sand')
        dp.palm(b, x, 1, z, rng, height=h, lean=lean)
    # Promenade benches looking over the water, lamps between them.
    for x, z, f in ((C, C - 8, 'north'), (C, C + 8, 'south'), (C - 8, C, 'west'), (C + 8, C, 'east')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    lamp_ring(b, 9.0, 8, offset=math.pi / 8)
    # Painter on the north-west sand, the bard's dais on the south-east.
    painter_corner(b, 6, 7, 'south', rng)
    b.set(4, 0, 5, 'sand')
    dp.cactus(b, 4, 1, 5, 2)
    stage(b, 23, 22, 27, 26, rng)
    b.custom(25, 2, 24, 'music_stand', facing='north')
    b.resident(25, 2, 25, 'bard')
    for x in (24, 26):
        b.custom(x, 1, 20, 'village_bench', facing='south')
    # Market stalls on the north-east sand, the notice board by the tavern slot.
    stall(b, 24, 6, 'west', 'orange', ['melon', 'decorated_pot[facing=west]', 'hay_block[axis=y]'])
    stall(b, 24, 10, 'west', 'cyan', ['barrel[facing=up]', 'potted_cactus', 'dried_kelp_block'])
    b.custom(13, 1, 4, 'notice_board', facing='south')
    # Bell on the south-west sand and a brazier ring for evenings.
    plazas.bell_frame(b, 8, 24, along='x', log='stripped_acacia_log', stone='cut_sandstone',
                      slab='smooth_sandstone_slab')
    dp.brazier(b, 5, 0, 27)
    for x, z, f in ((4, 27, 'east'), (6, 27, 'west'), (5, 26, 'south'), (5, 28, 'north')):
        b.custom(x, 1, z, 'campfire_bench', facing=f)
    scrub(b, rng, .08)
    return b


# ----------------------------------------------------------------- bazaar
def souk_hall(b, x0, z0, x1, z1, rng):
    """Covered bazaar: arcades on all four sides, a flat roof with merlons and a lantern dome."""
    h = 4
    for x0_, z0_, x1_, z1_ in ((x0, z0, x1, z0), (x0, z1, x1, z1), (x0, z0, x0, z1), (x1, z0, x1, z1)):
        dp.arcade(b, x0_, z0_, x1_, z1_, 1, h, pier='cut_sandstone', spacing=5, lintel='smooth_sandstone')
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, 0, z, 'smooth_sandstone' if (x + z) % 2 else 'cut_sandstone')
    b.fill(x0 + 1, h + 1, z0 + 1, x1 - 1, h + 1, z1 - 1, 'smooth_sandstone')
    dp.cornice(b, x0, z0, x1, z1, h + 1)
    dp.parapet(b, x0, z0, x1, z1, h + 2, style='merlon')
    # Drum and dome over the middle, with a gilded finial.
    cx, cz = (x0 + x1) // 2, (z0 + z1) // 2
    for x in range(cx - 2, cx + 3):
        for z in range(cz - 2, cz + 3):
            if abs(x - cx) == 2 or abs(z - cz) == 2:
                b.set(x, h + 2, z, 'cut_sandstone' if (x + z) % 2 else 'orange_terracotta')
    b.fill(cx - 1, h + 1, cz - 1, cx + 1, h + 1, cz + 1, 'air')
    dp.dome(b, cx, cz, h + 3, 2, mat='white_terracotta',
            finial=['cut_sandstone_slab[type=bottom]'])
    dp.lantern(b, cx, h + 3, cz, chain=1)
    # Inside: a tiled basin round the town_start pedestal, stalls between the piers.
    for x in range(cx - 1, cx + 2):
        for z in range(cz - 1, cz + 2):
            if (x, z) != (cx, cz):
                b.set(x, 1, z, 'water', level=0)
                b.set(x, 0, z, 'cyan_terracotta')
    for x in range(cx - 2, cx + 3):
        for z in range(cz - 2, cz + 3):
            if abs(x - cx) == 2 or abs(z - cz) == 2:
                b.set(x, 1, z, 'cut_sandstone_slab' if (x + z) % 2 else 'smooth_sandstone_slab', type='bottom')
    b.jigsaw(cx, 1, cz, 'up_north', 'town_start', final='minecraft:chiseled_sandstone')
    b.set(cx, 2, cz, 'decorated_pot', facing='north')
    goods = ['melon', 'decorated_pot[facing=north]', 'barrel[facing=up]', 'hay_block[axis=y]', 'potted_cactus',
             'dried_kelp_block', 'pumpkin', 'cyan_wool', 'orange_wool']
    for (x, z), col in (((x0 + 1, z0 + 1), 'red'), ((x1 - 1, z0 + 1), 'yellow'), ((x0 + 1, z1 - 1), 'cyan'),
                        ((x1 - 1, z1 - 1), 'orange')):
        b.set(x, 1, z, 'barrel', facing='up', open=False)
        b.set(x, 2, z, rng.choice(goods))
        for dx, dz in ((1 if x == x0 + 1 else -1, 0), (0, 1 if z == z0 + 1 else -1)):
            b.set(x + dx, 1, z + dz, 'acacia_planks')
            b.set(x + dx, 2, z + dz, rng.choice(goods))
        b.set(x + (2 if x == x0 + 1 else -2), 1, z + (2 if z == z0 + 1 else -2), f'{col}_carpet')
    for x, z in ((x0 + 3, z0 + 3), (x1 - 3, z0 + 3), (x0 + 3, z1 - 3), (x1 - 3, z1 - 3)):
        dp.lantern(b, x, h, z)


def bazaar():
    """Bazaar: a shaded souk hall over a tiled basin, stalls and a rug seller on the sand around it."""
    b, rng = plazas.base('desert/plaza_bazaar', ROLES_B, seed=212, ring=11.5, height=16, prefix='desert/',
                         paving=terracotta_flags, lawn='sand', ring_block='orange_terracotta', plants=False)
    souk_hall(b, C - 5, C - 5, C + 5, C + 5, rng)
    # Stalls out on the square.
    stall(b, 7, 9, 'east', 'red', ['melon', 'barrel[facing=up]', 'hay_block[axis=y]'])
    stall(b, 25, 23, 'west', 'yellow', ['decorated_pot[facing=west]', 'pumpkin', 'potted_dead_bush'])
    rug_stall(b, 22, 6, rng)
    # Palms in raised planters at the four corners of the hall.
    for x, z in ((C - 8, C - 8), (C + 8, C - 8), (C - 8, C + 8), (C + 8, C + 8)):
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                b.set(x + dx, 0, z + dz, 'sand' if (dx, dz) == (0, 0) else 'cut_sandstone')
                if (dx, dz) != (0, 0):
                    b.set(x + dx, 1, z + dz, 'smooth_sandstone_slab', type='bottom')
        dp.palm(b, x, 1, z, rng, height=6)
    painter_corner(b, 5, 21, 'east', rng)
    stage(b, 22, 26 - 4, 26, 26, rng, colors=('cyan', 'white', 'yellow', 'white'))
    b.custom(24, 2, 24, 'music_stand', facing='north')
    b.resident(24, 2, 25, 'bard')
    b.custom(13, 1, 4, 'notice_board', facing='south')
    plazas.bell_frame(b, 24, 9, along='z', log='stripped_jungle_log', stone='chiseled_sandstone',
                      slab='cut_sandstone_slab')
    for x, z, f in ((C - 7, C, 'west'), (C + 7, C, 'east'), (C, C - 7, 'north'), (C, C + 7, 'south')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    lamp_ring(b, 10.5, 8, offset=math.pi / 8)
    for x, z in ((4, 6), (28, 28), (6, 28)):
        dp.cactus(b, x, 1, z, 2 + (x % 2))
    scrub(b, rng, .1)
    return b


# ------------------------------------------------------------- domed well
def tile_star(b, rng):
    """Glazed tile star round the well pavilion."""
    for x in range(SIZE):
        for z in range(SIZE):
            r = math.hypot(x - C, z - C)
            a = math.atan2(z - C, x - C)
            if 8.4 < r <= 9.4:
                b.set(x, 0, z, 'cyan_glazed_terracotta' if (x + z) % 2 else 'white_glazed_terracotta',
                      facing=['north', 'east', 'south', 'west'][(x * 3 + z) % 4])
            elif 4.5 < r <= 8.4:
                ray = abs(math.sin(4 * a)) < .18 and r > 5
                b.set(x, 0, z, 'light_blue_glazed_terracotta' if ray else ('smooth_sandstone' if r > 6 else 'cut_sandstone'),
                      **({'facing': 'north'} if ray else {}))


def well_pavilion(b, rng):
    """Domed well: four L-shaped piers, pointed arches on every side, a ribbed dome and a hanging lantern."""
    x0, z0, x1, z1 = C - 3, C - 3, C + 3, C + 3
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, 0, z, 'cut_sandstone' if (x + z) % 2 else 'smooth_sandstone')
            corner = (x - x0 < 2 or x1 - x < 2) and (z - z0 < 2 or z1 - z < 2) and (x in (x0, x1) or z in (z0, z1))
            if corner:
                for y in range(1, 5):
                    b.set(x, y, z, 'cut_sandstone' if y in (1, 4) else 'smooth_sandstone')
    for (ax, az, bx, bz) in ((x0 + 2, z0, x1 - 2, z0), (x0 + 2, z1, x1 - 2, z1), (x0, z0 + 2, x0, z1 - 2),
                             (x1, z0 + 2, x1, z1 - 2)):
        dp.arch(b, ax, az, bx, bz, 4)
        for x, z in parts.along(ax, az, bx, bz):
            b.set(x, 5, z, 'cut_sandstone')
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                b.set(x, 5, z, 'chiseled_sandstone' if (x, z) in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)) else 'cut_sandstone')
    dp.cornice(b, x0, z0, x1, z1, 5)
    top = dp.dome(b, C, C, 6, 3, mat='smooth_sandstone')
    b.set(C, top + 1, C, 'gold_block')
    b.set(C, top + 2, C, 'lightning_rod', facing='up', powered=False)
    # The well: a ring of curbs round the town_start spring, a pulley and lantern hanging from the dome.
    for x in range(C - 1, C + 2):
        for z in range(C - 1, C + 2):
            if (x, z) == (C, C):
                continue
            corner = abs(x - C) == 1 and abs(z - C) == 1
            b.set(x, 1, z, 'cut_sandstone' if corner else 'sandstone_wall')
            if corner:
                b.set(x, 2, z, 'acacia_fence')
                b.set(x, 3, z, 'acacia_fence')
    b.set(C, 0, C, 'water', level=0)
    b.jigsaw(C, 1, C, 'up_north', 'town_start', final='minecraft:water')
    for x in range(C - 1, C + 2):
        for z in range(C - 1, C + 2):
            if abs(x - C) == 1 and abs(z - C) == 1:
                b.set(x, 4, z, 'acacia_slab', type='bottom')
            elif (x, z) != (C, C):
                b.set(x, 4, z, 'acacia_slab', type='bottom')
    b.set(C, 4, C, 'acacia_trapdoor', facing='north', half='top', open=False, powered=False, waterlogged=False)
    for y in range(5, top):
        b.set(C, y, C, dp.CHAIN, axis='y', waterlogged=False)
    for x, z in ((C - 2, C - 2), (C + 2, C + 2)):
        dp.lantern(b, x, 4, z, hanging=True)


def well_square():
    """Well square: a domed well pavilion on a glazed tile star, palms in planters and a fruit market."""
    b, rng = plazas.base('desert/plaza_well', ROLES_C, seed=213, ring=12.5, height=18, prefix='desert/',
                         paving=flagstones, lawn='sand', ring_block='cut_sandstone', plants=False)
    tile_star(b, rng)
    well_pavilion(b, rng)
    # Palms in planters on the diagonals, benches facing the well.
    for i in range(4):
        a = math.pi / 4 + i * math.pi / 2
        x, z = round(C + 7 * math.cos(a)), round(C + 7 * math.sin(a))
        b.set(x, 0, z, 'sand')
        for dx, dz in DIRS.values():
            b.set(x + dx, 1, z + dz, 'cut_sandstone_slab', type='bottom')
        dp.palm(b, x, 1, z, rng, height=6, lean=None)
    for x, z, f in ((C, C - 6, 'north'), (C, C + 6, 'south'), (C - 6, C, 'west'), (C + 6, C, 'east')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    stall(b, 8, 9, 'south', 'orange', ['melon', 'hay_block[axis=y]', 'decorated_pot[facing=south]'])
    stall(b, 24, 23, 'north', 'red', ['pumpkin', 'barrel[facing=up]', 'potted_cactus'])
    plazas.bell_frame(b, 9, 24, along='x', log='stripped_acacia_log', stone='cut_sandstone',
                      slab='smooth_sandstone_slab')
    painter_corner(b, 6, 18, 'east', rng)
    stage(b, 24, 14, 28, 18, rng, colors=('orange', 'white', 'red', 'white'))
    b.custom(26, 2, 16, 'music_stand', facing='west')
    b.resident(27, 2, 16, 'bard')
    b.custom(13, 1, 4, 'notice_board', facing='south')
    lamp_ring(b, 10.5, 8, offset=0.3)
    for x, z in ((4, 4), (28, 4), (4, 28)):
        b.set(x, 0, z, 'sand')
        dp.cactus(b, x, 1, z, 2)
    scrub(b, rng, .08)
    return b


DESIGNS = {'desert/plaza_oasis': oasis, 'desert/plaza_bazaar': bazaar, 'desert/plaza_well': well_square}
