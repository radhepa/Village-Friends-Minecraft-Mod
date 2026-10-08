"""Desert farms and pens. They favour the outer streets (``desert/lots_outer``).

Crops only grow where water reaches them, so every field is laid out around
irrigation channels; cacti stand on their own sand cells with clear sides.
"""
import random

from ...kit import Build
from .homes_kit import awning, palm, cactus, dry_tuft, stand_lamp

RIPE = {'wheat': 7, 'beetroots': 3, 'carrots': 7, 'potatoes': 7}


def crop(b, x, z, kind, rng):
    b.set(x, 0, z, 'farmland', moisture=7)
    ripe = RIPE[kind]
    b.set(x, 1, z, kind, age=ripe if rng.random() < .65 else max(1, ripe - 2))


def farm_irrigated():
    """Wheat and beetroot strips between three stone-lined irrigation channels."""
    rng = random.Random(4101)
    b = Build('desert/farm_irrigated', (15, 6, 13))
    for x in range(0, 15):
        for z in range(1, 13):
            if x in (0, 14) or z in (1, 12):
                b.set(x, 0, z, 'cut_sandstone')
            elif x in (3, 7, 11):
                b.set(x, 0, z, 'water', level=0)
            else:
                crop(b, x, z, 'beetroots' if x in (12, 13) else 'wheat', rng)
    for x in (3, 7, 11):
        b.set(x, 0, 1, 'smooth_sandstone_slab', type='double', waterlogged=False)
        b.set(x, 1, 1, 'cut_sandstone_slab', type='bottom', waterlogged=False)
    b.set(14, 1, 0, 'composter', level=4)
    b.set(13, 1, 0, 'hay_block', axis='x')
    b.set(0, 1, 0, 'hay_block', axis='y')
    b.set(0, 2, 0, 'hay_block', axis='x')
    b.set(7, 0, 0, 'smooth_sandstone')
    b.entrance(7)
    b.natural_ground()
    return b


def farm_melons():
    """Melon beds and beetroot rows either side of a central channel, with a
    shaded corner for the harvest."""
    rng = random.Random(4102)
    b = Build('desert/farm_melons', (13, 6, 11))
    for x in range(0, 13):
        for z in range(1, 11):
            if x in (0, 12) or z in (1, 10):
                b.set(x, 0, z, 'sandstone')
                if (z == 10 or x in (0, 12)) and (x + z) % 3 == 0:
                    b.set(x, 1, z, 'sandstone_wall')
                continue
            if x == 6:
                b.set(x, 0, z, 'water', level=0)
                continue
            if x < 6:
                b.set(x, 0, z, 'farmland', moisture=7)
                if x in (2, 4):
                    b.set(x, 1, z, 'melon_stem', age=rng.randrange(5, 8))
            else:
                crop(b, x, z, 'beetroots' if x < 10 else 'carrots', rng)
    # Ripe melons beside attached stems.
    for x, z, m in ((2, 2, 'west'), (4, 4, 'east'), (2, 6, 'west'), (4, 8, 'east'), (2, 8, 'south')):
        dx = {'west': -1, 'east': 1, 'south': 0}[m]
        dz = 1 if m == 'south' else 0
        b.set(x, 1, z, 'attached_melon_stem', facing=m)
        b.set(x + dx, 0, z + dz, 'farmland', moisture=7)
        b.set(x + dx, 1, z + dz, 'melon')
    b.set(6, 0, 1, 'cut_sandstone')
    b.set(6, 0, 0, 'smooth_sandstone')
    awning(b, 10, 0, 12, 1, 3, colors=('orange', 'white'), posts=[(10, 0), (12, 0)])
    for x, m in ((11, 'melon'), (12, 'melon')):
        b.set(x, 1, 0, m)
    b.entrance(6)
    b.natural_ground()
    return b


def cane_channel():
    """A long irrigation channel lined with sugar cane, a palm at each end."""
    rng = random.Random(4103)
    b = Build('desert/cane_channel', (15, 11, 9))
    for x in range(1, 14):
        b.set(x, 0, 4, 'water', level=0)
        for z in (3, 5):
            b.set(x, 0, z, 'sand')
            if x % 4 != 0:
                h = rng.choice([2, 2, 3])
                for y in range(1, 1 + h):
                    b.set(x, y, z, 'sugar_cane', age=0)
        for z in (2, 6):
            b.set(x, 0, z, 'sandstone' if x % 2 else 'smooth_sandstone')
    for x in (0, 14):
        for z in range(2, 7):
            b.set(x, 0, z, 'cut_sandstone')
    b.set(0, 1, 4, 'cut_sandstone_slab', type='bottom', waterlogged=False)
    b.set(14, 1, 4, 'cut_sandstone_slab', type='bottom', waterlogged=False)
    for x, z, lean in ((1, 7, 'west'), (13, 7, 'east')):
        b.set(x, 0, z, 'sand')
        palm(b, x, 1, z, height=6, lean=lean)
    b.set(8, 1, 1, 'hay_block', axis='x')
    for x in (4, 12):
        dry_tuft(b, x, 1, rng)
    for z in (0, 1):
        b.set(7, 0, z, 'smooth_sandstone')
    b.entrance(7)
    b.natural_ground()
    return b


def cactus_garden():
    """A walled garden of cacti, dead bushes and dry grass around a stone path."""
    rng = random.Random(4104)
    b = Build('desert/cactus_garden', (11, 7, 11))
    for x in range(0, 11):
        for z in range(1, 11):
            edge = x in (0, 10) or z in (1, 10)
            b.set(x, 0, z, 'sand')
            if edge and not (x == 5 and z == 1):
                b.set(x, 1, z, 'sandstone_wall' if (x + z) % 2 else 'smooth_sandstone_slab',
                      **({} if (x + z) % 2 else {'type': 'bottom', 'waterlogged': False}))
    for z in range(0, 10):
        b.set(5, 0, z, 'cut_sandstone' if z % 2 else 'smooth_sandstone')
    for x in range(2, 9):
        b.set(x, 0, 6, 'cut_sandstone' if x % 2 else 'smooth_sandstone')
    spots = [(2, 3, 3), (3, 8, 2), (7, 3, 2), (8, 8, 3), (8, 4, 1), (3, 4, 1)]
    for x, z, h in spots:
        cactus(b, x, z, h, flower=h >= 2 and rng.random() < .6)
    for x, z in ((2, 5), (4, 3), (6, 4), (8, 2), (4, 9), (6, 8), (2, 7), (8, 7)):
        if b.get(x, 1, z)[0] == 'minecraft:air':
            b.set(x, 1, z, rng.choice(['dead_bush', 'short_dry_grass', 'tall_dry_grass']))
    b.set(5, 1, 6, 'sandstone_wall')
    stand_lamp(b, 5, 2, 6)
    b.custom(4, 1, 6, 'village_bench', facing='east')
    b.entrance(5)
    b.natural_ground()
    return b


def camel_pen():
    """Camel corral: acacia rails, a shade canopy over hay and a water trough."""
    rng = random.Random(4105)
    b = Build('desert/camel_pen', (15, 7, 15))
    for x in range(0, 15):
        for z in range(1, 15):
            edge = x in (0, 14) or z in (1, 14)
            if edge:
                if (x, z) == (7, 1):
                    b.set(x, 1, z, 'acacia_fence_gate', facing='north', open=False, in_wall=False, powered=False)
                else:
                    b.set(x, 1, z, 'acacia_fence')
            else:
                b.set(x, 0, z, rng.choice(['sand', 'sand', 'sand', 'coarse_dirt']))
                if rng.random() < .06:
                    dry_tuft(b, x, z, rng)
    for x in (0, 14):
        for z in (1, 14):
            b.set(x, 1, z, 'cut_sandstone')
            b.set(x, 2, z, 'acacia_fence')
    # Shade over the hay at the back.
    awning(b, 8, 10, 13, 13, 4, colors=('orange', 'white'), stripe='z', posts=[(8, 10), (13, 10)])
    for x in (10, 11, 12, 13):
        b.set(x, 1, 13, 'hay_block', axis='x')
    b.set(12, 2, 13, 'hay_block', axis='y')
    for x in (2, 3, 4):
        b.set(x, 0, 13, 'water', level=0)
        b.set(x, 1, 13, 'air')
    for x in (1, 5):
        b.set(x, 0, 13, 'cut_sandstone')
    b.set(7, 1, 7, 'stripped_acacia_log', axis='y')
    b.set(7, 2, 7, 'acacia_fence')
    b.animal(4, 1, 5, 'camel')
    b.animal(10, 1, 6, 'camel')
    b.animal(5, 1, 10, 'camel', baby=True)
    b.set(7, 0, 0, 'smooth_sandstone')
    b.entrance(7)
    b.natural_ground()
    return b


def goat_pen():
    """Goat pen among sandstone boulders, with a shelter and hay."""
    rng = random.Random(4106)
    b = Build('desert/goat_pen', (11, 7, 12))
    for x in range(0, 11):
        for z in range(1, 12):
            edge = x in (0, 10) or z in (1, 11)
            if edge:
                if (x, z) == (5, 1):
                    b.set(x, 1, z, 'acacia_fence_gate', facing='north', open=False, in_wall=False, powered=False)
                else:
                    b.set(x, 1, z, 'acacia_fence')
            else:
                b.set(x, 0, z, rng.choice(['sand', 'coarse_dirt', 'sand']))
    for x, z, h in ((2, 4, 2), (3, 4, 1), (2, 5, 1), (8, 6, 1), (7, 3, 1)):
        for y in range(1, h + 1):
            b.set(x, y, z, rng.choice(['sandstone', 'smooth_sandstone']))
    b.set(3, 2, 4, 'sandstone_slab', type='bottom', waterlogged=False)
    # Lean-to shelter.
    for x, z in ((6, 8), (9, 8)):
        for y in (1, 2):
            b.set(x, y, z, 'stripped_acacia_log', axis='y')
    for x in range(5, 11):
        for z in range(8, 12):
            b.set(x, 3, z, 'acacia_slab', type='bottom', waterlogged=False)
    for x in (7, 8, 9):
        b.set(x, 1, 10, 'hay_block', axis='x')
    b.set(2, 0, 9, 'water', level=0)
    b.set(3, 0, 9, 'water', level=0)
    b.animal(4, 1, 6, 'goat')
    b.animal(7, 1, 5, 'goat')
    b.animal(3, 1, 8, 'goat', baby=True)
    b.set(5, 0, 0, 'smooth_sandstone')
    b.entrance(5)
    b.natural_ground()
    return b


DESIGNS = {'desert/farm_irrigated': farm_irrigated, 'desert/farm_melons': farm_melons,
           'desert/cane_channel': cane_channel, 'desert/cactus_garden': cactus_garden,
           'desert/camel_pen': camel_pen, 'desert/goat_pen': goat_pen}
