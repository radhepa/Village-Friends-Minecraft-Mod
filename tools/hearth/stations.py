"""Designs, compiles and previews the three Hearth & Harvest cooking stations and their screens.

The stations are built with the workstation model kit (tools/workstations/workstations.py): each model
is a small program of cuboids, one texel is 1/16 block and every texture with character is pixel art
painted here (stepped palettes, a dark outline per material, light from the top left, no antialiasing).
Designs face north; the blockstates turn them by `facing` (north y=0, east 90, south 180, west 270).

    cooking_pot   a black-iron pot that sits on a campfire: empty (dark inside) or filled (stew)
    clay_oven     a domed clay bread oven on a fieldstone plinth: cold or lit
    prep_table    a scrubbed kitchen table with a chopping board, knife, onion and herbs

The screens are 176x166 container panels (like a furnace) on 256x256 sheets, a 120x166 recipe book
panel, and the small sprites the screens draw over them (textures/gui/sprites/hearth/).

    python tools/hearth/stations.py            # write blockstates, models, item models, textures, GUI
    python tools/hearth/stations.py --check    # verify the compiled files match the designs
    python tools/hearth/stations.py --preview  # build/previews/hearth_stations.png and hearth_gui.png
    python tools/hearth/stations.py --boxes    # print the collision boxes in pixels for the Java side

Never hand-edit the compiled JSON or PNG; change the designs here and rerun.
"""
import io
import json
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS / 'workstations'))
sys.path.insert(0, str(TOOLS / 'tavern'))
import paint  # noqa: E402
import workstations as kit  # noqa: E402
import furniture  # noqa: E402

PROJECT, ASSETS, NS = kit.PROJECT, kit.ASSETS, kit.NS
put, rect, rgb = paint.put, paint.rect, paint.rgb


def raster(pattern, palette, base=None):
    """paint.raster, with palette values given with or without the leading '#'."""
    return paint.raster(pattern, {k: v if v.startswith('#') else '#' + v for k, v in palette.items()}, base)


class Model(kit.Model):
    """The workstation Model, with our own textures under block/hearth/.

    'mc:oak_planks' is vanilla, 'ws:iron' borrows a workstation texture, anything else is painted
    below and lands in textures/block/hearth/.
    """
    def tex(self, key):
        ref = key.replace(':', '_')
        if key.startswith('mc:'):
            self.textures[ref] = f'minecraft:block/{key[3:]}'
        elif key.startswith('ws:'):
            self.textures[ref] = f'{NS}:block/workstation/{key[3:]}'
        else:
            self.textures[ref] = f'{NS}:block/hearth/{key}'
        return '#' + ref

    def json(self, particle):
        data = super().json(particle)
        data['textures']['particle'] = self.textures[particle.replace(':', '_')]
        return data

    def ring(self, y0, y1, lo, hi, hole, tex, skip=()):
        """An octagonal collar from lo to hi (x and z) round a square hole, in four boxes.

        The octagon is a centre column (lo+c..hi-c by lo..hi) and two side pieces (lo..lo+c by
        lo+c..hi-c), with c = hole - lo, so cutting the hole out of the column leaves exactly four
        boxes. tex is a dict: 'out' for the outside, 'in' for the inside walls, 'up' and 'down'.
        """
        a, b = hole, 16 - hole
        out, inner, up, down = tex['out'], tex['in'], tex['up'], tex.get('down', tex['out'])
        both = {'up': up, 'down': down}
        self.box([a, y0, lo], [b, y1, a], {'south': inner, **both, '*': out}, skip=skip)    # north band
        self.box([a, y0, b], [b, y1, hi], {'north': inner, **both, '*': out}, skip=skip)    # south band
        self.box([lo, y0, a], [a, y1, b], {'east': inner, **both, '*': out}, skip=skip)     # west side
        self.box([b, y0, a], [hi, y1, b], {'west': inner, **both, '*': out}, skip=skip)     # east side
        return self


# -- block textures ---------------------------------------------------------------------------------
# A texture painted for a model part whose faces use vanilla's default UVs is laid out by height:
# texture row v shows the part at y = 16 - v, so bands of colour line up with the model's rims.

IRON = {'k': '1A191D', 'd': '29282D', 'm': '36353B', 'n': '434148', 'h': '57555D', 'H': '6F6C76', 'w': '8E8B97'}
POT_SIDE = """
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
HHHHHwHHHHHHHwHH
ddddddkddddddddd
hhhhhhhhhhHhhhhh
nnnnnnhnnnnnnnnn
nnnnnnnnnnnnnhnn
mmmmmmmmmmmmmmmm
mmmdmmmmmmdmmmmm
dddddddmdddddddd
kkdkkkkkkdkkkkkk
kkkkkkkkkkkkkkkk
"""
# Laid out by height: row 6 the lip, 7 the neck in shadow, 8 the lit shoulder, 9-11 the belly
# darkening down, 12 the lower belly, 13 the bottom, 14-15 the sooty base and feet.
POT_INNER = """
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
hhhhhhhhhhhhhhhh
mmmmdmmmmmmmmdmm
dddddddddddddddd
ddkdddddddkddddd
kkkkkkdkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
"""
POT_FLOOR = """
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkdkkkkkk
kkkkkdkkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkdkkkk
kkkkkkdkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
kkkkkkkkkkkkkkkk
"""
POT_RIM = """
HHHHHHHHHHHHHHHH
HHHwHHHHHHHHHwHH
HHHHHHHHHHHHHHHH
HHHHHHHHwHHHHHHH
HHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHH
HHwHHHHHHHHHHHHH
HHHHHHHHHHHHHwHH
HHHHHHHHHHHHHHHH
HHHHHHHHHHHHHHHH
"""
POT_RING = """
................
................
................
.....wHh........
....w...h.......
....H...n.......
....h...m.......
.....hnm........
................
................
................
................
................
................
................
................
"""
STEW = {'o': '4A2812', 'S': '7E4523', 's': '925530', 'L': 'B07448', 'p': 'C9B070', 'P': 'E8D59A',
        'c': 'C8632A', 'C': 'EE9145', 'g': '6E9A40'}
POT_STEW = """
SSSSSSSSSSSSSSSS
SSSSSSSSSSSSSSSS
SSSSSSSSSSSSSSSS
SSSSSSSSSSSSSSSS
SSSSooooooooSSSS
SSSSoSSsSSsSSSSS
SSSSoSPpsScSSSSS
SSSSosLsSsCcSSSS
SSSSoSsSgsSsSSSS
SSSSoScSsSPpSSSS
SSSSosCssLsSSSSS
SSSSoSsgSsSsSSSS
SSSSSSSSSSSSSSSS
SSSSSSSSSSSSSSSS
SSSSSSSSSSSSSSSS
SSSSSSSSSSSSSSSS
"""
LADLE = """
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
DddDddDddDddDddD
"""
WOOD = {'D': '8A6038', 'd': 'B08452'}


# The clay oven. Masonry is generated (stones and bricks lit on their top-left edges); the arch, the
# mouth and the flue are authored. The dome's texture is banded by height so each tier of the dome
# is lit on top and shaded underneath, which makes the stepped dome read as round.

STONE = {'o': '34302C', 'd': '5C5751', 'm': '726D66', 'n': '87827A', 'h': '9D978C', 'H': 'B4AEA2'}
BRICK = {'o': '2E1A12', 'g': '8C7B6A', 'q': '6A2C1C', 'r': '843C26', 'R': 'A24E33', 'v': 'DE9A66', 'V': 'BC7448',
         'k': '1E1410', 'K': '2C1D16'}
CLAY = {'o': '6A3C24', 'd': '93552F', 'm': 'A9673B', 'n': 'BB7846', 'h': 'CC8C55', 'H': 'DDA46C'}
FIRE = {'k': '4A1C0E', 'o': 'B4461A', 'e': 'DD5A1C', 'f': 'FF8A1E', 'F': 'FFC23A', 'w': 'FFF0A0', 'a': '6E6660',
        'A': '8A827A', 'd': '2E1E16', 'm': '3E2A1E', 'K': '1E1410'}


def masonry(courses, palette, chip=5):
    """Stones (or bricks) in courses: each course is (first row, last row, [columns where a stone
    starts]); a joint column sits just before each start and wraps round, so the texture tiles.
    Each stone is lit along its top and left edges and shaded along its bottom and right."""
    image = paint.blank()
    c = {k: rgb('#' + v) for k, v in palette.items()}
    for y in range(16):
        for x in range(16):
            image.putpixel((x, y), c['o'])
    for y0, y1, starts in courses:
        for i, x0 in enumerate(starts):
            end = starts[(i + 1) % len(starts)] + (16 if i + 1 == len(starts) else 0) - 1  # the joint column
            for y in range(y0, y1 + 1):
                for xx in range(x0, end):
                    x = xx % 16
                    top, bottom, left, right = y == y0, y == y1, xx == x0, xx == end - 1
                    if (top and right) or (bottom and left):
                        k = 'm'
                    elif bottom and right:
                        k = 'o' if y1 > y0 + 1 else 'd'
                    elif top:
                        k = 'H' if not left else 'h'
                    elif left:
                        k = 'h'
                    elif bottom or right:
                        k = 'd'
                    else:
                        k = 'm' if (x * 7 + y * 3) % chip == 0 else 'n'
                    image.putpixel((x, y), c[k])
    return image


def oven_stone():
    """Fieldstone for the plinth; the course in rows 11-15 is the one the plinth shows."""
    return masonry([(0, 3, [1, 7, 12]), (5, 9, [4, 9, 14]), (11, 15, [0, 6, 11])], STONE)


def oven_stone_top():
    """Big flagstones on top of the plinth (the hearth shelf in front of the mouth)."""
    return masonry([(0, 6, [0, 9]), (8, 15, [4, 12])], dict(STONE, n='938D84', m='857F77'), chip=7)


OVEN_NICHE = """
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
...KKKKKKKKKK...
...KbLbKbLbKK...
...KLlLbLlLbK...
...bLlbbLlbLb...
"""
NICHE = {'K': '1A120D', 'b': '4A3020', 'L': 'C29A5E', 'l': '9C7442'}


def oven_stone_front():
    """The plinth's front: fieldstone with a niche of firewood under the oven mouth (rows 12-15)."""
    return raster(OVEN_NICHE, NICHE, oven_stone())


def oven_brick():
    """Small fired bricks (3 wide, 1 tall) for the chimney and the sides of the arch."""
    return masonry([(y, y, [0, 4, 8, 12] if (y // 2) % 2 == 0 else [2, 6, 10, 14]) for y in range(0, 16, 2)],
                   {'o': BRICK['g'], 'd': BRICK['q'], 'm': BRICK['r'], 'n': BRICK['r'], 'h': BRICK['R'], 'H': BRICK['R']})


OVEN_CLAY = """
nnnnnnnnnnnnnnnn
hhHhhhhhhhhHhhhh
HHHHhHHHHHHHHhHH
mmmdmmmmmdmmmmmm
hhhhHhhhhhhhhHhh
nnnnnnnmnnnnnnnn
dddmddddddddmddd
hhHhhhhhhHhhhhhh
nnnnnnnnnnnnnnnn
nnmnnnnonnnnnmnn
dmdddddmdddddddd
mmmmmmmmmmmmmmmm
mmmmmmmmmmmmmmmm
mmmmmmmmmmmmmmmm
mmmmmmmmmmmmmmmm
mmmmmmmmmmmmmmmm
"""
# Banded by height: row 1 the cap (y 14-15), 2-3 the third tier, 4-6 the second, 7-10 the first.
OVEN_CLAY_TOP = """
hhhhhhhhhhhhhhhh
hhhhhHhhhhhhhhhh
hhhhhhhhhhhhnhhh
hhnhhhhhhhhhhhhh
hhhhhhhhhhHhhhhh
hhhhhhhhhhhhhhhh
hHhhhhhnhhhhhhhh
hhhhhhhhhhhhhhHh
hhhhhhhhhhhhhhhh
hhhhhhhhhhhhhhhh
hhhhHhhhhhhhnhhh
hhhhhhhhhhhhhhhh
hhhhhhhhhhHhhhhh
hhnhhhhhhhhhhhhh
hhhhhhhhhhhhhhhh
hhhhhhHhhhhhhhhh
"""
OVEN_FRONT = """
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrRRRgRRRRgRRrr
rrrqrgVvvVgrqrrr
rrrrgVv..vVgrrrr
rrrrVv....vVrrrr
rrrqv......vqrrr
rrrrV......Vrrrr
rrrqv......vqrrr
rrrrV......Vrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
"""
# The facade covers x 3-13, y 5-13 (columns 3-12, rows 3-10); the arch is open (transparent) in
# columns 5-10 from row 5 down, with a voussoir ring of lighter brick round it.
OVEN_MOUTH = """
................
................
................
................
................
KKKKKKKKKKKKKKKK
KKKKKdKKKdKKKKKK
KKKKKKKdKKKKKKKK
KKKKKKKKKKdKKKKK
KKKKKmKdKmKKKKKK
KKKKKaAaaAaKKKKK
................
................
................
................
................
"""
OVEN_MOUTH_LIT = """
................
................
................
................
................
kkkkkokkokkkkkkk
kkkkkekoekkkkkkk
kkkkkofFfeokkkkk
kkkkkFfFwFfkkkkk
kkkkkFwwFwFkkkkk
kkkkkeFFfFekkkkk
................
................
................
................
................
"""
OVEN_SOOT = """
KKKKKKKKKKKKKKKK
KdKKKKKKdKKKKKKK
KKKKdKKKKKKKdKKK
KKKKKKKKKKKKKKKK
KKdKKKKKKdKKKKKK
KKKKKKdKKKKKKKKK
KKKKKKKKKKKKdKKK
KdKKKKKKKKKKKKKK
KKKKKdKKKKdKKKKK
KKKKKKKKKKKKKKKK
KKKdKKKKKKKKKdKK
KKKKKKKKdKKKKKKK
KKKKKKKKKKKKKKKK
KdKKKKKKKKKKKKKK
KKKKKKdKKKKdKKKK
KKKKKKKKKKKKKKKK
"""
OVEN_GLOW = """
kkkkkkkkkkkkkkkk
kokkkkkkokkkkkkk
kkkkokkkkkkkokkk
kkkkkkkkkkkkkkkk
kkokkkkkkokkkkkk
kkkkkkokkkkkkkkk
kkkkkkkkkkkkokkk
kokkkkkkkkkkkkkk
kkkkkokkkkokkkkk
kkkkkkkkkkkkkkkk
kkkokkkkkkkkkokk
kkkkkkkkokkkkkkk
kkkkkkkkkkkkkkkk
kokkkkkkkkkkkkkk
kkkkkkokkkkokkkk
kkkkkkkkkkkkkkkk
"""
OVEN_FLUE = """
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrRRRqrrrrrr
rrrrrrR..qrrrrrr
rrrrrrR..qrrrrrr
rrrrrrqqqqrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
rrrrrrrrrrrrrrrr
"""
# The flue's top (x 6-10, z 3-7): a ring of brick round an open hole; the soot (or the glow of the
# fire) shows half a texel down inside it.


# The prep table. A scrubbed (pale, worn) oak top over vanilla oak legs; the small props on it share
# one atlas, prep_props, with explicit UVs (see prep_table() for which region is which).

SCRUB = {'o': '8A6E48', 'd': 'AB8D60', 'm': 'C2A676', 'n': 'D0B686', 'h': 'DDC597', 'H': 'EAD6AA'}
PREP_TOP = """
HhhhhhhHhhhhhhhh
nnnnmmnnnnnnnnnn
nnnnnnnnnnmmmnnn
dddddddddodddddd
hhhhhhhhhhhhhhhH
nnmmnnnndnnnnnnn
nnnnnnndnnnnmmnn
ddoddddddddddddd
hhhhHhhhhhhhhhhh
nnnnnnnnnnnnnnnn
nmmmnnnnnndnnnnn
ddddddddddddoddd
hhhhhhhhhhhHhhhh
nnnndnnnnnnnnmmn
nnndnnnnnnnnnnnn
dddddddodddddddd
"""
PREP_EDGE = """
HHHHHHHHHHHHHHHH
HHHoHHHHHHHoHHHH
dddodddddddodddd
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
"""
# The top's 2-texel edge shows rows 1-2: a lit arris over a darker face, with plank joints.
OAK = {'o': '4E3A20', 'd': '7E6237', 'm': '9F844D', 'n': 'AF8F55', 'h': 'B8945F', 'b': 'D9AE4E', 'B': 'F1D27A'}
PREP_APRON = """
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
hhhhhoooooohhhhh
nnmnnohbBhodnnmn
dddddooooooddddd
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
nnnnnnnnnnnnnnnn
"""
# The apron's front (x 2-14, y 10-13: columns 2-13, rows 3-5) with a drawer and its brass pull.
BOARD = {'o': '6B4526', 'd': '9A6A3A', 'm': 'B07A48', 'n': 'C28C56', 'h': 'D49F66', 'w': 'F4EEDC', 'y': 'E6DDB0',
         'g': '6E9A40'}
PREP_BOARD = """
dddddddddddddddd
dddddddddddddddd
ddhhhhhhhhdddddd
ddhnnnwnwddddddd
ddhnnnnwnddddddd
ddhnnnwnnddddddd
ddhnmnnnnddddddd
ddhnnnnmnddddddd
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
"""
# The board's top is columns 2-9, rows 2-8 (lit edge top-left, shadow edge bottom-right) with the
# dice of the halved onion beside it; row 0 is its edge.
PROPS = {'O': '4E2A12', 'a': '944A20', 'b': 'B8642E', 'c': 'D08A42', 'C': 'E8B262', 'w': 'F4EEDC', 'y': 'E8DFA8',
         's': 'A8ADB6', 'S': 'E8ECF2', 'z': '6E727A', 'k': '3E2616', 'K': '6B4428', 'B': 'D9AE4E',
         'j': '8E5030', 'J': 'B06A40', 'i': '6A3A22', 'x': '24160E', 'G': '4E7A5E',
         'u': 'BFAA80', 'U': 'DCCBA2', 't': '9C8862', 'L': '4A6A9A', 'l': '3A5480'}
PREP_PROPS = """
CcCCcCcCCcc.....
cbcbbcbCac......
ba.....cbb......
yyybcb..........
ywy.............
yyy.............
sSSSz...........
ssssz...........
kBk.............
kkkk............
JJjJJj..........
jjiJxj..........
...jjiUUUtUUUu..
......LLLlUKut..
......UuutUuut..
......uuttuttt..
"""
# Regions (columns x rows): the onion's core side 0-1 x 0-2, its belly side 2-4 x 0, the core's top
# 5-6 x 0-1, the belly's top 7-9 x 0-2 and the dry neck 10 x 0; the halved onion's cut face 0-2 x 3-5
# and its skin 3-5 x 3; the knife's blade 6 (tip first) and edge 7, its handle 8 and sides 9; the
# jug's side 0-2 x 10-11 and its mouth 3-5 x 10-12; the crock's side 6-9 x 12-15 and lid 10-13 x 12-15.
HERBS = {'g': '4E7A30', 'G': '7AA648', 'H': '9CC460', 'k': '3A5424', 'f': 'A07AC8'}
PREP_HERBS = """
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
.....HgfGg......
.....GgGHgG.....
......gkGg......
.......kk.......
"""
# A sprig bunch (columns 5-10, rows 12-15) for two crossed cards standing in the jug.


def block_textures():
    """Every texture the stations paint, by name (written to textures/block/hearth/<name>.png)."""
    return {
        'pot_side': raster(POT_SIDE, IRON), 'pot_inner': raster(POT_INNER, IRON), 'pot_floor': raster(POT_FLOOR, IRON),
        'pot_rim': raster(POT_RIM, IRON), 'pot_ring': raster(POT_RING, IRON), 'pot_stew': raster(POT_STEW, STEW),
        'ladle': raster(LADLE, WOOD),
        'oven_stone': oven_stone(), 'oven_stone_top': oven_stone_top(), 'oven_stone_front': oven_stone_front(),
        'oven_brick': oven_brick(), 'oven_clay': raster(OVEN_CLAY, CLAY), 'oven_clay_top': raster(OVEN_CLAY_TOP, CLAY),
        'oven_front': raster(OVEN_FRONT, BRICK), 'oven_mouth': raster(OVEN_MOUTH, FIRE), 'oven_mouth_lit': raster(OVEN_MOUTH_LIT, FIRE),
        'oven_soot': raster(OVEN_SOOT, FIRE), 'oven_glow': raster(OVEN_GLOW, FIRE), 'oven_flue': raster(OVEN_FLUE, BRICK),
        'prep_top': raster(PREP_TOP, SCRUB), 'prep_edge': raster(PREP_EDGE, SCRUB), 'prep_apron': raster(PREP_APRON, OAK),
        'prep_board': raster(PREP_BOARD, BOARD), 'prep_props': raster(PREP_PROPS, PROPS), 'prep_herbs': raster(PREP_HERBS, HERBS),
    }


# -- the designs ------------------------------------------------------------------------------------
# Collision boxes are the first argument of each Model (pixels), printed by --boxes for the Java side.

POT = {'out': 'pot_side', 'in': 'pot_inner', 'up': 'pot_rim', 'down': 'pot_floor'}


def cooking_pot(filled):
    """A black-iron cooking pot: three stubby feet, a round belly, a lit shoulder, a narrow neck, a
    flared lip and two rings hanging from lugs at the sides. It is the block above a campfire, so the
    flames lick its bottom. Filled, a stew sits three texels below the lip with a ladle in it."""
    m = Model('cooking_pot_filled' if filled else 'cooking_pot', [[2, 0, 2, 14, 10, 14]], gui=.75, gui_y=2)
    for x, z in ((4.5, 4.5), (10, 4.5), (7.25, 10)):
        m.box([x, 0, z], [x + 1.5, 1.5, z + 1.5], 'pot_side', skip=('up',))
    m.box([5, 1, 5], [11, 2, 11], {'down': 'pot_floor', '*': 'pot_side'}, skip=('up',))
    m.box([3.5, 2, 3.5], [12.5, 3, 12.5], {'up': 'pot_floor', 'down': 'pot_floor', '*': 'pot_side'})  # its top is the floor
    m.ring(3, 4, 2.5, 13.5, 4, POT)   # the lower belly
    m.ring(4, 7, 2, 14, 4, POT)       # the belly
    m.ring(7, 8, 2.5, 13.5, 4, POT)   # the shoulder
    m.ring(8, 9, 3.5, 12.5, 4, POT)   # the neck
    m.ring(9, 10, 3, 13, 4, POT)      # the lip
    for x0, x1, face, side in ((1.25, 3, 'west', 1.5), (13, 14.75, 'east', 14.5)):
        m.box([x0, 7, 7], [x1, 8, 9], 'pot_rim', skip=(('east',) if face == 'west' else ('west',)))
        m.plane([side, 3, 5.5], [side, 8, 10.5], 'pot_ring', [4, 3, 9, 8], (face,))
    if filled:
        m.box([4, 6, 4], [12, 7, 12], 'pot_stew', only=('up',))
        m.box([10, 5, 9], [10.75, 12.5, 9.75], 'ladle', rot=('x', 22.5, [10.375, 7, 9.375]), skip=('down',))
    return m


def octagon(m, y0, y1, x0, x1, z0, z1, c, tex):
    """A solid octagonal tier: a centre column and two side pieces with the corners cut by c."""
    m.box([x0 + c, y0, z0], [x1 - c, y1, z1], tex)
    m.box([x0, y0, z0 + c], [x0 + c, y1, z1 - c], tex, skip=('east',))
    m.box([x1 - c, y0, z0 + c], [x1, y1, z1 - c], tex, skip=('west',))
    return m


def clay_oven(lit):
    """A domed bread oven: a fieldstone plinth with a niche of firewood, a clay dome in four tiers, a
    brick arch facade with the mouth set back in it, and a brick flue above the arch. Lit, the fire
    glows in the mouth and on the walls of the arch."""
    m = Model('clay_oven_lit' if lit else 'clay_oven', [[0, 0, 0, 16, 16, 16]], gui=.625)
    m.box([0, 0, 0], [16, 5, 16], {'north': 'oven_stone_front', 'up': 'oven_stone_top', '*': 'oven_stone'})
    dome = {'up': 'oven_clay_top', 'down': 'oven_clay_top', '*': 'oven_clay'}
    octagon(m, 5, 9, 1, 15, 3, 15, 2, dome)
    octagon(m, 9, 12, 2, 14, 4, 14, 2, dome)
    octagon(m, 12, 14, 3.5, 12.5, 5, 13, 1.5, dome)
    m.box([5.5, 14, 6.5], [10.5, 15, 11.5], dome, skip=('down',))
    # The arch facade, its mouth set back 1.4 texels, and the walls and soffit of the opening.
    m.box([3, 5, 1.5], [13, 13, 3], {'north': 'oven_front', '*': 'oven_brick'}, skip=('south', 'down'))
    inside = 'oven_glow' if lit else 'oven_soot'
    m.box([5, 5, 2.9], [11, 11, 3], 'oven_mouth_lit' if lit else 'oven_mouth', only=('north',), light=15 if lit else 0)
    m.plane([5, 5, 1.5], [5, 11, 2.9], inside, [0, 5, 1.4, 11], ('east',), light=10 if lit else 0)
    m.plane([11, 5, 1.5], [11, 11, 2.9], inside, [0, 5, 1.4, 11], ('west',), light=10 if lit else 0)
    m.plane([5, 11, 1.5], [11, 11, 2.9], inside, [5, 0, 11, 1.4], ('down',), light=10 if lit else 0)
    # The flue, open at the top, with the soot (or the glow) half a texel down inside it.
    m.box([6, 12, 3], [10, 16, 7], {'up': 'oven_flue', '*': 'oven_brick'}, skip=('down',))
    m.box([6, 14.5, 3], [10, 15.5, 7], inside, only=('up',), light=10 if lit else 0)
    return m


SIDES = ('north', 'south', 'east', 'west')


def prep_table():
    """A scrubbed kitchen table: four oak legs, a drawer in the apron, a shelf with a flour sack and a
    crock under it, and on top a chopping board with a diced onion, a knife, a whole onion and a jug
    of herbs. The table is 15 texels tall; the props stand up to y 19."""
    m = Model('prep_table', [[0, 0, 0, 16, 15, 16]], gui=.58, gui_y=-1)
    leg, plank = 'mc:stripped_oak_log', 'mc:oak_planks'
    m.box([0, 13, 0], [16, 15, 16], {'up': 'prep_top', 'down': plank, '*': 'prep_edge'})
    for x in (1, 13):
        for z in (1, 13):
            m.box([x, 0, z], [x + 2, 13, z + 2], {'down': 'mc:stripped_oak_log_top', '*': leg}, skip=('up',))
    m.box([2, 10, 2], [14, 13, 14], {'north': 'prep_apron', '*': plank}, skip=('up',))
    m.box([1, 3, 1], [15, 4, 15], plank)
    # Under the table: a tied flour sack and a lidded crock with a blue band.
    m.box([3, 4, 6], [7, 9, 11], 'ws:burlap_plain', skip=('down',))
    m.box([4, 9, 7.5], [6, 10, 9.5], 'ws:rope', skip=('down',))
    m.box([9, 4, 6], [13, 7.5, 10], 'prep_props', uv={'up': [10, 12, 14, 16], **{f: [6, 12, 10, 15.5] for f in SIDES}}, skip=('down',))
    # On top: the chopping board, a halved onion and its dice, and the knife.
    m.box([2, 15, 2], [10, 16, 9], {'up': 'prep_board', '*': 'prep_board'},
          uv={'north': [6, 0, 14, 1], 'south': [2, 0, 10, 1], 'east': [7, 0, 14, 1], 'west': [2, 0, 9, 1]}, skip=('down',))
    m.box([3, 16, 3], [6, 17, 6], 'prep_props', uv={'up': [0, 3, 3, 6], **{f: [3, 3, 6, 4] for f in SIDES}}, skip=('down',))
    turn = ('y', 22.5, [7, 16, 7.25])
    m.box([4, 16, 6.75], [9, 16.25, 7.75], 'prep_props', uv={'up': [0, 6, 5, 7], 'north': [0, 7, 5, 7.25], 'south': [0, 7, 5, 7.25],
          'east': [4, 7, 5, 7.25], 'west': [0, 7, 1, 7.25]}, rot=turn, skip=('down',))
    m.box([9, 16, 6.75], [12, 16.75, 7.75], 'prep_props', uv={'up': [0, 8, 3, 9], 'north': [0, 9, 3, 9.75], 'south': [0, 9, 3, 9.75],
          'east': [3, 9, 4, 9.75], 'west': [0, 9, 1, 9.75]}, rot=turn, skip=('down',))
    # A whole onion: a round belly, a narrower core and its dry neck.
    m.box([11.5, 15, 3.5], [13.5, 17.5, 5.5], 'prep_props', uv={'up': [5, 0, 7, 2], **{f: [0, 0, 2, 2.5] for f in SIDES}}, skip=('down',))
    m.box([11, 15.5, 3], [14, 16.5, 6], 'prep_props', uv={'up': [7, 0, 10, 3], 'down': [7, 0, 10, 3], **{f: [2, 0, 5, 1] for f in SIDES}})
    m.box([12, 17.5, 4], [13, 18.25, 5], 'prep_props', uv={f: [10, 0, 11, .75] for f in (*SIDES, 'up')}, skip=('down',))
    # A little jug of herbs at the back.
    m.box([11, 15, 10], [14, 17, 13], 'prep_props', uv={'up': [3, 10, 6, 13], **{f: [0, 10, 3, 12] for f in SIDES}}, skip=('down',))
    for angle in (45, -45):
        m.plane([9.5, 15, 11.5], [15.5, 19, 11.5], 'prep_herbs', [5, 12, 11, 16], ('north', 'south'), rot=('y', angle, [12.5, 15, 11.5]))
    return m


def designs():
    return {
        'cooking_pot': [cooking_pot(False), cooking_pot(True)],
        'clay_oven': [clay_oven(False), clay_oven(True)],
        'prep_table': [prep_table()],
    }


PARTICLES = {'cooking_pot': 'pot_side', 'clay_oven': 'oven_clay', 'prep_table': 'prep_top'}
STATES = {'cooking_pot': 'filled', 'clay_oven': 'lit', 'prep_table': None}


def blockstate(name, models):
    """facing turns the model; filled/lit picks the second model. Other properties (the pot's lit) are
    left out of the variant keys, so every value of them matches."""
    variants = {}
    state = STATES[name]
    for facing, y in kit.ROTATION:
        if state:
            for on in (False, True):
                variants[f'facing={facing},{state}={str(on).lower()}'] = {'model': f'{NS}:block/{models[on].name}', 'y': y}
        else:
            variants[f'facing={facing}'] = {'model': f'{NS}:block/{models[0].name}', 'y': y}
    return {'variants': variants}


# -- the screens ------------------------------------------------------------------------------------
# Container panels are 176x166 at the top-left of a 256x256 sheet, laid out like vanilla's furnace:
# each item area (16x16) sits in an 18x18 recessed slot frame one texel up-left of it. The screens
# place slots, sprites and text at these coordinates, so they must not move.

GRID = [(x, y) for y in (17, 35) for x in (30, 48, 66)]
VESSEL = (48, 55)          # the pot's bowl slot and the oven's fuel slot
WELL = (31, 56)            # 14x14: the pot's fire well, the oven's flame
ARROW = (89, 34)           # 24x17
RESULT = (124, 35)
RESULT_FRAME = (119, 30)   # 26x26, five texels round the result slot like the furnace's
BOOK_BUTTON = (5, 34)      # 20x18, drawn by the screen over plain parchment
INVENTORY = [(8 + 18 * col, 84 + 18 * row) for row in range(3) for col in range(9)] + [(8 + 18 * col, 142) for col in range(9)]
PANEL, BOOK_PANEL = (176, 166), (120, 166)

PAPER = {'p': 'E3D3AE', 'q': 'D9C7A1', 'r': 'C6B086', 's': 'A28C64', 'l': 'F5ECD3', 'i': '6E5A3E'}
SLOT = {'d': '4A3826', 'f': '8F7E62', 'l': 'FBF3DD'}


def color(value):
    return value if isinstance(value, tuple) else rgb(value if value.startswith('#') else '#' + value)


def area(image, x0, y0, x1, y1, value):
    """Fills x0..x1, y0..y1 (inclusive)."""
    if x1 >= x0 and y1 >= y0:
        ImageDraw.Draw(image).rectangle([x0, y0, x1, y1], fill=color(value))


def recess(image, x, y, w, h, dark, fill, light):
    """A vanilla recessed frame: dark top and left edges, light bottom and right edges, the two odd
    corners in the fill colour."""
    area(image, x, y, x + w - 1, y + h - 1, fill)
    area(image, x, y, x + w - 2, y, dark); area(image, x, y, x, y + h - 2, dark)
    area(image, x + 1, y + h - 1, x + w - 1, y + h - 1, light); area(image, x + w - 1, y + 1, x + w - 1, y + h - 1, light)


def slot(image, x, y, palette=SLOT):
    """The 18x18 frame round the 16x16 item area at (x, y)."""
    recess(image, x - 1, y - 1, 18, 18, palette['d'], palette['f'], palette['l'])


def stamp(image, x, y, pattern, palette):
    """Paints an ASCII pattern at (x, y); '.' leaves what is there."""
    for j, row in enumerate(pattern.strip('\n').splitlines()):
        for i, ch in enumerate(row):
            if ch != '.':
                image.putpixel((x + i, y + j), color(palette[ch]))
    return image


def panel(w, h, band, size=256):
    """A rounded panel: a one-texel outline, a three-texel band of the station's material, a
    one-texel inner edge (shadowed under the top and left of the band, lit along the bottom and
    right) and parchment inside. band(t, d, side) gives the band's colour key at depth d (1-3) and
    position t along that side; band.palette maps its keys (and 'o' the outline) to colours."""
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            a, b = min(x, w - 1 - x), min(y, h - 1 - y)
            if a + b < 2:
                continue
            d = min(a, b)
            if d == 0 or a + b == 2:
                value = band.palette['o']
            elif d <= 3:
                side = ('top' if y == b else 'bottom') if b <= a else ('left' if x == a else 'right')
                t = x if side in ('top', 'bottom') else y
                value = band.palette[band(t, d, side)]
            elif d == 4:
                value = PAPER['s'] if (b == 4 and y == b) or (a == 4 and x == a) else PAPER['l']
                if b == 4 and a == 4:
                    value = PAPER['r']
            else:
                value = PAPER['q'] if (x * 37 + y * 101 + (x * y) % 13) % 61 == 0 else PAPER['p']
            image.putpixel((x, y), color(value))
    return image


def lit(side):
    return side in ('top', 'left')


def iron_band(t, d, side):
    """Blackened iron strapping, bevelled, with a rivet every 16 texels."""
    if d == 2:
        if t % 16 == 8:
            return 'w'
        if t % 16 == 9:
            return 'k'
        return 'm'
    return ('h' if lit(side) else 'k') if d == 1 else ('k' if lit(side) else 'n')


iron_band.palette = {'o': '141316', 'k': '27262B', 'm': '3B3940', 'n': '4C4A52', 'h': '66636D', 'w': '9A97A3'}


def brick_band(t, d, side):
    """Two courses of fired brick with a mortar joint between them."""
    if d == 2:
        return 'g'
    joint = (t + (0 if d == 1 else 3)) % 6 == 0
    if joint:
        return 'g'
    first = (t + (0 if d == 1 else 3)) % 6 == 1
    return 'R' if first and lit(side) else ('q' if not lit(side) else 'r')


brick_band.palette = {'o': '2E1A12', 'g': 'B9A58A', 'q': '7A3422', 'r': '94442C', 'R': 'B0573A'}


def wood_band(t, d, side):
    """Scrubbed pale planks, a lit arris outside and a shadowed one inside, joined every 44 texels
    with a nail head either side of each joint."""
    if t % 44 == 22:
        return 'o'
    if d == 2 and t % 44 in (19, 25):
        return 'N'
    if d == 1:
        return 'H' if lit(side) else 'd'
    if d == 3:
        return 'd' if lit(side) else 'H'
    return 'm' if t % 9 == 4 or t % 13 == 0 else 'n'


wood_band.palette = {'o': '5A4228', 'd': 'A88A5E', 'm': 'BFA273', 'n': 'D0B686', 'H': 'E8D4A8', 'N': '4A3A2A'}

WELL_ART = """
dddddddddddddf
dkkkkkkkkkkkkl
dkkkkkkkkkkkkl
dkkkkkkkkkkkkl
dkkkkkkkkkkkkl
dkkkkkkkkkkkkl
dkkkkkkkkkkkkl
dkkkkkkkkkkkkl
dkkkkkkkkkkkkl
dkkkkkkkkkkkkl
dGgGgGgGgGgGgl
dkaAkkAkaAkkAl
dAkaAkkAkkaAkl
flllllllllllll
"""
WELL_COLORS = {'d': '3A2A1E', 'l': 'F5ECD3', 'f': 'A28C64', 'k': '2A1E16', 'g': '4A4850', 'G': '6E6C76',
               'a': '7A726A', 'A': '453A32'}
BOWL_GHOST = """
................
................
................
................
................
................
................
..xxxxxxxxxxxx..
.xyyyyyyyyyyyyx.
.xxxxxxxxxxxxxx.
..xxxxxxxxxxxx..
...xxxxxxxxxx...
....xxxxxxxx....
......xxxx......
.....xxxxxx.....
................
"""
GHOST = {'x': '9C8C70', 'y': '84755B'}
FLAME_MASK = """
......#.......
......##......
.....###......
.....####.....
....#####.....
....######..#.
...#######.##.
..#.#######.#.
..###########.
.############.
.############.
.############.
..##########..
...########...
"""


def mask(pattern):
    rows = pattern.strip('\n').splitlines()
    return {(x, y) for y, row in enumerate(rows) for x, ch in enumerate(row) if ch == '#'}


def engraved(image, x0, y0, cells, fill, dark, light):
    """A shape pressed into the parchment: its top and left edges in shadow, bottom and right lit."""
    for x, y in cells:
        if (x, y - 1) not in cells or (x - 1, y) not in cells:
            value = dark
        elif (x, y + 1) not in cells or (x + 1, y) not in cells:
            value = light
        else:
            value = fill
        image.putpixel((x0 + x, y0 + y), color(value))


def arrow_cells():
    """The progress arrow: a five-texel shaft and a broad head, 24x17."""
    return {(x, y) for x in range(24) for y in range(17) if (x <= 15 and 6 <= y <= 10) or (x >= 15 and abs(y - 8) <= 23 - x)}


PREP_MOTIF = """
.......................................................
.......gg..............................................
......gGg.g............................................
.......gGgG............................................
...BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB....
..BhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhbB...
..BhbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbBBBB
..BhbbbbKKKKKKKKKKKKKKKKKKKKKKKKKKwwwwwwwwwbbbbbbbbB..B
..BhbbbKkkkkkkkkkkkkkkkkkkkkkkkkKwWWWWWWWWwbbOOObbbBBBB
..BhbbbbKkkkkkkkkkkkkkkkkkkkkkkkKwwwwwwwwwbbOoooObbB...
..BhbbbbbKKKKKKKKKKKKKKKKKKKKKKKKbbbbbbbbbbOoooObbbB...
..BhbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbOOObbbbB...
...BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB....
.......................................................
"""
MOTIF_COLORS = {'B': '8C7250', 'h': 'D8C090', 'b': 'C4A878', 'K': '7C7870', 'k': 'B4B0A6', 'w': '6E5236', 'W': '8E6E48',
                'O': 'A0763E', 'o': 'C89A58', 'g': '7E8E52', 'G': '9AAA66'}


def station(kind):
    """One station's 176x166 panel on its 256x256 sheet."""
    image = panel(*PANEL, {'pot': iron_band, 'oven': brick_band, 'prep': wood_band}[kind])
    for x, y in GRID + INVENTORY:
        slot(image, x, y)
    if kind == 'pot':
        slot(image, *VESSEL)
        stamp(image, *VESSEL, BOWL_GHOST, GHOST)
        stamp(image, *WELL, WELL_ART, WELL_COLORS)
    elif kind == 'oven':
        slot(image, *VESSEL)
        engraved(image, *WELL, mask(FLAME_MASK), PAPER['r'], PAPER['s'], PAPER['l'])
    else:
        stamp(image, 29, 55, PREP_MOTIF, MOTIF_COLORS)
    engraved(image, *ARROW, arrow_cells(), PAPER['r'], PAPER['s'], PAPER['l'])
    recess(image, *RESULT_FRAME, 26, 26, SLOT['d'], SLOT['f'], SLOT['l'])
    return image


# -- the recipe book panel and the screen sprites -------------------------------------------------

LEATHER = {'o': '2A140C', 'L': '86452A', 'l': '6A3320', 'd': '4E2416', 'S': 'C9A46A'}
BOOK_GRID, BOOK_CELL = (10, 22), 20
TITLE_BAND = (5, 18)       # the rows behind "Recipes", written at (10, 8)
FOOTER = (146, 162)        # page arrows at (24, 146) and (84, 146), the page number between them


def book_panel():
    """The 120x166 recipe book: a parchment page on a stitched leather cover (four texels round the
    top and sides, three along the bottom so the footer's arrows fit above it), a title band, faint
    squares where the 5x6 recipe cells go and a rule over the footer."""
    w, h = BOOK_PANEL
    image = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            a, b = min(x, w - 1 - x), min(y, h - 1 - y)
            if a + b < 2:
                continue
            d = min(a, b if y < h // 2 else b + 1)
            side = ('top' if y < h // 2 else 'bottom') if (b if y < h // 2 else b + 1) <= a else ('left' if x < w // 2 else 'right')
            if d == 0 or a + b == 2:
                value = LEATHER['o']
            elif d <= 3:
                t = x if side in ('top', 'bottom') else y
                if d == 2 and t % 4 in (1, 2) and 4 <= t <= (w if side in ('top', 'bottom') else h) - 5:
                    value = LEATHER['S']
                elif d == 1:
                    value = LEATHER['L'] if side in ('top', 'left') else LEATHER['d']
                else:
                    value = LEATHER['l'] if d == 2 else (LEATHER['d'] if side in ('top', 'left') else LEATHER['L'])
            elif d == 4:
                value = PAPER['s'] if side in ('top', 'left') else PAPER['l']
            else:
                value = PAPER['q'] if (x * 37 + y * 101 + (x * y) % 13) % 61 == 0 else PAPER['p']
            image.putpixel((x, y), color(value))
    top, bottom = TITLE_BAND
    area(image, 5, top, w - 6, bottom, PAPER['q'])
    area(image, 5, bottom + 1, w - 6, bottom + 1, PAPER['s'])
    area(image, 5, bottom + 2, w - 6, bottom + 2, PAPER['l'])
    stamp(image, w - 22, top + 2, BOOK_SPRIG, MOTIF_COLORS)
    gx, gy = BOOK_GRID
    for row in range(6):
        for col in range(5):
            x, y = gx + col * BOOK_CELL, gy + row * BOOK_CELL
            for i in range(2, 18):
                for j in (1, 18):
                    image.putpixel((x + i, y + j), color(PAPER['q']))
                    image.putpixel((x + j, y + i), color(PAPER['q']))
    area(image, 8, FOOTER[0] - 2, w - 9, FOOTER[0] - 2, PAPER['s'])
    area(image, 8, FOOTER[0] - 1, w - 9, FOOTER[0] - 1, PAPER['l'])
    return image


BOOK_SPRIG = """
.....gg..........
....gGg.....gg...
..g.gGg....gGg...
.gGggGgg..gGgg.g.
..gGgGgGggGgGggG.
...gggggGgggggg..
.....BBBBBBBB....
"""


def progress_sprite():
    """The filled arrow (same shape as the engraved one on the panels), ember-gold and outlined."""
    cells = arrow_cells()
    edge = {c for c in cells if any((c[0] + dx, c[1] + dy) not in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
    image = Image.new('RGBA', (24, 17), (0, 0, 0, 0))
    for x, y in cells:
        if (x, y) in edge:
            value = '6A2A0C'
        elif (x, y - 1) in edge:
            value = 'FFE08A'
        elif (x, y + 1) in edge or (x + 1, y) in edge:
            value = 'D9772A'
        else:
            value = 'F7B23C'
        image.putpixel((x, y), color(value))
    return image


FIRE_COLORS = {'r': 'B8361A', 'o': 'EE7420', 'F': 'FFC23A', 'w': 'FFF2A8', 'L': '4A2E18', 'l': '7A5230', 'e': 'E2471E',
               'k': '2A1A10', 'm': '9A6A40'}
HEAT = """
..............
.......r......
...r...or..r..
...or..oFr.or.
..roor.oFo.oFr
..rFor.rFFroFr
.roFForrFwFoFr
.rFwFoFoFwFFor
.roFwFFFwwwFr.
..rFwwwwwwFor.
..roFwwwwFFr..
..lLmeoooemLl.
.LllLLmLLmLLlL
..............
"""
# The fire under the pot: three tongues of flame over two crossed logs, inside the well's frame.


def flame_sprite():
    """The oven's burning flame: the panel's flame shape, hottest at the heart."""
    cells = mask(FLAME_MASK)
    image = Image.new('RGBA', (14, 14), (0, 0, 0, 0))
    layer, depth, left = {}, 0, set(cells)
    while left:
        rim = {c for c in left if any((c[0] + dx, c[1] + dy) not in left for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))}
        for c in rim:
            layer[c] = depth
        left -= rim
        depth += 1
    for (x, y), d in layer.items():
        image.putpixel((x, y), color(FIRE_COLORS['roFw'[min(d, 3)]]))
    return image


BUTTON = {'o': '3B2A1E', 'L': 'F5ECD3', 'f': 'D8C49A', 'D': 'A28C64'}
BUTTON_HOT = {'o': '7A4A12', 'L': 'FFFBE6', 'f': 'F4E2B0', 'D': 'D0A456'}
BOOK_ICON = """
.kkkkkkkkkkkk...
kbYRRRRRRRRYk...
kbRrrrrrrrrRkk..
kbRrGGGGGGrRkPk.
kYRrGyyyyGrRkPk.
kbRrGGGGGGrRkPk.
kbRrrrrrrrrRkPk.
kbRrrrrrrrrRkPk.
kYRrrrrrrrrRkPk.
kbRrrrrrrrrRkPk.
kbYRRRRRRRRYkPk.
kkkkkkkkkkkkkPk.
.kPpPpPpPpPpPkk.
..kkkkkgkkkkkk..
"""
BOOK_COLORS = {'k': '2E140C', 'R': 'B8402F', 'r': '8E2A22', 'b': '5E1A14', 'G': 'B8862E', 'y': 'F2D27A', 'Y': 'E8C84A',
               'P': 'F2E8CC', 'p': 'D2C6A2', 'g': '3E8A4A'}


def book_sprite(hot):
    """The 20x18 recipe book button: a bevelled parchment button holding a red leather recipe book
    (gold-cornered, a dark spine with gold bands, a ribbon); highlighted, the button warms to gold."""
    pal = BUTTON_HOT if hot else BUTTON
    image = Image.new('RGBA', (20, 18), (0, 0, 0, 0))
    for y in range(18):
        for x in range(20):
            a, b = min(x, 19 - x), min(y, 17 - y)
            if a + b < 2:
                continue
            if min(a, b) == 0 or a + b == 2:
                value = pal['o']
            elif min(a, b) == 1:
                value = pal['L'] if (y == 1 or x == 1) else pal['D']
            else:
                value = pal['f']
            image.putpixel((x, y), color(value))
    stamp(image, 3, 2, BOOK_ICON, BOOK_COLORS)
    return image


def cell_sprite(fill, dark, light, trim=None):
    """A recipe cell (20x20): a card pressed into the page, the recipe's icon drawn 2 texels in."""
    image = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
    recess(image, 0, 0, 20, 20, dark, fill, light)
    if trim:
        for i in range(1, 19):
            for j in (1, 18):
                image.putpixel((i, j), color(trim)); image.putpixel((j, i), color(trim))
    return image


UNKNOWN = """
................
..oooooooooooo..
..oPPPPPPPPPPo..
..oPPPkkkkPPpo..
..oPPkkPPkkPpo..
..oPPPPPPkkPpo..
..oPPPPPkkPPpo..
..oPPPPkkPPPpo..
..oPPPPkkPPPpo..
..oPPPPPPPPPpo..
..oPPPPkkPPPpo..
..opppRRRRpppo..
..ooooRrRRoooo..
......RRRd......
.......dd.......
................
"""
# A sealed family recipe card: a "?" in ink and a red wax seal over its bottom edge.
UNKNOWN_COLORS = {'o': '5A4228', 'P': 'F2E6C4', 'p': 'D2C094', 'k': '5A3A22', 'R': 'C33A2E', 'r': 'E66A58', 'd': '7A1E16'}


def gui_sprites():
    """Every sprite the screens draw, by atlas id (textures/gui/sprites/<id>.png)."""
    return {
        'hearth/progress': progress_sprite(),
        'hearth/heat': raster14(HEAT, FIRE_COLORS),
        'hearth/flame': flame_sprite(),
        'hearth/book': book_sprite(False),
        'hearth/book_highlighted': book_sprite(True),
        'hearth/recipe': cell_sprite('D4C29A', 'A28C64', 'F5ECD3'),
        'hearth/recipe_highlighted': cell_sprite('ECDDB4', 'B8862E', 'FFF6D0', trim='F2C860'),
        'hearth/recipe_missing': cell_sprite('D8A890', '8E2E22', 'F6D4C4'),
        'hearth/unknown': stamp(Image.new('RGBA', (16, 16), (0, 0, 0, 0)), 0, 0, UNKNOWN, UNKNOWN_COLORS),
    }


SPRITE_SIZES = {'progress': (24, 17), 'heat': (14, 14), 'flame': (14, 14), 'book': (20, 18), 'book_highlighted': (20, 18),
                'recipe': (20, 20), 'recipe_highlighted': (20, 20), 'recipe_missing': (20, 20), 'unknown': (16, 16)}


def raster14(pattern, palette):
    rows = pattern.strip('\n').splitlines()
    image = Image.new('RGBA', (len(rows[0]), len(rows)), (0, 0, 0, 0))
    return stamp(image, 0, 0, pattern, palette)


def gui_textures():
    """Every GUI texture, by path under textures/gui/."""
    found = {f'container/hearth_{kind}': station(kind) for kind in ('pot', 'oven', 'prep')}
    found['container/hearth_book'] = book_panel()
    found.update({f'sprites/{key}': image for key, image in gui_sprites().items()})
    return found


# -- compiling --------------------------------------------------------------------------------------

def dump(data, indent=2):
    return (json.dumps(data, indent=indent) + '\n').encode()


def png(image):
    buffer = io.BytesIO(); image.save(buffer, 'PNG')
    return buffer.getvalue()


def outputs():
    """Every compiled file: path -> bytes."""
    files = {}
    for key, image in block_textures().items():
        files[ASSETS / f'textures/block/hearth/{key}.png'] = png(image)
    for key, image in gui_textures().items():
        files[ASSETS / f'textures/gui/{key}.png'] = png(image)
    for name, models in designs().items():
        for model in models:
            files[ASSETS / f'models/block/{model.name}.json'] = dump(model.json(PARTICLES[name]), 1)
        files[ASSETS / f'blockstates/{name}.json'] = dump(blockstate(name, models))
        files[ASSETS / f'items/{name}.json'] = dump({'model': {'type': 'minecraft:model', 'model': f'{NS}:block/{models[0].name}'}})
    return files


def write():
    for path, data in outputs().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    models = [m for ms in designs().values() for m in ms]
    print(f'Hearth stations: {len(designs())} blocks, {len(models)} models '
          f'({", ".join(f"{m.name} {len(m.elements)}" for m in models)} elements), '
          f'{len(block_textures())} block textures, {len(gui_textures())} GUI textures.')


def problems_in(models):
    """Anything Minecraft would reject (or that breaks the house rules) in the compiled models."""
    found, painted = [], set(block_textures())
    for model in models:
        if len(model.elements) >= 40:
            found.append(f'{model.name}: {len(model.elements)} elements (keep it under 40)')
        for e in model.elements:
            if not all(-16 <= c <= 32 for c in e['from'] + e['to']):
                found.append(f'{model.name}: element {e["from"]}..{e["to"]} leaves -16..32')
            if any(e['from'][i] > e['to'][i] for i in range(3)):
                found.append(f'{model.name}: element {e["from"]}..{e["to"]} is inside out')
            r = e.get('rotation')
            if r and (r['axis'] not in ('x', 'y', 'z') or r['angle'] not in (0, 22.5, -22.5, 45, -45)):
                found.append(f'{model.name}: rotation {r} is not 0/22.5/45 on one axis')
            for face, spec in e['faces'].items():
                if not all(0 <= c <= 16 for c in spec['uv']):
                    found.append(f'{model.name}: {face} uv {spec["uv"]} leaves 0..16')
        for path in model.textures.values():
            if path.startswith(f'{NS}:block/hearth/') and path.rsplit('/', 1)[1] not in painted:
                found.append(f'{model.name}: missing texture {path}')
    return found


def gui_problems():
    """The screens' contract: sheet and sprite sizes, a slot frame round every item area the code
    uses, and the book button's corner left plain for the button."""
    found, gui = [], gui_textures()
    for key, image in gui.items():
        if key.startswith('container/') and image.size != (256, 256):
            found.append(f'{key}: {image.size}, not 256x256')
    for name, size in SPRITE_SIZES.items():
        image = gui.get(f'sprites/hearth/{name}')
        if image is None or image.size != size:
            found.append(f'sprites/hearth/{name}: {image.size if image else "missing"}, not {size[0]}x{size[1]}')
    paper = {color(v) for v in PAPER.values()}
    for kind in ('pot', 'oven', 'prep'):
        image = gui[f'container/hearth_{kind}']
        wanted = GRID + INVENTORY + ([VESSEL] if kind != 'prep' else [])
        for x, y in wanted:
            if image.getpixel((x - 1, y - 1)) != color(SLOT['d']) or image.getpixel((x + 16, y + 16)) != color(SLOT['l']):
                found.append(f'hearth_{kind}: no slot frame round ({x}, {y})')
        if image.getpixel(RESULT_FRAME) != color(SLOT['d']):
            found.append(f'hearth_{kind}: no result frame at {RESULT_FRAME}')
        bx, by = BOOK_BUTTON
        if any(image.getpixel((x, y)) not in paper for x in range(bx, bx + 20) for y in range(by, by + 18)):
            found.append(f'hearth_{kind}: the book button area is not plain parchment')
    return found


def check():
    def same(path, data):
        # Git may check text files out with CRLF line endings; compare them line by line.
        if not path.exists():
            return False
        current = path.read_bytes()
        return current == data if path.suffix == '.png' else current.replace(b'\r\n', b'\n') == data
    problems = [f'out of date: {p.relative_to(PROJECT)}' for p, data in outputs().items() if not same(p, data)]
    problems += problems_in([m for models in designs().values() for m in models])
    problems += gui_problems()
    if problems:
        print('Run tools/hearth/stations.py:\n  ' + '\n  '.join(problems)); sys.exit(1)
    print('Hearth stations are up to date.')


def boxes():
    for name, models in designs().items():
        rows = ','.join('{' + ','.join(f'{c:g}' for c in b) + '}' for b in models[0].boxes)
        print(f'{name}: new double[][]{{{rows}}}')


# -- preview ----------------------------------------------------------------------------------------

def client_jar():
    jars = sorted(Path.home().glob('.gradle/caches/fabric-loom/*/minecraft-client.jar'))
    return zipfile.ZipFile(jars[-1]) if jars else None


def vanilla_model(jar, name):
    """A vanilla block model with its parents' elements and textures resolved (for the preview)."""
    textures, elements = {}, None
    while name:
        data = json.loads(jar.read(f'assets/minecraft/models/{name.replace("minecraft:", "")}.json'))
        textures = {**data.get('textures', {}), **textures}
        elements = elements or data.get('elements')
        name = data.get('parent')
    m = Model(name or 'vanilla', [])
    m.elements = json.loads(json.dumps(elements or []))

    def resolve(ref):
        while ref.startswith('#'):
            ref = textures[ref[1:]]
        return ref if ':' in ref else 'minecraft:' + ref
    for e in m.elements:
        for spec in e['faces'].values():
            key = resolve(spec['texture']).replace(':', '_').replace('/', '_')
            m.textures[key] = resolve(spec['texture'])
            spec['texture'] = '#' + key
    return m


class Missing(dict):
    def __missing__(self, key):
        return Image.new('RGBA', (16, 16), (200, 0, 200, 255))


def preview_textures(jar, models):
    found = Missing({f'{NS}:block/hearth/{k}': v for k, v in block_textures().items()})
    found.update({f'{NS}:block/workstation/{k}': v for k, v in paint.textures().items()})
    if jar:
        for key in {v for m in models for v in m.textures.values() if v.startswith('minecraft:')}:
            try:
                found[key] = Image.open(io.BytesIO(jar.read(f'assets/minecraft/textures/{key[10:]}.png'))).convert('RGBA').crop((0, 0, 16, 16))
            except KeyError:
                pass
    return found


def framed(image, size, margin=12):
    """A render cropped to what was drawn and scaled to fit a size x size tile."""
    box = image.getbbox() or (0, 0, image.width, image.height)
    side = max(box[2] - box[0], box[3] - box[1]) + 2 * margin
    cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
    crop = image.crop((cx - side // 2, cy - side // 2, cx - side // 2 + side, cy - side // 2 + side))
    return crop.resize((size, size), Image.LANCZOS)


def lifted(model, dy):
    """A copy of a model moved up by dy texels (to stack it on another in a preview)."""
    out = furniture.Scene()
    out.textures = dict(model.textures)
    for e in model.elements:
        e = json.loads(json.dumps(e))
        e['from'][1] += dy; e['to'][1] += dy
        if 'rotation' in e:
            e['rotation']['origin'][1] += dy
        out.elements.append(e)
    return out


def merged(*models):
    """One scene of several models' elements (deep copies: diced pieces share their rotation dicts)."""
    out = furniture.Scene()
    for m in models:
        out.elements += json.loads(json.dumps(m.elements))
        out.textures.update(m.textures)
    return out


def preview_models():
    """build/previews/hearth_stations.png: every model from the front (north-east) and back (south-west),
    and the pot sitting on a lit campfire, the way it is used."""
    jar = client_jar()
    campfire = vanilla_model(jar, 'block/campfire') if jar else Model('campfire', [])
    models = [m for ms in designs().values() for m in ms]
    found = preview_textures(jar, models + [campfire])
    tiles = []
    for m in models:
        tiles.append((m.name, [kit.render(furniture.diced(m), found), kit.render(furniture.diced(m), found, view=(-1, .9, 1.15))]))
    for m in designs()['cooking_pot']:
        stack = merged(lifted(furniture.diced(campfire), -16), furniture.diced(m))
        stack = furniture.Scene.shrink(stack, .62, (8, -2, 8))
        tiles.append((f'{m.name} on a campfire', [kit.render(stack, found), kit.render(stack, found, view=(-1, .9, 1.15))]))
    tile = 280
    cols = 2
    sheet = Image.new('RGB', (cols * tile * 2, ((len(tiles) + cols - 1) // cols) * (tile + 24)), '#7FA7C9')
    draw = ImageDraw.Draw(sheet)
    dest = PROJECT / 'build/previews'
    dest.mkdir(parents=True, exist_ok=True)
    for n, (name, views) in enumerate(tiles):
        x, y = (n % cols) * tile * 2, (n // cols) * (tile + 24)
        for i, view in enumerate(views):
            small = framed(view, tile)
            sheet.paste(small, (x + i * tile, y + 24), small)
        views[0].save(dest / f'hearth-{name.replace(" ", "_")}.png')
        draw.text((x + 8, y + 6), f'{name}  (front from the north-east, back from the south-west)', fill='#10202E')
    sheet.save(dest / 'hearth_stations.png')
    print(dest / 'hearth_stations.png')


def vanilla_image(jar, path):
    if not jar:
        return None
    try:
        return Image.open(io.BytesIO(jar.read(f'assets/minecraft/textures/{path}.png'))).convert('RGBA')
    except KeyError:
        return None


def mod_item(name):
    path = ASSETS / f'textures/item/{name}.png'
    return Image.open(path).convert('RGBA') if path.exists() else None


def composed(kind, jar, progress=.6, fuel=.7):
    """A station's background with what its screen draws over it: the book button, the heat or the
    burning flame, a part-filled arrow, some items and the labels (in vanilla's text colour)."""
    textures = gui_textures()
    image = textures[f'container/hearth_{kind}'].crop((0, 0, *PANEL))
    sprites = gui_sprites()
    image.alpha_composite(sprites.get('hearth/book', Image.new('RGBA', (1, 1))), BOOK_BUTTON)
    if kind == 'pot' and 'hearth/heat' in sprites:
        image.alpha_composite(sprites['hearth/heat'], WELL)
    if kind == 'oven' and 'hearth/flame' in sprites:
        k = round(14 * fuel)
        image.alpha_composite(sprites['hearth/flame'].crop((0, 14 - k, 14, 14)), (WELL[0], WELL[1] + 14 - k))
    if 'hearth/progress' in sprites:
        image.alpha_composite(sprites['hearth/progress'].crop((0, 0, round(24 * progress), 17)), ARROW)
    items = {'pot': ['carrot', 'potato', 'beef', 'onion'], 'oven': ['wheat', 'egg', 'sugar', 'apple'], 'prep': ['carrot', 'beetroot', 'cod', 'potato']}[kind]
    for (x, y), name in zip(GRID, items):
        item = mod_item(name) or vanilla_image(jar, f'item/{name}')
        if item:
            image.alpha_composite(item.crop((0, 0, 16, 16)), (x, y))
    extra = {'pot': ('bowl', VESSEL), 'oven': ('charcoal', VESSEL)}.get(kind)
    if extra and kind == 'oven':
        item = vanilla_image(jar, f'item/{extra[0]}')
        if item:
            image.alpha_composite(item.crop((0, 0, 16, 16)), extra[1])
    for (x, y), name in zip(INVENTORY[18:], ['bread', 'bowl', 'carrot']):
        item = vanilla_image(jar, f'item/{name}')
        if item:
            image.alpha_composite(item.crop((0, 0, 16, 16)), (x, y))
    result = mod_item('hearty_stew') or vanilla_image(jar, 'item/rabbit_stew')
    if result:
        image.alpha_composite(result.crop((0, 0, 16, 16)), RESULT)
    mc_text(image, 8, 6, {'pot': 'Cooking Pot', 'oven': 'Clay Oven', 'prep': 'Prep Table'}[kind], jar)
    mc_text(image, 8, 72, 'Inventory', jar)
    return image


def mc_text(image, x, y, text, jar, value='404040'):
    """Writes text with Minecraft's own bitmap font (ascii.png), as the screen will."""
    font = vanilla_image(jar, 'font/ascii')
    if font is None:
        ImageDraw.Draw(image).text((x, y - 1), text, fill=color(value))
        return
    for ch in text:
        code = ord(ch)
        if ch == ' ':
            x += 4
            continue
        glyph = font.crop(((code % 16) * 8, (code // 16) * 8, (code % 16) * 8 + 8, (code // 16) * 8 + 8))
        width = max((i for i in range(8) for j in range(8) if glyph.getpixel((i, j))[3]), default=-1) + 1
        for i in range(width):
            for j in range(8):
                if glyph.getpixel((i, j))[3]:
                    image.putpixel((x + i, y + j), color(value))
        x += width + 1



def composed_book(jar):
    """The recipe book page with what its screen draws: recipe cells (one hovered, one missing an
    ingredient, one unlearned family recipe), the page arrows, the title and the page number."""
    image = gui_textures()['container/hearth_book'].crop((0, 0, *BOOK_PANEL))
    sprites = gui_sprites()
    names = ['bread', 'cookie', 'pumpkin_pie', 'cake', 'rabbit_stew', 'mushroom_stew', 'beetroot_soup', 'baked_potato',
             'cooked_cod', 'cooked_salmon', 'golden_carrot', 'honey_bottle', 'apple', 'sweet_berries']
    names = ['hearty_stew', 'shepherds_pie', 'apple_tart', 'ploughmans_lunch', 'fresh_village_bread'] + names
    gx, gy = BOOK_GRID
    for n, name in enumerate(names[:17]):
        x, y = gx + (n % 5) * BOOK_CELL, gy + (n // 5) * BOOK_CELL
        cell = 'hearth/recipe_highlighted' if n == 6 else 'hearth/recipe_missing' if n in (3, 11) else 'hearth/recipe'
        image.alpha_composite(sprites[cell], (x, y))
        if n == 16:
            image.alpha_composite(sprites['hearth/unknown'], (x + 2, y + 2))
            continue
        item = mod_item(name) or vanilla_image(jar, f'item/{name}')
        if item:
            image.alpha_composite(item.crop((0, 0, 16, 16)), (x + 2, y + 2))
    for name, x in (('page_backward', 24), ('page_forward', 84)):
        arrow = vanilla_image(jar, f'gui/sprites/recipe_book/{name}')
        if arrow:
            image.alpha_composite(arrow, (x, FOOTER[0]))
    mc_text(image, 10, 8, 'Recipes', jar)
    mc_text(image, 52, 151, '1/3', jar)
    return image


def preview_gui():
    """build/previews/hearth_gui.png: the recipe book beside each screen at 2x, with the sprites
    where the code draws them; the same at 1x; and every sprite at 8x."""
    jar = client_jar()
    book = composed_book(jar)
    shots = []
    for kind in ('pot', 'oven', 'prep'):
        both = Image.new('RGBA', (BOOK_PANEL[0] + 2 + PANEL[0], PANEL[1]), (0, 0, 0, 0))
        both.alpha_composite(book, (0, 0))
        both.alpha_composite(composed(kind, jar), (BOOK_PANEL[0] + 2, 0))
        shots.append(both)
    sprites = gui_sprites()
    strip_h = 20 * 8 + 24
    pad = 12
    width = max(shots[0].width * 2 * 2 + 3 * pad, sum(v.width * 8 + pad for v in sprites.values()) + pad)
    sheet = Image.new('RGB', (width, 2 * (shots[0].height * 2 + pad) + shots[0].height + strip_h + 3 * pad), '#2B3440')
    for n, shot in enumerate(shots):
        big = shot.resize((shot.width * 2, shot.height * 2), Image.NEAREST)
        x, y = pad + (n % 2) * (big.width + pad), pad + (n // 2) * (big.height + pad)
        sheet.paste(big, (x, y), big)
    y = pad + 2 * (shots[0].height * 2 + pad)
    x = pad
    for shot in shots:
        sheet.paste(shot, (x, y), shot)
        x += shot.width + pad
    x, y = pad, y + shots[0].height + pad
    for key, sprite in sprites.items():
        big = sprite.resize((sprite.width * 8, sprite.height * 8), Image.NEAREST)
        back = Image.new('RGB', big.size, '#' + PAPER['p'])
        sheet.paste(back, (x, y + 14))
        sheet.paste(big, (x, y + 14), big)
        ImageDraw.Draw(sheet).text((x, y), key.split('/')[1], fill='#E0E6EE')
        x += big.width + pad
    dest = PROJECT / 'build/previews/hearth_gui.png'
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest)
    print(dest)


def preview():
    preview_models()
    preview_gui()


if __name__ == '__main__':
    if '--check' in sys.argv: check()
    elif '--preview' in sys.argv: preview()
    elif '--boxes' in sys.argv: boxes()
    else: write()
