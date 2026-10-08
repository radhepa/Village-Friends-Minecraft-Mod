"""Small desert street details: date palms, a market cart, a well, a shade canopy,
a potter's pile and a haystack."""
import random

from ...kit import Build
from .homes_kit import awning, palm, dry_tuft, stand_lamp, hang, pot, rug


def palm_single():
    rng = random.Random(5101)
    b = Build('desert/decor_palm', (7, 11, 7))
    b.set(3, 0, 4, 'sand')
    palm(b, 3, 1, 4, height=7, lean='east')
    for x, z in ((1, 5), (5, 3), (2, 2)):
        dry_tuft(b, x, z, rng)
        b.set(x, 0, z, 'sand')
    b.entrance(3)
    b.natural_ground()
    return b


def palm_pair():
    rng = random.Random(5102)
    b = Build('desert/decor_palm_pair', (9, 11, 8))
    for x, z, h, lean in ((2, 5, 6, 'west'), (6, 4, 7, 'north')):
        b.set(x, 0, z, 'sand')
        palm(b, x, 1, z, height=h, lean=lean)
    b.custom(4, 1, 3, 'village_bench', facing='north')
    for x in range(3, 6):
        b.set(x, 0, 3, 'smooth_sandstone')
    b.set(4, 0, 2, 'cut_sandstone')
    dry_tuft(b, 7, 6, rng)
    b.entrance(4)
    b.natural_ground()
    return b


def cart():
    """A market cart under a striped awning, loaded with melons and pots."""
    b = Build('desert/decor_cart', (6, 5, 6))
    for x in (1, 2, 3):
        for z in (2, 3, 4):
            b.set(x, 1, z, 'acacia_slab', type='top', waterlogged=False)
    for z in (2, 4):
        b.set(0, 1, z, 'acacia_trapdoor', facing='west', half='bottom', open=True, powered=False, waterlogged=False)
        b.set(4, 1, z, 'acacia_trapdoor', facing='east', half='bottom', open=True, powered=False, waterlogged=False)
    b.set(1, 2, 3, 'melon')
    b.set(1, 2, 4, 'melon')
    pot(b, 3, 2, 2, 'north')
    b.set(3, 2, 4, 'pumpkin')
    b.set(2, 2, 2, 'yellow_carpet')
    b.set(2, 2, 4, 'orange_carpet')
    for x, z in ((1, 2), (3, 3)):
        if b.get(x, 2, z)[0] == 'minecraft:air':
            b.set(x, 2, z, 'red_carpet')
    b.set(5, 1, 3, 'acacia_fence')
    awning(b, 1, 2, 3, 4, 4, colors=('red', 'white'), stripe='z')
    for x, z in ((1, 2), (3, 4)):
        b.set(x, 3, z, 'acacia_fence')
    b.set(2, 0, 1, 'smooth_sandstone')
    b.set(2, 0, 0, 'smooth_sandstone')
    b.entrance(2)
    b.natural_ground()
    return b


def well():
    """A sandstone well with a pulley beam, water jars and a lantern."""
    b = Build('desert/decor_well', (7, 6, 7))
    for x in range(1, 6):
        for z in range(2, 7):
            b.set(x, 0, z, 'smooth_sandstone' if (x + z) % 2 else 'cut_sandstone')
    for x in range(2, 5):
        for z in range(3, 6):
            if (x, z) == (3, 4):
                b.set(x, 0, z, 'water', level=0)
                b.set(x, 1, z, 'water', level=0)
            else:
                b.set(x, 1, z, 'cut_sandstone' if (x + z) % 2 else 'chiseled_sandstone')
    for x in (2, 4):
        b.set(x, 2, 4, 'sandstone_wall')
        b.set(x, 3, 4, 'sandstone_wall')
    for x in (2, 3, 4):
        b.set(x, 4, 4, 'stripped_acacia_log', axis='x')
    b.set(3, 3, 4, 'iron_chain', axis='y', waterlogged=False)
    hang(b, 3, 2, 4)
    stand_lamp(b, 2, 5, 4)
    pot(b, 1, 1, 6, 'north')
    pot(b, 5, 1, 5, 'west')
    pot(b, 5, 1, 6, 'west')
    b.set(3, 0, 1, 'smooth_sandstone')
    b.set(3, 0, 0, 'smooth_sandstone')
    b.entrance(3)
    b.natural_ground()
    return b


def canopy():
    """A shady sitting spot: striped canopy on posts over a rug, benches and pots."""
    b = Build('desert/decor_canopy', (7, 5, 7))
    for x in range(1, 6):
        for z in range(2, 7):
            b.set(x, 0, z, 'smooth_sandstone' if (x + z) % 2 else 'cut_sandstone')
    awning(b, 1, 2, 5, 6, 4, colors=('cyan', 'white'), posts=[(1, 2), (5, 2), (1, 6), (5, 6)])
    rug(b, 2, 3, 4, 5, 1, 'red', 'orange')
    b.custom(2, 1, 5, 'village_bench', facing='north')
    b.custom(4, 1, 5, 'village_bench', facing='north')
    b.set(3, 1, 4, 'acacia_fence')
    b.set(3, 2, 4, 'white_carpet')
    hang(b, 3, 3, 4)
    pot(b, 1, 1, 4, 'east')
    pot(b, 5, 1, 4, 'west')
    b.set(3, 0, 1, 'smooth_sandstone')
    b.set(3, 0, 0, 'smooth_sandstone')
    b.entrance(3)
    b.natural_ground()
    return b


def pottery():
    """A potter's pile: decorated pots stacked on a sandstone stand, with a kiln."""
    b = Build('desert/decor_pottery', (7, 4, 5))
    for x in range(1, 6):
        b.set(x, 0, 2, 'cut_sandstone')
        b.set(x, 0, 3, 'smooth_sandstone')
    for x, z, f in ((1, 3, 'north'), (2, 3, 'north'), (2, 2, 'west'), (4, 3, 'north'), (5, 2, 'west')):
        pot(b, x, 1, z, f)
    b.set(3, 1, 3, 'smooth_sandstone_slab', type='double', waterlogged=False)
    pot(b, 3, 2, 3, 'north')
    b.set(5, 1, 3, 'furnace', facing='north', lit=True)
    b.set(5, 2, 3, 'cut_sandstone_slab', type='bottom', waterlogged=False)
    b.set(3, 0, 1, 'smooth_sandstone')
    b.set(3, 0, 0, 'smooth_sandstone')
    b.entrance(3)
    b.natural_ground()
    return b


def haystack():
    b = Build('desert/decor_haystack', (6, 5, 5))
    for x, z, y, axis in ((1, 2, 1, 'x'), (2, 2, 1, 'z'), (3, 2, 1, 'y'), (2, 3, 1, 'x'), (1, 3, 1, 'y'),
                          (2, 2, 2, 'y'), (1, 2, 2, 'x'), (4, 3, 1, 'z')):
        b.set(x, y, z, 'hay_block', axis=axis)
    for x in range(0, 6):
        for z in range(1, 5):
            if b.get(x, 1, z)[0] == 'minecraft:air':
                b.set(x, 0, z, 'sand')
    pot(b, 4, 1, 2, 'north')
    b.set(3, 2, 2, 'yellow_carpet')
    b.entrance(2)
    b.natural_ground()
    return b


DESIGNS = {'desert/decor_palm': palm_single, 'desert/decor_palm_pair': palm_pair, 'desert/decor_cart': cart,
           'desert/decor_well': well, 'desert/decor_canopy': canopy, 'desert/decor_pottery': pottery,
           'desert/decor_haystack': haystack}
