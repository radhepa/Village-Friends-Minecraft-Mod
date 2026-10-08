"""Desert homes: courtyard houses, a domed house, roof-terrace houses, a pueblo-style
adobe, a windcatcher tower house, an arcaded plaster house, a walled garden house
and the large family courtyard house.

Every home is a drop-in lot: north-facing ``building_entrance`` at [x,1,0], a
paved path to a real front door, at least one enclosed bedroom with paired beds
and a loot chest, and unemployed residents. Homes keep villager job-site blocks
(barrels, smokers, cauldrons, composters) out of their rooms so residents stay
free to take up a trade in the workshops nearby.
"""
import random

from ...kit import Build
from ... import parts
from .palette import AWNINGS
from .homes_kit import (LOOT, plinth, walls, frieze, wall_run, deck, parapet, flat_roof, beam_ends, spouts, lattice,
                        lattice_row, arch, door, awning, dome, palm, cactus, sand_patch, dry_tuft, path_line,
                        paving, hang, stand_lamp, candle, pot, shelf, table, chair, rug, ladder, plant, leaf)

SAND = 'smooth_sandstone'
CUT = 'cut_sandstone'


def kitchen_row(b, cells, y, facing, rng):
    """Hearth, worktop and storage along a wall (no job-site blocks)."""
    items = ['furnace', 'crafting_table', 'pot', 'shelf', 'pot', 'plant']
    for (x, z), item in zip(cells, items):
        if item == 'furnace':
            b.set(x, y, z, 'furnace', facing=facing, lit=False)
        elif item == 'pot':
            pot(b, x, y, z, facing)
        elif item == 'shelf':
            shelf(b, x, y, z, facing)
        elif item == 'plant':
            plant(b, x, y, z, rng)
        else:
            b.set(x, y, z, item)


def plaque(b, x, z):
    b.custom(x, 1, z, 'house_plaque', facing='north')


# --------------------------------------------------------------------------- 1
def courtyard_house():
    """Small L-shaped house: an arched gate opens into a paved courtyard with a
    palm and a pool; kitchen loggia on one side, living room and bedroom behind."""
    rng = random.Random(2101)
    b = Build('desert/courtyard_house', (15, 10, 16))
    # Kitchen wing (west) and main block (south).
    plinth(b, 1, 2, 5, 8)
    walls(b, 1, 2, 5, 8, 2, 4, SAND, corner=CUT)
    plinth(b, 1, 8, 13, 14)
    walls(b, 1, 8, 13, 14, 2, 4, SAND, corner=CUT)
    frieze(b, 1, 2, 5, 8, 4)
    frieze(b, 1, 8, 13, 14, 4)
    deck(b, 1, 2, 5, 8, 5)
    deck(b, 1, 8, 13, 14, 5)
    shared = {(x, 8) for x in (2, 3, 4)}
    parapet(b, 1, 2, 5, 8, 6, skip=shared)
    parapet(b, 1, 8, 13, 14, 6, skip=shared)
    spouts(b, [(0, 11), (14, 11), (7, 15), (0, 5)], 5)
    # Wing opens onto the courtyard through an arch; doorway into the living room.
    b.clear(5, 2, 4, 5, 4, 6)
    arch(b, (5, 4), (5, 6), 4, 'z')
    b.clear(3, 2, 8, 3, 3, 8)
    # Courtyard walls, gateway and pillar lantern.
    wall_run(b, 6, 2, 13, 2, 1, 3, SAND)
    wall_run(b, 13, 3, 13, 7, 1, 3, SAND)
    for x, z in [(x, 2) for x in range(6, 14)] + [(13, z) for z in range(3, 8)]:
        if (x + z) % 2 == 0:
            b.set(x, 4, z, 'cut_sandstone_slab', type='bottom', waterlogged=False)
    b.clear(6, 1, 2, 8, 2, 2)
    arch(b, (6, 2), (8, 2), 2, 'x')
    b.set(7, 3, 2, 'chiseled_sandstone')
    b.set(9, 4, 2, CUT)
    stand_lamp(b, 9, 5, 2)
    paving(b, 6, 3, 12, 7, rng)
    # Pool and palm.
    for x in (9, 10):
        for z in (4, 5):
            b.set(x, 0, z, 'water', level=0)
    for x, z in ((9, 3), (10, 3), (9, 6), (10, 6), (8, 4), (8, 5), (11, 4), (11, 5)):
        b.set(x, 1, z, 'smooth_sandstone_slab', type='bottom', waterlogged=False)
    b.set(12, 0, 4, 'sand')
    palm(b, 12, 1, 4, height=6, lean='west')
    b.custom(12, 1, 6, 'village_bench', facing='west')
    pot(b, 12, 1, 7, 'west')
    # Front door with a striped awning.
    door(b, 7, 2, 8, 'north', lamp=False, frame='cyan_terracotta')
    awning(b, 6, 6, 8, 7, 4, colors=('orange', 'white'), posts=[(6, 6), (8, 6)])
    hang(b, 8, 3, 7)  # beside the door: a lantern in the doorway blocks it
    # Kitchen loggia.
    kitchen_row(b, [(2, 3), (3, 3), (4, 3), (2, 4), (2, 5), (4, 7)], 2, 'south', rng)
    pot(b, 2, 2, 6, 'east')
    hang(b, 3, 4, 5)
    # Living room.
    rug(b, 3, 10, 6, 12, 2, 'orange', 'red')
    table(b, 4, 2, 11, cloth='white_carpet')
    chair(b, 3, 2, 11, 'west')
    chair(b, 5, 2, 11, 'east')
    chair(b, 4, 2, 13, 'south')
    b.custom(5, 2, 13, 'fireside_armchair', facing='north')
    chair(b, 6, 2, 13, 'south')
    shelf(b, 2, 3, 11, 'east')
    plant(b, 2, 2, 13, rng)
    pot(b, 7, 2, 13, 'north')
    hang(b, 4, 4, 11)
    # Bedroom.
    wall_run(b, 8, 9, 8, 13, 2, 4, SAND)
    b.door(8, 2, 11, facing='east', wood='acacia')
    b.bed(10, 2, 12, 'south', 'orange')
    b.bed(12, 2, 12, 'south', 'yellow')
    b.chest(11, 2, 13, 'north', loot=LOOT)
    rug(b, 10, 9, 12, 10, 2, 'white')
    plant(b, 12, 2, 9, rng)
    hang(b, 11, 4, 11)
    b.room('bedroom', (10, 3, 11))
    # Windows.
    lattice_row(b, [(10, 8), (11, 8)], 3, 'north')
    lattice_row(b, [(1, 10), (1, 12)], 3, 'west')
    lattice_row(b, [(13, 10), (13, 12)], 3, 'east')
    lattice_row(b, [(4, 14), (6, 14), (10, 14), (11, 14)], 3, 'south')
    lattice(b, 3, 3, 2, 'north')
    lattice(b, 1, 3, 5, 'west')
    # Street front.
    path_line(b, 7, 0, 1, rng)
    sand_patch(b, [(x, z) for x in range(1, 6) for z in (0, 1)] + [(x, 0) for x in range(9, 13)], rng, .3)
    plaque(b, 10, 1)
    cactus(b, 13, 0, 2, flower=True)
    b.entrance(7)
    b.resident(6, 2, 10)
    b.resident(9, 1, 7, child=True)
    b.natural_ground()
    return b


# --------------------------------------------------------------------------- 2
def dome_house():
    """A tall domed hall with a side bedroom and a striped porch canopy."""
    rng = random.Random(2102)
    b = Build('desert/dome_house', (13, 13, 14))
    plinth(b, 1, 4, 11, 12)
    walls(b, 1, 4, 11, 12, 2, 5, SAND, corner=CUT)
    frieze(b, 1, 4, 11, 12, 5, ('cyan_terracotta',))
    deck(b, 1, 4, 11, 12, 6)
    parapet(b, 1, 4, 11, 12, 7, cap='smooth_sandstone_slab', style='low')
    # The hall rises into the dome.
    dome(b, 4, 8, 6, 3, mat=SAND)
    for x in range(2, 7):
        for z in range(6, 11):
            if (x - 4) ** 2 + (z - 8) ** 2 <= 4:
                b.set(x, 6, z, 'air')
    for y in (7, 8):
        b.set(4, y, 8, 'iron_chain', axis='y', waterlogged=False)
    hang(b, 4, 6, 8)
    # Small dome cupola over the bedroom.
    b.set(9, 7, 8, CUT)
    b.set(9, 8, 8, 'sandstone_wall')
    stand_lamp(b, 9, 9, 8)
    # Porch.
    door(b, 4, 2, 4, 'north', lamp=False, frame='white_terracotta')
    awning(b, 2, 2, 6, 3, 5, colors=(AWNINGS[4], 'white'), posts=[(2, 2), (6, 2)])
    paving(b, 2, 1, 6, 3, rng)
    hang(b, 4, 4, 3)
    # Hall: dining, hearth and shelves.
    rug(b, 3, 7, 5, 9, 2, 'cyan', 'white')
    table(b, 4, 2, 8, cloth='orange_carpet')
    chair(b, 3, 2, 8, 'west')
    chair(b, 5, 2, 8, 'east')
    kitchen_row(b, [(2, 11), (3, 11), (5, 11), (2, 10), (6, 11)], 2, 'north', rng)
    shelf(b, 2, 3, 7, 'east')
    plant(b, 6, 2, 5, rng)
    pot(b, 2, 2, 5, 'east')
    # Bedroom.
    wall_run(b, 7, 5, 7, 11, 2, 5, SAND)
    b.door(7, 2, 6, facing='east', wood='acacia')
    b.bed(8, 2, 10, 'south', 'cyan')
    b.bed(10, 2, 10, 'south', 'white')
    b.chest(9, 2, 11, 'north', loot=LOOT)
    rug(b, 8, 7, 10, 8, 2, 'yellow')
    pot(b, 10, 2, 5, 'west')
    candle(b, 10, 2, 6, 3)
    b.set(10, 1, 6, SAND)
    hang(b, 9, 5, 8)
    b.room('bedroom', (9, 3, 9))
    # Windows.
    lattice_row(b, [(1, 7), (1, 9)], 3, 'west', height=2)
    lattice_row(b, [(2, 4), (6, 4)], 3, 'north', height=2)
    lattice_row(b, [(11, 7), (11, 9)], 3, 'east', height=2)
    lattice_row(b, [(4, 12), (9, 12)], 3, 'south', height=2)
    lattice(b, 9, 3, 4, 'north', height=2)
    # Yard.
    path_line(b, 4, 0, 0, rng)
    sand_patch(b, [(x, 0) for x in range(7, 13)] + [(0, z) for z in range(2, 14)] + [(12, z) for z in range(4, 14)],
               rng, .3)
    b.set(10, 0, 1, 'sand')
    palm(b, 10, 1, 1, height=6, lean='east')
    plaque(b, 8, 1)
    b.entrance(4)
    b.resident(3, 2, 6)
    b.natural_ground()
    return b


# --------------------------------------------------------------------------- 3
def terrace_house():
    """Two storeys: living room below, a bedroom with a wooden lattice bay above
    and a shaded roof terrace reached by a ladder."""
    rng = random.Random(2103)
    b = Build('desert/terrace_house', (13, 14, 15))
    plinth(b, 1, 4, 11, 12)
    walls(b, 1, 4, 11, 12, 2, 4, SAND, corner=CUT)
    deck(b, 1, 4, 11, 12, 5)
    walls(b, 1, 4, 11, 12, 6, 8, SAND, corner=CUT)
    frieze(b, 1, 4, 11, 12, 4, ('orange_terracotta', 'white_terracotta'))
    flat_roof(b, 1, 4, 11, 12, 9)
    beam_ends(b, 1, 4, 11, 12, 8, sides=('north', 'west', 'east'))
    spouts(b, [(0, 8), (12, 8), (6, 13)], 9)
    # Stairs along the east wall, railing round the stairwell.
    parts.stair_run(b, 10, 11, 2, 4, 'north', wood='acacia')
    for z in (9, 10, 11):
        b.set(9, 6, z, 'acacia_fence')
    b.set(10, 6, 11, 'acacia_fence')
    ladder(b, 10, 6, 9, 5, 'west')
    # Front door and canopy.
    door(b, 8, 2, 4, 'north', lamp=False, frame='red_terracotta')
    awning(b, 7, 2, 9, 3, 4, colors=('red', 'white'), posts=[(7, 2), (9, 2)])
    # Ground floor.
    for x in (2, 3, 4):
        chair(b, x, 2, 5, 'north')
    rug(b, 3, 7, 7, 9, 2, 'red', 'orange')
    table(b, 5, 2, 8, cloth='white_carpet')
    chair(b, 4, 2, 8, 'west')
    chair(b, 6, 2, 8, 'east')
    kitchen_row(b, [(2, 11), (3, 11), (4, 11), (2, 10), (5, 11), (7, 11)], 2, 'north', rng)
    shelf(b, 2, 3, 8, 'east')
    hang(b, 5, 4, 8)
    hang(b, 3, 4, 6)
    # Upstairs bedroom behind a partition, with a lattice bay on the street.
    wall_run(b, 8, 5, 8, 11, 6, 8, SAND)
    b.door(8, 6, 6, facing='east', wood='acacia')
    b.clear(3, 6, 4, 5, 7, 4)
    for x in (3, 4, 5):
        b.set(x, 4, 3, 'sandstone_stairs', facing='south', half='top', shape='straight', waterlogged=False, lock=True)
        b.set(x, 5, 3, 'jungle_slab', type='top', waterlogged=False)
        lattice(b, x, 6, 3, 'south', height=2)
        b.set(x, 8, 3, 'jungle_slab', type='bottom', waterlogged=False)
    b.bed(2, 6, 10, 'south', 'red')
    b.bed(4, 6, 10, 'south', 'orange')
    b.chest(3, 6, 11, 'north', loot=LOOT)
    rug(b, 3, 6, 6, 8, 6, 'white', 'cyan')
    plant(b, 6, 6, 11, rng)
    pot(b, 7, 6, 11, 'north')
    shelf(b, 7, 7, 9, 'west')
    hang(b, 4, 8, 8)
    b.room('bedroom', (5, 7, 9))
    plant(b, 9, 6, 5, rng)
    hang(b, 9, 8, 7)
    # Windows.
    lattice_row(b, [(3, 4), (5, 4)], 3, 'north')
    lattice_row(b, [(1, 7), (1, 9)], 3, 'west')
    lattice_row(b, [(3, 12), (6, 12)], 3, 'south')
    lattice(b, 11, 3, 6, 'east')
    lattice_row(b, [(1, 7), (1, 9)], 7, 'west')
    lattice_row(b, [(3, 12), (5, 12)], 7, 'south')
    lattice(b, 11, 7, 8, 'east')
    lattice(b, 9, 7, 4, 'north')
    # Roof terrace: canopy, low table and plants.
    awning(b, 2, 8, 6, 11, 12, colors=('orange', 'white'), stripe='z')
    for x, z in ((2, 8), (6, 8), (2, 11), (6, 11)):
        b.set(x, 10, z, 'acacia_fence')
        b.set(x, 11, z, 'acacia_fence')
    rug(b, 3, 9, 5, 10, 10, 'red')
    table(b, 4, 10, 9, cloth='orange_carpet')
    chair(b, 4, 10, 10, 'south')
    chair(b, 3, 10, 9, 'west')
    chair(b, 5, 10, 9, 'east')
    hang(b, 4, 11, 10)
    pot(b, 10, 10, 11, 'west')
    plant(b, 9, 10, 11, rng)
    plant(b, 2, 10, 5, rng)
    pot(b, 6, 10, 5, 'south')
    # Street front.
    path_line(b, 8, 0, 2, rng)
    sand_patch(b, [(x, z) for x in range(1, 7) for z in (0, 1, 2)] + [(x, 0) for x in (10, 11)], rng, .3)
    pot(b, 2, 1, 2, 'north')
    pot(b, 3, 1, 2, 'north')
    plaque(b, 10, 1)
    b.entrance(8)
    b.resident(6, 2, 6)
    b.resident(5, 6, 7, child=True)
    b.natural_ground()
    return b


# --------------------------------------------------------------------------- 4
def family_house():
    """The large courtyard home: rooms on four sides of a paved court with a pool
    and a tall palm, an arcaded sitting room, an upper guest storey and a roof terrace."""
    rng = random.Random(2104)
    b = Build('desert/family_house', (19, 16, 19))
    plinth(b, 1, 3, 17, 17)
    walls(b, 1, 3, 17, 17, 2, 4, SAND, corner=CUT)
    frieze(b, 1, 3, 17, 17, 4, ('orange_terracotta', 'yellow_terracotta'))
    # Inner walls: wings, courtyard ring.
    wall_run(b, 6, 4, 6, 16, 2, 4, SAND)
    wall_run(b, 12, 4, 12, 16, 2, 4, SAND)
    wall_run(b, 6, 7, 12, 7, 2, 4, SAND)
    wall_run(b, 6, 13, 12, 13, 2, 4, SAND)
    wall_run(b, 2, 10, 5, 10, 2, 4, SAND)
    wall_run(b, 13, 10, 16, 10, 2, 4, SAND)
    # Ground-floor roof (terrace) with the courtyard left open.
    deck(b, 1, 3, 17, 17, 5)
    b.clear(7, 5, 8, 11, 5, 12)
    for x, z, _, _ in parts.ring(6, 7, 12, 13):
        b.set(x, 5, z, CUT)
    parapet(b, 1, 3, 17, 17, 6)
    for x, z, _, _ in parts.ring(6, 7, 12, 13):
        if z != 13:
            b.set(x, 6, z, 'sandstone_wall')
    # Upper storey over the back range.
    walls(b, 1, 13, 17, 17, 6, 8, SAND, corner=CUT)
    frieze(b, 1, 13, 17, 17, 8, ('orange_terracotta', 'yellow_terracotta'))
    flat_roof(b, 1, 13, 17, 17, 9)
    dome(b, 9, 15, 10, 2, mat=SAND)
    spouts(b, [(0, 8), (18, 8), (0, 15), (18, 15)], 5)
    # Openings.
    door(b, 9, 2, 3, 'north', lamp=False, frame='cyan_terracotta')
    b.clear(8, 2, 7, 10, 4, 7)
    arch(b, (8, 7), (10, 7), 4, 'x')
    b.clear(6, 2, 5, 6, 3, 5)
    b.clear(12, 2, 5, 12, 3, 5)
    b.clear(6, 2, 9, 6, 3, 9)
    b.door(6, 2, 11, facing='east', wood='acacia')
    b.door(12, 2, 11, facing='west', wood='acacia')
    b.clear(7, 2, 13, 8, 4, 13)
    b.clear(10, 2, 13, 11, 4, 13)
    arch(b, (7, 13), (8, 13), 4, 'x')
    arch(b, (10, 13), (11, 13), 4, 'x')
    # Courtyard: paving, pool, palm.
    paving(b, 7, 8, 11, 12, rng, y=1, mats=('cut_sandstone', 'smooth_sandstone'))
    for x in range(8, 11):
        for z in range(9, 12):
            b.set(x, 1, z, 'water', level=0)
    b.set(9, 1, 10, 'chiseled_sandstone')
    b.set(9, 2, 10, 'sandstone_wall')
    stand_lamp(b, 9, 3, 10)
    b.set(7, 1, 8, 'sand')
    palm(b, 7, 2, 8, height=7, lean='south')
    for x, z in ((11, 8), (11, 12), (7, 12)):
        pot(b, x, 2, z, 'north')
    # Front door canopy and street front.
    awning(b, 8, 1, 10, 2, 4, colors=('cyan', 'white'), posts=[(8, 1), (10, 1)])
    hang(b, 10, 3, 2)  # beside the door, not in the doorway
    path_line(b, 9, 0, 1, rng)
    pot(b, 7, 1, 2, 'north')
    pot(b, 11, 1, 2, 'north')
    plaque(b, 12, 1)
    sand_patch(b, [(x, z) for x in list(range(1, 7)) + list(range(13, 18)) for z in (0, 1, 2)], rng, .25)
    # Entrance hall.
    rug(b, 8, 5, 10, 6, 2, 'red', 'orange')
    pot(b, 7, 2, 4, 'south')
    pot(b, 11, 2, 4, 'south')
    hang(b, 9, 4, 5)
    # Kitchen (west front).
    kitchen_row(b, [(2, 4), (3, 4), (4, 4), (2, 5), (2, 9), (5, 4)], 2, 'south', rng)
    shelf(b, 2, 3, 7, 'east')
    table(b, 3, 2, 7, cloth='white_carpet')
    chair(b, 3, 2, 8, 'south')
    chair(b, 4, 2, 7, 'east')
    hang(b, 3, 4, 6)
    # Children's room (west back).
    b.bed(2, 2, 15, 'south', 'lime')
    b.bed(4, 2, 15, 'south', 'yellow')
    b.chest(3, 2, 16, 'north', loot=LOOT)
    rug(b, 2, 12, 4, 13, 2, 'lime')
    candle(b, 5, 2, 16, 2)
    b.set(5, 1, 16, SAND)
    hang(b, 3, 4, 13)
    b.room('children_room', (3, 3, 12))
    # Parlour (east front).
    chair(b, 16, 2, 5, 'east')
    b.custom(16, 2, 6, 'fireside_armchair', facing='west')
    chair(b, 16, 2, 7, 'east')
    table(b, 14, 2, 6, cloth='cyan_carpet')
    rug(b, 14, 7, 15, 9, 2, 'cyan', 'white')
    plant(b, 16, 2, 4, rng)
    plant(b, 16, 2, 9, rng)
    shelf(b, 13, 3, 9, 'east')
    hang(b, 14, 4, 7)
    # Parents' room (east back).
    b.bed(14, 2, 15, 'south', 'red')
    b.bed(16, 2, 15, 'south', 'red')
    b.chest(15, 2, 16, 'north', loot=LOOT)
    rug(b, 14, 12, 16, 13, 2, 'orange', 'red')
    pot(b, 13, 2, 16, 'east')
    hang(b, 15, 4, 13)
    b.room('parents_room', (15, 3, 12))
    # Arcaded sitting room (back) with the stair to the upper storey.
    parts.stair_run(b, 7, 16, 2, 4, 'east', wood='acacia')
    chair(b, 11, 2, 14, 'east')
    chair(b, 11, 2, 15, 'east')
    rug(b, 8, 14, 10, 15, 2, 'white', 'orange')
    hang(b, 9, 4, 14)
    # Upper storey: guest room and a sitting room opening onto the terrace.
    wall_run(b, 7, 14, 7, 16, 6, 8, SAND)
    b.door(7, 6, 14, facing='east', wood='acacia')
    b.bed(2, 6, 15, 'south', 'white')
    b.bed(5, 6, 15, 'south', 'white')
    b.chest(3, 6, 16, 'north', loot=LOOT)
    plant(b, 4, 6, 16, rng)
    hang(b, 4, 8, 15)
    b.room('guest_room', (4, 7, 14))
    b.set(8, 6, 15, 'acacia_fence')
    b.set(9, 6, 15, 'acacia_fence')
    door(b, 14, 6, 13, 'north', step=None, lamp=False)
    rug(b, 12, 15, 15, 16, 6, 'orange', 'yellow')
    table(b, 13, 6, 16, cloth='white_carpet')
    chair(b, 16, 6, 16, 'east')
    chair(b, 16, 6, 15, 'east')
    pot(b, 11, 6, 14, 'south')
    hang(b, 13, 8, 15)
    # Terrace canopy.
    awning(b, 13, 4, 16, 7, 8, colors=('orange', 'white'))
    for x, z in ((13, 7), (16, 7)):
        for y in (6, 7):
            b.set(x, y, z, 'acacia_fence')
    chair(b, 14, 6, 4, 'north')
    chair(b, 15, 6, 4, 'north')
    hang(b, 14, 7, 6)
    pot(b, 2, 6, 4, 'south')
    plant(b, 3, 6, 4, rng)
    # Windows.
    lattice_row(b, [(3, 3), (4, 3), (14, 3), (15, 3)], 3, 'north')
    lattice_row(b, [(1, 6), (1, 12), (1, 15)], 3, 'west')
    lattice_row(b, [(17, 6), (17, 12), (17, 15)], 3, 'east')
    lattice_row(b, [(3, 17), (9, 17), (15, 17)], 3, 'south')
    lattice_row(b, [(12, 8)], 3, 'west')
    lattice_row(b, [(6, 15)], 3, 'east')
    lattice_row(b, [(3, 13), (5, 13), (10, 13), (16, 13)], 7, 'north')
    lattice_row(b, [(3, 17), (5, 17), (9, 17), (13, 17), (15, 17)], 7, 'south')
    lattice_row(b, [(1, 15)], 7, 'west')
    lattice_row(b, [(17, 15)], 7, 'east')
    b.entrance(9)
    b.resident(4, 2, 6)
    b.resident(14, 2, 8)
    b.resident(8, 2, 8, child=True)
    b.natural_ground()
    return b


# --------------------------------------------------------------------------- 5
def adobe_house():
    """Pueblo-style ochre adobe: rounded corners, projecting roof beams and a
    stepped upper bedroom reached by a ladder over the lower roof."""
    rng = random.Random(2105)
    b = Build('desert/adobe_house', (11, 12, 13))
    fill, upper = 'yellow_terracotta', 'orange_terracotta'
    plinth(b, 1, 3, 8, 10)
    walls(b, 1, 3, 8, 10, 2, 4, fill)
    deck(b, 1, 3, 8, 10, 5, edge='orange_terracotta')
    parapet(b, 1, 3, 8, 10, 6, cap='smooth_sandstone_slab', style='low', skip={(8, 7)})
    beam_ends(b, 1, 3, 8, 10, 4)
    walls(b, 1, 5, 5, 10, 6, 8, upper)
    deck(b, 1, 5, 5, 10, 9, edge='terracotta')
    parapet(b, 1, 5, 5, 10, 10, cap='smooth_sandstone_slab', style='low')
    beam_ends(b, 1, 5, 5, 10, 8, sides=('north', 'east'))
    # Soften the corners.
    for x, z in ((1, 3), (8, 3), (1, 10), (8, 10)):
        b.clear(x, 2, z, x, 6, z)
        b.set(x, 1, z, 'sandstone_slab', type='bottom', waterlogged=False)
    for x, z in ((1, 5), (5, 5), (1, 10), (5, 10)):
        b.clear(x, 6, z, x, 10, z)
    b.set(1, 5, 10, 'air')
    b.set(5, 5, 5, 'smooth_sandstone')
    # Doors and ladder.
    door(b, 4, 2, 3, 'north', lamp=True, frame='cyan_terracotta')
    ladder(b, 9, 1, 6, 7, 'east')
    door(b, 5, 6, 7, 'east', step=None, lamp=False)
    # Ground floor.
    kitchen_row(b, [(2, 9), (3, 9), (7, 9), (7, 8), (6, 9), (2, 4)], 2, 'north', rng)
    rug(b, 4, 5, 6, 7, 2, 'orange', 'brown')
    table(b, 5, 2, 6, cloth='red_carpet')
    chair(b, 4, 2, 6, 'west')
    chair(b, 6, 2, 6, 'east')
    shelf(b, 2, 3, 6, 'east')
    pot(b, 7, 2, 4, 'west')
    hang(b, 5, 4, 6)
    # Upper bedroom.
    b.bed(2, 6, 8, 'south', 'orange')
    b.bed(4, 6, 8, 'south', 'brown')
    b.chest(3, 6, 9, 'north', loot=LOOT)
    pot(b, 2, 6, 6, 'east')
    b.set(3, 6, 7, 'red_carpet')
    hang(b, 3, 8, 7)
    b.room('bedroom', (3, 7, 6))
    # Windows.
    lattice_row(b, [(2, 3), (6, 3)], 3, 'north', sill='cut_sandstone_slab')
    lattice_row(b, [(1, 6), (1, 8)], 3, 'west')
    lattice_row(b, [(8, 5)], 3, 'east')
    lattice_row(b, [(3, 10), (6, 10)], 3, 'south')
    lattice(b, 1, 7, 7, 'west')
    lattice(b, 3, 7, 10, 'south')
    lattice(b, 3, 7, 5, 'north')
    # Roof-terrace clutter: drying rack and pots.
    for x in (6, 7):
        b.set(x, 6, 9, 'acacia_fence')
    b.set(6, 7, 9, 'acacia_fence')
    b.set(7, 7, 9, 'acacia_fence')
    pot(b, 7, 6, 4, 'west')
    plant(b, 6, 6, 4, rng)
    # Yard.
    path_line(b, 4, 0, 1, rng)
    sand_patch(b, [(x, z) for x in range(0, 11) for z in (0, 1)], rng, .3)
    b.set(4, 0, 0, 'cut_sandstone')
    b.set(4, 0, 1, 'smooth_sandstone')
    b.set(4, 1, 0, 'air')
    b.set(4, 1, 1, 'air')
    cactus(b, 9, 1, 2)
    plaque(b, 6, 1)
    b.entrance(4)
    b.resident(5, 2, 8)
    b.resident(3, 6, 6, child=True)
    b.natural_ground()
    return b


# --------------------------------------------------------------------------- 6
def tower_house():
    """Two-storey tower house with an outside stair climbing the flank to the
    bedroom door and the roof, where a windcatcher catches the breeze."""
    rng = random.Random(2106)
    b = Build('desert/tower_house', (12, 18, 14))
    plinth(b, 1, 3, 9, 11)
    walls(b, 1, 3, 9, 11, 2, 4, 'sandstone', corner=CUT)
    deck(b, 1, 3, 9, 11, 5)
    walls(b, 1, 3, 9, 11, 6, 8, 'sandstone', corner=CUT)
    frieze(b, 1, 3, 9, 11, 4)
    frieze(b, 1, 3, 9, 11, 8)
    flat_roof(b, 1, 3, 9, 11, 9, skip={(9, 4)})
    # Outside stair: solid ramp under the steps, parapet wall on its outer side.
    for k in range(1, 10):
        z = 13 - k
        for y in range(0, k):
            b.set(10, y, z, 'sandstone')
            b.set(11, y, z, 'sandstone')
        b.set(10, k, z, 'sandstone_stairs', facing='north', half='bottom', shape='straight', waterlogged=False,
              lock=True)
        b.set(11, k, z, 'sandstone')
        b.set(11, k + 1, z, 'sandstone_wall')
    b.set(10, 0, 13, 'sandstone')
    # Upper bedroom door off the stair landing.
    door(b, 9, 6, 8, 'east', step=None, lamp=False)
    # Front door.
    door(b, 5, 2, 3, 'north', lamp=True)
    # Ground floor.
    kitchen_row(b, [(2, 10), (3, 10), (4, 10), (2, 9), (6, 10), (8, 10)], 2, 'north', rng)
    rug(b, 4, 6, 6, 8, 2, 'yellow', 'orange')
    table(b, 5, 2, 7, cloth='white_carpet')
    chair(b, 4, 2, 7, 'west')
    chair(b, 6, 2, 7, 'east')
    b.custom(8, 2, 5, 'fireside_armchair', facing='west')
    b.custom(8, 2, 7, 'fireside_armchair', facing='west')
    shelf(b, 2, 3, 6, 'east')
    plant(b, 2, 2, 4, rng)
    hang(b, 5, 4, 7)
    # Upper bedroom.
    b.bed(2, 6, 9, 'south', 'yellow')
    b.bed(4, 6, 9, 'south', 'orange')
    b.chest(3, 6, 10, 'north', loot=LOOT)
    rug(b, 3, 5, 6, 7, 6, 'white', 'yellow')
    pot(b, 8, 6, 10, 'west')
    plant(b, 8, 6, 4, rng)
    shelf(b, 2, 7, 6, 'east')
    hang(b, 5, 8, 7)
    b.room('bedroom', (6, 7, 9))
    # Windows.
    lattice_row(b, [(3, 3), (7, 3)], 3, 'north', sill='cut_sandstone_slab')
    lattice_row(b, [(1, 6), (1, 8)], 3, 'west')
    lattice_row(b, [(4, 11), (7, 11)], 3, 'south')
    lattice_row(b, [(3, 3), (5, 3), (7, 3)], 6, 'north', height=2, sill='cut_sandstone_slab')
    lattice_row(b, [(1, 6), (1, 8)], 7, 'west')
    lattice_row(b, [(5, 11)], 6, 'south', height=2)
    # Windcatcher.
    walls(b, 2, 8, 4, 10, 10, 14, SAND, corner=CUT)
    b.fill(3, 10, 9, 3, 14, 9, SAND)
    for x, z, face in ((3, 8, 'north'), (3, 10, 'south'), (2, 9, 'west'), (4, 9, 'east')):
        lattice(b, x, 13, z, face, height=2)
    for x in (2, 3, 4):
        for z in (8, 9, 10):
            b.set(x, 15, z, CUT if (x, z) != (3, 9) else 'chiseled_sandstone')
    for x, z in ((2, 8), (4, 8), (2, 10), (4, 10)):
        b.set(x, 16, z, 'cut_sandstone_slab', type='bottom', waterlogged=False)
    # Roof terrace.
    awning(b, 5, 4, 8, 6, 12, colors=('yellow', 'white'))
    for x, z in ((5, 6), (8, 6)):
        b.set(x, 10, z, 'acacia_fence')
        b.set(x, 11, z, 'acacia_fence')
    chair(b, 6, 10, 4, 'north')
    chair(b, 7, 10, 4, 'north')
    rug(b, 6, 5, 7, 5, 10, 'orange')
    hang(b, 6, 11, 5)
    pot(b, 8, 10, 10, 'west')
    plant(b, 7, 10, 10, rng)
    # Yard.
    path_line(b, 5, 0, 2, rng)
    sand_patch(b, [(x, z) for x in range(0, 10) for z in (0, 1, 2) if x != 5] + [(0, z) for z in range(3, 14)],
               rng, .3)
    plaque(b, 7, 1)
    pot(b, 3, 1, 2, 'north')
    b.entrance(5)
    b.resident(3, 2, 6)
    b.resident(6, 6, 6, child=True)
    b.natural_ground()
    return b


# --------------------------------------------------------------------------- 7
def plaster_house():
    """Whitewashed house fronted by a three-arched loggia with tiled floor; a white
    dome rises over the living room."""
    rng = random.Random(2107)
    b = Build('desert/plaster_house', (15, 11, 14))
    white = 'white_terracotta'
    plinth(b, 1, 2, 13, 12)
    walls(b, 1, 5, 13, 12, 2, 4, white, corner='stripped_jungle_log', base=None)
    frieze(b, 1, 5, 13, 12, 4, ('light_blue_terracotta',), only=('west', 'east', 'south'))
    # Loggia: arcade on the street side.
    wall_run(b, 1, 3, 1, 4, 2, 4, white)
    wall_run(b, 13, 3, 13, 4, 2, 4, white)
    for x in (1, 5, 9, 13):
        wall_run(b, x, 2, x, 2, 2, 4, white)
    for x0 in (2, 6, 10):
        arch(b, (x0, 2), (x0 + 2, 2), 4, 'x')
    flat_roof(b, 1, 2, 13, 12, 5, parapet_mat=white, cap='smooth_sandstone_slab')
    for x in range(2, 13):
        b.set(x, 5, 2, CUT)
    for i, x in enumerate(range(2, 13)):
        b.set(x, 1, 3, 'cyan_glazed_terracotta', facing=('north', 'east', 'south', 'west')[i % 4])
    b.set(7, 1, 1, 'sandstone_stairs', facing='south', half='bottom', shape='straight', waterlogged=False, lock=True)
    b.custom(3, 2, 4, 'village_bench', facing='south')
    b.custom(11, 2, 4, 'village_bench', facing='south')
    pot(b, 2, 2, 3, 'east')
    pot(b, 12, 2, 3, 'west')
    plant(b, 4, 2, 4, rng)
    plant(b, 10, 2, 4, rng)
    hang(b, 3, 4, 3)
    hang(b, 11, 4, 3)
    hang(b, 7, 4, 3)
    # Dome over the living room.
    dome(b, 5, 8.5, 6, 2, mat=white, finial='sandstone_wall')
    door(b, 7, 2, 5, 'north', wood='jungle', step=None, lamp=False, frame='light_blue_terracotta')
    # Living room.
    for z in (7, 8, 9):
        chair(b, 2, 2, z, 'west', wood='jungle')
    rug(b, 4, 7, 6, 10, 2, 'cyan', 'white')
    table(b, 5, 2, 9, wood='jungle', cloth='white_carpet')
    chair(b, 5, 2, 10, 'south', wood='jungle')
    chair(b, 6, 2, 9, 'east', wood='jungle')
    kitchen_row(b, [(8, 11), (7, 11), (6, 11), (2, 11), (3, 11), (2, 6)], 2, 'north', rng)
    shelf(b, 2, 3, 10, 'east', wood='jungle')
    hang(b, 5, 4, 8)
    # Bedroom.
    wall_run(b, 9, 6, 9, 11, 2, 4, white)
    b.door(9, 2, 8, facing='east', wood='jungle')
    b.bed(10, 2, 10, 'south', 'cyan')
    b.bed(12, 2, 10, 'south', 'light_blue')
    b.chest(11, 2, 11, 'north', loot=LOOT)
    rug(b, 10, 6, 12, 7, 2, 'light_blue')
    candle(b, 12, 2, 8, 2, 'white')
    b.set(12, 1, 8, SAND)
    hang(b, 11, 4, 9)
    b.room('bedroom', (11, 3, 8))
    # Windows.
    lattice_row(b, [(4, 5), (11, 5)], 3, 'north', wood='jungle')
    lattice_row(b, [(1, 8), (1, 10)], 3, 'west', wood='jungle', height=2)
    lattice_row(b, [(13, 7), (13, 10)], 3, 'east', wood='jungle', height=2)
    lattice_row(b, [(4, 12), (6, 12), (11, 12)], 3, 'south', wood='jungle', height=2)
    # Yard.
    path_line(b, 7, 0, 0, rng)
    sand_patch(b, [(x, z) for x in range(0, 15) for z in (0, 1) if x != 7] + [(0, z) for z in range(2, 14)]
               + [(14, z) for z in range(2, 14)], rng, .3)
    plaque(b, 5, 1)
    pot(b, 9, 1, 1, 'north')
    b.entrance(7)
    b.resident(4, 2, 7)
    b.resident(8, 2, 3, child=True)
    b.natural_ground()
    return b


# --------------------------------------------------------------------------- 8
def garden_house():
    """A walled four-part garden with a fountain and palm, the house across the back."""
    rng = random.Random(2108)
    b = Build('desert/garden_house', (15, 11, 18))
    # Garden walls with a gateway.
    wall_run(b, 1, 2, 13, 2, 1, 2, SAND)
    wall_run(b, 1, 3, 1, 9, 1, 2, SAND)
    wall_run(b, 13, 3, 13, 9, 1, 2, SAND)
    for x, z in [(x, 2) for x in range(1, 14)] + [(1, z) for z in range(3, 10)] + [(13, z) for z in range(3, 10)]:
        b.set(x, 3, z, 'smooth_sandstone_slab', type='bottom', waterlogged=False)
    b.clear(7, 1, 2, 7, 3, 2)
    for x in (6, 8):
        b.set(x, 3, 2, CUT)
        b.set(x, 4, 2, 'chiseled_sandstone')
        stand_lamp(b, x, 5, 2)
    # Garden: cross paths, fountain, planted quarters, palm.
    for z in range(3, 10):
        b.set(7, 0, z, 'cut_sandstone' if z % 2 else SAND)
    paving(b, 6, 5, 8, 7, rng)
    b.set(7, 0, 6, 'sandstone')
    b.set(7, 1, 6, 'water', level=0)
    for x, z in ((6, 6), (8, 6), (7, 5), (7, 7)):
        b.set(x, 1, z, 'chiseled_sandstone')
    flowers = ['orange_tulip', 'red_tulip', 'allium', 'short_grass', 'bush', 'azure_bluet', 'short_grass']
    for x0, x1, z0, z1 in ((2, 5, 3, 5), (9, 12, 3, 5), (2, 5, 7, 9), (9, 12, 7, 9)):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                b.set(x, 0, z, 'grass_block')
                if rng.random() < .6:
                    b.set(x, 1, z, rng.choice(flowers))
    for x in list(range(2, 6)) + list(range(9, 13)):
        b.set(x, 0, 6, 'water', level=0)
        b.set(x, 1, 6, 'air')
    b.set(3, 0, 4, 'grass_block')
    palm(b, 3, 1, 4, height=5, lean='north')
    b.set(11, 1, 8, 'air')
    palm(b, 11, 1, 8, height=4)
    # House across the back.
    plinth(b, 1, 10, 13, 16)
    walls(b, 1, 10, 13, 16, 2, 4, SAND, corner=CUT)
    frieze(b, 1, 10, 13, 16, 4, ('orange_terracotta', 'white_terracotta'))
    flat_roof(b, 1, 10, 13, 16, 5)
    spouts(b, [(0, 13), (14, 13)], 5)
    door(b, 7, 2, 10, 'north', lamp=False, frame='cyan_terracotta')
    awning(b, 6, 8, 8, 9, 4, colors=('red', 'white'), posts=[(6, 8), (8, 8)])
    hang(b, 8, 3, 9)  # beside the door, not in the doorway
    # Living room.
    kitchen_row(b, [(2, 15), (3, 15), (4, 15), (2, 14), (6, 15), (8, 15)], 2, 'north', rng)
    rug(b, 3, 11, 5, 13, 2, 'red', 'white')
    table(b, 4, 2, 12, cloth='orange_carpet')
    chair(b, 3, 2, 12, 'west')
    chair(b, 5, 2, 12, 'east')
    shelf(b, 2, 3, 12, 'east')
    plant(b, 8, 2, 11, rng)
    hang(b, 4, 4, 12)
    # Bedroom.
    wall_run(b, 9, 11, 9, 15, 2, 4, SAND)
    b.door(9, 2, 13, facing='east', wood='acacia')
    b.bed(10, 2, 14, 'south', 'red')
    b.bed(12, 2, 14, 'south', 'orange')
    b.chest(11, 2, 15, 'north', loot=LOOT)
    rug(b, 11, 11, 12, 12, 2, 'orange')
    hang(b, 11, 4, 13)
    b.room('bedroom', (11, 3, 13))
    # Windows.
    lattice_row(b, [(3, 10), (5, 10), (11, 10)], 3, 'north')
    lattice_row(b, [(1, 12), (1, 14)], 3, 'west')
    lattice_row(b, [(13, 12), (13, 14)], 3, 'east')
    lattice_row(b, [(4, 16), (10, 16)], 3, 'south')
    # Street front.
    path_line(b, 7, 0, 1, rng)
    sand_patch(b, [(x, z) for x in range(0, 15) for z in (0, 1) if x != 7], rng, .3)
    plaque(b, 9, 1)
    b.entrance(7)
    b.resident(5, 2, 14)
    b.resident(9, 1, 4, child=True)
    b.natural_ground()
    return b


DESIGNS = {
    'desert/courtyard_house': courtyard_house,
    'desert/dome_house': dome_house,
    'desert/terrace_house': terrace_house,
    'desert/family_house': family_house,
    'desert/adobe_house': adobe_house,
    'desert/tower_house': tower_house,
    'desert/plaster_house': plaster_house,
    'desert/garden_house': garden_house,
}
