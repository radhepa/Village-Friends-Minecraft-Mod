"""Savanna civic buildings that face the town square (one of each per village).

Each reproduces its plains counterpart's function -- the same residents, custom
workstations and enclosed bedrooms -- in savanna architecture: acacia frames,
packed-mud and terracotta walls, low hipped roofs in acacia or thatch with deep
eaves, verandas on posts, flat Sahel-style mud roofs with beam ends, and
stockades. Large slots are up to 17 wide (8 either side of the entrance); small
slots up to 11 wide (5 either side).
"""
import math
import random

from ...kit import Build, DIRS, is_air
from ... import parts
from . import core_parts as cp

LOOT = cp.LOOT


def plaque(b, x, y, z, facing='north'):
    b.custom(x, y, z, 'house_plaque', facing=facing)


def mud_box(b, x0, z0, x1, z1, top, wall='packed_mud', base='mud_bricks', floor='acacia_planks',
            ceiling='acacia_planks', corners=None, plinth=1):
    """Solid-walled room block: plinth to ``plinth``, walls up to ``top - 1`` and a ceiling at ``top``."""
    for y in range(0, plinth + 1):
        for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
            b.set(x, y, z, base)
        b.fill(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, floor if y == plinth else 'dirt')
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        for y in range(plinth + 1, top):
            b.set(x, y, z, corners if (corner and corners) else wall, **({'axis': 'y'} if corner and corners and corners.endswith('_log') else {}))
    if ceiling:
        b.fill(x0, top, z0, x1, top, z1, ceiling)


def band(b, x0, z0, x1, z1, y, old, new):
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        if b.get(x, y, z)[0] == 'minecraft:' + old:
            b.set(x, y, z, new)


def parapet(b, x0, z0, x1, z1, y, wall='mud_brick_wall', block='mud_bricks', pinnacles=None):
    """Crenellated mud parapet; ``pinnacles`` adds taller corner posts capped with a white knob."""
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        b.set(x, y, z, block if (corner or (x + z) % 2 == 0) else wall)
    if pinnacles:
        for x, z in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
            b.set(x, y + 1, z, 'mud_bricks')
            b.set(x, y + 2, z, pinnacles)


def tall_window(b, x, y, z, out, pane='glass_pane', height=2, shutters=True):
    parts.window(b, x, y, z, out, height=height, trim='acacia', shutters=shutters, pane=pane)


def banner_post(b, x, z, color='orange', y=1, height=4):
    for i in range(height):
        b.set(x, y + i, z, 'acacia_fence')
    b.set(x, y + height, z, f'{color}_banner', rotation=0)


# --------------------------------------------------------------------- tavern
def tavern():
    """The Acacia Shade: where the village eats lunch and supper, spends its evenings and hears the bard.

    An open-air boma terrace on the square; a two-storey terracotta hall under a deep thatch with the
    hearth and armchairs, two long trestle tables, a square table, a long bar with stools and room to
    stand, and the bard's dais; a flat-roofed mud kitchen behind with the cook's stove; two guest rooms
    upstairs. 37 seats, 12 of them under the open sky and 4 by the fire.

    Tavern furniture faces the way its sitter faces; stair chairs face their backrest side.
    """
    rng = random.Random(2301)
    b = Build('savanna/tavern', (17, 22, 29))
    _tavern_kitchen(b)
    _tavern_hall(b)
    _tavern_terrace(b, rng)
    _tavern_hearth(b)
    _tavern_common_room(b)
    _tavern_bar(b)
    _tavern_upstairs(b)
    _tavern_yard(b, rng)
    b.entrance(8)
    b.natural_ground()
    return b


def _tavern_hall(b):
    """Hall x1..15, z7..22: orange terracotta below, white above, acacia posts, a deep thatch roof."""
    x0, z0, x1, z1 = 1, 7, 15, 22
    for y in (0, 1):
        for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
            b.set(x, y, z, 'mud_bricks')
        b.fill(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, 'acacia_planks' if y == 1 else 'dirt')
    posts_x, posts_z = {1, 4, 8, 12, 15}, {7, 11, 15, 19, 22}
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        post = x in posts_x if facing in ('north', 'south') else z in posts_z
        for y in range(2, 10):
            if corner or post:
                b.set(x, y, z, 'stripped_acacia_log', axis='y')
            elif y == 6:
                b.set(x, y, z, 'stripped_acacia_log', axis='x' if facing in ('north', 'south') else 'z')
            else:
                b.set(x, y, z, 'orange_terracotta' if y < 6 else 'white_terracotta')
    b.fill(x0 + 1, 6, z0 + 1, x1 - 1, 6, z1 - 1, 'acacia_planks')
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        b.set(x, 10, z, 'stripped_acacia_log', axis='y' if corner else 'x' if facing in ('north', 'south') else 'z')
    b.fill(x0 + 1, 10, z0 + 1, x1 - 1, 10, z1 - 1, 'acacia_planks')
    # A zigzag frieze painted under the upper beam.
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        if b.get(x, 9, z)[0] == 'minecraft:white_terracotta' and (x + z) % 2:
            b.set(x, 9, z, 'brown_terracotta')
    cp.hip_roof(b, x0, z0, x1, z1, 11, cp.THATCH, overhang=1, lip=True)
    # Front: door, windows, sign and banners.
    b.door(8, 2, 7, facing='south', wood='acacia')
    b.set(8, 4, 7, 'chiseled_red_sandstone')
    for x in (3, 5, 11, 13):
        for y in (3, 4):
            b.set(x, y, 7, 'glass_pane')
    for x in (3, 6, 10, 13):
        for y in (7, 8):
            b.set(x, y, 7, 'glass_pane')
    for z in (9, 20):
        for y in (3, 4):
            b.set(15, y, z, 'glass_pane')
    for z in (9, 13, 17, 20):
        for y in (7, 8):
            b.set(1, y, z, 'glass_pane')
            b.set(15, y, z, 'glass_pane')
    for z in (9, 19):
        for y in (3, 4):
            b.set(1, y, z, 'glass_pane')
    for x in (4, 12):
        b.set(x, 5, 6, f'{"orange" if x == 4 else "red"}_wall_banner', facing='north')
    b.set(10, 1, 6, 'villagefriends:house_plaque', nbt={'id': 'villagefriends:house_plaque'}, facing='north')
    # The hearth's mud chimney climbs the outside of the west wall.
    for z in range(12, 17):
        b.set(0, 0, z, 'mud_bricks')
        for y in range(1, 7):
            b.set(0, y, z, 'mud_bricks')
    b.set(0, 7, 12, 'mud_brick_stairs', facing='south', half='bottom')
    b.set(0, 7, 16, 'mud_brick_stairs', facing='north', half='bottom')
    for z in range(13, 16):
        for y in range(7, 11):
            b.set(0, y, z, 'mud_bricks')
    for y in range(11, 17):
        b.set(0, y, 14, 'mud_bricks')
    b.set(0, 17, 14, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    for z in (13, 15):
        b.set(0, 11, z, 'mud_brick_slab', type='bottom', waterlogged=False)


def _tavern_terrace(b, rng):
    """Open-air boma terrace: packed-mud deck, woven fence, two long trestles with benches under the sky."""
    for x in range(1, 16):
        for z in range(1, 7):
            b.set(x, 0, z, 'acacia_planks' if 2 <= x <= 14 and 2 <= z <= 4 and x not in (7, 8, 9) else
                  rng.choice(['packed_mud', 'packed_mud', 'mud_bricks', 'coarse_dirt']))
    for z in range(0, 7):
        b.set(8, 0, z, 'mud_bricks' if z % 2 == 0 else 'packed_mud')
    for x in (7, 9):
        b.set(x, 0, 0, 'packed_mud')
    # Woven fence round the deck, sharpened posts at the corners and by the path.
    for x in range(0, 17):
        if x not in (7, 8, 9):
            b.set(x, 1, 0, 'acacia_fence')
    for z in range(1, 7):
        b.set(0, 1, z, 'acacia_fence')
        b.set(16, 1, z, 'acacia_fence')
    for x in (0, 6, 10, 16):
        b.set(x, 0, 0, 'mud_bricks')
        for y in (1, 2, 3):
            b.set(x, y, 0, 'stripped_acacia_log', axis='y')
        b.set(x, 4, 0, 'lantern', hanging=False, waterlogged=False)
    for x in (6, 10):
        b.set(x, 3, 1, f'{"orange" if x == 6 else "red"}_wall_banner', facing='south')
    # Two trestles of three tables, benches down both sides.
    for x0 in (2, 12):
        for x in range(x0, x0 + 3):
            b.custom(x, 1, 3, 'tavern_table')
            b.custom(x, 1, 2, 'village_bench', facing='south')
            b.custom(x, 1, 4, 'village_bench', facing='north')
    # Pots and grass along the hall front.
    for x in (2, 14):
        b.set(x, 1, 6, 'decorated_pot', facing='north', waterlogged=False, cracked=False)
    for x in (4, 12):
        cp.tall_grass(b, x, 6)


def _tavern_hearth(b):
    """The fireplace in the west wall with two armchairs and a settle before it."""
    for z in range(12, 17):
        for y in range(2, 6):
            b.set(1, y, z, 'mud_bricks')
        b.set(1, 1, z, 'mud_bricks')
        b.set(2, 1, z, 'mud_bricks')
    for z in range(13, 16):
        b.set(1, 2, z, 'air')
        b.set(1, 3, z, 'air')
        b.set(1, 4, z, 'stripped_acacia_log', axis='z')
    b.set(1, 2, 14, 'campfire', lit=True, signal_fire=False, facing='east', waterlogged=False)
    for z in (13, 15):
        b.set(1, 2, z, 'acacia_log', axis='x')
    for z in range(12, 17):
        b.set(2, 4, z, 'acacia_slab', type='top', waterlogged=False)
    b.set(2, 5, 12, 'candle', candles=3, lit=True, waterlogged=False)
    b.set(2, 5, 14, 'decorated_pot', facing='east', waterlogged=False, cracked=False)
    b.set(2, 5, 16, 'orange_candle', candles=2, lit=True, waterlogged=False)
    # A hide rug laid into the floor (wool keeps it walkable).
    for x in (3, 4):
        for z in range(12, 17):
            b.set(x, 1, z, 'orange_wool' if x == 3 and 13 <= z <= 15 else 'brown_wool')
    for z in (13, 15):
        b.custom(3, 2, z, 'fireside_armchair', facing='west')
    b.barrel(3, 2, 14, 'up')
    b.set(3, 3, 14, 'candle', candles=1, lit=True, waterlogged=False)
    for x in (2, 3):
        b.custom(x, 2, 11, 'village_bench', facing='south')
    b.set(2, 2, 17, 'acacia_log', axis='z')
    b.set(2, 3, 17, 'acacia_log', axis='z')
    b.set(3, 2, 17, 'acacia_log', axis='z')


def _tavern_common_room(b):
    """Long trestles, a square table, the bard's dais, beams and lanterns, the stairs up."""
    for z0 in (9, 14):
        for z in range(z0, z0 + 3):
            b.custom(6, 2, z, 'tavern_table')
            b.custom(5, 2, z, 'tavern_chair', facing='east')
            b.custom(7, 2, z, 'tavern_chair', facing='west')
    b.custom(3, 2, 19, 'tavern_table')
    for x, z, f in ((2, 19, 'east'), (4, 19, 'west'), (3, 18, 'south'), (3, 20, 'north')):
        b.custom(x, 2, z, 'tavern_chair', facing=f)
    # The bard's dais in the front corner, with a drum (note block) to play beside.
    for x in (2, 3):
        for z in (8, 9):
            b.set(x, 2, z, 'acacia_planks' if (x, z) != (3, 9) else 'orange_wool')
        b.set(x, 2, 10, 'acacia_slab', type='bottom', waterlogged=False)
    b.set(2, 3, 8, 'note_block', instrument='basedrum', note=0, powered=False)
    b.set(3, 3, 8, 'decorated_pot', facing='south', waterlogged=False, cracked=False)
    b.set(2, 5, 9, 'orange_wall_banner', facing='east')
    b.set(3, 5, 9, 'lantern', hanging=True, waterlogged=False)
    # Beams under the floor above, lanterns hung between them.
    for z in (12, 18):
        for x in range(2, 15):
            if b.get(x, 5, z)[0] == 'minecraft:air':
                b.set(x, 5, z, 'stripped_acacia_log', axis='x')
    for x, z in ((6, 13), (9, 10), (9, 16), (3, 16), (6, 20), (11, 20)):
        b.set(x, 4 if z in (12, 18) else 5, z, 'lantern', hanging=True, waterlogged=False)
    # Stairs up along the back wall.
    parts.stair_run(b, 7, 21, 2, 5, 'east', wood='acacia')
    b.barrel(5, 2, 21, 'north')
    b.set(5, 3, 21, 'hay_block', axis='y')


def _tavern_bar(b):
    """Bar along the east side: an acacia counter with five stools; the keeper's well half a step down."""
    for z in range(10, 19):
        b.set(12, 2, z, 'stripped_acacia_log', axis='z')
    b.set(12, 2, 19, 'stripped_acacia_log', axis='y')
    b.set(12, 3, 19, 'lantern', hanging=False, waterlogged=False)
    for z in (10, 12, 14, 16, 18):
        b.custom(11, 2, z, 'bar_stool', facing='east')
    for z in range(9, 22):
        b.set(13, 1, z, 'acacia_slab', type='bottom', waterlogged=False)
    b.barrel(13, 2, 8, 'west')
    b.barrel(14, 2, 8, 'west')
    b.barrel(14, 3, 8, 'up')
    b.custom(14, 2, 13, 'tap_stand', facing='west')
    b.custom(14, 2, 14, 'drinks_barrel', facing='west')
    for z in (9, 10, 11, 19, 20, 21):
        b.barrel(14, 2, z, 'west')
    for z in (10, 20):
        b.barrel(14, 3, z, 'west')
    b.set(14, 2, 12, 'brewing_stand', has_bottle_0=False, has_bottle_1=False, has_bottle_2=False)
    b.chest(14, 2, 15, 'west')
    b.set(14, 2, 16, 'decorated_pot', facing='west', waterlogged=False, cracked=False)
    b.set(14, 2, 17, 'water_cauldron', level=3)
    b.set(14, 2, 18, 'barrel', facing='up', open=False)
    for z in (10, 11, 12, 19, 20):
        b.set(14, 4, z, 'acacia_trapdoor', facing='west', half='top', open=False, powered=False, waterlogged=False)
    for z, item in ((10, 'candle'), (11, 'potted_cactus'), (12, 'candle'), (19, 'potted_dead_bush')):
        if item == 'candle':
            b.set(14, 5, z, 'candle', candles=3 if z % 2 else 2, lit=True, waterlogged=False)
        else:
            b.set(14, 5, z, item)
    b.set(14, 4, 13, 'orange_wall_banner', facing='west')
    b.set(14, 4, 14, 'red_wall_banner', facing='west')
    b.resident(13, 2, 14, 'tavern_keeper')
    # Serving hatch and door to the kitchen at the end of the well.
    b.set(12, 2, 22, 'acacia_stairs', facing='north', half='top', waterlogged=False, lock=True)
    b.set(12, 3, 22, 'air')
    b.door(13, 2, 22, facing='north', wood='acacia')


def _tavern_kitchen(b):
    """Flat-roofed mud kitchen (x7..15, z22..28): stove and smoker under a hood, pantry, back door."""
    x0, z0, x1, z1 = 7, 22, 15, 28
    for y in (0, 1):
        for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
            b.set(x, y, z, 'mud_bricks')
        b.fill(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, 'packed_mud' if y == 1 else 'dirt')
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        for y in range(2, 6):
            b.set(x, y, z, 'mud_bricks' if corner else 'packed_mud')
    b.fill(x0, 6, z0, x1, 6, z1, 'packed_mud')
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        if z > z0:
            b.set(x, 7, z, 'mud_bricks' if corner or (x + z) % 2 == 0 else 'mud_brick_wall')
    cp.toron(b, x0, z0, x1, z1, 4, every=2)
    for x in (9, 13):
        b.set(x, 3, z1, 'glass_pane')
    b.set(x1, 3, 25, 'glass_pane')
    b.custom(11, 2, 27, 'kitchen_stove', facing='north')
    b.set(12, 2, 27, 'smoker', facing='north', lit=True)
    b.set(10, 2, 27, 'water_cauldron', level=3)
    for x in (11, 12):
        b.set(x, 4, 27, 'mud_bricks')
        b.set(x, 5, 27, 'mud_bricks')
    for y in range(7, 10):
        b.set(11, y, 27, 'mud_bricks')
    b.set(11, 10, 27, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    b.set(9, 2, 23, 'crafting_table')
    b.barrel(14, 2, 23, 'west')
    b.barrel(14, 3, 23, 'west')
    b.barrel(14, 2, 27, 'up')
    b.set(14, 3, 27, 'hay_block', axis='y')
    b.set(14, 2, 25, 'mud_brick_slab', type='double', waterlogged=False)
    b.set(14, 3, 25, 'potted_red_mushroom')
    b.set(13, 2, 27, 'composter', level=4)
    b.set(8, 2, 27, 'decorated_pot', facing='east', waterlogged=False, cracked=False)
    parts.lantern(b, 11, 5, 24)
    b.resident(11, 2, 25, 'cook')
    b.door(7, 2, 25, facing='east', wood='acacia')
    b.set(6, 1, 25, 'mud_brick_stairs', facing='east', half='bottom', lock=True)


def _tavern_upstairs(b):
    """Two guest rooms on the west side; a landing with linen and a window seat on the east."""
    for z in range(8, 22):
        for y in (7, 8, 9):
            b.set(8, y, z, 'acacia_planks')
    for x in range(2, 8):
        for y in (7, 8, 9):
            b.set(x, y, 15, 'acacia_planks')
    b.door(8, 7, 11, facing='east', wood='acacia')
    b.door(8, 7, 18, facing='east', wood='acacia', hinge='right')
    for x in (9, 10):
        b.set(x, 7, 20, 'acacia_fence')
    for name, z0, color in (('guest_room_north', 8, 'orange'), ('guest_room_south', 16, 'red')):
        b.bed(3, 7, z0 + 1, 'west', color)
        b.bed(3, 7, z0 + 4, 'west', color)
        b.chest(2, 7, z0 + 2, 'east', loot=LOOT)
        b.set(2, 7, z0 + 3, 'barrel', facing='up', open=False)
        b.set(2, 8, z0 + 3, 'potted_cactus')
        parts.rug(b, 4, z0 + 2, 6, z0 + 4, 7, 'white', border=color)
        parts.lantern(b, 5, 9, z0 + 3)
        b.room(name, (5, 8, z0 + 3))
    b.barrel(14, 7, 8, 'west')
    b.barrel(14, 7, 9, 'west')
    b.set(14, 8, 8, 'white_wool')
    b.chest(13, 7, 8, 'south')
    b.set(9, 7, 8, 'bookshelf')
    parts.rug(b, 10, 10, 13, 16, 7, 'brown', border='orange')
    parts.lantern(b, 11, 9, 10)
    parts.lantern(b, 11, 9, 16)


def _tavern_yard(b, rng):
    """Back yard by the kitchen door: woodpile, kegs, hay and a shade acacia."""
    for x in range(1, 7):
        for z in range(23, 29):
            if rng.random() < .65:
                b.set(x, 0, z, rng.choice(['coarse_dirt', 'packed_mud', 'dirt_path', 'coarse_dirt']))
    for z in range(25, 26):
        b.set(5, 0, z, 'packed_mud')
    parts.woodpile(b, 1, 1, 23, 'x', length=4, wood='acacia', height=2)
    for x, z in ((1, 27), (2, 27), (1, 26)):
        b.barrel(x, 1, z, 'up')
    b.set(4, 1, 28, 'hay_block', axis='y')
    b.set(3, 1, 28, 'hay_block', axis='x')


# --------------------------------------------------------------------- garrison
def garrison():
    """Boma fort: a sharpened acacia stockade round a training yard, a stilted lookout and mud barracks."""
    rng = random.Random(2302)
    b = Build('savanna/garrison', (17, 16, 23))
    # Barracks along the back (x1..15, z14..21): flat mud roof with a parapet.
    mud_box(b, 1, 14, 15, 21, 6, wall='packed_mud', ceiling='packed_mud', corners='mud_bricks')
    parapet(b, 1, 14, 15, 21, 7, pinnacles='white_terracotta')
    band(b, 1, 14, 15, 21, 5, 'packed_mud', 'orange_terracotta')
    cp.toron(b, 1, 14, 15, 21, 5, every=2)
    for x in (4, 12):
        for y in range(2, 8):
            b.set(x, y, 14, 'mud_bricks')
    for x in (2, 6, 10, 14):
        b.set(x, 3, 21, 'glass_pane')
        b.set(x, 4, 21, 'glass_pane')
    for z in (16, 19):
        b.set(1, 3, z, 'glass_pane')
        b.set(15, 3, z, 'glass_pane')
    b.door(6, 2, 14, facing='south', wood='acacia')
    b.set(6, 1, 13, 'mud_brick_stairs', facing='south', half='bottom', lock=True)
    for x in (5, 7):
        b.set(x, 4, 13, 'wall_torch', facing='north')
    # Office and armoury (x2..7), bunk room (x9..14) behind a partition.
    for z in range(15, 21):
        for y in (2, 3, 4, 5):
            b.set(8, y, z, 'mud_bricks')
    b.door(8, 2, 17, facing='east', wood='acacia')
    b.custom(3, 2, 16, 'command_desk', facing='east')
    parts.chair(b, 2, 2, 16, 'west', wood='acacia')
    b.chest(2, 2, 19, 'east', loot='minecraft:chests/village/village_weaponsmith')
    b.set(2, 2, 20, 'anvil', facing='east')
    b.barrel(7, 2, 20, 'up')
    b.set(4, 2, 20, 'red_banner', rotation=8)
    b.custom(5, 2, 20, 'training_dummy', facing='north')
    parts.lantern(b, 4, 5, 18)
    for x in (10, 12, 14):
        b.bed(x, 2, 19, 'south', 'red')
    b.bed(13, 2, 16, 'north', 'orange')
    b.chest(11, 2, 15, 'south', loot=LOOT)
    b.set(9, 2, 20, 'barrel', facing='up', open=False)
    parts.lantern(b, 11, 5, 17)
    b.room('bunk_room', (11, 3, 17))
    # Stockade round the yard, with a gate on the square.
    cells = [(x, 0) for x in range(0, 17) if x not in (7, 8, 9)]
    cells += [(0, z) for z in range(1, 14)] + [(16, z) for z in range(1, 14)]
    cp.stockade(b, cells, h=4)
    for x in (6, 10):
        for y in range(1, 7):
            b.set(x, y, 0, 'stripped_acacia_log', axis='y')
        b.set(x, 7, 0, 'acacia_fence')
        b.set(x, 4, 1, 'red_wall_banner', facing='south')
    for x in range(6, 11):
        b.set(x, 6, 0, 'stripped_acacia_log', axis='x')
    for x in range(5, 12):
        b.set(x, 7, 0, 'acacia_slab', type='bottom', waterlogged=False)
    b.set(8, 7, 0, 'hay_block', axis='x')
    b.set(8, 5, 0, 'lantern', hanging=True, waterlogged=False)
    for x in (7, 8, 9):
        b.set(x, 0, 0, 'packed_mud')
    # Yard ground.
    for x in range(1, 16):
        for z in range(1, 14):
            r = rng.random()
            b.set(x, 0, z, 'coarse_dirt' if r < .5 else 'dirt_path' if r < .85 else 'gravel' if r < .95 else 'red_sand')
    for z in range(1, 14):
        b.set(8, 0, z, 'packed_mud')
    # Stilted lookout in the north-east corner.
    tx0, tz0, tx1, tz1 = 12, 2, 15, 5
    for x, z in ((tx0, tz0), (tx1, tz0), (tx0, tz1), (tx1, tz1)):
        b.set(x, 0, z, 'mud_bricks')
        for y in range(1, 10):
            b.set(x, y, z, 'acacia_log', axis='y')
    for x in range(tx0, tx1 + 1):
        for z in range(tz0, tz1 + 1):
            b.set(x, 6, z, 'acacia_planks' if (x, z) not in ((tx0, tz0), (tx1, tz0), (tx0, tz1), (tx1, tz1)) else 'acacia_log', axis='y')
    for x in range(tx0, tx1 + 1):
        for z in range(tz0, tz1 + 1):
            if (x in (tx0, tx1) or z in (tz0, tz1)) and is_air(b.get(x, 7, z)):
                b.set(x, 7, z, 'acacia_fence')
    b.set(tx0, 7, tz1, 'air')
    for y in range(1, 8):
        b.set(tx0, y, tz1 + 1, 'ladder', facing='south')
    b.set(tx0, 7, tz1, 'acacia_log', axis='y')
    b.set(tx0 + 1, 7, tz1, 'air')
    for x, z in ((tx0 - 1, tz0 + 1), (tx0 - 1, tz0 + 2)):
        b.set(x, 5, z, 'acacia_stairs', facing='east', half='top', lock=True)
    cp.hip_roof(b, tx0, tz0, tx1, tz1, 10, cp.THATCH, overhang=1, lip=True)
    b.set(tx0 + 1, 9, tz0 + 1, 'lantern', hanging=True, waterlogged=False)
    # Training yard.
    for x, z in ((3, 4), (3, 7), (6, 5)):
        b.custom(x, 1, z, 'training_dummy', facing='south')
    b.custom(1, 1, 10, 'archery_target', facing='east')
    b.custom(1, 1, 11, 'archery_target', facing='east')
    for x, z in ((14, 10), (15, 10), (15, 11)):
        b.set(x, 1, z, 'hay_block', axis='y')
    b.set(15, 2, 10, 'hay_block', axis='x')
    b.set(10, 1, 11, 'grindstone', face='floor', facing='north')
    b.barrel(11, 1, 11, 'up')
    b.set(12, 1, 11, 'smithing_table')
    for x in (10, 12):
        b.set(x, 1, 12, 'acacia_fence')
    cp.trough(b, 3, 12, 3, 'x')
    plaque(b, 7, 1, 12)
    for x, z in ((2, 2), (14, 8)):
        cp.brazier(b, x, z)
    b.resident(5, 1, 9, 'knight')
    b.resident(4, 1, 11, 'archer')
    b.entrance(8)
    b.natural_ground()
    return b


# --------------------------------------------------------------------- workshop
def workshop():
    """Tailor's terracotta house behind a cloth-hung veranda, and the carpenter's open thatch shed."""
    rng = random.Random(2303)
    b = Build('savanna/workshop', (17, 14, 20))
    # Tailor's house (x1..9, z7..16).
    mud_box(b, 1, 7, 9, 16, 6, wall='white_terracotta', ceiling='acacia_planks', corners='stripped_acacia_log')
    for x in (5,):
        for y in range(2, 6):
            b.set(x, y, 16, 'stripped_acacia_log', axis='y')
    for z in (11,):
        for y in range(2, 6):
            b.set(1, y, z, 'stripped_acacia_log', axis='y')
            b.set(9, y, z, 'stripped_acacia_log', axis='y')
    for x, z, facing, corner in parts.ring(1, 7, 9, 16):
        if b.get(x, 2, z)[0] == 'minecraft:white_terracotta':
            b.set(x, 2, z, 'orange_terracotta')
        if b.get(x, 5, z)[0] == 'minecraft:white_terracotta' and (x + z) % 2:
            b.set(x, 5, z, 'brown_terracotta')
    cp.hip_roof(b, 1, 7, 9, 16, 7, cp.THATCH, overhang=1, lip=True)
    b.door(5, 2, 7, facing='south', wood='acacia')
    for x in (3, 7):
        b.set(x, 3, 7, 'glass_pane')
        b.set(x, 4, 7, 'glass_pane')
    tall_window(b, 1, 3, 9, 'west')
    tall_window(b, 1, 3, 14, 'west', height=1)
    tall_window(b, 9, 3, 9, 'east')
    # Veranda across the front with hanging cloth.
    cp.veranda(b, 1, 9, 4, 6, 1, 6, roof=cp.ACACIA, posts=4, side='north')
    for x in range(1, 10):
        b.set(x, 0, 4, 'mud_bricks')
    for x in (5,):
        b.set(x, 1, 3, 'mud_brick_stairs', facing='south', half='bottom', lock=True)
    b.set(2, 2, 5, 'loom', facing='east')
    b.custom(8, 2, 5, 'village_bench', facing='west')
    # Inside: the tailor's shop at the front, bedroom behind a partition.
    b.custom(3, 2, 10, 'sewing_table', facing='east')
    b.set(2, 2, 8, 'loom', facing='east')
    for z, c in zip(range(8, 12), ['orange', 'red', 'yellow', 'lime']):
        b.set(8, 2, z, f'{c}_wool')
        b.set(8, 3, z, f'{c}_carpet')
    parts.rug(b, 4, 9, 6, 10, 2, 'yellow', border='orange')
    b.chest(2, 2, 11, 'east', loot=LOOT)
    parts.lantern(b, 5, 5, 9)
    b.resident(4, 2, 9, 'tailor')
    for x in range(2, 9):
        for y in (2, 3, 4, 5):
            b.set(x, y, 12, 'acacia_planks')
    b.door(5, 2, 12, facing='south', wood='acacia')
    b.bed(3, 2, 14, 'south', 'orange')
    b.bed(7, 2, 14, 'south', 'light_blue')
    b.chest(5, 2, 15, 'north', loot=LOOT)
    b.set(2, 2, 13, 'decorated_pot', facing='east', waterlogged=False, cracked=False)
    parts.lantern(b, 5, 5, 14)
    b.room('bedroom', (5, 3, 14))
    # Carpenter's open shed (x11..15, z5..15) under a low thatch roof.
    for x, z in ((11, 5), (15, 5), (11, 10), (15, 10), (11, 15), (15, 15)):
        b.set(x, 0, z, 'mud_bricks')
        for y in range(1, 5):
            b.set(x, y, z, 'stripped_acacia_log', axis='y')
    for z in (5, 10, 15):
        for x in range(12, 15):
            b.set(x, 4, z, 'stripped_acacia_log', axis='x')
    for x in (11, 15):
        for z in range(6, 15):
            if z != 10:
                b.set(x, 4, z, 'stripped_acacia_log', axis='z')
    cp.hip_roof(b, 11, 5, 15, 15, 5, cp.THATCH, overhang=1, lip=True)
    for x in range(11, 16):
        for z in range(5, 16):
            b.set(x, 0, z, 'acacia_planks' if (x + z) % 4 else 'stripped_acacia_log', axis='x')
    b.custom(13, 1, 8, 'sawmill', facing='west')
    b.set(13, 1, 12, 'crafting_table')
    for z in range(6, 10):
        for y in (1, 2):
            if not (y == 2 and z in (6, 9)):
                b.set(14, y, z, 'acacia_log', axis='z')
    for x in (12, 13, 14):
        b.set(x, 1, 14, 'acacia_planks')
    b.set(12, 2, 14, 'acacia_slab', type='bottom', waterlogged=False)
    b.set(12, 1, 11, 'acacia_fence')
    b.barrel(14, 1, 11, 'up')
    b.set(13, 4, 10, 'stripped_acacia_log', axis='x')
    b.set(13, 3, 10, 'lantern', hanging=True, waterlogged=False)
    b.resident(12, 1, 10, 'carpenter')
    # Front yard: dye vats and cloth drying on a rack.
    for x, c in ((11, 'orange'), (12, 'red'), (13, 'yellow')):
        b.set(x, 1, 2, 'water_cauldron', level=3)
    b.set(14, 1, 2, 'barrel', facing='up', open=False)
    cp.drying_rack(b, 1, 1, 'x', 4, hides=('red', 'orange', 'yellow'))
    for z in range(0, 4):
        b.set(8, 0, z, 'packed_mud')
    for x in range(5, 8):
        b.set(x, 0, 3, 'packed_mud')
    for x in range(11, 16):
        b.set(x, 0, 4, 'packed_mud')
    plaque(b, 7, 1, 2)
    b.entrance(8)
    b.natural_ground()
    return b


# --------------------------------------------------------------------- chapel
def grave(b, x, z, rng):
    """A cairn of mud and stones with a marker post."""
    b.set(x, 0, z, 'coarse_dirt')
    b.set(x, 0, z + 1, 'coarse_dirt')
    kind = rng.random()
    if kind < .5:
        b.set(x, 1, z, 'mud_brick_wall')
        b.set(x, 1, z + 1, 'mud_brick_slab', type='bottom', waterlogged=False)
    else:
        b.set(x, 1, z, 'stripped_acacia_log', axis='y')
        b.set(x, 2, z, 'acacia_fence')
        b.set(x, 1, z + 1, 'dead_bush' if kind > .8 else 'short_dry_grass')


def chapel():
    """Sahel mud chapel: ribbed walls bristling with beam ends, a tapering bell tower and a cairn yard."""
    rng = random.Random(2304)
    b = Build('savanna/chapel', (17, 22, 24))
    # Nave (x3..13, z7..20) with a flat roof and crenellated parapet.
    mud_box(b, 3, 7, 13, 20, 7, wall='packed_mud', base='mud_bricks', floor='acacia_planks',
            ceiling='packed_mud', corners='mud_bricks')
    parapet(b, 3, 7, 13, 20, 8)
    # Buttress ribs rise above the parapet; beam ends between them.
    for z in (9, 12, 15, 18):
        for x in (2, 14):
            for y in range(0, 9):
                b.set(x, y, z, 'mud_bricks')
            b.set(x, 9, z, 'mud_brick_wall')
            b.set(x, 10, z, 'white_terracotta')
    for x in (5, 8, 11):
        for y in range(0, 9):
            b.set(x, y, 21, 'mud_bricks')
        b.set(x, 9, 21, 'mud_brick_wall')
    cp.toron(b, 3, 7, 13, 20, 4, every=2)
    cp.toron(b, 3, 7, 13, 20, 6, every=2)
    # Tall slit windows of amber glass.
    for z in (10, 13, 16):
        for x, out in ((3, 'west'), (13, 'east')):
            for y in (3, 4, 5):
                b.set(x, y, z, 'orange_stained_glass_pane' if y < 5 else 'yellow_stained_glass_pane')
            dx = -1 if out == 'west' else 1
            if is_air(b.get(x + dx, 4, z)):
                pass
    for x in (7, 8, 9):
        for y in (3, 4, 5, 6):
            if not (y == 6 and x != 8):
                b.set(x, y, 20, 'red_stained_glass_pane' if x == 8 else 'orange_stained_glass_pane')
    # Bell tower over the entrance (x6..10, z3..7), sharing the nave's front wall.
    tx0, tz0, tx1, tz1 = 6, 3, 10, 7
    for y in range(0, 16):
        for x in range(tx0, tx1 + 1):
            for z in range(tz0, tz1 + 1):
                edge = x in (tx0, tx1) or z in (tz0, tz1)
                corner = x in (tx0, tx1) and z in (tz0, tz1)
                if y <= 1 and not edge:
                    b.set(x, y, z, 'acacia_planks' if y == 1 else 'dirt')
                elif edge and (y <= 10 or corner or y in (14, 15)):
                    b.set(x, y, z, 'mud_bricks' if corner or y <= 1 else 'packed_mud')
                elif not edge and y == 10:
                    b.set(x, y, z, 'acacia_planks')
                elif edge and y == 11:
                    b.set(x, y, z, 'mud_brick_slab', type='bottom', waterlogged=False)
                elif edge and y == 13:
                    b.set(x, y, z, 'mud_brick_slab', type='top', waterlogged=False)
    b.fill(tx0, 14, tz0, tx1, 14, tz1, 'mud_bricks')
    b.fill(tx0, 15, tz0, tx1, 15, tz1, 'packed_mud')
    parapet(b, tx0, tz0, tx1, tz1, 16, pinnacles='white_terracotta')
    for x in range(tx0 + 1, tx1):
        for z in range(tz0 + 1, tz1):
            b.set(x, 16, z, 'packed_mud')
    b.set(8, 17, 5, 'mud_bricks')
    b.set(8, 18, 5, 'mud_brick_wall')
    b.set(8, 19, 5, 'white_terracotta')
    b.set(8, 20, 5, 'lightning_rod', facing='up', powered=False)
    b.set(8, 12, 5, 'bell', attachment='ceiling', facing='north', powered=False)
    for x, z, f in ((8, tz0 - 1, 'north'), (tx0 - 1, 5, 'west'), (tx1 + 1, 5, 'east')):
        for y in (4, 8):
            b.set(x, y, z, 'acacia_fence')
    for y in range(2, 10):
        for x in (tx0 - 1, tx1 + 1):
            if y <= 9:
                b.set(x, y, tz0, 'mud_bricks')
    for x in (tx0 - 1, tx1 + 1):
        b.set(x, 0, tz0, 'mud_bricks')
        b.set(x, 1, tz0, 'mud_bricks')
        b.set(x, 10, tz0, 'white_terracotta')
    b.door(8, 2, tz0, facing='south', wood='acacia')
    b.set(8, 4, tz0, 'chiseled_red_sandstone')
    b.set(7, 4, tz0, 'red_sandstone_stairs', facing='east', half='top', lock=True)
    b.set(9, 4, tz0, 'red_sandstone_stairs', facing='west', half='top', lock=True)
    b.set(8, 1, tz0 - 1, 'mud_brick_stairs', facing='south', half='bottom', lock=True)
    b.set(8, 0, tz0 - 1, 'mud_bricks')
    b.door(8, 2, tz1, facing='south', wood='acacia')
    for x in (7, 9):
        b.set(x, 7, tz0, 'orange_stained_glass_pane')
    parts.lantern(b, 8, 9, 5)
    # Interior: pews, aisle, altar with the brewing stand and candles.
    for z in (10, 12, 14, 16):
        for x in (4, 5, 6, 10, 11, 12):
            b.set(x, 2, z, 'acacia_stairs', facing='north', half='bottom', lock=True, shape='straight')
    for z in range(9, 18):
        b.set(8, 2, z, 'orange_carpet' if z % 2 else 'red_carpet')
    for x in range(5, 12):
        b.set(x, 1, 18, 'stripped_acacia_log', axis='x')
        b.set(x, 1, 19, 'stripped_acacia_log', axis='x')
    b.set(8, 2, 19, 'chiseled_red_sandstone')
    b.set(7, 2, 19, 'mud_brick_slab', type='top', waterlogged=False)
    b.set(9, 2, 19, 'mud_brick_slab', type='top', waterlogged=False)
    b.set(8, 3, 19, 'candle', candles=3, lit=True, waterlogged=False)
    b.set(7, 3, 19, 'brewing_stand')
    b.set(9, 3, 19, 'orange_candle', candles=2, lit=True, waterlogged=False)
    for x in (4, 12):
        b.set(x, 2, 19, 'decorated_pot', facing='north', waterlogged=False, cracked=False)
    for z in (9, 13, 17):
        parts.lantern(b, 8, 6, z)
    for x, z in ((4, 8), (12, 8)):
        b.set(x, 2, z, 'potted_acacia_sapling')
    # Cairn yard on the flanks behind a low mud wall.
    for z in range(9, 20, 3):
        grave(b, 0, z, rng)
        grave(b, 16, z, rng)
    for x in range(0, 17):
        b.set(x, 1, 23, 'mud_brick_wall' if x % 4 else 'mud_bricks')
    for z in range(8, 23):
        if b.get(0, 1, z)[0] == 'minecraft:air' and z % 3 == 1:
            pass
    cp.acacia_tree(b, 1, 3, rng, height=4, lean='east', bend=2, radius=2)
    # Front court: path, braziers, beds of grass.
    for z in range(0, 2):
        b.set(8, 0, z, 'mud_bricks' if z % 2 else 'packed_mud')
        b.set(7, 0, z, 'packed_mud')
        b.set(9, 0, z, 'packed_mud')
    for x in (5, 11):
        cp.brazier(b, x, 1)
    cp.tall_grass(b, 13, 2)
    cp.tall_grass(b, 3, 6)
    b.entrance(8)
    b.natural_ground()
    return b


# --------------------------------------------------------------------- apothecary
def apothecary():
    """Healer's rondavel: round mud hut under a stepped thatch cone, herb garden and drying rack in front."""
    rng = random.Random(2305)
    b = Build('savanna/apothecary', (11, 14, 17))
    cx, cz, r = 5, 10, 4.6
    inside, wall = set(), set()
    for x in range(11):
        for z in range(17):
            d = math.hypot(x - cx, z - cz)
            if d <= r - 1:
                inside.add((x, z))
            elif d <= r:
                wall.add((x, z))
    for x, z in inside | wall:
        b.set(x, 0, z, 'mud_bricks' if (x, z) in wall else 'dirt')
        b.set(x, 1, z, 'mud_bricks' if (x, z) in wall else 'acacia_planks')
    for x, z in wall:
        for y in range(2, 6):
            b.set(x, y, z, 'packed_mud')
        b.set(x, 4, z, 'orange_terracotta' if (x + z) % 2 else 'white_terracotta')
    for x, z in ((cx - 4, cz), (cx + 4, cz), (cx, cz + 4)):
        for y in range(1, 6):
            b.set(x, y, z, 'stripped_acacia_log', axis='y')
    for x, z in inside | wall:
        b.set(x, 6, z, 'acacia_planks')
    cp.cone_roof(b, cx, cz, 6, 4, mat='hay_block', cap='bamboo_mosaic_slab')
    # Door, windows and a little porch canopy.
    b.door(cx, 2, cz - 4, facing='south', wood='acacia')
    for x in (cx - 1, cx, cx + 1):
        b.set(x, 1, cz - 5, 'mud_brick_slab', type='bottom', waterlogged=False) if x != cx else \
            b.set(x, 1, cz - 5, 'mud_brick_stairs', facing='south', half='bottom', lock=True)
    for x, z, out in ((cx - 4, cz - 2, 'west'), (cx + 4, cz - 2, 'east'), (cx + 3, cz + 3, 'east')):
        b.set(x, 3, z, 'glass_pane')
    # Infirmary (front) and the healer's bedroom (back) behind a partition.
    for x in range(2, 9):
        for y in (2, 3, 4, 5):
            if (x, 11) in inside:
                b.set(x, y, 11, 'acacia_planks')
    b.door(cx, 2, 11, facing='south', wood='acacia')
    b.custom(2, 2, 9, 'alchemical_press', facing='east')
    b.set(2, 2, 10, 'brewing_stand')
    b.set(3, 2, 8, 'water_cauldron', level=2)
    b.custom(8, 2, 9, 'apothecary_cot', facing='west')
    b.custom(7, 2, 7, 'apothecary_cot', facing='west')
    b.set(8, 2, 10, 'barrel', facing='up', open=False)
    parts.lantern(b, cx, 5, 8)
    b.resident(4, 2, 9, 'apothecary')
    b.bed(3, 2, 12, 'south', 'lime')
    b.chest(7, 2, 13, 'west', loot=LOOT)
    b.set(4, 2, 13, 'potted_cactus')
    b.set(7, 2, 12, 'potted_red_mushroom')
    parts.lantern(b, cx, 5, 13)
    b.room('apothecary_bedroom', (cx, 3, 13))
    # Herb garden and a drying rack.
    for x in range(0, 11):
        for z in range(0, 5):
            if x in (4, 5, 6) or (x, z) in wall or (x, z) in inside:
                continue
            if z == 0 or x in (0, 10):
                continue
            b.set(x, 0, z, 'coarse_dirt' if (x + z) % 3 == 0 else 'rooted_dirt')
            plant = rng.choice(['sweet_berry_bush', 'short_grass', 'red_mushroom', 'dandelion', 'orange_tulip',
                                'bush', 'short_dry_grass'])
            if plant == 'sweet_berry_bush':
                b.set(x, 1, z, plant, age=2)
            elif plant == 'red_mushroom':
                b.set(x, 0, z, 'podzol')
                b.set(x, 1, z, plant)
            else:
                b.set(x, 1, z, plant)
    for z in range(0, 5):
        b.set(cx, 0, z, 'packed_mud' if z % 2 else 'coarse_dirt')
    cp.drying_rack(b, 7, 3, 'x', 3, hides=('green', 'lime', 'brown'))
    plaque(b, 3, 1, 4)
    b.set(1, 1, 4, 'decorated_pot', facing='north', waterlogged=False, cracked=False)
    b.set(6, 1, 4, 'lantern', hanging=False, waterlogged=False)
    b.entrance(cx)
    b.natural_ground()
    return b


# --------------------------------------------------------------------- library
def library():
    """Manuscript house: thick mud walls with beam ends, a flat roof terrace and a thatched reading shade."""
    rng = random.Random(2306)
    b = Build('savanna/library', (11, 15, 17))
    mud_box(b, 1, 4, 9, 14, 6, wall='mud_bricks', base='mud_bricks', floor='acacia_planks', ceiling='packed_mud',
            corners='mud_bricks')
    for x, z, facing, corner in parts.ring(1, 4, 9, 14):
        for y in (2, 3, 4, 5):
            if not corner and (x + y + z) % 5 == 0:
                b.set(x, y, z, 'packed_mud')
    parapet(b, 1, 4, 9, 14, 7, pinnacles='white_terracotta')
    cp.toron(b, 1, 4, 9, 14, 3, every=2)
    cp.toron(b, 1, 4, 9, 14, 6, every=2)
    b.set(5, 3, 3, 'air')
    # Carved doorway and narrow windows.
    b.door(5, 2, 4, facing='south', wood='acacia')
    for y in range(2, 5):
        for x in (4, 6):
            b.set(x, y, 3, 'cut_red_sandstone' if y < 4 else 'chiseled_red_sandstone')
    b.set(5, 4, 3, 'red_sandstone_slab', type='top', waterlogged=False)
    b.set(5, 5, 4, 'chiseled_red_sandstone')
    b.set(5, 1, 3, 'mud_brick_stairs', facing='south', half='bottom', lock=True)
    b.set(5, 0, 3, 'mud_bricks')
    for x in (2, 8):
        for y in (3, 4):
            b.set(x, y, 4, 'glass_pane')
    for z in (7, 10, 13):
        for x in (1, 9):
            b.set(x, 3, z, 'glass_pane')
            b.set(x, 4, z, 'glass_pane')
    # Reading room: shelves, archives, lectern and a table.
    for z in range(5, 10):
        for x in (2, 8):
            for y in (2, 3, 4):
                if z != 7:
                    b.set(x, y, z, 'bookshelf')
    b.custom(3, 2, 9, 'archives', facing='north')
    b.set(7, 2, 9, 'chiseled_bookshelf', facing='north')
    b.set(7, 3, 9, 'bookshelf')
    b.set(3, 2, 5, 'lectern', facing='south', has_book=False, powered=False)
    parts.table(b, 5, 2, 7, wood='acacia')
    parts.chair(b, 4, 2, 7, 'west', wood='acacia')
    parts.chair(b, 6, 2, 7, 'east', wood='acacia')
    parts.lantern(b, 5, 5, 6)
    parts.lantern(b, 5, 5, 8)
    b.resident(4, 2, 6, 'scholar')
    # Scholar's room behind a partition.
    for x in range(2, 9):
        for y in (2, 3, 4, 5):
            b.set(x, y, 10, 'acacia_planks')
    b.door(5, 2, 10, facing='south', wood='acacia')
    b.bed(3, 2, 12, 'south', 'brown')
    b.chest(7, 2, 13, 'west', loot=LOOT)
    b.set(7, 2, 11, 'bookshelf')
    b.set(7, 3, 11, 'bookshelf')
    b.set(5, 2, 13, 'potted_acacia_sapling')
    parts.lantern(b, 5, 5, 12)
    b.room('scholar_bedroom', (5, 3, 12))
    # Roof terrace: a thatched reading shade and a ladder up the east wall.
    for x, z in ((3, 8), (7, 8), (3, 12), (7, 12)):
        for y in range(7, 10):
            b.set(x, y, z, 'stripped_acacia_log', axis='y')
    cp.hip_roof(b, 3, 8, 7, 12, 10, cp.THATCH, overhang=1, lip=True)
    b.set(5, 7, 10, 'lectern', facing='north', has_book=False, powered=False)
    for x in (4, 6):
        b.set(x, 7, 12, 'acacia_stairs', facing='south', half='bottom', lock=True, shape='straight')
    b.set(5, 9, 10, 'lantern', hanging=True, waterlogged=False)
    for y in range(2, 9):
        b.set(10, y, 10, 'ladder', facing='east')
    b.set(9, 7, 10, 'mud_bricks')
    b.set(9, 8, 10, 'air')
    b.set(10, 8, 10, 'air')
    # Front court: lamps and benches.
    for z in range(0, 3):
        b.set(5, 0, z, 'mud_bricks' if z % 2 else 'packed_mud')
    for x in (2, 8):
        cp.brazier(b, x, 2)
    plaque(b, 3, 1, 3)
    b.set(8, 1, 3, 'decorated_pot', facing='north', waterlogged=False, cracked=False)
    b.entrance(5)
    b.natural_ground()
    return b


# --------------------------------------------------------------------- market slot
def market_stalls():
    """Three thatched stalls round a packed-mud yard: produce, pottery and cloth."""
    rng = random.Random(2307)
    b = Build('savanna/market_stalls', (11, 7, 11))
    for x in range(11):
        for z in range(11):
            if rng.random() < .9:
                b.set(x, 0, z, rng.choice(['packed_mud', 'packed_mud', 'coarse_dirt', 'mud_bricks', 'dirt_path']))
    cp.thatched_stall(b, 4, 8, 'north', ['melon', None, 'pumpkin'], cloth='orange')
    cp.thatched_stall(b, 8, 4, 'west', ['decorated_pot', None, 'decorated_pot'], cloth='red')
    cp.thatched_stall(b, 2, 2, 'east', ['red_wool', None, 'yellow_wool'], cloth='yellow')
    cp.lamp(b, 5, 5)
    cp.pot_cluster(b, [(1, 8), (2, 9), (1, 9)])
    b.set(9, 1, 9, 'hay_block', axis='y')
    b.set(9, 1, 8, 'hay_block', axis='y')
    b.set(9, 2, 9, 'hay_block', axis='x')
    b.entrance(5)
    b.natural_ground()
    return b


def market_shade():
    """A shade acacia with a ring of seats, a drinking trough and a basket seller's mat."""
    rng = random.Random(2308)
    b = Build('savanna/market_shade', (11, 10, 11))
    for x in range(11):
        for z in range(11):
            d = math.hypot(x - 5, z - 6)
            if d <= 5.2:
                b.set(x, 0, z, 'coarse_dirt' if d < 1.6 else rng.choice(['packed_mud', 'dirt_path', 'coarse_dirt']))
    for z in range(0, 4):
        b.set(5, 0, z, 'packed_mud')
    cp.acacia_tree(b, 5, 6, rng, height=4, lean='east', bend=2, radius=3)
    for x, z, f in ((4, 6, 'east'), (6, 6, 'west'), (5, 7, 'north')):
        b.set(x, 1, z, 'acacia_stairs', facing=f, half='bottom', lock=True, shape='straight')
    for x, z in ((2, 3), (8, 9)):
        cp.log_seat(b, x, 1, z, 'x')
        cp.log_seat(b, x + 1, 1, z, 'x')
    cp.trough(b, 1, 6, 3, 'z')
    for x in range(7, 10):
        for z in range(2, 5):
            b.set(x, 1, z, 'orange_carpet' if (x + z) % 2 else 'red_carpet')
    for x, z in ((8, 3),):
        b.set(x, 1, z, 'decorated_pot', facing='north', waterlogged=False, cracked=False)
    b.barrel(9, 1, 2, 'up')
    b.set(7, 1, 4, 'hay_block', axis='y')
    cp.brazier(b, 2, 1)
    b.entrance(5)
    b.natural_ground()
    return b


def market_kraal():
    """Livestock market: a woven-fence kraal with a donkey and sheep, hay, a trough and the trader's shade."""
    rng = random.Random(2309)
    b = Build('savanna/market_kraal', (11, 8, 11))
    for x in range(11):
        for z in range(11):
            b.set(x, 0, z, 'coarse_dirt' if rng.random() < .5 else 'dirt_path' if rng.random() < .5 else 'packed_mud')
    pen = [(x, z) for x in range(1, 10) for z in range(4, 10) if x in (1, 9) or z in (4, 9)]
    cp.woven_fence(b, [c for c in pen if c != (5, 4)])
    b.set(5, 1, 4, 'acacia_fence_gate', facing='north', open=False, powered=False, in_wall=False)
    for x, z in ((1, 4), (9, 4), (1, 9), (9, 9)):
        b.set(x, 0, z, 'packed_mud')
        b.set(x, 1, z, 'stripped_acacia_log', axis='y')
        b.set(x, 2, z, 'acacia_fence')
    for x, z in ((2, 8), (3, 8), (2, 7)):
        b.set(x, 1, z, 'hay_block', axis='y')
    cp.trough(b, 6, 8, 2, 'x')
    b.animal(4, 1, 6, 'donkey')
    b.animal(6, 1, 6, 'sheep')
    b.animal(3, 1, 5, 'sheep', baby=True)
    # The trader's shade by the gate.
    for x, z in ((7, 0), (9, 0), (7, 2), (9, 2)):
        for y in (1, 2, 3):
            b.set(x, y, z, 'acacia_fence')
    for x in range(6, 11):
        for z in range(0, 4):
            if x in range(7, 10) and z in range(0, 3):
                b.set(x, 4, z, 'hay_block', axis='y')
            elif x in range(6, 11) and z in range(0, 4):
                b.set(x, 4, z, cp.THATCH.slab, type='bottom', waterlogged=False)
    b.set(8, 1, 2, 'acacia_stairs', facing='south', half='bottom', lock=True, shape='straight')
    b.barrel(9, 1, 1, 'up')
    b.set(7, 1, 1, 'decorated_pot', facing='north', waterlogged=False, cracked=False)
    cp.brazier(b, 2, 2)
    for z in range(0, 4):
        b.set(5, 0, z, 'packed_mud')
    b.entrance(5)
    b.natural_ground()
    return b


DESIGNS = {'savanna/tavern': tavern, 'savanna/garrison': garrison, 'savanna/workshop': workshop,
           'savanna/chapel': chapel, 'savanna/apothecary': apothecary, 'savanna/library': library,
           'savanna/market_stalls': market_stalls, 'savanna/market_shade': market_shade,
           'savanna/market_kraal': market_kraal}
