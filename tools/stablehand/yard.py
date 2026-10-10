"""Stables: the Horse Stall, Hay Trough and Saddle Rack (models, blockstates, item models, the few painted
textures, recipes and the loot tables that make them drop themselves), the Horse Papers sprite and the
stablehand's trades.

Built on the workstation model kit (tools/workstations/workstations.py), the way tools/tavern/furniture.py
is: each block is a small program of cuboids, wood comes from vanilla textures, and only the hay, the
saddle leather, the saddle blanket, the stall's bedding and its name plate are painted here. One texel is
always 1/16 block. Designs face north (the front is toward -Z); the blockstates turn them like every other
directional block (north y=0, east 90, south 180, west 270), so FoundationBlock's rotated collision boxes
line up. The trough has five models, one per `hay` level (0 empty to 4 heaped).

Trades: five levels (`trade_set/stablehand/level_N.json`, three offers picked from each), every offer its own
`villager_trade/stablehand/<name>.json`. Horse Papers carry the `villagefriends:horse_papers` component; the
level-4 papers depend on the stablehand's villager type (vanilla's `minecraft:villager/variant` predicate, as
the cartographer's village maps do), so each village sells its own kind of horse.

    python tools/stablehand/stablehand.py --only yard           # write (with every other Stablehand module: no --only)
    python tools/stablehand/stablehand.py --check --only yard   # verify, including vanilla item ids
    python tools/stablehand/stablehand.py --preview --only yard # build/previews/stablehand_yard.png
    python tools/stablehand/yard.py --boxes                     # the collision boxes for StableBlocks.java
    python tools/stablehand/yard.py --check                     # boxes and texture references only

Writing fails when StableBlocks.java's boxes differ from the designs: run --boxes and paste them there.
Never hand-edit the compiled JSON or PNG; change this file and rerun.
"""
import random
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / 'workstations'))
sys.path.insert(0, str(HERE.parent / 'tavern'))
import furniture  # noqa: E402  (the tavern's preview helpers: diced, Scene, preview_textures)
import paint  # noqa: E402
import workstations as ws  # noqa: E402
from breeds import BREEDS  # noqa: E402
from gear import NAMES as GEAR_NAMES  # noqa: E402  (every gear id; lang.py relies on it too)
from kit import ASSETS, DATA, NS, PROJECT, dump, item_files, png_bytes, raster  # noqa: E402

JAVA = PROJECT / 'src/main/java/dev/villagefriends/stable/data/StableBlocks.java'
put, rect, noise = paint.put, paint.rect, paint.noise


class Model(ws.Model):
    """The workstation Model, with our painted textures under block/stablehand/.

    'mc:spruce_planks' is vanilla, 'ws:iron' borrows a workstation texture, anything else is painted below.
    """
    def tex(self, key):
        ref = key.replace(':', '_')
        if key.startswith('mc:'):
            self.textures[ref] = f'minecraft:block/{key[3:]}'
        elif key.startswith('ws:'):
            self.textures[ref] = f'{NS}:block/workstation/{key[3:]}'
        else:
            self.textures[ref] = f'{NS}:block/stablehand/{key}'
        return '#' + ref

    def json(self, particle):
        data = super().json(particle)
        data['textures']['particle'] = self.textures[particle.replace(':', '_')]
        return data


# -- painted textures -------------------------------------------------------------------------------
# Light from the top left, stepped palettes, seeded noise, so every run paints the same pixels.

HAY = ['#F0DB8C', '#E4C76A', '#D8B85A', '#C9A54A', '#B7923C', '#9C7A2E', '#7E6026']


def hay(seed=301):
    """Loose hay seen from above: a golden tangle of strands crossing every which way, darker gaps
    between them. Tiles on every side, so a trough of any length reads as one heap."""
    image = noise(HAY[1:6], [3, 5, 4, 3, 1], seed)
    rand = random.Random(seed)
    for _ in range(26):
        x, y = rand.randrange(16), rand.randrange(16)
        dx, dy = rand.choice([(1, 0), (1, 1), (1, -1), (0, 1), (2, 1), (1, 2)])
        length = rand.randrange(3, 6)
        light = rand.random() < .55
        for i in range(length):
            px, py = (x + dx * i) % 16, (y + dy * i) % 16
            put(image, px, py, HAY[0] if light and i < 2 else HAY[1] if light else HAY[4])
            # A strand casts a one-pixel shadow down and to the right.
            sx, sy = (px + 1) % 16, (py + 1) % 16
            if light and image.getpixel((sx, sy))[:3] != paint.rgb(HAY[0])[:3]:
                put(image, sx, sy, HAY[5])
    for _ in range(9):
        put(image, rand.randrange(16), rand.randrange(16), HAY[6])
    return image


def bedding():
    """The stall floor: straw strewn thin over a darker earth, flatter and paler than a trough's hay."""
    image = noise(['#C9A960', '#BC9A52', '#D4B66C', '#A98A4A', '#8D7344'], [5, 4, 3, 2, 1], 311)
    rand = random.Random(312)
    for _ in range(20):
        x, y = rand.randrange(16), rand.randrange(16)
        dx = rand.choice([1, -1])
        for i in range(rand.randrange(2, 5)):
            put(image, (x + dx * i) % 16, y, '#E2C983' if i == 0 else '#C9A960')
    for _ in range(10):
        put(image, rand.randrange(16), rand.randrange(16), '#6E5634')
    return image


LEATHER = {'k': '#2E1B10', 'D': '#43281A', 'd': '#5A3420', 'm': '#6E4027', 'n': '#7C4A2D', 'h': '#94603A', 'H': '#B07A4C',
           's': '#D9C08A'}


def leather(seed=321):
    """Saddle leather: warm brown with a faint grain, a polished light on the top left."""
    image = noise([LEATHER['m'], LEATHER['n'], LEATHER['d']], [5, 4, 2], seed)
    for y in range(16):
        for x in range(16):
            if (x * 3 + y * 5) % 11 == 0:
                put(image, x, y, LEATHER['h'])
    for x, y in ((2, 2), (3, 2), (2, 3), (9, 4), (10, 4), (5, 9)):
        put(image, x, y, LEATHER['H'])
    return image


def seat():
    """The seat from above (used at u 5..11, v 4..12): a stitched panel with a darker welt round it."""
    image = leather(322)
    for y in range(4, 12):
        put(image, 5, y, LEATHER['D']); put(image, 10, y, LEATHER['D'])
        if y % 2 == 0:
            put(image, 6, y, LEATHER['s']); put(image, 9, y, LEATHER['s'])
    for x in range(7, 9):
        for y in range(5, 11):
            put(image, x, y, LEATHER['h'] if y < 8 else LEATHER['n'])
    put(image, 7, 5, LEATHER['H'])
    return image


def flap():
    """A saddle flap hanging down the horse's side: a tooled border and a stitched edge (the whole 16x16,
    used at u 5..11 on the rack, so the border shows on every edge)."""
    image = leather(323)
    for i in range(16):
        put(image, i, 0, LEATHER['H']); put(image, 0, i, LEATHER['h'])
        put(image, i, 15, LEATHER['k']); put(image, 15, i, LEATHER['D'])
    for x0, x1 in ((5, 10),):
        for y in range(1, 15):
            put(image, x0, y, LEATHER['D']); put(image, x1, y, LEATHER['D'])
            if y % 2:
                put(image, x0 + 1, y, LEATHER['s']); put(image, x1 - 1, y, LEATHER['s'])
    for x in range(5, 11):
        put(image, x, 14, LEATHER['D'])
    return image


BLANKET = {'B': '#26406B', 'b': '#2F4F82', 'l': '#3D6299', 'c': '#E8DDBB', 'C': '#C9BC95', 'r': '#A8392E', 'R': '#7E2A22'}


def blanket():
    """A woven saddle blanket: indigo twill with a cream-and-madder border and a short fringe along the
    bottom rows, which is the edge that shows below the saddle."""
    image = Image.new('RGBA', (16, 16))
    for y in range(16):
        for x in range(16):
            twill = (x + y) % 4
            put(image, x, y, BLANKET['l'] if twill == 0 else BLANKET['b'] if twill < 3 else BLANKET['B'])
    for x in range(16):
        put(image, x, 11, BLANKET['c']); put(image, x, 12, BLANKET['r'] if x % 4 else BLANKET['R'])
        put(image, x, 13, BLANKET['c'] if x % 2 else BLANKET['C'])
        put(image, x, 14, BLANKET['C'] if x % 2 == 0 else (0, 0, 0, 0))
        put(image, x, 15, (0, 0, 0, 0))
    return image


PLATE = {'o': '#5C4430', 'w': '#C9AE7A', 'W': '#DCC392', 'v': '#B0925F', 'i': '#4A3A28', 'n': '#D4A845'}
NAME_PLATE = """
nWWWWWWn........
owiwiiwo........
oviiwiwo........
oooooooo........
................
................
................
................
................
................
................
................
................
................
................
................
"""


def name_plate():
    """The stall's name plate (u 0..8, v 0..4): a pale board with a brass nail in each top corner and the
    horse's name burnt into it. The rest of the texture is the board's plain grain for its edges."""
    image = raster(NAME_PLATE, PLATE)
    for y in range(4, 16):
        for x in range(16):
            put(image, x, y, PLATE['w'] if (x + 2 * y) % 7 else PLATE['v'])
    return image


def textures():
    return {'hay': hay(), 'bedding': bedding(), 'leather': leather(), 'seat': seat(), 'flap': flap(),
            'blanket': blanket(), 'name_plate': name_plate()}


# -- the designs ------------------------------------------------------------------------------------
# Collision boxes are the first argument of each Model and must match StableBlocks.java (--boxes).

POST, RAIL, BOARD = 'mc:stripped_spruce_log', 'mc:stripped_spruce_log', 'mc:spruce_planks'


def horse_stall():
    """The back of a stall: straw bedding on the floor, a plank back board between two posts with a
    rail along the top, a slatted hay rack and a name plate with a horseshoe above it. It stands against
    the stable's back wall and the horse lives in front of it."""
    m = Model('horse_stall', [[0, 0, 0, 16, 2, 16], [0, 2, 12, 16, 16, 16], [3, 6, 9, 13, 10.5, 12]], gui=.55, gui_y=-.5)
    m.box([0, 0, 0], [16, 2, 16], 'bedding', skip=('down',))
    # Loose straw kicked up against the back board.
    m.box([2, 2, 10.5], [6, 2.75, 12], 'bedding', skip=('down', 'south'))
    m.box([9.5, 2, 11], [14, 2.5, 12], 'bedding', skip=('down', 'south'))
    for x in (0, 14):
        m.box([x, 2, 12], [x + 2, 16, 16], {'up': 'mc:stripped_spruce_log_top', '*': POST}, skip=('down',))
    m.box([2, 2, 13], [14, 14, 16], BOARD, skip=('east', 'west', 'down', 'up'))
    m.box([2, 14, 12.5], [14, 16, 16], RAIL, skip=('east', 'west'), face_rot={'up': 90, 'down': 90})
    # The hay rack: a plank bottom, end boards and four slats in front of a heap of hay.
    m.box([3, 6, 9.5], [13, 6.75, 13], BOARD, skip=('south',))
    m.box([3, 6.75, 9.5], [3.75, 10.5, 13], BOARD, skip=('south', 'down'))
    m.box([12.25, 6.75, 9.5], [13, 10.5, 13], BOARD, skip=('south', 'down'))
    m.box([3.75, 6.75, 10.5], [12.25, 9.5, 13], 'hay', only=('up', 'north'))
    m.box([5, 9.5, 11.25], [11, 10.25, 12.5], 'hay', skip=('down', 'south'))
    for x in (4.75, 6.75, 8.75, 10.75):
        m.box([x, 6.75, 9.5], [x + .5, 10, 10], POST, skip=('down', 'up', 'south'))
    m.box([3.75, 10, 9.5], [12.25, 10.5, 10], RAIL, skip=('south', 'down'))
    # The name plate, nailed to the board above the rack.
    m.box([4, 11, 12.5], [12, 15, 13], {'north': 'name_plate', '*': 'mc:birch_planks'}, uv={'north': [0, 0, 8, 4]}, skip=('south',))
    return m


TROUGH_HAY = [0, 1.5, 3, 4.25, 5.25]  # how far the hay rises above the trough floor at each fill level


def hay_trough(level):
    """A long plank trough on four stubby legs, with iron straps at the corners. `level` 0 is empty; 4 is
    heaped above the rim with a few stalks sticking out."""
    m = Model(f'hay_trough_{level}', [[0, 0, 2, 16, 8, 14]], gui=.6)
    for x in (1, 13):
        for z in (3, 11):
            m.box([x, 0, z], [x + 2, 2, z + 2], 'mc:spruce_log', skip=('up',))
    m.box([0, 2, 2], [16, 3, 14], BOARD)
    m.box([0, 3, 2], [16, 8, 3.5], BOARD, skip=('up',))
    m.box([0, 3, 12.5], [16, 8, 14], BOARD, skip=('up',))
    m.box([0, 3, 3.5], [1.5, 8, 12.5], BOARD, skip=('north', 'south', 'up'))
    m.box([14.5, 3, 3.5], [16, 8, 12.5], BOARD, skip=('north', 'south', 'up'))
    # A darker rim along the top edges.
    rim = 'mc:stripped_dark_oak_log'
    m.box([0, 8, 2], [16, 8.5, 3.5], rim, skip=('down',), face_rot={'up': 90})
    m.box([0, 8, 12.5], [16, 8.5, 14], rim, skip=('down',), face_rot={'up': 90})
    m.box([0, 8, 3.5], [1.5, 8.5, 12.5], rim, skip=('down', 'north', 'south'))
    m.box([14.5, 8, 3.5], [16, 8.5, 12.5], rim, skip=('down', 'north', 'south'))
    # Iron straps over the four corners.
    for x0, x1 in ((0, 1.25), (14.75, 16)):
        m.box([x0, 3.5, 1.75], [x1, 7.5, 2], 'ws:iron', skip=('south', 'up', 'down'))
        m.box([x0, 3.5, 14], [x1, 7.5, 14.25], 'ws:iron', skip=('north', 'up', 'down'))
    if level:
        top = 3 + TROUGH_HAY[level]
        m.box([1.5, 3, 3.5], [14.5, top, 12.5], 'hay', only=('up',))
        if level >= 3:
            m.box([3, top, 5], [13, top + 1, 11], 'hay', skip=('down',))
        if level == 4:
            m.box([5, top + 1, 6.5], [11, top + 1.75, 9.5], 'hay', skip=('down',))
            for x, z, angle in ((4, 8, 22.5), (10, 7, -22.5), (7, 9.5, 22.5)):
                m.plane([x, top, z], [x + 3, top + 3, z], 'hay', [2, 0, 5, 3], ('north', 'south'), rot=('y', angle, [x + 1.5, top, z]))
    return m


def saddle_rack():
    """A saddle stand: a post on a cross foot carrying a rail, a striped blanket draped over it and a
    leather saddle on top, its flaps and stirrups hanging down both sides. The pommel faces the front."""
    m = Model('saddle_rack', [[2, 0, 2, 14, 2, 14], [6, 2, 6, 10, 10, 10], [3, 7, 2, 13, 15, 14]], gui=.55, gui_y=-1)
    foot, post = 'mc:stripped_spruce_log', 'mc:spruce_log'
    m.box([2, 0, 6.5], [14, 1.5, 9.5], foot, skip=('down',))
    m.box([6.5, 0, 2], [9.5, 1.5, 6.5], foot, skip=('down', 'south'))
    m.box([6.5, 0, 9.5], [9.5, 1.5, 14], foot, skip=('down', 'north'))
    m.box([6, 1.5, 6], [10, 2.5, 10], foot, skip=('down',))
    m.box([7, 2.5, 7], [9, 10, 9], post, skip=('down', 'up'))
    m.box([6.5, 10, 2], [9.5, 11.5, 14], foot, face_rot={'up': 90, 'down': 90})
    # The blanket over the rail, hanging lower than the saddle on both sides; its striped edge shows below.
    m.box([4, 11.5, 3], [12, 12, 13], 'blanket', uv={'up': [0, 0, 8, 10], 'north': [0, 10, 8, 11], 'south': [0, 10, 8, 11]}, skip=('down', 'east', 'west'))
    side = {'west': [3, 10, 13, 15], 'east': [3, 10, 13, 15], 'north': [0, 10, .5, 15], 'south': [0, 10, .5, 15]}
    m.box([4, 7, 3], [4.5, 12, 13], 'blanket', uv=side, skip=('up',))
    m.box([11.5, 7, 3], [12, 12, 13], 'blanket', uv=side, skip=('up',))
    # The saddle: seat, pommel at the front, cantle at the back, flaps and stirrups.
    m.box([5, 12, 4], [11, 13.5, 12], {'up': 'seat', '*': 'leather'}, uv={'up': [5, 4, 11, 12]}, skip=('down',))
    m.box([6, 12, 3.25], [10, 15, 5], 'leather', skip=('down',))
    m.box([6.75, 15, 3.5], [9.25, 15.75, 4.5], 'leather', skip=('down',))
    m.box([5.5, 12, 11], [10.5, 14.5, 12.75], 'leather', skip=('down',))
    # The flaps hang outside the blanket and stop short of its striped edge.
    for x0, x1 in ((3.5, 4), (12, 12.5)):
        m.box([x0, 8.5, 5], [x1, 12.5, 11], 'flap', uv={'west': [5, 1, 11, 5], 'east': [5, 1, 11, 5]}, skip=('up', 'down'))
    for x0, x1, s0, s1 in ((2.5, 3.5, 3, 3.5), (12.5, 13.5, 12.5, 13)):
        m.box([s0, 4, 7.75], [s1, 7.5, 8.25], 'leather', skip=('up', 'down'))
        m.box([x0, 2.5, 6.75], [x1, 4, 7.25], 'ws:iron')
        m.box([x0, 2.5, 8.75], [x1, 4, 9.25], 'ws:iron')
        m.box([x0, 2.5, 7.25], [x1, 3, 8.75], 'ws:iron', skip=('north', 'south'))
    return m


def designs():
    return {'horse_stall': [horse_stall()], 'hay_trough': [hay_trough(n) for n in range(5)], 'saddle_rack': [saddle_rack()]}


PARTICLES = {'horse_stall': 'bedding', 'hay_trough': 'mc:spruce_planks', 'saddle_rack': 'leather'}
# The trough's inventory icon shows it part full, so it reads as a hay trough and not a box.
ITEM_MODEL = {'horse_stall': 'horse_stall', 'hay_trough': 'hay_trough_3', 'saddle_rack': 'saddle_rack'}
JAVA_FACTORY = {'hay_trough': 'HayTroughBlock'}


# -- Horse Papers ---------------------------------------------------------------------------------
# A sheet of parchment with a horseshoe emblem and lines of ink, its foot sealed with red wax on a blue
# ribbon: a horse's papers, ready to hand over.

PAPERS = """
................
.oooooooooooo...
.oPPPPPPPPPPpo..
.oPhPPhPPPPPpo..
.oPhPPhPiiiPpo..
.oPPhhPPPPPPpo..
.oPPPPPPiiPPpo..
.oPiiiiiiiPPpo..
.oPPPPPPPPPPpo..
.oPiiiiiPPPPpo..
.oPPPPPPPPRRpo..
.oPiiiPPPRrrRo..
.oppppppRrrrxo..
.oooooooRxrxxo..
........bxxxb...
.......bb...bb..
"""
PAPERS_COLORS = {'o': '5A4430', 'P': 'F2E3BF', 'p': 'D9C49A', 'i': '7A6043', 'h': '8A5A30',
                 'R': 'E0566A', 'r': 'C7283C', 'x': '7E1424', 'b': '2F5D8C'}


def papers():
    return raster(PAPERS, PAPERS_COLORS)


# -- recipes ----------------------------------------------------------------------------------------

def shaped(result, pattern, key):
    return {'type': 'minecraft:crafting_shaped', 'category': 'building', 'result': {'id': f'{NS}:{result}', 'count': 1},
            'pattern': pattern, 'key': key}


RECIPES = {
    'horse_stall': shaped('horse_stall', ['F F', 'PHP', 'PPP'], {'F': '#minecraft:wooden_fences', 'P': '#minecraft:planks', 'H': 'minecraft:hay_block'}),
    'hay_trough': shaped('hay_trough', ['PHP', 'PPP'], {'P': '#minecraft:planks', 'H': 'minecraft:hay_block'}),
    'saddle_rack': shaped('saddle_rack', [' L ', 'PPP', 'S S'], {'L': 'minecraft:leather', 'P': '#minecraft:planks', 'S': 'minecraft:stick'}),
}


def loot(name):
    """A broken block drops itself (a trough's hay is lost with it), unless an explosion destroyed it."""
    return {'type': 'minecraft:block', 'pools': [{'rolls': 1, 'entries': [{'type': 'minecraft:item', 'name': f'{NS}:{name}'}],
                                                  'conditions': [{'condition': 'minecraft:survives_explosion'}]}]}


# -- trades -----------------------------------------------------------------------------------------
# Per level: what the stablehand sells (item, emeralds) and buys (item, how many for one emerald). Bare names
# are Stablehand's own items; "papers:<breed>" is Horse Papers for a breed, "donkey" or "mule"; "papers:local"
# is one offer per village type below, of which a stablehand only ever sees their own.

TRADES = {
    1: {'sells': [('grooming_brush', 3), ('bridle', 5)], 'buys': [('minecraft:wheat', 20), ('minecraft:carrot', 18)]},
    2: {'sells': [('papers:rouncey', 10), ('minecraft:saddle', 6), ('hay_trough', 4)], 'buys': [('minecraft:leather', 6), ('minecraft:apple', 10)]},
    3: {'sells': [('saddlebags', 12), ('caparison', 8), ('papers:palfrey', 14), ('papers:donkey', 6)], 'buys': [('minecraft:hay_block', 4)]},
    4: {'sells': [('leather_barding', 10), ('mail_barding', 18), ('horse_whistle', 10), ('papers:local', 18)], 'buys': [('minecraft:golden_carrot', 3)]},
    5: {'sells': [('plate_barding', 28), ('jousting_lance', 16), ('papers:destrier', 32), ('pack_saddle', 8), ('papers:mule', 10)], 'buys': []},
}
AMOUNT = 3
XP = [2, 5, 10, 15, 30]
# The horse each village breeds, by the stablehand's villager type (vanilla's types; plains also covers jungle and swamp).
LOCAL_PAPERS = {'courser': ['plains', 'jungle', 'swamp'], 'desert': ['desert'], 'steppe_pony': ['savanna'], 'fjord': ['taiga'], 'draft': ['snow']}
OWN_ITEMS = {'grooming_brush', 'horse_whistle', 'horse_papers', 'jousting_lance', 'horse_stall', 'hay_trough', 'saddle_rack'}


def uses(name):
    """How often an offer can be taken before the stablehand restocks: a horse is a big purchase."""
    if name.startswith('papers:'):
        return 3
    return 6 if name in set(GEAR_NAMES) or name == 'jousting_lance' else 12


def gives(name):
    if name.startswith('papers:'):
        return {'id': f'{NS}:horse_papers', 'components': {f'{NS}:horse_papers': {'breed': name[len('papers:'):]}}}
    if ':' in name:
        return {'id': name}
    assert name in OWN_ITEMS | set(GEAR_NAMES), f'Unknown Stablehand item in a trade: {name}'
    return {'id': f'{NS}:{name}'}


def sell(name, price, level, variants=None):
    trade = {'wants': {'id': 'minecraft:emerald', 'count': price}, 'gives': gives(name), 'max_uses': uses(name), 'xp': XP[level - 1],
             'reputation_discount': 0.05}
    if variants:
        trade['merchant_predicate'] = {'type': 'minecraft:entity_properties', 'entity': 'this', 'predicate': {
            'minecraft:predicates': {'minecraft:villager/variant': [f'minecraft:{v}' for v in variants]}}}
    return trade


def buy(name, count, level):
    return {'wants': {'id': name, 'count': count}, 'gives': {'id': 'minecraft:emerald'}, 'max_uses': 16, 'xp': XP[level - 1],
            'reputation_discount': 0.05}


def trades():
    """{trade path name: trade} and {level: [trade path names]}."""
    offers, sets = {}, {}
    breeds = {b['id'] for b in BREEDS} | {'donkey', 'mule'}
    for level, row in TRADES.items():
        names = []
        for name, price in row['sells']:
            if name == 'papers:local':
                for breed, variants in LOCAL_PAPERS.items():
                    assert breed in breeds, breed
                    key = f'level_{level}_papers_{breed}'
                    offers[key] = sell(f'papers:{breed}', price, level, variants)
                    names.append(key)
                continue
            if name.startswith('papers:'):
                assert name[len('papers:'):] in breeds, name
            key = f'level_{level}_papers_{name[len("papers:"):]}' if name.startswith('papers:') else f'level_{level}_{name.split(":")[-1]}'
            offers[key] = sell(name, price, level)
            names.append(key)
        for name, count in row['buys']:
            key = f'level_{level}_{name.split(":")[-1]}'
            offers[key] = buy(name, count, level)
            names.append(key)
        sets[level] = names
    return offers, sets


# -- compiling --------------------------------------------------------------------------------------

def blockstate(name, models):
    variants = {}
    for facing, y in ws.ROTATION:
        if name == 'hay_trough':
            for level, model in enumerate(models):
                variants[f'facing={facing},hay={level}'] = {'model': f'{NS}:block/{model.name}', 'y': y}
        else:
            variants[f'facing={facing}'] = {'model': f'{NS}:block/{models[0].name}', 'y': y}
    return {'variants': variants}


def outputs():
    """Every file the yard writes: path -> bytes. Refuses to write while StableBlocks.java's boxes are stale."""
    problems = box_problems()
    if problems:
        raise SystemExit('yard: ' + '\n  '.join(problems))
    files = {}
    for key, image in textures().items():
        files[ASSETS / f'textures/block/stablehand/{key}.png'] = png_bytes(image)
    for name, models in designs().items():
        for model in models:
            files[ASSETS / f'models/block/{model.name}.json'] = dump(model.json(PARTICLES[name]))
        files[ASSETS / f'blockstates/{name}.json'] = dump(blockstate(name, models))
        files[ASSETS / f'models/item/{name}.json'] = dump({'parent': f'{NS}:block/{ITEM_MODEL[name]}'})
        files[ASSETS / f'items/{name}.json'] = dump({'model': {'type': 'minecraft:model', 'model': f'{NS}:item/{name}'}})
    files.update(item_files('horse_papers', papers()))
    for name, recipe in RECIPES.items():
        files[DATA / f'{NS}/recipe/{name}.json'] = dump(recipe)
        files[DATA / f'{NS}/loot_table/blocks/{name}.json'] = dump(loot(name))
    offers, sets = trades()
    for name, trade in offers.items():
        files[DATA / f'{NS}/villager_trade/stablehand/{name}.json'] = dump(trade)
    for level, names in sets.items():
        files[DATA / f'{NS}/trade_set/stablehand/level_{level}.json'] = dump({
            'trades': [f'{NS}:stablehand/{n}' for n in names], 'amount': AMOUNT, 'random_sequence': f'{NS}:trade_set/stablehand/level_{level}'})
    return files


def java_boxes():
    """The collision boxes StableBlocks.java registers, by block name."""
    source = JAVA.read_text(encoding='utf-8')
    found = {}
    for name, body in re.findall(r'add\("(\w+)",\s*new double\[\]\[\]\{(.*?)\},\s*\w+::new\)', source):
        found[name] = [[float(c) for c in row.split(',')] for row in re.findall(r'\{([^{}]*)\}', body)]
    return found


def box_problems():
    java, problems = java_boxes(), []
    for name, models in designs().items():
        if java.get(name) != [[float(c) for c in b] for b in models[0].boxes]:
            problems.append(f'{name}: StableBlocks.java boxes {java.get(name)} differ from the design (run tools/stablehand/yard.py --boxes)')
    return problems


def check():
    """Boxes, coordinates, UVs and texture references (the runner's --check compares the files themselves)."""
    problems = box_problems()
    painted, borrowed = set(textures()), set(paint.textures())
    for name, models in designs().items():
        for model in models:
            for e in model.elements:
                if not all(-16 <= c <= 32 for c in e['from'] + e['to']):
                    problems.append(f'{model.name}: element outside -16..32: {e["from"]} {e["to"]}')
                for face in e['faces'].values():
                    if not all(0 <= c <= 16 for c in face['uv']):
                        problems.append(f'{model.name}: uv outside the texture: {face}')
            for path in model.textures.values():
                key = path.rsplit('/', 1)[1]
                if path.startswith(f'{NS}:block/stablehand/') and key not in painted or path.startswith(f'{NS}:block/workstation/') and key not in borrowed:
                    problems.append(f'{model.name}: missing texture {path}')
    if problems:
        print('yard:\n  ' + '\n  '.join(problems)); sys.exit(1)
    print('yard: boxes, models and textures check out.')


def boxes():
    for name, models in designs().items():
        rows = ','.join('{' + ','.join(f'{c:g}' for c in b) + '}' for b in models[0].boxes)
        print(f'{name.upper()} = add("{name}", new double[][]{{{rows}}}, {JAVA_FACTORY.get(name, "FoundationBlock")}::new);')


# -- preview ----------------------------------------------------------------------------------------

def scene():
    """A stable's back wall: three stalls with a trough between each pair and the saddle rack at the end."""
    d = designs()
    floor = Model('floor', [])
    for x in range(-1, 8):
        for z in range(-2, 1):
            floor.box([16 * x, -1, 16 * z], [16 * x + 16, 0, 16 * z + 16], 'mc:spruce_planks', uv={'up': [0, 0, 16, 16]}, only=('up',))
    s = furniture.Scene().place(floor, 0, 0)
    for x in (0, 2, 4):
        s.place(d['horse_stall'][0], x, 0)
    s.place(d['hay_trough'][4], 1, 0)
    s.place(d['hay_trough'][1], 3, 0)
    s.place(d['saddle_rack'][0], 6, -1, 'west')
    return s.shrink(.4, (56, 8, 0))


def preview():
    models = [m for ms in designs().values() for m in ms]
    found = furniture.preview_textures(models + [Model('floor', []).box([0, 0, 0], [1, 1, 1], 'mc:spruce_planks')])
    found.update({f'{NS}:block/stablehand/{k}': v for k, v in textures().items()})
    dest = PROJECT / 'build/previews'
    dest.mkdir(parents=True, exist_ok=True)
    tile = 300
    sheet = Image.new('RGB', (tile * 4, (tile + 24) * 4), '#7FA7C9')
    draw = ImageDraw.Draw(sheet)
    for n, model in enumerate(models):
        front = ws.render(furniture.diced(model), found)
        back = ws.render(furniture.diced(model), found, view=(-1, .9, 1.15))
        x, y = (n % 2) * tile * 2, (n // 2) * (tile + 24)
        for i, view in enumerate((front, back)):
            small = view.resize((tile, tile))
            sheet.paste(small, (x + i * tile, y + 24), small)
        draw.text((x + 8, y + 6), f'{model.name}  (front from the north-east, back from the south-west)', fill='#10202E')
    icon = papers().resize((128, 128), Image.NEAREST)
    sheet.paste(icon, (tile * 2 + 40, (tile + 24) * 3 + 60), icon)
    draw.text((tile * 2 + 40, (tile + 24) * 3 + 40), 'horse_papers (8x)', fill='#10202E')
    swatches = textures()
    for i, (key, image) in enumerate(swatches.items()):
        big = image.resize((96, 96), Image.NEAREST)
        sheet.paste(big, (tile * 3 + (i % 3) * 100, (tile + 24) * 3 + 40 + (i // 3) * 112), big)
    sheet.save(dest / 'stablehand_yard.png')
    views = [ws.render(scene(), found, scale=22), ws.render(scene(), found, scale=22, view=(-1, .9, 1.15))]
    board = Image.new('RGB', (views[0].width * 2, views[0].height), '#7FA7C9')
    for i, view in enumerate(views):
        board.paste(view, (i * view.width, 0), view)
    ImageDraw.Draw(board).text((10, 8), 'north-east view  |  south-west view  (stalls against the back wall, troughs between, the rack at the end)', fill='#10202E')
    board.save(dest / 'stablehand_yard_scene.png')
    print(dest / 'stablehand_yard.png')
    print(dest / 'stablehand_yard_scene.png')


if __name__ == '__main__':
    if '--boxes' in sys.argv: boxes()
    elif '--check' in sys.argv: check()
    elif '--preview' in sys.argv: preview()
    else: print(__doc__)
