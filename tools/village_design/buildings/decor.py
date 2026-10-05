"""Small street-side details that fill gaps between buildings."""
import random

from ..kit import Build
from .. import parts


def haystack():
    b = Build('decor_haystack', (5, 5, 5))
    for x, z, y, axis in ((1, 2, 1, 'x'), (2, 2, 1, 'z'), (3, 2, 1, 'y'), (2, 3, 1, 'x'), (1, 3, 1, 'y'),
                          (2, 2, 2, 'y'), (1, 2, 2, 'x')):
        b.set(x, y, z, 'hay_block', axis=axis)
    b.set(3, 1, 3, 'barrel', facing='up', open=False)
    b.entrance(2)
    b.natural_ground()
    return b


def cart():
    """A hay cart with spoked trapdoor wheels."""
    b = Build('decor_cart', (5, 4, 6))
    for z in (2, 3, 4):
        b.set(1, 1, z, 'spruce_slab', type='top')
        b.set(2, 1, z, 'spruce_slab', type='top')
        b.set(3, 1, z, 'spruce_slab', type='top')
    for z in (2, 4):
        b.set(0, 1, z, 'spruce_trapdoor', facing='west', half='bottom', open=True)
        b.set(4, 1, z, 'spruce_trapdoor', facing='east', half='bottom', open=True)
    b.set(1, 2, 3, 'hay_block', axis='z')
    b.set(2, 2, 3, 'hay_block', axis='z')
    b.set(2, 2, 4, 'barrel', facing='up', open=False)
    b.set(3, 2, 2, 'pumpkin')
    b.set(2, 1, 1, 'spruce_fence')
    b.set(2, 1, 0, 'air')
    b.entrance(2)
    b.natural_ground()
    return b


def tree_oak():
    rng = random.Random(701)
    b = Build('decor_tree_oak', (7, 10, 7))
    parts.oak_tree(b, 3, 1, 4, rng, height=5, radius=2)
    for x, z in ((1, 6), (5, 6), (2, 5)):
        b.set(x, 1, z, parts.flowers(rng))
    b.entrance(3)
    b.natural_ground()
    return b


def tree_birch():
    rng = random.Random(702)
    b = Build('decor_tree_birch', (7, 10, 7))
    parts.birch_tree(b, 3, 1, 4, rng, height=6)
    b.set(1, 1, 5, 'fern')
    b.set(5, 1, 3, 'short_grass')
    b.entrance(3)
    b.natural_ground()
    return b


def flowerbed():
    rng = random.Random(703)
    b = Build('decor_flowerbed', (7, 3, 5))
    for x in range(0, 7):
        for z in range(1, 5):
            edge = x in (0, 6) or z in (1, 4)
            if edge:
                b.set(x, 0, z, 'stripped_spruce_log', axis='x' if z in (1, 4) else 'z')
            else:
                b.set(x, 0, z, 'rooted_dirt')
                b.set(x, 1, z, parts.flowers(rng))
    b.set(3, 1, 4, 'spruce_fence')
    b.set(3, 2, 4, 'lantern')
    b.entrance(3)
    b.natural_ground()
    return b


def well():
    b = Build('decor_well', (5, 6, 6))
    for x in range(1, 4):
        for z in range(2, 5):
            b.set(x, 0, z, 'cobblestone')
            b.set(x, 1, z, 'water' if (x, z) == (2, 3) else 'mossy_cobblestone' if (x + z) % 2 else 'cobblestone_wall',
                  **({'level': 0} if (x, z) == (2, 3) else {}))
    for x, z in ((1, 2), (3, 2), (1, 4), (3, 4)):
        b.set(x, 1, z, 'cobblestone')
    for z in (2, 4):
        b.set(2, 2, z, 'spruce_fence')
        b.set(2, 3, z, 'spruce_fence')
    for z in range(1, 6):
        b.set(1, 4, z, 'spruce_stairs', facing='east', half='bottom')
        b.set(3, 4, z, 'spruce_stairs', facing='west', half='bottom')
        b.set(2, 4, z, 'spruce_planks' if z in (1, 5) else 'spruce_slab', **({} if z in (1, 5) else {'type': 'top'}))
        b.set(2, 5, z, 'spruce_slab', type='bottom')
    b.set(2, 3, 3, 'chain', axis='y')
    b.set(2, 2, 3, 'lantern', hanging=True)
    b.entrance(2)
    b.natural_ground()
    return b


def lamp_bench():
    b = Build('decor_lamp_bench', (5, 6, 4))
    b.set(2, 0, 2, 'cobblestone')
    parts.lamp_post(b, 2, 1, 2, height=3, fence='spruce_fence')
    b.custom(1, 1, 2, 'village_bench', facing='north')
    b.custom(3, 1, 2, 'village_bench', facing='north')
    parts.bush(b, 0, 1, 3)
    parts.bush(b, 4, 1, 3, 'flowering_azalea_leaves')
    b.entrance(2)
    b.natural_ground()
    return b


def woodpile():
    b = Build('decor_woodpile', (6, 4, 5))
    parts.woodpile(b, 1, 1, 3, 'x', length=4, wood='oak', height=2)
    b.set(4, 1, 1, 'stripped_oak_log', axis='y')
    b.set(1, 1, 1, 'barrel', facing='up', open=False)
    b.entrance(2)
    b.natural_ground()
    return b


DESIGNS = {'decor_haystack': haystack, 'decor_cart': cart, 'decor_tree_oak': tree_oak,
           'decor_tree_birch': tree_birch, 'decor_flowerbed': flowerbed, 'decor_well': well,
           'decor_lamp_bench': lamp_bench, 'decor_woodpile': woodpile}
