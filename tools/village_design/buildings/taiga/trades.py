"""Taiga workplaces for the vanilla professions.

Each holds the vanilla job site block so unemployed residents of nearby homes
can take up the trade. No residents live here. Lots follow the drop-in contract.
"""
import random

from ...kit import Build
from ... import parts
from ...parts import log
from . import homes_logs as H

LOOT = 'minecraft:chests/village/village_'


def chained_lantern(b, x, y, z, links):
    """Lantern hanging at ``y`` on ``links`` chain links (the top link must hang from something solid)."""
    for i in range(1, links + 1):
        b.set(x, y + i, z, 'iron_chain', axis='y', waterlogged=False)
    b.set(x, y, z, 'lantern', hanging=True, waterlogged=False)


def smithy():
    """Log forge hall, open to the street between stout posts: blast furnace, smithing table, grindstone."""
    rng = random.Random(4201)
    b = Build('taiga/smithy', (13, 13, 14))
    H.rubble(b, 1, 4, 11, 11, rng, floor='cobblestone')
    for x in range(2, 11):
        for z in range(5, 11):
            b.set(x, 1, z, rng.choice(['cobblestone', 'stone_bricks', 'andesite', 'cobblestone', 'gravel']))
    H.log_walls(b, 1, 4, 11, 11, 2, 5)
    # Stone back wall around the forge.
    for x in range(1, 6):
        for y in (2, 3, 4):
            b.set(x, y, 11, rng.choice(['cobblestone', 'mossy_cobblestone', 'stone_bricks']))
    # Open the front between log posts; the top course stays as a lintel beam.
    for x in range(2, 11):
        if x != 6:
            b.clear(x, 2, 4, x, 4, 4)
    for x in (1, 6, 11):
        for y in (2, 3, 4):
            b.set(x, y, 4, 'spruce_log', axis='y')
    for x in range(2, 11):
        if x != 6:
            b.set(x, 1, 4, 'stone_bricks')
    ridge = H.roof(b, 1, 4, 11, 11, 5, 'dark_oak', axis='x', pitch=1, gable=log('spruce_log', 'z'), trim='spruce')
    H.window(b, 1, 3, 7, 'west')
    H.window(b, 11, 3, 8, 'east')
    H.window(b, 8, 3, 11, 'south')
    # Forge: stone hearth with a lava trough under a stone hood and a tall chimney.
    for x in (2, 3, 4):
        b.set(x, 2, 10, 'stone_bricks')
        b.set(x, 3, 10, 'stone_brick_stairs', facing='south', half='top', lock=True)
        b.set(x, 4, 10, 'stone_bricks')
        b.set(x, 5, 10, 'cobblestone')
    b.set(3, 2, 10, 'lava_cauldron')
    H.chimney(b, 3, 10, 6, ridge + 1, rng)
    b.set(2, 2, 9, 'blast_furnace', facing='east', lit=True)
    b.set(5, 2, 8, 'anvil', facing='east')
    b.set(9, 2, 10, 'smithing_table')
    b.set(10, 2, 9, 'grindstone', face='floor', facing='north')
    b.barrel(10, 2, 10, 'up', loot=LOOT + 'toolsmith')
    b.chest(7, 2, 10, 'north', loot=LOOT + 'armorer')
    b.barrel(2, 2, 5, 'up', loot=LOOT + 'weaponsmith')
    b.set(5, 2, 10, 'water_cauldron', level=3)
    for z in (6, 7):
        b.set(10, 3, z, 'spruce_trapdoor', facing='west', half='top', open=True, powered=False, waterlogged=False)
    chained_lantern(b, 6, 5, 7, 3)
    chained_lantern(b, 9, 4, 6, 3)
    # Forecourt: coal heap, quench barrel, log store.
    H.path(b, 6, 0, 2, rng)
    for x in range(2, 11):
        b.set(x, 0, 3, rng.choice(['gravel', 'cobblestone', 'coarse_dirt', 'gravel']))
    b.set(1, 1, 2, 'coal_block')
    b.set(1, 2, 2, 'coal_block') if rng.random() < .5 else None
    b.set(2, 1, 2, 'barrel', facing='up', open=False)
    b.set(10, 1, 2, 'water_cauldron', level=2)
    H.lantern_post(b, 11, 1, 2, height=2)
    H.woodpile(b, 12, 1, 6, 'z', length=4)
    b.entrance(6)
    H.undergrowth(b, [(x, z) for x in range(13) for z in (0, 1, 12, 13)], rng, .25)
    b.natural_ground()
    return b


def smokehouse():
    """The butcher's smokehouse: steep log house with smokers inside and a smoking rack over fire pits."""
    rng = random.Random(4202)
    b = Build('taiga/smokehouse', (13, 15, 13))
    H.rubble(b, 1, 4, 7, 10, rng)
    H.log_walls(b, 1, 4, 7, 10, 2, 4, wood='spruce_log', chink='stripped_spruce_log')
    ridge = H.roof(b, 1, 4, 7, 10, 4, 'dark_oak', axis='z', pitch=2, gable=log('stripped_spruce_log', 'x'),
                   trim='spruce')
    H.door(b, 4, 2, 4, 'north')
    H.window(b, 7, 3, 7, 'east')
    b.set(4, 6, 4, 'glass_pane')
    # Smokers and the cold store.
    b.set(2, 2, 9, 'smoker', facing='east', lit=True)
    b.set(3, 2, 9, 'smoker', facing='north', lit=True)
    b.set(2, 3, 9, 'cobblestone')
    b.set(3, 3, 9, 'cobblestone')
    H.chimney(b, 2, 9, 4, ridge, rng)
    b.barrel(6, 2, 9, 'up', loot=LOOT + 'butcher')
    b.barrel(6, 2, 8, 'west')
    b.set(5, 2, 9, 'hay_block', axis='y')
    b.set(2, 2, 5, 'crafting_table')
    for x, z in ((3, 7), (5, 7)):
        chained_lantern(b, x, 4, z, 2)
    for z in (5, 6, 7):
        b.set(6, 4, z, 'spruce_fence')
    # Smoking rack: fire pits under a fence rail, roofed with slabs.
    for z in (5, 6, 7, 8):
        b.set(9, 0, z, 'cobblestone')
        b.set(11, 0, z, 'cobblestone')
        b.set(10, 0, z, 'campfire', lit=True, signal_fire=False, facing='west', waterlogged=False) \
            if z in (5, 7) else b.set(10, 0, z, 'coarse_dirt')
    for z in (4, 9):
        for y in (1, 2, 3):
            b.set(9, y, z, 'spruce_log', axis='y')
            b.set(11, y, z, 'spruce_log', axis='y')
    for z in range(4, 10):
        b.set(10, 3, z, 'spruce_fence')
        b.set(9, 4, z, 'spruce_stairs', facing='east', half='bottom')
        b.set(10, 4, z, 'spruce_slab', type='bottom', waterlogged=False)
        b.set(11, 4, z, 'spruce_stairs', facing='west', half='bottom')
    for z in (5, 6, 7, 8):
        b.set(9, 3, z, 'spruce_fence')
        b.set(11, 3, z, 'spruce_fence')
    for z in (5, 7):
        b.set(10, 2, z, 'iron_chain', axis='y', waterlogged=False)
    b.set(12, 1, 6, 'hay_block', axis='z')
    b.set(12, 1, 7, 'hay_block', axis='y')
    H.woodpile(b, 9, 1, 11, 'x', length=3)
    H.path(b, 4, 0, 2, rng)
    b.set(4, 0, 3, 'dirt_path')
    b.entrance(4)
    H.undergrowth(b, [(x, z) for x in range(13) for z in (0, 1, 12)], rng, .25)
    b.natural_ground()
    return b


def fletcher():
    """Fletcher's hut with an archery range of hay-backed targets."""
    rng = random.Random(4203)
    b = Build('taiga/fletcher', (12, 12, 16))
    H.rubble(b, 2, 3, 8, 8, rng)
    H.log_walls(b, 2, 3, 8, 8, 2, 4)
    ridge = H.roof(b, 2, 3, 8, 8, 4, 'spruce', axis='x', pitch=2, gable=log('stripped_spruce_log', 'z'),
                   trim='dark_oak')
    H.door(b, 5, 2, 3, 'north')
    H.window(b, 3, 3, 3, 'north')
    H.window(b, 7, 3, 3, 'north')
    H.window(b, 4, 3, 8, 'south', width=2)
    b.set(2, 6, 5, 'glass_pane')
    b.set(2, 6, 6, 'glass_pane')
    b.set(3, 2, 7, 'fletching_table')
    b.barrel(7, 2, 7, 'up', loot=LOOT + 'fletcher')
    b.set(7, 2, 4, 'crafting_table')
    b.set(3, 2, 4, 'barrel', facing='up', open=False)
    for z in (5, 6):
        b.set(8 - 1, 3, z, 'spruce_trapdoor', facing='west', half='top', open=True, powered=False, waterlogged=False)
    H.wall_hide(b, 5, 3, 7, 'north', 'green')
    b.set(5, 5, 5, 'lantern', hanging=True, waterlogged=False)
    b.set(5, 5, 6, 'spruce_planks')
    H.hearth(b, 8, 6, 2, 'west', rng, top=ridge)
    # Range: targets on hay against a log backstop.
    for x in range(1, 11):
        b.set(x, 0, 11, 'coarse_dirt' if x % 2 else 'dirt_path')
    for x in (2, 5, 8):
        b.set(x, 1, 13, 'hay_block', axis='y')
        b.set(x, 2, 13, 'target', power=0)
    for x in range(1, 11):
        b.set(x, 1, 14, log('spruce_log', 'x'))
        if x % 3 == 1:
            b.set(x, 2, 14, log('spruce_log', 'x'))
    b.set(10, 1, 10, 'spruce_fence')
    b.set(10, 2, 10, 'lantern', waterlogged=False)
    H.path(b, 5, 0, 2, rng)
    b.set(9, 1, 1, 'barrel', facing='up', open=False)
    H.drying_rack(b, 9, 4, 1, length=2, axis='z', hides=('white', 'brown'))
    b.entrance(5)
    H.undergrowth(b, [(x, z) for x in range(12) for z in (0, 1, 9, 15)], rng, .3)
    b.natural_ground()
    return b


def shepherd():
    """Shepherd's log barn with a loom and a fenced sheep pen."""
    rng = random.Random(4204)
    b = Build('taiga/shepherd', (16, 13, 16))
    H.rubble(b, 1, 3, 7, 10, rng)
    H.log_walls(b, 1, 3, 7, 10, 2, 5, chink='stripped_spruce_log')
    for z in range(5, 9):
        b.clear(7, 2, z, 7, 4, z)
        b.set(7, 1, z, 'spruce_planks')
    for z in (4, 9):
        for y in (2, 3, 4):
            b.set(7, y, z, 'spruce_log', axis='y')
    H.roof(b, 1, 3, 7, 10, 5, 'dark_oak', axis='z', pitch=1, gable=log('spruce_log', 'x'), trim='spruce')
    H.door(b, 4, 2, 3, 'north')
    H.window(b, 1, 3, 6, 'west', width=2)
    b.set(4, 7, 3, 'glass_pane')
    b.set(2, 2, 9, 'loom', facing='east')
    for z, c in zip((5, 6, 7), ('white', 'light_gray', 'brown')):
        b.set(2, 2, z, f'{c}_wool')
    b.set(2, 3, 6, 'white_wool')
    b.chest(5, 2, 9, 'north', loot=LOOT + 'shepherd')
    b.set(4, 2, 9, 'hay_block', axis='y')
    b.set(3, 2, 9, 'hay_block', axis='x')
    b.set(4, 3, 9, 'hay_block', axis='y')
    b.set(4, 5, 6, 'lantern', hanging=True, waterlogged=False)
    b.set(4, 6, 6, 'spruce_planks')
    # Sheep pen opening off the barn.
    for x in range(8, 16):
        for z in range(3, 15):
            edge = x == 15 or z in (3, 14)
            if x == 8 and not (5 <= z <= 8):
                edge = True
            if edge and not (x == 8 and 4 <= z <= 9):
                b.set(x, 1, z, 'spruce_fence')
            elif not edge and x > 8 and rng.random() < .12:
                b.set(x, 1, z, rng.choice(['short_grass', 'fern']))
    for z in (10, 11, 12, 13):
        b.set(8, 1, z, 'spruce_fence')
    b.set(8, 1, 3, 'spruce_fence')
    H.gate(b, 11, 1, 3)
    b.set(14, 1, 13, 'hay_block', axis='y')
    b.set(13, 1, 13, 'water_cauldron', level=3)
    b.set(15, 2, 3, 'lantern', waterlogged=False)
    for x, z in ((10, 6), (12, 9), (11, 11), (13, 6)):
        b.animal(x, 1, z, 'sheep')
    H.path(b, 4, 0, 2, rng)
    b.set(11, 0, 2, 'dirt_path')
    b.entrance(4)
    H.undergrowth(b, [(x, z) for x in range(8) for z in (0, 1, 12, 13, 14, 15)], rng, .3)
    b.natural_ground()
    return b


def fisher():
    """Fisher's dock hut on a still pond, with a plank jetty on log piles."""
    rng = random.Random(4205)
    b = Build('taiga/fisher', (14, 11, 16))
    H.rubble(b, 1, 3, 6, 8, rng)
    H.log_walls(b, 1, 3, 6, 8, 2, 4)
    H.roof(b, 1, 3, 6, 8, 4, 'spruce', axis='x', pitch=1, gable=log('stripped_spruce_log', 'z'), trim='dark_oak')
    H.door(b, 3, 2, 3, 'north')
    H.window(b, 6, 3, 5, 'east', width=2)
    H.window(b, 5, 3, 3, 'north')
    H.window(b, 3, 3, 8, 'south')
    b.barrel(5, 2, 7, 'up', loot=LOOT + 'fisher')
    b.barrel(5, 2, 6, 'up')
    b.set(2, 2, 7, 'crafting_table')
    b.set(2, 2, 4, 'barrel', facing='north', open=False)
    b.set(3, 4, 6, 'lantern', hanging=True, waterlogged=False)
    b.set(3, 5, 6, 'spruce_planks')
    # Pond with a clay and gravel rim.
    for x in range(3, 14):
        for z in range(9, 16):
            dx, dz = (x - 8.5) / 5.2, (z - 12.2) / 3.2
            r = dx * dx + dz * dz
            if r <= 1:
                b.set(x, 0, z, 'water', level=0)
            elif r <= 1.55:
                b.set(x, 0, z, rng.choice(['gravel', 'clay', 'podzol', 'coarse_dirt', 'gravel']))
    # Jetty from the hut's back door side out over the water.
    for z in range(9, 14):
        b.set(7, 1, z, 'spruce_slab', type='bottom', waterlogged=False)
        b.set(8, 1, z, 'spruce_slab', type='bottom', waterlogged=False)
    for x, z in ((7, 13), (8, 13), (7, 10), (8, 10)):
        b.set(x, 0, z, 'spruce_log', axis='y')
    b.set(9, 1, 13, 'spruce_fence')
    b.set(9, 2, 13, 'lantern', waterlogged=False)
    b.set(6, 1, 9, 'barrel', facing='up', open=False)
    for x, z in ((11, 11), (5, 12), (10, 14)):
        if b.get(x, 0, z)[0] == 'minecraft:water':
            b.set(x, 1, z, 'lily_pad')
    # Net drying rack beside the hut.
    for z in (3, 5, 7):
        b.set(8, 1, z, 'spruce_fence')
        b.set(8, 2, z, 'spruce_fence')
    for z in range(3, 8):
        b.set(8, 3, z, 'spruce_fence')
    for z in (4, 5, 6):
        b.set(8, 4, z, 'white_carpet' if z != 5 else 'light_gray_carpet')
    b.set(9, 1, 4, 'dried_kelp_block')
    b.set(9, 1, 5, 'barrel', facing='up', open=False)
    H.path(b, 3, 0, 2, rng)
    b.entrance(3)
    H.undergrowth(b, [(x, z) for x in range(14) for z in (0, 1)] + [(x, z) for x in (10, 11, 12, 13)
                                                                    for z in range(2, 9)], rng, .3)
    b.natural_ground()
    return b


def cartographer():
    """A log watchtower: map room below, study above, a roofed lookout deck on top."""
    rng = random.Random(4206)
    b = Build('taiga/cartographer', (11, 22, 13))
    H.rubble(b, 2, 3, 8, 9, rng)
    H.log_walls(b, 2, 3, 8, 9, 2, 9)
    H.ceiling(b, 3, 4, 7, 8, 6)
    # Lookout deck one block wider than the tower.
    b.fill(1, 10, 2, 9, 10, 10, 'spruce_planks')
    for x, z, facing, corner in parts.ring(1, 2, 9, 10):
        if corner:
            for y in (11, 12, 13):
                b.set(x, y, z, 'spruce_log', axis='y')
        else:
            b.set(x, 11, z, 'spruce_fence')
    for x in range(2, 9):
        b.set(x, 9, 2, 'spruce_stairs', facing='south', half='top', lock=True)
        b.set(x, 9, 10, 'spruce_stairs', facing='north', half='top', lock=True)
    for z in range(3, 10):
        b.set(1, 9, z, 'spruce_stairs', facing='east', half='top', lock=True)
        b.set(9, 9, z, 'spruce_stairs', facing='west', half='top', lock=True)
    parts.pyramid_roof(b, 0, 1, 10, 11, 14, 'dark_oak_stairs', 'dark_oak_planks', pitch=1,
                       finial=['spruce_fence', 'lightning_rod'])
    b.clear(1, 14, 2, 9, 14, 10)
    for x in range(1, 10):
        for z in range(2, 11):
            if x in (1, 9) or z in (2, 10):
                b.set(x, 14, z, 'dark_oak_planks')
    # Stairs: ground to study, study to the deck.
    parts.stair_run(b, 7, 8, 2, 5, 'north', wood='spruce')
    parts.stair_run(b, 3, 4, 7, 4, 'south', wood='spruce')
    H.door(b, 5, 2, 3, 'north')
    H.window(b, 3, 3, 3, 'north')
    H.window(b, 2, 3, 6, 'west', height=2)
    H.window(b, 8, 3, 5, 'east')
    for side, (x, z) in (('north', (5, 3)), ('south', (5, 9)), ('west', (2, 6)), ('east', (8, 6))):
        H.window(b, x, 7, z, side, height=2, shutters=True)
    # Map room.
    b.set(3, 2, 8, 'cartography_table')
    b.chest(3, 2, 7, 'east', loot=LOOT + 'cartographer')
    b.set(5, 2, 8, 'bookshelf')
    b.set(4, 2, 8, 'bookshelf')
    b.set(5, 3, 8, 'potted_fern')
    b.set(5, 5, 6, 'lantern', hanging=True, waterlogged=False)
    # Study.
    H.table(b, 5, 7, 7)
    b.set(5, 8, 7, 'white_carpet')
    H.chair(b, 6, 7, 7, 'east')
    b.set(5, 9, 5, 'lantern', hanging=True, waterlogged=False)
    b.set(7, 7, 4, 'barrel', facing='up', open=False)
    b.set(5, 13, 6, 'lantern', hanging=True, waterlogged=False)
    b.set(5, 14, 6, 'dark_oak_planks')
    H.path(b, 5, 0, 2, rng)
    b.entrance(5)
    H.undergrowth(b, [(x, z) for x in range(11) for z in (0, 1, 11, 12)], rng, .3)
    b.natural_ground()
    return b


def mason():
    """Mason's yard: stonecutter under a log lean-to, cut stone stacked by a half-built wall."""
    rng = random.Random(4207)
    b = Build('taiga/mason', (12, 9, 12))
    for x in range(1, 11):
        for z in range(2, 11):
            b.set(x, 0, z, rng.choice(['gravel', 'cobblestone', 'andesite', 'coarse_dirt', 'stone', 'gravel']))
    for x, z in ((1, 6), (6, 6), (1, 10), (6, 10)):
        for y in (1, 2, 3):
            b.set(x, y, z, 'spruce_log', axis='y')
    for x in range(0, 8):
        b.set(x, 4, 6, 'spruce_stairs', facing='south', half='bottom')
        for z in range(7, 11):
            b.set(x, 4, z, 'spruce_slab', type='bottom', waterlogged=False)
    for z in (6, 10):
        b.set(2, 3, z, log('spruce_log', 'x'))
        b.set(3, 3, z, log('spruce_log', 'x'))
        b.set(4, 3, z, log('spruce_log', 'x'))
        b.set(5, 3, z, log('spruce_log', 'x'))
    b.set(3, 1, 8, 'stonecutter', facing='north')
    b.chest(2, 1, 10, 'north', loot=LOOT + 'mason')
    b.set(5, 1, 9, 'crafting_table')
    b.set(4, 3, 8, 'lantern', hanging=True, waterlogged=False)
    # Half-built mossy wall and cut stone piles.
    for x in range(8, 11):
        for y in range(1, 4 if x < 10 else 2):
            b.set(x, y, 9, rng.choice(['stone_bricks', 'mossy_stone_bricks', 'cobblestone', 'mossy_cobblestone']))
    b.set(10, 2, 9, 'stone_brick_slab', type='bottom', waterlogged=False)
    b.set(8, 4, 9, 'mossy_stone_brick_stairs', facing='east', half='bottom')
    for x, z, y in ((8, 3, 1), (9, 3, 1), (8, 4, 1), (8, 3, 2), (9, 6, 1), (10, 6, 1), (10, 5, 1)):
        b.set(x, y, z, rng.choice(['stone_bricks', 'cobblestone', 'polished_andesite', 'mossy_stone_bricks']))
    b.set(9, 2, 3, 'stone_brick_slab', type='bottom', waterlogged=False)
    b.set(2, 1, 3, 'mossy_cobblestone_wall')
    b.set(2, 2, 3, 'lantern', waterlogged=False)
    b.set(3, 1, 3, 'barrel', facing='up', open=False)
    # A mossy boulder the mason is quarrying.
    for x, y, z in ((10, 1, 2), (10, 2, 2), (9, 1, 2), (10, 1, 3)):
        b.set(x, y, z, rng.choice(['mossy_cobblestone', 'stone', 'cobblestone']))
    H.path(b, 5, 0, 1, rng)
    b.entrance(5)
    H.undergrowth(b, [(0, z) for z in range(12)] + [(11, z) for z in range(12)] + [(x, 11) for x in range(12)],
                  rng, .35)
    b.natural_ground()
    return b


def tannery():
    """Leatherworker's log workshop with vats, a cauldron and hide racks in the yard."""
    rng = random.Random(4208)
    b = Build('taiga/tannery', (13, 12, 14))
    H.rubble(b, 1, 5, 7, 11, rng)
    H.log_walls(b, 1, 5, 7, 11, 2, 4, chink='stripped_spruce_log')
    ridge = H.roof(b, 1, 5, 7, 11, 4, 'dark_oak', axis='z', pitch=1, gable=log('spruce_log', 'x'), trim='spruce')
    H.door(b, 4, 2, 5, 'north')
    H.window(b, 7, 3, 8, 'east', width=2)
    H.window(b, 2, 3, 5, 'north')
    b.set(4, 7, 5, 'glass_pane')
    b.set(2, 2, 10, 'cauldron')
    b.set(3, 2, 10, 'water_cauldron', level=2)
    b.chest(6, 2, 10, 'north', loot=LOOT + 'tannery')
    b.barrel(6, 2, 9, 'west')
    b.set(2, 2, 6, 'crafting_table')
    for z in (7, 8):
        b.set(2, 3, z, 'brown_wall_banner', facing='east')
    H.wall_hide(b, 5, 3, 10, 'north', 'white')
    b.set(4, 4, 8, 'lantern', hanging=True, waterlogged=False)
    b.set(4, 5, 8, 'spruce_planks')
    # Yard: vats and hide racks.
    for x in (9, 10):
        b.set(x, 1, 7, 'water_cauldron', level=3)
    b.set(9, 1, 9, 'cauldron')
    b.set(11, 1, 9, 'barrel', facing='up', open=False)
    H.drying_rack(b, 8, 3, 1, length=3, hides=('brown', 'brown', 'white'))
    H.drying_rack(b, 8, 12, 1, length=3, hides=('white', 'brown', 'brown'))
    b.set(12, 1, 6, 'spruce_fence')
    b.set(12, 2, 6, 'lantern', waterlogged=False)
    H.path(b, 4, 0, 4, rng)
    b.entrance(4)
    H.undergrowth(b, [(x, z) for x in range(13) for z in (0, 1)] + [(0, z) for z in range(14)], rng, .3)
    b.natural_ground()
    return b


DESIGNS = {
    'taiga/smithy': smithy,
    'taiga/smokehouse': smokehouse,
    'taiga/fletcher': fletcher,
    'taiga/shepherd': shepherd,
    'taiga/fisher': fisher,
    'taiga/cartographer': cartographer,
    'taiga/mason': mason,
    'taiga/tannery': tannery,
}
