"""Small savanna details between buildings: lone acacias, a termite mound, hay, a trough, a cart and a rack."""
import random

from ...kit import Build
from . import homes_parts as hp


def tree_acacia():
    """A lone flat-topped acacia with dry grass at its foot."""
    rng = random.Random(7101)
    b = Build('savanna/decor_tree_acacia', (9, 11, 9))
    hp.acacia_tree(b, 3, 1, 5, rng, height=3, lean='east', lean_len=2, canopy=3.0)
    hp.yard(b, hp.disk(4, 5, 2.2), rng, mix=['coarse_dirt', 'grass_block', 'coarse_dirt'])
    hp.tufts(b, [(x, z) for x in range(9) for z in range(1, 9)], rng, .2)
    b.set(4, 1, 0, 'air')
    b.entrance(4)
    b.natural_ground()
    return b


def tree_acacia_twin():
    """A big acacia with two crowns on forked limbs, shading a stone seat."""
    rng = random.Random(7102)
    b = Build('savanna/decor_tree_acacia_twin', (13, 12, 13))
    hp.acacia_tree(b, 6, 1, 7, rng, height=4, lean='east', lean_len=2, canopy=3.0, second=('west', 3, 2.4))
    hp.yard(b, hp.disk(6, 7, 2.6), rng, mix=['coarse_dirt', 'grass_block', 'coarse_dirt', 'dirt'])
    b.custom(6, 1, 4, 'village_bench', facing='north')
    b.set(4, 1, 5, 'granite')
    hp.tufts(b, [(x, z) for x in range(13) for z in range(1, 13)], rng, .15)
    b.entrance(6)
    b.natural_ground()
    return b


def termite_mound():
    """A tall termite mound of baked earth beside a granite boulder."""
    rng = random.Random(7103)
    b = Build('savanna/decor_termite_mound', (7, 9, 7))
    layers = [(0, 1.6), (1, 1.4), (2, 1.0), (3, 0.8), (4, 0.6), (5, 0.3)]
    for y, r in layers:
        for x, z in hp.disk(2.5, 4, r):
            b.set(x, y, z, rng.choice(['coarse_dirt', 'packed_mud', 'red_sand', 'terracotta', 'coarse_dirt']))
    b.set(2, 6, 4, 'terracotta')
    b.set(3, 6, 4, 'packed_mud')
    b.set(2, 7, 4, 'mud_brick_wall')
    for x, z, y in ((5, 2, 1), (5, 3, 1), (4, 2, 1), (5, 2, 2)):
        b.set(x, y, z, rng.choice(['granite', 'granite', 'polished_granite']))
    b.set(5, 0, 2, 'granite')
    b.set(5, 0, 3, 'granite')
    b.set(4, 0, 2, 'granite')
    hp.tufts(b, [(x, z) for x in range(7) for z in range(1, 7)], rng, .3)
    b.entrance(3)
    b.natural_ground()
    return b


def haystack():
    """A thatched haystack on a log base with a pitchfork-rake (fence) leaning on it."""
    rng = random.Random(7104)
    b = Build('savanna/decor_haystack', (5, 6, 5))
    for x in (1, 2, 3):
        for z in (2, 3, 4):
            b.set(x, 0, z, 'coarse_dirt')
            b.set(x, 1, z, 'hay_block', axis='y')
    for x, z in ((1, 3), (2, 2), (2, 3), (2, 4), (3, 3)):
        b.set(x, 2, z, 'hay_block', axis='y')
    b.set(2, 3, 3, 'hay_block', axis='y')
    b.set(2, 4, 3, 'acacia_fence')
    b.set(4, 1, 3, 'acacia_fence')
    b.entrance(2)
    b.natural_ground()
    return b


def trough():
    """A mud-brick water trough with a bucket post, for passing herds."""
    rng = random.Random(7105)
    b = Build('savanna/decor_trough', (7, 5, 6))
    for x in range(1, 6):
        for z in (2, 3, 4):
            edge = x in (1, 5) or z in (2, 4)
            b.set(x, 0, z, 'mud_bricks')
            b.set(x, 1, z, 'mud_brick_slab' if edge else 'water', **({'type': 'bottom', 'waterlogged': False}
                                                                     if edge else {'level': 0}))
    for x in range(2, 5):
        b.set(x, 1, 3, 'water', level=0)
        b.set(x, 0, 3, 'mud_bricks')
    for x, z in ((0, 3), (6, 3)):
        b.set(x, 1, z, 'acacia_fence')
        b.set(x, 2, z, 'acacia_fence')
    b.set(0, 3, 3, 'lantern', hanging=False, waterlogged=False)
    hp.yard(b, {(x, z) for x in range(7) for z in range(1, 6)}, rng, mix=['mud', 'coarse_dirt', 'grass_block'])
    b.entrance(3)
    b.natural_ground()
    return b


def cart():
    """An acacia ox cart loaded with hay, pots and a barrel."""
    b = Build('savanna/decor_cart', (5, 4, 7))
    for z in (2, 3, 4, 5):
        for x in (1, 2, 3):
            b.set(x, 1, z, 'acacia_slab', type='top', waterlogged=False)
    for z in (3, 4):
        b.set(0, 1, z, 'acacia_trapdoor', facing='west', half='bottom', open=True, powered=False, waterlogged=False)
        b.set(4, 1, z, 'acacia_trapdoor', facing='east', half='bottom', open=True, powered=False, waterlogged=False)
    b.set(1, 2, 4, 'hay_block', axis='z')
    b.set(2, 2, 4, 'hay_block', axis='z')
    b.set(1, 2, 5, 'hay_block', axis='z')
    b.set(3, 2, 5, 'barrel', facing='up', open=False)
    hp.pot(b, 3, 2, 3)
    b.set(2, 1, 1, 'acacia_fence')
    b.entrance(2)
    b.natural_ground()
    return b


def drying_rack():
    """Hides stretched on an acacia rack beside a pile of wood."""
    b = Build('savanna/decor_drying_rack', (7, 5, 5))
    hp.drying_rack(b, 1, 3, 'x', length=5, hides=('brown', 'orange', 'white'), face='north')
    b.set(1, 1, 4, 'acacia_log', axis='x')
    b.set(2, 1, 4, 'acacia_log', axis='x')
    b.set(5, 1, 4, 'water_cauldron', level=2)
    b.entrance(3)
    b.natural_ground()
    return b


DESIGNS = {
    'savanna/decor_tree_acacia': tree_acacia,
    'savanna/decor_tree_acacia_twin': tree_acacia_twin,
    'savanna/decor_termite_mound': termite_mound,
    'savanna/decor_haystack': haystack,
    'savanna/decor_trough': trough,
    'savanna/decor_cart': cart,
    'savanna/decor_drying_rack': drying_rack,
}
