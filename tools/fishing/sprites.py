"""Authored 16px sprites for Tall Tales Fishing, in the style of tools/item_sprites.py, tools/tavern/sprites.py
and tools/hearth/sprites.py: native pixel patterns, a dark outline per material, stepped palettes, light from
the top left and no antialiasing. Every fish is posed like vanilla's cod: head at the lower left, tail at
the upper right.

Eighty fish cannot each be drawn from scratch and still look like one catch, so they are built from body
templates (small, slender, torpedo, deep, spiny, pike, eel, whiskered, flatfish, shark, crayfish ...) with
lettered fill regions: K the back, H and h the upper and middle flank, W the belly and w its shadow, d D the
dorsal fin, f F the other fins, e the eye and g the gill line, plus a few letters a template keeps for itself
(x whiskers and feelers, L G a glowing lure, m t a mouth and its teeth, E an eye's rim). A fish names its
template and a palette for those letters, then lays its markings over the body: bars, spots, a stripe, a
thumbprint, scales. The nine legends get templates of their own that fill more of the square.

Also writes a silhouette of every fish in the table, the four vanilla fish included (traced from their
textures in the Loom cache): the same shape in one dark ink, for the angler's journal to show while a fish
is still uncaught.

    python tools/fishing/sprites.py            # write textures, models/item and items/ for every fish, and the silhouettes
    python tools/fishing/sprites.py --check    # verify the files match the patterns and every fish has a sprite
    python tools/fishing/sprites.py --preview  # build/previews/fishing_fish.png and fishing_silhouettes.png, 8x

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
INK = '2A2622'  # the journal's silhouette ink


# -- drawing ----------------------------------------------------------------------------------------

def rgba(color):
    return tuple(bytes.fromhex(color)) + (255,)


def rows_of(pattern):
    return pattern.strip('\n').split('\n') if isinstance(pattern, str) else list(pattern)


def merged(*palettes, **extra):
    out = {}
    for p in palettes:
        out.update(p)
    out.update(extra)
    return out


def draw(template, palette, *marks):
    """Paints a template in a palette, then each mark over it. A mark is a pattern of its own ('.'
    transparent): 16 rows, or (pattern, x, y) for a small one placed at x, y. Marks may only land on
    the fish, never on the empty pixels around it. A palette without d and D paints the dorsal fin
    like the other fins."""
    rows = rows_of(template)
    assert len(rows) == 16 and all(len(r) == 16 for r in rows), rows
    colours = merged({'d': palette.get('f'), 'D': palette.get('F')}, palette)
    image = Image.new('RGBA', (16, 16))
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != '.':
                image.putpixel((x, y), rgba(colours[ch]))
    for mark in marks:
        pattern, x0, y0 = mark if isinstance(mark, tuple) else (mark, 0, 0)
        for j, row in enumerate(rows_of(pattern)):
            for i, ch in enumerate(row):
                if ch != '.':
                    assert rows[y0 + j][x0 + i] != '.', ('mark off the fish', x0 + i, y0 + j)
                    image.putpixel((x0 + i, y0 + j), rgba(colours[ch]))
    return image


def where(template, letter, test):
    """A mark: `letter` on every template pixel (x, y, ch) that passes test."""
    return [''.join(letter if ch != '.' and test(x, y, ch) else '.' for x, ch in enumerate(row))
            for y, row in enumerate(rows_of(template))]


BODY = 'KHhWwge'


def bars(template, letter, diagonals, on='KHh'):
    """Bars across the body: the `on` pixels of the given diagonals (x - y). A fish lies head down-left,
    tail up-right, so each diagonal is a line straight across it; give two neighbours for a bold bar."""
    return where(template, letter, lambda x, y, ch: ch in on and x - y in diagonals)


def depth(template):
    """{(x, y): 0..1} for the body pixels: how far each lies from the back (0) to the belly (1),
    measured across the body (along its diagonal x - y)."""
    rows = rows_of(template)
    across = {}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in BODY:
                across.setdefault(x - y, []).append(x + y)
    out = {}
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in BODY:
                lo, hi = min(across[x - y]), max(across[x - y])
                out[(x, y)] = (x + y - lo) / (hi - lo) if hi > lo else 0.5
    return out


def along(template, letter, lo, hi, on=BODY, ends=(-99, 99), every=1):
    """A stripe along the body: the `on` pixels between depths lo and hi (0 the back, 1 the belly),
    between diagonals ends[0] and ends[1] (x - y, head to tail); every=n keeps one diagonal in n,
    which breaks the stripe into a row of spots."""
    deep = depth(template)
    return where(template, letter, lambda x, y, ch: ch in on and (x, y) in deep and lo <= deep[(x, y)] <= hi
                 and ends[0] <= x - y <= ends[1] and (x - y) % every == 0)


def spots(template, letter, on='KH', step=4, phase=0):
    """Spots scattered evenly over the `on` pixels: one in `step` along a staggered grid."""
    return where(template, letter, lambda x, y, ch: ch in on and (x + 2 * y) % step == phase)


def lattice(template, letter, on='Hh', across=4, phase=0, parity=0):
    """A diamond net over the `on` pixels, one dot every `across` diagonals: big scales, or a pattern of dents."""
    return where(template, letter, lambda x, y, ch: ch in on and (x + y) % 2 == parity and (x - y) % across == phase)


FISH = {}


def fish(name):
    def register(fn):
        FISH[name] = fn
        return fn
    return register


# -- body templates ---------------------------------------------------------------------------------
# o outline, K back, H upper flank (in the light), h flank, W belly, w its shadow, d D dorsal fin,
# f F tail and lower fins, e eye, g gill line. Head at the lower left, tail at the upper right, so the
# back faces up-left and the belly down-right; the shell and the flatfish are seen from above.

# Fish: small to large, then the long ones.

SMALL = """
................
..........o.....
.........oFo....
.........oFFo...
.....o.oooFoFo..
....oDoKKKfFfFo.
....oDKKhhwooo..
....oKKhhwwo....
...oKKHhwwo.....
...oKHhWwo......
..oKKgWwwo......
..oKewgwo.......
..ohwwoo........
...ooo..........
................
................
"""

SLENDER = """
...........oo...
..........oFFo..
..........oFfoo.
........oooFfFFo
.....oooKKKffffo
....oDDKKhhwooo.
.....oKKhhwwo...
....oKKHhwwo....
...oKKHhWwo.....
..oKKHhWwwo.....
.oKKghWwwo......
.oKehgwwfo......
.oKhWwwoo.......
.ohwwwo.........
..oooo..........
................
"""

TORPEDO = """
...........oo...
..........oFFo..
..........oFfoo.
....oooooooFfFFo
...oDDDKKKKffffo
....oKKKHhhwooo.
...oKKHHhWwwo...
...oKHHhWwwo....
..oKKHhWWwo.....
.oKKHHWWwwo.....
.oKHgWWwwo......
.oKeWgwwfo......
.oKhWwwoFo......
.ohwwwo.o.......
..oooo..........
................
"""

DEEP = """
...........oo...
...oo.....oFFo..
..oDDoo...oFfoo.
..oDdDDooooFfFFo
...oKKKKKKKffffo
..oKKKHHHHhwooo.
.oKKKKHHHhWwo...
.oKKKHHhhhWwo...
.oKHHHhhWWWwo...
.oKHHhhWWWwwFo..
.oKHghWWWWwoFo..
.oKehgWWWwwoo...
..ohWWWwwwfo....
..ohwwwwooFo....
...ooooo..o.....
................
"""

SPINY = """
...........oo...
......o...oFFo..
...o.oDo..oFfoo.
..oDoDdDoooFfFFo
.oDoDddKKKKffffo
..oDdKKKHhhwooo.
...oKKHHHWwwo...
...oKHHhWWwo....
..oKKHhhWwwFo...
.oKKHHhWWwoFo...
.oKHghWWwwoo....
.oKehgWwwo......
.oKhWWwwfFo.....
.ohwwwwoooFo....
..ooooo...o.....
................
"""

SAIL = """
..o........oo...
.oDoo.....oFFo..
..oDDoo...oFfoo.
.oDddDDooooFfFFo
..oDdddDKKKffffo
..oDddKKKhhwooo.
..oDdKKHhhwwo...
...oKKHHWwwo....
...oKHHWWwo.....
..oKKHWWwwo.....
.oKKghWwwo......
.oKehgwwfo......
.oKhWwwoo.......
.ohwwwo.........
..oooo..........
................
"""

PIKE = """
...........oo...
......o...oFFo..
.....oDoo.oFfoo.
.....oDDDooFfFFo
......oKKKKffffo
.....oKKHHhwooo.
....oKKHHWWwo...
...oKKHHWWwwFo..
..oKKHHWWwwffo..
.oKKHHWWwwooo...
.oKHHWWwwo......
oKKhgWwwo.......
oKehwgwo........
ohwwwooFo.......
.oooo..o........
................
"""

PIKEPERCH = """
...........oo...
..........oFFo..
......ooo.oFfoo.
....ooDDDooFfFFo
...oDDoKKKKffffo
..oDddKKHHhwooo.
...oDKKHHWWwo...
...oKKHHWWwwFo..
..oKKHHWWwwffo..
.oKKHHWWwwooo...
.oKHHWWwwo......
oKKhgWwwo.......
oKehwgwo........
ohwwwooFo.......
.oooo..o........
................
"""

GAR = """
...........oo...
..........oFFo..
.......o..oFfFo.
......oDoooFffFo
......oDKKKffffo
......oKKHhwooo.
.....oKKHhWwo...
....oKKHhWwwo...
...oKKHhWwwfFo..
..oKKHhWwwooo...
..oKHgWwwo......
..oKeWgwo.......
..ohwwwo........
.ohoooo.........
oho.............
.o..............
"""

LONGFIN = """
...........oo...
..........oFFo..
......ooo.oFfFo.
.....oDDDooFffFo
....oDdKKKKffffo
...oDdKKHHhwooo.
..oDdKKHHWWwo...
.oDdKKHHWWwwFo..
..oKKHHWWwwffo..
.oKKHHWWwwoFo...
oKKHHWWwwo.o....
oKHHgWwwo.......
oKeWWgwo........
ohwwwwo.........
.ooooo..........
................
"""

AROWANA = """
...........oo...
.....oo...oFFo..
....oDDoo.oFfFo.
.....oDDDooFffFo
.....oDKKKKffffo
.....oKKHhhwooo.
....oKKHHWwwo...
...oKKHHWWwfFo..
..oKKHHWWwwffo..
..oKHHhWwwfffo..
.oKKghWWwoFffo..
.oeHHgWwwoooo...
.oKhWWwwo.......
xohwwwwo........
.xooooo.........
................
"""

EEL = """
................
...........oooo.
.........ooKKFFo
........oKKHhhFo
.......oKHhWwwo.
.......oKHWwoo..
......oKHhWo....
......oKHWwo....
.....oKHhWo.....
.....oKHWwo.....
...ooKHhWo......
..oKKHhWwo......
.oKHhWwwo.......
oKeWwwoo........
.owwoo..........
..oo............
"""

# Whiskered bottom-feeders.

GUDGEON = """
................
..........o.....
.........oFo....
.........oFFo...
.....o..ooFfFo..
....oDooKKfffFo.
....oDKKKhwooo..
....oKKHhwwo....
...oKKHhWwo.....
..oKKHhWwwo.....
..oKghWwwo......
..oehgwwo.......
.xohwwwo........
x.xoooo.........
..x.............
................
"""

WHISKERED = """
...........oo...
..........oFFo..
..........oFfoo.
........oooFfFFo
...o..ooKKKffffo
..oDooKKKhhwooo.
..oDKKKHHhwwo...
..oKKHHHWWwfo...
.oKKHHhWWwwfo...
oKKHHhhWwwffo...
oKHHhgWWwoFo....
.oehhgWwwoo.....
xoKWWWgwo.......
.xowwwwo........
x.xoooo.........
..x.............
"""

STURGEON = """
..........o.....
.........oFo....
.........oFFo...
.....oo..oFfo...
....oDDoooFfFo..
.....oKKKKfffo..
....oKKHHhwoo...
...oKKHHWWwo....
..oKKHHWWwwo....
.oKKHHWWwwfFo...
.oKHgWWwwooo....
.oKeWgwwo.......
.oKhwwwo........
.ohwwoo.........
..xoo...........
.x..............
"""

# The open sea.

MAHI = """
...........oo...
..........oFFo..
.......oo.oFfoo.
.....ooDDooFfFFo
.oo.oDDdKKKffffo
oDDoDdKKKhhwooo.
oDdDdKKHHhwwo...
oDdKKKHHWWwfFo..
oDKKHHHWWwwfo...
oKKHHhhWwwffo...
oKHghhWWwooo....
oKehgWWwwo......
.ohWWWwwo.......
..owwwwo........
...oooo.........
................
"""

TUNA = """
..........o.....
.........oFo....
.........oFFo...
..o......oFfoo..
.oDoooooooFfFFo.
.oDDDKKKKKffffFo
..oKKKHHHhwoooo.
.oKKHHHhhWwo....
.oKHHHHhWWwo....
.oKHHHhhWwwo....
.oKHghhWWwfFo...
.oKehgWWwwffo...
..ohWWWwwooo....
...owwwwo.......
....oooo........
................
"""

SWORD = """
..........o.....
.........oFo....
.........oFFo...
..oo.....oFfoo..
.oDDooooooFfFFo.
..oDDDKKKKffffFo
..oDdKKHHhwoooo.
...oKKHHhWwo....
..oKKHHhWWwo....
..oKHHhWWwwo....
..oKHgWWwwo.....
..oKeWgwwo......
..ohwwwwfFo.....
.ohooooooo......
oho.............
.o..............
"""

SHARK = """
............oo..
...........oFFo.
......o...oFffo.
.....oDo.oFffo..
....oDdoooFffo..
....oDdKKKfffFo.
....oDKKhhwooo..
...oKKKHhwwo....
..oKKHHhWwo.....
..oKHHWWwwo.....
.oKKhWWwwo......
.oKehggwo.......
.oKwwwffo.......
.ohwooFfo.......
..oo..oo........
................
"""

FLAT = """
...........oo...
..........oFFo..
....ooooo.oFfFo.
...oFFFFFooFffFo
..oFfHHHHHHffffo
.oFfHHHHhhhwooo.
.oFHHHHhhhhwo...
oFfHHHhhhhhwFo..
oFHHHhhhhhhwfo..
oFHHehhhhhwwfo..
.oHhhhhhhwwwfo..
.oHhhehhwwwffo..
..ohhhhwwwffo...
...owwwwfffo....
....ooFffoo.....
......ooo.......
"""

FLAT_LONG = """
...........oo...
..........oFFo..
.......oo.oFfoo.
....oooFFooFfFFo
...oFFFfHHHffffo
..oFfHHHHhhwooo.
.oFfHHHhhhhwo...
.oFHHHhhhhwwFo..
oFfHHhhhhhwffo..
oFHHhhhhhhwfo...
.oHehhhhhwwfo...
.oHhhhhhwwffo...
.oHhehwwwffo....
.ohwwwwfffo.....
..ooooFfoo......
......oo........
"""

RAY = """
................
................
................
............xx..
.......oo..x....
.....ooHHox.....
....oHHHhho.....
..ooHHHhhhho....
.oHHHhhhhhhho...
oHHHhhhhhhhhwo..
.oHHhehhhhhwo...
..oHhhhhhhhwo...
...ohhhhhwwo....
....ohhwwwo.....
.....owwoo......
......oo........
"""

# Odd ones.

ANGLER = """
................
.....ooo........
....o...o.......
.ooo.....o..oo..
oGLGo...ooooFFo.
oGLGo.ooKKKFfFo.
.oGoooKKHHhwFFo.
..ooKKHHHhhhwo..
..oKHHHeHhhhwo..
.oKHHHhhhhhWwo..
.omtmtmhhhWWwo..
.ommmmmmhWWwo...
.omtmtmhWWwwo...
..ohWWWwwwoo....
...owwwwoo......
....oooo........
"""

MONK = """
...........oo...
..........oFFo..
...X......oFfFo.
....o..oo.oFffFo
.....ooDDooFfffo
.....ooDKKhoooo.
....oDKKKhwo....
..ooeKKHhwwo....
.oKKKHHhWwo.....
oKKHHHhWwwo.....
omHHHhWWwo......
otmHhhWwwo......
.otmhWWwfo......
..otmWwwfFo.....
...otmwooFo.....
....ooo..o......
"""

LION = """
................
.o.o............
odoDo.o...oo....
.oDodoDo.oFFo...
oDodoDddooFfFo..
.odoDdKKKKfffo..
odoDdKKHHhwoo...
.oDdKKHHhWwo....
..oKKHHhWWwo....
..oKHHhWWwwo....
..oKHhWWwwFo....
..oKeWWwwFFfo...
..ohwwwwFFfo....
...ooooFFfoFo...
.......ofoFo....
........o.o.....
"""

MUDSKIPPER = """
...........oo...
..........oFFo..
........o.oFfFo.
..oo..ooDooFffFo
.oDDooDDdKKffffo
.oDdDoDKKKhwooo.
..oDdKKKhhwwo...
..oDKKHHhwwo....
.oEKKHHWWwo.....
oEeHHHWWwwo.....
oeHHhWWwwo......
.oHhWWwwo.......
.oKWWwwo........
..owwwfFo.......
...ooooFFo......
.......oo.......
"""

# Shellfish and the rest of the sea bed.

CRAYFISH = """
............oo..
..........ooFFo.
.........oFFfFFo
.........oFfFfo.
..oo....ohKhKo..
.oHHo..oHhKhwo..
oHhhHooHhKhwo...
oHhohHHHhhwo....
.ohohHHHhhwo....
..ooHHhhhwo.....
...oeHhhwo......
...xohhwo.......
..xoHHhwo.......
.xoHhhHho.......
.ohwoohwo.......
..oo..oo........
"""

CRAB = """
................
................
................
.o...oooooo...o.
..o.oHHHHHHooo..
...oHHHHhhhhwo..
.ooHHHhhhhhhhwoo
..oHHhhhhhhhhwo.
.ooHhhhhhhhhhwoo
..oohhhhhhhhwoo.
..ooowhhhhhwoo..
.oHHooeKKeooHHo.
oHhhHooooooHhhHo
oHhoho....ohohwo
.ohwo......owho.
..oo........oo..
"""

SHRIMP = """
................
.......oooo.....
.....ooKKKKo....
....oKKHHHhwo...
...oKHHhhhhhwo..
..oKHHhwwwhhhwo.
..oKHhwooowhhwo.
.oKHhhwo..ohhwo.
.oKHhwo...owhwo.
.oKHhwo....oFFo.
.oeHhwo...oFfFo.
..ohhwo....oFo..
..xofofo....o...
.x..o.o.........
x...............
................
"""

OYSTER = """
................
..........ooo...
........ooHHHo..
.......oHHHhhho.
......oHHKKKKhho
.....oHHKhhhhKwo
....oHHKhHHHhKwo
...oHHKhHhhhKhwo
...oHKhHhKKhKhwo
..oHHKhHKhhKhwwo
..oHKhhKhhKhwwo.
..oHKhhhKKhwwo..
..ohKKhhhhwwo...
...ohwKKKwwo....
....owwwwoo.....
.....oooo.......
"""

OCTOPUS = """
......ooo.......
.....oHHHo......
....oHHHhho.....
...oHHHhhhho....
...oHHhhhhho....
...oHHhhhhwo....
...oHehhhEwo....
...ohhhhhhwo....
..ohhhhhhhhwo...
.ohhohhohhohwo..
ohhoohhoohhohwo.
ohoohho.ohhoohwo
ohhoho.ohho.ohwo
.ohohhooho.ohwo.
..o.oho.o...owo.
.....o.......o..
"""

JELLY = """
................
.....oooooo.....
...ooHHHHHHoo...
..oHHHHhhhhhho..
.oHHHhhhhhhhhwo.
.oHhhKhhhhKhhwo.
oHHhKhKhhKhKhhwo
oHhhhKhhhhKhhhwo
ohhhhhhhhhhhhwwo
owwwwwwwwwwwwwwo
.ooFoFFooFFoFoo.
..oFoFoFoFooFo..
...oFooFoFoFo...
..oFo.oFooFoFo..
...o..oFo.o.o...
.......o........
"""

CUCUMBER = """
................
................
................
.........o.o.o..
.......ooHoHoHo.
.....ooHoHHHHHHo
....oHoHHhhhhhwo
...oHHHHhhhhhwwo
..oHHhhhhhhhwwo.
.oFHhhhhhhwwwo..
oFfHhhhhwwwoo...
oFfhhhwwKKo.....
.oFwwKKooo......
..ooooo.........
................
................
"""

# The legends: bigger bodies, closer to the corners.

GREAT_WHISKERED = """
...........oo...
..........oFFo..
..........oFfoo.
......oooooFfFFo
...oooKKKKKffffo
..oDDKKHHHhwooo.
..oKKKHHhWWwo...
.oKKHHHhhWwwo...
.oKHHHHhWWwfFo..
oKKHHHhhWwwfo...
oKHHHghWWwffo...
.oHehhgWwwoo....
.oKhhWgwwo......
.xowWWwwo.......
x.xoowwo........
x..x.oo.........
"""

GREAT_DEEP = """
...o.o.....oo...
..oDoDo...oFFo..
.oDdDdDo..oFfoo.
.oDdKKKKoooFfFFo
..oKKKKHHKKffffo
.oKKKKHHHhhwooo.
.oKKKHHhhhWwo...
oKKKHHhhhWWwo...
oKKKHhhhhWWwo...
oKKHHhhhWWWwo...
.oHHghhWWWWwo...
.oKehgWWWWwwo...
.oKhhWWWWwwo....
..owwWWwwwfFo...
...ooowwoooo....
......oo........
"""

GREAT_SPINY = """
.o.o.o.....oo...
oDoDoDo...oFFo..
.oDdDdDo..oFfoo.
.oDddddDoooFfFFo
..oDKKKKKKKffffo
..oKKKHHHHhwooo.
.oKKKKHHHhWwo...
.oKKKHHhhhWwo...
oKKHHHhhWWWwo...
oKHHHhhWWWwwFo..
oKHHghWWWWwoFo..
.oHehgWWWwwoo...
.oKWWWWwwwo.....
.ohwwwwwoFFo....
..oooooo.ooFo...
...........o....
"""

GREAT_PIKE = """
...........oo...
......o...oFFo..
.....oDoo.oFfoo.
.....oDDDooFfFFo
.....oKKKKKffffo
....oKKHHHhwooo.
...oKKHHhhWwo...
..oKKHHhhWWwFo..
.oKKHHhhWWwwfo..
.oKHHhhWWwwoFo..
oKKHhhWWwwo.o...
oKHHgWWwwo......
oKeWWgwwo.......
ohhWwwwo........
.oowwoo.........
...oo...........
"""

GREAT_STURGEON = """
..........o.....
.........oFo....
.....o...oFFo...
....oDoo.oFfo...
....oDKKooFfFo..
....oKKHHKfffo..
...oKKHHhWwoo...
..oKKHHhhWwo....
.oKKHHhhWWwo....
.oKHHhhWWwwFo...
.oKHghWWwwoFo...
oKKehgWwwo.o....
oKhhWWwwo.......
.owwwwwo........
..ooooo.........
................
"""

GREAT_SHARK = """
............oo..
......o....oFFo.
.....oDo..oFffo.
....oDdo.oFffo..
...oDddoooFffo..
...oDddKKKfffFo.
...oDKKKHhwooo..
..oKKKHHhWwo....
.oKKHHHhWwwo....
.oKHHhhWWwo.....
.oKHhhWWwwo.....
oKKHWggwwo......
oKehWwwwo.......
ohwwwwffFo......
.oooooFffo......
......ooo.......
"""

GREAT_ANGLER = """
....ooo.........
...o...o...oo...
.oooo...o.oFFo..
oGLLGo.oooFfFo..
oGLLGooKKKKfFFo.
.oGGoKKKHHHhfFo.
..oKKHHHHHhhwo..
.oKHHHHHhhhhwo..
.oKHHHeHhhhWwo..
oKHHHhhhhhWWwo..
omtmtmhhhhWWwo..
ommmmmmhhWWwo...
omtmtmhhWWwwo...
.ohWWWWwwwoo....
..owwwwwoo......
...ooooo........
"""

GREAT_EEL = """
...........oooo.
.........ooKKFFo
........oKKHHhFo
.......oKHHhWwo.
......oKHhWWwo..
......oKHhWwo...
.....oKHhWwo....
.....oKHhWwo....
....oKHhWwo.....
....oKHhWwo.....
..ooKHhWwo......
.oKKHhWWwo......
oKHHhWwwo.......
oKeWWwwo........
.owwwoo.........
..ooo...........
"""

GREAT_AROWANA = """
...........oo...
.....oo...oFFo..
....oDDoo.oFfFo.
....oDdDDooFffFo
.....oKKKKKffffo
....oKKHHHhwooo.
...oKKHHhWWwo...
..oKKHHhhWwwFo..
.oKKHHhhWWwffo..
.oKHHHhWWwwffFo.
.oKHHhhWwwfffo..
oKKHghWWwoooFo..
oKeHWgWwwo..o...
ohhWWwwwo.......
xoowwwoo........
.x.ooo..........
"""


# -- fish -------------------------------------------------------------------------------------------
# Rivers and lakes ----------------------------------------------------------------------------------

@fish('minnow')
def _():
    # olive back, a dark stripe down the side, silver below
    return draw(SMALL, {'o': '2A3024', 'K': '5E6A48', 'H': 'B8C0A4', 'h': '5A6650', 'W': 'EEF0E6', 'w': '9AA294',
                        'f': '8A9478', 'F': 'B4BCA4', 'e': '101410', 'g': '7E8874'})


@fish('gudgeon')
def _():
    colours = {'o': '2E2618', 'K': '6A5A3A', 'H': 'C8B890', 'h': 'A08C64', 'W': 'EEE6D0', 'w': '9A8A6A',
               'f': '9C8A64', 'F': 'C4B48C', 'e': '1A1410', 'g': '8A7858', 'x': '8A7858', 'b': '4E4028'}
    return draw(GUDGEON, colours, along(GUDGEON, 'b', 0.3, 0.6, ends=(-5, 4), every=3))


@fish('roach')
def _():
    # silver, with red fins and a red eye
    return draw(TORPEDO, {'o': '26303A', 'K': '4A6670', 'H': 'D8E0E0', 'h': 'A8B8BC', 'W': 'F4F6F2', 'w': '8C9CA4',
                          'f': 'C84A30', 'F': 'E87A50', 'd': '8A9AA0', 'D': 'B0BCC0', 'e': 'C82828', 'g': '8A9AA2'})


@fish('dace')
def _():
    return draw(SLENDER, {'o': '2A3440', 'K': '5A7088', 'H': 'DCE4EA', 'h': 'B4C2CC', 'W': 'F6F8F8', 'w': '90A0AC',
                          'f': 'C8C090', 'F': 'E4DCB0', 'e': '141820', 'g': '90A0AC'})


@fish('chub')
def _():
    # bronze, big dark-edged scales, reddish lower fins
    colours = {'o': '2E2618', 'K': '5A5030', 'H': 'D8C890', 'h': 'B4A06A', 'W': 'F0E8D0', 'w': '8C7C58',
               'f': 'B8583A', 'F': 'D88050', 'd': '6E6040', 'D': '948458', 'e': '141008', 'g': '7C6C48', 'n': '8E7C50'}
    return draw(TORPEDO, colours, lattice(TORPEDO, 'n', 'HhW'))


@fish('perch')
def _():
    # green-gold with dark bars, a spiny dorsal, orange-red lower fins
    colours = {'o': '263018', 'K': '4E6024', 'H': 'C8CC6A', 'h': '9CA848', 'W': 'F0EAC8', 'w': '8C9450',
               'f': 'D8642A', 'F': 'F09858', 'd': '5E6E34', 'D': '8E9A58', 'e': '141008', 'g': '6E7A34', 'b': '34421A'}
    return draw(SPINY, colours, bars(SPINY, 'b', (-6, -5, -2, -1, 2, 3)))


@fish('carp')
def _():
    colours = {'o': '3A2610', 'K': '6E5020', 'H': 'D8B060', 'h': 'B48C3C', 'W': 'F2E0A8', 'w': '8E6A30',
               'f': '9A6A30', 'F': 'C09048', 'e': '141008', 'g': '8E6A30', 'n': '9A7432'}
    return draw(DEEP, colours, lattice(DEEP, 'n', 'Hh'))


@fish('tench')
def _():
    # slimy olive-green with a small red eye
    return draw(TORPEDO, {'o': '1A2410', 'K': '2E4A1E', 'H': '8EA448', 'h': '5E7E30', 'W': 'C0BE68', 'w': '4A6024',
                          'f': '34481E', 'F': '50682A', 'e': 'C83020', 'g': '3E5A24'})


@fish('bluegill')
def _():
    # olive with faint bars, an orange breast, a blue cheek and the black ear flap
    colours = {'o': '1E2830', 'K': '3A5050', 'H': '8AA088', 'h': '6A8070', 'W': 'F0A838', 'w': 'B87A28',
               'f': '4A6060', 'F': '7A9090', 'e': '141414', 'g': '101010', 'b': '58705E', 'c': '5A98C8'}
    return draw(DEEP, colours, bars(DEEP, 'b', (-5, -4, -1, 0, 3, 4)), ('c', 3, 12), ('g', 5, 10))


@fish('whitefish')
def _():
    return draw(SLENDER, {'o': '3A3C40', 'K': '7A7E80', 'H': 'EEF0EE', 'h': 'CCD2D2', 'W': 'FAFAF6', 'w': 'A8AEB0',
                          'f': 'B8BCBE', 'F': 'DCE0E0', 'e': '141414', 'g': 'A8AEB0'})


@fish('tilapia')
def _():
    colours = {'o': '2A2C30', 'K': '5A6068', 'H': 'B8C0C4', 'h': '8E989E', 'W': 'E2E6E4', 'w': '7A848A',
               'f': 'A84C3C', 'F': 'C87060', 'd': '6A7078', 'D': '9AA0A8', 'e': '1A1414', 'g': '6A7078', 'b': '7E888E'}
    return draw(DEEP, colours, bars(DEEP, 'b', (-5, -1, 3)))


@fish('crayfish')
def _():
    return draw(CRAYFISH, {'o': '3A1A0E', 'H': 'D8844A', 'h': 'A8542A', 'w': '74321A', 'K': '4A1E0E',
                           'f': 'B05A2C', 'F': 'E09A60', 'e': '101010', 'x': '6A3418'})


@fish('blindfish')
def _():
    # pale pink, and no eye at all
    return draw(SMALL, {'o': '8A6A70', 'K': 'D8B8BC', 'H': 'FFF0F0', 'h': 'F0D8DC', 'W': 'FFF8F8', 'w': 'C8A8AE',
                        'f': 'E8C8CC', 'F': 'FFE8EC', 'e': 'E0C4C8', 'g': 'D8B8BC'})


@fish('bream')
def _():
    return draw(DEEP, {'o': '2E2410', 'K': '5A4A24', 'H': 'C8A860', 'h': 'A48440', 'W': 'E8D8A8', 'w': '7A6230',
                       'f': '4A3C24', 'F': '6E5A38', 'e': '141008', 'g': '7A6230'})


@fish('pike')
def _():
    # green, with rows of pale bean-shaped spots
    colours = {'o': '1E2A14', 'K': '3E5422', 'H': '7E9A44', 'h': '5E7A34', 'W': 'E8E8C8', 'w': '8A9668',
               'f': '8A6A36', 'F': 'B08C50', 'e': '141008', 'g': '4E6A2A', 'p': 'D8DCA0'}
    return draw(PIKE, colours, lattice(PIKE, 'p', 'KH', 3, 0, 1))


@fish('brown_trout')
def _():
    # golden brown, black spots on the back, red ones on the side
    colours = {'o': '2E2210', 'K': '6A4E24', 'H': 'D8B868', 'h': 'B89448', 'W': 'F4E8C4', 'w': '8E7040',
               'f': '8A6A38', 'F': 'B08C50', 'e': '141008', 'g': '8E7040', 'r': 'C83A20', 'k': '2A1C10'}
    return draw(TORPEDO, colours, spots(TORPEDO, 'k', 'KH', 5), spots(TORPEDO, 'r', 'hW', 5, 2))


@fish('rainbow_trout')
def _():
    # olive back, a pink stripe down the side, black spots on the back and tail
    colours = {'o': '26301C', 'K': '4E6A3A', 'H': 'B8C8A0', 'h': 'B8C8A0', 'W': 'F4F2EC', 'w': '98A498',
               'f': '7A8A64', 'F': 'A0B088', 'e': '141410', 'g': 'B85A6A', 'k': '2A3020', 'p': 'E0788A'}
    return draw(TORPEDO, colours, along(TORPEDO, 'p', 0.4, 0.62, on='HhW'), spots(TORPEDO, 'k', 'KHfF'))


@fish('barbel')
def _():
    return draw(WHISKERED, {'o': '2E2414', 'K': '5E4A26', 'H': 'C8A868', 'h': 'A08448', 'W': 'ECDCB4', 'w': '7E6638',
                            'f': 'B0603A', 'F': 'D08458', 'd': '6E5A34', 'D': '9A8050', 'e': '141008', 'g': '7E6638',
                            'x': 'E0B890'})


@fish('river_eel')
def _():
    return draw(EEL, {'o': '1E1A0E', 'K': '3E3A1E', 'H': '6A6430', 'h': '8A8240', 'W': 'D8C060', 'w': 'A08A3A',
                      'f': '3E3A1E', 'F': '5A5428', 'e': '101008', 'g': '3E3A1E'})


@fish('largemouth_bass')
def _():
    # green, a dark blotchy stripe from gill to tail, a red eye
    colours = {'o': '1E2A14', 'K': '3E5A24', 'H': '9AB060', 'h': '7A9648', 'W': 'ECEAC4', 'w': '8C9660',
               'f': '6E8044', 'F': '98AA64', 'e': '8A2410', 'g': '4E6A2E', 'b': '2E3E1A'}
    return draw(SPINY, colours, along(SPINY, 'b', 0.35, 0.6, ends=(-6, 99)))


@fish('smallmouth_bass')
def _():
    colours = {'o': '2E2010', 'K': '5E4224', 'H': 'B89458', 'h': '9A7840', 'W': 'E8D8B0', 'w': '7E6236',
               'f': '8A6A3A', 'F': 'B08C54', 'e': 'C83020', 'g': '6E5230', 'b': '5A3E1E'}
    return draw(SPINY, colours, bars(SPINY, 'b', (-5, -4, -1, 0, 3, 4)))


@fish('arctic_char')
def _():
    # dark back with pale spots, a belly like a winter sunset, white-edged fins
    colours = {'o': '1E2620', 'K': '3E4E40', 'H': '6E7E6A', 'h': '8A8A70', 'W': 'E85A3A', 'w': 'B03A24',
               'f': 'C84A30', 'F': 'F4F0E8', 'd': '4E5E50', 'D': '7E8E7E', 'e': '141414', 'g': '4E5E50', 'p': 'F0C8B8'}
    return draw(TORPEDO, colours, spots(TORPEDO, 'p', 'KH', 4, 1))


@fish('lamprey')
def _():
    # a round sucking mouth and a row of gill holes
    colours = {'o': '2A2620', 'K': '4E463A', 'H': '8A8070', 'h': '726A5A', 'W': 'B0A890', 'w': '6E6656',
               'f': '4E463A', 'F': '6E6656', 'e': '141414', 'g': '4E463A', 'm': '1A1410', 'p': '2E2820'}
    return draw(EEL, colours, ('m', 1, 13), along(EEL, 'p', 0.3, 0.6, ends=(-9, -4), every=2))


@fish('desert_pupfish')
def _():
    return draw(SMALL, {'o': '102850', 'K': '2A60B0', 'H': '7AC0F8', 'h': '4A90E0', 'W': 'C8E8FF', 'w': '3A70C0',
                        'f': '1A3A70', 'F': '4A90E0', 'e': '101420', 'g': '3A70C0'})


@fish('piranha')
def _():
    # grey back, a red belly and a mouthful of teeth
    return draw(DEEP, {'o': '2A2A30', 'K': '5A5E68', 'H': 'B8BCC4', 'h': '8E949E', 'W': 'D84A3A', 'w': 'A0302A',
                       'f': '6A6E78', 'F': '9A9EA8', 'e': 'B02020', 'g': '6A6E78', 't': 'FFFFFF'}, ('t', 3, 12))


@fish('bowfin')
def _():
    # olive, a long dorsal fin, and a dark eyespot ringed with orange at the tail
    colours = {'o': '1E2414', 'K': '3A4A24', 'H': '7A8848', 'h': '5E6E36', 'W': 'C8C890', 'w': '6A7040',
               'd': '4E6030', 'D': '7A9050', 'f': '4E6030', 'F': '6E8040', 'e': '141008', 'g': '3A4A24',
               'k': '141008', 'r': 'E09030'}
    return draw(LONGFIN, colours, ("""
rk
.r
""", 9, 4))


@fish('mudskipper')
def _():
    colours = {'o': '2A2418', 'K': '5A4E38', 'H': 'A89A78', 'h': '86785A', 'W': 'D8CCB0', 'w': '6E6248',
               'f': '6A5E46', 'F': '9A8C6C', 'e': '101010', 'E': 'C8D0C8', 'g': '6E6248', 'b': '7AB8E8'}
    return draw(MUDSKIPPER, colours, spots(MUDSKIPPER, 'b', 'Hh'))


@fish('stone_loach')
def _():
    # mottled yellow-brown with dark saddles over the back
    colours = {'o': '2A2210', 'K': '5A4A24', 'H': 'C8B470', 'h': 'A89050', 'W': 'E8DCB0', 'w': '7E6A38',
               'f': 'A89060', 'F': 'C8B080', 'e': '141008', 'g': '7E6A38', 'x': 'A08A60', 'b': '4A3A18'}
    return draw(GUDGEON, colours, bars(GUDGEON, 'b', (-4, -3, 0, 1, 4)))


@fish('zander')
def _():
    # grey-green, faint bars, a spiny first dorsal and glassy eyes
    colours = {'o': '22282A', 'K': '4A5650', 'H': 'A8B4AC', 'h': '849088', 'W': 'E8ECE4', 'w': '7A8680',
               'f': '8A9690', 'F': 'B0BCB6', 'd': '5A6660', 'D': '8A9690', 'e': 'D8E8C0', 'g': '5A6660', 'b': '6A766E'}
    return draw(PIKEPERCH, colours, bars(PIKEPERCH, 'b', (-6, -5, -2, -1, 2, 3)))


@fish('grayling')
def _():
    # silver-grey with a purple sail spotted red
    colours = {'o': '2A2830', 'K': '5A5868', 'H': 'C8C8D0', 'h': '9A9AAA', 'W': 'ECECF0', 'w': '7E7E8E',
               'd': '6A4A78', 'D': 'A070B0', 'f': '7A7488', 'F': 'A8A0B8', 'e': '141414', 'g': '7E7E8E', 'r': 'E04050',
               'k': '3A3848'}
    return draw(SAIL, colours, where(SAIL, 'r', lambda x, y, ch: ch == 'd' and (x + y) % 3 == 0),
                where(SAIL, 'k', lambda x, y, ch: ch in 'H' and (x - y) < -4 and (x + 2 * y) % 4 == 0))


@fish('catfish')
def _():
    return draw(WHISKERED, {'o': '1A1E1A', 'K': '3A423A', 'H': '6A766A', 'h': '525C52', 'W': 'C8CCB8', 'w': '6A7266',
                            'f': '3A423A', 'F': '5A645A', 'e': '101010', 'g': '3A423A', 'x': '8A968A'})


@fish('golden_carp')
def _():
    # a carp the colour of a crown, its scales catching the light
    colours = {'o': '5A3808', 'K': 'C08018', 'H': 'FFE070', 'h': 'F0B830', 'W': 'FFF4C0', 'w': 'C88A20',
               'f': 'E89020', 'F': 'FFC050', 'e': '1A1008', 'g': 'C88A20', 'n': 'D89A20', 'z': 'FFFDE8'}
    return draw(DEEP, colours, lattice(DEEP, 'n', 'Hh'),
                lattice(DEEP, 'z', 'H', 4, 2))


@fish('burbot')
def _():
    # marbled yellow-brown, an eel-like cod with one chin barbel
    colours = {'o': '2A2410', 'K': '5A4A20', 'H': 'B8A050', 'h': '8E7838', 'W': 'E0D4A0', 'w': '6E5E30',
               'f': '6E5E30', 'F': '9A8848', 'e': '141008', 'g': '5A4A20', 'x': '8E7838', 'b': '4A3A18'}
    return draw(WHISKERED, colours, where(WHISKERED, 'b', lambda x, y, ch: ch in 'KHh' and (2 * x + y) % 5 == 0))


@fish('arowana')
def _():
    # silver, big scales edged with pink, two chin barbels
    colours = {'o': '3A3438', 'K': '7A7480', 'H': 'E8E4EC', 'h': 'C8C2CC', 'W': 'F8F4F4', 'w': 'A49EAA',
               'f': 'C89090', 'F': 'E8B4B0', 'e': '141414', 'g': 'A49EAA', 'x': 'B8B0B8', 'n': 'E0A0A4'}
    return draw(AROWANA, colours, lattice(AROWANA, 'n', 'HhW', 3, 0, 1))


@fish('nile_perch')
def _():
    # a silver giant with a glowing yellow eye
    return draw(SPINY, {'o': '2A3038', 'K': '5A6878', 'H': 'D8E0E6', 'h': 'B0BCC6', 'W': 'F4F6F8', 'w': '8A98A6',
                        'f': '8A98A6', 'F': 'B8C4D0', 'd': '6A7888', 'D': '9AA8B6', 'e': 'F0D040', 'g': '8A98A6'})


@fish('snakehead')
def _():
    colours = {'o': '241C14', 'K': '4E3A26', 'H': '9A7A52', 'h': '7A5E3E', 'W': 'D8C8A8', 'w': '6A5236',
               'f': '4E3A26', 'F': '7A5E3E', 'e': 'C8A030', 'g': '4E3A26', 'b': '2E2218'}
    return draw(LONGFIN, colours, spots(LONGFIN, 'b', 'KHh'))


@fish('gar')
def _():
    colours = {'o': '242414', 'K': '4E5028', 'H': 'A8A870', 'h': '868858', 'W': 'E0DEC0', 'w': '6E7048',
               'f': '6E7048', 'F': '9A9A68', 'e': '141008', 'g': '4E5028', 'b': '3A3A1C'}
    return draw(GAR, colours, spots(GAR, 'b', 'Hhf', 4, 1))


@fish('glow_minnow')
def _():
    # dark at the edges, glowing at the core
    return draw(SMALL, {'o': '0E1A2A', 'K': '1E3A5A', 'H': '7AF0E8', 'h': 'C8FFF8', 'W': '3AC8D8', 'w': '2A7090',
                        'f': '2A5A80', 'F': '5AB8D8', 'e': '0A1018', 'g': '2A7090'})


@fish('oasis_tetra')
def _():
    # a neon-blue stripe, red behind, silver below
    colours = {'o': '1A2028', 'K': '3A4A40', 'H': 'B8C8C8', 'h': 'B8C8C8', 'W': 'E8F0F0', 'w': '8A98A0',
               'f': 'C0C8C8', 'F': 'E0E8E8', 'e': '141414', 'g': '8A98A0', 'n': '3AD8F0', 'r': 'D83040'}
    return draw(SMALL, colours, along(SMALL, 'r', 0.55, 1, ends=(-5, 99)), along(SMALL, 'n', 0.2, 0.5, ends=(-8, 99)))


@fish('sturgeon')
def _():
    # grey-brown, armoured with rows of pale bony plates, barbels under the snout
    colours = {'o': '222420', 'K': '4A4E46', 'H': '9A9E90', 'h': '7A7E72', 'W': 'D8D8C8', 'w': '6A6E62',
               'f': '5A5E54', 'F': '8A8E80', 'e': '141414', 'g': '4A4E46', 's': 'E8E8D8', 'x': 'C8C8B8'}
    return draw(STURGEON, colours, where(STURGEON, 's', lambda x, y, ch: ch == 'K' and (x - y) % 2 == 0),
                along(STURGEON, 's', 0.45, 0.6, ends=(-7, 99), every=2))


@fish('ghost_catfish')
def _():
    # so pale its spine and ribs show through
    colours = {'o': '7A8088', 'K': 'C8D0D8', 'H': 'F4F8FC', 'h': 'E0E8F0', 'W': 'FFFFFF', 'w': 'B8C0CA',
               'f': 'D8E0E8', 'F': 'F0F4F8', 'e': '2A3040', 'g': 'B8C0CA', 'x': 'A8B0BA', 'b': 'B0BCC8'}
    return draw(WHISKERED, colours, along(WHISKERED, 'b', 0.3, 0.42, ends=(-6, 99)),
                bars(WHISKERED, 'b', (-4, -2, 0, 2), on='Hh'))


# The sea -------------------------------------------------------------------------------------------

@fish('herring')
def _():
    return draw(SLENDER, {'o': '1E2E3A', 'K': '3A6080', 'H': 'D0E0E8', 'h': 'A8C0CC', 'W': 'F4F8FA', 'w': '7E98A8',
                          'f': '8A9EAC', 'F': 'B8C8D2', 'e': '101418', 'g': '7E98A8'})


@fish('sardine')
def _():
    # blue back and a row of dark spots along the shoulder
    colours = {'o': '1A2840', 'K': '2E5A8A', 'H': 'D8E4EC', 'h': 'B0C4D0', 'W': 'F6F8FA', 'w': '8498A8',
               'f': '8AA0B4', 'F': 'B8C8D6', 'e': '101418', 'g': '8498A8', 'b': '1E3A5A'}
    return draw(SLENDER, colours, along(SLENDER, 'b', 0.25, 0.45, ends=(-6, 3), every=2))


@fish('anchovy')
def _():
    # green-blue back and a bright silver stripe
    return draw(SMALL, {'o': '1E2E30', 'K': '3E6A68', 'H': '8AAEAE', 'h': 'F0F8F8', 'W': 'D8E4E4', 'w': '7E9A9C',
                        'f': '8AA4A4', 'F': 'B4CACA', 'e': '101414', 'g': '7E9A9C'})


@fish('mackerel')
def _():
    # blue-green back barred with black, silver-white below
    colours = {'o': '142630', 'K': '2A6A70', 'H': '4A9A98', 'h': 'D8E4E8', 'W': 'F8FAFA', 'w': '98A8B0',
               'f': '4A6A78', 'F': '7A9AA8', 'e': '101418', 'g': '98A8B0', 'b': '102028'}
    return draw(TORPEDO, colours, bars(TORPEDO, 'b', (-6, -5, -3, -1, 0, 2, 4), on='KH'))


@fish('mullet')
def _():
    # grey, with thin dark stripes running nose to tail
    colours = {'o': '2A3038', 'K': '5A6470', 'H': 'C0C8D0', 'h': 'B0B8C2', 'W': 'EEF0F2', 'w': '7E8892',
               'f': '7A8490', 'F': 'A4ACB6', 'e': '141418', 'g': '7E8892', 'b': '6A7480'}
    return draw(TORPEDO, colours, along(TORPEDO, 'b', 0.25, 0.4, ends=(-6, 99)),
                along(TORPEDO, 'b', 0.55, 0.7, ends=(-6, 99)))


@fish('pollock')
def _():
    # olive-brown with a pale curving lateral line
    colours = {'o': '1E2418', 'K': '3E4A2E', 'H': '7A8A5A', 'h': '9AA478', 'W': 'E8E8D0', 'w': '8A9070',
               'f': '4E5A38', 'F': '7A8A5A', 'e': '141410', 'g': '4E5A38', 'l': 'D8E0B8'}
    return draw(TORPEDO, colours, along(TORPEDO, 'l', 0.3, 0.4, ends=(-6, 99)))


@fish('sea_bream')
def _():
    # silver-pink with a gold band between the eyes
    return draw(DEEP, {'o': '3A2E34', 'K': '7A6878', 'H': 'E8D8E0', 'h': 'C8B4C0', 'W': 'FAF2F4', 'w': 'A08C98',
                       'f': 'B89AA8', 'F': 'D8C0CC', 'e': '141414', 'g': 'A08C98', 'y': 'F0C040'}, ('yy', 2, 10))


@fish('shore_crab')
def _():
    return draw(CRAB, {'o': '1E2414', 'H': '7A8A3A', 'h': '5A6A2A', 'w': '3E4A1E', 'K': '2E3818', 'e': '101010'})


@fish('shrimp')
def _():
    return draw(SHRIMP, {'o': '6A4A48', 'H': 'F0D0C8', 'h': 'D8A8A0', 'w': 'B07E78', 'K': 'C08880',
                         'f': 'E0B0A8', 'F': 'F8D8D0', 'e': '101010', 'x': 'A07A74'})


@fish('sea_cucumber')
def _():
    # a warty brown lump, a frill of feeding tentacles at one end
    colours = {'o': '2A1410', 'H': 'A0583A', 'h': '7A3E28', 'w': '5A2A1C', 'K': '4A2016',
               'F': 'E8C8A0', 'f': 'C89A78', 'p': 'C8805A'}
    return draw(CUCUMBER, colours, spots(CUCUMBER, 'p', 'h'))


@fish('arctic_cod')
def _():
    colours = {'o': '2E2A24', 'K': '6A6050', 'H': 'C8C0A8', 'h': 'A89E86', 'W': 'F2EEE2', 'w': '8A806C',
               'f': '8A806C', 'F': 'B0A890', 'e': '141414', 'g': '8A806C', 'b': '7A6E58'}
    return draw(TORPEDO, colours, spots(TORPEDO, 'b', 'KHh'))


@fish('sea_bass')
def _():
    # silver with a dark blue-grey back and a dark spot on the gill cover
    return draw(SPINY, {'o': '222A34', 'K': '4A5A6E', 'H': 'C8D0D8', 'h': 'A0AAB6', 'W': 'F2F4F6', 'w': '7E8896',
                        'f': '6A7686', 'F': '98A2B0', 'e': '141418', 'g': '2A3440'})


@fish('haddock')
def _():
    # a black lateral line and the dark thumbprint above the fin
    colours = {'o': '2A2630', 'K': '5A5268', 'H': 'B8B4C4', 'h': '9E98AC', 'W': 'F0EEF2', 'w': '7E7890',
               'f': '5A5268', 'F': '8A849A', 'e': '141414', 'g': '5A5268', 'k': '1E1A24'}
    return draw(TORPEDO, colours, along(TORPEDO, 'k', 0.28, 0.36, ends=(-6, 99)), ("""
k.
kk
""", 6, 9))


@fish('flounder')
def _():
    colours = {'o': '2E2416', 'H': 'A08458', 'h': '806840', 'w': '5E4A2C', 'F': 'C0A478', 'f': '8E7450',
               'e': '141008', 'r': 'D8843A'}
    return draw(FLAT, colours, spots(FLAT, 'r', 'Hh', 5))


@fish('red_snapper')
def _():
    return draw(SPINY, {'o': '4A1418', 'K': 'A0303A', 'H': 'F08080', 'h': 'D85058', 'W': 'F8D0C8', 'w': 'B04048',
                        'f': 'D85058', 'F': 'F0A0A0', 'd': 'C8404A', 'D': 'E87078', 'e': 'B02020', 'g': 'B04048'})


@fish('conger_eel')
def _():
    return draw(EEL, {'o': '1E2228', 'K': '4A525C', 'H': '8A929A', 'h': '6E767E', 'W': 'D8DCDE', 'w': '7A8288',
                      'f': '2A3038', 'F': '4A525C', 'e': '101418', 'g': '4A525C'})


@fish('dogfish')
def _():
    # a small sandy shark, freckled dark
    colours = {'o': '3A2E20', 'K': '8A7454', 'H': 'D8C4A0', 'h': 'B8A07A', 'W': 'F4ECDC', 'w': '9A8660',
               'f': '8A7454', 'F': 'B8A07A', 'e': '141414', 'g': '6A5636', 'b': '4A3A28'}
    return draw(SHARK, colours, spots(SHARK, 'b', 'KHh'))


@fish('lobster')
def _():
    # blue-black in the water, orange feelers
    return draw(CRAYFISH, {'o': '0A0E18', 'H': '4A6E9E', 'h': '2A4470', 'w': '18284A', 'K': '0C1428',
                           'f': '2A4A78', 'F': '6A8AB8', 'e': '101010', 'x': 'D87A40'})


@fish('oyster')
def _():
    return draw(OYSTER, {'o': '2E2C28', 'H': 'C8C4B8', 'h': '9E9A8E', 'w': '6E6A60', 'K': '5A564C'})


@fish('moon_jelly')
def _():
    return draw(JELLY, {'o': '6A7AA8', 'H': 'F0F4FF', 'h': 'D0DAF4', 'w': 'A8B4DC', 'K': 'B488D0',
                        'f': 'C8D2F0', 'F': 'E8EEFF', 'x': '9AA6CC'})


@fish('halibut')
def _():
    colours = {'o': '1E1C14', 'H': '6A6448', 'h': '4E4A34', 'w': '363424', 'F': '8A845E', 'f': '5E5840',
               'e': '141008', 'b': '3A3626', 'p': '8A8466'}
    return draw(FLAT_LONG, colours, spots(FLAT_LONG, 'b', 'Hh'),
                spots(FLAT_LONG, 'p', 'h', 4, 2))


@fish('tuna')
def _():
    return draw(TUNA, {'o': '0E1A2E', 'K': '1E3A6A', 'H': '3A5E90', 'h': 'C8D4E0', 'W': 'F2F6FA', 'w': '8A9AAC',
                       'f': '2A4A78', 'F': '5A7AAA', 'e': '101418', 'g': '1E3A6A'})


@fish('mahi_mahi')
def _():
    colours = {'o': '1A3020', 'K': '2A8A5A', 'H': '8AD050', 'h': 'F0D030', 'W': 'F8F0A0', 'w': 'C0A020',
               'd': '2A7AA8', 'D': '4AA8D8', 'f': 'D0B020', 'F': 'F0E070', 'e': '141414', 'g': '2A8A5A', 'b': '3A7AC8'}
    return draw(MAHI, colours, spots(MAHI, 'b', 'Hh'))


@fish('monkfish')
def _():
    colours = {'o': '2A1C14', 'K': '4A3020', 'H': 'A07850', 'h': '7E5A3A', 'W': 'C8A478', 'w': '5A3E28',
               'f': '8E6A48', 'F': 'C8A478', 'e': '101010', 'g': '5A3E28', 't': 'F0E8D8', 'm': '2A1410', 'X': 'D8B888',
               'b': '5A3E28'}
    return draw(MONK, colours, spots(MONK, 'b', 'KHh'))


@fish('lionfish')
def _():
    # banded red and white, with a mane of striped venomous spines
    colours = {'o': '3A1414', 'K': 'D8B8A8', 'H': 'F8EEE6', 'h': 'E8D4C8', 'W': 'FFF8F2', 'w': 'C8A898',
               'f': 'A83028', 'F': 'F4E8E0', 'd': 'A83028', 'D': 'F4E8E0', 'e': '141414', 'g': 'A83028', 'b': 'A83028',
               'B': '7A1E18'}
    bands = (-7, -6, -3, -2, 1, 2)
    return draw(LION, colours, bars(LION, 'b', bands, on='KHhWw'), bars(LION, 'B', bands, on='K'))


@fish('octopus')
def _():
    return draw(OCTOPUS, {'o': '3A1418', 'H': 'D87070', 'h': 'B04A50', 'w': '7E2E38', 'e': '141010', 'E': '141010'})


@fish('stingray')
def _():
    return draw(RAY, {'o': '2A2620', 'H': 'B8A888', 'h': '98886A', 'w': '74664E', 'e': '141008', 'x': '3A3226'})


@fish('swordfish')
def _():
    return draw(SWORD, {'o': '1A1A2A', 'K': '3A3A5A', 'H': '8A88A8', 'h': 'B8B4C4', 'W': 'ECEAF0', 'w': '8A889C',
                        'f': '3A3A5A', 'F': '6A6A8A', 'e': '141418', 'g': '3A3A5A', 'B': '8A88A8'})


@fish('blue_shark')
def _():
    return draw(SHARK, {'o': '101E3A', 'K': '2A4A9A', 'H': '4A70C8', 'h': '7E9CD8', 'W': 'F2F4FA', 'w': '9AA8C8',
                        'f': '2A4A9A', 'F': '4A70C8', 'e': '101010', 'g': '2A4A9A'})


@fish('anglerfish')
def _():
    return draw(ANGLER, {'o': '0E0A08', 'K': '2A2018', 'H': '5A4A38', 'h': '3E3226', 'W': '6A5A46', 'w': '2A2018',
                         'f': '2A2018', 'F': '4A3E30', 'e': 'D8E8F0', 'g': '2A2018', 'L': 'D8FFF8', 'G': '58C8C0',
                         'm': '140C08', 't': 'E8E0D0'})


# The legends -------------------------------------------------------------------------------------

@fish('old_whiskers')
def _():
    # nearly black, an amber eye, long pale whiskers and an old hook scar
    colours = {'o': '0E0C08', 'K': '2A241A', 'H': '5A4E38', 'h': '42382A', 'W': 'A89878', 'w': '4A3E2E',
               'f': '2A241A', 'F': '4A4030', 'd': '2A241A', 'D': '4A4030', 'e': 'E8A830', 'g': '2A241A',
               'x': 'C8B898', 'z': 'B8A480'}
    return draw(GREAT_WHISKERED, colours, ("""
z..
.z.
..z
""", 6, 6))


@fish('sunscale')
def _():
    # hammered gold: every scale a little dent that catches the noon sun
    colours = {'o': '5A3404', 'K': 'C07810', 'H': 'FFE070', 'h': 'F8C840', 'W': 'FFF4C8', 'w': 'D09020',
               'f': 'E89020', 'F': 'FFD050', 'd': 'E87818', 'D': 'FFD050', 'e': '8A1010', 'g': 'D09020',
               'n': 'D89A20', 'z': 'FFFDF0'}
    return draw(GREAT_DEEP, colours, lattice(GREAT_DEEP, 'n', 'KHhW'),
                lattice(GREAT_DEEP, 'z', 'Hh', 4, 2))


@fish('river_king')
def _():
    # a silver giant crowned with a purple and gold fin
    colours = {'o': '1E2630', 'K': '4A5A70', 'H': 'E8EEF4', 'h': 'C0CCD8', 'W': 'FFFFFF', 'w': '8E9CAC',
               'd': '6A3A8A', 'D': 'F0C840', 'f': '8E9CAC', 'F': 'C8D4E0', 'e': 'F0C040', 'g': '8E9CAC', 'b': 'A8B6C6'}
    return draw(GREAT_SPINY, colours, bars(GREAT_SPINY, 'b', (-6, -5, -2, -1, 2, 3)))


@fish('rimefin')
def _():
    # a pike of living ice, spotted with frost
    colours = {'o': '1E3A5A', 'K': '4A88C0', 'H': 'D0ECFF', 'h': '9ACCF0', 'W': 'F4FCFF', 'w': '6AA4D4',
               'f': '8AC4F0', 'F': 'E8F8FF', 'e': '0E2440', 'g': '6AA4D4', 'z': 'FFFFFF'}
    return draw(GREAT_PIKE, colours, lattice(GREAT_PIKE, 'z', 'Khf', 3, 0, 1))


@fish('old_mossback')
def _():
    # an ancient sturgeon with moss growing along its back
    colours = {'o': '1A1C14', 'K': '3E4A2A', 'H': '7A7A66', 'h': '5E5E50', 'W': 'BEBCA8', 'w': '54544A',
               'f': '3E4234', 'F': '6A6E58', 'e': '141008', 'g': '3E4234', 's': 'C8C8B0', 'm': '4E7A24', 'M': '8AB848'}
    return draw(GREAT_STURGEON, colours, along(GREAT_STURGEON, 's', 0.45, 0.58, ends=(-8, 99), every=2),
                where(GREAT_STURGEON, 'm', lambda x, y, ch: ch == 'K'),
                where(GREAT_STURGEON, 'M', lambda x, y, ch: ch in 'KdD' and (x + y) % 2 == 0))


@fish('stormjaw')
def _():
    # storm-grey, pale jaws full of teeth and a lightning scar down its side
    colours = {'o': '0E1014', 'K': '2E343C', 'H': '5A626C', 'h': '46505A', 'W': 'C8CCD0', 'w': '6A727A',
               'f': '2E343C', 'F': '4E5660', 'e': 'F0F0A0', 'g': '1E2228', 'z': 'F8F070', 't': 'F0F0E8'}
    return draw(GREAT_SHARK, colours, ("""
.z
z.
.z
z.
""", 6, 6), ('t.t', 2, 13))


@fish('bog_lantern')
def _():
    return draw(GREAT_ANGLER, {'o': '0E140A', 'K': '2A3418', 'H': '5A6A30', 'h': '425024', 'W': '7A8448', 'w': '2E3A1A',
                               'f': '2A3418', 'F': '4A5A2A', 'e': 'E8F078', 'g': '2A3418', 'L': 'FFFFC0', 'G': 'D8F060',
                               'm': '0A0E06', 't': 'E8E0C0'})


@fish('deepglow')
def _():
    # a blind white eel, glowing blue along its sides
    colours = {'o': '2A5A8A', 'K': '8AC8F0', 'H': 'F0FAFF', 'h': 'C8ECFF', 'W': 'FFFFFF', 'w': '7AB8E8',
               'e': 'C8ECFF', 'g': '5AD8FF', 'F': 'C8ECFF', 'f': '8AC8F0', 'b': '5AD8FF'}
    return draw(GREAT_EEL, colours, along(GREAT_EEL, 'b', 0.35, 0.55, every=2))


@fish('jade_arowana')
def _():
    # a dragon of a fish: jade scales, gold barbels, a gold eye
    colours = {'o': '0E2A1E', 'K': '1E6A48', 'H': '7AE0A8', 'h': '3AB880', 'W': 'D8F8E0', 'w': '2A8A60',
               'f': '1E6A48', 'F': '3AB880', 'd': '1E6A48', 'D': '58C890', 'e': 'F0C040', 'g': '1E6A48',
               'x': 'E0B040', 'n': '1E7A50'}
    return draw(GREAT_AROWANA, colours, lattice(GREAT_AROWANA, 'n', 'HhW', 3, 0, 1))


# -- end of sprites --------------------------------------------------------------------------------


# -- the vanilla fish: silhouettes traced from the client jar ---------------------------------------

def client_jar():
    """The Minecraft client jar in the Loom cache, for this project's version when it is there."""
    version = None
    for line in (PROJECT / 'gradle.properties').read_text(encoding='utf-8').splitlines():
        if line.strip().startswith('minecraft_version='):
            version = line.split('=', 1)[1].strip()
    cache = Path.home() / '.gradle/caches/fabric-loom'
    if version and (cache / version / 'minecraft-client.jar').exists():
        return cache / version / 'minecraft-client.jar'
    jars = sorted(cache.glob('*/minecraft-client.jar'))
    return jars[-1] if jars else None


def vanilla_items(names):
    """{name: 16px image} for the vanilla item textures that could be read."""
    jar = client_jar()
    if jar is None:
        return {}
    out = {}
    with zipfile.ZipFile(jar) as archive:
        listed = set(archive.namelist())
        for name in names:
            path = f'assets/minecraft/textures/item/{name}.png'
            if path in listed:
                out[name] = Image.open(io.BytesIO(archive.read(path))).convert('RGBA').crop((0, 0, 16, 16))
    return out


def silhouette(image):
    """The same shape in the journal's ink: opaque wherever the sprite is."""
    out = Image.new('RGBA', (16, 16))
    for y in range(16):
        for x in range(16):
            if image.getpixel((x, y))[3] > 0:
                out.putpixel((x, y), rgba(INK))
    return out


# -- compiling --------------------------------------------------------------------------------------

def table():
    rows, header = [], None
    for raw in (HERE / 'fish.tsv').read_text(encoding='utf-8').splitlines():
        if not raw.strip() or raw.startswith('#'):
            continue
        cells = [c.strip() for c in raw.split('\t')]
        if header is None:
            header = cells
        else:
            rows.append(dict(zip(header, cells)))
    return rows


def is_vanilla(row):
    return 'existing' in row['flags'].split(',')


def missing():
    return [r['id'] for r in table() if not is_vanilla(r) and r['id'] not in FISH]


def png(image):
    for pixel in image.getdata():
        assert pixel[3] in (0, 255), pixel
    buffer = io.BytesIO()
    image.save(buffer, 'PNG')
    return buffer.getvalue()


def dump(data):
    return (json.dumps(data, indent=2) + '\n').encode()


def outputs():
    """{path: bytes} for every file this tool owns, and the vanilla fish whose silhouettes could not be traced."""
    rows = table()
    vanilla = vanilla_items([r['id'] for r in rows if is_vanilla(r)])
    files, untraced = {}, []
    for row in rows:
        name = row['id']
        if is_vanilla(row):
            if name not in vanilla:
                untraced.append(name)
                continue
            sprite = vanilla[name]
        else:
            sprite = FISH[name]()
            files[ASSETS / f'textures/item/fish/{name}.png'] = png(sprite)
            files[ASSETS / f'models/item/{name}.json'] = dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': f'{NS}:item/fish/{name}'}})
            files[ASSETS / f'items/{name}.json'] = dump({'model': {'type': 'minecraft:model', 'model': f'{NS}:item/{name}'}})
        files[ASSETS / f'textures/gui/sprites/fishing/silhouette/{name}.png'] = png(silhouette(sprite))
    return files, untraced


def require_all():
    gone = missing()
    if gone:
        print('No sprite for:\n  ' + '\n  '.join(gone))
        sys.exit(1)


def warn_untraced(untraced):
    if untraced:
        print('No Minecraft client jar in the Loom cache (run a Gradle build once), so these silhouettes were '
              'left as they are: ' + ', '.join(untraced))


def write():
    require_all()
    files, untraced = outputs()
    for path, data in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    warn_untraced(untraced)
    fish_count = sum(1 for r in table() if not is_vanilla(r))
    print(f'Fishing sprites: {fish_count} fish, {len(table()) - len(untraced)} silhouettes ({len(files)} files).')


def check():
    require_all()

    def same(path, data):
        if not path.exists():
            return False
        current = path.read_bytes()
        return current == data if path.suffix == '.png' else current.replace(b'\r\n', b'\n') == data
    files, untraced = outputs()
    bad = [str(p.relative_to(PROJECT)) for p, data in files.items() if not same(p, data)]
    bad += [f'src/main/resources/assets/{NS}/textures/gui/sprites/fishing/silhouette/{n}.png' for n in untraced
            if not (ASSETS / f'textures/gui/sprites/fishing/silhouette/{n}.png').exists()]
    if bad:
        print('Out of date (run tools/fishing/sprites.py):\n  ' + '\n  '.join(bad))
        sys.exit(1)
    warn_untraced(untraced)
    print('Fishing sprites are up to date.')


# -- previews ---------------------------------------------------------------------------------------

def sheet(tiles, dest, columns=10, background='#8BA9C4'):
    """Each tile at 8x with 1x and 2x thumbnails under it, labelled."""
    big, pad, label, thumbs = 128, 14, 14, 40
    w, h = big + pad, label + big + thumbs + pad
    rows = (len(tiles) + columns - 1) // columns
    out = Image.new('RGB', (columns * w + pad, rows * h + pad), background)
    draw_ = ImageDraw.Draw(out)
    for n, (name, image) in enumerate(tiles):
        x, y = pad + (n % columns) * w, pad + (n // columns) * h
        draw_.text((x, y), name[:22], fill='#14202C')
        if image is None:
            draw_.rectangle((x, y + label, x + big - 1, y + label + big - 1), outline='#AA3333')
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
    """The fish in table order with the vanilla ones last for comparison; the silhouettes on journal paper."""
    rows = table()
    vanilla = vanilla_items([r['id'] for r in rows if is_vanilla(r)])
    ours = [(r['name'], FISH[r['id']]() if r['id'] in FISH else None) for r in rows if not is_vanilla(r)]
    theirs = [(r['name'] + ' (vanilla)', vanilla.get(r['id'])) for r in rows if is_vanilla(r)]
    sheet(ours + theirs, PROJECT / 'build/previews/fishing_fish.png')
    sheet([(name, silhouette(image) if image else None) for name, image in theirs + ours],
          PROJECT / 'build/previews/fishing_silhouettes.png', background='#E8DCC0')


if __name__ == '__main__':
    if '--check' in sys.argv:
        check()
    elif '--preview' in sys.argv:
        preview()
    else:
        write()
