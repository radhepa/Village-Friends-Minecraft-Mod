"""Small snowy street-side details: spruces, firewood, a sledge, a snowman, a lamp and bench, an ice sculpture."""
import random

from ...kit import Build
from ... import parts
from . import homes_kit as k


def tree_spruce():
    """One tall snow-dusted spruce with a few ferns at its foot."""
    rng = random.Random(7401)
    b = Build('snowy/tree_spruce', (9, 14, 9))
    k.spruce(b, 4, 1, 5, rng, height=11, radius=3, sparse=.15)
    for x, z in ((1, 7), (7, 2)):
        b.set(x, 1, z, 'fern')
    b.entrance(4)
    b.natural_ground()
    return b


def spruce_grove():
    """A tall and a young spruce together, with a snow-covered stump."""
    rng = random.Random(7402)
    b = Build('snowy/spruce_grove', (11, 12, 10))
    k.spruce(b, 3, 1, 6, rng, height=9, radius=2, sparse=.1)
    k.spruce(b, 8, 1, 4, rng, height=6, radius=2, sparse=.2)
    b.set(8, 1, 8, 'spruce_log', axis='y')
    k.snow(b, 8, 2, 8, 2)
    b.set(6, 1, 8, 'fern')
    b.entrance(5)
    b.natural_ground()
    return b


def firewood():
    """Firewood stacked under a little snowy roof, with a chopping block and a basket barrel."""
    b = Build('snowy/firewood', (7, 6, 6))
    for x in (0, 6):
        for y in (1, 2):
            b.set(x, y, 4, 'spruce_fence')
    k.woodpile(b, 1, 1, 4, along='x', length=5, height=2)
    for x in range(0, 7):
        b.set(x, 3, 4, 'spruce_planks')
        b.set(x, 3, 3, 'spruce_stairs', facing='south', half='bottom')
        b.set(x, 3, 5, 'spruce_stairs', facing='north', half='bottom')
        b.set(x, 4, 4, 'spruce_planks')
        k.snow(b, x, 5, 4, 2)
    k.chopping_block(b, 2, 1, 2)
    b.set(3, 1, 2, 'spruce_log', axis='x')
    b.barrel(5, 1, 2, 'up')
    b.entrance(3)
    b.natural_ground()
    return b


def sledge():
    """A loaded cargo sledge with a lantern pole, parked by the road."""
    b = Build('snowy/sledge', (5, 5, 7))
    for z in (2, 3, 4, 5):
        b.set(1, 1, z, 'spruce_trapdoor', facing='west', half='bottom', open=True, powered=False, waterlogged=False)
        b.set(3, 1, z, 'spruce_trapdoor', facing='east', half='bottom', open=True, powered=False, waterlogged=False)
        b.set(2, 1, z, 'spruce_slab', type='top', waterlogged=False)
    b.set(2, 1, 1, 'spruce_stairs', facing='south', half='top', lock=True)
    b.set(2, 2, 3, 'barrel', facing='up', open=False)
    b.set(2, 2, 4, 'spruce_log', axis='z')
    b.set(2, 2, 5, 'spruce_log', axis='z')
    b.set(2, 3, 4, 'white_carpet')
    b.set(2, 3, 5, 'brown_carpet')
    b.set(2, 2, 2, 'spruce_fence')
    b.set(2, 3, 2, 'lantern', hanging=False, waterlogged=False)
    b.entrance(2)
    b.natural_ground()
    return b


def snowman():
    """A snowman with a pumpkin head, stick arms and a snowball pile."""
    b = Build('snowy/snowman', (5, 5, 5))
    b.set(2, 1, 3, 'snow_block')
    b.set(2, 2, 3, 'snow_block')
    b.set(2, 3, 3, 'carved_pumpkin', facing='north')
    b.set(2, 4, 3, 'spruce_trapdoor', facing='north', half='bottom', open=False, powered=False, waterlogged=False)
    b.set(1, 2, 3, 'spruce_fence')
    b.set(3, 2, 3, 'spruce_fence')
    for x, z, n in ((1, 2, 2), (3, 2, 3), (1, 4, 1), (3, 4, 2), (2, 2, 1)):
        k.snow(b, x, 1, z, n)
    b.entrance(2)
    b.natural_ground()
    return b


def lamp_bench():
    """A lamp post on a stone footing between two benches, with spruce-leaf shrubs."""
    b = Build('snowy/lamp_bench', (5, 6, 4))
    b.set(2, 0, 2, 'cobblestone')
    parts.lamp_post(b, 2, 1, 2, height=3, fence='spruce_fence')
    b.custom(1, 1, 2, 'village_bench', facing='north')
    b.custom(3, 1, 2, 'village_bench', facing='north')
    k.leaf(b, 0, 1, 3)
    k.leaf(b, 4, 1, 3)
    k.snow(b, 0, 2, 3, 2)
    k.snow(b, 4, 2, 3, 1)
    b.entrance(2)
    b.natural_ground()
    return b


def ice_sculpture():
    """A carved ice stag on a stone plinth, lit by two lanterns."""
    b = Build('snowy/ice_sculpture', (7, 8, 7))
    for x in range(1, 6):
        for z in range(2, 6):
            b.set(x, 0, z, 'stone_bricks')
            b.set(x, 1, z, 'stone_brick_slab', type='bottom', waterlogged=False) if x in (1, 5) or z in (2, 5) \
                else b.set(x, 1, z, 'polished_andesite')
    # Legs, body, neck, head and antlers.
    for x in (2, 4):
        b.set(x, 2, 3, 'packed_ice')
        b.set(x, 2, 4, 'packed_ice')
    for x in (2, 3, 4):
        b.set(x, 3, 3, 'packed_ice')
        b.set(x, 3, 4, 'packed_ice')
    b.set(3, 4, 3, 'blue_ice')
    b.set(3, 5, 3, 'blue_ice')
    b.set(3, 5, 2, 'packed_ice')
    b.set(2, 6, 3, 'blue_ice')
    b.set(4, 6, 3, 'blue_ice')
    b.set(1, 7, 3, 'packed_ice')
    b.set(5, 7, 3, 'packed_ice')
    b.set(4, 3, 5, 'packed_ice')
    for x in (1, 5):
        b.set(x, 1, 2, 'stone_bricks')
        b.set(x, 2, 2, 'lantern', hanging=False, waterlogged=False)
    b.entrance(3)
    b.natural_ground()
    return b


DESIGNS = {
    'snowy/tree_spruce': tree_spruce,
    'snowy/spruce_grove': spruce_grove,
    'snowy/firewood': firewood,
    'snowy/sledge': sledge,
    'snowy/snowman': snowman,
    'snowy/lamp_bench': lamp_bench,
    'snowy/ice_sculpture': ice_sculpture,
}
