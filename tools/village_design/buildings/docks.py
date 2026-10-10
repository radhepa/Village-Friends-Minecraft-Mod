"""Fishing docks: one small jetty per village type, placed by the mod's own code.

When a village has water nearby, the fishing feature places its type's dock at a
suitable shoreline, rotated to point out over the water, and drives the pilings
down to the bed. The docks belong to no pool and no structure: they are listed in
``tools/standalone_templates.json`` and compiled to ``villagefriends:dock/<type>``
(BUILDING_EDITING.md, "Docks").

The contract below is what the Java code relies on; ``check`` enforces it on every
design.

- 5 wide (X 0..4), 12 long (Z 0..11), 4 high. Z 0..1 is the land end on the shore;
  the deck runs from Z 2 to Z 11 out over the water, toward +Z (south).
- The walking surface is Y 0 for the whole length and nothing lies below it.
  Rails, posts, lanterns and props stand on Y 1..3.
- Pilings: one block (a log or a wall) at Y 0 on X 0 and 4 at Z 3, 7 and 11. The
  game extends every log or wall on Y 0 down to the ground, so no other log or wall
  may sit on Y 0.
- The walkway (X 1..3) is solid underfoot with two clear blocks above it all the
  way along; props may stand on X 1 or 3 at Z 2..4 only, and X 2 is always clear.
- The fishing end (X 1..3, Z 11) is open: nothing above the deck there.
- No jigsaws, structure blocks, entities or loot. Job-site blocks (barrels,
  composters and the like) stay off the docks too, so a dock never turns an
  unemployed villager into a fisher or a farmer.
"""
import random

from ..kit import Build, bid, full_cube

SIZE = (5, 4, 12)
LAND = (0, 1)
DECK = range(2, 12)
END = 11
PILINGS = tuple((x, z) for z in (3, 7, 11) for x in (0, 4))
WALK = (1, 2, 3)
SIDES = (0, 4)
PROP_ROWS = range(2, 5)
# Village points of interest (the vanilla job sites and the bell): never on a dock.
POI_BLOCKS = {'barrel', 'composter', 'blast_furnace', 'smoker', 'cartography_table', 'brewing_stand', 'cauldron',
             'water_cauldron', 'fletching_table', 'grindstone', 'lectern', 'loom', 'smithing_table', 'stonecutter',
             'bell'}
FORBIDDEN = {'jigsaw', 'structure_block', 'structure_void', 'cobweb', 'chest', 'trapped_chest'}


# ------------------------------------------------------------------ drawing
def deck(b, boards, edge, beam=None):
    """Y 0 from Z 2 to the end: ``boards`` on the walkway, ``edge`` on X 0 and 4, ``beam`` across the piling rows."""
    beams = {z for _, z in PILINGS}
    for z in DECK:
        for x in range(5):
            if x in SIDES:
                b.set(x, 0, z, edge, waterlogged=False) if bid_of(edge).endswith('_slab') else b.set(x, 0, z, edge)
            else:
                b.set(x, 0, z, beam if beam and z in beams else boards)


def bid_of(spec):
    return spec.split('[')[0].split(':')[-1]


def pilings(b, spec):
    """The six pilings. A wall stays a bare post (no arms), so the column the game drives down is clean."""
    for x, z in PILINGS:
        if spec.endswith('_wall'):
            b.set(x, 0, z, spec, lock=True, up=True, north='none', south='none', east='none', west='none',
                  waterlogged=False)
        else:
            b.set(x, 0, z, spec, axis='y')


def rail(b, x, z0, z1, fence):
    for z in range(z0, z1 + 1):
        b.set(x, 1, z, fence)


def lantern_post(b, x, z, fence, base=None, y=1):
    """A post of ``fence`` (with an optional ``base`` block under it) carrying a lantern on Y 3."""
    if base:
        b.set(x, y, z, base, **({'axis': 'y'} if base.endswith('_log') else {}))
        y += 1
    for yy in range(y, 3):
        b.set(x, yy, z, fence)
    b.set(x, 3, z, 'lantern', hanging=False, waterlogged=False)


def hanging_lantern(b, x, y, z, chain=0):
    for i in range(chain):
        b.set(x, y - i, z, 'chain', axis='y', waterlogged=False)
    b.set(x, y - chain, z, 'lantern', hanging=True, waterlogged=False)


def pot(b, x, y, z, facing='north'):
    b.set(x, y, z, 'decorated_pot', facing=facing, cracked=False, waterlogged=False)


def stool(b, x, z, wood):
    b.set(x, 1, z, f'{wood}_fence')
    b.set(x, 2, z, f'{wood}_pressure_plate', powered=False)


def seat(b, x, z, back, wood):
    """A stair seat; ``back`` is the side of its backrest."""
    b.set(x, 1, z, f'{wood}_stairs', facing=back, half='bottom', shape='straight', waterlogged=False, lock=True)


# ------------------------------------------------------------------ contract
def is_log(state):
    """Members of ``#minecraft:logs``."""
    name = bid(state)
    return name.endswith(('_log', '_wood', '_hyphae')) or name in (
        'crimson_stem', 'warped_stem', 'stripped_crimson_stem', 'stripped_warped_stem')


def is_wall(state):
    """Members of ``#minecraft:walls`` (wall signs, torches and banners are not walls)."""
    return bid(state).endswith('_wall')


def walkable(state):
    name = bid(state)
    return full_cube(state) or name.endswith('_slab') or name == 'dirt_path'


def check(b):
    """The dock contract; every dock design ends with it."""
    assert (b.w, b.h, b.d) == SIZE, f'{b.name}: docks are {SIZE}'
    cells = {pos: state for pos, state in b.grid.items() if state[0] != 'minecraft:air'}
    for (x, y, z), state in cells.items():
        assert state[0].startswith('minecraft:'), f'{b.name}: docks use vanilla blocks only ({x}, {y}, {z})'
        assert bid(state) not in FORBIDDEN, f'{b.name}: no {bid(state)} on a dock ({x}, {y}, {z})'
        assert bid(state) not in POI_BLOCKS, f'{b.name}: {bid(state)} is a village point of interest ({x}, {y}, {z})'
    assert not b.entities, f'{b.name}: docks carry no entities'
    assert not any('LootTable' in n for n in b.nbt.values()), f'{b.name}: docks carry no loot'
    piles = {(x, z): s for (x, y, z), s in cells.items() if y == 0 and (is_log(s) or is_wall(s))}
    assert set(piles) == set(PILINGS), f'{b.name}: logs or walls on Y 0 must be exactly the pilings, found {sorted(piles)}'
    assert len({s[0] for s in piles.values()}) == 1, f'{b.name}: every piling is one block, found {sorted({s[0] for s in piles.values()})}'
    for z in range(SIZE[2]):
        for x in WALK:
            assert walkable(b.get(x, 0, z)), f'{b.name}: walkway at ({x}, 0, {z}) is {b.get(x, 0, z)[0]}'
            if x != 2 and z in PROP_ROWS:
                continue
            for y in (1, 2):
                assert (x, y, z) not in cells, f'{b.name}: walkway needs two clear blocks above ({x}, 0, {z}); ({x}, {y}, {z}) is {cells[(x, y, z)][0]}'
    for x in WALK:
        for y in range(1, SIZE[1]):
            assert (x, y, END) not in cells, f'{b.name}: the fishing end is open; ({x}, {y}, {END}) is {cells[(x, y, END)][0]}'
    return b


def finish(b):
    """Connect fences and walls (``Build.finish`` is safe to repeat), then check the contract on the result."""
    return check(b.finish())


# ------------------------------------------------------------------ the docks
def dock_plains():
    """Plains: an oak jetty off a cobbled landing, spruce cross-beams over the pilings, lanterns at both ends,
    a bench by the landing and a mooring bollard with a coil of chain."""
    b = Build('dock_plains', SIZE)
    # The landing: a worn path onto a cobbled sill.
    for x in range(5):
        b.set(x, 0, 0, 'dirt_path' if x in WALK else 'coarse_dirt')
        b.set(x, 0, 1, 'mossy_cobblestone' if x in SIDES else 'cobblestone')
    deck(b, 'oak_planks', 'oak_slab[type=top]', beam='spruce_planks')
    pilings(b, 'oak_log')
    for x in SIDES:
        lantern_post(b, x, 1, 'oak_fence')
        rail(b, x, 2, 10, 'oak_fence')
        lantern_post(b, x, END, 'oak_fence', base='oak_log')
    # A bench against the east rail by the landing.
    seat(b, 3, 2, 'east', 'oak')
    seat(b, 3, 3, 'east', 'oak')
    # Bait pot and a hay bale by the west rail.
    pot(b, 1, 1, 4, 'east')
    b.set(0, 1, 0, 'hay_block', axis='z')
    # A gap in the east rail for tying up a boat: a bollard wound with chain.
    b.set(4, 1, 9, 'chain', axis='x', waterlogged=False)
    b.set(4, 1, 8, 'oak_log', axis='y')
    b.set(4, 2, 8, 'chain', axis='y', waterlogged=False)
    return finish(b)


def dock_desert():
    """Desert: a jungle-wood landing stage on sandstone piers, a striped awning over the shore end with a
    sandstone bench and a pot in its shade, cut-sandstone posts and lanterns on sandstone columns at the end."""
    b = Build('dock_desert', SIZE)
    for x in range(5):
        b.set(x, 0, 0, 'smooth_sandstone' if x in WALK else 'cut_sandstone')
        b.set(x, 0, 1, 'cut_sandstone' if x in WALK else 'chiseled_sandstone')
    deck(b, 'jungle_planks', 'jungle_slab[type=top]', beam='acacia_planks')
    pilings(b, 'sandstone_wall')
    for x in SIDES:
        rail(b, x, 5, 10, 'jungle_fence')
        b.set(x, 1, 7, 'cut_sandstone')
        b.set(x, 1, END, 'cut_sandstone')
        b.set(x, 2, END, 'sandstone_wall')
        b.set(x, 3, END, 'lantern', hanging=False, waterlogged=False)
        # Awning posts.
        for z in (2, 4):
            b.set(x, 1, z, 'jungle_fence')
            b.set(x, 2, z, 'jungle_fence')
        b.set(x, 1, 3, 'cut_sandstone')
    # The striped awning over the shady end.
    for x in range(5):
        for z in (2, 3, 4):
            b.set(x, 3, z, 'orange_wool' if x % 2 == 0 else 'white_wool')
    hanging_lantern(b, 1, 2, 2)
    seat(b, 3, 3, 'east', 'smooth_sandstone')
    seat(b, 3, 4, 'east', 'smooth_sandstone')
    pot(b, 1, 1, 2, 'east')
    pot(b, 4, 1, 0, 'west')
    b.set(0, 1, 1, 'potted_cactus')
    return finish(b)


def dock_savanna():
    """Savanna: an acacia jetty through a log gateway with a hanging lantern, off a packed-mud landing with
    hay bales and a pot, and a bench just inside the gate."""
    b = Build('dock_savanna', SIZE)
    for x in range(5):
        b.set(x, 0, 0, 'coarse_dirt' if x in SIDES else 'dirt_path')
        b.set(x, 0, 1, 'mud_bricks' if x in SIDES else 'packed_mud')
    deck(b, 'acacia_planks', 'acacia_slab[type=top]', beam='dark_oak_planks')
    pilings(b, 'acacia_log')
    # The gateway at the head of the jetty.
    for x in SIDES:
        for y in (1, 2, 3):
            b.set(x, y, 2, 'acacia_log', axis='y')
    for x in WALK:
        b.set(x, 3, 2, 'stripped_acacia_log', axis='x')
    hanging_lantern(b, 1, 2, 2)
    for x in SIDES:
        rail(b, x, 3, 10, 'acacia_fence')
        b.set(x, 1, 7, 'stripped_acacia_log', axis='y')
        lantern_post(b, x, END, 'acacia_fence', base='stripped_acacia_log')
    seat(b, 3, 3, 'east', 'acacia')
    seat(b, 3, 4, 'east', 'acacia')
    b.set(0, 1, 0, 'hay_block', axis='y')
    b.set(0, 1, 1, 'hay_block', axis='z')
    pot(b, 4, 1, 0, 'west')
    return finish(b)


def dock_snowy():
    """Snowy: a spruce jetty off a stone-brick landing with a brazier and a lantern on stone pillars, heavy log
    posts capped with snow, a cold box of packed ice for the catch, a bundle of sailcloth and lanterns at the end."""
    rng = random.Random(9401)
    b = Build('dock_snowy', SIZE)
    for x in range(5):
        b.set(x, 0, 0, 'cobblestone' if x in SIDES else rng.choice(['gravel', 'dirt_path', 'dirt_path']))
        b.set(x, 0, 1, 'stone_bricks' if x in SIDES else 'cobblestone')
    deck(b, 'spruce_planks', 'spruce_slab[type=top]', beam='dark_oak_planks')
    pilings(b, 'spruce_log')
    for x in SIDES:
        rail(b, x, 2, 10, 'spruce_fence')
        for z in (3, 7):
            b.set(x, 1, z, 'spruce_log', axis='y')
            b.set(x, 2, z, 'spruce_log', axis='y')
            b.set(x, 3, z, 'snow', layers=2)
        lantern_post(b, x, END, 'spruce_fence', base='spruce_log')
    for x in SIDES:
        b.set(x, 1, 0, 'stone_bricks')
    b.set(0, 2, 0, 'campfire', lit=True, signal_fire=False, facing='east', waterlogged=False)
    b.set(4, 2, 0, 'lantern', hanging=False, waterlogged=False)
    # The catch on ice and a coil of rope.
    b.set(1, 1, 3, 'packed_ice')
    b.set(1, 1, 4, 'blue_ice')
    b.set(1, 2, 3, 'snow', layers=1)
    seat(b, 3, 2, 'east', 'spruce')
    b.set(4, 1, 9, 'white_wool')
    b.set(4, 2, 9, 'light_blue_carpet')
    b.set(0, 1, 1, 'snow', layers=1)
    b.set(4, 1, 1, 'snow', layers=2)
    return finish(b)


def dock_taiga():
    """Taiga: a spruce jetty on dark-oak pilings off a mossy landing, dark-oak rails and moss-capped posts,
    lanterns hung from crooked arms at the end, a log stack, a chopping block, a pumpkin and moss on the boards."""
    b = Build('dock_taiga', SIZE)
    for x in range(5):
        b.set(x, 0, 0, 'podzol' if x in SIDES else 'dirt_path')
        b.set(x, 0, 1, 'mossy_cobblestone' if x in SIDES else 'cobblestone')
    deck(b, 'spruce_planks', 'spruce_slab[type=top]', beam='dark_oak_planks')
    pilings(b, 'dark_oak_log')
    for x in SIDES:
        rail(b, x, 2, 10, 'dark_oak_fence')
        for z in (3, 7, END):
            b.set(x, 1, z, 'dark_oak_log', axis='y')
            b.set(x, 2, z, 'dark_oak_log', axis='y')
        for z in (3, 7):
            b.set(x, 3, z, 'moss_carpet')
    # Arms over the rails with hanging lanterns at the end.
    for x in SIDES:
        b.set(x, 3, END, 'dark_oak_fence')
        b.set(x, 3, END - 1, 'dark_oak_fence')
        hanging_lantern(b, x, 2, END - 1)
    # Split logs by the landing, a pumpkin and moss.
    b.set(0, 1, 0, 'spruce_log', axis='z')
    b.set(0, 1, 1, 'spruce_log', axis='z')
    b.set(0, 2, 0, 'spruce_log', axis='z')
    b.set(4, 1, 1, 'stripped_spruce_log', axis='y')
    b.set(4, 2, 1, 'spruce_pressure_plate', powered=False)
    b.set(4, 1, 0, 'pumpkin')
    b.set(1, 1, 3, 'moss_carpet')
    b.set(3, 1, 4, 'moss_carpet')
    stool(b, 3, 2, 'spruce')
    return finish(b)


DESIGNS = {'dock_plains': dock_plains, 'dock_desert': dock_desert, 'dock_savanna': dock_savanna,
           'dock_snowy': dock_snowy, 'dock_taiga': dock_taiga}
