"""Village homes: cottages, two-storey houses, a townhouse, a farmhouse and the family house.

Every home is a drop-in lot: north-facing ``building_entrance`` at [x,1,0],
a path to a real front door and at least one enclosed bedroom with paired
beds. Palettes vary per variant so neighbouring houses differ.
"""
import random

from ..kit import Build
from .. import parts
from ..parts import Body, Style, ROOFS

LOOT = 'minecraft:chests/village/village_plains_house'
PALETTES = {
    'oak': Style(frame='stripped_dark_oak_log', fill='calcite', floor='spruce_planks', roof='spruce',
                 base='cobblestone', trim='spruce', door='spruce', upper_fill='calcite'),
    'birch': Style(frame='stripped_spruce_log', fill='birch_planks', floor='oak_planks', roof='dark_oak',
                   base='stone_bricks', trim='dark_oak', door='dark_oak', upper_fill='birch_planks'),
    'spruce': Style(frame='spruce_log', fill='calcite', floor='spruce_planks', roof='slate',
                    base='cobblestone', trim='spruce', door='spruce', upper_fill='calcite'),
    'plaster': Style(frame='stripped_spruce_log', fill='white_terracotta', floor='oak_planks', roof='dark_oak',
                     base='cobblestone', trim='spruce', door='spruce', upper_fill='white_terracotta'),
    'brick': Style(frame='stripped_dark_oak_log', fill='bricks', floor='dark_oak_planks', roof='slate',
                   base='stone_bricks', trim='dark_oak', door='dark_oak', upper_fill='calcite'),
    'timber': Style(frame='stripped_oak_log', fill='oak_planks', floor='spruce_planks', roof='spruce',
                    base='cobblestone', trim='spruce', door='spruce', upper_fill='calcite'),
}
TRIM = {'spruce': ROOFS['dark_oak'], 'dark_oak': ROOFS['spruce'], 'slate': ROOFS['stone'], 'oak': ROOFS['spruce']}


def trim_for(style):
    return TRIM[next(k for k, v in ROOFS.items() if v is style.roof)]


def path(b, x, z0, z1, rng, y=0):
    for z in range(z0, z1 + 1):
        b.set(x, y, z, rng.choice(['dirt_path', 'dirt_path', 'gravel', 'coarse_dirt']))


def garden(b, x0, x1, z0, z1, rng, density=.75):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            b.set(x, 0, z, 'grass_block')
            if rng.random() < density:
                b.set(x, 1, z, parts.flowers(rng))


def kitchen(b, rng, cells, y=2, facing='east'):
    """Place a few kitchen/living fixtures on the given floor cells (in order)."""
    items = ['crafting_table', 'furnace', 'barrel', 'smoker', 'chest', 'potted']
    for (x, z), item in zip(cells, items):
        if item == 'furnace':
            b.set(x, y, z, 'furnace', facing=facing, lit=False)
        elif item == 'smoker':
            b.set(x, y, z, 'smoker', facing=facing, lit=False)
        elif item == 'barrel':
            b.barrel(x, y, z, 'up')
        elif item == 'chest':
            b.chest(x, y, z, facing, loot=LOOT)
        elif item == 'potted':
            b.set(x, y, z, rng.choice(['potted_red_tulip', 'potted_azure_bluet', 'potted_fern', 'potted_oxeye_daisy']))
        else:
            b.set(x, y, z, item)


def two_storey_interior(b, body, rng, colors=('red', 'red'), rooms=2, stair_wood='spruce'):
    """Stairs along the east wall, living room below, one or two bedrooms above.

    Works for any body at least 9 wide (interior >= 7) and 9 deep.
    """
    a, c = body.x0 + 1, body.x1 - 1
    d, f = body.z0 + 1, body.z1 - 1
    y0 = body.floor_y[0] + 1
    fy = body.floor_y[1]
    steps = fy - body.floor_y[0]
    parts.stair_run(b, c, f, y0, steps, 'north', wood=stair_wood)
    uy = fy + 1
    top = fy + body.heights[1]
    # Upstairs follows the (possibly jettied) upper storey; the stair column stays at x = c.
    ux0, uz0, ux1, uz1 = body.rect(1)
    a, d, f = ux0 + 1, uz0 + 1, uz1 - 1
    # Partition between the stair landing (x = c-1..c) and the bedrooms.
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
        b.bed(a, uy, mid - 1, 'north', colors[0])
        b.bed(a, uy, mid + 1, 'south', colors[1])
        b.chest(c - 3, uy, d, 'south', loot=LOOT)
        parts.lantern(b, a + 1, top, d + 1)
        parts.lantern(b, a + 1, top, f - 1)
        b.room('bedroom_north', (c - 3, uy + 1, d + 1))
        b.room('bedroom_south', (c - 3, uy + 1, f - 1))
    else:
        b.door(c - 2, uy, d + 1, facing='east', wood=body.style.door)
        b.bed(a, uy, f, 'north', colors[0])
        b.bed(a + 2, uy, f, 'north', colors[1])
        b.chest(a + 1, uy, f, 'north', loot=LOOT)
        parts.lantern(b, (a + c - 2) // 2, top, (d + f) // 2)
        b.room('bedroom', (c - 3, uy + 1, d + 1))
    parts.lantern(b, c - 1, top, d)
    # Ground floor living room.
    a, d, f = body.x0 + 1, body.z0 + 1, body.z1 - 1
    table_x, table_z = (a + c - 1) // 2, (d + f) // 2
    parts.table(b, table_x, y0, table_z, wood=stair_wood)
    parts.chair(b, table_x - 1, y0, table_z, 'west', wood=stair_wood)
    parts.chair(b, table_x + 1, y0, table_z, 'east', wood=stair_wood)
    kitchen(b, rng, [(a, f), (a, f - 1), (a + 1, f), (a, d + 2), (a, d + 3)], y=y0, facing='east')
    parts.lantern(b, table_x, fy - 1, table_z)


def cottage(name, palette, seed, axis='x', pitch=1, chimney='west', beds=('red', 'red'), porch=False):
    """One-storey timber cottage with a gable chimney and a separate bedroom."""
    st = PALETTES[palette]
    rng = random.Random(seed)
    b = Build(name, (11, 19, 14))
    body = Body(b, 1, 4, 9, 11, st, heights=(3,), spacing=3 if axis == 'x' else 4).build()
    body.roof(axis=axis, pitch=pitch, gable=st.upper_fill, trim=trim_for(st))
    parts.front_door(b, 5, 2, 4, 'north', wood=st.door,
                     step='stone_brick_stairs' if st.base == 'stone_bricks' else 'cobblestone_stairs', lamps=not porch)
    if axis == 'x':
        body.windows(0, 'north', [(1, 2), (6, 2)], height=1, box='flowering_azalea_leaves')
        body.gable_window('east')
    else:
        body.windows(0, 'north', [(1, 2), (6, 2)], height=2, box='flowering_azalea_leaves')
        body.gable_window('north', height=2)
    body.windows(0, 'south', [(1, 2), (6, 2)], height=1)
    body.windows(0, 'east', [(2, 2), (5, 1)], height=1, box='azalea_leaves')
    body.windows(0, 'west', [3], height=1)
    # Chimney on a side wall.
    cx = 0 if chimney == 'west' else 10
    for y in range(1, 4):
        for z in (6, 7, 8):
            b.set(cx, y, z, 'cobblestone' if y <= 2 else 'stone_bricks')
    for z, f in ((6, 'south'), (8, 'north')):
        b.set(cx, 4, z, 'stone_brick_stairs', facing=f, half='bottom')
    parts.chimney(b, cx, 7, 4, body.ridge + 1, 'bricks')
    if porch:
        for x in (3, 7):
            b.set(x, 0, 2, 'cobblestone')
            for y in (1, 2, 3):
                b.set(x, y, 2, f'{st.trim}_fence')
        for x in range(2, 9):
            b.set(x, 4, 2, f'{st.trim}_stairs', facing='south', half='bottom')
            b.set(x, 4, 3, f'{st.trim}_planks')
        b.set(5, 3, 3, 'lantern', hanging=True)
        for x in range(3, 8):
            b.set(x, 0, 3, f'{st.trim}_planks')
        b.custom(3, 1, 3, 'village_bench', facing='north')
    # Interior: living room to the west, bedroom to the east behind a partition.
    for z in range(5, 11):
        for y in (2, 3, 4):
            b.set(6, y, z, st.floor)
    b.door(6, 2, 7, facing='east', wood=st.door)
    b.bed(8, 2, 10, 'north', beds[0])
    b.bed(8, 2, 6, 'south', beds[1])
    b.chest(7, 2, 10, 'east', loot=LOOT)
    parts.lantern(b, 7, 4, 8)
    b.room('bedroom', (7, 3, 8))
    kitchen(b, rng, [(2, 5), (2, 10), (3, 10), (2, 9)])
    parts.table(b, 3, 2, 7, wood=st.trim)
    parts.chair(b, 4, 2, 7, 'east', wood=st.trim)
    parts.chair(b, 3, 2, 6, 'north', wood=st.trim)
    parts.lantern(b, 4, 4, 6)
    b.set(5, 2, 10, 'potted_red_tulip')
    # Yard.
    path(b, 5, 0, 3 if not porch else 1, rng)
    b.entrance(5)
    if not porch:
        garden(b, 2, 3, 1, 2, rng)
        garden(b, 7, 8, 1, 2, rng)
        parts.lamp_post(b, 1, 1, 1, height=2)
    else:
        garden(b, 1, 2, 0, 1, rng)
        garden(b, 8, 9, 0, 1, rng)
    parts.woodpile(b, 6, 1, 13, 'x', length=3)
    b.custom(4, 1, 1 if not porch else 0, 'house_plaque', facing='north')
    b.resident(4, 2, 8)
    b.natural_ground()
    return b


def tall_house(name, palette, seed, axis='z', pitch=1, jetty=('north',), stone=True, beds=('red', 'blue'),
               chimney='east', rooms=2, child=True):
    """Two-storey house: stone ground floor, timbered upper storey, bedrooms upstairs."""
    st = PALETTES[palette]
    rng = random.Random(seed)
    b = Build(name, (13, 21, 16))
    body = Body(b, 2, 5, 10, 13, st, heights=(3, 3), jetty=jetty, stone_ground=stone).build()
    body.roof(axis=axis, pitch=pitch, gable=st.upper_fill, trim=trim_for(st))
    parts.front_door(b, 5, 2, 5, 'north', wood=st.door, step='cobblestone_stairs')
    body.windows(0, 'north', [1, (6, 2)], height=1, box='flowering_azalea_leaves')
    body.windows(0, 'west', [(2, 2), (5, 1)], height=1)
    body.windows(0, 'south', [(2, 1), (5, 1)], height=1)
    body.windows(1, 'north', [(1, 2), (5, 2)], height=2, shutters=True)
    body.windows(1, 'west', [2, 6], height=1)
    body.windows(1, 'east', [2], height=1)
    body.windows(1, 'south', [2, 5], height=1)
    if axis == 'z':
        body.gable_window('north')
        body.gable_window('south')
    else:
        body.gable_window('west')
    # Chimney stack up the outside of a side wall.
    cx = 11 if chimney == 'east' else 1
    for y in range(1, 4):
        for z in (9, 10):
            b.set(cx, y, z, 'cobblestone')
    parts.chimney(b, cx, 9, 4, body.ridge + 1, 'bricks')
    b.set(cx, 4, 10, 'brick_stairs', facing='north', half='bottom')
    two_storey_interior(b, body, rng, colors=beds, rooms=rooms)
    # Yard: path, flower borders, a lamp and a back garden.
    path(b, 5, 0, 4, rng)
    b.entrance(5)
    garden(b, 2, 3, 1, 3, rng)
    garden(b, 7, 9, 1, 2, rng)
    parts.lamp_post(b, 8, 1, 3, height=2)
    b.custom(4, 1, 2, 'house_plaque', facing='north')
    crop = rng.choice(['wheat', 'carrots', 'potatoes'])
    for x in range(3, 10):
        b.set(x, 0, 15, 'farmland', moisture=7)
        b.set(x, 1, 15, crop, age=7 if rng.random() < .6 else 5)
    for x in (2, 10):
        b.set(x, 1, 15, f'{st.trim}_fence')
    b.set(1, 1, 15, 'composter', level=4)
    b.resident(5, 2, 8)
    if child:
        b.resident(4, 2, 10, child=True)
    else:
        b.resident(4, 2, 10)
    b.natural_ground()
    return b


def townhouse(name, palette, seed, beds=('yellow', 'yellow')):
    """Narrow, tall gable-fronted townhouse with a jettied upper floor."""
    st = PALETTES[palette]
    rng = random.Random(seed)
    b = Build(name, (11, 22, 15))
    body = Body(b, 1, 5, 9, 13, st, heights=(3, 3), jetty=('north', 'south'), stone_ground=False).build()
    body.roof(axis='z', pitch=2, gable=st.upper_fill, trim=trim_for(st))
    parts.front_door(b, 5, 2, 5, 'north', wood=st.door, step='cobblestone_stairs')
    body.windows(0, 'north', [(1, 2), (6, 2)], height=1, box='flowering_azalea_leaves')
    body.windows(0, 'west', [(2, 2), (5, 1)], height=1)
    body.windows(1, 'north', [1, 3, 5, 7], height=2, shutters=False)
    body.windows(1, 'west', [3, 6], height=1)
    body.windows(1, 'south', [2, 6], height=1)
    body.gable_window('north', height=2)
    parts.chimney(b, 3, 12, 6, body.ridge, 'bricks')
    two_storey_interior(b, body, rng, colors=beds, rooms=1)
    path(b, 5, 0, 4, rng)
    b.entrance(5)
    garden(b, 1, 3, 1, 3, rng, .6)
    garden(b, 7, 9, 1, 3, rng, .6)
    b.custom(4, 1, 3, 'house_plaque', facing='north')
    b.barrel(8, 1, 4, 'up')
    b.resident(4, 2, 8)
    b.natural_ground()
    return b


def farmhouse():
    """L-shaped farmhouse with a cross-gabled wing, big chimney and kitchen garden."""
    st = PALETTES['timber']
    rng = random.Random(41)
    b = Build('farmhouse', (16, 19, 18))
    wing = Body(b, 1, 10, 6, 15, st, heights=(3,)).build()
    wing.roof(axis='z', pitch=1, gable='calcite', trim=ROOFS['dark_oak'], rake=(0, 1))
    main = Body(b, 1, 4, 11, 10, st, heights=(3,), spacing=5).build()
    main.roof(axis='x', pitch=1, gable='calcite', trim=ROOFS['dark_oak'])
    parts.front_door(b, 6, 2, 4, 'north', wood='spruce', step='cobblestone_stairs')
    main.windows(0, 'north', [(1, 2), (3, 1), (8, 2)], height=1, box='flowering_azalea_leaves')
    main.windows(0, 'east', [(2, 2)], height=1)
    main.windows(0, 'south', [(7, 2)], height=1)
    wing.windows(0, 'west', [(2, 2)], height=1)
    wing.windows(0, 'south', [(2, 2)], height=1)
    wing.windows(0, 'east', [(2, 1)], height=1)
    main.gable_window('east')
    for y in range(1, 4):
        for z in (6, 7, 8):
            b.set(12, y, z, 'cobblestone')
    parts.chimney(b, 12, 7, 4, main.ridge + 1, 'bricks')
    # Interior: hall and kitchen in the main block, bedroom in the wing.
    for x in range(2, 6):
        for y in (2, 3, 4):
            b.set(x, y, 10, 'spruce_planks')
    b.door(4, 2, 10, facing='south', wood='spruce')
    b.bed(2, 2, 14, 'north', 'brown')
    b.bed(5, 2, 14, 'north', 'brown')
    b.chest(3, 2, 14, 'north', loot=LOOT)
    parts.lantern(b, 3, 4, 12)
    b.room('bedroom', (4, 3, 12))
    parts.table(b, 7, 2, 7, wood='spruce')
    parts.chair(b, 6, 2, 7, 'west')
    parts.chair(b, 8, 2, 7, 'east')
    kitchen(b, rng, [(10, 5), (10, 9), (9, 9), (2, 5)], facing='west')
    b.set(2, 2, 7, 'composter', level=3)
    parts.lantern(b, 7, 4, 6)
    # Kitchen garden behind, fenced.
    for x in range(8, 15):
        for z in range(11, 17):
            edge = x in (8, 14) or z in (11, 16)
            if edge:
                b.set(x, 1, z, 'spruce_fence' if not (x == 11 and z == 11) else 'spruce_fence_gate',
                      **({'facing': 'north', 'open': False, 'in_wall': False, 'powered': False} if (x == 11 and z == 11) else {}))
            elif x == 11:
                b.set(x, 0, z, 'water')
            else:
                b.set(x, 0, z, 'farmland', moisture=7)
                b.set(x, 1, z, 'carrots' if x < 11 else 'potatoes', age=7)
    b.set(13, 1, 4, 'hay_block', axis='y')
    b.set(14, 1, 4, 'hay_block', axis='x')
    b.set(13, 2, 4, 'hay_block', axis='y')
    path(b, 6, 0, 3, rng)
    b.entrance(6)
    garden(b, 2, 4, 1, 2, rng)
    b.custom(5, 1, 2, 'house_plaque', facing='north')
    parts.oak_tree(b, 14, 1, 1, rng, height=4, radius=2)
    b.resident(7, 2, 8)
    b.resident(3, 2, 12)
    b.natural_ground()
    return b


def family_house():
    """The large family home: stone ground floor, jettied plaster upper floor, two bedrooms."""
    st = PALETTES['plaster']
    rng = random.Random(42)
    b = Build('family_house', (15, 21, 17))
    body = Body(b, 2, 5, 12, 13, st, heights=(3, 3), jetty=('north',), stone_ground=True).build()
    body.roof(axis='x', pitch=1, gable='white_terracotta', trim=ROOFS['spruce'])
    # Front cross gable.
    parts.gable_roof(b, 5, 4, 9, 8, body.top, st.roof, axis='z', gable='white_terracotta')
    for y in (body.top + 1, body.top + 2):
        b.set(7, y, 4, 'glass_pane')
    parts.front_door(b, 7, 2, 5, 'north', wood='spruce', step='cobblestone_stairs')
    body.windows(0, 'north', [(1, 2), (7, 2)], height=1, box='flowering_azalea_leaves')
    body.windows(0, 'west', [(2, 2), (5, 1)], height=1)
    body.windows(0, 'south', [(2, 2), (6, 2)], height=1)
    body.windows(1, 'north', [2, 4, 6, 8], height=2, shutters=True)
    body.windows(1, 'west', [3, 6], height=1)
    body.windows(1, 'south', [2, 4, 7], height=1)
    body.gable_window('west')
    for y in range(1, 4):
        for z in (8, 9, 10):
            b.set(13, y, z, 'cobblestone')
    parts.chimney(b, 13, 9, 4, body.ridge + 1, 'bricks')
    two_storey_interior(b, body, rng, colors=('red', 'lime'), rooms=2)
    path(b, 7, 0, 4, rng)
    b.entrance(7)
    garden(b, 2, 5, 1, 3, rng)
    garden(b, 9, 12, 1, 3, rng)
    b.custom(6, 1, 3, 'house_plaque', facing='north')
    parts.lamp_post(b, 9, 1, 4, height=2)
    parts.birch_tree(b, 13, 1, 15, rng, height=5)
    b.custom(4, 1, 15, 'village_bench', facing='north')
    b.resident(5, 2, 8)
    b.resident(8, 2, 10, child=True)
    b.natural_ground()
    return b


DESIGNS = {
    'cottage_oak': lambda: cottage('cottage_oak', 'oak', 11, axis='z', pitch=2, chimney='east', beds=('red', 'red')),
    'cottage_birch': lambda: cottage('cottage_birch', 'birch', 12, axis='x', pitch=1, chimney='east', beds=('yellow', 'yellow')),
    'cottage_spruce': lambda: cottage('cottage_spruce', 'spruce', 13, axis='x', pitch=1, chimney='west',
                                      beds=('blue', 'blue'), porch=True),
    'cottage_plaster': lambda: cottage('cottage_plaster', 'plaster', 14, axis='z', pitch=1, chimney='west',
                                       beds=('orange', 'orange')),
    'house_tall_oak': lambda: tall_house('house_tall_oak', 'timber', 21, axis='z', pitch=1, beds=('red', 'blue')),
    'house_tall_brick': lambda: tall_house('house_tall_brick', 'brick', 22, axis='x', pitch=1, jetty=(),
                                           chimney='west', beds=('green', 'green'), rooms=1, child=False),
    'townhouse': lambda: townhouse('townhouse', 'spruce', 31),
    'townhouse_plaster': lambda: townhouse('townhouse_plaster', 'plaster', 32, beds=('pink', 'pink')),
    'farmhouse': farmhouse,
    'family_house': family_house,
}
