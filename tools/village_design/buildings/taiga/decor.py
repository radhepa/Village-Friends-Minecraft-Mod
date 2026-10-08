"""Small taiga details that fill gaps between buildings: spruces, log stacks, boulders,
a campfire ring, a drying rack and a carved totem post."""
import random

from ...kit import Build
from ...parts import log
from . import homes_logs as H


def tree_spruce():
    """One tall spruce with a fern and berry skirt."""
    rng = random.Random(4401)
    b = Build('taiga/decor_spruce', (7, 15, 7))
    H.spruce(b, 3, 1, 4, height=11, shape=[0, 1, 1, 2, 1, 2, 1, 2, 3, 2, 3])
    H.undergrowth(b, [(x, z) for x in range(7) for z in range(1, 7)], rng, .3)
    b.set(3, 0, 1, 'podzol')
    b.entrance(3)
    b.natural_ground()
    return b


def spruce_pair():
    """A tall and a young spruce over a mossy log lying in the needles."""
    rng = random.Random(4402)
    b = Build('taiga/decor_spruce_pair', (10, 16, 9))
    H.spruce(b, 3, 1, 5, height=12, shape=[0, 1, 1, 2, 1, 2, 1, 2, 3, 2, 3, 2])
    H.spruce(b, 7, 1, 3, height=7, shape=[0, 1, 1, 2, 1, 2])
    for x in (5, 6, 7, 8):
        b.set(x, 1, 7, log('spruce_log', 'x'))
    b.set(6, 2, 7, 'moss_carpet')
    b.set(7, 2, 7, 'brown_mushroom')
    H.undergrowth(b, [(x, z) for x in range(10) for z in range(1, 9)], rng, .3)
    b.entrance(5)
    b.natural_ground()
    return b


def log_stack():
    """Seasoning firewood under a slab roof, a chopping block and a saw-horse."""
    rng = random.Random(4403)
    b = Build('taiga/decor_log_stack', (7, 5, 6))
    H.woodpile(b, 1, 1, 4, 'x', length=5, height=3)
    b.set(5, 1, 2, 'stripped_spruce_log', axis='y')
    b.set(4, 1, 2, 'spruce_log', axis='x')
    b.set(1, 1, 2, 'spruce_fence')
    b.set(2, 1, 2, 'spruce_fence')
    b.set(1, 2, 2, log('stripped_spruce_log', 'x'))
    b.set(2, 2, 2, log('stripped_spruce_log', 'x'))
    H.undergrowth(b, [(0, z) for z in range(6)] + [(6, z) for z in range(6)], rng, .4)
    b.entrance(3)
    b.natural_ground()
    return b


def boulder():
    """A mossy boulder half sunk into the forest floor."""
    rng = random.Random(4404)
    b = Build('taiga/decor_boulder', (7, 5, 7))
    cells = [(2, 1, 3), (3, 1, 3), (4, 1, 3), (2, 1, 4), (3, 1, 4), (4, 1, 4), (3, 1, 2), (3, 1, 5), (2, 1, 2),
             (3, 2, 3), (3, 2, 4), (2, 2, 3), (4, 2, 4), (3, 3, 3)]
    for x, y, z in cells:
        b.set(x, y, z, rng.choice(['mossy_cobblestone', 'mossy_cobblestone', 'stone', 'cobblestone', 'andesite']))
    for x, y, z in ((3, 4, 3), (2, 3, 3), (4, 3, 4), (3, 3, 4)):
        b.set(x, y, z, 'moss_carpet')
    b.set(4, 2, 3, 'mossy_cobblestone_slab', type='bottom', waterlogged=False)
    b.set(5, 1, 4, 'mossy_cobblestone_stairs', facing='west', half='bottom')
    b.set(1, 1, 3, 'mossy_cobblestone_stairs', facing='east', half='bottom')
    H.undergrowth(b, [(x, z) for x in range(7) for z in range(1, 7)], rng, .35)
    b.entrance(3)
    b.natural_ground()
    return b


def campfire_ring():
    """A stone-ringed fire with log seats around it."""
    rng = random.Random(4405)
    b = Build('taiga/decor_campfire_ring', (9, 4, 9))
    for x in range(2, 7):
        for z in range(3, 8):
            if abs(x - 4) + abs(z - 5) <= 2:
                b.set(x, 0, z, rng.choice(['coarse_dirt', 'podzol', 'gravel']))
    for x, z in ((3, 5), (5, 5), (4, 4), (4, 6)):
        b.set(x, 0, z, rng.choice(['cobblestone', 'mossy_cobblestone']))
    b.set(4, 1, 5, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    b.set(4, 0, 5, 'cobblestone')
    b.set(1, 1, 4, log('stripped_spruce_log', 'z'))
    b.set(1, 1, 5, log('stripped_spruce_log', 'z'))
    b.set(7, 1, 5, log('stripped_spruce_log', 'z'))
    b.set(7, 1, 6, log('stripped_spruce_log', 'z'))
    b.set(4, 1, 8, log('spruce_log', 'x'))
    b.set(5, 1, 8, log('spruce_log', 'x'))
    b.set(3, 1, 2, 'spruce_stairs', facing='north', half='bottom', lock=True)
    b.set(6, 1, 7, 'barrel', facing='up', open=False)
    H.woodpile(b, 7, 1, 2, 'z', length=2, height=1, roofed=False)
    H.undergrowth(b, [(x, z) for x in range(9) for z in range(1, 9)], rng, .2)
    b.set(4, 0, 1, 'dirt_path')
    b.set(4, 0, 2, 'dirt_path')
    b.entrance(4)
    b.natural_ground()
    return b


def drying_rack():
    """Hide-drying frames and a stretching rack."""
    rng = random.Random(4406)
    b = Build('taiga/decor_drying_rack', (8, 5, 5))
    H.drying_rack(b, 1, 2, 1, length=4, hides=('brown', 'white', 'brown', 'light_gray'))
    H.drying_rack(b, 2, 4, 1, length=2, hides=('brown', 'brown'))
    b.set(6, 1, 4, 'barrel', facing='up', open=False)
    b.set(7, 1, 4, 'cauldron')
    H.undergrowth(b, [(x, 1) for x in range(8)] + [(0, 4), (1, 4)], rng, .4)
    b.entrance(3)
    b.natural_ground()
    return b


def totem():
    """A carved totem post: log column with trapdoor wings, a lantern-lit face and spruce antlers."""
    rng = random.Random(4407)
    b = Build('taiga/decor_totem', (5, 9, 5))
    for x in (1, 2, 3):
        for z in (2, 3, 4):
            b.set(x, 0, z, rng.choice(['mossy_cobblestone', 'cobblestone', 'mossy_cobblestone']))
    b.set(2, 1, 3, 'mossy_cobblestone')
    for y in (2, 3, 4):
        b.set(2, y, 3, 'stripped_spruce_log' if y == 3 else 'spruce_log', axis='y')
    b.set(2, 5, 3, 'carved_pumpkin', facing='north')
    b.set(2, 6, 3, 'stripped_spruce_log', axis='y')
    for x, f in ((1, 'west'), (3, 'east')):
        b.set(x, 4, 3, 'spruce_trapdoor', facing=f, half='top', open=True, powered=False, waterlogged=False)
        b.set(x, 6, 3, 'spruce_fence')
        b.set(x, 7, 3, 'spruce_fence')
    b.set(2, 7, 3, 'spruce_fence')
    b.set(1, 1, 2, 'lantern', waterlogged=False)
    H.berry_bush(b, 4, 4, rng)
    H.berry_bush(b, 0, 3, rng)
    b.entrance(2)
    b.natural_ground()
    return b


DESIGNS = {
    'taiga/decor_spruce': tree_spruce,
    'taiga/decor_spruce_pair': spruce_pair,
    'taiga/decor_log_stack': log_stack,
    'taiga/decor_boulder': boulder,
    'taiga/decor_campfire_ring': campfire_ring,
    'taiga/decor_drying_rack': drying_rack,
    'taiga/decor_totem': totem,
}
