"""Authored art for Tall Tales Fishing, in the style of tools/hearth/sprites.py, tools/hearth/stations.py and
tools/tavern/sprites.py: native pixel patterns, a dark outline per material, stepped palettes (3-5 tones),
light from the top left, no antialiasing and alpha only 0 or 255.

    rods          reinforced_rod and anglers_rod on vanilla's fishing rod (same diagonal, same reel spot), each
                  with a _cast texture that, like vanilla's, drops the line hanging from the tip; models parent
                  minecraft:item/handheld_rod and items/ switches on minecraft:fishing_rod/cast
    items         bait (bait_worms, chum, glow_bait, legend_lure), tackle (cork_bobber, lead_sinker, barbed_hook,
                  treasure_hook, spinner) and anglers_journal, message_in_a_bottle, grilled_fish
    trophy_mount  a wooden wall plaque with a brass nameplate, 12x10x1 against the south face for facing=north
                  (turned like a wall sign); the game draws the mounted fish in front of its plain middle
    minigame      textures/gui/sprites/fishing/minigame/: the catch-bar frame (40x152; the water track is
                  x 6..21, the progress channel x 28..33, both y 6..145), the nine-sliced catch zone, the fish,
                  the legendary fish and the treasure chest
    journal       textures/gui/fishing/journal.png (an open book in the top-left 280x180 of a 512x256 sheet;
                  the left page's content is x 14..134, the right page's x 146..266, both y 14..166) and its
                  slot, selected slot and star sprites (textures/gui/sprites/fishing/journal/)

    python tools/fishing/art.py            # write every texture, model, item definition and the blockstate
    python tools/fishing/art.py --check    # verify the files match the patterns and the screens' contract
    python tools/fishing/art.py --preview  # build/previews/fishing_art_items.png, _block.png and _gui.png

Never hand-edit the PNG or JSON; change the patterns here and rerun.
"""
import io
import json
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ASSETS = PROJECT / 'src/main/resources/assets/villagefriends'
NS = 'villagefriends'
sys.path.insert(0, str(HERE.parent / 'workstations'))


# -- drawing ----------------------------------------------------------------------------------------

def rgba(color):
    return tuple(bytes.fromhex(color.lstrip('#'))) + (255,)


def rows_of(pattern):
    return pattern.strip('\n').split('\n') if isinstance(pattern, str) else list(pattern)


def stamp(image, pattern, palette, x=0, y=0):
    """Paints a pattern onto the image at x, y; '.' and ' ' leave what is there."""
    for j, row in enumerate(rows_of(pattern)):
        for i, ch in enumerate(row):
            if ch not in '. ':
                assert 0 <= x + i < image.width and 0 <= y + j < image.height, (x + i, y + j, row)
                image.putpixel((x + i, y + j), rgba(palette[ch]))
    return image


def sprite(*layers, size=(16, 16)):
    """Layers are (pattern, palette, x, y), drawn back to front onto a transparent image."""
    image = Image.new('RGBA', size, (0, 0, 0, 0))
    for pattern, palette, x, y in layers:
        stamp(image, pattern, palette, x, y)
    return image


def area(image, x0, y0, x1, y1, color):
    """Fills x0..x1, y0..y1 (inclusive)."""
    if x1 >= x0 and y1 >= y0:
        ImageDraw.Draw(image).rectangle([x0, y0, x1, y1], fill=rgba(color))


def merged(*palettes, **extra):
    out = {}
    for p in palettes:
        out.update(p)
    out.update(extra)
    return out


# -- rods: vanilla's rod, re-made in new materials -----------------------------------------------------
# Lanes run with the rod: 'l' the line along its top, 'c' the lit edge, 'w'/'e' the wood, 'd' the shadowed
# edge. The reel sits under the grip where vanilla's does; the hanging line and hook are a separate layer
# so the _cast texture is the rod without it, exactly like vanilla's fishing_rod_cast.

HANGING_LINE = """
................
................
................
................
..............l.
..............l.
..............t.
..............t.
..............g.
..............t.
.............t..
.............l..
............l...
..........W.W...
..........hW....
................
"""
LINE = {'l': '444444', 't': '646464', 'g': '747474', 'W': 'FFFFFF', 'h': '969696'}  # vanilla's line and hook

REINFORCED_ROD = """
................
.............tl.
............tcd.
...........lced.
..........lcwd..
.........lIij...
........lcwd....
.......lcwd.....
......lIij......
.....lced.......
.....Iij........
....cezZx.......
...ccdzZx.......
..ccd.xx........
..ij............
................
"""
REINFORCED = {'l': '444444', 't': 'A8B0B4',
              'c': '3A2818', 'w': '6E4C2C', 'e': '523820', 'd': '1C1208',   # dark wood
              'I': 'D8DCDE', 'i': '9AA2A6', 'j': '4E5458',                    # iron bands, ferrule and butt cap
              'Z': 'D8DCDE', 'z': '9AA2A6', 'x': '3A4044'}                    # the iron reel

ANGLERS_ROD = """
................
.............Yl.
............Ycd.
...........lced.
..........lcwd..
.........lYyz...
........lcGd....
.......lcwd.....
......lYyz......
.....lced.......
.....Yyz........
....KkZZx.......
...KKkzZx.......
..Kkq.xx........
..yz............
................
"""
ANGLERS = {'l': '444444',
           'c': '4A1E12', 'w': '8E4228', 'G': 'C0663E', 'e': '6A2E1C', 'd': '260C06',   # polished mahogany
           'Y': 'F8D868', 'y': 'D8A830', 'z': '8A5A12',                                 # gold fittings
           'K': 'E2BC86', 'k': 'C49660', 'q': '8E6434',                                 # the cork grip
           'Z': 'FFE680', 'x': '7A4E10'}                                                # the gold reel

RODS = {'reinforced_rod': (REINFORCED_ROD, REINFORCED, LINE),
        'anglers_rod': (ANGLERS_ROD, ANGLERS, LINE)}


def rod(name, cast):
    pattern, palette, line = RODS[name]
    layers = [(pattern, palette, 0, 0)]
    if not cast:
        layers.append((HANGING_LINE, line, 0, 0))
    return sprite(*layers)


# -- items ------------------------------------------------------------------------------------------

ITEMS = {}


def item(name):
    def register(fn):
        ITEMS[name] = fn
        return fn
    return register


# Bait ---------------------------------------------------------------------------------------------

@item('bait_worms')
def _():
    worms = """
................
................
..........oo....
.........oPPo...
.........oPbo...
..ooo....oPpo...
.oPPPo..oPbo....
oPpbpPo.oPpo....
oPo.oPpopPbo....
obo..oPbPpo.....
.o....oppo......
................
................
................
................
................
"""
    soil = """
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
...kkkk..kkkk...
..kDcDDkkDDcDk..
.kDdDDdDDdDDdDk.
.kdDsDdDdDsDddk.
..kssdsddsdsdk..
...kkkkkkkkkk...
"""
    front = """
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
....ob..........
...oPo..........
................
................
................
"""
    worm = {'o': '4A2420', 'P': 'E89A8E', 'p': 'C46E64', 'b': '9A4A44'}
    dirt = {'k': '24160C', 'D': '6A4A2C', 'd': '4E3420', 's': '3A2618', 'c': '8E6E48'}
    return sprite((soil, dirt, 0, 0), (worms, worm, 0, 0), (front, worm, 0, 0))


@item('chum')
def _():
    return sprite(("""
................
.....kkkkkk.....
....k......k....
...k..ooo...k...
..k..oTTo....k..
..k...oto....k..
.oooooooooooooo.
oSRrRsSoRrSRWRro
oHhhhhhhhhhhhmbo
.oIiiiiiiiiiijo.
.oHhhHhhHhhHmbo.
.oHhhHhhHhhHmbo.
.oIiiiiiiiiiijo.
..oHhHhhHhHmbo..
..ooooooooooooo.
................
""", {'k': '3E3A34', 'o': '2E1C10', 'T': 'C4D0D4', 't': '7E929C',
      'S': 'D8E0E4', 's': '8E9CA4', 'R': 'E07868', 'r': 'A84A40', 'W': 'F4EEDA',
      'H': 'B8844E', 'h': '9A6A3A', 'm': '7A5028', 'b': '5A3A1C',
      'I': 'A8AEB2', 'i': '7E868A', 'j': '4E5458'}, 0, 0))


@item('glow_bait')
def _():
    hook = """
................
........kkk.....
........k.k.....
........kik.....
.........ik.....
.........ik.....
.........ik.....
.........ik.....
.........ik.....
.........ik.....
.........ik.....
...k.....ik.....
..kik....ik.....
..kIik..kIk.....
...kIiiiIk......
....kkkkk.......
"""
    paste = """
................
................
..y.............
.yWy.....oooo...
..y....ooYYYYo..
......oYWWYYyyo.
......oYWYYYyyo.
.....oYYYYYyyOo.
.....oYYYYyyOOo.
......oyyyyOOo..
.......oOOOOo...
........oooo....
.............y..
............yWy.
.............y..
................
"""
    return sprite((hook, {'k': '2E3A44', 'I': 'D8E0E4', 'i': '9AA8B0'}, 0, 0),
                  (paste, {'o': '6A2A08', 'W': 'FFFBD0', 'Y': 'FFD84A', 'y': 'F8A832', 'O': 'D8701C'}, 0, 0))


@item('legend_lure')
def _():
    # a gold minnow plug, chased with scales and set with a ruby eye, trailing a tuft of red, teal and
    # white feathers, one hook hanging from its belly
    feathers = """
................
............F...
...........FfT..
..........FfTtW.
..........fTtWw.
...........TtWwF
...........tWwFf
...........TwFfT
..........FTtWw.
..........FfTtW.
...........FfT..
............F...
................
................
................
................
"""
    lure = """
................
................
................
kk...ooooo......
k.kooYYYYyoo....
.koYGYYYyYyyo...
..oYRYyyzyyzzo..
..oYrYyzyyzzzo..
...ozyyyzyzzo...
....oozzzzoo....
......oooo......
.......k........
...k...ik.......
...ki..ik.......
....kiiik.......
.....kkk........
"""
    return sprite((feathers, {'F': 'C83030', 'f': '7E1A1A', 'T': '2EA090', 't': '1E6A62', 'W': 'F4F0E4', 'w': 'C8C0B0'}, 0, 0),
                  (lure, {'k': '2E3A44', 'i': 'C8D0D4', 'o': '5A3A08', 'Y': 'F8D868', 'G': 'FFF6C0', 'y': 'D8A830',
                          'z': '9A6A14', 'R': 'E83848', 'r': '8E1A26'}, 0, 0))


# Tackle -------------------------------------------------------------------------------------------

@item('cork_bobber')
def _():
    return sprite(("""
................
.......qq.......
.......QQq......
.......Qq.......
.....ooQqoo.....
....oRhRRRro....
...oRhhRRRrro...
...oRRRRRrrro...
...oRRRRrrrro...
...kWWWWWWwvk...
...kWWWWWwwvk...
....kWWWwwvk....
.....kWwwvk.....
......kwvk......
.......kk.......
................
""", {'q': '6A4A28', 'Q': 'C89A5E', 'o': '4A1410', 'R': 'E03A2E', 'r': 'A82220', 'h': 'FF8A70',
      'k': '5A5048', 'W': 'FFFFFF', 'w': 'E2DCD0', 'v': 'B4AA9C'}, 0, 0))


@item('lead_sinker')
def _():
    small = """
................
................
...oo...........
..o..o..........
...oo...........
...oo...........
..oHho..........
.oHhhmo.........
.oHhmmo.........
.ohhmdo.........
..oddo..........
...oo...........
................
................
................
................
"""
    big = """
................
................
................
.........oo.....
........o..o....
.........oo.....
.........oo.....
........oHho....
.......oWHhmo...
.......oHhhmo...
......oHHhhmmo..
......oHhhhmmo..
......ohhhmmdo..
.......ommddo...
........oooo....
................
"""
    lead = {'o': '24282C', 'W': 'DCE2E6', 'H': 'B8C0C6', 'h': '8C949C', 'm': '6A727A', 'd': '4E545C'}
    return sprite((small, merged(lead, H='A4ACB2', h='7E868E', m='5E666E', d='464C54'), 1, 0), (big, lead, 0, 0))


HOOK = """
................
.........oooo...
........oHhmmo..
........oho.mo..
........oHmmo...
.........oHmo...
.........oHmo...
...o.....oHmo...
..oHo....oHmo...
..oHmo...oHmo...
..oHoMo..oHmo...
..oHo.o..oHmo...
..oHho..oHhmo...
...oHhooHhmo....
....ohhhhmo.....
.....oooo.......
"""
STEEL = {'o': '1E2428', 'H': 'D8DEE2', 'h': 'A4AEB4', 'm': '6E787E', 'M': 'A4AEB4'}


@item('barbed_hook')
def _():
    return sprite((HOOK, STEEL, 0, 0))


@item('treasure_hook')
def _():
    # a horseshoe magnet over the hook, to pull up whatever glints on the bottom
    magnet = """
...oooo..oooo...
...oWSo..oWSo...
...oSso..oSso...
...oRro..oRro...
...oRro..oRro...
...oRRooooRro...
....oRRRRRro....
.....oooooo.....
"""
    hook = """
........oo......
.......oHmo.....
...o...oHmo.....
..oHo..oHmo.....
..oHmo.oHmo.....
..oHo.oHhmo.....
...oHhhhmo......
....ooooo.......
"""
    sparks = """
.k............k.
k..............k
"""
    return sprite((magnet, {'o': '3A1410', 'R': 'D83A30', 'r': '8E2020', 'W': 'FFFFFF', 'S': 'E0E6EA', 's': '9AA4AA'}, 0, 0),
                  (hook, STEEL, 0, 8), (sparks, {'k': '8EC8F0'}, 0, 1))


@item('spinner')
def _():
    # a willow-leaf blade on a clevis that spins round the wire, red and brass beads, a hook under them
    return sprite(("""
.........oo...k.
........oWHoww.k
.......oWHhmo.k.
......oWHhmo.w..
.....oHHhmo.w...
....oHhhmo.w....
....ohmmo.w.....
.....ooo.qRq....
........qRrq....
.......qbBq.....
......qbBq......
......kqq.......
.....ik.........
.k...ik.........
.kik.ik.........
..kiiik.........
""", {'o': '2E3A44', 'W': 'FFFFFF', 'H': 'DCE4E8', 'h': 'AEBAC2', 'm': '7E8C96', 'w': '6E787E',
      'k': '2E3A44', 'i': 'C8D0D4', 'q': '4A1410', 'R': 'E04A3A', 'r': 'A02A20', 'b': 'E8C060', 'B': 'A87A20'}, 0, 0))


# Other items --------------------------------------------------------------------------------------

@item('anglers_journal')
def _():
    # weathered blue-green leather, a fish pressed into the cover, brass-capped corners and spine bands
    return sprite(("""
................
..oooooooooooo..
.oDdLLLLLLLLLBo.
.oDdLlllllllldoP
.oBdLleeeellldop
.oDdLeEkEEeledop
.oDdLeEEEEEeEdop
.oDdLeEEEEeledop
.oBdLleeeellldop
.oDdLlllllllldop
.oDdLlllllllldop
.oDdlddddddddBop
.oooooooooooooPp
..ppppppppppppp.
...oooooooooooo.
................
""", {'o': '122626', 'L': '4E8A82', 'l': '3A706A', 'd': '2A5652', 'D': '1E403E',
      'E': '62A296', 'e': '24484A', 'k': '1A3432', 'B': 'D8B050', 'P': 'F4EAD0', 'p': 'C8B88E'}, 0, 0))


@item('message_in_a_bottle')
def _():
    return sprite(("""
............cCo.
...........cCLco
..........oocCo.
.........ohgoo..
........ohhgno..
......oohhgggno.
.....ohhhPpgno..
....ohhPPpprno..
...ohhPPpprgno..
..ohgPPpprgno...
..ohgPprggnno...
..ongrggnno.....
..onnggnno......
...onnnoo.......
....ooo.........
................
""", {'o': '2E5A50', 'n': '5E9488', 'g': '8EC0B0', 'h': 'D4F0E6',
      'c': '7C4930', 'C': 'BC7850', 'L': 'E3A07A',
      'P': 'F4EAD0', 'p': 'D2C094', 'r': 'C03A2E'}, 0, 0))


@item('grilled_fish')
def _():
    # a fillet off the grill, golden-brown, scored across by the bars and seared darker underneath,
    # with a wedge of lemon
    fillet = """
................
................
................
................
................
......oooo......
...oooHHHHoo....
..oHgHhhgHWHoo..
.oHghhhghhhgHHoo
.oghhhghhhghhmbo
.ohhhghhhghmbbo.
.ommgmmmgmbbo...
.obbbbbbbbo.....
..oooooooo......
................
................
"""
    lemon = """
.oooo.
oWwwwo
oYwwYo
.oYYo.
..oo..
"""
    return sprite((fillet, {'o': '4A2410', 'H': 'FCE6B8', 'W': 'FFF8E6', 'h': 'F0C888', 'm': 'D8963E', 'b': 'A85A20',
                            'g': '5E2E12'}, 0, 0),
                  (lemon, {'o': '6A5010', 'Y': 'F2C82A', 'W': 'FFFCD8', 'w': 'FAEC8A'}, 10, 11))


# -- the trophy mount ----------------------------------------------------------------------------------
# One 16x16 texture, laid out for vanilla's default UVs: the board's front (north face) fills u 2..13,
# v 3..12, the raised nameplate's front is painted where it sits on the board (u 5..10, v 10..11), the
# board's edges take rows 0 and 15 and columns 0 and 15, and the nameplate's edges rows 1 and 14 and
# columns 1 and 14. The middle of the board stays plain wood: the mounted fish is drawn there.

MOUNT = """
dddddddddddddddd
sggggnnnnnnggggs
sgggggggggggggga
sggoooooooooogga
sgoHHHHHHHHHHoga
sgoHpppppppphoga
sgoHpgggpppphoga
sgoHpppppppphoga
sgoHppppgggphoga
sgoHpppppppphoga
sNoHpBBBBBBphoNa
sNoHhbbbbbbhhoNa
sggoooooooooogga
sggggggggggggggs
sggggTTTTTTggggs
LLLLLLLLLLLLLLLL
"""
WALNUT = {'o': '3A2414', 'H': 'C89058', 'h': '6E4424', 'p': 'A06C3A', 'g': '94622F',
          'B': 'F2D27A', 'b': 'C0923A', 'T': 'F2D27A', 'N': 'C0923A', 'n': '8A6420',
          'L': 'B88048', 'd': '5A3A20', 's': '8A5A30', 'a': '7A4E28'}
# The nameplate: a bright top edge, an engraved line along its face, brass shadow under it.
NAMEPLATE = """
BBBBBB
bnnnnb
"""
BRASS = {'B': 'F2D27A', 'b': 'C0923A', 'n': '8A6420'}


def mount_texture():
    image = stamp(Image.new('RGBA', (16, 16), (0, 0, 0, 0)), MOUNT, WALNUT)
    return stamp(image, NAMEPLATE, BRASS, 5, 10)


def auto_uv(face, frm, to):
    """Vanilla's default UVs for a face of an element inside the block."""
    (x1, y1, z1), (x2, y2, z2) = frm, to
    return {'down': [x1, 16 - z2, x2, 16 - z1], 'up': [x1, z1, x2, z2],
            'north': [16 - x2, 16 - y2, 16 - x1, 16 - y1], 'south': [x1, 16 - y2, x2, 16 - y1],
            'west': [z1, 16 - y2, z2, 16 - y1], 'east': [16 - z2, 16 - y2, 16 - z1, 16 - y1]}[face]


def element(frm, to, cull=(), hidden=()):
    """A cuboid with vanilla's default UVs on every face but the hidden ones (faces pressed against
    another element); cull lists the faces on the block's edge that the wall behind can hide."""
    faces = {}
    for face in ('north', 'south', 'east', 'west', 'up', 'down'):
        if face in hidden:
            continue
        spec = {'uv': [c if c % 1 else int(c) for c in auto_uv(face, frm, to)], 'texture': '#board'}
        if face in cull:
            spec['cullface'] = face
        faces[face] = spec
    return {'from': list(frm), 'to': list(to), 'faces': faces}


def mount_model():
    """Facing north: the board hangs on the wall to the south (z 15..16), its front toward -z; a rounded
    12x10 board (the 1 px corners cut), centred on x and on y 8, with the nameplate raised half a texel."""
    return {
        'parent': 'minecraft:block/block',
        'textures': {'board': f'{NS}:block/trophy_mount', 'particle': f'{NS}:block/trophy_mount'},
        'elements': [
            element([2, 4, 15], [14, 12, 16], cull=('south',)),
            element([3, 12, 15], [13, 13, 16], cull=('south',), hidden=('down',)),
            element([3, 3, 15], [13, 4, 16], cull=('south',), hidden=('up',)),
            element([5, 4, 14.5], [11, 6, 15], hidden=('south',)),
        ],
    }


def mount_blockstate():
    return {'variants': {f'facing={f}': {'model': f'{NS}:block/trophy_mount', 'y': y}
                         for f, y in (('north', 0), ('east', 90), ('south', 180), ('west', 270))}}


@item('trophy_mount')
def _():
    # the plaque as it hangs, with a bass mounted on it so that it reads in the inventory
    bass = """
..kkkk....
.kGGGGk.kk
keGGgGGkGk
.kLLLLk.kk
..kkkk....
"""
    return sprite(("""
................
................
..oooooooooooo..
.oHHHHHHHHHHHHo.
.oHppppppppppho.
.oHppppppppppho.
.oHppppppppppho.
.oHppppppppppho.
.oHppppppppppho.
.oHppppppppppho.
.oHppBBBBBBppho.
.oHppbnnnnbppho.
.ohhhhhhhhhhhho.
..oooooooooooo..
................
................
""", merged(WALNUT, BRASS), 0, 0), (bass, {'k': '22301E', 'G': '6E9A4E', 'g': '4E7438', 'L': 'D8E0B0', 'e': 'F0F0E0'}, 3, 4))


# -- the minigame sprites -------------------------------------------------------------------------------

FRAME_SIZE = (40, 152)
WATER = (6, 6, 21, 145)       # x0, y0, x1, y1, inclusive: the water track (16x140)
PROGRESS = (28, 6, 33, 145)   # the progress channel (6x140)
TIMBER = {'o': '2A180C', 'H': 'C8955A', 'h': 'A8763E', 'm': '8A5C2C', 'd': '6A4220', 'g': '7A4E24',
          'n': '5A4A3A', 'N': 'D8C8A8'}
ROPE = {'R': 'E6CC8E', 'r': 'B89658', 'q': '7A5E30'}
WATER_BANDS = ['2F7C82', '2A7079', '25646F', '205865', '1B4C5A']
WATER_EDGE, WATER_LIGHT = '133E4A', '3E8E90'
GROOVE = {'k': '120C08', 'f': '1E1610', 'l': '3A2C1E'}


def wood_at(x, y, x0, y0, x1, y1, vertical):
    """A plank from x0..x1, y0..y1: lit along its top and left edges, shadowed along the bottom and
    right, with a few grain lines running along it."""
    if x == x0 or y == y0:
        return 'H'
    if x == x1 or y == y1:
        return 'd'
    along, across = (y, x - x0) if vertical else (x, y - y0)
    if (across * 7 + along // 9) % 5 == 0 and along % 9 < 6:
        return 'm'
    return 'h'


FISH_CARVING = """
...ggg....
.ggggggg.g
gHgggggggg
.ggggggg.g
...ggg....
"""
LASHING = """
qqqqqq
RRRRrq
rrrrqq
RRRRrq
rrrrqq
qqqqqq
"""
# Glints of light in the water, (x, y, length) from the track's top-left: dashes near the surface,
# fewer and shorter further down.
GLINTS = [(3, 4, 3), (10, 11, 2), (6, 20, 3), (12, 29, 2), (4, 39, 2), (9, 48, 2), (13, 59, 2), (5, 70, 2),
          (11, 83, 1), (7, 95, 2), (3, 108, 1), (12, 119, 1), (8, 131, 1)]


def frame_sprite():
    """The catch bar: three upright posts (left, middle, right) and two crossbars, outlined, nailed where
    they meet, with rope wound round the outer posts near each end and halfway down, a fish carved in
    the top bar over the water and the two channels cut through."""
    w, h = FRAME_SIZE
    image = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    bars = [(1, 1, w - 2, 5, False), (1, h - 6, w - 2, h - 2, False)]
    posts = [(1, 6, 5, h - 7, True), (22, 6, 27, h - 7, True), (34, 6, w - 2, h - 7, True)]
    for x in range(w):
        for y in range(h):
            if (x in (0, w - 1) and y in (0, 1, h - 2, h - 1)) or (y in (0, h - 1) and x in (1, w - 2)):
                continue  # rounded corners
            if x in (0, w - 1) or y in (0, h - 1):
                image.putpixel((x, y), rgba(TIMBER['o']))
                continue
            for x0, y0, x1, y1, vertical in bars + posts:
                if x0 <= x <= x1 and y0 <= y <= y1:
                    image.putpixel((x, y), rgba(TIMBER[wood_at(x, y, x0, y0, x1, y1, vertical)]))
    # A dark seam where each post meets the crossbars.
    for x0, y0, x1, y1, _ in posts:
        area(image, x0, y0, x1, y0, TIMBER['d'])
        area(image, x0, y1, x1, y1, TIMBER['g'])
    # The channels, each with a one-texel lip: shadowed above and to the left, lit below and to the right.
    for x0, y0, x1, y1 in (WATER, PROGRESS):
        area(image, x0 - 1, y0 - 1, x1 + 1, y0 - 1, TIMBER['o'])
        area(image, x0 - 1, y0 - 1, x0 - 1, y1 + 1, TIMBER['o'])
        area(image, x0, y1 + 1, x1 + 1, y1 + 1, TIMBER['H'])
        area(image, x1 + 1, y0, x1 + 1, y1 + 1, TIMBER['H'])
    x0, y0, x1, y1 = WATER
    for y in range(y0, y1 + 1):
        band = WATER_BANDS[min(len(WATER_BANDS) - 1, (y - y0) * len(WATER_BANDS) // (y1 - y0 + 1))]
        for x in range(x0, x1 + 1):
            image.putpixel((x, y), rgba(WATER_EDGE if x == x0 or y == y0 else band))
    for gx, gy, length in GLINTS:
        area(image, x0 + gx, y0 + gy, x0 + gx + length - 1, y0 + gy, WATER_LIGHT)
    x0, y0, x1, y1 = PROGRESS
    area(image, x0, y0, x1, y1, GROOVE['f'])
    area(image, x0, y0, x1, y0, GROOVE['k'])
    area(image, x0, y0, x0, y1, GROOVE['k'])
    stamp(image, FISH_CARVING, TIMBER, 9, 1)
    for x in (0, w - 6):
        for y in (8, h // 2 - 3, h - 14):
            stamp(image, LASHING, ROPE, x, y)
    # Nail heads where the posts meet the crossbars.
    for y in (2, h - 4):
        for x in (3, 24, 25, w - 4):
            stamp(image, 'N\nn', TIMBER, x, y)
    return image


ZONE = """
.BBBBBBBBBBBBBB.
BgggggggggggggGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BgfffffffffffgGB
BGGGGGGGGGGGGGGB
.BBBBBBBBBBBBBB.
"""
ZONE_COLORS = {'B': 'A8F27A', 'g': '78D45C', 'G': '58B048', 'f': '4C9E5A'}

BAR_FISH = """
................
................
.......oooo.....
......oFFffo....
....ooHHHHHHoo..
...oHHHHHHHHhhoo
..oHWkHHHHHhhhoF
.oHHkkHHHHhhhhfF
.oHHHHHHHhhhhoFf
..oSSSSSShhmmofF
...oSSSShmmmooFo
....ooommmoo..oo
......offo......
.......oo.......
................
................
"""
SILVER_FISH = {'o': '14243A', 'H': 'B8E0F0', 'h': '84B8D4', 'm': '5E8EB0', 'S': 'F2FAFC', 'W': 'FFFFFF',
               'k': '0A1018', 'F': '6EA8D0', 'f': '4A7EA8'}
GOLD_FISH = {'o': '4A2A06', 'H': 'FFE070', 'h': 'F0B830', 'm': 'C8861A', 'S': 'FFF6C8', 'W': 'FFFFFF',
             'k': '1A0E02', 'F': 'F8A828', 'f': 'C87418', 'C': 'FFF2A0', 'c': 'E83848'}
CROWN = """
....C.C.C.......
....CcCcC.......
....CCCCC.......
"""

TREASURE = """
..oooooooo..
.oHHHHHHhGo.
oGHhhhhhhhGo
oGhhhhhhhmGo
oGGGGGGGGGGo
oHhhhoYohhmo
oHhhhoyohmmo
oHhhhhohmmmo
oGhhhhhhmmGo
oGGGGGGGGGGo
.oooooooooo.
............
"""
CHEST = {'o': '3A2010', 'H': 'B8844A', 'h': '94622F', 'm': '6E4420', 'G': 'E8BC48', 'Y': 'FFF0A0', 'y': '8A6420'}


# -- the journal ----------------------------------------------------------------------------------------

BOOK = (280, 180)
LEFT_PAGE = (14, 14, 134, 166)     # x0, y0, x1, y1 inclusive: the left page's content area
RIGHT_PAGE = (146, 14, 266, 166)
GUTTER = (136, 144)
PAPER = {'p': 'E3D3AE', 'q': 'D9C7A1', 'r': 'C6B086', 's': 'A28C64', 'l': 'F5ECD3', 'i': '6E5A3E'}
LEATHER = {'o': '0E201E', 'L': '3E7470', 'l': '2E5E5A', 'd': '224A46', 'S': 'C9B07A', 'B': 'D8B050', 'b': '8A6A20'}
RIBBON = {'R': 'B8342A', 'r': '7E1E18'}
RULE_EVERY = 12


GUTTER_SHADE = {135: 'q', 136: 'r', 137: 'r', 138: 's', 141: 's', 142: 'r', 143: 'r', 144: 'q', 145: 'q'}


def page_color(x, y, left):
    """Parchment with faint flecks and ruled lines, darkening in steps (outside the content areas) where
    the page curves down into the gutter."""
    if x in GUTTER_SHADE:
        return PAPER[GUTTER_SHADE[x]]
    if (x * 37 + y * 101 + (x * y) % 13) % 61 == 0:
        return PAPER['q']
    x0, y0, x1, y1 = LEFT_PAGE if left else RIGHT_PAGE
    if x0 + 2 <= x <= x1 - 2 and y0 <= y <= y1 and (y - y0) % RULE_EVERY == RULE_EVERY - 1:
        return PAPER['q']  # a faint ruled line
    return PAPER['p']


CORNER = """
BBBBb
Bb...
Bb...
B....
b....
"""


def journal_texture():
    """The open journal: a stitched leather cover (six texels showing at the top, five down the sides),
    the edges of the page block along the sides and bottom, two pages meeting in a dark seam with a
    ribbon marker hanging out of it, brass caps on the corners."""
    image = Image.new('RGBA', (512, 256), (0, 0, 0, 0))
    w, h = BOOK
    for y in range(h):
        for x in range(w):
            a, b = min(x, w - 1 - x), min(y, h - 1 - y)
            if a + b < 3:
                continue
            d = min(a, b)
            if d == 0 or a + b == 3:
                value = LEATHER['o']
            elif d == 1:
                value = LEATHER['L'] if (y == b and y < h // 2) or (x == a and x < w // 2) else LEATHER['d']
            elif d == 2 and ((x if b <= a else y) % 4 in (1, 2)):
                value = LEATHER['S']
            elif (x * 13 + y * 7 + x * y) % 29 == 0:
                value = LEATHER['d']
            else:
                value = LEATHER['l']
            image.putpixel((x, y), rgba(value))
    # The block of pages: its edges show as fine lines down the sides and along the bottom.
    for y in range(5, 174):
        for x in range(5, 275):
            if y >= 170:
                value = 's' if y == 173 else ('r' if y % 2 else 'l')
            elif x <= 7 or x >= 272:
                value = 's' if x in (5, 274) else ('r' if x % 2 else 'l')
            else:
                continue
            image.putpixel((x, y), rgba(PAPER[value]))
    # The two open pages, a lit top edge and a shadowed bottom and outer edge on each.
    for left, (x0, x1) in ((True, (8, 140)), (False, (139, 271))):
        for y in range(6, 170):
            for x in range(x0, x1 + 1):
                image.putpixel((x, y), rgba(page_color(x, y, left)))
        area(image, x0, 6, x1, 6, PAPER['l'])
        area(image, x0, 169, x1, 169, PAPER['r'])
        area(image, x0 if left else x1, 6, x0 if left else x1, 169, PAPER['r'])
    area(image, 139, 5, 140, 170, PAPER['i'])
    for x, y, fx, fy in ((1, 1, False, False), (w - 6, 1, True, False), (1, h - 6, False, True), (w - 6, h - 6, True, True)):
        rows = rows_of(CORNER)
        rows = [r[::-1] for r in rows] if fx else rows
        rows = rows[::-1] if fy else rows
        stamp(image, rows, LEATHER, x, y)
    stamp(image, """
RR
Rr
Rr
Rr
Rr
Rr
Rr
Rr
Rr
Rr
Rr
R.
""", RIBBON, 139, 168)
    return image


SLOT = """
.oooooooooooooooooo.
oqqqqqqqqqqqqqqqqqqo
oq................lo
oq................lo
oq................lo
oq................lo
oq................lo
oq................lo
oq................lo
oq................lo
oq................lo
oq................lo
oq................lo
oq................lo
oq................lo
oq................lo
oq................lo
oq................lo
oqlllllllllllllllllo
.oooooooooooooooooo.
"""
INK = {'o': '5A4630', 'q': 'C6B086', 'l': 'F5ECD3', 'p': 'E8DABA'}
GILT = {'o': '8A5A12', 'q': 'F2C860', 'l': 'FFF2C0', 'p': 'F2E4BA'}


def slot_sprite(palette):
    image = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
    area(image, 1, 1, 18, 18, palette['p'])
    return stamp(image, SLOT, palette)


STAR = """
...o...
..oYo..
ooYWYoo
oYYYYyo
.oYyyo.
.oyooyo
.oo..oo
"""
STAR_GOLD = {'o': '6A4208', 'Y': 'F8D040', 'y': 'D89A20', 'W': 'FFF6C0'}
STAR_FAINT = {'o': 'B8A27A', 'Y': 'B8A27A', 'y': 'B8A27A', 'W': 'B8A27A'}


def star_sprite(filled):
    if filled:
        return sprite((STAR, STAR_GOLD, 0, 0), size=(7, 7))
    rows = rows_of(STAR)
    cells = {(x, y) for y, r in enumerate(rows) for x, ch in enumerate(r) if ch != '.'}
    image = Image.new('RGBA', (7, 7), (0, 0, 0, 0))
    for x, y in cells:
        if any((x + dx, y + dy) not in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            image.putpixel((x, y), rgba(STAR_FAINT['o']))
    return image


def gui_sprites():
    """Every GUI atlas sprite, by path under textures/gui/sprites/."""
    return {
        'fishing/minigame/frame': frame_sprite(),
        'fishing/minigame/zone': sprite((ZONE, ZONE_COLORS, 0, 0), size=(16, 24)),
        'fishing/minigame/fish': sprite((BAR_FISH, SILVER_FISH, 0, 0)),
        'fishing/minigame/fish_legendary': sprite((BAR_FISH, GOLD_FISH, 0, 0), (CROWN, GOLD_FISH, 0, 0)),
        'fishing/minigame/treasure': sprite((TREASURE, CHEST, 0, 0), size=(12, 12)),
        'fishing/journal/slot': slot_sprite(INK),
        'fishing/journal/slot_selected': slot_sprite(GILT),
        'fishing/journal/star': star_sprite(True),
        'fishing/journal/star_empty': star_sprite(False),
    }


SIZES = {'fishing/minigame/frame': FRAME_SIZE, 'fishing/minigame/zone': (16, 24), 'fishing/minigame/fish': (16, 16),
         'fishing/minigame/fish_legendary': (16, 16), 'fishing/minigame/treasure': (12, 12),
         'fishing/journal/slot': (20, 20), 'fishing/journal/slot_selected': (20, 20),
         'fishing/journal/star': (7, 7), 'fishing/journal/star_empty': (7, 7)}
ZONE_META = {'gui': {'scaling': {'type': 'nine_slice', 'width': 16, 'height': 24, 'border': 3}}}


# -- compiling --------------------------------------------------------------------------------------

def png(image):
    buffer = io.BytesIO()
    image.save(buffer, 'PNG')
    return buffer.getvalue()


def dump(data):
    return (json.dumps(data, indent=2) + '\n').encode()


def item_files(files, name, image):
    files[ASSETS / f'textures/item/{name}.png'] = png(image)
    files[ASSETS / f'models/item/{name}.json'] = dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': f'{NS}:item/{name}'}})
    files[ASSETS / f'items/{name}.json'] = dump({'model': {'type': 'minecraft:model', 'model': f'{NS}:item/{name}'}})


def outputs():
    """Every compiled file: path -> bytes."""
    files = {}
    for name in RODS:
        for cast, suffix in ((False, ''), (True, '_cast')):
            files[ASSETS / f'textures/item/{name}{suffix}.png'] = png(rod(name, cast))
            files[ASSETS / f'models/item/{name}{suffix}.json'] = dump(
                {'parent': 'minecraft:item/handheld_rod', 'textures': {'layer0': f'{NS}:item/{name}{suffix}'}})
        files[ASSETS / f'items/{name}.json'] = dump({'model': {
            'type': 'minecraft:condition', 'property': 'minecraft:fishing_rod/cast',
            'on_false': {'type': 'minecraft:model', 'model': f'{NS}:item/{name}'},
            'on_true': {'type': 'minecraft:model', 'model': f'{NS}:item/{name}_cast'}}})
    for name, fn in ITEMS.items():
        item_files(files, name, fn())
    files[ASSETS / 'textures/block/trophy_mount.png'] = png(mount_texture())
    files[ASSETS / 'models/block/trophy_mount.json'] = dump(mount_model())
    files[ASSETS / 'blockstates/trophy_mount.json'] = dump(mount_blockstate())
    for key, image in gui_sprites().items():
        files[ASSETS / f'textures/gui/sprites/{key}.png'] = png(image)
    files[ASSETS / 'textures/gui/sprites/fishing/minigame/zone.png.mcmeta'] = dump(ZONE_META)
    files[ASSETS / 'textures/gui/fishing/journal.png'] = png(journal_texture())
    return files


def write():
    files = outputs()
    for path, data in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(f'Fishing art: {len(RODS)} rods, {len(ITEMS)} items, the trophy mount and {len(gui_sprites()) + 1} GUI '
          f'textures ({len(files)} files).')


def contract():
    """What the code and Minecraft rely on: sizes, hard alpha, the minigame's open channels and the
    journal's plain page areas."""
    found = []
    images = {p.relative_to(ASSETS).as_posix(): Image.open(io.BytesIO(d)).convert('RGBA')
              for p, d in outputs().items() if p.suffix == '.png'}
    for path, image in images.items():
        if any(a not in (0, 255) for a in image.getchannel('A').getdata()):
            found.append(f'{path}: alpha other than 0 and 255')
        if path.startswith('textures/item/') or path.startswith('textures/block/'):
            if image.size != (16, 16):
                found.append(f'{path}: {image.size}, not 16x16')
    for key, size in SIZES.items():
        image = images.get(f'textures/gui/sprites/{key}.png')
        if image is None or image.size != size:
            found.append(f'{key}: {image.size if image else "missing"}, not {size[0]}x{size[1]}')
    frame = images['textures/gui/sprites/fishing/minigame/frame.png']
    for name, (x0, y0, x1, y1) in (('water track', WATER), ('progress channel', PROGRESS)):
        if any(frame.getpixel((x, y))[3] != 255 for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)):
            found.append(f'frame: the {name} is not fully painted')
    if image_has(images['textures/gui/sprites/fishing/minigame/frame.png'], lambda p: p[3] == 0, (2, 2, 37, 149)):
        found.append('frame: holes inside the frame')
    journal = images['textures/gui/fishing/journal.png']
    if journal.size != (512, 256):
        found.append(f'journal: {journal.size}, not 512x256')
    if image_has(journal, lambda p: p[3] != 0, (BOOK[0], 0, 511, 255)) or image_has(journal, lambda p: p[3] != 0, (0, BOOK[1], 511, 255)):
        found.append('journal: paint outside the top-left 280x180')
    parchment = {rgba(PAPER[k]) for k in 'pq'}
    for x0, y0, x1, y1 in (LEFT_PAGE, RIGHT_PAGE):
        if image_has(journal, lambda p: p not in parchment, (x0, y0, x1, y1)):
            found.append(f'journal: the page area {x0},{y0}..{x1},{y1} is not plain parchment')
    return found


def image_has(image, test, box):
    x0, y0, x1, y1 = box
    return any(test(image.getpixel((x, y))) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))


def check():
    def same(path, data):
        # Git may check text files out with CRLF line endings; compare them line by line.
        if not path.exists():
            return False
        current = path.read_bytes()
        return current == data if path.suffix == '.png' else current.replace(b'\r\n', b'\n') == data
    problems = [f'out of date: {p.relative_to(PROJECT)}' for p, data in outputs().items() if not same(p, data)]
    problems += contract()
    if problems:
        print('Run tools/fishing/art.py:\n  ' + '\n  '.join(problems))
        sys.exit(1)
    print('Fishing art is up to date.')


# -- previews ---------------------------------------------------------------------------------------

def client_jar():
    jars = sorted(Path.home().glob('.gradle/caches/fabric-loom/*/minecraft-client.jar'))
    return zipfile.ZipFile(jars[-1]) if jars else None


def vanilla(jar, path):
    if not jar:
        return None
    try:
        return Image.open(io.BytesIO(jar.read(f'assets/minecraft/textures/{path}.png'))).convert('RGBA')
    except KeyError:
        return None


def sheet(tiles, dest, columns=8, background='#8BA9C4'):
    """Each tile at 8x with 1x and 2x thumbnails under it, labelled."""
    big, pad, label, thumbs = 128, 14, 14, 40
    w, h = big + pad, label + big + thumbs + pad
    rows = (len(tiles) + columns - 1) // columns
    out = Image.new('RGB', (columns * w + pad, rows * h + pad), background)
    draw = ImageDraw.Draw(out)
    for n, (name, image) in enumerate(tiles):
        x, y = pad + (n % columns) * w, pad + (n // columns) * h
        draw.text((x, y), name[:22], fill='#14202C')
        scaled = image.resize((image.width * 8, image.height * 8), Image.NEAREST)
        out.paste(scaled, (x, y + label), scaled)
        out.paste(image, (x, y + label + big + 8), image)
        double = image.resize((image.width * 2, image.height * 2), Image.NEAREST)
        out.paste(double, (x + 28, y + label + big + 4), double)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest)
    print(dest)


def preview_items(jar):
    tiles = []
    for name in RODS:
        tiles += [(name, rod(name, False)), (f'{name}_cast', rod(name, True))]
    for path in ('item/fishing_rod', 'item/fishing_rod_cast'):
        image = vanilla(jar, path)
        if image:
            tiles.append((f'{path.split("/")[-1]} (vanilla)', image))
    tiles += [(name, fn()) for name, fn in ITEMS.items()]
    for path in ('item/cooked_cod', 'item/book', 'item/glow_berries', 'item/potion'):
        image = vanilla(jar, path)
        if image:
            tiles.append((f'{path.split("/")[-1]} (vanilla)', image))
    sheet(tiles, PROJECT / 'build/previews/fishing_art_items.png')


def preview_block(jar):
    """The plaque from the front and from the north-east, alone and hung on a wall with a fish in front."""
    import workstations as kit

    class Bag:
        def __init__(self, elements, textures):
            self.elements, self.textures = elements, textures
    model = mount_model()
    textures = {f'{NS}:block/trophy_mount': mount_texture()}
    wall = vanilla(jar, 'block/spruce_planks') or Image.new('RGBA', (16, 16), (110, 80, 50, 255))
    textures['minecraft:block/spruce_planks'] = wall.crop((0, 0, 16, 16))
    board = [dict(e, faces={f: dict(s, texture='#board') for f, s in e['faces'].items()}) for e in model['elements']]
    refs = {'board': f'{NS}:block/trophy_mount', 'wall': 'minecraft:block/spruce_planks'}
    wall_el = {'from': [-8, -4, 16], 'to': [24, 20, 17], 'faces': {'north': {'uv': [0, 0, 16, 16], 'texture': '#wall'}}}
    fish = vanilla(jar, 'item/cod') or ITEMS['grilled_fish']()  # stands in for the fish the game draws
    views = []
    for view in ((0, 0, -1), (1, .9, -1.15), (-1, .6, -1.2)):
        views.append(kit.render(Bag(board, refs), textures, scale=14, view=view))
        views.append(kit.render(Bag([wall_el] + board, refs), textures, scale=14, view=view))
    front = views[1].copy()
    cx, cy = front.width // 2, int(front.height * .58)
    big = fish.resize((14 * 10, 14 * 10), Image.NEAREST)
    front.alpha_composite(big, (cx - 70, cy - 70 - 14))
    views.append(front)
    tile = 300
    out = Image.new('RGB', (tile * 4, tile * 2 + 40), '#7FA7C9')
    draw = ImageDraw.Draw(out)
    for n, view in enumerate(views + [mount_texture(), ITEMS['trophy_mount']()]):
        box = view.getbbox() or (0, 0, view.width, view.height)
        crop = view.crop(box)
        k = min((tile - 30) / crop.width, (tile - 30) / crop.height)
        k = max(1, int(k)) if view.width <= 16 else k
        crop = crop.resize((max(1, int(crop.width * k)), max(1, int(crop.height * k))), Image.NEAREST)
        x, y = (n % 4) * tile + 15, (n // 4) * (tile + 20) + 30
        out.paste(crop, (x, y), crop)
    draw.text((8, 6), 'trophy_mount: front, front on a wall, north-east, on a wall, south-west, on a wall; '
                      'with a fish drawn in front; the block texture; the item', fill='#10202E')
    dest = PROJECT / 'build/previews/fishing_art_block.png'
    out.save(dest)
    print(dest)


def minigame_composite():
    """The frame with what the game draws over it: the zone part-way up, the fish, the treasure and a
    part-filled progress bar."""
    sprites = gui_sprites()
    image = sprites['fishing/minigame/frame'].copy()
    zone = sprites['fishing/minigame/zone']
    tall = Image.new('RGBA', (16, 36), (0, 0, 0, 0))  # the zone nine-sliced to 36 tall
    tall.paste(zone.crop((0, 0, 16, 3)), (0, 0))
    for y in range(3, 33):
        tall.paste(zone.crop((0, 3 + (y - 3) % 18, 16, 4 + (y - 3) % 18)), (0, y))
    tall.paste(zone.crop((0, 21, 16, 24)), (0, 33))
    image.alpha_composite(tall, (6, 80))
    image.alpha_composite(sprites['fishing/minigame/fish'], (6, 88))
    image.alpha_composite(sprites['fishing/minigame/treasure'], (8, 30))
    area(image, 28, 90, 33, 145, 'E8A030')
    area(image, 28, 90, 33, 90, 'FFD070')
    legend = sprites['fishing/minigame/frame'].copy()
    legend.alpha_composite(tall, (6, 40))
    legend.alpha_composite(sprites['fishing/minigame/fish_legendary'], (6, 60))
    area(legend, 28, 120, 33, 145, '58C050')
    return image, legend


def journal_composite(jar):
    """The journal with slots, a selected slot, stars and fish in them, as the screen might lay it out."""
    sprites = gui_sprites()
    image = journal_texture().crop((0, 0, *BOOK))
    fish = [vanilla(jar, f'item/{n}') for n in ('cod', 'salmon', 'tropical_fish', 'pufferfish')]
    for n in range(20):
        x, y = LEFT_PAGE[0] + 2 + (n % 5) * 24, LEFT_PAGE[1] + 16 + (n // 5) * 24
        image.alpha_composite(sprites['fishing/journal/slot_selected' if n == 6 else 'fishing/journal/slot'], (x, y))
        f = fish[n % 4] if n < 9 else None
        if f:
            image.alpha_composite(f.crop((0, 0, 16, 16)), (x + 2, y + 2))
    for n in range(5):
        image.alpha_composite(sprites['fishing/journal/star' if n < 3 else 'fishing/journal/star_empty'],
                              (RIGHT_PAGE[0] + 4 + n * 9, RIGHT_PAGE[1] + 40))
    big = fish[1]
    if big:
        big = big.crop((0, 0, 16, 16)).resize((48, 48), Image.NEAREST)
        image.alpha_composite(big, (RIGHT_PAGE[0] + 36, RIGHT_PAGE[1] + 60))
    draw = ImageDraw.Draw(image)
    draw.text((RIGHT_PAGE[0] + 4, RIGHT_PAGE[1] + 4), 'Salmon', fill='#3F2F1E')
    draw.text((RIGHT_PAGE[0] + 4, RIGHT_PAGE[1] + 120), 'Caught 3, best 64 cm', fill='#3F2F1E')
    draw.text((LEFT_PAGE[0] + 2, LEFT_PAGE[1] + 2), 'Angler\'s Journal', fill='#3F2F1E')
    return image


def preview_gui(jar):
    sprites = gui_sprites()
    game, legend = minigame_composite()
    book = journal_composite(jar)
    pad = 16
    width = max(book.width * 2 + 4 * FRAME_SIZE[0] * 2 + 6 * pad, sum(s.width * 8 + pad for k, s in sprites.items() if 'frame' not in k) + pad)
    height = book.height * 2 + 2 * pad + 200 + book.height + pad
    out = Image.new('RGB', (width, height), '#2B3440')
    x = pad
    for image in (sprites['fishing/minigame/frame'], game, legend):
        big = image.resize((image.width * 2, image.height * 2), Image.NEAREST)
        out.paste(big, (x, pad), big)
        x += big.width + pad
    big = book.resize((book.width * 2, book.height * 2), Image.NEAREST)
    out.paste(big, (x, pad), big)
    y = pad + max(book.height * 2, FRAME_SIZE[1] * 2) + pad
    x = pad
    for image in (game, legend):
        out.paste(image, (x, y), image)
        x += image.width + pad
    out.paste(book, (x, y), book)
    x += book.width + pad
    draw = ImageDraw.Draw(out)
    for key, image in sprites.items():
        if 'frame' in key:
            continue
        big = image.resize((image.width * 8, image.height * 8), Image.NEAREST)
        if x + big.width > width:
            x, y = pad, y + book.height + pad
        back = Image.new('RGB', big.size, '#' + (PAPER['p'] if 'journal' in key else WATER_BANDS[2]))
        out.paste(back, (x, y + 14))
        out.paste(big, (x, y + 14), big)
        draw.text((x, y), key.split('/')[-1], fill='#E0E6EE')
        x += big.width + pad
    dest = PROJECT / 'build/previews/fishing_art_gui.png'
    out.save(dest)
    print(dest)


def preview():
    jar = client_jar()
    preview_items(jar)
    preview_block(jar)
    preview_gui(jar)


if __name__ == '__main__':
    if '--check' in sys.argv:
        check()
    elif '--preview' in sys.argv:
        preview()
    else:
        write()
