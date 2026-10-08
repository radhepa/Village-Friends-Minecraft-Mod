"""Taiga fields, pens and gardens. These favour the outer streets (``taiga/lots_outer``)."""
import random

from ...kit import Build
from ...parts import log
from . import homes_logs as H


def border(b, x0, z0, x1, z1, mat='stripped_spruce_log', skip=()):
    """Log kerb around a field at ground level."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if (x in (x0, x1) or z in (z0, z1)) and (x, z) not in skip:
                b.set(x, 0, z, log(mat, 'z' if x in (x0, x1) else 'x'))


def scarecrow(b, x, z, facing='north'):
    b.set(x, 1, z, 'spruce_fence')
    b.set(x, 2, z, 'spruce_fence')
    b.set(x - 1, 2, z, 'spruce_trapdoor', facing='west', half='top', open=True, powered=False, waterlogged=False)
    b.set(x + 1, 2, z, 'spruce_trapdoor', facing='east', half='top', open=True, powered=False, waterlogged=False)
    b.set(x, 3, z, 'carved_pumpkin', facing=facing)


def pumpkin_field():
    """Pumpkin field: stems in rows, ripe pumpkins beside them, a water channel and a scarecrow."""
    rng = random.Random(4301)
    b = Build('taiga/pumpkin_field', (11, 6, 12))
    border(b, 0, 1, 10, 11, skip={(5, 1)})
    taken = set()
    for x in range(1, 10):
        for z in range(2, 11):
            if x == 5:
                b.set(x, 0, z, 'water', level=0)
                continue
            b.set(x, 0, z, 'farmland', moisture=7)
    for x in [x for x in range(1, 10) if x != 5]:
        for z in (2, 4, 6, 8):
            if rng.random() < .55 and (x, z + 1) not in taken:
                b.set(x, 1, z, 'attached_pumpkin_stem', facing='south')
                b.set(x, 1, z + 1, 'pumpkin')
                taken.add((x, z + 1))
            else:
                b.set(x, 1, z, 'pumpkin_stem', age=rng.randrange(3, 8))
    for x in (2, 8):
        b.set(x, 1, 10, 'pumpkin_stem', age=7)
    b.set(5, 0, 1, 'dirt_path')
    b.set(5, 0, 0, 'dirt_path')
    b.set(5, 1, 2, 'spruce_slab', type='bottom', waterlogged=False)
    scarecrow(b, 9, 0)
    b.set(1, 1, 0, 'carved_pumpkin', facing='north')
    b.set(2, 1, 0, 'pumpkin')
    b.set(0, 1, 0, 'barrel', facing='up', open=False)
    b.entrance(5)
    b.natural_ground()
    return b


def potato_field():
    """Potato and beetroot plots with water channels, a composter and a covered tool rack."""
    rng = random.Random(4302)
    b = Build('taiga/potato_field', (15, 6, 12))
    for x0, x1, crop, ripe in ((0, 6, 'potatoes', 7), (8, 14, 'potatoes', 7)):
        border(b, x0, 2, x1, 11)
        mid = (x0 + x1) // 2
        for x in range(x0 + 1, x1):
            for z in range(3, 11):
                if x == mid:
                    b.set(x, 0, z, 'water', level=0)
                else:
                    b.set(x, 0, z, 'farmland', moisture=7)
                    c = 'beetroots' if (x0 == 8 and z >= 8) else crop
                    full = 3 if c == 'beetroots' else ripe
                    b.set(x, 1, z, c, age=full if rng.random() < .7 else max(1, full - 2))
    for z in range(0, 12):
        b.set(7, 0, z, 'dirt_path' if z % 3 else 'coarse_dirt')
    b.set(7, 1, 11, 'composter', level=4)
    # Tool rack under a little slab roof.
    for x in (12, 14):
        b.set(x, 1, 0, 'spruce_fence')
        b.set(x, 2, 0, 'spruce_fence')
    for x in (11, 12, 13, 14):
        b.set(x, 3, 0, 'spruce_slab', type='bottom', waterlogged=False)
    b.barrel(13, 1, 0, 'up')
    b.set(13, 2, 0, 'spruce_trapdoor', facing='north', half='top', open=True, powered=False, waterlogged=False)
    b.set(1, 1, 0, 'hay_block', axis='y')
    b.set(2, 1, 0, 'hay_block', axis='x')
    b.set(1, 2, 0, 'hay_block', axis='z')
    b.set(4, 1, 1, 'barrel', facing='up', open=False)
    b.entrance(7)
    b.natural_ground()
    return b


def berry_patch():
    """Sweet berry rows on podzol with a picker's bench and baskets."""
    rng = random.Random(4303)
    b = Build('taiga/berry_patch', (11, 5, 10))
    for x in range(0, 11):
        for z in range(1, 10):
            if x == 5:
                b.set(x, 0, z, 'dirt_path' if z % 3 else 'coarse_dirt')
                continue
            b.set(x, 0, z, 'podzol' if rng.random() < .75 else 'coarse_dirt')
            if x % 2 == 1 or x in (4, 6):
                if (x, z) in ((4, 5), (6, 5)):
                    continue
                b.set(x, 1, z, 'sweet_berry_bush', age=rng.choice([2, 3, 3, 1]))
            elif rng.random() < .3:
                b.set(x, 1, z, rng.choice(['fern', 'short_grass', 'brown_mushroom']))
    b.set(4, 1, 5, 'barrel', facing='up', open=False)
    b.set(6, 1, 5, 'composter', level=6)
    for x in (0, 10):
        b.set(x, 1, 1, 'spruce_fence')
        b.set(x, 2, 1, 'lantern', waterlogged=False)
    b.set(5, 0, 0, 'dirt_path')
    b.entrance(5)
    b.natural_ground()
    return b


def chicken_coop():
    """A closed spruce-fence run (no gaps for foxes) and a little log coop."""
    rng = random.Random(4304)
    b = Build('taiga/chicken_coop', (11, 7, 11))
    for x in range(0, 11):
        for z in range(1, 11):
            edge = x in (0, 10) or z in (1, 10)
            if edge:
                if (x, z) == (5, 1):
                    H.gate(b, x, 1, z)
                else:
                    b.set(x, 1, z, 'spruce_fence')
            elif rng.random() < .1:
                b.set(x, 1, z, rng.choice(['short_grass', 'fern']))
    # Coop: 3x3 log hut with a doorway, slab roof and hay nests.
    H.log_walls(b, 6, 6, 9, 9, 1, 2, notch=False)
    b.clear(7, 1, 6, 7, 2, 6)
    for x in range(5, 11):
        for z in range(5, 11):
            b.set(x, 3, z, 'spruce_slab', type='bottom', waterlogged=False, clip=True)
    b.set(8, 1, 7, 'hay_block', axis='y')
    b.set(8, 1, 8, 'hay_block', axis='x')
    b.set(7, 1, 8, 'composter', level=2)
    b.set(6, 2, 7, 'spruce_trapdoor', facing='west', half='top', open=True, powered=False, waterlogged=False)
    b.set(3, 1, 8, 'water_cauldron', level=3)
    b.set(2, 1, 8, 'hay_block', axis='y')
    for x, z in ((3, 4), (4, 6), (2, 3), (6, 3), (7, 4)):
        b.animal(x, 1, z, 'chicken')
    b.animal(3, 1, 5, 'chicken', baby=True)
    b.set(5, 0, 0, 'dirt_path')
    b.set(0, 2, 1, 'lantern', waterlogged=False)
    b.entrance(5)
    b.natural_ground()
    return b


def goat_pen():
    """Fenced pen with mossy rocks for goats to climb, pigs at the trough and a lean-to shelter."""
    rng = random.Random(4305)
    b = Build('taiga/goat_pen', (14, 7, 13))
    for x in range(0, 14):
        for z in range(1, 13):
            edge = x in (0, 13) or z in (1, 12)
            if edge:
                if (x, z) == (6, 1):
                    H.gate(b, x, 1, z)
                else:
                    b.set(x, 1, z, 'spruce_fence')
            elif rng.random() < .08:
                b.set(x, 1, z, rng.choice(['short_grass', 'fern']))
    # Climbing rocks.
    for x, y, z in ((3, 1, 4), (4, 1, 4), (3, 1, 5), (3, 2, 4), (4, 1, 5), (10, 1, 4), (10, 1, 5), (9, 1, 4),
                    (10, 2, 4)):
        b.set(x, y, z, rng.choice(['mossy_cobblestone', 'stone', 'cobblestone', 'mossy_cobblestone']))
    b.set(4, 2, 4, 'mossy_cobblestone_slab', type='bottom', waterlogged=False)
    # Lean-to shelter on log posts.
    for x in (8, 12):
        for y in (1, 2):
            b.set(x, y, 8, 'spruce_log', axis='y')
            b.set(x, y, 11, 'spruce_log', axis='y')
    for x in range(7, 14):
        b.set(x, 3, 8, 'spruce_stairs', facing='south', half='bottom', clip=True)
        for z in (9, 10, 11):
            b.set(x, 3, z, 'spruce_slab', type='top', waterlogged=False, clip=True) if x < 13 else None
    for x in (9, 10, 11):
        b.set(x, 1, 11, 'hay_block', axis='x')
    b.set(11, 2, 11, 'hay_block', axis='y')
    for x in (2, 3, 4):
        b.set(x, 1, 11, 'water_cauldron', level=3)
    for x, z, kind, baby in ((5, 6, 'goat', False), (8, 5, 'goat', False), (6, 4, 'goat', True),
                             (3, 9, 'pig', False), (5, 9, 'pig', False)):
        b.animal(x, 1, z, kind, baby=baby)
    b.set(6, 0, 0, 'dirt_path')
    b.set(6, 0, 1, 'dirt_path')
    b.entrance(6)
    b.natural_ground()
    return b


def apiary():
    """Beehives hung on young spruces and posts among berry bushes and woodland flowers."""
    rng = random.Random(4306)
    b = Build('taiga/apiary', (11, 10, 10))
    for x, z in ((2, 6), (8, 6)):
        H.spruce(b, x, 1, z, height=6, shape=[0, 1, 1, 2, 1])
    b.set(2, 2, 5, 'beehive', facing='north', honey_level=rng.randrange(0, 5))
    b.set(8, 2, 5, 'beehive', facing='north', honey_level=rng.randrange(0, 5))
    for x, z in ((5, 4), (5, 8)):
        b.set(x, 1, z, 'spruce_log', axis='y')
        b.set(x, 2, z, 'beehive', facing='north', honey_level=rng.randrange(0, 5))
        b.set(x, 3, z, 'spruce_slab', type='bottom', waterlogged=False)
    flowers = ['cornflower', 'lily_of_the_valley', 'allium', 'fern', 'oxeye_daisy', 'fern']
    for x in range(0, 11):
        for z in range(1, 10):
            if (x, 1, z) in b.grid or x == 5 and z < 4:
                continue
            r = rng.random()
            if r < .15:
                H.berry_bush(b, x, z, rng)
            elif r < .55:
                b.set(x, 0, z, rng.choice(['grass_block', 'podzol', 'grass_block']))
                b.set(x, 1, z, rng.choice(flowers))
    for z in (0, 1, 2, 3):
        b.set(5, 0, z, 'dirt_path')
    b.set(4, 1, 2, 'barrel', facing='up', open=False)
    b.entrance(5)
    b.natural_ground()
    return b


DESIGNS = {
    'taiga/pumpkin_field': pumpkin_field,
    'taiga/potato_field': potato_field,
    'taiga/berry_patch': berry_patch,
    'taiga/chicken_coop': chicken_coop,
    'taiga/goat_pen': goat_pen,
    'taiga/apiary': apiary,
}
