"""Snowy homes: an igloo, log cabins, a stone cottage, an A-frame, a longhouse and two-storey houses.

Every home is a drop-in lot: north-facing ``building_entrance`` at [x,1,0], a
path to a real front door (most behind an enclosed cold porch), a hearth with
a smoking chimney, and at least one enclosed bedroom with paired beds.
"""
import math
import random

from ...kit import Build
from ... import parts
from .palette import STYLES, ROOFS, LOOT
from . import homes_kit as k


def log_cabin():
    """Saddle-notched spruce log cabin with a cold porch, a stone chimney and a box-bed alcove."""
    rng = random.Random(7101)
    b = Build('snowy/log_cabin', (13, 19, 16))
    x0, z0, x1, z1 = 2, 5, 10, 11
    parts.foundation(b, x0, z0, x1, z1, STYLES['cabin'], top=1)
    k.log_walls(b, x0, z0, x1, z1, 2, 4)
    parts.beam_ring(b, x0, z0, x1, z1, 5, 'spruce_log')
    parts.floor(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, 5, 'spruce_planks')
    ridge = parts.gable_roof(b, x0, z0, x1, z1, 5, ROOFS['dark_oak'], axis='z', pitch=2, gable='spruce_planks')
    k.vestibule(b, 6, z0, 1, roof=ROOFS['dark_oak'])
    k.fireplace(b, x0, 8, 'west', 1, ridge + 1)
    # Small windows with shutters; a gable window to the attic.
    k.window(b, 4, 3, z0, 'north')
    k.window(b, 9, 3, z0, 'north')
    k.window(b, x1, 3, 8, 'east')
    k.window(b, 5, 3, z1, 'south')
    k.window(b, 8, 3, z1, 'south')
    b.set(6, 9, z0, 'glass_pane')
    b.set(6, 9, z1, 'glass_pane')
    # Bedroom alcove to the east.
    for z in range(z0 + 1, z1):
        for y in (2, 3, 4):
            b.set(7, y, z, 'spruce_planks')
    b.door(7, 2, 7, facing='east', wood='spruce')
    k.bed_pair(b, 8, 2, 10, 'north', 'light_blue', (1, 0))
    b.chest(9, 2, 6, 'west', loot=LOOT)
    b.set(8, 2, 6, 'white_carpet')
    k.room_lamp(b, 8, 5, 8)
    b.room('bedroom', (8, 3, 8))
    # Living room by the fire.
    k.kitchen(b, rng, [(3, 10), (4, 10), (3, 6)], 2, facing='east')
    parts.table(b, 5, 2, 9)
    parts.chair(b, 5, 2, 10, 'south')
    parts.chair(b, 6, 2, 9, 'east')
    k.fur_rug(b, 3, 7, 4, 9, 2, 'white', 'brown')
    b.custom(4, 2, 7, 'fireside_armchair', facing='west')
    b.custom(4, 2, 9, 'fireside_armchair', facing='west')
    k.room_lamp(b, 5, 5, 7)
    # Yard: path, lamp, woodpile under the east eave, chopping block, a young spruce.
    k.path_line(b, 6, 0, 2, rng)
    b.entrance(6)
    k.lamp_post(b, 9, 1, 2, height=2)
    k.plaque(b, 4, 2)
    k.woodpile(b, 11, 1, 6, along='z', length=5)
    k.chopping_block(b, 11, 1, 3)
    k.spruce(b, 1, 1, 14, rng, height=7, radius=2)
    k.snow_roof(b, 0, 0, 12, 15, rng, 5, eave_y=5)
    b.resident(5, 2, 7)
    b.natural_ground()
    return b


def _dome(cx, cz, r, h):
    def inside(x, y, z, shrink=0.0):
        rr, hh = r - shrink, h - shrink
        if rr <= 0 or hh <= 0:
            return False
        return ((x - cx) ** 2 + (z - cz) ** 2) / rr ** 2 + ((y - 0.5) / hh) ** 2 <= 1
    return inside


def igloo():
    """Snow-block igloo: entry tunnel with a door, a hearth dome with a stone chimney and a sleeping dome."""
    rng = random.Random(7102)
    b = Build('snowy/igloo', (17, 9, 16))
    main, bed = _dome(6, 8, 4.6, 5.2), _dome(12, 8, 3.7, 4.3)
    wall = 10  # partition plane between the domes
    for x in range(b.w):
        for z in range(b.d):
            for y in range(0, b.h):
                outer = main(x, y, z) or bed(x, y, z)
                if not outer:
                    continue
                if y == 0:
                    b.set(x, 0, z, 'snow_block')
                    continue
                inner = (main(x, y, z, 1.1) and x < wall) or (bed(x, y, z, 1.1) and x > wall)
                if not inner:
                    b.set(x, y, z, 'packed_ice' if y == 1 and rng.random() < .55 else 'snow_block')
    # Entry tunnel with the front door.
    for z in range(1, 5):
        for y in (1, 2):
            b.set(5, y, z, 'snow_block')
            b.set(7, y, z, 'snow_block')
        for x in (5, 6, 7):
            b.set(x, 3, z, 'snow_block')
        b.set(6, 1, z, 'air')
        b.set(6, 2, z, 'air')
        b.set(6, 0, z, 'spruce_planks')
    b.set(5, 1, 1, 'blue_ice')
    b.set(7, 1, 1, 'blue_ice')
    b.set(6, 3, 1, 'packed_ice')
    b.door(6, 1, 2, facing='south', wood='spruce')
    b.set(6, 1, 5, 'air')
    b.set(6, 2, 5, 'air')
    # Hearth in the back of the big dome, chimney outside.
    b.set(6, 1, 12, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    b.set(5, 1, 12, 'cobblestone')
    b.set(7, 1, 12, 'cobblestone')
    b.set(6, 2, 12, 'chiseled_stone_bricks')
    b.set(5, 2, 12, 'stone_brick_stairs', facing='east', half='top')
    b.set(7, 2, 12, 'stone_brick_stairs', facing='west', half='top')
    b.set(6, 0, 11, 'cobblestone')
    k.stove_chimney(b, 6, 13, 0, 6)
    # Ice windows.
    b.set(2, 2, 8, 'light_blue_stained_glass')
    b.set(6, 2, 4, 'snow_block')
    b.set(15, 2, 8, 'light_blue_stained_glass')
    # Living dome: furs, kitchen corner, lanterns.
    k.fur_rug(b, 4, 6, 8, 9, 1, 'white', 'light_gray')
    for x in (4, 8):
        for z in (6, 9):
            b.set(x, 1, z, 'brown_carpet')
    b.set(3, 1, 10, 'crafting_table')
    b.barrel(3, 1, 6, 'up')
    b.set(4, 1, 11, 'smoker', facing='north', lit=True)
    b.set(8, 1, 11, 'barrel', facing='up', open=False)
    k.room_lamp(b, 6, 4, 8)
    k.stand_lantern(b, 9, 1, 6)
    # Sleeping dome behind its own door.
    b.door(wall, 1, 8, facing='east', wood='spruce')
    b.bed(12, 1, 9, 'north', 'white')
    b.set(13, 1, 9, 'brown_carpet')
    b.set(13, 1, 7, 'light_gray_carpet')
    b.chest(12, 1, 6, 'south', loot=LOOT) if bed(12, 2, 6, 1.1) else b.chest(13, 1, 8, 'west', loot=LOOT)
    k.stand_lantern(b, 11, 1, 10) if bed(11, 2, 10, 1.1) else None
    b.set(13, 1, 10, 'white_candle', candles=3, lit=True, waterlogged=False)
    b.room('bedroom', (12, 2, 8))
    # Outside: path, ice-lamp, sledge, woodpile and a fishing hole marker.
    k.path_line(b, 6, 0, 0, rng)
    b.entrance(6)
    b.set(9, 1, 1, 'packed_ice')
    b.set(9, 2, 1, 'spruce_fence')
    b.set(9, 3, 1, 'lantern', hanging=False, waterlogged=False)
    k.plaque(b, 3, 2)
    k.sled(b, 13, 1, 2, along='z')
    k.woodpile(b, 8, 1, 14, along='x', length=4)
    b.resident(5, 1, 8)
    b.natural_ground()
    return b



def stone_cottage():
    """Stone-brick cottage with a timber frame, a slate roof, a cold porch and a gable chimney."""
    rng = random.Random(7103)
    st = STYLES['stone']
    b = Build('snowy/stone_cottage', (14, 17, 16))
    x0, z0, x1, z1 = 2, 5, 11, 11
    body = parts.Body(b, x0, z0, x1, z1, st, heights=(3,), spacing=3).build()
    ridge = body.roof(axis='x', pitch=2, gable='spruce_planks')
    k.vestibule(b, 5, z0, 1, roof=ROOFS['slate'], walls='spruce_planks')
    k.fireplace(b, x0, 8, 'west', 1, ridge + 1)
    k.window(b, 8, 3, z0, 'north', width=2)
    k.window(b, 4, 3, z1, 'south')
    k.window(b, 9, 3, z1, 'south')
    k.window(b, x1, 3, 8, 'east')
    body.gable_window('east')
    body.gable_window('west')
    # Bedroom to the east behind a plank partition.
    for z in range(z0 + 1, z1):
        for y in (2, 3, 4):
            b.set(7, y, z, 'spruce_planks')
    b.door(7, 2, 8, facing='east', wood='spruce')
    k.bed_pair(b, 9, 2, 10, 'north', 'cyan', (1, 0))
    b.chest(10, 2, 6, 'west', loot=LOOT)
    b.barrel(8, 2, 6, 'up')
    b.set(8, 2, 10, 'white_candle', candles=2, lit=True, waterlogged=False)
    k.room_lamp(b, 9, 5, 8)
    b.room('bedroom', (9, 3, 7))
    # Living room around the hearth.
    k.kitchen(b, rng, [(3, 10), (4, 10), (3, 6)], 2, facing='east')
    parts.table(b, 5, 2, 9)
    parts.chair(b, 6, 2, 9, 'east')
    parts.chair(b, 5, 2, 10, 'south')
    k.fur_rug(b, 3, 7, 4, 9, 2, 'light_gray', 'gray')
    b.custom(4, 2, 9, 'fireside_armchair', facing='west')
    k.room_lamp(b, 5, 5, 7)
    # Yard.
    k.path_line(b, 5, 0, 2, rng)
    b.entrance(5)
    k.lamp_post(b, 9, 1, 2, height=2)
    k.plaque(b, 3, 2)
    k.woodpile(b, 12, 1, 6, along='z', length=5)
    k.sled(b, 11, 1, 2, along='x', load=False)
    k.leaf(b, 1, 1, 13)
    k.leaf(b, 2, 1, 13)
    k.leaf(b, 1, 2, 13)
    k.snow_roof(b, 0, 0, 13, 15, rng, 5, eave_y=5)
    b.resident(4, 2, 7)
    b.natural_ground()
    return b


def a_frame():
    """Steep A-frame cabin whose roof reaches the ground; a glazed gable front and a hearth bedroom."""
    rng = random.Random(7104)
    st = STYLES['cabin']
    b = Build('snowy/a_frame', (11, 15, 17))
    parts.foundation(b, 1, 3, 9, 13, st, top=1)
    ridge = parts.gable_roof(b, 2, 3, 8, 13, 2, ROOFS['dark_oak'], axis='z', overhang=1, pitch=2)
    for z in (3, 9, 13):
        k.seal_gable(b, z, 2, ridge, 0, 10, 'spruce_planks')
    # Glazed front gable around the door.
    for y in range(5, ridge):
        for x in range(3, 8):
            if b.get(x, y, 3)[0] == 'minecraft:spruce_planks':
                b.set(x, y, 3, 'glass_pane')
    for x in range(2, 9):
        if b.get(x, 4, 3)[0] == 'minecraft:spruce_planks':
            b.set(x, 4, 3, 'stripped_spruce_log', axis='x')
    for y in (2, 3):
        b.set(2, y, 3, 'stripped_spruce_log', axis='y')
        b.set(8, y, 3, 'stripped_spruce_log', axis='y')
    b.set(3, 3, 3, 'glass_pane')
    b.set(7, 3, 3, 'glass_pane')
    parts.front_door(b, 5, 2, 3, 'north', wood='spruce', step='cobblestone_stairs', lamps=False)
    k.fireplace(b, 5, 13, 'south', 1, ridge + 1)
    b.door(5, 2, 9, facing='south', wood='spruce')
    # Bedroom by the hearth at the back.
    b.bed(3, 2, 12, 'north', 'red')
    b.bed(7, 2, 12, 'north', 'red')
    b.chest(3, 2, 10, 'south', loot=LOOT)
    b.barrel(7, 2, 10, 'up')
    k.hang(b, 5, 6, 11, links=2)
    b.room('bedroom', (5, 3, 11))
    # Living room under the glass.
    b.set(8, 2, 5, 'smoker', facing='west', lit=True)
    b.barrel(8, 2, 6, 'up')
    b.set(8, 2, 7, 'crafting_table')
    b.set(8, 2, 8, 'water_cauldron', level=3)
    parts.table(b, 3, 2, 6)
    parts.chair(b, 3, 2, 7, 'south')
    parts.chair(b, 4, 2, 6, 'east')
    k.fur_rug(b, 4, 5, 6, 7, 2, 'white', 'red')
    k.hang(b, 5, 6, 6, links=2)
    # Yard.
    k.path_line(b, 5, 0, 1, rng)
    b.entrance(5)
    k.lamp_post(b, 2, 1, 1, height=2)
    k.plaque(b, 8, 1)
    k.woodpile(b, 0, 1, 5, along='z', length=6)
    k.chopping_block(b, 10, 1, 4)
    b.custom(3, 1, 1, 'village_bench', facing='north')
    k.snow_roof(b, 0, 0, 10, 16, rng, 3, eave_y=2)
    b.resident(4, 2, 7)
    b.natural_ground()
    return b


LONG = parts.Style(frame='spruce_log', fill='spruce_planks', floor='spruce_planks', roof=ROOFS['slate'],
                   base='cobblestone', base_stairs='cobblestone_stairs', trim='spruce', door='spruce',
                   upper_fill='spruce_planks', ceiling='spruce_planks', accent='dark_oak')


def longhouse():
    """Stone-and-timber longhouse: a hall with a great hearth between two end bedrooms."""
    rng = random.Random(7105)
    b = Build('snowy/longhouse', (24, 17, 15))
    x0, z0, x1, z1 = 2, 4, 21, 10
    body = parts.Body(b, x0, z0, x1, z1, LONG, heights=(3,), spacing=4).build()
    # Stone lower course under the timber.
    for x, z, facing, corner in parts.ring(x0, z0, x1, z1):
        if not corner:
            b.set(x, 2, z, 'cobblestone')
    ridge = body.roof(axis='x', pitch=2, gable='spruce_planks')
    k.vestibule(b, 11, z0, 1, roof=ROOFS['slate'], walls='spruce_planks', frame='spruce_log')
    k.fireplace(b, 11, z1, 'south', 1, ridge + 1)
    for x in (4, 9, 14, 19):
        k.window(b, x, 3, z0, 'north')
    for x in (5, 8, 15, 18):
        k.window(b, x, 3, z1, 'south')
    k.window(b, x0, 3, 7, 'west')
    k.window(b, x1, 3, 7, 'east')
    body.gable_window('west')
    body.gable_window('east')
    # Partitions with doors to the two bedrooms.
    for px in (7, 16):
        for z in range(z0 + 1, z1):
            for y in (2, 3, 4):
                b.set(px, y, z, 'spruce_planks')
    b.door(7, 2, 7, facing='east', wood='spruce')
    b.door(16, 2, 7, facing='west', wood='spruce')
    k.bed_pair(b, 3, 2, 9, 'north', 'blue', (1, 0))
    b.chest(6, 2, 9, 'north', loot=LOOT)
    b.barrel(3, 2, 5, 'up')
    k.room_lamp(b, 5, 5, 7)
    b.room('bedroom_west', (5, 3, 6))
    k.bed_pair(b, 19, 2, 9, 'north', 'red', (1, 0))
    b.chest(17, 2, 9, 'north', loot=LOOT)
    b.set(20, 2, 5, 'white_candle', candles=3, lit=True, waterlogged=False)
    k.room_lamp(b, 18, 5, 7)
    b.room('bedroom_east', (18, 3, 6))
    # The hall: long table, benches, kitchen corners and the hearth.
    for x in (9, 10, 12, 13):
        parts.table(b, x, 2, 7)
        parts.chair(b, x, 2, 8, 'south')
    k.kitchen(b, rng, [(15, 9), (15, 5), (8, 9), (8, 5), (14, 9)], 2, facing='west')
    b.custom(10, 2, 9, 'fireside_armchair', facing='south')
    b.custom(12, 2, 9, 'fireside_armchair', facing='south')
    k.room_lamp(b, 11, 5, 7)
    k.room_lamp(b, 9, 5, 5)
    k.room_lamp(b, 13, 5, 5)
    # Yard: lamps by the porch, woodpile, sledge, drying rack.
    k.path_line(b, 11, 0, 1, rng)
    b.entrance(11)
    k.lamp_post(b, 8, 1, 2, height=2)
    k.lamp_post(b, 14, 1, 2, height=2)
    k.plaque(b, 9, 1)
    k.woodpile(b, 0, 1, 5, along='z', length=5)
    k.sled(b, 18, 1, 1, along='x')
    for x in (3, 6):
        b.set(x, 1, 13, 'spruce_fence')
        b.set(x, 2, 13, 'spruce_fence')
    for x in (4, 5):
        b.set(x, 2, 13, 'spruce_fence')
    b.set(4, 1, 13, 'white_wool')
    b.set(5, 1, 13, 'light_gray_wool')
    k.snow_roof(b, 0, 0, 23, 14, rng, 5, eave_y=5)
    b.resident(10, 2, 6)
    b.resident(13, 2, 6, child=True)
    b.natural_ground()
    return b


def upstairs(b, body, rng, colors, rooms=2, wood='spruce'):
    """Stairs along the east wall; one or two enclosed bedrooms upstairs."""
    a, c = body.x0 + 1, body.x1 - 1
    d, f = body.z0 + 1, body.z1 - 1
    y0 = body.floor_y[0] + 1
    fy = body.floor_y[1]
    parts.stair_run(b, c, f, y0, fy - body.floor_y[0], 'north', wood=wood)
    uy, top = fy + 1, fy + body.heights[1]
    ux0, uz0, ux1, uz1 = body.rect(1)
    a, d, f = ux0 + 1, uz0 + 1, uz1 - 1
    for z in range(d, f + 1):
        for y in range(uy, top + 1):
            b.set(c - 2, y, z, body.style.floor)
    if rooms == 2:
        mid = (d + f) // 2
        for x in range(a, c - 2):
            for y in range(uy, top + 1):
                b.set(x, y, mid, body.style.floor)
        b.door(c - 2, uy, d + 1, facing='east', wood=body.style.door)
        b.door(c - 2, uy, f - 1, facing='east', wood=body.style.door)
        k.bed_pair(b, a, uy, mid - 1, 'north', colors[0], (1, 0))
        b.bed(a, uy, mid + 1, 'south', colors[1])
        b.chest(c - 3, uy, d, 'south', loot=LOOT)
        b.barrel(c - 3, uy, f, 'up')
        k.room_lamp(b, a + 2, top + 1, d + 1)
        k.room_lamp(b, a + 2, top + 1, f - 1)
        b.room('bedroom_north', (c - 3, uy + 1, d + 1))
        b.room('bedroom_south', (c - 3, uy + 1, f - 1))
    else:
        b.door(c - 2, uy, d + 1, facing='east', wood=body.style.door)
        b.bed(a, uy, f, 'north', colors[0])
        b.bed(a + 2, uy, f, 'north', colors[1])
        b.chest(a + 1, uy, f, 'north', loot=LOOT)
        k.fur_rug(b, a, d, a + 1, d + 2, uy, 'white', 'white')
        k.room_lamp(b, (a + c - 2) // 2, top + 1, (d + f) // 2)
        b.room('bedroom', (c - 3, uy + 1, d + 1))
    k.room_lamp(b, c - 1, top + 1, d)


def dormer(b, x, z, y, roof, cheek='spruce_log', fill='spruce_planks'):
    """Gabled dormer on a north roof slope; its window sits in the wall plane at ``z``."""
    for yy in (y, y + 1, y + 2):
        b.set(x - 1, yy, z, cheek, axis='y')
        b.set(x + 1, yy, z, cheek, axis='y')
        b.set(x - 1, yy, z + 1, fill)
        b.set(x + 1, yy, z + 1, fill)
    b.set(x, y, z, 'glass_pane')
    b.set(x, y + 1, z, 'glass_pane')
    b.set(x, y + 2, z, fill)
    for zz in (z - 1, z, z + 1, z + 2):
        b.set(x - 2, y + 2, zz, roof.stairs, facing='east', half='bottom')
        b.set(x + 2, y + 2, zz, roof.stairs, facing='west', half='bottom')
        b.set(x - 1, y + 3, zz, roof.stairs, facing='east', half='bottom')
        b.set(x + 1, y + 3, zz, roof.stairs, facing='west', half='bottom')
        b.set(x, y + 3, zz, roof.full)
        b.set(x, y + 4, zz, roof.slab, type='bottom', waterlogged=False)
    b.set(x, y + 3, z, fill)


def family_house():
    """Two-storey family house: stone ground floor, white upper storey, a steep roof with two dormers."""
    rng = random.Random(7106)
    st = STYLES['white']
    b = Build('snowy/family_house', (16, 23, 17))
    body = parts.Body(b, 2, 5, 13, 13, st, heights=(3, 3), stone_ground=True).build()
    ridge = body.roof(axis='x', pitch=2, gable='white_terracotta')
    for dx in (5, 10):
        dormer(b, dx, 5, 10, ROOFS['spruce'], fill='white_terracotta')
    k.vestibule(b, 7, 5, 1, roof=ROOFS['spruce'], walls='white_terracotta', frame='spruce_log',
                step='stone_brick_stairs', base='stone_bricks')
    k.fireplace(b, 2, 9, 'west', 1, ridge + 1)
    body.windows(0, 'north', [(1, 2), (8, 2)], height=1)
    body.windows(0, 'south', [(2, 2), (7, 2)], height=1)
    body.windows(0, 'east', [2, 6], height=1)
    body.windows(1, 'north', [2, 9], height=2)
    body.windows(1, 'south', [2, 5, 8], height=1)
    body.windows(1, 'west', [3, 5], height=1)
    body.windows(1, 'east', [3], height=1)
    upstairs(b, body, rng, ('light_blue', 'yellow'), rooms=2)
    # Ground floor: hearth-side living room and kitchen.
    k.fur_rug(b, 3, 7, 5, 11, 2, 'white', 'red')
    b.custom(4, 2, 8, 'fireside_armchair', facing='west')
    b.custom(4, 2, 10, 'fireside_armchair', facing='west')
    parts.table(b, 8, 2, 9)
    parts.chair(b, 7, 2, 9, 'west')
    parts.chair(b, 9, 2, 9, 'east')
    parts.chair(b, 8, 2, 10, 'south')
    k.kitchen(b, rng, [(3, 12), (4, 12), (5, 12), (10, 12), (3, 6)], 2, facing='north')
    b.set(10, 2, 6, 'bookshelf')
    k.room_lamp(b, 8, 5, 8)
    k.room_lamp(b, 4, 5, 9)
    # Yard: path, lamps, woodpile, sledge and a snowy spruce.
    k.path_line(b, 7, 0, 2, rng)
    b.entrance(7)
    k.lamp_post(b, 4, 1, 2, height=2)
    k.plaque(b, 10, 2)
    k.woodpile(b, 14, 1, 7, along='z', length=5)
    k.sled(b, 11, 1, 1, along='x')
    k.spruce(b, 1, 1, 15, rng, height=7, radius=2)
    k.snow_roof(b, 0, 0, 15, 16, rng, 9, eave_y=9)
    b.resident(6, 2, 8)
    b.resident(9, 2, 7, child=True)
    b.natural_ground()
    return b


TOWN = parts.Style(frame='spruce_log', fill='cobblestone', floor='spruce_planks', roof=ROOFS['dark_oak'],
                   base='cobblestone', base_stairs='cobblestone_stairs', trim='spruce', door='spruce',
                   upper_fill='stripped_spruce_log', ceiling='spruce_planks', accent='dark_oak')


def townhouse():
    """Narrow gable-fronted house: stone ground floor, jettied log upper storey, steep dark-oak roof."""
    rng = random.Random(7107)
    b = Build('snowy/townhouse', (13, 23, 17))
    body = parts.Body(b, 2, 5, 10, 13, TOWN, heights=(3, 3), jetty=('north',), stone_ground=True).build()
    ridge = body.roof(axis='z', pitch=2, gable='spruce_planks')
    parts.front_door(b, 5, 2, 5, 'north', wood='spruce', step='cobblestone_stairs', lamps=False)
    b.set(5, 4, 4, 'lantern', hanging=True, waterlogged=False)
    k.fireplace(b, 2, 9, 'west', 1, ridge + 1)
    body.windows(0, 'north', [1, (6, 2)], height=1)
    body.windows(0, 'south', [2, 6], height=1)
    body.windows(0, 'east', [3], height=1)
    body.windows(1, 'north', [1, 3, 5, 7], height=2, shutters=False)
    body.windows(1, 'west', [3, 6], height=1)
    body.windows(1, 'south', [2, 6], height=1)
    body.gable_window('north', height=2)
    body.gable_window('south')
    upstairs(b, body, rng, ('white', 'white'), rooms=1)
    k.kitchen(b, rng, [(3, 12), (4, 12), (5, 12), (3, 6)], 2, facing='north')
    parts.table(b, 6, 2, 9)
    parts.chair(b, 6, 2, 10, 'south')
    parts.chair(b, 5, 2, 9, 'west')
    k.fur_rug(b, 3, 8, 4, 10, 2, 'brown', 'brown')
    b.custom(4, 2, 10, 'fireside_armchair', facing='west')
    k.room_lamp(b, 6, 5, 7)
    k.path_line(b, 5, 0, 3, rng)
    b.entrance(5)
    k.lamp_post(b, 9, 1, 2, height=2)
    k.plaque(b, 3, 2)
    k.woodpile(b, 11, 1, 7, along='z', length=5)
    b.barrel(8, 1, 3, 'up')
    k.snow_roof(b, 0, 0, 12, 16, rng, 9, eave_y=9)
    b.resident(4, 2, 8)
    b.natural_ground()
    return b


def trapper_cabin():
    """Long, low log cabin with a deep front porch, a lean-to woodshed and furs drying."""
    rng = random.Random(7108)
    st = STYLES['cabin']
    b = Build('snowy/trapper_cabin', (16, 14, 14))
    x0, z0, x1, z1 = 2, 5, 11, 10
    parts.foundation(b, x0, z0, x1, z1, st, top=1)
    k.log_walls(b, x0, z0, x1, z1, 2, 4)
    parts.beam_ring(b, x0, z0, x1, z1, 5, 'spruce_log')
    parts.floor(b, x0 + 1, z0 + 1, x1 - 1, z1 - 1, 5, 'spruce_planks')
    ridge = parts.gable_roof(b, x0, z0, x1, z1, 5, ROOFS['spruce'], axis='x', pitch=2, gable='spruce_planks')
    # Porch: plank deck, log posts, a slab roof under the eave.
    for x in range(x0, x1 + 1):
        for z in (2, 3, 4):
            b.set(x, 1, z, 'spruce_planks')
            b.set(x, 0, z, 'cobblestone')
        b.set(x, 5, 3, 'spruce_slab', type='bottom', waterlogged=False)
        b.set(x, 5, 2, 'spruce_slab', type='bottom', waterlogged=False)
        b.set(x, 4, 1, 'spruce_stairs', facing='south', half='bottom')
    for x in (x0, 6, x1):
        for y in (2, 3, 4):
            b.set(x, y, 2, 'stripped_spruce_log', axis='y')
    b.set(5, 1, 1, 'spruce_stairs', facing='south', half='bottom', lock=True)
    parts.front_door(b, 5, 2, z0, 'north', wood='spruce', lamps=False)
    k.hang(b, 8, 4, 3)
    b.custom(3, 2, 4, 'village_bench', facing='north')
    b.custom(4, 2, 4, 'village_bench', facing='north')
    b.barrel(10, 2, 4, 'up')
    # Furs on a drying frame at the porch end.
    b.set(9, 2, 3, 'spruce_fence')
    b.set(9, 3, 3, 'brown_wool')
    b.set(10, 3, 3, 'white_wool')
    k.fireplace(b, x0, 7, 'west', 1, ridge + 1)
    k.window(b, 8, 3, z0, 'north', width=2)
    k.window(b, 4, 3, z1, 'south')
    k.window(b, 9, 3, z1, 'south')
    # Bedroom.
    for z in range(z0 + 1, z1):
        for y in (2, 3, 4):
            b.set(7, y, z, 'spruce_planks')
    b.door(7, 2, 7, facing='east', wood='spruce')
    k.bed_pair(b, 8, 2, 9, 'north', 'brown', (1, 0))
    b.chest(10, 2, 9, 'north', loot=LOOT)
    b.set(10, 2, 6, 'white_carpet')
    k.room_lamp(b, 9, 5, 7)
    b.room('bedroom', (9, 3, 7))
    # Living room.
    k.kitchen(b, rng, [(3, 9), (4, 9), (3, 6)], 2, facing='east')
    parts.table(b, 5, 2, 8)
    parts.chair(b, 6, 2, 8, 'east')
    k.fur_rug(b, 4, 6, 4, 7, 2, 'white', 'white')
    b.custom(4, 2, 6, 'fireside_armchair', facing='west')
    k.room_lamp(b, 5, 5, 7)
    # Lean-to woodshed on the east.
    for z in (z0, z1):
        b.set(14, 0, z, 'cobblestone')
        for y in (1, 2):
            b.set(14, y, z, 'spruce_fence')
        b.set(14, 3, z, 'stripped_spruce_log', axis='y')
    for z in range(z0 - 1, z1 + 2):
        b.set(12, 5, z, 'spruce_stairs', facing='west', half='bottom')
        b.set(13, 4, z, 'spruce_stairs', facing='west', half='bottom')
        b.set(14, 4, z, 'spruce_slab', type='bottom', waterlogged=False)
    for z in range(z0 + 1, z1):
        for y in (1, 2):
            b.set(12, y, z, 'spruce_log', axis='x')
            b.set(13, y, z, 'spruce_log', axis='x')
        b.set(12, 3, z, 'spruce_log', axis='x')
    # Yard.
    k.path_line(b, 5, 0, 1, rng)
    b.entrance(5)
    k.chopping_block(b, 13, 1, 2)
    k.plaque(b, 3, 1)
    k.spruce(b, 1, 1, 12, rng, height=6, radius=2)
    k.snow_roof(b, 0, 0, 15, 13, rng, 3, eave_y=4)
    b.resident(5, 2, 7)
    b.resident(4, 2, 8, child=True)
    b.natural_ground()
    return b


DESIGNS = {
    'snowy/log_cabin': log_cabin,
    'snowy/igloo': igloo,
    'snowy/stone_cottage': stone_cottage,
    'snowy/a_frame': a_frame,
    'snowy/longhouse': longhouse,
    'snowy/family_house': family_house,
    'snowy/townhouse': townhouse,
    'snowy/trapper_cabin': trapper_cabin,
}
