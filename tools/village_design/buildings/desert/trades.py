"""Desert workshops for the vanilla professions.

Each holds its vanilla job-site block and no residents, so unemployed villagers
from the homes nearby can take up the trade. Workshops keep other professions'
job sites out (no barrels outside the fisher's hut, no cauldrons outside the
tannery). Lots follow the drop-in contract.
"""
import random

from ...kit import Build
from ... import parts
from .homes_kit import (plinth, walls, frieze, wall_run, flat_roof, deck, parapet, lattice, lattice_row, arch, door,
                        awning, canopy_edge, pergola, dome, palm, cactus, sand_patch, dry_tuft, path_line, paving,
                        hang, stand_lamp, candle, pot, shelf, table, chair, rug, ladder)

SAND = 'smooth_sandstone'
CUT = 'cut_sandstone'
LOOT = 'minecraft:chests/village/village_'


def shell(b, x0, z0, x1, z1, h=3, fill=SAND, band=('orange_terracotta',), style='crenel'):
    """Plinth, masonry walls, painted band and a flat roof; returns the roof deck Y."""
    plinth(b, x0, z0, x1, z1)
    walls(b, x0, z0, x1, z1, 2, 1 + h, fill, corner=CUT)
    if band:
        frieze(b, x0, z0, x1, z1, 1 + h, band)
    flat_roof(b, x0, z0, x1, z1, 2 + h, style=style)
    return 2 + h


def smithy():
    """Open-fronted forge behind two sandstone arches: blast furnace, smithing table,
    grindstone and anvil, a smoking chimney and a striped canopy over the yard."""
    rng = random.Random(3101)
    b = Build('desert/smithy', (13, 11, 13))
    shell(b, 1, 4, 11, 11, band=('red_terracotta', 'orange_terracotta'))
    b.clear(2, 2, 4, 5, 4, 4)
    b.clear(7, 2, 4, 10, 4, 4)
    arch(b, (2, 4), (5, 4), 4, 'x')
    arch(b, (7, 4), (10, 4), 4, 'x')
    # Hearth and chimney.
    b.set(2, 2, 9, 'blast_furnace', facing='east', lit=True)
    b.set(2, 2, 8, 'magma_block')
    b.set(2, 3, 8, 'sandstone_stairs', facing='west', half='top', shape='straight', waterlogged=False, lock=True)
    b.set(2, 2, 7, 'blast_furnace', facing='east', lit=False)
    parts.chimney(b, 2, 8, 6, 8, 'cut_sandstone')
    b.set(4, 2, 8, 'anvil', facing='east')
    b.set(9, 2, 10, 'smithing_table')
    b.set(10, 2, 7, 'grindstone', face='floor', facing='north')
    b.chest(10, 2, 10, 'west', loot=LOOT + 'toolsmith')
    b.chest(3, 2, 10, 'north', loot=LOOT + 'armorer')
    b.chest(10, 2, 9, 'west', loot=LOOT + 'weaponsmith')
    b.set(8, 2, 10, 'crafting_table')
    b.set(6, 2, 10, 'iron_block')
    for z in (8, 9):
        b.set(6, 2, z, 'polished_granite')
    hang(b, 4, 4, 7)
    hang(b, 8, 4, 8)
    lattice_row(b, [(5, 11), (8, 11)], 3, 'south')
    lattice_row(b, [(11, 6), (11, 9)], 3, 'east')
    lattice(b, 1, 3, 6, 'west')
    # Yard and canopy.
    paving(b, 1, 1, 11, 3, rng, mats=('sandstone', 'smooth_sandstone', 'gravel', 'sand'))
    awning(b, 2, 2, 10, 3, 4, colors=('red', 'white'), posts=[(2, 2), (10, 2)])
    b.set(4, 1, 3, 'sandstone_stairs', facing='south', half='bottom', shape='straight', waterlogged=False, lock=True)
    b.set(9, 1, 3, 'sandstone_stairs', facing='south', half='bottom', shape='straight', waterlogged=False, lock=True)
    b.set(1, 1, 2, 'coal_block')
    b.set(1, 2, 2, 'coal_block')
    b.set(1, 1, 1, 'coal_block')
    b.set(11, 1, 1, 'raw_iron_block')
    b.set(11, 1, 2, 'cut_sandstone_slab', type='bottom', waterlogged=False)
    path_line(b, 4, 0, 0, rng)
    sand_patch(b, [(x, 0) for x in range(0, 13) if x != 4], rng, .25)
    b.entrance(4)
    b.natural_ground()
    return b


def butcher():
    """Butcher's shop: a counter window under a red awning, twin smokers and a
    chopping block, with a chimney over the smokehouse."""
    rng = random.Random(3102)
    b = Build('desert/butcher', (11, 10, 12))
    shell(b, 1, 4, 9, 10, band=('red_terracotta',))
    door(b, 7, 2, 4, 'north', lamp=False, frame='red_terracotta')
    # Counter window.
    b.clear(2, 3, 4, 4, 3, 4)
    for x in (2, 3, 4):
        b.set(x, 2, 4, 'smooth_sandstone_slab', type='double', waterlogged=False)
        b.set(x, 2, 5, 'acacia_slab', type='top', waterlogged=False)
    awning(b, 2, 2, 5, 3, 4, colors=('red', 'white'), posts=[(2, 2)])
    # Smokehouse corner.
    b.set(2, 2, 9, 'smoker', facing='north', lit=True)
    b.set(3, 2, 9, 'smoker', facing='north', lit=False)
    parts.chimney(b, 2, 9, 6, 7, 'cut_sandstone')
    b.set(5, 2, 8, 'stripped_acacia_log', axis='y')
    b.set(5, 3, 8, 'acacia_pressure_plate', powered=False)
    b.chest(8, 2, 9, 'north', loot=LOOT + 'butcher')
    b.set(8, 2, 6, 'crafting_table')
    for x in (4, 6):
        b.set(x, 4, 9, 'iron_chain', axis='y', waterlogged=False)
        hang(b, x, 3, 9)
    hang(b, 5, 4, 6)
    pot(b, 2, 2, 7, 'east')
    lattice_row(b, [(1, 6), (1, 8)], 3, 'west')
    lattice_row(b, [(9, 7)], 3, 'east')
    lattice_row(b, [(5, 10)], 3, 'south')
    # Street front.
    path_line(b, 7, 0, 2, rng)
    sand_patch(b, [(x, z) for x in range(0, 11) for z in (0, 1) if x != 7], rng, .2)
    b.set(9, 1, 2, 'hay_block', axis='y')
    pot(b, 9, 1, 3, 'north')
    b.entrance(7)
    b.natural_ground()
    return b


def fletcher():
    """Fletcher's hut with a sand archery range: targets on hay bales and a slatted
    shade over the shooting line."""
    rng = random.Random(3103)
    b = Build('desert/fletcher', (11, 9, 16))
    shell(b, 1, 3, 7, 8, band=('yellow_terracotta',))
    door(b, 4, 2, 3, 'north', lamp=True, frame='yellow_terracotta')
    b.set(2, 2, 7, 'fletching_table')
    b.chest(6, 2, 7, 'north', loot=LOOT + 'fletcher')
    b.set(6, 2, 4, 'crafting_table')
    for z in (5, 6):
        b.set(2, 2, z, 'hay_block', axis='z')
    b.set(2, 3, 5, 'bamboo_block', axis='y')
    hang(b, 4, 4, 6)
    lattice_row(b, [(2, 3), (6, 3)], 3, 'north')
    lattice_row(b, [(1, 5), (7, 6)], 3, 'west')
    lattice(b, 7, 3, 5, 'east')
    lattice(b, 4, 3, 8, 'south')
    # Range.
    for x in range(0, 11):
        for z in range(9, 16):
            b.set(x, 0, z, 'sand')
    for x in (2, 5, 8):
        b.set(x, 1, 15, 'hay_block', axis='y')
        b.set(x, 2, 15, 'target', power=0)
    for x in range(1, 10):
        b.set(x, 0, 10, 'cut_sandstone')
    for x in (1, 9):
        for y in (1, 2, 3):
            b.set(x, y, 10, 'acacia_fence')
    pergola(b, 1, 9, 9, 11, 4, axis='x')
    for x in (1, 9):
        b.set(x, 4, 10, 'stripped_acacia_log', axis='z')
    for x in range(2, 9):
        b.set(x, 4, 10, 'stripped_acacia_log', axis='x')
    hang(b, 5, 3, 10)
    b.set(9, 1, 12, 'hay_block', axis='x')
    dry_tuft(b, 4, 13, rng)
    dry_tuft(b, 7, 14, rng)
    # Street front.
    path_line(b, 4, 0, 2, rng)
    sand_patch(b, [(x, z) for x in range(0, 11) for z in (0, 1, 2) if x != 4] + [(8, z) for z in range(3, 9)]
               + [(9, z) for z in range(3, 9)], rng, .25)
    cactus(b, 9, 5, 2)
    b.entrance(4)
    b.natural_ground()
    return b


def weaver():
    """Weaver's workshop (shepherd): a loom among bales of dyed wool, carpets drying
    on a rail and a sheep pen with a trough."""
    rng = random.Random(3104)
    b = Build('desert/weaver', (16, 9, 15))
    shell(b, 1, 3, 7, 10, band=('cyan_terracotta', 'white_terracotta'))
    door(b, 4, 2, 3, 'north', lamp=False, frame='cyan_terracotta')
    b.set(2, 2, 9, 'loom', facing='north')
    b.chest(6, 2, 9, 'north', loot=LOOT + 'shepherd')
    for (x, z), c in zip(((2, 5), (2, 6), (2, 7), (3, 9), (2, 5)), ('white', 'red', 'yellow', 'cyan', 'orange')):
        b.set(x, 2, z, f'{c}_wool')
    b.set(2, 3, 5, 'orange_wool')
    b.set(2, 3, 6, 'white_wool')
    rug(b, 4, 6, 5, 8, 2, 'red', 'yellow')
    hang(b, 4, 4, 7)
    lattice_row(b, [(2, 3), (6, 3)], 3, 'north')
    lattice_row(b, [(1, 6), (1, 8)], 3, 'west')
    lattice_row(b, [(3, 10), (5, 10)], 3, 'south')
    lattice_row(b, [(7, 5), (7, 8)], 3, 'east')
    # Drying rail on the roof.
    for x in range(2, 7):
        b.set(x, 6, 7, 'acacia_fence')
        b.set(x, 7, 7, ('orange', 'white', 'cyan', 'yellow', 'red')[x - 2] + '_carpet')
    # Sheep pen.
    for x in range(8, 16):
        for z in range(3, 14):
            edge = x in (8, 15) or z in (3, 13)
            if edge:
                if (x, z) == (11, 3):
                    b.set(x, 1, z, 'acacia_fence_gate', facing='north', open=False, in_wall=False, powered=False)
                else:
                    b.set(x, 1, z, 'acacia_fence')
            else:
                b.set(x, 0, z, 'sand' if rng.random() < .7 else 'coarse_dirt')
                if rng.random() < .1:
                    b.set(x, 1, z, 'short_dry_grass')
    for z in (11, 12):
        b.set(14, 1, z, 'hay_block', axis='z')
    for x in (10, 11, 12):
        b.set(x, 0, 12, 'water', level=0)
        b.set(x, 1, 12, 'air')
    for x, z in ((10, 6), (13, 8), (11, 10)):
        b.animal(x, 1, z, 'sheep')
    awning(b, 13, 4, 14, 6, 3, colors=('cyan', 'white'), posts=[(13, 6)])
    # Street front.
    path_line(b, 4, 0, 2, rng)
    path_line(b, 11, 0, 2, rng)
    sand_patch(b, [(x, z) for x in range(0, 16) for z in (0, 1, 2) if x not in (4, 11)], rng, .2)
    b.entrance(4)
    b.natural_ground()
    return b


def fisher():
    """Fisher's hut on an oasis pond: a jetty, reeds of sugar cane, a palm and a
    drying rack."""
    rng = random.Random(3105)
    b = Build('desert/fisher', (13, 10, 15))
    shell(b, 1, 3, 6, 8, band=('cyan_terracotta',))
    door(b, 3, 2, 3, 'north', lamp=True, frame='cyan_terracotta')
    b.barrel(5, 2, 7, 'up', loot=LOOT + 'fisher')
    b.set(2, 2, 7, 'crafting_table')
    pot(b, 5, 2, 4, 'west')
    hang(b, 3, 4, 5)
    lattice_row(b, [(5, 3)], 3, 'north')
    lattice_row(b, [(6, 5), (6, 7)], 3, 'east')
    lattice(b, 1, 3, 6, 'west')
    # Pond.
    water = set()
    for x in range(0, 13):
        for z in range(9, 15):
            dx, dz = (x - 6.5) / 5.2, (z - 11.8) / 2.6
            r = dx * dx + dz * dz
            if r <= 1:
                b.set(x, 0, z, 'water', level=0)
                water.add((x, z))
            elif r <= 1.7:
                b.set(x, 0, z, rng.choice(['sand', 'sand', 'sandstone', 'smooth_sandstone']))
    for x, z in ((2, 10), (11, 11), (3, 13), (10, 13)):
        if (x, z) not in water and any((x + dx, z + dz) in water for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            b.set(x, 0, z, 'sand')
            b.set(x, 1, z, 'sugar_cane', age=0)
            b.set(x, 2, z, 'sugar_cane', age=0)
    for z in range(8, 13):
        b.set(7, 1, z, 'jungle_slab', type='bottom', waterlogged=False)
    b.set(7, 0, 8, 'sandstone')
    b.set(8, 1, 12, 'jungle_fence')
    stand_lamp(b, 8, 2, 12)
    # Drying rack and palm.
    for x in (8, 10):
        b.set(x, 1, 5, 'jungle_fence')
        b.set(x, 2, 5, 'jungle_fence')
    b.set(9, 2, 5, 'jungle_fence')
    b.set(9, 3, 5, 'dried_kelp_block')
    b.set(11, 0, 7, 'sand')
    palm(b, 11, 1, 7, height=6, lean='north')
    # Street front.
    path_line(b, 3, 0, 2, rng)
    sand_patch(b, [(x, z) for x in range(0, 13) for z in (0, 1, 2) if x != 3] + [(x, z) for x in range(7, 13)
               for z in range(3, 9) if (x, z) != (11, 7)], rng, .2)
    b.entrance(3)
    b.natural_ground()
    return b


def cartographer():
    """A slim three-storey map tower with a domed lookout, reached by ladders."""
    rng = random.Random(3106)
    b = Build('desert/cartographer', (9, 19, 11))
    plinth(b, 1, 3, 7, 9)
    for y0 in (2, 6, 10):
        walls(b, 1, 3, 7, 9, y0, y0 + 2, SAND, corner=CUT)
        frieze(b, 1, 3, 7, 9, y0 + 2, ('white_terracotta', 'light_blue_terracotta'))
        deck(b, 1, 3, 7, 9, y0 + 3)
    parapet(b, 1, 3, 7, 9, 14)
    door(b, 4, 2, 3, 'north', lamp=True, frame='light_blue_terracotta')
    ladder(b, 6, 2, 13, 8, 'west')
    b.set(2, 2, 8, 'cartography_table')
    b.chest(2, 2, 7, 'east', loot=LOOT + 'cartographer')
    b.set(2, 2, 4, 'bookshelf')
    hang(b, 4, 4, 6)
    # Map room and study above.
    table(b, 3, 6, 6, cloth='white_carpet')
    chair(b, 3, 6, 7, 'south')
    b.set(2, 6, 8, 'bookshelf')
    b.set(2, 7, 8, 'bookshelf')
    pot(b, 2, 6, 4, 'east')
    hang(b, 4, 8, 6)
    rug(b, 2, 5, 5, 7, 10, 'light_blue', 'white')
    b.custom(3, 10, 7, 'fireside_armchair', facing='north')
    candle(b, 2, 10, 4, 3)
    b.set(2, 9, 4, SAND)
    hang(b, 4, 12, 6)
    for y in (3, 7, 11):
        lattice_row(b, [(3, 3), (5, 3)], y, 'north', height=1 if y == 3 else 2)
        lattice_row(b, [(1, 6)], y, 'west', height=1 if y == 3 else 2)
        lattice_row(b, [(4, 9)], y, 'south', height=1 if y == 3 else 2)
        lattice_row(b, [(7, 5)], y, 'east', height=1 if y == 3 else 2)
    # Lookout: a little domed kiosk on four posts.
    for x, z in ((2, 4), (4, 4), (2, 6), (4, 6)):
        for y in (15, 16):
            b.set(x, y, z, 'sandstone_wall')
    deck(b, 2, 4, 4, 6, 17, CUT, CUT)
    dome(b, 3, 5, 18, 1, mat=SAND, finial=None)
    b.set(3, 18, 5, 'chiseled_sandstone')
    hang(b, 3, 16, 5)
    # Street front.
    path_line(b, 4, 0, 2, rng)
    sand_patch(b, [(x, z) for x in range(0, 9) for z in (0, 1, 2) if x != 4], rng, .25)
    b.entrance(4)
    b.natural_ground()
    return b


def mason():
    """Mason's yard: a stonecutter under a canopy, stacked sandstone blocks and a
    half-built wall on scaffolding."""
    rng = random.Random(3107)
    b = Build('desert/mason', (11, 8, 11))
    paving(b, 0, 1, 10, 10, rng, mats=('sandstone', 'sand', 'smooth_sandstone', 'gravel', 'cut_sandstone'))
    for x, z in ((1, 5), (5, 5), (1, 9), (5, 9)):
        for y in (1, 2, 3):
            b.set(x, y, z, 'stripped_acacia_log', axis='y')
    awning(b, 0, 5, 6, 9, 4, colors=('yellow', 'white'), stripe='z')
    b.set(3, 1, 7, 'stonecutter', facing='north')
    b.chest(2, 1, 9, 'north', loot=LOOT + 'mason')
    hang(b, 3, 3, 7)
    for x in range(7, 11):
        for y in range(1, 3 if x < 10 else 2):
            b.set(x, y, 9, rng.choice(['sandstone', 'cut_sandstone', 'smooth_sandstone', 'chiseled_sandstone']))
    for x in (7, 8):
        b.set(x, 3, 9, 'scaffolding', distance=0, bottom=False, waterlogged=False)
    for x, z, m in ((7, 3, 'cut_sandstone'), (8, 3, 'smooth_sandstone'), (7, 4, 'sandstone'), (7, 3, 'cut_sandstone')):
        b.set(x, 1, z, m)
    b.set(7, 2, 3, 'smooth_sandstone_slab', type='bottom', waterlogged=False)
    b.set(9, 1, 5, 'sandstone_stairs', facing='west', half='bottom')
    b.set(9, 1, 6, 'cut_sandstone_slab', type='bottom', waterlogged=False)
    b.set(2, 1, 2, 'sandstone_wall')
    stand_lamp(b, 2, 2, 2)
    for x in range(0, 11):
        if x != 5:
            b.set(x, 0, 0, 'sand')
    path_line(b, 5, 0, 1, rng)
    b.entrance(5)
    b.natural_ground()
    return b


def tannery():
    """Leatherworker's tannery: a honeycomb of dye pits in front of the workshop,
    hides drying on the roof rail."""
    rng = random.Random(3108)
    b = Build('desert/tannery', (13, 10, 14))
    dyes = ['red_terracotta', 'yellow_terracotta', 'white_terracotta', 'brown_terracotta', 'orange_terracotta',
            'cyan_terracotta', 'yellow_terracotta', 'red_terracotta', 'white_terracotta', 'orange_terracotta']
    i = 0
    for x in range(1, 12):
        for z in range(2, 8):
            pit = x % 2 == 0 and z in (3, 5) and x != 6
            b.set(x, 0, z, dyes[i % len(dyes)] if pit else 'sandstone')
            if pit:
                i += 1
                b.set(x, 1, z, 'water', level=0)
            else:
                b.set(x, 1, z, CUT if z != 7 else SAND)
    b.set(6, 1, 1, 'sandstone_stairs', facing='south', half='bottom', shape='straight', waterlogged=False, lock=True)
    # Workshop.
    shell(b, 3, 8, 10, 12, band=('brown_terracotta',))
    door(b, 6, 2, 8, 'north', step=None, lamp=False, frame='brown_terracotta')
    b.set(4, 2, 11, 'cauldron')
    b.chest(9, 2, 11, 'north', loot=LOOT + 'tannery')
    b.set(9, 2, 9, 'crafting_table')
    for x in (5, 6):
        b.set(x, 2, 11, 'brown_wool')
    b.set(4, 2, 9, 'acacia_fence')
    b.set(4, 3, 9, 'brown_carpet')
    hang(b, 6, 4, 10)
    lattice_row(b, [(4, 8), (8, 8)], 3, 'north')
    lattice_row(b, [(3, 10), (10, 10)], 3, 'west')
    lattice(b, 10, 3, 10, 'east')
    lattice(b, 6, 3, 12, 'south')
    # Hides drying on the roof.
    for x in range(4, 10):
        b.set(x, 7, 10, 'acacia_fence')
        b.set(x, 8, 10, ('brown', 'orange', 'yellow', 'brown', 'red', 'white')[x - 4] + '_carpet')
    for x in (4, 9):
        b.set(x, 7, 9, 'acacia_fence')
    # Street front.
    path_line(b, 6, 0, 1, rng)
    sand_patch(b, [(x, z) for x in range(0, 13) for z in (0, 1) if x != 6] + [(0, z) for z in range(2, 14)]
               + [(12, z) for z in range(2, 14)], rng, .2)
    b.entrance(6)
    b.natural_ground()
    return b


def scribe():
    """Scribe's house (librarian): a domed reading room lined with shelves around a lectern."""
    rng = random.Random(3109)
    b = Build('desert/scribe', (11, 13, 12))
    top = shell(b, 1, 3, 9, 10, h=4, band=('white_terracotta', 'light_blue_terracotta'), style='low')
    dome(b, 5, 6.5, top, 3, mat=SAND)
    door(b, 5, 2, 3, 'north', lamp=True, frame='light_blue_terracotta')
    b.set(5, 2, 8, 'lectern', facing='north', has_book=False, powered=False)
    for z in range(5, 10):
        for y in (2, 3, 4):
            b.set(2, y, z, 'bookshelf' if (z + y) % 3 else 'chiseled_bookshelf')
            b.set(8, y, z, 'bookshelf' if (z + y) % 4 else 'chiseled_bookshelf')
    for z in range(5, 10):
        for y in (2, 3, 4):
            s = b.get(2, y, z)
            if s[0].endswith('chiseled_bookshelf'):
                b.set(2, y, z, 'chiseled_bookshelf', facing='east')
            s = b.get(8, y, z)
            if s[0].endswith('chiseled_bookshelf'):
                b.set(8, y, z, 'chiseled_bookshelf', facing='west')
    rug(b, 4, 5, 6, 7, 2, 'light_blue', 'white')
    b.custom(4, 2, 6, 'fireside_armchair', facing='east')
    table(b, 5, 2, 5, cloth='white_carpet')
    candle(b, 3, 2, 9, 3)
    b.set(3, 1, 9, SAND)
    candle(b, 7, 2, 9, 2)
    b.set(7, 1, 9, SAND)
    hang(b, 5, 5, 7)
    lattice_row(b, [(3, 3), (7, 3)], 3, 'north', height=2)
    lattice_row(b, [(4, 10), (6, 10)], 3, 'south', height=2)
    path_line(b, 5, 0, 2, rng)
    sand_patch(b, [(x, z) for x in range(0, 11) for z in (0, 1, 2) if x != 5], rng, .25)
    pot(b, 3, 1, 2, 'north')
    pot(b, 7, 1, 2, 'north')
    b.entrance(5)
    b.natural_ground()
    return b


DESIGNS = {'desert/smithy': smithy, 'desert/butcher': butcher, 'desert/fletcher': fletcher,
           'desert/weaver': weaver, 'desert/fisher': fisher, 'desert/cartographer': cartographer,
           'desert/mason': mason, 'desert/tannery': tannery, 'desert/scribe': scribe}
