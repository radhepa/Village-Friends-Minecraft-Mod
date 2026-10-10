"""The village stable: three horse stalls under one roof, a tack corner for the stablehand and a fenced yard.

Stablehand's building (STABLEHAND in the mod). It favours the outer streets (``plains/lots_outer``) like the
paddock. Each stall has a Horse Stall block against the back wall and its own Hay Trough; the Saddle Rack in the
tack corner is the stablehand's workstation. The three horses carry the ``villagefriends.stable_horse`` entity tag:
when they first load, each settles into a free stall nearby, takes a breed the village keeps and becomes the
village's horse (their coats and stats are rolled then, so the template doesn't set them). No beds: the stable is
a workplace, so it stays out of housing.

The other village types build the same stable in their own materials (``buildings/<type>/stable.py`` pass a
``Materials`` to :func:`build`), so a desert village keeps desert horses in a sandstone stable.
"""
import random
from dataclasses import dataclass

from ..kit import Build
from .. import parts
from ..parts import ROOFS, Roof

STALL_X = (2, 6, 10)          # the Horse Stall block in each stall, against the back wall
DIVIDERS = (4, 8, 12)         # fence lines between the stalls (and the tack corner)
FRONT, BACK = 6, 12           # the open front of the stall row and its back wall
HORSE = {'Tame': True, 'Tags': ['villagefriends.stable_horse'], 'equipment': {'saddle': {'id': 'minecraft:saddle', 'count': 1}}}


@dataclass(frozen=True)
class Materials:
    post: str                 # corner and front posts (a log, set upright)
    wall: str                 # back and side walls
    roof: Roof
    gable: str                # the roof's end triangles
    fence: str
    gate: str
    floor: tuple              # the stall row's floor, picked at random per block
    yard: tuple               # the yard's ground, picked at random per block
    plant: str = ''           # an occasional plant in the yard ('' for none)
    pitch: int = 1            # 2 for a steep roof (the template grows to fit)
    log_post: bool = True     # the post block takes an axis


PLAINS = Materials(post='stripped_spruce_log', wall='spruce_planks', roof=ROOFS['spruce'], gable='spruce_planks', fence='spruce_fence',
                   gate='spruce_fence_gate', floor=('coarse_dirt', 'coarse_dirt', 'rooted_dirt', 'packed_mud'), yard=('grass_block',),
                   plant='short_grass')


def build(name, m, seed):
    """Three stalls with troughs, a tack corner with the saddle rack, hay and water, and a fenced yard in front."""
    rng = random.Random(seed)
    b = Build(name, (15, 10 if m.pitch == 1 else 14, 14))
    post = {'axis': 'y'} if m.log_post else {}
    # The stall row's floor: trodden earth under straw.
    for x in range(0, 15):
        for z in range(FRONT, BACK + 1):
            b.set(x, 0, z, rng.choice(m.floor))
    # Back and side walls between posts; the front stands open on posts with a beam across the top.
    for x in range(0, 15):
        for y in (1, 2, 3):
            b.set(x, y, BACK, m.post if x in (0, 4, 8, 12, 14) else m.wall, **(post if x in (0, 4, 8, 12, 14) else {}))
    for x in (0, 14):
        for z in range(FRONT, BACK):
            for y in (1, 2, 3):
                b.set(x, y, z, m.post if z == FRONT else m.wall, **(post if z == FRONT else {}))
    for x in DIVIDERS:
        for y in (1, 2, 3):
            b.set(x, y, FRONT, m.post, **post)
        for z in range(FRONT + 1, BACK):
            b.set(x, 1, z, m.fence)
    for x in range(1, 14):
        if x not in DIVIDERS:
            b.set(x, 3, FRONT, m.post, **({'axis': 'x'} if m.log_post else {}))
    ridge = parts.gable_roof(b, 0, FRONT, 14, BACK, 4, m.roof, axis='x', overhang=1, rake=0, gable=m.gable, pitch=m.pitch)
    assert ridge < b.h, f'{name}: the roof needs a taller template'
    # Each stall: its Horse Stall against the back wall, a trough full of hay beside it, a lantern on a chain from the rafters.
    rafter = 4 + 2 * m.pitch  # the air just under the roof above the middle of each stall
    for x in STALL_X:
        b.custom(x, 1, BACK - 1, 'horse_stall', facing='north')
        b.set(x + 1, 1, BACK - 1, 'villagefriends:hay_trough', facing='north', hay=4)
        parts.lantern(b, x, rafter, BACK - 2, chain=rafter - 3)
    # The tack corner: the stablehand's Saddle Rack, hay bales, a barrel and water.
    b.custom(13, 1, 9, 'saddle_rack', facing='west')
    b.set(13, 1, BACK - 1, 'hay_block', axis='y')
    b.set(13, 2, BACK - 1, 'hay_block', axis='x')
    b.set(13, 1, BACK - 2, 'barrel', facing='up', open=False)
    b.set(13, 1, FRONT + 1, 'water_cauldron', level=3)
    b.resident(13, 1, 8, job='stablehand')
    # The yard in front: open ground behind a fence with a gate on the street side, water and a hay bale for the horses.
    for x in range(0, 15):
        for z in range(1, FRONT):
            edge = x in (0, 14) or z == 1
            if edge:
                if x == 7 and z == 1:
                    b.set(x, 1, z, m.gate, facing='north', open=False, in_wall=False, powered=False)
                else:
                    b.set(x, 1, z, m.fence)
            else:
                b.set(x, 0, z, rng.choice(m.yard))
                if m.plant and rng.random() < .12:
                    b.set(x, 1, z, m.plant)
    b.set(2, 1, 2, 'water_cauldron', level=3)
    b.set(12, 1, 2, 'hay_block', axis='z')
    for x in STALL_X:
        b.animal(x, 1, BACK - 3, 'horse', **HORSE)
    b.set(7, 0, 0, 'dirt_path')
    b.set(7, 0, 1, 'dirt_path')
    b.entrance(7)
    b.natural_ground()
    return b


def stable():
    return build('stable', PLAINS, 611)


DESIGNS = {'stable': stable}
