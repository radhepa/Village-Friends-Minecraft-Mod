"""Savanna town centres: 33x33 squares built on the shared plaza base.

Slots and exits sit exactly where the plains squares have them (``plazas.base``);
the roles move around the sides like plains. Each centre has its own savanna
centrepiece: the great acacia meeting tree, a thatched market pavilion, or a
watering hole with drinking troughs.
"""
import math
import random

from ..plazas import base, bell_frame, SIZE, C
from ... import parts
from ...kit import is_air
from . import core_parts as cp


def _lawn(b):
    return [(x, z) for x in range(SIZE) for z in range(SIZE) if b.get(x, 0, z)[0] == 'minecraft:grass_block']


def bell(b, x, z, along='x'):
    bell_frame(b, x, z, along=along, log='stripped_acacia_log', stone='mud_bricks', slab='acacia_slab')


def painter_corner(b, x, z, facing='south'):
    """Easel under a small cloth sunshade on four acacia poles."""
    b.custom(x, 1, z, 'easel_canvas', facing=facing)
    for px, pz in ((x - 1, z - 1), (x + 2, z - 1), (x - 1, z + 2), (x + 2, z + 2)):
        for y in (1, 2, 3):
            b.set(px, y, pz, 'acacia_fence')
    for px in range(x - 1, x + 3):
        for pz in range(z - 1, z + 3):
            b.set(px, 4, pz, 'orange_wool' if (px + pz) % 2 else 'white_wool')
    b.set(x + 1, 1, z - 1, 'decorated_pot', facing='south', waterlogged=False, cracked=False)
    b.resident(x + 1, 1, z + 1, 'painter')


def bard_stage(b, x0, z0, facing='north'):
    """A raised acacia stage (5x4) with drums and a thatch canopy; the bard faces ``facing``."""
    for x in range(x0, x0 + 5):
        for z in range(z0, z0 + 4):
            b.set(x, 1, z, 'acacia_slab', type='bottom', waterlogged=False)
    for x, z in ((x0, z0 + 3), (x0 + 4, z0 + 3), (x0, z0), (x0 + 4, z0)):
        b.set(x, 1, z, 'stripped_acacia_log', axis='y')
        for y in (2, 3, 4):
            b.set(x, y, z, 'acacia_fence')
    cp.hip_roof(b, x0, z0, x0 + 4, z0 + 3, 5, cp.THATCH, overhang=1, lip=True)
    b.custom(x0 + 2, 2, z0 + 1, 'music_stand', facing=facing)
    b.resident(x0 + 2, 2, z0 + 2, 'bard')
    # Drums: note blocks and pots along the back.
    b.set(x0 + 1, 2, z0 + 3, 'note_block', instrument='basedrum', note=0, powered=False)
    b.set(x0 + 3, 2, z0 + 3, 'decorated_pot', facing='north', waterlogged=False, cracked=False)
    b.set(x0 + 2, 1, z0 - 1, 'acacia_stairs', facing='south', half='bottom', lock=True)
    parts.lantern(b, x0 + 2, 4, z0 + 2)


def fire_circle(b, x, z):
    b.set(x, 0, z, 'mud_bricks')
    b.set(x, 1, z, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    for dx, dz, f in ((-2, 0, 'east'), (2, 0, 'west'), (0, -2, 'south'), (0, 2, 'north')):
        b.custom(x + dx, 1, z + dz, 'campfire_bench', facing=f)
    for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        b.set(x + dx, 0, z + dz, 'coarse_dirt')


# ------------------------------------------------------------------ meeting tree
def meeting_tree():
    """The great acacia: elders' ring bench under three flat crowns, a fire circle and a bard's stage."""
    roles = {'north': ('garrison', 'library'), 'east': ('tavern', 'market'),
             'south': ('chapel', 'apothecary'), 'west': ('workshop', 'market')}
    b, rng = base('savanna/plaza_meeting_tree', roles, seed=2201, ring=8.5, height=20, prefix='savanna/',
                  paving=cp.paving, lawn='grass_block', ring_block='mud_bricks', plants=False)
    cp.savanna_plants(b, _lawn(b), rng, chance=.35)
    # Grass ring round the tree, edged with a low mud kerb.
    for x in range(SIZE):
        for z in range(SIZE):
            r = math.hypot(x - C - .5, z - C - .5)
            if r <= 4.6:
                b.set(x, 0, z, 'grass_block')
                b.set(x, 1, z, 'air')
                if 2.4 < r and rng.random() < .25:
                    b.set(x, 1, z, 'short_grass')
    cp.great_acacia(b, C, C, rng)
    b.jigsaw(C, 1, C, 'up_north', 'town_start', final='minecraft:acacia_log')
    # Ring bench: backrests against the tree, sitters face the square.
    for x in range(C - 4, C + 6):
        for z in range(C - 4, C + 6):
            r = math.hypot(x - C - .5, z - C - .5)
            if 3.6 <= r < 4.6:
                dx, dz = x - C - .5, z - C - .5
                if abs(dx) >= abs(dz):
                    f = 'east' if dx < 0 else 'west'
                else:
                    f = 'south' if dz < 0 else 'north'
                if (x, z) in ((C - 4, C), (C + 5, C + 1), (C, C + 5), (C + 1, C - 4)):
                    b.set(x, 1, z, 'acacia_trapdoor', facing=f, half='bottom', open=False, powered=False,
                          waterlogged=False)
                else:
                    b.set(x, 1, z, 'acacia_stairs', facing=f, half='bottom', lock=True, shape='straight')
    # Lanterns hang from the crowns.
    for x, z in ((C + 4, C - 3), (C - 4, C + 1), (C + 3, C + 5), (C + 6, C - 5)):
        for y in range(14, 4, -1):
            if not is_air(b.get(x, y, z)) and is_air(b.get(x, y - 1, z)):
                b.set(x, y - 1, z, 'lantern', hanging=True, waterlogged=False)
                break
    # Painter (north-west) and the bard's stage (south-east).
    painter_corner(b, 6, 6)
    bard_stage(b, 23, 24, facing='north')
    for x, f in ((24, 'south'), (26, 'south')):
        b.custom(x, 1, 22, 'village_bench', facing=f)
    # Bell, notice board and benches.
    bell(b, 25, 8, along='z')
    b.custom(13, 1, 4, 'notice_board', facing='south')
    b.set(12, 1, 4, 'acacia_fence')
    b.set(14, 1, 4, 'acacia_fence')
    for x, z, f in ((4, 19, 'east'), (19, 4, 'south'), (28, 13, 'west'), (13, 28, 'north')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    # Fire circle on the south-west lawn, hide racks beside it.
    fire_circle(b, 6, 24)
    cp.drying_rack(b, 4, 28, 'x', 4)
    # Small acacias and grass on the lawns.
    cp.acacia_tree(b, 28, 5, rng, height=4, lean='west', bend=2, radius=2)
    for x, z in ((28, 26), (5, 5), (10, 29), (29, 23)):
        cp.tall_grass(b, x, z)
    # Lantern posts on the mud-brick ring and by the paths.
    for x, z in ((C - 6, C - 6), (C + 7, C - 6), (C - 6, C + 7), (C + 7, C + 7)):
        cp.lamp(b, x, z)
    for x, z in ((10, 3), (29, 10), (22, 29), (3, 22)):
        cp.lamp(b, x, z, base='packed_mud')
    return b


# ------------------------------------------------------------------ market pavilion
def pavilion(b, x0, z0, x1, z1, rng):
    """Open market pavilion: acacia posts on mud plinths under a deep, low thatch roof."""
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        if corner or ((x - x0) % 4 == 0 and facing in ('north', 'south')) or \
                ((z - z0) % 4 == 0 and facing in ('east', 'west')):
            b.set(x, 1, z, 'mud_bricks')
            for y in range(2, 5):
                b.set(x, y, z, 'stripped_acacia_log', axis='y')
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        b.set(x, 5, z, 'stripped_acacia_log', axis='x' if facing in ('north', 'south') else 'z')
        if corner:
            b.set(x, 5, z, 'stripped_acacia_log', axis='y')
    # Cross beams and the roof.
    cx, cz = (x0 + x1) // 2, (z0 + z1) // 2
    for x in range(x0 + 1, x1):
        b.set(x, 5, cz, 'stripped_acacia_log', axis='x')
    for z in range(z0 + 1, z1):
        b.set(cx, 5, z, 'stripped_acacia_log', axis='z')
    top = cp.hip_roof(b, x0, z0, x1, z1, 6, cp.THATCH, overhang=2, lip=True)
    # Central post (the town start) holds up the roof's crown.
    for y in range(2, 6):
        b.set(cx, y, cz, 'stripped_acacia_log', axis='y')
    b.jigsaw(cx, 1, cz, 'up_north', 'town_start', final='minecraft:stripped_acacia_log')
    for x, z in ((cx - 3, cz - 3), (cx + 3, cz - 3), (cx - 3, cz + 3), (cx + 3, cz + 3)):
        parts.lantern(b, x, 5, z)
    return top


def market_pavilion():
    """Market square: a great thatched pavilion of stalls, a pottery yard and a shaded well."""
    roles = {'north': ('workshop', 'apothecary'), 'east': ('chapel', 'market'),
             'south': ('tavern', 'library'), 'west': ('garrison', 'market')}
    b, rng = base('savanna/plaza_market', roles, seed=2202, ring=12.5, height=20, prefix='savanna/',
                  paving=cp.market_paving, lawn='grass_block', ring_block='brown_terracotta', plants=False)
    cp.savanna_plants(b, _lawn(b), rng, chance=.4)
    x0, z0, x1, z1 = C - 6, C - 6, C + 6, C + 6
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, 0, z, 'acacia_planks' if (x + z) % 5 else 'stripped_acacia_log', axis='x')
    pavilion(b, x0, z0, x1, z1, rng)
    # Stalls under the roof: four counters facing out, goods on a central rack.
    goods = [
        ['melon', 'pumpkin', 'hay_block[axis=y]'],
        ['decorated_pot', 'decorated_pot', 'flower_pot'],
        ['orange_wool', 'red_wool', 'yellow_wool'],
        ['barrel[facing=up]', 'dried_kelp_block', 'bee_nest[facing=south]'],
    ]
    for (x, z, f), g in zip(((C - 1, z0 + 1, 'north'), (x1 - 1, C - 1, 'east'), (C + 1, z1 - 1, 'south'),
                             (x0 + 1, C + 1, 'west')), goods):
        dx, dz = {'north': (0, -1), 'south': (0, 1), 'east': (1, 0), 'west': (-1, 0)}[f]
        lx, lz = {'north': (1, 0), 'east': (0, 1), 'south': (-1, 0), 'west': (0, -1)}[f]
        for i in range(3):
            cx, cz = x + lx * i, z + lz * i
            b.set(cx, 1, cz, 'barrel' if i == 1 else 'acacia_planks', **({'facing': 'up', 'open': False} if i == 1 else {}))
            spec = g[i]
            if spec.startswith('decorated_pot'):
                b.set(cx, 2, cz, 'decorated_pot', facing=f, waterlogged=False, cracked=False)
            else:
                b.set(cx, 2, cz, spec)
    for (x, z) in ((C - 2, C - 2), (C + 2, C + 2), (C + 2, C - 2), (C - 2, C + 2)):
        b.barrel(x, 1, z, 'up')
        if (x + z) % 4 == 0:
            b.set(x, 2, z, 'hay_block', axis='y')
        else:
            cp.pot_cluster(b, [(x, z)], y=2)
    cp.pot_cluster(b, [(C - 1, C + 3), (C + 3, C + 1)])
    # Pottery yard (north-east lawn): pots, a kiln-like oven and a seller's mat.
    for x in range(23, 28):
        for z in range(5, 10):
            b.set(x, 0, z, 'packed_mud' if (x + z) % 3 else 'terracotta')
    cp.pot_cluster(b, [(23, 5), (24, 5), (23, 6), (27, 9), (26, 9), (27, 8)])
    b.set(25, 1, 7, 'mud_bricks')
    b.set(25, 2, 7, 'furnace', facing='south', lit=True)
    b.set(25, 3, 7, 'mud_brick_wall')
    for x in (24, 26):
        b.set(x, 1, 7, 'mud_brick_stairs', facing='west' if x == 26 else 'east', half='bottom', lock=True)
    b.set(25, 1, 9, 'orange_carpet')
    b.set(24, 1, 9, 'red_carpet')
    # Shaded water trough on the south-west lawn.
    cp.trough(b, 6, 23, 4, 'x')
    cp.acacia_tree(b, 4, 27, rng, height=4, lean='east', bend=2, radius=3)
    # Painter by the north-west lawn, bard under an acacia on the south-east lawn.
    painter_corner(b, 6, 6)
    cp.acacia_tree(b, 27, 27, rng, height=4, lean='north', bend=2, radius=3)
    b.custom(25, 1, 24, 'music_stand', facing='west')
    b.resident(26, 1, 24, 'bard')
    for z in (22, 26):
        b.custom(23, 1, z, 'village_bench', facing='east')
    b.set(24, 1, 26, 'note_block', instrument='basedrum', note=0, powered=False)
    # Bell, notice board, benches and lights.
    bell(b, 9, 24, along='x')
    b.custom(13, 1, 4, 'notice_board', facing='south')
    for x, z, f in ((4, C, 'east'), (28, C - 3, 'west'), (C + 3, 28, 'north')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    for x, z, f in ((10, 16, 'east'), (22, 18, 'west')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    for x, z in ((4, 4), (28, 4), (28, 21)):
        cp.lamp(b, x, z)
    for x, z in ((C - 8, C - 8), (C + 8, C - 8), (C + 8, C + 8), (C - 8, C + 8)):
        cp.brazier(b, x, z)
    return b


# ------------------------------------------------------------------ watering hole
def watering_hole():
    """A spring-fed watering hole with a totem island, drinking troughs, reeds and shade trees."""
    roles = {'north': ('tavern', 'apothecary'), 'east': ('garrison', 'market'),
             'south': ('workshop', 'library'), 'west': ('chapel', 'market')}
    b, rng = base('savanna/plaza_waterhole', roles, seed=2203, ring=9.5, height=16, prefix='savanna/',
                  paving=cp.paving, lawn='grass_block', ring_block='packed_mud', plants=False)
    cp.savanna_plants(b, _lawn(b), rng, chance=.35)
    water, bank = set(), set()
    for x in range(C - 8, C + 9):
        for z in range(C - 8, C + 9):
            a = math.atan2(z - C, x - C)
            edge = 6.1 + 1.0 * math.sin(3 * a + .7) + .6 * math.sin(5 * a)
            r = math.hypot(x - C, z - C)
            if r <= edge:
                water.add((x, z))
            elif r <= edge + 1.6:
                bank.add((x, z))
    island = {(x, z) for x in range(C - 1, C + 2) for z in range(C - 1, C + 2)}
    for x, z in bank:
        b.set(x, 0, z, rng.choice(['mud', 'coarse_dirt', 'mud', 'clay', 'coarse_dirt', 'grass_block']))
        b.set(x, 1, z, 'air')
    for x, z in water - island:
        b.set(x, 0, z, 'water', level=0)
        b.set(x, 1, z, 'air')
        if rng.random() < .07:
            b.set(x, 1, z, 'lily_pad')
    # Reeds and grass on the banks, sugar cane where it touches water.
    for x, z in sorted(bank):
        wet = any((x + dx, z + dz) in water for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        roll = rng.random()
        if wet and roll < .22 and b.get(x, 0, z)[0] != 'minecraft:mud':
            b.set(x, 0, z, 'grass_block')
            for y in range(1, 2 + int(rng.random() * 2)):
                b.set(x, y, z, 'sugar_cane', age=0)
        elif roll < .3:
            b.set(x, 1, z, 'short_grass')
    # Totem island.
    for x, z in island:
        b.set(x, 0, z, 'mud_bricks' if (x, z) == (C, C) else 'coarse_dirt')
        b.set(x, 1, z, 'air')
    for x, z in island - {(C, C)}:
        if (x + z) % 2:
            b.set(x, 1, z, 'short_grass')
    b.jigsaw(C, 1, C, 'up_north', 'town_start', final='minecraft:mud_bricks')
    b.set(C, 2, C, 'stripped_acacia_log', axis='y')
    b.set(C, 3, C, 'orange_glazed_terracotta', facing='south')
    b.set(C, 4, C, 'stripped_acacia_log', axis='y')
    b.set(C, 5, C, 'red_glazed_terracotta', facing='north')
    b.set(C, 6, C, 'stripped_acacia_log', axis='y')
    for dx, dz, f in ((1, 0, 'east'), (-1, 0, 'west')):
        b.set(C + dx, 6, C + dz, 'acacia_trapdoor', facing=f, half='top', open=True, powered=False, waterlogged=False)
    b.set(C, 7, C, 'lantern', hanging=False, waterlogged=False)
    # A boardwalk out to the island from the south.
    for z in range(C + 2, C + 9):
        if (C, z) in water or (C, z) in bank:
            b.set(C, 0, z, 'acacia_planks')
            b.set(C, 1, z, 'air')
            for x in (C - 1, C + 1):
                if (x, z) in water and z % 2 == 0:
                    b.set(x, 0, z, 'stripped_acacia_log', axis='y')
    # Drinking troughs and hitching rails on the paved ring.
    cp.trough(b, 7, 22, 3, 'z')
    cp.trough(b, 25, 8, 3, 'x')
    # Shade acacias on the lawns.
    cp.acacia_tree(b, 7, 7, rng, height=4, lean='south', bend=2, radius=3)
    cp.acacia_tree(b, 26, 26, rng, height=4, lean='west', bend=2, radius=3, fork=True)
    # Painter (north-east lawn, looking at the water) and bard (south-east, under the tree).
    painter_corner(b, 25, 3, facing='south')
    b.custom(23, 1, 26, 'music_stand', facing='north')
    b.resident(23, 1, 27, 'bard')
    b.set(25, 1, 27, 'note_block', instrument='basedrum', note=0, powered=False)
    for x in (22, 24):
        b.custom(x, 1, 24, 'village_bench', facing='south')
    # Bell on the south-west lawn, notice board by the north slot.
    bell(b, 9, 26, along='x')
    b.custom(13, 1, 4, 'notice_board', facing='south')
    # Benches looking over the water.
    for x, z, f in ((C, C - 9, 'north'), (C - 9, C, 'west'), (C + 9, C, 'east')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    # Lights on the ring.
    for a in range(8):
        ang = math.pi / 8 + a * math.pi / 4
        x, z = round(C + 10.5 * math.cos(ang)), round(C + 10.5 * math.sin(ang))
        if is_air(b.get(x, 1, z)) and b.get(x, 0, z)[0] != 'minecraft:water':
            cp.lamp(b, x, z)
    return b


DESIGNS = {'savanna/plaza_meeting_tree': meeting_tree, 'savanna/plaza_market': market_pavilion,
           'savanna/plaza_waterhole': watering_hole}
