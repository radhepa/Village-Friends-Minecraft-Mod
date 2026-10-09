"""Authored 16px sprites for Hearth & Harvest, in the style of tools/item_sprites.py and tools/tavern/sprites.py:
native pixel patterns, a dark outline per material, stepped palettes, light from the top left and no
antialiasing. Sixty-odd dishes cannot each be drawn from scratch and still look like one kitchen, so they
are built from a few templates (bowl, pie dish, raised pie, cob loaf, tart, cake, slice, jar, platter, board,
trencher) with lettered fill regions: a dish names its template, a palette and the pixels of the region
that shows what is inside (a stew's surface, a pie's lid, a jar's contents), then lays any extras on top.

Also draws the crops: each produce item, its seeds and four growth stages per crop for the vanilla
`minecraft:block/crop` model (transparent, rooted on the bottom row, no outlines, like vanilla carrots).

    python tools/hearth/sprites.py            # write textures, models/item and items/ for every id in the tables
    python tools/hearth/sprites.py --check    # verify the files match the patterns and every id has a sprite
    python tools/hearth/sprites.py --preview  # build/previews/hearth_items.png and hearth_crops.png, 8x

Never hand-edit the PNG or JSON; change the patterns here and rerun.
"""
import io
import json
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from item_sprites import BREAD, SOUP, WHEAT  # noqa: E402
from tavern import sprites as tavern  # noqa: E402

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
ASSETS = PROJECT / 'src/main/resources/assets/villagefriends'
NS = 'villagefriends'


# -- drawing ----------------------------------------------------------------------------------------

def rgba(color):
    return tuple(bytes.fromhex(color)) + (255,)


def rows_of(pattern):
    return pattern.strip('\n').split('\n') if isinstance(pattern, str) else list(pattern)


def paint(image, pattern, palette, x=0, y=0):
    """Draws a pattern onto the image at x, y; '.' and ' ' are transparent."""
    for j, row in enumerate(rows_of(pattern)):
        for i, ch in enumerate(row):
            if ch not in '. ':
                assert 0 <= x + i < 16 and 0 <= y + j < 16, (x + i, y + j, row)
                image.putpixel((x + i, y + j), rgba(palette[ch]))
    return image


def region(template, key):
    """The bounding box (x, y, w, h) of a template's fill region."""
    cells = [(i, j) for j, row in enumerate(rows_of(template)) for i, ch in enumerate(row) if ch == key]
    xs, ys = [c[0] for c in cells], [c[1] for c in cells]
    return min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1


def fill(image, template, key, spec, palette):
    """Paints spec (rows the size of the region's bounding box) wherever the template has `key`."""
    x0, y0, w, h = region(template, key)
    mask = rows_of(template)
    spec = rows_of(spec)
    assert len(spec) == h and all(len(r) == w for r in spec), (key, w, h, spec)
    for j, row in enumerate(spec):
        for i, ch in enumerate(row):
            if mask[y0 + j][x0 + i] == key:
                assert ch not in '. ', (key, i, j, spec)
                image.putpixel((x0 + i, y0 + j), rgba(palette[ch]))
    return image


def compose(*steps):
    """Each step is (pattern, palette, x, y) or a callable(image); drawn back to front."""
    image = Image.new('RGBA', (16, 16))
    for step in steps:
        if callable(step):
            step(image)
        else:
            paint(image, *step)
    return image


def merged(*palettes, **extra):
    out = {}
    for p in palettes:
        out.update(p)
    out.update(extra)
    return out


# -- shared food colours ----------------------------------------------------------------------------
# One letter per ingredient so a dish's fill pattern reads like its recipe ('c' is always carrot).
# Each dish adds its own base letters (a broth, A highlight, q shadow; or a filling) on top.

FOOD = {
    'c': 'E8862A', 'C': 'F6AE52',            # carrot
    'l': '5E9434', 'L': '9CC45A',            # leek greens
    'w': 'EEE6C6', 'W': 'FFFBEA',            # onion, leek white, garlic, fish flesh
    'g': '386E28', 'G': '5E9C3A',            # herbs
    'm': '7A4026', 'M': 'A2603A', 'n': '4E2616',  # cooked meat
    'p': 'E2C46A', 'P': 'F4E0A0',            # potato
    'r': 'A8283A', 'R': 'D84850',            # beet, apple skin, berry red
    'u': '7E5234', 'U': 'D8C29E',            # mushroom cap, mushroom flesh
    'x': 'E8D498', 'X': 'B89C5E',            # barley and wheat grains
    'k': 'B4D282', 'K': '78A44C',            # cabbage
    'y': 'F0C43C', 'Y': 'FBE48A',            # egg yolk, cheese
    'h': 'E0961C', 'H': 'F8C44A',            # honey
    'v': '7E4E8E', 'V': 'B48CC4',            # garlic purple, sporecap
    'f': 'F0A07A', 'F': 'C86848',            # salmon and crab pink
    'z': 'FFFFFF',                           # sugar sparkle, cream
}


# -- bowls: a wooden bowl like hearty_stew, the stew surface is the S region -------------------------

BOWL = """
................
................
................
................
.....oooooo.....
...ooHHHHhhoo...
..oHSSSSSSSSho..
.oHSSSSSSSSSSho.
.oHSSSSSSSSSSmo.
.omHSSSSSSSShmo.
..omHHhhhhhmmo..
...ommmmmmmbo...
....obbbbbbo....
.....oooooo.....
................
................
"""
WOOD = merged(SOUP, S=SOUP['b'])  # the existing hearty_stew bowl


def centred(spec, width):
    """Pads rows narrower than the region (an ellipse's short end rows) with '.' on both sides."""
    return [row.center(width, '.') if len(row) < width else row for row in rows_of(spec)]


def bowl(surface, broth, *over, under=()):
    """A bowl of stew. surface: 4 rows, 8/10/10/8 pixels wide; broth: the dish's own letters merged
    over FOOD (a broth, A highlight, q shadow); over: (pattern, palette, x, y) laid on top."""
    palette = merged(FOOD, broth)
    return compose(*under, (BOWL, WOOD, 0, 0),
                   lambda im: fill(im, BOWL, 'S', centred(surface, 10), palette), *over)


ITEMS = {}
CROPS = {}


def item(name):
    def register(fn):
        ITEMS[name] = fn
        return fn
    return register


# Things that stick out of a bowl

FISH_TAIL = """
.o...o
oTo.oTo
oTtotTo
.oTtTo.
..oTo..
..oto..
"""
SILVER = {'o': '2E3A44', 'T': 'C4D0D4', 't': '7E929C'}
SPOON = """
....oo
...oHo
..oHo.
.oho..
oho...
.o....
"""
SPOONWOOD = {'o': '4A301C', 'H': 'DDB680', 'h': 'B08250'}
STEAM = """
.s...s.
..S.S..
.S...S.
..s.s..
"""
STEAM_PUFF = {'s': 'A4B1A9', 'S': 'E1E7D5'}  # the steam over the mug of cider
BONE = """
....oo.
...oWWo
...oWwo
..oWwo.
.oWwo..
oWwo...
"""
IVORY = {'o': '5A4A38', 'W': 'F4EEDA', 'w': 'C8BC9C'}


# Pottages and broths ---------------------------------------------------------------------------------


@item('onion_pottage')
def _():
    return bowl("""
qqqaaqqq
aaAAwwaxaa
aawwaaawaa
qqaagaqq
""", {'a': 'C98A30', 'A': 'E8B654', 'q': 'A2662A', 'w': 'F6E4AE'})


@item('green_pottage')
def _():
    return bowl("""
qqqaaqqq
aaAALaakaa
aaagawLaaa
qqagaaqq
""", {'a': '6E9A3C', 'A': '92BA58', 'q': '4E7A2C'})


@item('barley_porridge')
def _():
    return bowl("""
qqqxaqqq
aaAxaHhxaa
aaxhHhaXaa
qqaXaxqq
""", {'a': 'E6D8B0', 'A': 'F6EED6', 'q': 'C8B488'}, (SPOON, SPOONWOOD, 9, 1))


@item('leek_broth')
def _():
    return bowl("""
qqqaaqqq
aaAAaLwaaa
aaLwaaaxaa
qqaaLwqq
""", {'a': 'D2AE48', 'A': 'EACB70', 'q': 'A88630'})


@item('cabbage_soup')
def _():
    return bowl("""
qqqkkqqq
aaAkKacaaa
aakaakkcaa
qqacakqq
""", {'a': 'B8843E', 'A': 'D8A85A', 'q': '8E6028'})


@item('garlic_broth')
def _():
    return bowl("""
qqqaaqqq
aaAAWvagaa
aagaaaWWva
qqaWvaqq
""", {'a': 'D4BC6E', 'A': 'ECDA9C', 'q': 'B09A50'}, (STEAM, STEAM_PUFF, 4, 0))


@item('mushroom_pottage')
def _():
    return bowl("""
qqqaaqqq
aaAUUaRaaa
aaauaaUUaa
qqaRauqq
""", {'a': '6A4428', 'A': '8A5E38', 'q': '4E301C'})


@item('beet_pottage')
def _():
    return bowl("""
qqqaaqqq
aaAAaaxaaa
aaxaaaaxaa
qqaaxaqq
""", {'a': 'A82838', 'A': 'D04A5A', 'q': '7A1828'})


# Meat and fish stews ---------------------------------------------------------------------------------

@item('hare_stew')
def _():
    return bowl("""
qqqaaqqq
aaAAcaLMaa
aaMmaaacaa
qqaLcMqq
""", {'a': '9A4426', 'A': 'BA6038', 'q': '70301A'})


@item('beef_stew')
def _():
    return bowl("""
qqqaaqqq
aAMMmapPaa
apPaaMMmwa
qqawaMmq
""", {'a': '4E2A18', 'A': '6E3E24', 'q': '361C0C'})


@item('mutton_stew')
def _():
    return bowl("""
qqqaaqqq
aaAxaMmLaa
aaLlaxaxaa
qqaMmxqq
""", {'a': 'C4B48E', 'A': 'DCD0AE', 'q': 'A08E68'})


@item('chicken_pottage')
def _():
    return bowl("""
qqqaaqqq
aaAAeElaaa
aaLaaeEgaa
qqagaLqq
""", {'a': 'E8D490', 'A': 'F6E8B8', 'q': 'C4AC64', 'e': 'FFF6E0', 'E': 'C4A070'})


@item('pork_cabbage_stew')
def _():
    return bowl("""
qqqkkqqq
aaAeEakKaa
aakKaeEaaa
qqaeEkqq
""", {'a': 'B88A54', 'A': 'D4A86C', 'q': '946638', 'e': 'EEB0A4', 'E': 'C07870'})


@item('fishermans_stew')
def _():
    return bowl("""
qqqaaqqq
aaAWwapaaa
aapaaWwaaa
qqaWwaqq
""", {'a': 'D06A30', 'A': 'EC9050', 'q': 'A44A20'}, (FISH_TAIL, SILVER, 8, 1))


@item('fish_herb_soup')
def _():
    return bowl("""
qqqaaqqq
aaAWWaGgaa
aaggaaWWaa
qqaWwgqq
""", {'a': 'A8BE78', 'A': 'C8D898', 'q': '849A58'})


@item('hunters_stew')
def _():
    return bowl("""
qqqaaqqq
aaAMmaUuaa
aaUuaMmaaa
qqaMmaqq
""", {'a': '4E2A1C', 'A': '6E3E28', 'q': '361A10'}, (BONE, IVORY, 7, 2))


# Sweet, creamy and feast-day bowls -----------------------------------------------------------------

@item('frumenty')
def _():
    # medieval frumenty: saffron-yellow wheat in milk, with currants
    return bowl("""
qqqaaqqq
aaAxanaXaa
aaXanAaxaa
qqaXanqq
""", {'a': 'EEB032', 'A': 'FAD468', 'q': 'C48A20', 'n': '5A2A2E'})


@item('harvest_stew')
def _():
    return bowl("""
qqqaaqqq
aaAcaLwpaa
aawpacaLaa
qqaLvcqq
""", {'a': 'B8682C', 'A': 'D48A44', 'q': '8E4A1C'})


@item('stewed_apples')
def _():
    return bowl("""
qqqaaqqq
aaAaaaaaaa
aaaaaaaAaa
qqaaaaqq
""", {'a': 'D88A24', 'A': 'F0B040', 'q': 'A86018'}, (APPLES, STEWED, 3, 3))


@item('honey_posset')
def _():
    return bowl("""
qqqaaqqq
aaAhhhauaa
aahauHhaaa
qqahhaqq
""", {'a': 'F2EAD6', 'A': 'FFFCF0', 'q': 'D6CAAE', 'u': 'A8784C'})


@item('leek_cheese_soup')
def _():
    return bowl("""
qqqaaqqq
aaALwaYyaa
aaYaaLwAaa
qqaLwYqq
""", {'a': 'C8D08C', 'A': 'E0E6B0', 'q': 'A4AC68'})


# Heaped bowls and the Not-So-Vanilla Mobs stews ------------------------------------------------------

ROLLS = """
.oooo.oooo.
oKKkkoKKkko
okvkvokvkvo
.oooo.oooo.
...oooo....
..oKKkko...
..okvkvo...
...oooo....
"""
LEAFROLL = {'o': '2E4A1E', 'K': 'C4DE94', 'k': '8CB45A', 'v': '5E8A3A'}
SALAD = """
.....oo.....
...ooGGo.o..
..oGGgGooLo.
.oGgLLgGLLlo
oGgwwgGGgllo
.oggGggKKkgo
"""
CLAW = """
.oo....
oRRo...
oRro.o.
.oRooRo
.oRRRro
..oRrro
...oro.
"""
SHELL = {'o': '4A140C', 'R': 'E05838', 'r': 'A82A1C'}
CAP = """
..ooo..
.oVVzo.
oVzVVvo
ovvvvvo
.ooooo.
"""
APPLES = """
...ooo.....
..oRRPo.oo.
.oRrPPooRPo
.oopPoooRpo
oRPoooRrPpo
oRPpo.oooo.
.ooo.......
"""
STEWED = {'o': '5A2010', 'R': 'D84040', 'r': 'A02828', 'P': 'FBE7A6', 'p': 'E8C070'}


@item('cabbage_rolls')
def _():
    return bowl("""
qqqaaqqq
aaAaaaaaaa
aaaaaaaaaa
qqaaaaqq
""", {'a': 'B04028', 'A': 'D06040', 'q': '84281C'}, (ROLLS, LEAFROLL, 2, 3))


@item('herb_salad')
def _():
    return bowl("""
qqqGGqqq
GGGgGGgGGG
ggGGgGGggg
qqgGgGqq
""", {'q': '2E5A20'}, (SALAD, merged(FOOD, o='24461A'), 2, 2))


@item('boar_stew')
def _():
    return bowl("""
qqqaaqqq
axAMMnaxaa
aanMMaxMna
qqxaxaqq
""", {'a': '7E3222', 'A': 'A04A32', 'q': '561C14', 'M': '9A5A44', 'n': '3A1A10'})


@item('brineclaw_bisque')
def _():
    return bowl("""
qqqaaqqq
aaAAzaaWaa
aaaWaaAaaa
qqaazaqq
""", {'a': 'E88A60', 'A': 'F6B088', 'q': 'C86A44'}, (CLAW, SHELL, 8, 1))


@item('sporecap_pottage')
def _():
    return bowl("""
qqqaaqqq
aaAVzaxaaa
aaxaaVzgaa
qqagaxqq
""", {'a': '8A7A98', 'A': 'A898B4', 'q': '6A5A78', 'z': 'EDE4F2'}, (CAP, {'o': '4A3058', 'V': 'C4A0D4', 'v': '8E62A0', 'z': 'F4EEF6'}, 3, 3))


# -- jars and bottles: a linen-covered glass jar, the contents are the S region ---------------------

JAR = """
................
................
.....oooooo.....
....oLLLCCco....
....oLCCCccdo...
....ottttttto...
...odCcdcCcddo..
...onggggggnno..
..ohSSSSSSSSno..
..ohSSSSSSSSno..
..ohSSSSSSSSno..
..ohSSSSSSSSno..
..ohSSSSSSSSno..
..onSSSSSSSSgo..
...onnnnnnnno...
....oooooooo....
"""
JARGLASS = {'o': '3E5A6A', 'n': '749CAE', 'g': 'A7C8D5', 'h': 'D9EDF0', 'S': 'A7C8D5',
            'L': 'F6F0DE', 'C': 'E2D8C0', 'c': 'C4B898', 'd': '9A8E70', 't': 'A0522D'}


def jar(contents, colours, *over):
    """contents: 6 rows of 8, seen through the glass."""
    palette = merged(FOOD, colours)
    return compose((JAR, JARGLASS, 0, 0), lambda im: fill(im, JAR, 'S', contents, palette), *over)


@item('sauerkraut')
def _():
    return jar("""
AAkaaAkk
kaaAkkaa
aAkkaaAk
kkaaAkka
aaAkkaaK
KkkKaKKK
""", {'a': 'E0D27A', 'A': 'F4EAB0', 'k': 'C8B455', 'K': 'A89440'})


@item('pickled_onions')
def _():
    return jar("""
aWaaaWaa
WwqaWwqa
aqanaqaa
aaWaaaWa
aWwqaWwq
gaqaaaqa
""", {'a': 'A8763A', 'q': 'C8BC98', 'W': 'FFFBEA', 'w': 'EEE6CC', 'g': '6E8A3C', 'n': '2E2018'})


@item('mulled_cider')
def _():
    berries = """
.gg
oRo
oRro
.oo.
"""
    return compose((TONIC_BOTTLE, CIDERGLASS, 0, 0),
                   (berries, {'o': '4E1A14', 'R': 'D8443A', 'r': 'A52C27', 'g': '5E8A3A'}, 10, 3))


TONIC_BOTTLE = """
................
......cCCc......
......cLLc......
......ohgo......
.....tttttt.....
.....ohhgno.....
....ohhgggno....
...ohhSSssgno...
..ohhSSssddgno..
..ohSSssdddano..
..ohSssddadano..
..onssddaaaano..
...ogddaaagno...
....ongggnno....
.....oooooo.....
................
"""
CIDERGLASS = {'o': '466779', 'n': '749CAE', 'g': 'A7C8D5', 'h': 'D9EDF0', 'w': 'F4F5DF',
              'c': '7C4930', 'C': 'BC7850', 'L': 'E3A07A', 't': 'A0522D',
              'S': 'E8904A', 's': 'C8602E', 'd': '983624', 'a': '6E2418'}


# -- breads: a round cob (X is the score in its crust) and the village loaf ------------------------

COB = """
................
................
................
................
......oooo......
....ooHHhhoo....
...oHHhhhhhmo...
..oHHhhXhhhmmo..
..oHhhXXXhhmmo..
.oHhhhhXhhhmmbo.
.oHhhhhhhhmmmbo.
.ohhhhhhhmmmbbo.
.ommhhhmmmmbbbo.
..obbmmmmbbbbo..
...oooooooooo...
................
"""


def cob(crust, *over):
    """crust: o outline, H h m b light to dark, X the score."""
    return compose((COB, crust, 0, 0), *over)


@item('barley_loaf')
def _():
    bran = """
...xX.....
.........X
xX......x.
.......x..
..X.......
....xX....
"""
    return cob({'o': '35200F', 'H': '9E6E3A', 'h': '84562C', 'm': '6A4222', 'b': '4C2E16', 'X': 'C8A878'},
               (bran, {'x': 'A88A5A', 'X': 'C8A878'}, 2, 6))


@item('wastel')
def _():
    flour = """
..zz..
.z..z.
z.zz.z
.z..z.
"""
    return cob({'o': '6A4A20', 'H': 'F6E4B0', 'h': 'E8C886', 'm': 'CCA25E', 'b': 'A07838', 'X': 'FFF6DA'},
               (flour, {'z': 'FFFDF4'}, 4, 5))


@item('honey_loaf')
def _():
    glaze = """
....zGGg...
..GzGGGGgg.
.GGGg.gGGgg
gGg.....gGg
gg.......gg
g..........g
...........g
"""
    return cob({'o': '4A2A10', 'H': 'C88A40', 'h': 'A86A2C', 'm': '88501E', 'b': '683A14', 'X': 'F0C870'},
               (glaze, {'G': 'F8C83A', 'g': 'E0961C', 'z': 'FFF4C0'}, 2, 5))


@item('herb_bread')
def _():
    flecks = """
.....g..
...G....
.....g.G
..g.....
....G...
.g......
...g....
"""
    return compose((BREAD, merged(WHEAT, H='E2BC60', h='CCA048'), 0, 0), (flecks, FOOD, 2, 3))


# -- trenchers: a thick slice of coarse bread, crumb (T) up, eaten plate and all --------------------

TRENCHER = """
................
................
................
................
................
................
...oooooooooo...
..oCCCCCCCCCCo..
.oCTTTTTTTTTTmo.
oCTTTTTTTTTTTTmo
oCTTTTTTTTTTTTmo
omCTTTTTTTTTTmbo
ommmmmmmmmmmmmbo
ohhhhhhhhhhhhbbo
.obbbbbbbbbbbbo.
..oooooooooooo..
"""
RYE = {'o': '3A2412', 'C': 'B07C46', 'm': '84582C', 'b': '5A3818', 'h': '946232', 'T': 'C8A070'}
CRUMB = {'a': 'CCA676', 'A': 'E0C494', 'q': 'A8804C', 'x': '8A6438'}
TRENCHER_TOP = """
AaqaAaaxaA
AaxaaqaAaaqa
aqaAaaxaqaAa
aAaqaaAaxa
"""


def trencher(*over):
    return compose((TRENCHER, RYE, 0, 0), lambda im: fill(im, TRENCHER, 'T', centred(TRENCHER_TOP, 12), CRUMB), *over)


@item('trencher')
def _():
    return trencher()


@item('trencher_roast')
def _():
    beef = """
...nnnn.......
..nMMMMn.nnnn.
.nMMMMMMnMMMMn
.nMmmMMnMMMMMn
nwwnmmnMMmmMn.
nWwn.nnmmMMn..
.nn....nnnn...
"""
    return trencher((beef, {'n': '4A1E12', 'M': 'C4705C', 'm': '9A4E3C', 'w': 'E8DAB0', 'W': 'FFF6DA'}, 1, 4))


@item('trencher_cheese')
def _():
    cheese = """
....oooo....
..ooWWWwoo..
.oWWWwwWWwo.
oWWgwwwwGwwo
oWwwwGwwwwgo
.oowwwwgwoo.
"""
    return trencher((cheese, merged(FOOD, o='9A9070', W='FFFDF0', w='EEE8D0'), 2, 4))


@item('trencher_mushroom')
def _():
    shrooms = """
...........
.ooo...ooo.
oUUuo.oUUuo
ouuuoyouuuo
.oso.yyoso.
yyoooUuoyy.
.oUUuuuuo..
.ouuuuuuo..
..oosso....
"""
    return trencher((shrooms, merged(FOOD, o='3E2414', U='B07A4E', u='7E5034', s='E8DCC0', y='F4D468'), 2, 3))


# -- pies: shepherds_pie's earthenware dish with a crimped pastry lid (the S region) ----------------

PIE = """
................
................
................
................
.....oooooo.....
...ooSSSSSSoo...
..oSSSSSSSSSSo..
.oSSSSSSSSSSSSo.
.oSSSSSSSSSSSSo.
oCcSSSSSSSSSScdo
oCcCcCcCcCcCcdco
oTTTTTTtttttttqo
.oKKKkkkkkkkkqo.
..oKKkkkkkkqqo..
...oooooooooo...
................
"""
DISH = {'o': '3E2214', 'T': 'DC8A5C', 't': 'B9653E', 'K': 'A9542F', 'k': '8C4325', 'q': '66301A', 'S': 'E9BC68'}
GOLDEN = {'o': '5A3418', 'L': 'F3D58C', 'C': 'E9BC68', 'c': 'C98F3D', 'd': '9A6128'}
LID = """
LLLCCC
LLLCCCCCcc
LLCCCCCCCccc
LCCCCCCCcccd
cCCCCcccdd
"""


def pie(*over, lid=LID, crust=GOLDEN, filling=None):
    """A pie in its dish. lid: 5 rows (6/10/12/12/10 wide) over the pastry palette plus FOOD."""
    palette = merged(FOOD, crust, filling or {})
    return compose((PIE, merged(DISH, {k: v for k, v in crust.items() if k in 'Ccd'}), 0, 0),
                   lambda im: fill(im, PIE, 'S', centred(lid, 12), palette), *over)


@item('leek_pie')
def _():
    slits = """
...oL....
..oLl.oL.
..ol.oLl.
....ol...
"""
    return pie((slits, merged(GOLDEN, FOOD, o='6A4A1C'), 3, 5))


@item('chicken_pie')
def _():
    decor = """
.cc......cc.
cLLc.oo.cLLc
.cc.owwo.cc.
.....oo.....
"""
    return pie((decor, merged(GOLDEN, c='B07830', L='FBE6B4', w='F4E6C0', o='5A3418'), 2, 5))


@item('steak_pie')
def _():
    # a pie bird: the blackbird funnel that lets the steam out
    bird = """
.oo...
oBBo..
oBeyy.
.oBo..
oBBBo.
oBBBBo
"""
    return pie((bird, {'o': '141418', 'B': '2E2E36', 'e': 'FFFFFF', 'y': 'F0B030'}, 5, 2),
               crust={'o': '4A2810', 'L': 'D89848', 'C': 'B87430', 'c': '945A24', 'd': '6E401A'})


@item('fish_pie')
def _():
    return pie((FISH_TAIL, SILVER, 9, 2), lid="""
YYybYy
YYyyYybyyy
YybyyYyyybyy
yyyYybyyyyBy
yByyybyyBy
""", filling={'y': 'F0C43C', 'Y': 'FBE48A', 'b': 'C88A30', 'B': '9E6420'})


@item('apple_pie')
def _():
    crust = merged(GOLDEN, L='F0C878', C='DDA552', c='BA7E34', d='8E5A22')
    dome = """
...oooooo...
.ooLLLCCCoo.
oLLLCCCCCCco
"""
    slits = """
oo..oo..oo
PP..PP..PP
"""
    return pie((dome, crust, 2, 3), (slits, merged(crust, P='FBE7A6', o='7A4A18'), 3, 6), crust=crust, lid="""
LLCCCC
LLLCCCCCcc
LLCCCCCCCccc
LCCCCCCCcccd
cCCCCcccdd
""")


@item('berry_pie')
def _():
    return pie(lid="""
LvLrLv
vLvrLvrLrv
LrLvLrLvLrLv
vLvrLvrLrLvd
rLrvLrcLvd
""", filling={'v': '5A2A6A', 'r': '8A3A86'})


# -- raised pies (hot-water crust, no dish) and the pasty --------------------------------------------

RAISED = """
................
................
................
................
.....oooooo.....
...ooLLCCCCoo...
..oLLCCooCCcco..
..oCCCofoCccdo..
..oCcCcCcCcCdo..
..oHhHhHhmhmbo..
..oHhHhHhmhmbo..
..oHhHhHhmhmbo..
..oHhHhHmhmmbo..
...obbbbbbbbo...
....oooooooo....
................
"""
HALF = """
................
................
................
................
................
.....oooooo.....
...ooLLCCCCoo...
..oLLCCCCCCcco..
..oCcCcCcCcCdo..
..oddddddddddo..
..odFFFFFFFFdo..
..odFFFFFFFFdo..
..odFFFFFFFFdo..
..odFFFFFFFFdo..
..oddddddddddo..
...oooooooooo...
"""
HOTWATER = {'o': '4A2A10', 'L': 'F6DCA0', 'C': 'E8B868', 'c': 'C88E3C', 'd': 'A06A28', 'f': '5A2C18',
            'H': 'E8B060', 'h': 'D0943E', 'm': 'B07430', 'b': '86541E', 'F': 'D0943E'}


@item('mutton_pie')
def _():
    leaves = """
.cc....cc.
cLLc..cLLc
.cc....cc.
"""
    return compose((RAISED, HOTWATER, 0, 0), (leaves, merged(HOTWATER, L='FBE6B4', c='A86E2C'), 3, 5))


@item('pork_pie')
def _():
    # cut through, the way pork pies are sold: pink meat, a ring of jelly under the lid
    face = """
yyyyyyyy
PPpPPPPP
PPPPPpPP
PpPPPPpP
"""
    return compose((HALF, merged(HOTWATER, d='DCA458'), 0, 0),
                   lambda im: fill(im, HALF, 'F', face, {'y': 'F2D27A', 'P': 'E8A49A', 'p': 'C8786E'}))


PASTY = """
................
................
................
................
................
................
......oooo......
....ooCcCcoo....
...oCcCcCcCco...
..oHHhhhhhhhmo..
.oHHhhhhhhhhmmo.
.oHhhhhhhhhhmmbo
.ohhhhhhhhhmmmbo
..ommmmmmmmmbbo.
...oooooooooo...
................
"""


@item('pasty')
def _():
    return compose((PASTY, {'o': '4A2A10', 'C': 'F6DCA0', 'c': 'C88E3C', 'H': 'F0C878', 'h': 'DDA552',
                            'm': 'BA7E34', 'b': '8E5A22'}, 0, 0))


# -- tarts and cakes: apple_tart's open shell, a whole round cake, a wedge slice --------------------

TART = """
................
................
................
................
.....oooooo.....
...ooCcCcCcoo...
..oCSSSSSSSSCo..
.oCcSSSSSSSScdo.
.oCcSSSSSSSScdo.
..oCcCcCcCcdco..
..ocdcdcdcdcdo..
...oddddddddo...
....oooooooo....
................
................
................
"""
SHELL_PASTRY = {'o': '5A3418', 'C': 'E9BC68', 'c': 'C98F3D', 'd': '9A6128', 'S': 'E9BC68'}  # apple_tart's


def tart(filling, colours, *over):
    """filling: 3 rows of 8 inside the crust."""
    return compose((TART, SHELL_PASTRY, 0, 0), lambda im: fill(im, TART, 'S', filling, merged(FOOD, colours)), *over)


CAKE = """
................
................
................
................
................
.....oooooo.....
...ooTTTTTToo...
..oTTTTTTTTTTo..
.oTTTTTTTTTTTTo.
.oTTTTTTTTTTTTo.
.oSTTTTTTTTTTSo.
.oSSSTTTTTTSSSo.
.oSSSSSSSSSSSSo.
.oSSSSSSSSSSSSo.
..oSSSSSSSSSSo..
...oooooooooo...
"""


def stripes(image, template, key, layers):
    """Colours each column's run of `key` cells top to bottom with layers[i] = (light, mid, dark),
    so the bands follow the cake's curve; light on the left, dark on the right."""
    rows = rows_of(template)
    for x in range(16):
        ys = [y for y in range(len(rows)) if x < len(rows[y]) and rows[y][x] == key]
        for i, y in enumerate(ys):
            light, mid, dark = layers[min(i, len(layers) - 1)]
            image.putpixel((x, y), rgba(light if x <= 4 else dark if x >= 11 else mid))
    return image


def cake(top, palette, layers, *over):
    """A whole round cake: top is 6 rows (6/10/12/12/10/6 wide), layers the side bands."""
    return compose((CAKE, {'o': '4A2A18', 'T': 'FFFFFF', 'S': 'FFFFFF'}, 0, 0),
                   lambda im: fill(im, CAKE, 'T', centred(top, 12), merged(FOOD, palette)),
                   lambda im: stripes(im, CAKE, 'S', layers), *over)


SLICE = """
................
................
................
................
................
............oo..
..........ooTTo.
........ooTTTTEo
......ooTTTTTTEo
....ooTTTTTTTTEo
..ooTTTTTTTTTTEo
.oFFFFFFFFFFFFRo
.oFFFFFFFFFFFFRo
.oFFFFFFFFFFFFRo
.oFFFFFFFFFFFFRo
.ooooooooooooooo
"""


def cake_slice(top, face, palette):
    """A wedge: top is 5 rows of 10 (the triangle), face 4 rows of 12 (the cut side); palette
    also gives E and R, the outer crust at the back."""
    colours = merged(FOOD, palette)
    return compose((SLICE, merged({'o': '4A2A18', 'T': 'FFFFFF', 'F': 'FFFFFF'}, palette), 0, 0),
                   lambda im: fill(im, SLICE, 'T', top, colours),
                   lambda im: fill(im, SLICE, 'F', face, colours))


@item('custard_tart')
def _():
    return tart("""
qqqqqqqq
yYYyyuyy
YyuyyyyY
""", {'y': 'FAD650', 'Y': 'FFF0A0', 'q': 'D8A030', 'u': '9A6230'})


@item('onion_tart')
def _():
    return tart("""
qbqqBbqq
bByybBby
yybBbyBb
""", {'y': 'F4E0A0', 'q': 'C8A050', 'b': '8E4E1E', 'B': 'C07834'})


@item('honey_cake')
def _():
    drips = """
h...h....h
h...h.....
....h.....
"""
    comb = """
.ooo.
oHhHo
ohHho
.ooo.
"""
    return cake("""
LLCCCC
LLCCCCCCCC
LhhhhhhhhhCc
CHhhhhhhhhgc
cChhhhhhgc
cccccc
""", {'h': 'EEA02A', 'H': 'F8CC5A', 'g': 'C88418', 'C': 'D8A050', 'c': 'B88038', 'L': 'E8B868'},
                [('E0961C', 'D08418', 'B06A10'), ('F2D490', 'E8C27A', 'C8A058'), ('F2D490', 'E8C27A', 'C8A058'),
                 ('E8C27A', 'D6AC62', 'B48A44')],
                (drips, {'h': 'D08418'}, 3, 12), (comb, {'o': '8A5210', 'H': 'FFE070', 'h': 'E8A820'}, 5, 6))


@item('celebration_cake')
def _():
    berries = """
...oR.oR...
.oR......oR
"""
    return cake("""
zzWWWW
zzWWWWWWWw
zWWWWWWWWWww
WWWWWWWWWwww
WWWWWWWwww
WWWwww
""", {'z': 'FFFFFF', 'W': 'FBF2E2', 'w': 'E6D8C4'},
                [('FBF2E2', 'F2E6D0', 'D8C8B0'), ('F6D890', 'EEC878', 'D0A858'), ('E04858', 'C83048', 'A02038'),
                 ('F6D890', 'EEC878', 'D0A858'), ('FBF2E2', 'F2E6D0', 'D8C8B0')],
                (berries, {'o': '5A1018', 'R': 'E0303C'}, 2, 6))


@item('seed_cake')
def _():
    return cake_slice("""
........cC
......cCCC
....cCCCCC
..cCCCCCcc
cCCCCCccdd
""", """
YYnYYYYnYYyY
YnYYYnYYYyYy
YYYnYYYYnYyy
yYYYYnYyYyyy
""", {'C': 'D8A050', 'c': 'C08840', 'd': 'A06E2C', 'Y': 'F6E2A4', 'y': 'E6CC88', 'n': '5A4028',
      'E': 'A06E2C', 'R': 'B88040'})


@item('spice_cake')
def _():
    return cake_slice("""
........zW
......zWWw
....zWWWWw
..zWWWWWww
zWWWWWwwgg
""", """
mMmmMmmmMmmn
mmMmmmMmmmnn
MmmmMmmmmMmn
mmmMmmmMmnnn
""", {'z': 'FFFFFF', 'W': 'F6EEE0', 'w': 'DCD0BC', 'g': 'B8A890', 'M': '8A4E2A', 'm': '6E3A1E', 'n': '52280F',
      'E': '52280F', 'R': '6E3A1E'})


# -- roasts: on a pewter platter ---------------------------------------------------------------------

PLATTER = """
................
................
................
................
................
................
................
................
................
..oooooooooooo..
.oHHHhhhhhhhhmo.
oHhPPPPPPPPPPhmo
oHhPPPPPPPPPPhmo
omhhhhhhhhhhhmbo
.ommmmmmmmmmmbo.
..oooooooooooo..
"""
PEWTER = {'o': '343A42', 'H': 'D2D8DA', 'h': 'A8B2B6', 'm': '7E888E', 'b': '5C646C', 'P': '949EA4'}


def platter(*over):
    return compose((PLATTER, PEWTER, 0, 0), *over)


ROAST = {'o': '3E1E0C', 'H': 'E0A458', 'h': 'C47C34', 'm': '9A5624', 'b': '6E3814', 'W': 'F6EEDA', 'w': 'C8BC9C',
         'g': '386E28', 'G': '5E9C3A'}
APPLE = {'o': '4E1A14', 'R': 'E04848', 'r': 'A82C2C', 'P': 'FBE7A6', 'k': '5A3A1E', 'g': '6FA040'}


@item('roast_chicken')
def _():
    bird = """
.oo.......oo...
oWWo.....oWWo..
.owo.ooooowo...
..ohHHHhhho....
.oHHhhhhhhhmo..
oHHhhhhhhhhmmo.
oHhhhhhhhhmmmbo
oHhhhhhhhmmmmbo
.ohhhhmmmmmbbo.
..ommmmmmbbbo..
"""
    herbs = """
gG..........Gg
.gG........Gg.
"""
    return platter((herbs, ROAST, 1, 10), (bird, ROAST, 1, 2))


@item('roast_pork')
def _():
    # a rolled loin: the cut end shows the pink spiral, the rest is scored crackling
    joint = """
...ooooooooo..
..oFFoHhHhHhoo
.oFfFFoHhHhHhmo
.oFfFfFohHhHmmo
.oFFfFFohHhhmbo
.oFfFFFohhhmmbo
..oFFFommmmbbo.
...oooooooooo..
"""
    apples = """
.ooo.......ooo.
oRrPo.....oPRro
oRPPo.....oPPRo
.ooo.......ooo.
"""
    return platter((joint, merged(ROAST, F='F0C0A8', f='D08878'), 0, 3), (apples, APPLE, 0, 10))


@item('roast_mutton')
def _():
    leg = """
..........oo.
.........oWWo
........oWwo.
.......ooo...
.....ooHho...
...ooHHhhmo..
..oHHhWhhmo..
.oHhhhhhWmbo.
oHhWhhhhmmbo.
ohhhhhmmmbo..
.ommmmmbbo...
..ooooooo....
"""
    return platter((leg, ROAST, 1, 1))


@item('roast_boar')
def _():
    haunch = """
...........oo.
..........oWWo
.........oWwo.
....oooooooo..
..ooHhhhhmmo..
.oHHhhhhhmmbo.
oHHhhhhhmmmbo.
oHhhhhhmmmbbo.
.ommmmmmbbbo..
..oooooooo....
"""
    apples = """
.ook.......ook.
oRRro.....oRRro
oRrro.....oRrro
.ooo.......ooo.
"""
    return platter((haunch, merged(ROAST, H='B8683A', h='8E4826', m='6E3418', b='4A200E'), 1, 2), (apples, APPLE, 0, 10))


@item('roast_potatoes')
def _():
    pile = """
.....ooo.......
...ooHHho.ooo..
..oHHhhmooHHho.
.ooHhhmoHHhhmo.
oHHoommoHhhmmo.
oHhhhoWwoommoo.
oHhhmoWWoHHhho.
.ohmmooooHhhmmo
.ooooHHhooommo.
...gohhmmo.gG..
"""
    return platter((pile, merged(FOOD, o='5A3410', H='F6D684', h='E2AC4C', m='B87830', W='FFFBEA', w='DCD2B4'), 1, 3))


@item('herb_omelette')
def _():
    omelette = """
....oooooo....
..ooYYYYYyoo..
.oYYYgYYyyyyo.
oYYGYYYyyGyyyo
oYYYYyyyyyygyo
oyyyyyyyyyyyyo
.ommmmmmmmmmo.
..oooooooooo..
"""
    return platter((omelette, merged(FOOD, o='7A5A18', Y='FBE07A', y='F0C440', m='C89428'), 1, 5))


@item('smoked_fish')
def _():
    fish = """
.....ooooo......
...ooTTTTToo..oo
..oTTTtTTTTToooT
.oWeTTTTTTTTTTTo
oLLgLLLLLLLLttto
.oLlLLLLLLLtoooT
..ooLLLLLllo..oo
....oooooo......
"""
    return platter((fish, {'o': '3E2410', 'T': 'B87428', 't': '8A4E18', 'L': 'EEC470', 'l': 'D8A048',
                           'e': '1A1008', 'W': 'FFF0C0', 'g': '6A3A12'}, 0, 4))


SMALL_DISH = """
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
.oooooooooooooo.
oTSSSSSSSSSSSStq
oTTTTTTTtttttttq
.oKKKkkkkkkkkqo.
..oooooooooooo..
................
"""


@item('baked_apples')
def _():
    # cored, filled with honey and baked until the skins wrinkle
    apples = """
..ooooo...ooooo.
.oRRhRro.oRRhRro
oRRrHrrooRRrHrro
oRwrrrrooRrrwrro
oRrrwrrooRwrrrro
.orrrrro.orrrrro
..ooooo...ooooo.
"""
    return compose((SMALL_DISH, merged(DISH, q='3E2214', S='E0961C'), 0, 0),
                   (apples, {'o': '4A1810', 'R': 'B8502C', 'r': '8E3A1E', 'w': '6A2814', 'h': 'E0961C', 'H': 'F8C84A'}, 0, 4))


@item('honey_wafers')
def _():
    # pressed in a wafer iron: a honeycomb grid on each one
    wafer = """
..ooooo..
.oHhHhHo.
oHhhhhhho
ohHhHhHho
oHhhhhhmo
ohHhHhmmo
.ohhhmmo.
..ooooo..
"""
    palette = {'o': '6A4214', 'H': 'F6D07A', 'h': 'D8A048', 'm': 'B07A30'}
    return compose((wafer, palette, 0, 6), (wafer, palette, 6, 2), (wafer, palette, 7, 8))


# -- boards: the tavern's oak board, as under the Ploughman's Lunch --------------------------------

FARM_CHEESE = {'o': '6E5A30', 'W': 'FBF6E2', 'w': 'E8DFC0', 'M': 'E6D6A8', 'm': 'D2BE88', 'b': 'AE9A66',
               'Y': 'FCE9A0', 'y': 'F0D070'}
CHEESE_ROUND = """
....oooo....
..ooWWWwoo..
.oWWWWWWwoo.
oWWWWWWwoYYo
oMWWWwwoYYyo
oMMMMMMoYyyo
oMmmmmmoyyyo
.ommmmmoyyo.
..oooooooo..
"""
BREAD_HUNK = """
...ooo..
..oHHHo.
.oHhhhmo
oHhhhmmo
ommmmbbo
.oooooo.
"""
LOAF_CRUST = {'o': '4A2E14', 'H': 'C98C4A', 'h': 'A96D33', 'm': '84502A', 'b': '6A3E1E'}


@item('cheese_board')
def _():
    return compose((tavern.BOARD, tavern.OAK, 0, 9), (BREAD_HUNK, LOAF_CRUST, 0, 4),
                   (tavern.APPLE, tavern.FRUIT, 9, 4), (CHEESE_ROUND, FARM_CHEESE, 1, 6))


@item('cold_cuts')
def _():
    cheese = """
.oooooo.
oYYYYYyo
oYyyyyyo
oyyyyyyo
.oooooo.
"""
    slices = """
..oooo.........
.oPPPPoooo.....
.oPppPPPPPoooo.
..ooPppPPPPPPPo
....ooPpPPPpPPo
......ooPppPPo.
........oooo...
"""
    return compose((tavern.BOARD, tavern.OAK, 0, 9), (BREAD_HUNK, LOAF_CRUST, 8, 3),
                   (cheese, {'o': '8A6A1C', 'Y': 'FCEB9E', 'y': 'F2CD62'}, 1, 3),
                   (slices, {'o': '7A3A2A', 'P': 'F4BCA8', 'p': 'D88E7C'}, 0, 6))


@item('picnic_bundle')
def _():
    # a checked cloth knotted at the top, a loaf poking out of one side
    bundle = """
.....oo..oo.....
....oRWo.oWRo...
.....oRooRWo....
......oRWRo.....
....ooRWRWRoo...
..ooWRWRWRWRWoo.
.oRWRWRWRWRWRWro
.oWRWRWRWRWRWrwo
oRWRWRWRWRWRWrwo
oWRWRWRWRWRWrwro
.oRWRWRWRWRwrwo.
..oooooooooooo..
"""
    loaf = """
.oo.
oHHo
oHho
.oo.
"""
    return compose((bundle, {'o': '4A1A14', 'R': 'C8383A', 'W': 'F4EEE0', 'r': '962628', 'w': 'C8C0B0'}, 0, 3),
                   (loaf, LOAF_CRUST, 0, 6))


# -- kitchen ingredients ----------------------------------------------------------------------------

@item('flour')
def _():
    sack = """
......o..o......
.....oLoocLo....
......oLLco.....
......ottto.....
.....oLLLcco....
....oLLLLcccdo..
...oLLLLLccccdo.
...oLLLLLcccddo.
...oLLLLccccddo.
...oLLLccccdddo.
..ooWWoocccddo..
.oWWWWwWoooooo..
.ooooooo........
"""
    return compose((sack, {'o': '5A4A32', 'L': 'E8DCBE', 'c': 'CDBE9A', 'd': 'A8987A', 't': 'A0522D',
                           'W': 'FFFDF6', 'w': 'E6E2D8'}, 0, 2))


@item('butter')
def _():
    pat = """
.....ooooooo....
....oYYYYYYYyo..
...oYYYyYyYyyo..
..oYYYYYyYYyyo..
..oyyyyyyyyymo..
..oyyyyyyyyymo..
..ommmmmmmmmmo..
"""
    dish = """
.oooooooooooooo.
oWWWWWWWWWWWWwwo
ommmmmmmmmmmmmbo
.oooooooooooooo.
"""
    return compose((dish, {'o': '4A301C', 'W': 'C99A5B', 'w': 'AD7F45', 'm': '8A5D31', 'b': '6B4423'}, 0, 11),
                   (pat, {'o': '8A6A1C', 'Y': 'FFF0A8', 'y': 'F6DC78', 'm': 'DEBC52'}, 0, 5))


@item('cheese')
def _():
    return compose((CHEESE_ROUND, FARM_CHEESE, 2, 4))


@item('pastry')
def _():
    sheet = """
....oooooooo....
..ooPPPPPPppoo..
.oPPPPPPPPppppo.
oPPPPPPPPPpppppo
opPPPPPPppppppdo
.opppppppppddo..
..oooooooooo....
"""
    pin = """
...........oo
..........oHo
........ooHho
......ooHhho.
....ooHhhho..
..ooHhhhoo...
.oHhhhoo.....
oHhhoo.......
ohoo.........
oo...........
"""
    return compose((sheet, {'o': '8A7048', 'P': 'FBF0D4', 'p': 'EADAB0', 'd': 'CDB88A'}, 0, 8),
                   (pin, {'o': '4A301C', 'H': 'DDB680', 'h': 'B08250'}, 2, 2))


# -- crop produce -----------------------------------------------------------------------------------

@item('onion')
def _():
    return compose(("""
.........gg.....
........gGg.....
.......oGgo.....
......oHHho.....
.....oHHlhmo....
....oHHhlhhmo...
...oHHhhlhhlmo..
...oHhhlhhhlmo..
...oHhhlhhlmmo..
...ohhhlhhlmbo..
....ohhlhhmbo...
.....ommmmbo....
......owwo......
.....w.ww.w.....
""", {'o': '4A2810', 'H': 'EEBE6A', 'h': 'D09440', 'l': 'B07030', 'm': 'A06628', 'b': '7A4A1C',
      'g': '4E8A30', 'G': '7CB850', 'w': 'E8DCB8'}, 0, 1))


@item('cabbage')
def _():
    return compose(("""
....oo....oo....
...oKKoooKKko...
..oKkkKLLKkkKo..
.oKkKLLLLLLkKko.
.okKLLwLLLLlKko.
oKkLLLLwLLLLlkKo
oKkLLLLwLLLllkbo
oKkkLLLwLLlllkbo
.oKkklLwLllkkbo.
.okKkklllllkkbo.
..oKKkkkkkkKbo..
...oobbbbbboo...
.....oooooo.....
""", {'o': '2A4418', 'K': '5E9A3A', 'k': '467A2A', 'b': '345E20', 'L': 'D2E8A6', 'l': 'A8CC78',
      'w': 'EEF6D2'}, 0, 2))


@item('barley')
def _():
    return compose(("""
........a..a..a.
.....a...a.a.a..
...a..a..a.aa...
....a.aoXooXo.a.
..a..aoXxoXxoa..
...aaoXxoXxXoo..
.....oXxXXxXXxo.
....oXxXXxXXxXo.
....oXXxXXxXo...
...osXXxXXoo....
...ottXXoo......
..ossto.........
.osso...........
osso............
oso.............
.o..............
""", {'o': '6A5020', 'X': 'F0D484', 'x': 'C8A050', 'a': 'E6D6A0', 's': 'C8A858', 't': 'A0522D'}, 0, 0))


@item('garlic')
def _():
    return compose(("""
.......oo.......
.......oWo......
......oWwo......
.....oWWwwo.....
...ooWWWwwwoo...
..oWWvWWwvwwwo..
.oWWWvWWwwvwwmo.
.oWWWvWwwwvwwmo.
.oWWWvWwwwvwmmo.
..oWWvWwwvwmmo..
...oowwwwwmoo...
.....oooooo.....
......w.w.w.....
""", {'o': '6A5A60', 'W': 'FBF8F0', 'w': 'E2DCD4', 'm': 'C4B8B4', 'v': 'A070A8'}, 0, 2))


@item('leek')
def _():
    return compose(("""
...........gG.Go
.........GgGgGgo
..........gGgGo.
.......ogGgGgo..
......ogGgGo....
.....oLlGo......
....oLLlo.......
...oWLlo........
..oWWlo.........
.oWWwo..........
oWWwo...........
owwo............
.oo.............
r.r.............
""", {'o': '2E4A22', 'G': '3E7A3C', 'g': '2E5E30', 'L': 'B4D282', 'l': '8EB860', 'W': 'FBF8E8', 'w': 'DCD8C0',
      'r': 'D8CCA8'}, 0, 1))


@item('herbs')
def _():
    # parsley, thyme and sage, tied with twine
    return compose(("""
.........oSSo...
.....ot.oSsSSo..
.oo..otTooSsSso.
oPPpootTtoSssSo.
pPpPPpotTooSsso.
oPpPpPotToSSso..
.opPpPpeToooo...
..oppPoeeo......
...oooeeo.......
.....orro.......
....oeeo........
...oeeo.........
..oeeo..........
.oeeo...........
.oeo............
..o.............
""", {'o': '24401A', 'p': '3E8A2E', 'P': '6CC048', 'T': '2E6A2A', 't': '5E9A4A', 'S': 'B4C2A4', 's': '849A7C',
      'e': '7E9A48', 'r': 'A0522D'}, 0, 0))


# -- seeds: small handfuls in the vanilla seed style (two tones, no outline) ------------------------

@item('onion_seeds')
def _():
    return compose(("""
.....hb.........
....bbb...hb....
.........bbbb...
..hb............
..bbb.....hbb...
......hb...bb...
.....bbbb.......
................
...hbb...hb.....
....bb...bbb....
""", {'h': '7A706A', 'b': '1E1A1C'}, 0, 3))


@item('cabbage_seeds')
def _():
    return compose(("""
....Rr..........
....rr....Rr....
..........rr....
.Rr...Rr........
.rr...rr....Rr..
............rr..
...Rr...Rr......
...rr...rr......
""", {'R': 'B0623E', 'r': '6E3220'}, 1, 3))


@item('barley_seeds')
def _():
    return compose(("""
....Xx......Xx..
...Xxs.....Xxs..
....s.......s...
.Xx.....Xx......
Xxs....Xxs......
.s......s...Xx..
...........Xxs..
...Xx.......s...
..Xxs...Xx......
...s...Xxs......
........s.......
""", {'X': 'F0D890', 'x': 'D0AE60', 's': 'A8843C'}, 1, 3))


@item('leek_seeds')
def _():
    return compose(("""
.......g........
......kk....g...
.g.....k...kk...
.kk.........k...
..k...g.........
.....kk.....g...
......k....kk...
..g.........k...
..kk..g.........
...k..kk........
.......k........
""", {'g': '7E8E74', 'k': '24281E'}, 2, 3))


@item('herb_seeds')
def _():
    return compose(("""
....a.....g.....
...ab.b..gk.....
........a.....a.
.g..a........ab.
gk.ab..g.b......
.......gk...g...
..b..a......gk..
....ab..ab......
.g.....b....a...
gk...g....b.ab..
.....gk.........
""", {'a': 'D8BC80', 'b': '8A6A40', 'g': '8E9E68', 'k': '5E6E40'}, 0, 3))


@item('garlic_clove')
def _():
    return compose(("""
........o.......
.......oWo......
.......oWo......
......oWWwo.....
.....oWWWwo.....
.....oWWWwwo....
....oWWWWwwo....
....oWWWwwwo....
....oWWwwwmo....
....ovvvvvmo....
.....oooooo.....
""", {'o': '6A5A60', 'W': 'FBF8F0', 'w': 'E2DCD4', 'm': 'C4B8B4', 'v': 'B488B8'}, 1, 3))


# -- Not-So-Vanilla Mobs drops and the recipe card -------------------------------------------------

@item('boar_haunch')
def _():
    return compose(("""
...........oo...
..........oWWo..
.........oWwWo..
........oWwoo...
......ooPPo.....
....ooPPPPPo....
...oPPPPpPPdo...
..oPPPpPPPPddo..
.oPPPPPPPpPddob.
.oPPpPPPPPddbo..
oPPPPPPpPddbbob.
oPpPPPPPddbbo...
.oPPPPdddbbob...
..oddddbbo.b....
...ooooo........
""", {'o': '3A1A14', 'W': 'F6EEDA', 'w': 'C8BC9C', 'P': 'EC9C94', 'p': 'C87070', 'd': '6A4030', 'b': '2E2018'}, 0, 1))


@item('brineclaw_meat')
def _():
    return compose(("""
..oo............
.oRRo...........
.oRro.oo........
..oRooRRo.......
..oRRRRro.......
...oRRrrooooo...
...oRRrroWWWWo..
....oRroWWfWWWo.
....oRroWfWWfWo.
.....oroWWWfWo..
......ooWWWWo...
........oooo....
""", {'o': '4A140C', 'R': 'E05838', 'r': 'A82A1C', 'W': 'FBF4EA', 'f': 'F0904A'}, 0, 2))


@item('sporecap')
def _():
    return compose(("""
.....oooooo.....
...ooVVzVVvoo...
..oVVzVVVVzvvo..
.oVzVVVVzVVvvvo.
.oVVVzVVVVvzvvo.
oVVVVVVVVvvvvvvo
ovvVVvvvvvvvvvbo
.oooooSSsoooooo.
......oSSso.....
......oSsso.....
.......ooo......
""", {'o': '3A2A48', 'V': 'B4A4CC', 'v': '8474A0', 'b': '5A4A70', 'z': 'F4EEF6', 'S': 'E8E0D0', 's': 'C8BCAC'}, 0, 3))


@item('recipe_card')
def _():
    return compose(("""
..oooooooooo....
..oPPPPPPPPdoo..
..oPllllllPdPdo.
..oPPPPPPPPdddo.
..oPllllPlllPPo.
..oPPPPPPPPPPPo.
..oPlllllPPPPPo.
..oPPPPPPPPPPPo.
..oPllllPoooooo.
..oPPPPPorRRro..
..opppppoRzRRro.
..oooooooRRRrro.
.........orrro..
.........oo.oo..
""", {'o': '4A3622', 'P': 'F2E6C4', 'p': 'D8C8A0', 'd': 'C8B488', 'l': '8A7458', 'R': 'D03838', 'r': '962226',
      'z': 'F07070'}, 0, 1))


# -- crop stages: for minecraft:block/crop, plants rooted on the bottom row, no outlines -------------

def plants(palette, *tufts):
    """tufts: (pattern, x), each standing on the bottom row."""
    image = Image.new('RGBA', (16, 16))
    for pattern, x in tufts:
        rows = rows_of(pattern)
        paint(image, rows, palette, x, 16 - len(rows))
    return image


def crop(name, palette, stages):
    CROPS[name] = lambda stage: plants(palette, *stages[stage])


ONION_LEAF = {'L': '8CC07A', 'G': '4E8A4A', 'g': '336636', 'y': 'C8C060', 'W': 'EEEAD0', 'w': 'C8C2A0',
              'B': 'D89A48', 'b': 'A86A2C', 'H': 'F0C070'}
crop('onion', ONION_LEAF, [
    [("""
L
G
g
""", 2), ("""
.L
G.
g.
""", 7), ("""
L
g
""", 12)],
    [("""
L..L
G.LG
GLG.
.GG.
.gg.
.gg.
""", 0), ("""
.L.
LG.
G.G
GG.
gg.
""", 6), ("""
L..L
G.LG
.GG.
.gg.
.gg.
""", 11)],
    [("""
L.L..L
G.G.LG
G.GLG.
.GG.G.
.GGGG.
..GGg.
..Ggg.
..gg..
..WW..
..ww..
""", 0), ("""
.L..L
LG.LG
G.G.G
G.GG.
.GGG.
..Gg.
..gg.
.WW..
.ww..
""", 5), ("""
L.L.L
G.GG.
.GGG.
.GGG.
..GG.
..gg.
.WWw.
.ww..
""", 10)],
    [("""
y.....y.
Gy...yG.
.G..LG.L
.GL.G.LG
..GLGLG.
..GGGG..
..GGGg..
...GGg..
...gg...
..HBBb..
.HBBBbb.
.BBBbbb.
..bbbb..
""", 0), ("""
....y..
L..yG..
G.LG..L
G.G...G
.GGL.G.
.GGGGG.
..GGG..
..Gg...
..gg...
.HBBb..
HBBBbb.
BBBbbb.
.bbbb..
""", 6), ("""
.L..y
.GLGy
GLG..
GGL..
.GG..
.Gg..
.gg..
HBBb.
BBbb.
.bb..
""", 11)],
])

GARLIC_LEAF = {'L': 'A2C86A', 'G': '5E9440', 'g': '40702E', 'y': 'C8BC6A', 'W': 'F6F2EA', 'w': 'D6D0C8', 'v': 'A880B0'}
crop('garlic', GARLIC_LEAF, [
    [("""
L
G
""", 3), ("""
LL
.G
.g
""", 8), ("""
L
g
""", 13)],
    [("""
LL.LL
.GLG.
.GG..
..g..
..g..
""", 0), ("""
L..
GLL
GG.
.g.
.g.
""", 6), ("""
LL.
.GL
.G.
.g.
""", 12)],
    [("""
LL...LL
.GL.LG.
.GG.GG.
..GGG..
..GGg..
..Ggg..
..gg...
..gg...
..WW...
""", 0), ("""
LL..L
.GLLG
.GGG.
.GGg.
..Gg.
..gg.
..gg.
..WW.
""", 7), ("""
.LL
LG.
GG.
Gg.
gg.
gg.
WW.
""", 13)],
    [("""
y......yy
Gy....LLG
GG...LGG.
.GG.LGG..
.GGLGG...
..GGGg...
..GGgg...
...Ggg...
...gg....
..WWWw...
.WvWWvw..
.WWvWww..
..wwww...
""", 0), ("""
.yy..
.GG.L
..GLG
..GG.
.GGg.
.Ggg.
.gg..
.gg..
WWWw.
WvWvw
WWww.
.ww..
""", 8), ("""
.L.
LG.
G..
GG.
Gg.
gg.
gg.
WWw
vWw
ww.
""", 13)],
])

CABBAGE_LEAF = {'L': 'A8CC78', 'K': '5E9A3A', 'k': '3E7428', 'h': 'C4E096', 'H': 'E2F0C0', 'v': 'F2F8DE'}
crop('cabbage', CABBAGE_LEAF, [
    [("""
L.L
.k.
""", 2), ("""
LL
.k
""", 8), ("""
L.L
.k.
""", 12)],
    [("""
L...L
KL.LK
.KkK.
..k..
""", 0), ("""
L..L
KLLK
.kk.
""", 6), ("""
L...L
KL.LK
.KkK.
..k..
""", 11)],
    [("""
.L...L.
LKL.LKL
KKKLKKK
.KkKkK.
.kkkkk.
..kkk..
""", 0), ("""
L...L.
KL.LKL
KKLKKK
.KkKk.
..kkk.
""", 5), ("""
.L..L
LKLLK
KKKKK
KkKkK
.kkk.
..k..
""", 11)],
    [("""
L.......
KL.L..L.
.KLhHhLK
LKhHHHhK
KKhHvHhK
KkhHhhhk
.kKhhkKk
.kkKkKk.
..kkkkk.
""", 0), ("""
.L.......
.KL..L.L.
KLhhHhLK.
KhHHHHhKL
KhHHvHhhK
KkhHHhhkK
.kKhhhkKk
..kKkKkk.
...kkkk..
""", 7)],
])


BARLEY_STALK = {'L': '8CC060', 'G': '5E9A3A', 'g': '3E7428', 'l': 'B8C868', 'Y': 'ECD07C', 'y': 'C8A450',
                'a': 'F2E4B0', 's': 'C8B068', 'S': 'A08A44'}
GREEN_EARS = """
...L......L.....
..lL..L..lL..L..
..ll.lL..ll.lL..
..lL.ll..lL.ll..
...G.lL...G.lL..
..LG..G..LG..G..
..G..LG..G..LG..
.LG..G..LG..G...
.G.G.G..G.G.G.L.
.GG..GG.GG..GGG.
.Gg.Gg..Gg.Gg.g.
.gg.gg..gg.gg.g.
"""
RIPE_EARS = """
..a.....a.......
a..a.a...a..a...
.a.aYa.a..aYa.a.
..aYya..aYya.a..
...Yy....Yy..aYa
..aYya..aYya.Yya
...Yy.aY..Yy..Yy
...s.aYya.s..sY.
..s...Yy..s..s..
..s..aYya.s.s...
.s.S..Yy.s..sS..
.s.S..sS.s.SsS..
.sSS..sS.SsS.S..
.SS.SsS..SS..SS.
.SS.SSS.SSS.SSS.
"""
crop('barley', BARLEY_STALK, [
    [("""
.L
LG
Gg
""", 1), ("""
L
G
g
""", 6), ("""
L.
GL
gG
""", 9), ("""
L
g
""", 14)],
    [("""
L..L
G.LG
G.G.
GLG.
.GG.
.Gg.
.gg.
""", 0), ("""
.L.
LG.
G.L
GG.
gg.
""", 5), ("""
L..L
G.LG
.GG.
.Gg.
.gg.
.gg.
""", 9)],
    [(GREEN_EARS, 0)],
    [(RIPE_EARS, 0)],
])

LEEK_FAN = {'L': '6EA478', 'G': '3E7A5A', 'g': '2A5A40', 'l': 'A8D098', 'W': 'F2F0E0', 'w': 'D4D0BC'}
crop('leek', LEEK_FAN, [
    [("""
L.L
.G.
""", 2), ("""
.L
LG
.g
""", 7), ("""
L.L
.g.
""", 12)],
    [("""
L.L
.GL
.G.
.l.
.W.
""", 1), ("""
L..L
.GL.
.G..
.l..
.W..
""", 6), ("""
L.L
LG.
.G.
.W.
""", 12)],
    [("""
L...L
G..G.
.G.G.
.GGg.
..Gg.
..Gg.
..ll.
..lL.
..WW.
..Ww.
""", 0), ("""
L..L
G.G.
.GG.
.Gg.
.Gg.
.ll.
.lL.
.WW.
.Ww.
""", 5), ("""
.L..L
.G.G.
..GG.
..Gg.
..ll.
..lL.
..WW.
..Ww.
""", 10)],
    [("""
G....G
G...G.
.G..G.
.G.Gg.
G.GGg.
.GGg..
..Gg..
..Gg..
..lL..
..ll..
..WW..
..WW..
..Ww..
..Ww..
..ww..
""", 0), ("""
.G..G
G..G.
.G.Gg
.GGg.
G.Gg.
.GGg.
..Gg.
..lL.
..ll.
..WW.
..WW.
..Ww.
..ww.
""", 5), ("""
G...G
.G.G.
.GGg.
GGg..
.Gg..
.Gg..
.lL..
.ll..
.WW..
.Ww..
.ww..
""", 10)],
])

HERB_BUSH = {'P': '6CC048', 'p': '3E8A2E', 'S': 'A8B898', 's': '7E9474', 'T': '2E6A2A', 'f': 'B890D0', 'F': 'F4F0F8'}
crop('herbs', HERB_BUSH, [
    [("""
P.P
.p.
""", 2), ("""
S.S
.s.
""", 7), ("""
PP
.p
""", 12)],
    [("""
P.P
pPp
.p.
""", 1), ("""
S.S
sSs
.s.
""", 6), ("""
T.T
TPT
.p.
""", 11)],
    [("""
..P...
.PpP.S
PpPpSs
.pPSsS
..pss.
..p.s.
""", 0), ("""
.T.T.
TTPpT
.TpPp
..pp.
..p..
""", 6), ("""
..S.
.SsS
SsSs
.ss.
..s.
""", 12)],
    [("""
.f..F...
fTf.FPF.
TfTPpPpS
.TTpPpSs
TTpPpSsS
.TpPSsSs
..pp.ss.
..p...s.
""", 0), ("""
..F..f..
.FPF.fTf
SPpPpTfT
SsPpPTT.
sSsPpPTT
SsSsPpT.
.ss.pp..
.s...p..
""", 8)],
])


# -- end of sprites --------------------------------------------------------------------------------


# -- compiling --------------------------------------------------------------------------------------

def table(name):
    rows, header = [], None
    for raw in (HERE / name).read_text(encoding='utf-8').splitlines():
        if not raw.strip() or raw.startswith('#'):
            continue
        cells = [c.strip() for c in raw.split('\t')]
        if header is None:
            header = cells
        else:
            rows.append(dict(zip(header, cells)))
    return rows


def wanted():
    """Every item id the tables need a sprite for, in table order, and the crop ids."""
    crops = table('crops.tsv')
    ids = [d['id'] for d in table('dishes.tsv') if 'existing' not in d['flags'].split(',')]
    ids += [x for c in crops for x in (c['id'], c['seed'])]
    ids += [i['id'] for i in table('ingredients.tsv')]
    return ids + ['recipe_card'], [c['id'] for c in crops]


def missing():
    items, crops = wanted()
    return [i for i in items if i not in ITEMS] + [f'{c} (crop stages)' for c in crops if c not in CROPS]


def png(image):
    buffer = io.BytesIO()
    image.save(buffer, 'PNG')
    return buffer.getvalue()


def dump(data):
    return (json.dumps(data, indent=2) + '\n').encode()


def outputs():
    items, crops = wanted()
    files = {}
    for name in items:
        files[ASSETS / f'textures/item/{name}.png'] = png(ITEMS[name]())
        files[ASSETS / f'models/item/{name}.json'] = dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': f'{NS}:item/{name}'}})
        files[ASSETS / f'items/{name}.json'] = dump({'model': {'type': 'minecraft:model', 'model': f'{NS}:item/{name}'}})
    for crop in crops:
        for stage in range(4):
            files[ASSETS / f'textures/block/{crop}_stage{stage}.png'] = png(CROPS[crop](stage))
    return files


def require_all():
    gone = missing()
    if gone:
        print('No sprite for:\n  ' + '\n  '.join(gone))
        sys.exit(1)


def write():
    require_all()
    files = outputs()
    for path, data in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(f'Hearth sprites: {len(wanted()[0])} items, {4 * len(wanted()[1])} crop stages ({len(files)} files).')


def check():
    require_all()

    def same(path, data):
        if not path.exists():
            return False
        current = path.read_bytes()
        return current == data if path.suffix == '.png' else current.replace(b'\r\n', b'\n') == data
    bad = [str(p.relative_to(PROJECT)) for p, data in outputs().items() if not same(p, data)]
    if bad:
        print('Out of date (run tools/hearth/sprites.py):\n  ' + '\n  '.join(bad))
        sys.exit(1)
    print('Hearth sprites are up to date.')


# -- previews ---------------------------------------------------------------------------------------

def vanilla(paths):
    """Vanilla textures for comparison, read from the Loom cache when it is there (preview only)."""
    jars = sorted(Path.home().glob('.gradle/caches/fabric-loom/*/minecraft-client.jar'))
    if not jars:
        return []
    with zipfile.ZipFile(jars[-1]) as jar:
        names = set(jar.namelist())
        out = []
        for path in paths:
            full = f'assets/minecraft/textures/{path}.png'
            if full in names:
                image = Image.open(io.BytesIO(jar.read(full))).convert('RGBA').crop((0, 0, 16, 16))
                out.append((f'{path.split("/")[-1]} (vanilla)', image))
        return out


def existing(names):
    return [(f'{n} (existing)', Image.open(ASSETS / f'textures/item/{n}.png').convert('RGBA'))
            for n in names if (ASSETS / f'textures/item/{n}.png').exists()]


def sheet(tiles, dest, columns=10, background='#8BA9C4'):
    """Each tile at 8x with 1x and 2x thumbnails under it, labelled."""
    big, pad, label, thumbs = 128, 14, 14, 40
    w, h = big + pad, label + big + thumbs + pad
    rows = (len(tiles) + columns - 1) // columns
    out = Image.new('RGB', (columns * w + pad, rows * h + pad), background)
    draw = ImageDraw.Draw(out)
    for n, (name, image) in enumerate(tiles):
        x, y = pad + (n % columns) * w, pad + (n // columns) * h
        draw.text((x, y), name[:22], fill='#14202C')
        if image is None:
            draw.rectangle((x, y + label, x + big - 1, y + label + big - 1), outline='#AA3333')
            continue
        scaled = image.resize((big, big), Image.NEAREST)
        out.paste(scaled, (x, y + label), scaled)
        out.paste(image, (x, y + label + big + 8), image)
        double = image.resize((32, 32), Image.NEAREST)
        out.paste(double, (x + 28, y + label + big + 4), double)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest)
    print(dest)


def preview():
    items, crops = wanted()
    tiles = [(name, ITEMS[name]() if name in ITEMS else None) for name in items]
    tiles += existing(['hearty_stew', 'shepherds_pie', 'apple_tart', 'fresh_village_bread', 'ploughmans_lunch', 'birthday_cake_slice'])
    tiles += vanilla(['item/mushroom_stew', 'item/beetroot_soup', 'item/rabbit_stew', 'item/bread', 'item/pumpkin_pie',
                      'item/cake', 'item/honey_bottle', 'item/wheat_seeds', 'item/beetroot_seeds', 'item/carrot'])
    sheet(tiles, PROJECT / 'build/previews/hearth_items.png')
    stages = []
    for crop in crops:
        stages += [(f'{crop}_stage{s}', CROPS[crop](s) if crop in CROPS else None) for s in range(4)]
    stages += vanilla([f'block/carrots_stage{s}' for s in range(4)] + [f'block/wheat_stage{s}' for s in (2, 4, 6, 7)])
    sheet(stages, PROJECT / 'build/previews/hearth_crops.png', columns=4, background='#9DB8CF')


if __name__ == '__main__':
    if '--check' in sys.argv:
        check()
    elif '--preview' in sys.argv:
        preview()
    else:
        write()
