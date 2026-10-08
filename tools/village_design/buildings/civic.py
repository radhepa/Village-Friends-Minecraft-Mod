"""Civic buildings that face the town square (one of each per village).

Large slots are up to 17 wide; small slots up to 11 wide. Each keeps the lot
contract (north-facing ``building_entrance`` at [x,1,0]) and its profession
workstations, residents and beds.
"""
import random

from ..kit import Build
from .. import parts
from ..parts import Body, Style, ROOFS

LOOT_HOUSE = 'minecraft:chests/village/village_plains_house'


def plaque(b, x, z, facing='north'):
    b.custom(x, 1, z, 'house_plaque', facing=facing)


def tavern():
    """The Hearth: where the village eats lunch and supper, spends its evenings and hears the bard.

    A pergola beer garden on the square; a stone common room with a big hearth and armchairs, two long
    trestle tables, two square tables, a long bar with stools and room to lean, and the bard's corner;
    the kitchen wing behind with a serving hatch; two guest rooms upstairs; a yard with wood and kegs.

    Tavern furniture (``tavern_table``, ``tavern_chair``, ``bar_stool``, ``fireside_armchair`` and the
    benches) faces the way its sitter faces; stair chairs face their backrest side.
    """
    rng = random.Random(301)
    st = Style(frame='stripped_dark_oak_log', fill='cobblestone', floor='spruce_planks', roof='dark_oak',
               base='cobblestone', trim='spruce', door='dark_oak', upper_fill='calcite')
    b = Build('tavern', (17, 22, 29))
    # Kitchen wing first, so the hall's back wall and roof tuck over it.
    wing = Body(b, 8, 21, 15, 27, Style(frame='stripped_dark_oak_log', fill='bricks', floor='stone_bricks',
                                          roof='dark_oak', base='cobblestone', trim='spruce'), heights=(4,))
    wing.build()
    wing.roof(axis='z', pitch=1, gable='bricks', rake=(0, 1))
    # The hall: walls x 1..15, z 6..21; common room x 2..14, z 7..20 on the floor at Y=1; rooms on Y=6.
    hall = Body(b, 1, 6, 15, 21, st, heights=(4, 3), stone_ground=True)
    hall.build()
    hall.roof(axis='z', pitch=1, gable='calcite', trim=ROOFS['spruce'])
    _tavern_facade(b, hall, wing)
    _tavern_terrace(b, rng)
    _tavern_hearth(b)
    _tavern_common_room(b)
    _tavern_bar(b)
    _tavern_kitchen(b)
    _tavern_upstairs(b)
    _tavern_yard(b, rng)
    b.entrance(8)
    b.natural_ground()
    return b


def _tavern_facade(b, hall, wing):
    """Gable end to the square: stone below with dark timber posts, plaster and flower boxes above."""
    for x in (4, 7, 9, 12):
        for y in range(2, 6):
            b.set(x, y, 6, 'stripped_dark_oak_log', axis='y')
    hall.windows(0, 'north', [(1, 2), (12, 2)], height=2, shutters=True)
    hall.windows(0, 'north', [(4, 2), (9, 2)], height=2, shutters=False)
    hall.windows(0, 'west', [(2, 2), (12, 2)], height=2, shutters=True)
    hall.windows(0, 'east', [(2, 2), (10, 2)], height=2, shutters=True)
    hall.windows(0, 'south', [(2, 1)], height=2, shutters=True)
    hall.windows(1, 'north', [2, (5, 2), (8, 2), 12], height=2, shutters=False, box='flowering_azalea_leaves')
    hall.windows(1, 'west', [(2, 2), (12, 2)], height=2, shutters=True)
    hall.windows(1, 'east', [2, 6, (9, 2), 13], height=2, shutters=True)
    hall.windows(1, 'south', [(3, 2)], height=2, shutters=True)
    hall.gable_window('north', height=2)
    hall.gable_window('south', height=1)
    # Timber posts break up the long stone walls, in line with the frame above; the front gable is half-timbered.
    for z in (10, 17):
        for y in range(2, 6):
            b.set(1, y, z, 'stripped_dark_oak_log', axis='y')
    for z in (10, 13, 19):
        for y in range(2, 6):
            b.set(15, y, z, 'stripped_dark_oak_log', axis='y')
    for x in (5, 7):
        for y in range(2, 6):
            b.set(x, y, 21, 'stripped_dark_oak_log', axis='y')
    for x in range(5, 12):
        b.set(x, 14, 6, 'stripped_dark_oak_log', axis='x')
    for y in (11, 15, 16, 17):
        b.set(8, y, 6, 'stripped_dark_oak_log', axis='y')
    wing.windows(0, 'east', [(2, 2)], height=1)
    wing.windows(0, 'south', [(1, 1), (5, 1)], height=1)
    parts.front_door(b, 8, 2, 6, 'north', wood='dark_oak', step='cobblestone_stairs', lamps=False)
    b.set(8, 4, 6, 'chiseled_stone_bricks')
    plaque(b, 10, 5)
    # The hearth's brick chimney climbs the outside of the west wall in steps.
    for z in range(12, 17):
        b.set(0, 0, z, 'cobblestone')
        b.set(0, 1, z, 'cobblestone')
        for y in range(2, 6):
            b.set(0, y, z, 'bricks')
    b.set(0, 6, 12, 'brick_stairs', facing='south', half='bottom')
    b.set(0, 6, 16, 'brick_stairs', facing='north', half='bottom')
    for z in range(13, 16):
        for y in range(6, 10):
            b.set(0, y, z, 'bricks')
    b.set(0, 10, 13, 'brick_stairs', facing='south', half='bottom')
    b.set(0, 10, 15, 'brick_stairs', facing='north', half='bottom')
    parts.chimney(b, 0, 14, 10, hall.ridge + 1, 'bricks')


def _tavern_terrace(b, rng):
    """Beer garden under a pergola: two trestle tables with benches, open to the sky above the seats."""
    for x in range(1, 16):
        for z in range(1, 6):
            b.set(x, 0, z, 'spruce_planks')
    for z in range(0, 6):
        b.set(8, 0, z, 'cobblestone' if z % 2 == 0 else 'gravel')
    for x in (7, 9):
        b.set(x, 0, 0, 'gravel')
    # Posts along the front, beams on top (none of them over a seat, so the seats stay out in the open).
    for x in (1, 6, 10, 15):
        for y in range(1, 5):
            b.set(x, y, 1, 'spruce_fence')
        for z in range(2, 5):
            b.set(x, 5, z, 'stripped_spruce_log', axis='z')
    for x in range(1, 16):
        for z in (1, 5):
            b.set(x, 5, z, 'stripped_spruce_log', axis='x')
    for x in (1, 6, 10, 15):
        b.set(x, 5, 1, 'stripped_spruce_log', axis='y')
    for x in range(1, 16):
        if x not in (7, 8, 9):
            parts.bush(b, x, 6, 1, 'flowering_azalea_leaves' if x % 3 else 'azalea_leaves')
    for x in (1, 15):
        parts.bush(b, x, 6, 2, 'azalea_leaves')
    for x, z in ((6, 3), (10, 3), (3, 1), (13, 1)):
        b.set(x, 4, z, 'lantern', hanging=True, waterlogged=False)
    for x in (7, 9):
        b.set(x, 4, 5, 'lantern', hanging=True, waterlogged=False)
    b.set(8, 4, 1, 'dark_oak_hanging_sign', rotation=8, attached=False, waterlogged=False)
    for x in (6, 10):
        b.set(x, 5, 0, 'red_wall_banner', facing='north')
    # Two trestle tables of two with benches along both sides.
    for x0 in (3, 12):
        for x in (x0, x0 + 1):
            b.custom(x, 1, 3, 'tavern_table')
            b.custom(x, 1, 2, 'village_bench', facing='south')
            b.custom(x, 1, 4, 'village_bench', facing='north')
    # Flower boxes along the front edge.
    for x in list(range(1, 7)) + list(range(10, 16)):
        b.set(x, 0, 0, 'rooted_dirt')
        if x in (1, 6, 10, 15):
            parts.bush(b, x, 1, 0, 'flowering_azalea_leaves')
        else:
            b.set(x, 1, 0, parts.flowers(rng))


def _tavern_hearth(b):
    """The big fireplace in the west wall, with armchairs facing the fire and settles either side."""
    for z in range(12, 17):
        for y in range(2, 6):
            b.set(1, y, z, 'bricks')
        b.set(2, 1, z, 'bricks')
        b.set(1, 1, z, 'bricks')
    for z in range(13, 16):
        b.set(1, 2, z, 'air')
        b.set(1, 3, z, 'air')
        b.set(1, 4, z, 'stripped_dark_oak_log', axis='z')
    b.set(1, 2, 14, 'campfire', lit=True, signal_fire=False, facing='east', waterlogged=False)
    for z in (13, 15):
        b.set(1, 2, z, 'spruce_log', axis='x')
    for z in range(12, 17):
        b.set(2, 4, z, 'dark_oak_slab', type='top', waterlogged=False)
    b.set(2, 5, 12, 'candle', candles=3, lit=True, waterlogged=False)
    b.set(2, 5, 13, 'potted_fern')
    b.set(2, 5, 16, 'candle', candles=2, lit=True, waterlogged=False)
    # A rug laid into the floor (wool, so it stays a walkable floor).
    for x in (3, 4):
        for z in range(12, 17):
            b.set(x, 1, z, 'red_wool' if x == 3 and 13 <= z <= 15 else 'brown_wool')
    for z in (13, 15):
        b.custom(3, 2, z, 'fireside_armchair', facing='west')
    b.barrel(3, 2, 14, 'up')
    b.set(3, 3, 14, 'candle', candles=1, lit=True, waterlogged=False)
    for x in (2, 3):
        b.custom(x, 2, 11, 'village_bench', facing='south')
    # Firewood stacked by the hearth.
    b.set(2, 2, 17, 'spruce_log', axis='z')
    b.set(2, 3, 17, 'spruce_log', axis='z')
    b.set(3, 2, 17, 'spruce_log', axis='z')


def _tavern_common_room(b):
    """Long tables, square tables, the bard's corner, beams, chandelier and the stairs up."""
    # Two long trestle tables of three, chairs down both sides.
    for z0 in (8, 13):
        for z in range(z0, z0 + 3):
            b.custom(6, 2, z, 'tavern_table')
            b.custom(5, 2, z, 'tavern_chair', facing='east')
            b.custom(7, 2, z, 'tavern_chair', facing='west')
    # A square table by the south-west window, and an old fence-and-plate table with stair chairs.
    b.custom(3, 2, 19, 'tavern_table')
    for x, z, f in ((2, 19, 'east'), (4, 19, 'west'), (3, 18, 'south'), (3, 20, 'north')):
        b.custom(x, 2, z, 'tavern_chair', facing=f)
    parts.table(b, 6, 2, 18, wood='dark_oak')
    for x, z, back in ((5, 18, 'west'), (7, 18, 'east'), (6, 17, 'north'), (6, 19, 'south')):
        parts.chair(b, x, 2, z, back, wood='spruce')
    # The bard's corner: a low dais by the front window, two slab steps, a note block to play beside.
    for x in (2, 3):
        for z in (7, 8):
            b.set(x, 2, z, 'dark_oak_planks' if (x, z) != (3, 8) else 'red_wool')
        b.set(x, 2, 9, 'spruce_slab', type='bottom', waterlogged=False)
    b.set(2, 3, 7, 'note_block', instrument='bass', note=0, powered=False)
    b.set(3, 5, 7, 'yellow_wall_banner', facing='south')
    b.set(2, 5, 8, 'red_wall_banner', facing='east')
    b.set(3, 5, 8, 'lantern', hanging=True, waterlogged=False)
    # Exposed ceiling beams, lanterns hung from them, and a chandelier over the middle.
    for z in (9, 15, 18):
        for x in range(2, 15):
            if b.get(x, 5, z)[0] == 'minecraft:air':
                b.set(x, 5, z, 'stripped_dark_oak_log', axis='x')
    for x, z in ((9, 9), (9, 15), (9, 18), (3, 15), (12, 15)):
        b.set(x, 4, z, 'lantern', hanging=True, waterlogged=False)
    for x, z in ((5, 12), (6, 12), (7, 12), (6, 11), (6, 13)):
        b.set(x, 5, z, 'dark_oak_fence')
    for x, z in ((5, 12), (7, 12), (6, 11), (6, 13)):
        b.set(x, 4, z, 'lantern', hanging=True, waterlogged=False)
    # Stairs up along the back wall, with a cupboard of barrels underneath.
    parts.stair_run(b, 7, 20, 2, 5, 'east', wood='spruce')
    b.barrel(10, 2, 20, 'north')
    b.barrel(11, 2, 20, 'north')
    b.barrel(11, 3, 20, 'north')
    b.set(4, 2, 7, 'barrel', facing='up', open=False)
    b.set(4, 3, 7, 'potted_azure_bluet')


def _tavern_bar(b):
    """The bar along the east wall: a stripped dark oak counter with five stools and room to lean.

    The keeper's well behind it is half a step down (a slab floor), so patrons never take it for
    standing room; the tap stand and drinks barrel stand against the wall at the back of the well.
    """
    for z in range(9, 18):
        b.set(12, 2, z, 'stripped_dark_oak_log', axis='z')
    b.set(12, 2, 18, 'stripped_dark_oak_log', axis='y')
    b.set(12, 3, 18, 'lantern', hanging=False, waterlogged=False)
    for z in (9, 11, 13, 15, 17):
        b.custom(11, 2, z, 'bar_stool', facing='east')
    for z in range(9, 21):
        b.set(13, 1, z, 'spruce_slab', type='bottom', waterlogged=False)
    # The back bar: kegs, shelves of candles and pots, the keeper's stations.
    b.barrel(13, 2, 8, 'west')
    b.barrel(14, 2, 8, 'west')
    b.barrel(14, 2, 7, 'up')
    b.barrel(13, 2, 7, 'west')
    b.custom(14, 2, 13, 'tap_stand', facing='west')
    b.custom(14, 2, 14, 'drinks_barrel', facing='west')
    for z in (9, 10, 11, 12, 18, 19, 20):
        b.barrel(14, 2, z, 'west')
    for z in (10, 12, 19):
        b.barrel(14, 3, z, 'west')
    b.set(14, 3, 11, 'brewing_stand', has_bottle_0=False, has_bottle_1=False, has_bottle_2=False)
    b.chest(14, 2, 15, 'west')
    b.set(14, 2, 16, 'barrel', facing='up', open=False)
    b.set(14, 2, 17, 'water_cauldron', level=3)
    for z in (10, 11, 12, 19, 20):
        b.set(14, 4, z, 'spruce_trapdoor', facing='west', half='top', open=False, powered=False, waterlogged=False)
    for z, item in ((10, 'candle'), (11, 'potted_red_tulip'), (12, 'candle'), (19, 'potted_fern'), (20, 'candle')):
        if item == 'candle':
            b.set(14, 5, z, 'candle', candles=3 if z % 2 else 2, lit=True, waterlogged=False)
        else:
            b.set(14, 5, z, item)
    b.set(14, 4, 13, 'red_wall_banner', facing='west')
    b.set(14, 4, 14, 'yellow_wall_banner', facing='west')
    for z in (10, 13, 16):
        b.set(13, 5, z, 'hanging_roots', waterlogged=False)
    b.resident(13, 2, 14, 'tavern_keeper')
    # Serving hatch and door to the kitchen at the end of the well.
    b.set(12, 2, 21, 'spruce_stairs', facing='north', half='top', waterlogged=False, lock=True)
    b.set(12, 3, 21, 'air')
    b.door(13, 2, 21, facing='north', wood='spruce')


def _tavern_kitchen(b):
    """The cook's kitchen: stove and smoker under a brick hood, prep table, pantry and water."""
    b.custom(11, 2, 26, 'kitchen_stove', facing='north')
    b.set(12, 2, 26, 'smoker', facing='north', lit=True)
    b.set(10, 2, 26, 'water_cauldron', level=3)
    for x in (11, 12):
        b.set(x, 4, 26, 'bricks')
        b.set(x, 5, 26, 'bricks')
    parts.chimney(b, 11, 26, 6, 12, 'bricks')
    b.set(9, 2, 22, 'crafting_table')
    b.barrel(9, 2, 23, 'east')
    b.barrel(9, 3, 23, 'east')
    b.barrel(9, 2, 25, 'up')
    b.barrel(9, 2, 26, 'up')
    b.set(9, 3, 26, 'hay_block', axis='y')
    b.barrel(14, 2, 22, 'west')
    b.set(14, 2, 23, 'smooth_stone_slab', type='double')
    b.set(14, 2, 24, 'smooth_stone_slab', type='double')
    b.set(14, 3, 23, 'potted_red_mushroom')
    b.set(13, 2, 26, 'barrel', facing='up', open=False)
    b.set(14, 2, 26, 'composter', level=4)
    for x, z in ((10, 23), (13, 24), (11, 22)):
        b.set(x, 5, z, 'hanging_roots', waterlogged=False)
    parts.lantern(b, 12, 5, 24)
    b.resident(11, 2, 24, 'cook')
    parts.front_door(b, 8, 2, 24, 'west', wood='spruce', step='cobblestone_stairs', lamps=False)


def _tavern_upstairs(b):
    """Two guest rooms on the west side, a landing and linen store on the east."""
    for z in range(7, 21):
        for y in (7, 8, 9):
            b.set(8, y, z, 'spruce_planks')
    for x in range(2, 8):
        for y in (7, 8, 9):
            b.set(x, y, 14, 'spruce_planks')
    b.door(8, 7, 10, facing='east', wood='spruce')
    b.door(8, 7, 17, facing='east', wood='spruce', hinge='right')
    for x in (9, 10):
        b.set(x, 7, 19, 'spruce_fence')
    # North room.
    b.bed(3, 7, 9, 'west', 'red')
    b.bed(3, 7, 12, 'west', 'red')
    b.chest(2, 7, 10, 'east', loot=LOOT_HOUSE)
    b.set(2, 7, 11, 'barrel', facing='up', open=False)
    b.set(2, 8, 11, 'potted_dandelion')
    parts.table(b, 6, 7, 8, wood='spruce')
    b.set(7, 7, 13, 'barrel', facing='up', open=False)
    parts.rug(b, 4, 10, 6, 12, 7, 'white', border='red')
    parts.lantern(b, 5, 9, 10)
    b.room('guest_room_north', (5, 8, 11))
    # South room.
    b.bed(3, 7, 16, 'west', 'green')
    b.bed(3, 7, 19, 'west', 'green')
    b.chest(2, 7, 17, 'east', loot=LOOT_HOUSE)
    b.set(2, 7, 18, 'barrel', facing='up', open=False)
    b.set(2, 8, 18, 'potted_azure_bluet')
    parts.table(b, 6, 7, 20, wood='spruce')
    parts.rug(b, 4, 16, 6, 18, 7, 'white', border='green')
    parts.lantern(b, 5, 9, 17)
    b.room('guest_room_south', (5, 8, 17))
    # Landing and linen store.
    for z in (7, 8):
        b.barrel(14, 7, z, 'west')
    b.set(14, 8, 7, 'white_wool')
    b.chest(13, 7, 7, 'south')
    b.set(9, 7, 7, 'bookshelf')
    b.set(9, 8, 7, 'bookshelf')
    parts.rug(b, 10, 10, 13, 15, 7, 'brown', border='red')
    parts.lantern(b, 11, 9, 9)
    parts.lantern(b, 11, 9, 16)


def _tavern_yard(b, rng):
    """Back yard by the kitchen door: woodpile, kegs, hay, a chopping block and a kitchen garden."""
    for x in range(1, 8):
        for z in range(22, 29):
            if rng.random() < .6:
                b.set(x, 0, z, rng.choice(['coarse_dirt', 'gravel', 'dirt_path', 'coarse_dirt']))
    parts.woodpile(b, 2, 1, 22, 'x', length=4, wood='spruce', height=2)
    b.set(5, 1, 25, 'stripped_oak_log', axis='y')
    for x, z, f in ((1, 26, 'east'), (1, 27, 'east'), (2, 27, 'north')):
        b.barrel(x, 1, z, f)
    b.barrel(1, 2, 27, 'up')
    for x, z in ((6, 27), (6, 28), (5, 28)):
        b.set(x, 1, z, 'hay_block', axis='y')
    b.set(6, 2, 28, 'hay_block', axis='x')
    for x in (1, 2, 3):
        b.set(x, 0, 24, 'rooted_dirt')
        b.set(x, 1, 24, rng.choice(['fern', 'short_grass', 'poppy']))
    for x in range(9, 15):
        if x % 2:
            b.barrel(x, 1, 28, 'up')


def crenellate(b, x0, z0, x1, z1, y, mat='stone_brick_wall', block_mat='stone_bricks'):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                b.set(x, y, z, block_mat if (x + z) % 2 == 0 else mat)


def garrison():
    """Watch house: stone barracks, a crenellated watchtower and a fenced training yard."""
    rng = random.Random(302)
    st = Style(frame='stripped_spruce_log', fill='stone_bricks', floor='spruce_planks', roof='slate',
               base='cobblestone', trim='spruce', door='spruce', upper_fill='spruce_planks')
    b = Build('garrison', (17, 24, 21))
    bar = Body(b, 1, 11, 15, 18, st, heights=(4, 3), stone_ground=True, spacing=4).build()
    bar.roof(axis='x', pitch=1, gable='spruce_planks', trim=ROOFS['stone'])
    bar.windows(0, 'north', [(2, 2), (11, 2)], height=2)
    bar.windows(0, 'south', [3, 6, 9, 12], height=2, shutters=False)
    bar.windows(1, 'north', [2, 5, 9, 12], height=2, shutters=False)
    bar.windows(1, 'south', [2, 5, 9, 12], height=2, shutters=False)
    bar.gable_window('west')
    parts.front_door(b, 7, 2, 11, 'north', wood='spruce', step='stone_brick_stairs', lamps=True)
    # Watchtower at the yard's front corner.
    tx0, tz0, tx1, tz1 = 11, 1, 15, 5
    for y in range(0, 15):
        for x in range(tx0, tx1 + 1):
            for z in range(tz0, tz1 + 1):
                edge = x in (tx0, tx1) or z in (tz0, tz1)
                corner = x in (tx0, tx1) and z in (tz0, tz1)
                if y == 0 or (edge and y <= 13):
                    b.set(x, y, z, 'cobblestone' if y <= 1 else ('stone_bricks' if not corner else 'polished_andesite'))
                elif not edge and y in (4, 8, 13):
                    b.set(x, y, z, 'spruce_planks')
    for y in range(2, 14):
        b.set(tx0 + 1, y, tz0 + 1, 'ladder', facing='south')
        b.set(tx0 + 1, y, tz0, 'stone_bricks')
    for y in (4, 8, 13):
        b.set(tx0 + 1, y, tz0 + 1, 'ladder', facing='south')
    # Corbelled parapet and battlements.
    for x in range(tx0 - 1, tx1 + 2):
        for z in range(tz0 - 1, tz1 + 2):
            if x in (tx0 - 1, tx1 + 1) or z in (tz0 - 1, tz1 + 1):
                if b.inside(x, 13, z):
                    f = 'south' if z == tz0 - 1 else 'north' if z == tz1 + 1 else 'east' if x == tx0 - 1 else 'west'
                    b.set(x, 12, z, 'stone_brick_stairs', facing=f, half='top', clip=True)
                    b.set(x, 13, z, 'stone_bricks')
    for x in range(tx0, tx1 + 1):
        for z in range(tz0, tz1 + 1):
            b.set(x, 13, z, 'spruce_planks' if tx0 < x < tx1 and tz0 < z < tz1 else 'stone_bricks')
    b.set(tx0 + 1, 13, tz0 + 1, 'spruce_trapdoor', facing='south', half='top', open=False)
    crenellate(b, tx0 - 1, tz0 - 1, tx1 + 1, tz1 + 1, 14)
    for x, z in ((tx0 - 1, tz0 - 1), (tx1 + 1, tz0 - 1), (tx0 - 1, tz1 + 1), (tx1 + 1, tz1 + 1)):
        b.set(x, 14, z, 'stone_bricks', clip=True)
        b.set(x, 15, z, 'lantern', clip=True)
    # Pointed spire roof over the platform.
    for x, z in ((tx0, tz0), (tx1, tz0), (tx0, tz1), (tx1, tz1)):
        for y in (14, 15):
            b.set(x, y, z, 'spruce_fence')
    parts.pyramid_roof(b, tx0, tz0, tx1, tz1, 16, 'deepslate_tile_stairs', 'deepslate_tiles', pitch=2,
                       finial=['stone_brick_wall', 'lightning_rod'])
    for (x, z, f) in ((tx0 + 2, tz0 - 1, 'north'), (tx0 - 1, tz0 + 2, 'west')):
        b.set(x, 10, z, 'red_wall_banner', facing=f, clip=True)
    for z in (tz0 + 2,):
        for y in (6, 10):
            b.set(tx1, y, z, 'glass_pane')
            b.set(tx0, y, z, 'glass_pane')
    b.door(tx0 + 2, 1, tz1, facing='north', wood='spruce')
    b.set(tx0 + 2, 0, tz1 + 1, 'cobblestone')
    # Training yard.
    for x in range(1, 16):
        for z in range(1, 11):
            if not (tx0 <= x <= tx1 and tz0 <= z <= tz1):
                b.set(x, 0, z, 'gravel' if rng.random() < .55 else rng.choice(['coarse_dirt', 'dirt_path', 'cobblestone']))
    for x in range(0, 17):
        for z in (0,):
            if x not in (7, 8, 9) and not (tx0 - 1 <= x <= tx1 + 1):
                b.set(x, 1, z, 'spruce_fence')
    for z in range(0, 11):
        b.set(0, 1, z, 'spruce_fence')
        if z > tz1 + 1:
            b.set(16, 1, z, 'spruce_fence')
    for x in (6, 10):
        b.set(x, 1, 0, 'stripped_spruce_log', axis='y')
        b.set(x, 2, 0, 'stripped_spruce_log', axis='y')
        b.set(x, 3, 0, 'lantern')
    for x in range(7, 10):
        b.set(x, 0, 0, 'cobblestone')
    for x, z in ((3, 3), (3, 6), (6, 5)):
        b.custom(x, 1, z, 'training_dummy', facing='south')
    b.custom(2, 1, 9, 'archery_target', facing='east')
    b.custom(2, 1, 8, 'archery_target', facing='east')
    for x, z in ((14, 8), (15, 8), (15, 9)):
        b.set(x, 1, z, 'hay_block', axis='y')
    b.set(10, 1, 9, 'grindstone', face='floor', facing='north')
    b.barrel(11, 1, 9, 'up')
    b.set(12, 1, 9, 'smithing_table')
    plaque(b, 6, 10)
    # Interior: guard office and armoury below, bunk room above.
    b.custom(3, 2, 14, 'command_desk', facing='east')
    parts.chair(b, 2, 2, 14, 'west')
    b.chest(2, 2, 17, 'east', loot='minecraft:chests/village/village_weaponsmith')
    b.set(3, 2, 17, 'anvil', facing='east')
    b.barrel(13, 2, 17, 'up')
    b.barrel(14, 2, 17, 'up')
    b.custom(12, 2, 13, 'training_dummy', facing='west')
    for x in (4, 10):
        parts.lantern(b, x, 5, 15)
    parts.stair_run(b, 14, 12, 2, 5, 'south', wood='spruce')
    for z in range(12, 18):
        for y in (7, 8, 9):
            b.set(13, y, z, 'spruce_planks')
    b.door(13, 7, 15, facing='west', wood='spruce')
    for x in (3, 6, 9):
        b.bed(x, 7, 17, 'north', 'red')
    b.bed(11, 7, 12, 'south', 'red')
    b.chest(12, 7, 17, 'north', loot=LOOT_HOUSE)
    parts.lantern(b, 7, 9, 14)
    b.set(2, 7, 12, 'crafting_table')
    b.room('bunk_room', (8, 8, 14))
    b.resident(5, 1, 6, 'knight')
    b.resident(4, 1, 9, 'archer')
    b.entrance(8)
    b.natural_ground()
    return b


def workshop():
    """Carpenter's lumber shed and the tailor's shop under one roof line."""
    rng = random.Random(303)
    st = Style(frame='stripped_oak_log', fill='oak_planks', floor='spruce_planks', roof='spruce',
               base='cobblestone', trim='spruce', door='spruce', upper_fill='calcite')
    b = Build('workshop', (17, 18, 20))
    main = Body(b, 1, 6, 10, 15, st, heights=(3, 3), jetty=('north',), spacing=3).build()
    main.roof(axis='z', pitch=1, gable='calcite', trim=ROOFS['dark_oak'])
    main.windows(0, 'north', [(1, 2), (7, 2)], height=2, box='flowering_azalea_leaves')
    main.windows(0, 'west', [(2, 2), (6, 2)], height=1)
    main.windows(1, 'north', [(2, 2), (6, 2)], height=2, shutters=True)
    main.windows(1, 'west', [3, 6], height=1)
    main.windows(1, 'south', [(3, 2)], height=1)
    main.gable_window('north')
    parts.front_door(b, 5, 2, 6, 'north', wood='spruce', step='cobblestone_stairs')
    # Open-sided lumber shed on the east with a lean-to roof.
    for x, z in ((11, 6), (15, 6), (11, 15), (15, 15), (15, 10)):
        b.set(x, 0, z, 'cobblestone')
        for y in range(1, 5):
            b.set(x, y, z, 'stripped_spruce_log', axis='y')
    for z in range(5, 17):
        for i, x in enumerate(range(16, 10, -1)):
            b.set(x, 5 + i // 2, z, 'spruce_slab' if i % 2 == 0 else 'spruce_planks', type='bottom')
    for x in range(11, 16):
        for z in range(6, 16):
            b.set(x, 0, z, 'spruce_planks' if (x + z) % 4 else 'stripped_spruce_log', axis='x')
    b.custom(13, 1, 9, 'sawmill', facing='west')
    b.set(13, 1, 12, 'crafting_table')
    parts.woodpile(b, 15, 1, 7, 'z', length=3, wood='oak', height=3)
    parts.woodpile(b, 12, 1, 14, 'x', length=3, wood='spruce', height=2)
    for x in (11, 12):
        b.set(x, 1, 7, 'oak_planks')
    b.set(11, 2, 7, 'oak_slab', type='bottom')
    b.set(14, 1, 15, 'barrel', facing='up', open=False)
    parts.lantern(b, 13, 5, 10)
    b.resident(12, 1, 10, 'carpenter')
    # Tailor's shop on the ground floor.
    b.custom(3, 2, 13, 'sewing_table', facing='north')
    b.set(2, 2, 10, 'loom', facing='east')
    for z, c in zip(range(8, 14), ['red', 'yellow', 'blue', 'green', 'white', 'purple']):
        b.set(9, 2, z, f'{c}_wool')
        b.set(9, 3, z, f'{c}_carpet')
    parts.rug(b, 4, 9, 7, 11, 2, 'light_gray', border='blue')
    b.chest(2, 2, 14, 'east', loot=LOOT_HOUSE)
    parts.lantern(b, 5, 4, 10)
    b.resident(4, 2, 12, 'tailor')
    parts.stair_run(b, 8, 14, 2, 4, 'west', wood='spruce')
    # Bedroom above.
    for x in range(2, 10):
        for y in (6, 7, 8):
            b.set(x, y, 11, 'spruce_planks')
    b.door(3, 6, 11, facing='north', wood='spruce')
    b.bed(2, 6, 7, 'south', 'light_blue')
    b.bed(5, 6, 7, 'south', 'orange')
    b.chest(7, 6, 6, 'south', loot=LOOT_HOUSE)
    parts.lantern(b, 5, 8, 8)
    b.room('bedroom', (4, 7, 9))
    for x in range(1, 11):
        for z in range(0, 6):
            if z >= 1 and x in (1, 2, 8, 9, 10) and rng.random() < .7:
                b.set(x, 0, z, 'grass_block')
                b.set(x, 1, z, parts.flowers(rng))
    b.set(5, 0, 5, 'dirt_path')
    for x in range(11, 16):
        b.set(x, 0, 5, 'dirt_path')
    b.entrance(8)
    for z in range(0, 5):
        b.set(8, 0, z, 'dirt_path')
    for x in range(5, 9):
        b.set(x, 0, 4, 'dirt_path')
    plaque(b, 7, 4)
    b.natural_ground()
    return b


def grave(b, x, z, rng, facing='north'):
    """Headstone at (x, z) with a planted mound toward the south."""
    b.set(x, 0, z + 1, rng.choice(['podzol', 'coarse_dirt', 'rooted_dirt']))
    b.set(x, 0, z + 2, rng.choice(['podzol', 'coarse_dirt']))
    kind = rng.random()
    if kind < .4:
        b.set(x, 1, z, rng.choice(['cobblestone_wall', 'mossy_cobblestone_wall', 'stone_brick_wall']))
    elif kind < .75:
        b.set(x, 1, z, rng.choice(['stone_brick_stairs', 'mossy_stone_brick_stairs']), facing='south', half='bottom', lock=True)
    else:
        b.set(x, 1, z, 'chiseled_stone_bricks')
        b.set(x, 2, z, 'stone_brick_wall')
    if rng.random() < .6:
        b.set(x, 1, z + 1, parts.flowers(rng))


def chapel():
    """Stone chapel with a belfry and spire, stained glass and a walled graveyard."""
    rng = random.Random(304)
    b = Build('chapel', (17, 26, 21))
    st = Style(frame='stone_bricks', fill='stone_bricks', floor='polished_andesite', roof='slate',
               base='cobblestone', trim='spruce', door='dark_oak', upper_fill='stone_bricks', ceiling='spruce_planks')
    nave = Body(b, 4, 7, 12, 18, st, heights=(6,), stone_ground=True).build(ceiling=False)
    nave.roof(axis='z', pitch=1, gable='stone_bricks', trim=ROOFS['stone'])
    # Buttresses and tall stained-glass windows along the nave.
    for z in (8, 11, 14, 17):
        for x, f in ((3, 'west'), (13, 'east')):
            b.set(x, 1, z, 'cobblestone')
            b.set(x, 2, z, 'stone_bricks')
            b.set(x, 3, z, 'stone_bricks')
            b.set(x, 4, z, 'stone_brick_stairs', facing={'west': 'east', 'east': 'west'}[f], half='bottom')
    for z in (9, 10, 12, 13, 15, 16):
        if z in (9, 12, 15):
            for x in (4, 12):
                for y in (3, 4, 5):
                    b.set(x, y, z, 'yellow_stained_glass_pane' if y < 5 else 'orange_stained_glass_pane')
                    b.set(x, y, z + 1, 'white_stained_glass_pane' if y < 5 else 'orange_stained_glass_pane')
    for x in (7, 8, 9):
        for y in (3, 4, 5, 6):
            if not (y == 6 and x != 8):
                b.set(x, y, 18, 'red_stained_glass_pane' if x == 8 else 'yellow_stained_glass_pane')
    # Bell tower with an open belfry and spire.
    tx0, tz0, tx1, tz1 = 6, 3, 10, 7
    for y in range(0, 15):
        for x in range(tx0, tx1 + 1):
            for z in range(tz0, tz1 + 1):
                edge = x in (tx0, tx1) or z in (tz0, tz1)
                corner = x in (tx0, tx1) and z in (tz0, tz1)
                if y <= 1:
                    b.set(x, y, z, 'cobblestone' if edge else 'polished_andesite')
                elif edge and (y < 11 or corner or y == 14):
                    b.set(x, y, z, 'stone_bricks' if not corner else 'polished_andesite')
                elif not edge and y == 10:
                    b.set(x, y, z, 'spruce_planks')
                elif edge and 11 <= y <= 13 and not corner:
                    b.set(x, y, z, 'air')
                    if y == 13:
                        b.set(x, y, z, 'stone_brick_stairs', facing={tz0: 'north', tz1: 'south'}.get(z, 'west' if x == tx0 else 'east'),
                              half='top', lock=True)
                    elif y == 11:
                        b.set(x, y, z, 'stone_brick_slab', type='bottom')
    for x in range(tx0, tx1 + 1):
        for z in range(tz0, tz1 + 1):
            b.set(x, 14, z, 'stone_bricks')
    b.set(8, 13, 5, 'bell', attachment='ceiling', facing='north', powered=False)
    b.set(8, 12, 5, 'bell', attachment='ceiling', facing='north', powered=False)
    b.set(8, 13, 5, 'chain', axis='y')
    parts.pyramid_roof(b, tx0, tz0, tx1, tz1, 15, 'deepslate_tile_stairs', 'deepslate_tiles', pitch=3,
                       finial=['deepslate_tile_wall', 'lightning_rod'])
    for x in range(tx0 - 1, tx1 + 2):
        for z in range(tz0 - 1, tz1 + 2):
            if x in (tx0 - 1, tx1 + 1) or z in (tz0 - 1, tz1 + 1):
                f = 'south' if z == tz0 - 1 else 'north' if z == tz1 + 1 else 'east' if x == tx0 - 1 else 'west'
                b.set(x, 14, z, 'stone_brick_stairs', facing={'south': 'north', 'north': 'south', 'east': 'west',
                                                              'west': 'east'}[f], half='top', lock=True)
    for x in (7, 9):
        b.set(x, 7, tz0, 'glass_pane')
    b.door(8, 2, tz0, facing='south', wood='dark_oak')
    b.set(8, 4, tz0, 'chiseled_stone_bricks')
    b.set(8, 1, tz0 - 1, 'stone_brick_stairs', facing='south', half='bottom', lock=True)
    b.door(8, 2, tz1, facing='south', wood='dark_oak')
    # Interior: pews, altar with a brewing stand (the cleric's station) and candles.
    for z in (10, 12, 14):
        for x in (5, 6, 7, 9, 10, 11):
            b.set(x, 2, z, 'spruce_stairs', facing='north', half='bottom', lock=True, shape='straight')
    for x in range(5, 12):
        b.set(x, 1, 17, 'spruce_planks')
        b.set(x, 1, 16, 'spruce_planks')
    for x in (7, 8, 9):
        b.set(x, 2, 17, 'chiseled_stone_bricks' if x == 8 else 'stone_brick_slab', type='top')
    b.set(8, 3, 17, 'candle', candles=3, lit=True, waterlogged=False)
    b.set(7, 3, 17, 'brewing_stand')
    b.set(9, 3, 17, 'candle', candles=2, lit=True, waterlogged=False)
    for z in range(9, 16):
        b.set(8, 2, z, 'red_carpet')
    for z in (9, 13, 16):
        parts.lantern(b, 8, 9, z, chain=1)
    # Graveyard on both flanks, walled with a low fence.
    for z in range(8, 18, 3):
        for x in (1, 15):
            grave(b, x, z, rng)
    for z in (10, 16):
        grave(b, 2 if z == 10 else 14, z, rng)
    for x in range(0, 17):
        b.set(x, 1, 20, 'cobblestone_wall' if x % 4 else 'mossy_cobblestone')
    for z in range(7, 20):
        b.set(0, 1, z, 'cobblestone_wall' if z % 4 else 'mossy_cobblestone')
        b.set(16, 1, z, 'cobblestone_wall' if z % 4 else 'mossy_cobblestone')
    parts.spruce_tree(b, 14, 1, 9, height=7)
    b.custom(2, 1, 18, 'village_bench', facing='east')
    # Front: path, lanterns, flower beds.
    for z in range(0, 3):
        b.set(8, 0, z, 'stone_bricks' if z % 2 else 'cobblestone')
        b.set(7, 0, z, 'gravel')
        b.set(9, 0, z, 'gravel')
    for x in (5, 11):
        parts.lamp_post(b, x, 1, 2, height=2, fence='dark_oak_fence')
        b.set(x, 0, 2, 'cobblestone')
    for x in (1, 2, 3, 13, 14, 15):
        for z in (2, 3, 4, 5):
            b.set(x, 0, z, 'grass_block')
            if rng.random() < .6:
                b.set(x, 1, z, parts.flowers(rng))
    b.entrance(8)
    b.natural_ground()
    return b


def apothecary():
    """Narrow herbalist's house: infirmary below, the apothecary's bedroom above, herb garden in front."""
    rng = random.Random(305)
    st = Style(frame='spruce_log', fill='calcite', floor='spruce_planks', roof='dark_oak', base='mossy_cobblestone',
               trim='spruce', door='spruce', upper_fill='calcite')
    b = Build('apothecary', (11, 22, 17))
    body = Body(b, 1, 5, 9, 13, st, heights=(3, 3), jetty=('north',), spacing=4).build()
    body.roof(axis='z', pitch=2, gable='spruce_planks', trim=ROOFS['spruce'])
    body.windows(0, 'north', [(1, 2), (6, 2)], height=1, box='flowering_azalea_leaves')
    body.windows(0, 'west', [(1, 2), (5, 2)], height=1)
    body.windows(0, 'east', [(1, 2), (5, 2)], height=1)
    body.windows(1, 'north', [2, 6], height=2, shutters=True)
    body.windows(1, 'east', [3, 6], height=1)
    body.windows(1, 'west', [3], height=1)
    body.gable_window('north', height=2)
    parts.front_door(b, 5, 2, 5, 'north', wood='spruce', step='mossy_cobblestone_stairs')
    # Vines trail from the west eave.
    for z in range(5, 14):
        for y in range(body.top - 2, body.top):
            if rng.random() < .55 and b.get(0, y, z)[0] == 'minecraft:air':
                b.set(0, y, z, 'vine', east=True)
    # Infirmary and workroom.
    b.custom(2, 2, 6, 'alchemical_press', facing='east')
    b.set(2, 2, 7, 'brewing_stand')
    b.set(2, 2, 8, 'water_cauldron', level=2)
    for z in (10, 12):
        b.custom(7, 2, z, 'apothecary_cot', facing='west')
    b.set(8, 2, 11, 'potted_fern')
    b.set(2, 2, 12, 'barrel', facing='up', open=False)
    for x in (3, 4):
        b.set(x, 4, 12, 'spruce_slab', type='top')
    parts.lantern(b, 5, 4, 9)
    parts.stair_run(b, 8, 9, 2, 4, 'north', wood='spruce')
    b.resident(4, 2, 9, 'apothecary')
    # Bedroom upstairs, behind a partition that also closes off the stairwell.
    for x in range(2, 9):
        for y in (6, 7, 8):
            b.set(x, y, 8, 'spruce_planks')
    b.door(5, 6, 8, facing='south', wood='spruce')
    b.bed(3, 6, 12, 'north', 'green')
    b.chest(2, 6, 12, 'east', loot=LOOT_HOUSE)
    b.set(7, 6, 12, 'potted_azure_bluet')
    parts.lantern(b, 5, 8, 10)
    b.room('apothecary_bedroom', (5, 7, 10))
    b.set(3, 6, 6, 'brewing_stand')
    b.set(2, 6, 6, 'bookshelf')
    # Herb garden.
    for x in range(1, 10):
        for z in range(1, 4):
            if x in (4, 5, 6):
                continue
            b.set(x, 0, z, 'podzol' if x in (1, 9) else 'rooted_dirt')
            plant = rng.choice(['sweet_berry_bush', 'fern', 'short_grass', 'red_mushroom', 'brown_mushroom', 'allium', 'azure_bluet'])
            if plant == 'sweet_berry_bush':
                b.set(x, 1, z, plant, age=2)
            elif 'mushroom' in plant and x not in (1, 9):
                b.set(x, 0, z, 'podzol')
                b.set(x, 1, z, plant)
            else:
                b.set(x, 1, z, plant)
    for z in range(0, 5):
        b.set(5, 0, z, 'mossy_cobblestone' if z % 2 else 'gravel')
    plaque(b, 4, 4)
    b.set(6, 1, 4, 'lantern', hanging=False)
    b.entrance(5)
    b.natural_ground()
    return b


def library():
    """Scholar's library: stone ground floor lined with books, timbered upper floor, tall glass gable."""
    rng = random.Random(306)
    st = Style(frame='stripped_spruce_log', fill='stone_bricks', floor='dark_oak_planks', roof='slate',
               base='cobblestone', trim='dark_oak', door='dark_oak', upper_fill='calcite')
    b = Build('library', (11, 24, 17))
    body = Body(b, 1, 4, 9, 14, st, heights=(4, 3), stone_ground=True).build()
    body.roof(axis='z', pitch=2, gable='calcite', trim=ROOFS['dark_oak'])
    body.windows(0, 'north', [(1, 2), (6, 2)], height=2, shutters=False, sill='stone_brick')
    body.windows(0, 'west', [3, 7], height=2, shutters=False)
    body.windows(0, 'east', [3, 7], height=2, shutters=False)
    body.windows(1, 'north', [(2, 1), (4, 1), (6, 1)], height=2, shutters=False)
    body.windows(1, 'west', [2, 5, 8], height=2)
    body.windows(1, 'east', [2, 5, 8], height=2)
    for y in range(body.top + 1, body.top + 5):
        for x in (4, 5, 6):
            if b.get(x, y, 4)[0] == 'minecraft:calcite':
                b.set(x, y, 4, 'glass_pane')
    parts.front_door(b, 5, 2, 4, 'north', wood='dark_oak', step='stone_brick_stairs')
    # Bookshelves line the ground floor.
    for z in range(5, 14):
        for x in (2, 8):
            for y in (2, 3, 4):
                if (x == 2 and z in (7,)) or (x == 8 and z in (7, 11)):
                    continue
                if b.get(x - 1 if x == 2 else x + 1, y, z)[0] == 'minecraft:glass_pane':
                    continue
                b.set(x, y, z, 'bookshelf')
    for x in range(3, 8):
        for y in (2, 3, 4):
            b.set(x, y, 13, 'bookshelf')
    b.custom(5, 2, 12, 'archives', facing='north')
    b.set(4, 2, 9, 'lectern', facing='north', has_book=False, powered=False)
    parts.table(b, 5, 2, 7, wood='dark_oak')
    parts.chair(b, 4, 2, 7, 'west', wood='dark_oak')
    parts.chair(b, 6, 2, 7, 'east', wood='dark_oak')
    parts.lantern(b, 5, 5, 8)
    parts.lantern(b, 5, 5, 11)
    parts.stair_run(b, 7, 12, 2, 5, 'north', wood='dark_oak')
    b.resident(5, 2, 10, 'scholar')
    # Upper floor: reading gallery and the scholar's room.
    for x in range(2, 9):
        for y in (7, 8, 9):
            if x != 7:
                b.set(x, y, 10, 'dark_oak_planks')
    for z in range(11, 14):
        for y in (7, 8, 9):
            b.set(7, y, z, 'dark_oak_planks')
    b.door(4, 7, 10, facing='south', wood='dark_oak')
    b.bed(3, 7, 13, 'north', 'blue')
    b.chest(5, 7, 13, 'north', loot=LOOT_HOUSE)
    b.set(6, 7, 13, 'bookshelf')
    b.set(6, 8, 13, 'bookshelf')
    parts.lantern(b, 4, 9, 12)
    b.room('scholar_bedroom', (5, 8, 12))
    for x in (2, 3):
        for y in (7, 8):
            b.set(x, y, 5, 'bookshelf')
    parts.table(b, 5, 7, 6, wood='dark_oak')
    b.set(5, 8, 6, 'candle', candles=2, lit=True, waterlogged=False)
    parts.lantern(b, 5, 9, 7)
    # Front steps and lamps.
    for z in range(0, 4):
        b.set(5, 0, z, 'stone_bricks' if z % 2 else 'polished_andesite')
    for x in (3, 7):
        parts.lamp_post(b, x, 1, 2, height=2, fence='dark_oak_fence')
        b.set(x, 0, 2, 'stone_bricks')
    for x in (1, 2, 8, 9):
        for z in (1, 2, 3):
            b.set(x, 0, z, 'grass_block')
            if rng.random() < .5:
                b.set(x, 1, z, parts.flowers(rng))
    plaque(b, 4, 3)
    b.entrance(5)
    b.natural_ground()
    return b


def market_stalls():
    """A cluster of three market stalls around a paved yard."""
    rng = random.Random(307)
    b = Build('market_stalls', (11, 7, 11))
    for x in range(0, 11):
        for z in range(0, 11):
            if rng.random() < .85:
                b.set(x, 0, z, rng.choice(['cobblestone', 'gravel', 'stone_bricks', 'dirt_path', 'andesite']))
    from .plazas import stall
    stall(b, 1, 9, 'north', 'red', ['pumpkin', 'melon', 'hay_block[axis=y]'])
    stall(b, 9, 7, 'west', 'yellow', ['barrel[facing=up]', 'composter[level=7]', 'bee_nest[facing=west]'])
    stall(b, 1, 3, 'east', 'blue', ['hay_block[axis=y]', 'barrel[facing=up]', 'carved_pumpkin[facing=east]'])
    parts.lamp_post(b, 5, 1, 6, height=3)
    b.set(5, 0, 6, 'cobblestone')
    for x, z in ((8, 1), (9, 1), (8, 2)):
        b.barrel(x, 1, z, 'up')
    b.entrance(5)
    b.natural_ground()
    return b


def market_garden():
    """A pocket garden with a pergola, well and benches."""
    rng = random.Random(308)
    b = Build('market_garden', (11, 8, 11))
    for x in range(0, 11):
        for z in range(0, 11):
            b.set(x, 0, z, 'grass_block')
    for z in range(0, 11):
        b.set(5, 0, z, 'dirt_path' if z % 3 else 'gravel')
    for x in range(1, 10):
        b.set(x, 0, 5, 'dirt_path' if x % 3 else 'gravel')
    for x0, z0 in ((1, 1), (7, 1), (1, 7), (7, 7)):
        for x in range(x0, x0 + 3):
            for z in range(z0, z0 + 3):
                if rng.random() < .8:
                    b.set(x, 1, z, parts.flowers(rng))
    for x, z in ((3, 3), (7, 3), (3, 7), (7, 7)):
        b.set(x, 1, z, 'oak_fence')
        b.set(x, 2, z, 'oak_fence')
        b.set(x, 3, z, 'oak_fence')
    for x in range(3, 8):
        for z in (3, 7):
            b.set(x, 4, z, 'stripped_oak_log', axis='x')
    for z in range(3, 8):
        for x in (3, 7):
            if b.get(x, 4, z)[0] == 'minecraft:air':
                b.set(x, 4, z, 'stripped_oak_log', axis='z')
    for x in range(3, 8):
        for z in range(3, 8):
            if (x + z) % 2 == 0 and b.get(x, 4, z)[0] == 'minecraft:air':
                parts.bush(b, x, 4, z, 'flowering_azalea_leaves')
    for x, z, f in ((4, 5, 'east'), (6, 5, 'west')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    parts.lantern(b, 5, 3, 5)
    b.entrance(5)
    b.natural_ground()
    return b


DESIGNS = {'tavern': tavern, 'garrison': garrison, 'workshop': workshop, 'chapel': chapel,
           'apothecary': apothecary, 'library': library, 'market_stalls': market_stalls,
           'market_garden': market_garden}
