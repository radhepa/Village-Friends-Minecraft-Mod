"""Desert civic buildings that face the town square (one of each per village).

Same roles, residents, workstations and bedrooms as the plains civic buildings,
drawn as sandstone architecture: flat roofs with parapets, domes, arcades,
lattice windows, wind towers and striped awnings. Large slots are up to 17 wide
(entrance at x=8), small slots up to 11 wide (entrance at x=5).
"""
import random

from ...kit import Build
from ... import parts
from . import core_parts as dp
from .palette import LOOT

WEAPONS = 'minecraft:chests/village/village_weaponsmith'


def plaque(b, x, z, facing='north', y=1):
    b.custom(x, y, z, 'house_plaque', facing=facing)


def storey(b, x0, z0, x1, z1, y0, y1, fill='smooth_sandstone', corner='cut_sandstone', band=None):
    """One storey of solid walls; ``band`` is the course laid on top (the next floor's edge)."""
    dp.walls(b, x0, z0, x1, z1, y0, y1, fill=fill, corner=corner)
    if band:
        for x, z, _, _ in parts.ring(x0, z0, x1, z1):
            b.set(x, y1 + 1, z, band)


def deck(b, x0, z0, x1, z1, y, mat='acacia_planks'):
    b.fill(x0 + 1, y, z0 + 1, x1 - 1, y, z1 - 1, mat)


def sand_yard(b, x0, z0, x1, z1, rng, mix=('sand', 'sand', 'sandstone', 'smooth_sandstone')):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if b.get(x, 0, z)[0] == 'minecraft:air':
                b.set(x, 0, z, rng.choice(mix))


# --------------------------------------------------------------------- tavern
def tavern():
    """The Caravanserai: a walled forecourt with tables, a lofty hall with a hearth, a bar and the bard's
    dais, the kitchen behind, guest rooms upstairs and a wind tower on the roof.

    Tavern furniture faces the way its sitter faces. 32 seats: 12 in the forecourt (half under a striped
    awning, half under the sky), 4 at the hearth, 12 at two long tables and 4 bar stools.
    """
    rng = random.Random(1301)
    b = Build('desert/tavern', (17, 19, 29))
    _caravanserai_court(b, rng)
    _caravanserai_hall(b)
    _caravanserai_kitchen(b, rng)
    _caravanserai_bar(b)
    _caravanserai_upstairs(b)
    b.entrance(8)
    b.natural_ground()
    return b


def _caravanserai_court(b, rng):
    """Forecourt behind a gate arch: two long tables, palms in planters, lamps."""
    for x in range(1, 16):
        for z in range(1, 10):
            b.set(x, 0, z, 'smooth_sandstone' if (x + z) % 3 else 'cut_sandstone')
    for z in range(0, 10):
        b.set(8, 0, z, 'cut_sandstone' if z % 2 else 'chiseled_sandstone')
    # Low walls with a gate arch.
    for x in range(1, 16):
        if x in (7, 8, 9):
            continue
        b.set(x, 1, 1, 'cut_sandstone')
        b.set(x, 2, 1, 'sandstone_wall')
    for z in range(1, 10):
        for x in (1, 15):
            b.set(x, 1, z, 'cut_sandstone')
            b.set(x, 2, z, 'sandstone_wall')
    for x in (6, 10):
        for y in range(1, 5):
            b.set(x, y, 1, 'cut_sandstone' if y in (1, 4) else 'smooth_sandstone')
        b.set(x, 5, 1, 'smooth_sandstone_slab', type='bottom')
    dp.arch(b, 7, 1, 9, 1, 4)
    for x in (7, 8, 9):
        b.set(x, 5, 1, 'cut_sandstone')
    b.set(8, 6, 1, 'chiseled_sandstone')
    b.set(8, 3, 1, 'acacia_hanging_sign', rotation=8, attached=False, waterlogged=False)
    for x in (6, 10):
        b.set(x, 3, 0, 'orange_wall_banner', facing='north')
    # Two long tables of three: the west one under an awning, the east one open to the sky.
    for x0 in (3, 11):
        for x in range(x0, x0 + 3):
            b.custom(x, 1, 5, 'tavern_table')
            b.custom(x, 1, 4, 'tavern_chair', facing='south')
            b.custom(x, 1, 6, 'tavern_chair', facing='north')
    dp.canopy(b, 2, 3, 6, 7, 5, along='x', posts=((2, 3), (6, 3), (2, 7), (6, 7)))
    dp.wall_post(b, 14, 0, 3, height=2)
    dp.wall_post(b, 14, 0, 8, height=2)
    dp.wall_post(b, 10, 0, 8, height=2)
    dp.lantern(b, 4, 4, 5)
    # Palms in raised planters by the hall door.
    for px in (3, 13):
        for dx in (-1, 0, 1):
            b.set(px + dx, 0, 9, 'sand' if dx == 0 else 'cut_sandstone')
            if dx:
                b.set(px + dx, 1, 9, 'smooth_sandstone_slab', type='bottom')
        dp.palm(b, px, 1, 9, rng, height=7, lean='west' if px == 3 else 'east')
    dp.pot(b, 2, 1, 2, 'cactus')
    dp.pot(b, 14, 1, 2, 'dead_bush')


def _caravanserai_hall(b):
    """The hall: walls, the guest floor, the roof and wind tower, the hearth, tables and the bard's dais."""
    dp.plinth(b, 1, 10, 15, 22, top=1, floor='smooth_sandstone')
    storey(b, 1, 10, 15, 22, 2, 6, band='cut_sandstone')
    deck(b, 1, 10, 15, 22, 7)
    storey(b, 1, 10, 15, 22, 8, 10, band='cut_sandstone')
    deck(b, 1, 10, 15, 22, 11, 'smooth_sandstone')
    dp.parapet(b, 1, 10, 15, 22, 12, style='merlon')
    dp.cornice(b, 1, 10, 15, 22, 11)
    for x in range(2, 15):
        if x % 2:
            b.set(x, 6, 10, 'orange_terracotta')
    dp.door(b, 8, 2, 10, 'north', wood='acacia')
    dp.awning(b, [(x, 10) for x in range(6, 11)], 5, 'north', colors=('orange', 'white'))
    plaque(b, 9, 9)
    for x in (3, 13):
        dp.lattice(b, x, 3, 10, 'north', height=2, width=1)
        dp.lattice(b, x, 9, 10, 'north', height=1)
    for x in (5, 11):
        dp.lattice(b, x, 9, 10, 'north', height=1)
    for z in (12, 20):
        dp.lattice(b, 1, 3, z, 'west', height=2)
    for z in (13, 19):
        dp.lattice(b, 1, 9, z, 'west', height=1)
    dp.lattice(b, 15, 9, 15, 'east', height=1)
    for z in (12, 21):
        dp.lattice(b, 15, 3, z, 'east', height=2)
    for z in range(11, 22):
        if z % 2:
            b.set(1, 6, z, 'orange_terracotta')
            b.set(15, 6, z, 'orange_terracotta')
    # Wind tower over the east side of the roof.
    for y in range(12, 17):
        for x, z, _, corner in parts.ring(12, 18, 14, 20):
            b.set(x, y, z, 'cut_sandstone' if corner or y in (12, 16) else 'smooth_sandstone')
    for y in (14, 15):
        for (x, z, out) in ((13, 18, 'north'), (13, 20, 'south'), (12, 19, 'west'), (14, 19, 'east')):
            dp.lattice(b, x, y, z, out, height=1)
    b.fill(12, 17, 18, 14, 17, 20, 'smooth_sandstone_slab', type='bottom')
    b.set(13, 17, 19, 'cut_sandstone')
    # The hearth: a carved fireplace in the west wall, its flue climbing the outside.
    for z in (15, 17):
        for y in (2, 3):
            b.set(1, y, z, 'cut_sandstone')
    b.set(1, 2, 16, 'campfire', lit=True, signal_fire=False, facing='east', waterlogged=False)
    b.set(1, 3, 16, 'air')
    for z in (15, 16, 17):
        b.set(1, 4, z, 'chiseled_sandstone')
        b.set(2, 4, z, 'smooth_sandstone_slab', type='top', waterlogged=False)
        for y in range(1, 8):
            b.set(0, y, z, 'smooth_sandstone' if y < 7 else 'cut_sandstone')
    for y in range(8, 13):
        b.set(0, y, 16, 'smooth_sandstone')
    b.set(0, 13, 16, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    b.set(2, 5, 15, 'candle', candles=3, lit=True, waterlogged=False)
    b.set(2, 5, 17, 'decorated_pot', facing='east')
    for z in (15, 17):
        b.custom(3, 2, z, 'fireside_armchair', facing='west')
    b.barrel(3, 2, 16, 'up')
    b.set(3, 3, 16, 'candle', candles=1, lit=True, waterlogged=False)
    b.custom(2, 2, 14, 'village_bench', facing='south')
    b.custom(2, 2, 18, 'village_bench', facing='north')
    for z in (14, 15, 16, 17, 18):
        b.set(4, 1, z, 'red_wool' if z in (15, 16, 17) else 'orange_wool')
    # Two long tables of three with chairs down both sides.
    for z0 in (12, 17):
        for z in range(z0, z0 + 3):
            b.custom(6, 2, z, 'tavern_table')
            b.custom(5, 2, z, 'tavern_chair', facing='east')
            b.custom(7, 2, z, 'tavern_chair', facing='west')
    # The bard's dais by the door with its note block.
    for x in (2, 3):
        for z in (11, 12):
            b.set(x, 2, z, 'cut_sandstone' if (x, z) != (3, 12) else 'red_wool')
    for z in (11, 12):
        b.set(4, 2, z, 'smooth_sandstone_slab', type='bottom', waterlogged=False)
    b.set(2, 3, 11, 'note_block', instrument='bass', note=0, powered=False)
    b.set(3, 5, 11, 'orange_wall_banner', facing='south')
    # Lanterns on chains from the ceiling and a brass chandelier over the middle.
    for x, z in ((6, 11), (6, 16), (6, 21), (9, 13), (9, 19), (3, 13), (3, 19)):
        dp.lantern(b, x, 6, z)
    # Stairs up along the back wall.
    parts.stair_run(b, 4, 21, 2, 6, 'east', wood='acacia')
    for x in (2, 3):
        b.barrel(x, 2, 21, 'up')
    b.set(2, 3, 21, 'decorated_pot', facing='north')


def _caravanserai_bar(b):
    """The bar along the east wall: a log counter with four stools; the keeper's well half a step down."""
    for z in range(13, 20):
        b.set(11, 2, z, 'stripped_acacia_log', axis='z')
    b.set(11, 3, 13, 'lantern', hanging=False, waterlogged=False)
    b.set(11, 3, 19, 'decorated_pot', facing='west')
    for z in (13, 15, 17, 19):
        b.custom(10, 2, z, 'bar_stool', facing='east')
    for x in (12, 13, 14):
        for z in range(11, 22):
            b.set(x, 1, z, 'smooth_sandstone_slab', type='bottom', waterlogged=False)
    b.custom(14, 2, 15, 'tap_stand', facing='west')
    b.custom(14, 2, 16, 'drinks_barrel', facing='west')
    for z in (11, 12, 13, 18, 19, 20):
        b.barrel(14, 2, z, 'west')
    for z in (12, 19):
        b.barrel(14, 3, z, 'west')
    b.set(14, 3, 13, 'brewing_stand', has_bottle_0=False, has_bottle_1=False, has_bottle_2=False)
    b.set(14, 2, 17, 'water_cauldron', level=3)
    b.set(14, 2, 14, 'decorated_pot', facing='west')
    for z in (11, 13, 18, 20):
        b.set(14, 4, z, 'acacia_trapdoor', facing='west', half='top', open=False, powered=False, waterlogged=False)
        if z in (11, 20):
            b.set(14, 5, z, 'decorated_pot', facing='west')
        else:
            b.set(14, 5, z, 'candle', candles=2, lit=True, waterlogged=False)
    b.set(14, 4, 15, 'orange_wall_banner', facing='west')
    b.set(14, 4, 16, 'cyan_wall_banner', facing='west')
    b.resident(13, 2, 16, 'tavern_keeper')
    b.door(13, 2, 22, facing='north', wood='acacia')
    b.set(11, 2, 22, 'acacia_stairs', facing='north', half='top', waterlogged=False, lock=True)
    b.set(11, 3, 22, 'air')


def _caravanserai_kitchen(b, rng):
    """Kitchen wing behind the bar and a sandy back yard."""
    dp.plinth(b, 8, 22, 15, 28, top=1, floor='smooth_sandstone')
    storey(b, 8, 22, 15, 28, 2, 6, band='cut_sandstone')
    deck(b, 8, 22, 15, 28, 7, 'smooth_sandstone')
    dp.parapet(b, 8, 22, 15, 28, 8, style='wall', skip={(x, 22) for x in range(8, 16)})
    b.custom(11, 2, 27, 'kitchen_stove', facing='north')
    b.set(12, 2, 27, 'smoker', facing='north', lit=True)
    b.set(10, 2, 27, 'water_cauldron', level=3)
    for x in (11, 12):
        b.set(x, 4, 27, 'cut_sandstone')
        b.set(x, 5, 27, 'cut_sandstone')
    for y in range(8, 11):
        b.set(12, y, 27, 'cut_sandstone')
    b.set(12, 11, 27, 'campfire', lit=True, signal_fire=False, facing='north', waterlogged=False)
    b.set(9, 2, 23, 'crafting_table')
    b.barrel(9, 2, 26, 'up')
    b.barrel(9, 2, 27, 'up')
    b.set(9, 3, 27, 'hay_block', axis='y')
    b.barrel(14, 2, 24, 'west')
    b.set(14, 2, 25, 'smooth_sandstone_slab', type='double')
    b.set(14, 2, 26, 'smooth_sandstone_slab', type='double')
    b.set(14, 3, 25, 'melon')
    b.set(14, 2, 27, 'composter', level=4)
    b.set(13, 2, 27, 'decorated_pot', facing='north')
    dp.lantern(b, 12, 6, 24)
    b.resident(11, 2, 25, 'cook')
    dp.door(b, 8, 2, 25, 'west', wood='acacia', head=None)
    dp.lattice(b, 15, 3, 25, 'east', height=1)
    dp.lattice(b, 10, 3, 28, 'south', height=1)
    # Back yard.
    sand_yard(b, 1, 23, 7, 28, rng)
    for x, z in ((1, 27), (2, 27), (1, 26)):
        b.barrel(x, 1, z, 'up')
    b.set(2, 1, 26, 'hay_block', axis='y')
    b.set(5, 1, 28, 'water_cauldron', level=3)
    parts.woodpile(b, 2, 1, 23, 'x', length=4, wood='acacia', height=2)
    dp.palm(b, 5, 1, 26, rng, height=6, lean='south')


def _caravanserai_upstairs(b):
    """Two guest rooms on the west, a corridor over the stairs and a store on the east."""
    for z in range(11, 22):
        for y in (8, 9, 10):
            b.set(6, y, z, 'smooth_sandstone')
    for x in range(2, 6):
        for y in (8, 9, 10):
            b.set(x, y, 16, 'smooth_sandstone')
    b.door(6, 8, 13, facing='east', wood='acacia')
    b.door(6, 8, 19, facing='east', wood='acacia', hinge='right')
    for x in (7, 8):
        b.set(x, 8, 20, 'acacia_fence')
    # North room.
    b.bed(3, 8, 12, 'west', 'orange')
    b.bed(3, 8, 14, 'west', 'orange')
    b.chest(2, 8, 13, 'east', loot=LOOT)
    b.set(5, 8, 15, 'decorated_pot', facing='north')
    parts.rug(b, 4, 12, 4, 14, 8, 'red', border='orange')
    dp.lantern(b, 4, 10, 13)
    b.room('guest_room_north', (4, 9, 13))
    # South room.
    b.bed(3, 8, 18, 'west', 'cyan')
    b.bed(3, 8, 20, 'west', 'cyan')
    b.chest(2, 8, 19, 'east', loot=LOOT)
    b.set(5, 8, 17, 'decorated_pot', facing='north')
    parts.rug(b, 4, 18, 4, 20, 8, 'cyan', border='white')
    dp.lantern(b, 4, 10, 19)
    b.room('guest_room_south', (4, 9, 19))
    # Store and landing.
    for z in (11, 12):
        b.barrel(14, 8, z, 'west')
    b.set(14, 9, 11, 'white_wool')
    b.chest(13, 8, 11, 'south')
    parts.rug(b, 10, 13, 13, 17, 8, 'orange', border='red')
    dp.lantern(b, 10, 10, 12)
    dp.lantern(b, 10, 10, 18)


# ------------------------------------------------------------------- garrison
def garrison():
    """Kasbah: a crenellated gatehouse, a tapering watch tower, a drill yard and a two-storey barracks."""
    rng = random.Random(1302)
    b = Build('desert/garrison', (17, 20, 21))
    # Yard floor.
    for x in range(0, 17):
        for z in range(1, 13):
            b.set(x, 0, z, rng.choice(['sand', 'sand', 'sandstone', 'smooth_sandstone', 'gravel']))
    # Curtain walls with crenellations.
    for x in range(0, 17):
        b.set(x, 0, 1, 'sandstone')
        for y in range(1, 5):
            b.set(x, y, 1, 'smooth_sandstone' if y < 4 else 'cut_sandstone')
        merlon = x % 2 == 0
        b.set(x, 5, 1, 'cut_sandstone' if merlon else 'smooth_sandstone_slab', **({} if merlon else {'type': 'bottom'}))
    for z in range(1, 13):
        for x in (0, 16):
            b.set(x, 0, z, 'sandstone')
            for y in range(1, 5):
                b.set(x, y, z, 'smooth_sandstone' if y < 4 else 'cut_sandstone')
            merlon = z % 2 == 0
            b.set(x, 5, z, 'cut_sandstone' if merlon else 'smooth_sandstone_slab', **({} if merlon else {'type': 'bottom'}))
    # Gatehouse: two square towers flanking a pointed gate arch.
    for x0 in (5, 10):
        for x in range(x0, x0 + 2):
            for z in range(0, 3):
                for y in range(0, 7):
                    b.set(x, y, z, 'cut_sandstone' if y in (0, 3, 6) else 'smooth_sandstone')
                merlon = (x + z) % 2 == 0
                b.set(x, 7, z, 'cut_sandstone' if merlon else 'smooth_sandstone_slab',
                      **({} if merlon else {'type': 'bottom'}))
        horn = x0 if x0 == 5 else x0 + 1
        b.set(horn, 8, 0, 'chiseled_sandstone')
        b.set(horn, 9, 0, 'sandstone_wall')
        b.set(x0 if x0 == 10 else x0 + 1, 4, 0, 'chiseled_sandstone')
    for x in range(7, 10):
        for z in range(0, 3):
            b.set(x, 0, z, 'smooth_sandstone')
            b.clear(x, 1, z, x, 3, z)
            b.set(x, 4, z, 'smooth_sandstone')
            b.set(x, 5, z, 'cut_sandstone')
            b.set(x, 6, z, 'cut_sandstone_slab', type='bottom')
    for z in (0, 2):
        dp.arch(b, 7, z, 9, z, 3)
    b.set(8, 5, 0, 'chiseled_sandstone')
    for x in (4, 12):
        dp.wall_post(b, x, 0, 0, height=1)
    # Watch tower in the north-east corner: stepped kasbah tower with corner horns.
    tx0, tz0, tx1, tz1 = 12, 2, 16, 6
    for y in range(0, 14):
        for x in range(tx0, tx1 + 1):
            for z in range(tz0, tz1 + 1):
                edge = x in (tx0, tx1) or z in (tz0, tz1)
                corner = x in (tx0, tx1) and z in (tz0, tz1)
                if y == 0:
                    b.set(x, y, z, 'sandstone')
                elif edge:
                    b.set(x, y, z, 'cut_sandstone' if corner or y in (5, 9, 13) else 'smooth_sandstone')
                elif y in (5, 9):
                    b.set(x, y, z, 'acacia_planks')
                else:
                    b.set(x, y, z, 'air')
    for y in range(1, 14):
        b.set(13, y, 3, 'ladder', facing='south')
    for x in range(tx0 + 1, tx1):
        for z in range(tz0 + 1, tz1):
            b.set(x, 13, z, 'acacia_planks')
    b.set(13, 13, 3, 'acacia_trapdoor', facing='south', half='top', open=False, powered=False, waterlogged=False)
    dp.cornice(b, tx0, tz0, tx1, tz1, 13)
    for x, z, f, corner in parts.ring(tx0 - 1, tz0 - 1, tx1 + 1, tz1 + 1):
        if b.inside(x, 14, z):
            b.set(x, 14, z, 'cut_sandstone' if (x + z) % 2 == 0 or corner else 'smooth_sandstone_slab',
                  **({} if (x + z) % 2 == 0 or corner else {'type': 'bottom'}))
    for x, z in ((tx0, tz0), (tx1, tz0), (tx0, tz1), (tx1, tz1)):
        for y in (14, 15):
            b.set(x, y, z, 'cut_sandstone')
        b.set(x, 16, z, 'sandstone_wall')
        b.set(x, 17, z, 'lantern', hanging=False, waterlogged=False)
    for (x, z, out) in ((14, tz0, 'north'), (tx0, 4, 'west'), (14, tz1, 'south')):
        for y in (7, 11):
            dp.lattice(b, x, y, z, out, height=1)
    # Kasbah band of terracotta lozenges under the parapet; banners over the square.
    for x, z, _, corner in parts.ring(tx0, tz0, tx1, tz1):
        if not corner and (x + z) % 2 == 0:
            b.set(x, 12, z, 'orange_terracotta')
    for x in (13, 15):
        b.set(x, 10, tz0 - 1, 'red_wall_banner', facing='north')
    b.door(14, 1, tz1, facing='south', wood='acacia')
    b.set(14, 3, tz1, 'chiseled_sandstone')
    # Barracks along the back: guard office and armoury below, bunk room above.
    dp.plinth(b, 0, 13, 16, 20, top=1, floor='smooth_sandstone')
    storey(b, 0, 13, 16, 20, 2, 5, band='cut_sandstone')
    deck(b, 0, 13, 16, 20, 6)
    storey(b, 0, 13, 16, 20, 7, 9, band='cut_sandstone')
    deck(b, 0, 13, 16, 20, 10, 'smooth_sandstone')
    dp.parapet(b, 0, 13, 16, 20, 11, style='merlon')
    dp.door(b, 8, 2, 13, 'north', wood='acacia', lamps=True)
    for x in (3, 13):
        dp.lattice(b, x, 3, 13, 'north', height=2)
        dp.lattice(b, x, 8, 13, 'north', height=1)
    for x in (5, 11):
        dp.lattice(b, x, 8, 13, 'north', height=1)
        dp.lattice(b, x, 8, 20, 'south', height=1)
    dp.awning(b, [(x, 13) for x in range(1, 16) if x not in (7, 8, 9)], 5, 'north',
              colors=('red', 'white'))
    for x in range(1, 16):
        if x % 2:
            b.set(x, 9, 13, 'orange_terracotta')
    for x in (3, 13):
        dp.lattice(b, x, 3, 20, 'south', height=2)
    for z in (16, 18):
        dp.lattice(b, 0, 3, z, 'west', height=2)
        dp.lattice(b, 16, 3, z, 'east', height=1)
        dp.lattice(b, 0, 8, z, 'west', height=1)
    plaque(b, 6, 12)
    b.custom(3, 2, 15, 'command_desk', facing='east')
    parts.chair(b, 2, 2, 15, 'west', wood='acacia')
    b.chest(1, 2, 19, 'east', loot=WEAPONS)
    b.set(2, 2, 19, 'anvil', facing='east')
    b.set(4, 2, 19, 'grindstone', face='floor', facing='north')
    b.barrel(12, 2, 19, 'up')
    b.barrel(13, 2, 19, 'up')
    b.custom(11, 2, 15, 'training_dummy', facing='west')
    parts.rug(b, 4, 16, 6, 17, 2, 'red', border='red')
    for x in (4, 11):
        dp.lantern(b, x, 5, 17)
    parts.stair_run(b, 15, 19, 2, 5, 'north', wood='acacia')
    for z in range(14, 20):
        for y in (7, 8, 9):
            b.set(14, y, z, 'smooth_sandstone')
    b.door(14, 7, 15, facing='west', wood='acacia')
    for x in (1, 4, 7, 10):
        b.bed(x, 7, 19, 'north', 'red')
    b.chest(12, 7, 19, 'north', loot=LOOT)
    b.set(1, 7, 14, 'crafting_table')
    dp.lantern(b, 6, 9, 16)
    dp.lantern(b, 11, 9, 16)
    b.room('bunk_room', (7, 8, 16))
    # Drill yard.
    for x, z in ((3, 4), (3, 8), (6, 6)):
        b.custom(x, 1, z, 'training_dummy', facing='south')
    b.custom(1, 1, 9, 'archery_target', facing='east')
    b.custom(1, 1, 10, 'archery_target', facing='east')
    for x, z in ((15, 10), (15, 11), (14, 11)):
        b.set(x, 1, z, 'hay_block', axis='y')
    b.set(10, 1, 11, 'grindstone', face='floor', facing='north')
    b.barrel(11, 1, 11, 'up')
    b.set(12, 1, 11, 'smithing_table')
    b.set(13, 1, 9, 'water_cauldron', level=3)
    b.resident(5, 1, 7, 'knight')
    b.resident(4, 1, 10, 'archer')
    b.entrance(8)
    b.natural_ground()
    return b


# ------------------------------------------------------------------- workshop
def workshop():
    """Craft yard: the tailor's plastered house with a dye yard, beside the carpenter's shaded timber shed."""
    rng = random.Random(1303)
    b = Build('desert/workshop', (17, 14, 18))
    plaster, corner = 'white_terracotta', 'stripped_jungle_log'
    # Tailor's house x1..9 z5..14.
    dp.plinth(b, 1, 5, 9, 14, top=1, floor='smooth_sandstone')
    dp.walls(b, 1, 5, 9, 14, 2, 5, fill=plaster, corner=corner)
    for x, z, _, _ in parts.ring(1, 5, 9, 14):
        b.set(x, 6, z, 'cut_sandstone')
    deck(b, 1, 5, 9, 14, 6)
    dp.walls(b, 1, 5, 9, 14, 7, 9, fill=plaster, corner=corner)
    for x, z, _, _ in parts.ring(1, 5, 9, 14):
        b.set(x, 10, z, 'cut_sandstone')
    deck(b, 1, 5, 9, 14, 10, 'smooth_sandstone')
    dp.parapet(b, 1, 5, 9, 14, 11, style='wall')
    for y in range(2, 10):
        for x, z in ((1, 5), (9, 5), (1, 14), (9, 14)):
            b.set(x, y, z, corner, axis='y')
    dp.door(b, 5, 2, 5, 'north', wood='jungle')
    dp.awning(b, [(x, 5) for x in range(2, 9)], 5, 'north', colors=('cyan', 'white'))
    for x in (3, 7):
        dp.lattice(b, x, 3, 5, 'north', height=2, sill='sandstone_stairs')
        dp.lattice(b, x, 8, 5, 'north', height=1, wood='jungle')
    for z in (8, 11):
        dp.lattice(b, 1, 3, z, 'west', height=2)
        dp.lattice(b, 1, 8, z, 'west', height=1)
    dp.lattice(b, 9, 8, 12, 'east', height=1)
    # Tailor's shop.
    b.custom(4, 2, 13, 'sewing_table', facing='north')
    b.set(2, 2, 10, 'loom', facing='east')
    for z, c in zip(range(6, 10), ['red', 'yellow', 'cyan', 'orange']):
        b.set(2, 2, z, f'{c}_wool')
        b.set(2, 3, z, f'{c}_carpet')
    parts.rug(b, 4, 8, 6, 10, 2, 'cyan', border='orange')
    b.chest(2, 2, 13, 'east', loot=LOOT)
    b.set(6, 2, 13, 'decorated_pot', facing='north')
    dp.lantern(b, 5, 5, 9)
    b.resident(4, 2, 11, 'tailor')
    parts.stair_run(b, 8, 13, 2, 5, 'north', wood='jungle')
    # Bedroom upstairs behind a partition; the landing runs along the stairs.
    for z in range(6, 14):
        for y in (7, 8, 9):
            b.set(6, y, z, plaster)
    b.door(6, 7, 7, facing='west', wood='jungle')
    b.bed(2, 7, 13, 'north', 'cyan')
    b.bed(5, 7, 13, 'north', 'orange')
    b.chest(3, 7, 13, 'north', loot=LOOT)
    b.set(4, 7, 13, 'decorated_pot', facing='north')
    parts.rug(b, 2, 8, 5, 10, 7, 'orange', border='red')
    dp.lantern(b, 3, 9, 9)
    b.room('bedroom', (4, 8, 7))
    dp.lantern(b, 8, 9, 7)
    # Roof: cloth drying line under a little canopy.
    dp.canopy(b, 2, 11, 5, 13, 13, along='x', colors=('orange', 'white', 'cyan', 'white'))
    for x, c in ((6, 'red'), (7, 'yellow')):
        b.set(x, 11, 12, f'{c}_wool')
    dp.pot(b, 8, 11, 7, 'cactus')
    # Carpenter's shed x10..16 z4..15: log posts, a slatted acacia roof, striped valance.
    for x in range(11, 16):
        for z in range(5, 15):
            b.set(x, 0, z, 'acacia_planks' if (x + z) % 3 else 'stripped_acacia_log', axis='x')
    for x, z in ((10, 4), (16, 4), (10, 15), (16, 15), (16, 9), (10, 9)):
        b.set(x, 0, z, 'cut_sandstone')
        for y in range(1, 5):
            b.set(x, y, z, 'stripped_acacia_log', axis='y')
    for x in range(10, 17):
        for z in range(4, 16):
            if x in (10, 16) or z in (4, 15):
                b.set(x, 5, z, 'stripped_acacia_log', axis='x' if z in (4, 15) else 'z')
            elif z % 2 == 0:
                b.set(x, 5, z, 'acacia_slab', type='top')
            elif x % 3 == 1:
                b.set(x, 5, z, 'stripped_acacia_log', axis='z')
    for z in range(6, 15, 3):
        for x in range(11, 16):
            if b.get(x, 5, z)[0] == 'minecraft:air':
                b.set(x, 5, z, 'acacia_slab', type='top')
    for x in range(10, 17):
        b.set(x, 4, 3, 'orange_wool' if x % 2 else 'white_wool')
    for z in range(10, 15):
        for y in (1, 2):
            b.set(16, y, z, 'smooth_sandstone')
    b.custom(13, 1, 8, 'sawmill', facing='west')
    b.set(13, 1, 12, 'crafting_table')
    parts.woodpile(b, 15, 1, 5, 'z', length=3, wood='acacia', height=3)
    parts.woodpile(b, 12, 1, 14, 'x', length=3, wood='jungle', height=2)
    b.set(11, 1, 6, 'acacia_planks')
    b.set(11, 2, 6, 'acacia_slab', type='bottom')
    b.barrel(15, 1, 13, 'up')
    dp.lantern(b, 13, 4, 10)
    b.resident(12, 1, 10, 'carpenter')
    # Dye yard in front: vats and a drying frame hung with banners.
    for x, z, c in ((2, 3, 'red'), (3, 3, 'cyan')):
        b.set(x, 1, z, 'water_cauldron', level=3)
    for x in (1, 4):
        b.set(x, 0, 1, 'cut_sandstone')
        for y in (1, 2, 3):
            b.set(x, y, 1, 'acacia_fence')
    for x in range(1, 5):
        b.set(x, 4, 1, 'stripped_acacia_log', axis='x')
    for x, c in ((2, 'orange'), (3, 'cyan')):
        b.set(x, 4, 0, f'{c}_wall_banner', facing='north')
    sand_yard(b, 1, 0, 9, 4, rng, mix=('sand', 'sandstone', 'sand'))
    for z in range(0, 4):
        b.set(8, 0, z, 'smooth_sandstone')
    for x in range(5, 9):
        b.set(x, 0, 3, 'smooth_sandstone')
    b.set(5, 0, 4, 'smooth_sandstone')
    plaque(b, 6, 4)
    b.set(7, 1, 1, 'decorated_pot', facing='north')
    dp.cactus(b, 1, 1, 3, 2)
    b.entrance(8)
    b.natural_ground()
    return b


# --------------------------------------------------------------------- chapel
def grave(b, x, z, rng):
    b.set(x, 0, z + 1, 'sand')
    kind = rng.random()
    if kind < .5:
        b.set(x, 1, z, 'sandstone_wall')
    elif kind < .8:
        b.set(x, 1, z, 'sandstone_stairs', facing='south', half='bottom', shape='straight', lock=True)
    else:
        b.set(x, 1, z, 'chiseled_sandstone')
        b.set(x, 2, z, 'sandstone_slab', type='bottom')
    if rng.random() < .5:
        b.set(x, 1, z + 1, 'dead_bush')


def chapel():
    """Domed temple: a square sanctuary under a great dome, an arched porch and a minaret with the bell."""
    rng = random.Random(1304)
    b = Build('desert/chapel', (17, 22, 21))
    x0, z0, x1, z1 = 3, 7, 13, 17
    dp.plinth(b, x0, z0, x1, z1, top=1, floor='smooth_sandstone')
    dp.walls(b, x0, z0, x1, z1, 2, 8, fill='smooth_sandstone', corner='cut_sandstone')
    for x, z, _, _ in parts.ring(x0, z0, x1, z1):
        b.set(x, 9, z, 'cut_sandstone')
    # Roof deck with merlons; the dome rises from it and stays open to the hall below.
    b.fill(x0 + 1, 9, z0 + 1, x1 - 1, 9, z1 - 1, 'smooth_sandstone')
    dp.cornice(b, x0, z0, x1, z1, 9)
    dp.parapet(b, x0, z0, x1, z1, 10, style='merlon')
    cx, cz = 8, 12
    # An open oculus in the deck, a drum with tiled band and lattice lights, then the dome.
    for x in range(cx - 4, cx + 5):
        for z in range(cz - 4, cz + 5):
            d = ((x - cx) ** 2 + (z - cz) ** 2) ** .5
            if d <= 2.6:
                b.set(x, 9, z, 'air')
            elif d <= 3.6:
                b.set(x, 9, z, 'cut_sandstone')
                b.set(x, 10, z, 'smooth_sandstone')
                b.set(x, 11, z, 'cyan_glazed_terracotta' if (x + z) % 2 else 'white_glazed_terracotta',
                      facing='north')
    for x, z, out in ((cx, cz - 3, 'north'), (cx, cz + 3, 'south'), (cx - 3, cz, 'west'), (cx + 3, cz, 'east')):
        dp.lattice(b, x, 10, z, out, height=1)
    top = dp.dome(b, cx, cz, 12, 3, mat='smooth_sandstone', band='cut_sandstone')
    b.set(cx, top + 1, cz, 'gold_block')
    b.set(cx, top + 2, cz, 'lightning_rod', facing='up', powered=False)
    for y in range(9, top):
        b.set(cx, y, cz, dp.CHAIN, axis='y', waterlogged=False)
    dp.lantern(b, cx, 8, cz, hanging=True)
    # Tall stained lattice windows and a rose window over the altar.
    for z in (9, 12, 15):
        for x, out in ((x0, 'west'), (x1, 'east')):
            for y in (3, 4, 5):
                b.set(x, y, z, 'yellow_stained_glass_pane' if y < 5 else 'orange_stained_glass_pane')
    for x in (7, 8, 9):
        for y in (4, 5, 6):
            if not (y in (4, 6) and x != 8):
                b.set(x, y, z1, 'red_stained_glass_pane' if (x, y) == (8, 5) else 'orange_stained_glass_pane')
    # Porch: one pointed arch on two piers, a balcony roof.
    for x in range(6, 11):
        for z in range(3, 7):
            b.set(x, 0, z, 'cut_sandstone' if (x + z) % 2 else 'smooth_sandstone')
    dp.arcade(b, 6, 3, 10, 3, 1, 4, spacing=4)
    for x in (6, 10):
        for y in range(1, 5):
            b.set(x, y, 6, 'cut_sandstone')
    b.fill(6, 5, 3, 10, 5, 6, 'smooth_sandstone')
    dp.parapet(b, 6, 3, 10, 6, 6, style='merlon', skip={(x, 6) for x in range(7, 10)})
    dp.door(b, 8, 2, z0, 'north', wood='jungle', head='chiseled_sandstone')
    for x in (7, 9):
        b.set(x, 2, z0, 'cut_sandstone')
    dp.lantern(b, 8, 4, 5)
    # Interior: pews, aisle carpet, altar with the cleric's brewing stand, candles.
    for z in (10, 12, 14):
        for x in (5, 6, 7, 9, 10, 11):
            b.set(x, 2, z, 'acacia_stairs', facing='north', half='bottom', lock=True, shape='straight')
    for z in range(9, 16):
        b.set(8, 2, z, 'red_carpet')
    for x in range(5, 12):
        b.set(x, 1, 16, 'cut_sandstone')
    for x in (7, 8, 9):
        b.set(x, 2, 16, 'chiseled_sandstone' if x == 8 else 'smooth_sandstone_slab', type=None if x == 8 else 'top')
    b.set(8, 3, 16, 'candle', candles=3, lit=True, waterlogged=False)
    b.set(7, 3, 16, 'candle', candles=2, lit=True, waterlogged=False)
    b.set(9, 3, 16, 'candle', candles=2, lit=True, waterlogged=False)
    b.set(6, 2, 16, 'brewing_stand')
    b.set(10, 2, 16, 'decorated_pot', facing='north')
    for x, z in ((4, 8), (12, 8), (4, 16), (12, 16)):
        dp.lantern(b, x, 2, z, hanging=False)
    # Minaret at the front-east corner with an open belfry.
    mx0, mz0, mx1, mz1 = 13, 2, 15, 4
    for y in range(0, 15):
        for x in range(mx0, mx1 + 1):
            for z in range(mz0, mz1 + 1):
                edge = x in (mx0, mx1) or z in (mz0, mz1)
                corner = x in (mx0, mx1) and z in (mz0, mz1)
                if y == 0:
                    b.set(x, y, z, 'sandstone')
                elif edge:
                    b.set(x, y, z, 'cut_sandstone' if corner or y in (5, 10, 14) else 'smooth_sandstone')
    for y in (11, 12, 13):
        for x, z in ((14, mz0), (14, mz1), (mx0, 3), (mx1, 3)):
            b.set(x, y, z, 'air')
    for x, z, f in ((14, mz0, 'north'), (14, mz1, 'south'), (mx0, 3, 'west'), (mx1, 3, 'east')):
        dp.arch(b, x, z, x, z, 13)
    b.set(14, 13, 3, 'bell', attachment='ceiling', facing='north', powered=False)
    for x in range(mx0 - 1, mx1 + 2):
        for z in range(mz0 - 1, mz1 + 2):
            if x in (mx0 - 1, mx1 + 1) or z in (mz0 - 1, mz1 + 1):
                if b.inside(x, 10, z):
                    f = 'south' if z == mz0 - 1 else 'north' if z == mz1 + 1 else 'east' if x == mx0 - 1 else 'west'
                    b.set(x, 9, z, 'sandstone_stairs', facing=f, half='top', shape='straight', lock=True)
                    b.set(x, 10, z, 'smooth_sandstone_slab', type='bottom')
    b.fill(mx0, 14, mz0, mx1, 14, mz1, 'cut_sandstone')
    mt = dp.dome(b, 14, 3, 15, 1, mat='smooth_sandstone')
    b.set(14, mt + 1, 3, 'gold_block')
    b.set(14, mt + 2, 3, 'lightning_rod', facing='up', powered=False)
    for z in (mz0, mz1):
        dp.lattice(b, 14, 6, z, 'north' if z == mz0 else 'south', height=2)
    # Walled garden with palms and graves.
    for x in range(0, 17):
        b.set(x, 1, 20, 'cut_sandstone' if x % 4 == 0 else 'sandstone_wall')
    for z in range(7, 20):
        for x in (0, 16):
            b.set(x, 1, z, 'cut_sandstone' if z % 4 == 0 else 'sandstone_wall')
    sand_yard(b, 1, 7, 15, 19, rng, mix=('sand',))
    for z in (9, 12, 15):
        grave(b, 1, z, rng)
    for z in (10, 13):
        grave(b, 15, z, rng)
    dp.palm(b, 2, 1, 18, rng, height=6, lean='west')
    dp.palm(b, 14, 1, 18, rng, height=7, lean='east')
    b.custom(8, 1, 19, 'village_bench', facing='north')
    # Front path and lamps.
    for z in range(0, 3):
        b.set(8, 0, z, 'smooth_sandstone' if z % 2 else 'cut_sandstone')
    for x in (4, 12):
        dp.wall_post(b, x, 0, 3, height=2)
    for x, z in ((2, 4), (3, 5), (11, 5)):
        b.set(x, 0, z, 'sand')
        dp.cactus(b, x, 1, z, 1 + (x % 2))
    b.entrance(8)
    b.natural_ground()
    return b


# ----------------------------------------------------------------- apothecary
def apothecary():
    """Herbalist's house: ochre walls, an infirmary below, a still room and bedroom above, a teal dome."""
    rng = random.Random(1305)
    b = Build('desert/apothecary', (11, 16, 17))
    x0, z0, x1, z1 = 1, 5, 9, 13
    dp.plinth(b, x0, z0, x1, z1, top=1, floor='smooth_sandstone')
    dp.walls(b, x0, z0, x1, z1, 2, 5, fill='yellow_terracotta', corner='cut_sandstone')
    for x, z, _, _ in parts.ring(x0, z0, x1, z1):
        b.set(x, 6, z, 'cut_sandstone')
    deck(b, x0, z0, x1, z1, 6)
    dp.walls(b, x0, z0, x1, z1, 7, 9, fill='yellow_terracotta', corner='cut_sandstone')
    for x, z, _, _ in parts.ring(x0, z0, x1, z1):
        b.set(x, 10, z, 'cut_sandstone')
    deck(b, x0, z0, x1, z1, 10, 'smooth_sandstone')
    dp.parapet(b, x0, z0, x1, z1, 11, style='merlon')
    top = dp.dome(b, 5, 9, 11, 2, mat='oxidized_cut_copper',
                  band='cut_sandstone')
    b.set(5, top + 1, 9, 'gold_block')
    dp.door(b, 5, 2, z0, 'north', wood='acacia')
    dp.awning(b, [(x, z0) for x in range(3, 8)], 5, 'north', colors=('cyan', 'white'))
    for x in (3, 7):
        dp.lattice(b, x, 3, z0, 'north', height=1, sill='sandstone_stairs')
        dp.lattice(b, x, 7, z0, 'north', height=2)
    for z in (7, 11):
        dp.lattice(b, x0, 3, z, 'west', height=1)
        dp.lattice(b, x1, 3, z, 'east', height=1)
    dp.lattice(b, x0, 8, 11, 'west', height=1)
    dp.lattice(b, x1, 8, 11, 'east', height=1)
    # Infirmary and workroom.
    b.custom(2, 2, 7, 'alchemical_press', facing='east')
    b.set(2, 2, 8, 'brewing_stand')
    b.set(2, 2, 9, 'water_cauldron', level=2)
    for z in (10, 12):
        b.custom(6, 2, z, 'apothecary_cot', facing='west')
    b.set(6, 2, 11, 'potted_fern')
    b.barrel(2, 2, 12, 'up')
    b.set(3, 2, 12, 'decorated_pot', facing='north')
    dp.lantern(b, 4, 5, 9)
    parts.stair_run(b, 8, 12, 2, 5, 'north', wood='acacia')
    b.resident(4, 2, 9, 'apothecary')
    # Upstairs: the still room in front, the bedroom behind a partition.
    for x in range(2, 9):
        for y in (7, 8, 9):
            b.set(x, y, 9, 'yellow_terracotta')
    for z in range(10, 13):
        for y in (7, 8, 9):
            b.set(8, y, z, 'yellow_terracotta')
    b.door(5, 7, 9, facing='south', wood='acacia')
    b.bed(2, 7, 12, 'north', 'cyan')
    b.chest(3, 7, 12, 'north', loot=LOOT)
    b.set(7, 7, 12, 'potted_azure_bluet')
    dp.lantern(b, 5, 9, 11)
    b.room('apothecary_bedroom', (5, 8, 11))
    b.set(2, 7, 6, 'brewing_stand')
    b.set(3, 7, 6, 'bookshelf')
    dp.lantern(b, 4, 9, 7)
    # Herb garden in front, watered by two little cisterns with reeds.
    for x in range(1, 10):
        for z in range(1, 4):
            if x in (4, 5, 6):
                continue
            edge = x in (1, 9) or z in (1, 3) or x in (3, 7)
            b.set(x, 0, z, 'rooted_dirt' if not edge else 'coarse_dirt')
            plant = rng.choice(['azure_bluet', 'allium', 'fern', 'sweet_berry_bush', 'short_dry_grass', 'dead_bush'])
            if plant == 'sweet_berry_bush':
                b.set(x, 1, z, plant, age=2)
            else:
                b.set(x, 1, z, plant)
    for x in (2, 8):
        b.set(x, 0, 2, 'water', level=0)
        b.set(x, 1, 2, 'air')
        b.set(x, 1, 1, 'sugar_cane', age=0)
        b.set(x, 2, 1, 'sugar_cane', age=0)
    for z in range(0, 5):
        b.set(5, 0, z, 'smooth_sandstone' if z % 2 else 'cut_sandstone')
    for x in (4, 6):
        b.set(x, 0, 4, 'cut_sandstone')
    plaque(b, 4, 4)
    b.set(6, 1, 4, 'lantern', hanging=False, waterlogged=False)
    b.entrance(5)
    b.natural_ground()
    return b


# -------------------------------------------------------------------- library
def library():
    """House of Wisdom: a tall portal (iwan) framed in blue tiles, a lofty book hall and a small dome."""
    rng = random.Random(1306)
    b = Build('desert/library', (11, 19, 17))
    x0, z0, x1, z1 = 1, 4, 9, 14
    dp.plinth(b, x0, z0, x1, z1, top=1, floor='smooth_sandstone')
    dp.walls(b, x0, z0, x1, z1, 2, 6, fill='smooth_sandstone', corner='cut_sandstone')
    for x, z, _, _ in parts.ring(x0, z0, x1, z1):
        b.set(x, 7, z, 'cut_sandstone')
    deck(b, x0, z0, x1, z1, 7, 'jungle_planks')
    dp.walls(b, x0, z0, x1, z1, 8, 10, fill='smooth_sandstone', corner='cut_sandstone')
    for x, z, _, _ in parts.ring(x0, z0, x1, z1):
        b.set(x, 11, z, 'cut_sandstone')
    deck(b, x0, z0, x1, z1, 11, 'smooth_sandstone')
    dp.parapet(b, x0, z0, x1, z1, 12, style='merlon')
    top = dp.dome(b, 5, 9, 12, 2, mat='smooth_sandstone',
                  band='light_blue_glazed_terracotta')
    b.set(5, top + 1, 9, 'gold_block')
    # Blue tile frieze under the parapet on the front.
    for x in range(x0 + 1, x1):
        b.set(x, 10, z0, 'light_blue_glazed_terracotta', facing='north')
    # Iwan: a tall framed portal stepping out of the facade.
    for y in range(1, 10):
        for x in (3, 7):
            b.set(x, y, 3, 'cut_sandstone' if y in (1, 9) else 'smooth_sandstone')
    for x in range(3, 8):
        b.set(x, 9, 3, 'cut_sandstone')
        b.set(x, 10, 3, 'cut_sandstone_slab', type='bottom') if x in (3, 7) else b.set(x, 10, 3, 'cut_sandstone')
    for x in (4, 5, 6):
        for y in (6, 7, 8):
            b.set(x, y, 3, 'cyan_glazed_terracotta' if y == 8 else 'smooth_sandstone', facing='north') if y == 8 \
                else b.set(x, y, 3, 'smooth_sandstone')
    dp.arch(b, 4, 3, 6, 3, 5)
    for x in (4, 5, 6):
        b.set(x, 0, 3, 'cut_sandstone')
    for x in (4, 6):
        b.set(x, 4, z0, 'light_blue_glazed_terracotta', facing='north')
    dp.door(b, 5, 2, z0, 'north', wood='jungle', head='cyan_glazed_terracotta')
    # Tall lattice windows.
    for x in (2, 8):
        dp.lattice(b, x, 3, z0, 'north', height=3, wood='jungle')
    for z in (7, 11):
        dp.lattice(b, x0, 3, z, 'west', height=3, wood='jungle')
        dp.lattice(b, x1, 3, z, 'east', height=3, wood='jungle')
    for z in (6, 9, 12):
        dp.lattice(b, x0, 9, z, 'west', height=1, wood='jungle')
        dp.lattice(b, x1, 9, z, 'east', height=1, wood='jungle')
    # Book hall.
    for z in range(5, 14):
        for x in (2, 8):
            if z in (7, 11):
                continue
            for y in (2, 3, 4, 5):
                if x == 8 and z >= 8:
                    continue
                b.set(x, y, z, 'bookshelf')
    for x in (2, 3, 4, 6):
        for y in (2, 3, 4):
            b.set(x, y, 13, 'bookshelf')
    b.custom(5, 2, 13, 'archives', facing='north')
    b.set(4, 2, 10, 'lectern', facing='north', has_book=False, powered=False)
    parts.table(b, 5, 2, 7, wood='jungle')
    parts.chair(b, 4, 2, 7, 'west', wood='jungle')
    parts.chair(b, 6, 2, 7, 'east', wood='jungle')
    parts.rug(b, 3, 8, 6, 11, 2, 'cyan', border='blue')
    b.set(3, 2, 10, 'air')
    dp.lantern(b, 5, 6, 8, chain=0)
    dp.lantern(b, 5, 6, 11)
    parts.stair_run(b, 7, 13, 2, 6, 'north', wood='jungle')
    b.resident(5, 2, 10, 'scholar')
    # Upper floor: reading gallery in front, the scholar's room behind.
    for x in range(2, 9):
        for y in (8, 9, 10):
            b.set(x, y, 10, 'smooth_sandstone')
    b.door(4, 8, 10, facing='south', wood='jungle')
    b.bed(3, 8, 13, 'north', 'blue')
    b.chest(5, 8, 13, 'north', loot=LOOT)
    b.set(6, 8, 13, 'bookshelf')
    b.set(6, 9, 13, 'bookshelf')
    b.set(8, 8, 13, 'bookshelf')
    dp.lantern(b, 5, 10, 12)
    b.room('scholar_bedroom', (5, 9, 12))
    for x in (2, 3):
        for y in (8, 9):
            b.set(x, y, 5, 'bookshelf')
    parts.table(b, 4, 8, 7, wood='jungle')
    dp.lantern(b, 5, 10, 7)
    # Front: steps, palms in pots and lamps.
    for z in range(0, 3):
        b.set(5, 0, z, 'smooth_sandstone' if z % 2 else 'cut_sandstone')
    for x in (2, 8):
        dp.wall_post(b, x, 0, 2, height=2)
    for x in (1, 9):
        dp.pot(b, x, 1, 3, 'cactus')
    plaque(b, 3, 2)
    b.entrance(5)
    b.natural_ground()
    return b


# ------------------------------------------------------------------- markets
def market_souk():
    """Covered souk: three stalls under one long striped canopy with rugs and cushions."""
    rng = random.Random(1307)
    b = Build('desert/market_souk', (11, 7, 11))
    for x in range(0, 11):
        for z in range(0, 11):
            if rng.random() < .9:
                b.set(x, 0, z, rng.choice(['smooth_sandstone', 'sandstone', 'cut_sandstone', 'sand']))
    # Back wall of booths with arched niches.
    for x in range(0, 11):
        for y in range(1, 5):
            b.set(x, y, 10, 'smooth_sandstone' if y < 4 else 'cut_sandstone')
    for x0, col, goods in ((1, 'orange', ['decorated_pot[facing=north]', 'melon', 'hay_block[axis=y]']),
                           (4, 'cyan', ['barrel[facing=up]', 'potted_cactus', 'dried_kelp_block']),
                           (7, 'red', ['red_wool', 'yellow_wool', 'cyan_wool'])):
        for i in range(3):
            b.set(x0 + i, 1, 7, 'acacia_planks' if i != 1 else 'barrel', **({} if i != 1 else {'facing': 'up', 'open': False}))
            b.set(x0 + i, 2, 7, goods[i])
        for i in range(3):
            b.set(x0 + i, 1, 9, f'{col}_carpet')
        b.set(x0 + 1, 1, 8, 'air')
    dp.canopy(b, 0, 6, 10, 9, 4, along='x', posts=((0, 6), (10, 6), (0, 9), (10, 9)))
    for x in range(0, 11):
        b.set(x, 4, 5, 'acacia_trapdoor', facing='north', half='top', open=True, powered=False, waterlogged=False)
    for x in (3, 7):
        dp.lantern(b, x, 3, 8)
    for x, z, f in ((2, 3, 'east'), (8, 3, 'west')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    dp.pot(b, 0, 1, 1, 'cactus')
    dp.pot(b, 10, 1, 1, 'dead_bush')
    b.entrance(5)
    b.natural_ground()
    return b


def market_cistern():
    """Cistern kiosk: a little domed pavilion over a water basin, with palms and benches."""
    rng = random.Random(1308)
    b = Build('desert/market_cistern', (11, 12, 11))
    for x in range(0, 11):
        for z in range(0, 11):
            b.set(x, 0, z, 'smooth_sandstone' if (x + z) % 2 else 'sandstone')
    cx, cz = 5, 6
    for x in range(cx - 2, cx + 3):
        for z in range(cz - 2, cz + 3):
            corner = abs(x - cx) == 2 and abs(z - cz) == 2
            if corner:
                for y in range(1, 4):
                    b.set(x, y, z, 'cut_sandstone')
            elif abs(x - cx) == 2 or abs(z - cz) == 2:
                b.set(x, 1, z, 'smooth_sandstone_slab', type='bottom')
            else:
                b.set(x, 0, z, 'cyan_terracotta')
                b.set(x, 1, z, 'water', level=0)
    b.set(cx, 1, cz, 'chiseled_sandstone')
    for (ax, az, bx, bz) in ((cx - 1, cz - 2, cx + 1, cz - 2), (cx - 1, cz + 2, cx + 1, cz + 2),
                             (cx - 2, cz - 1, cx - 2, cz + 1), (cx + 2, cz - 1, cx + 2, cz + 1)):
        dp.arch(b, ax, az, bx, bz, 3)
    for x in range(cx - 2, cx + 3):
        for z in range(cz - 2, cz + 3):
            if abs(x - cx) == 2 or abs(z - cz) == 2:
                b.set(x, 4, z, 'cut_sandstone')
    top = dp.dome(b, cx, cz, 5, 2, mat='white_terracotta')
    b.set(cx, top + 1, cz, 'gold_block')
    dp.lantern(b, cx, 4, cz)
    b.set(cx, 4, cz, 'lantern', hanging=True, waterlogged=False)
    for x, z in ((1, 9), (9, 2)):
        b.set(x, 0, z, 'sand')
        dp.palm(b, x, 1, z, rng, height=5)
    for x, z, f in ((1, 4, 'east'), (9, 8, 'west')):
        b.custom(x, 1, z, 'village_bench', facing=f)
    dp.pot(b, 9, 1, 10, 'cactus')
    b.entrance(5)
    b.natural_ground()
    return b


def market_spice():
    """Spice and pottery yard: sacks, jars and rugs hung on a frame, shaded by a striped canopy."""
    rng = random.Random(1309)
    b = Build('desert/market_spice', (11, 7, 11))
    for x in range(0, 11):
        for z in range(0, 11):
            if rng.random() < .85:
                b.set(x, 0, z, rng.choice(['sand', 'sandstone', 'smooth_sandstone', 'terracotta']))
    # Rug frame along the back.
    for x in (1, 9):
        b.set(x, 0, 9, 'cut_sandstone')
        for y in (1, 2, 3):
            b.set(x, y, 9, 'acacia_fence')
    for x in range(1, 10):
        b.set(x, 4, 9, 'stripped_acacia_log', axis='x')
    for x, c in zip(range(2, 9), ['red', 'orange', 'yellow', 'cyan', 'magenta', 'orange', 'red']):
        b.set(x, 3, 9, f'{c}_wool')
        if x % 2 == 0:
            b.set(x, 2, 9, f'{c}_wool')
    # Jars and sacks in rows.
    for x in (2, 4, 6, 8):
        for z in (4, 6):
            if rng.random() < .5:
                b.set(x, 1, z, 'decorated_pot', facing=rng.choice(['north', 'east', 'south', 'west']))
            else:
                b.set(x, 1, z, rng.choice(['composter[level=7]', 'barrel[facing=up]', 'hay_block[axis=y]',
                                           'dried_kelp_block', 'pumpkin']))
    dp.canopy(b, 1, 3, 9, 7, 4, along='z', colors=('yellow', 'white', 'orange', 'white'),
              posts=((1, 3), (9, 3), (1, 7), (9, 7)))
    dp.lantern(b, 5, 3, 5)
    dp.pot(b, 0, 1, 0, 'cactus')
    dp.cactus(b, 10, 1, 10, 2)
    b.entrance(5)
    b.natural_ground()
    return b


DESIGNS = {'desert/tavern': tavern, 'desert/garrison': garrison, 'desert/workshop': workshop,
           'desert/chapel': chapel, 'desert/apothecary': apothecary, 'desert/library': library,
           'desert/market_souk': market_souk, 'desert/market_cistern': market_cistern,
           'desert/market_spice': market_spice}
