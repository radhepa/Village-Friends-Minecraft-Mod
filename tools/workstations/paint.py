"""Hand-authored 16px textures for the profession workstations.

Surfaces (burlap, straw, staves, bricks, cast iron) are painted from seeded noise over stepped
palettes; details (faces, targets, oven doors, sheet music, paintings, saw blades) are ASCII
rasters like tools/item_sprites.py. Light comes from the top left, like vanilla blocks.
Every function returns a 16x16 RGBA image; transparent pixels make cutout faces.
"""
import random
from PIL import Image


def rgb(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def blank():
    return Image.new('RGBA', (16, 16), (0, 0, 0, 0))


def raster(pattern, palette, base=None):
    """Paints a 16-row pattern; '.' leaves the base (or transparency)."""
    image = base.copy() if base is not None else blank()
    rows = [r for r in pattern.strip('\n').splitlines()]
    assert len(rows) == 16, len(rows)
    for y, row in enumerate(rows):
        assert len(row) == 16, (y, row, len(row))
        for x, ch in enumerate(row):
            if ch != '.':
                image.putpixel((x, y), rgb(palette[ch]))
    return image


def noise(colors, weights, seed, size=16):
    rand = random.Random(seed)
    image = Image.new('RGBA', (size, size))
    for y in range(size):
        for x in range(size):
            image.putpixel((x, y), rgb(rand.choices(colors, weights)[0]))
    return image


def put(image, x, y, color):
    if 0 <= x < 16 and 0 <= y < 16:
        image.putpixel((x, y), rgb(color) if isinstance(color, str) else color)


def rect(image, x0, y0, x1, y1, color):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(image, x, y, color)


def shade(image, factor, box=(0, 0, 15, 15)):
    x0, y0, x1, y1 = box
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            r, g, b, a = image.getpixel((x, y))
            if a:
                image.putpixel((x, y), (min(255, int(r * factor)), min(255, int(g * factor)), min(255, int(b * factor)), a))
    return image


# -- shared materials -------------------------------------------------------------------------------

def iron():
    """Cast iron: dark, a little mottled, a bevel of light on the top-left."""
    image = noise(['#45454B', '#4D4D53', '#3E3E44', '#55555C'], [5, 4, 3, 1], 11)
    for i in range(16):
        put(image, i, 0, '#6A6A72'); put(image, 0, i, '#5E5E66')
        put(image, i, 15, '#2E2E33'); put(image, 15, i, '#34343A')
    return image


def brass():
    image = noise(['#D4A845', '#C9993A', '#DDB453', '#B98A30'], [5, 3, 3, 1], 12)
    for i in range(16):
        put(image, i, 0, '#F1D27A'); put(image, 0, i, '#EAC768')
        put(image, i, 15, '#9A6F22'); put(image, 15, i, '#A57826')
    for x, y in [(3, 3), (4, 4), (11, 8), (12, 9), (6, 12)]:
        put(image, x, y, '#F6DE92')
    return image


def rope():
    image = blank()
    for y in range(16):
        for x in range(16):
            k = (x + y) % 4
            image.putpixel((x, y), rgb(['#CDA766', '#B88F50', '#9A733A', '#B88F50'][k]))
    return image


def burlap(seed=21, seam=True):
    image = noise(['#C9A86E', '#BF9C62', '#D2B37A', '#B48F58'], [6, 4, 2, 2], seed)
    for y in range(16):
        for x in range(16):
            if (x + 2 * y) % 5 == 0:
                r, g, b, a = image.getpixel((x, y))
                image.putpixel((x, y), (r - 16, g - 16, b - 12, a))
    if seam:
        for y in range(16):
            put(image, 7, y, '#A07D48')
            if y % 2 == 0:
                put(image, 8, y, '#6B4A2A')
    return image


def straw(seed=31):
    image = noise(['#D8B85A', '#C9A54A', '#E4C76A', '#B7923C'], [5, 4, 2, 2], seed)
    rand = random.Random(seed)
    for _ in range(14):
        x, y = rand.randrange(16), rand.randrange(16)
        for i in range(3):
            put(image, (x + i) % 16, y, '#EDD587' if i == 0 else '#B08A36')
    return image


def staves(horizontal, seed=41):
    """Oak barrel staves with two iron hoops. Horizontal staves run left-right (hoops vertical)."""
    image = blank()
    rand = random.Random(seed)
    plank = ['#A0703F', '#93663A', '#8A5E34', '#9C6B3C']
    for a in range(16):
        stave = a // 4
        for b in range(16):
            color = plank[(stave + (1 if rand.random() < .18 else 0)) % 4]
            if a % 4 == 3:
                color = '#5E3F22'
            elif a % 4 == 0:
                color = '#B07E4A' if rand.random() < .7 else color
            x, y = (b, a) if horizontal else (a, b)
            put(image, x, y, color)
    for hoop in (3, 12):
        for a in range(16):
            x, y = (hoop, a) if horizontal else (a, hoop)
            x2, y2 = (hoop + 1, a) if horizontal else (a, hoop + 1)
            put(image, x, y, '#3C3C42'); put(image, x2, y2, '#5A5A62')
    return image


def stove_bricks():
    """Warm masonry with soot creeping up from the firebox."""
    image = blank()
    for y in range(16):
        row = y // 4
        for x in range(16):
            offset = 0 if row % 2 == 0 else 4
            mortar = y % 4 == 3 or (x + offset) % 8 == 7
            if mortar:
                color = '#B9A68C'
            else:
                color = ['#9A5038', '#8E4932', '#A4593F', '#874430'][(x * 7 + y * 3 + row) % 4]
            put(image, x, y, color)
    for y in range(6):
        shade(image, .62 + y * .06, (0, y, 15, y))
    return image


# -- training dummy ---------------------------------------------------------------------------------

def dummy_face():
    """Stitched X eyes, rosy cheeks and a lopsided stitched grin on the head's 8x8 face (columns 4-11, rows 4-11)."""
    image = burlap(23, seam=False)
    for cx in (4, 9):
        for dy, row in enumerate(["x.x", ".x.", "x.x"]):
            for dx, ch in enumerate(row):
                if ch == 'x':
                    put(image, cx + dx, 6 + dy, '#3A2416')
    for x in range(5, 11):
        put(image, x, 10, '#4A2E1A')
    for x in (5, 7, 9):
        put(image, x, 9, '#7A5530')
    for x in (6, 8, 10):
        put(image, x, 11, '#7A5530')
    put(image, 4, 9, '#C4675A'); put(image, 11, 9, '#C4675A')
    return image


def dummy_chest():
    """Burlap with a red bullseye painted where you should aim."""
    image = burlap(25)
    for y in range(16):
        for x in range(16):
            d = ((x + .5 - 8) ** 2 + (y + .5 - 4.5) ** 2) ** .5
            if d <= 1.1:
                put(image, x, y, '#B33A2E')
            elif d <= 2.2:
                put(image, x, y, '#E6D9B8')
            elif d <= 3.3:
                put(image, x, y, '#A8352A')
    return image


# -- archery target ---------------------------------------------------------------------------------

def target_face():
    """Archery rings centered on (8, 7): gold, red, blue, black, white, on a straw boss."""
    image = straw(33)
    for y in range(16):
        for x in range(16):
            d = ((x + .5 - 8) ** 2 + (y + .5 - 7) ** 2) ** .5
            if d <= 1.25: c = '#F2C531' if (x + y) % 3 else '#FFE066'
            elif d <= 2.6: c = '#D23B2E'
            elif d <= 4.0: c = '#3E6FB8'
            elif d <= 5.4: c = '#2A2A30'
            elif d <= 6.8: c = '#ECE4CF'
            else: continue
            put(image, x, y, c)
    for y in range(16):  # a little wear on the paint
        for x in range(16):
            if (x * 13 + y * 7) % 23 == 0:
                r, g, b, a = image.getpixel((x, y)); image.putpixel((x, y), (int(r * .85), int(g * .85), int(b * .85), a))
    return image


def arrow():
    """Shaft along the u axis, fletching at the right end; used on thin elements."""
    image = blank()
    for x in range(16):
        put(image, x, 7, '#7A5530'); put(image, x, 8, '#5E4024')
    for x in range(11, 16):
        put(image, x, 6, '#E8E2D2' if x % 2 else '#C93A2E'); put(image, x, 9, '#E8E2D2' if x % 2 else '#C93A2E')
    for y in range(16):
        for x in range(16):
            if y not in (6, 7, 8, 9) and image.getpixel((x, y))[3] == 0:
                put(image, x, y, '#7A5530')
    return image


# -- kitchen stove ----------------------------------------------------------------------------------

STOVE = {'o': '#26262B', 'i': '#3F3F45', 'I': '#4D4D54', 'h': '#6E6E77', 'H': '#8C8C96', 'r': '#7C7C86',
         'b': '#D9AE4E', 'B': '#F1D27A', 'g': '#1A1A1E', 'x': '#303036',
         'f': '#FF8A1E', 'F': '#FFD34A', 'e': '#E2471E', 'w': '#FFF1A8', 'k': '#5B2A12'}
STOVE_FRONT = """
oooooooooooooooo
oHhhhhhhhhhhhhho
ohiiiiiiiiiiiiio
ohirbbbbbbbbriio
ohiiiiiiiiiiiiio
ohiIIIIIIIIIIiio
ohiIggggggggIiio
ohiIgxgxgxgxIiio
ohiIggggggggIiio
ohiIgxgxgxgxIiio
ohiIggggggggIiio
ohiIIIIIIIIIIiio
ohrixxxxxxxxirio
ohiiiiiiiiiiiiio
ohhhhhhhhhhhhhho
oooooooooooooooo
"""
STOVE_FRONT_LIT = """
oooooooooooooooo
oHhhhhhhhhhhhhho
ohiiiiiiiiiiiiio
ohirbbbbbbbbriio
ohiiiiiiiiiiiiio
ohiIIIIIIIIIIiio
ohiIkkfkkfkkIiio
ohiIkfFfffFfIiio
ohiIfFwFFwFfIiio
ohiIfFwwwFFfIiio
ohiIeffFFffeIiio
ohiIIIIIIIIIIiio
ohrixxxxxxxxirio
ohiiiiiiiiiiiiio
ohhhhhhhhhhhhhho
oooooooooooooooo
"""


def stove_front(lit):
    return raster(STOVE_FRONT_LIT if lit else STOVE_FRONT, STOVE)


def stove_top():
    image = iron()
    for cx, cy, r in [(5, 5, 3.4), (11, 10, 3.0)]:
        for y in range(16):
            for x in range(16):
                d = ((x + .5 - cx) ** 2 + (y + .5 - cy) ** 2) ** .5
                if r - 1 <= d <= r:
                    put(image, x, y, '#2A2A2F')
                elif r - 1.9 <= d < r - 1:
                    put(image, x, y, '#6A6A72')
    return image


def pot_side():
    image = iron()
    rect(image, 0, 0, 15, 1, '#5E5E66')
    for x in range(16):
        put(image, x, 2, '#2A2A2F')
    for x in (2, 13):
        put(image, x, 6, '#6E6E77')
    return image


def stew():
    return raster("""
oooooooooooooooo
oSssSSsssSSssSso
osScsSsSgsSssSso
oSsSssScSsSsSsso
osSspsSsSssSgSso
oSsSsSsSsSpsSsso
osgsSsScsSsSsSso
oSsSsSpsSsSsScso
osSssSsSsgsSsSso
oSsSgsSsSsSsSsso
osScsSsSsSscSsso
oSsSsSpsSssSsgso
osSsSsSsSsSsSsso
oSssgSsSsSpsSsso
osSsSsSsSsSsSsso
oooooooooooooooo
""", {'o': '#2E2E33', 's': '#8A4E2A', 'S': '#A3613A', 'c': '#E07A2A', 'p': '#D9C27A', 'g': '#5E8A3A'})


def copper():
    image = noise(['#D98A5A', '#C9774A', '#E39A68', '#B8683E'], [5, 4, 2, 2], 51)
    for i in range(16):
        put(image, i, 0, '#F2B58A'); put(image, 0, i, '#EBA77A'); put(image, i, 15, '#8E4A2A'); put(image, 15, i, '#9A5232')
    for x, y in [(4, 10), (5, 11), (11, 4), (12, 13), (9, 12)]:
        put(image, x, y, '#5FA38C')  # a touch of verdigris
    return image


def pipe():
    image = noise(['#3A3A40', '#424248', '#34343A'], [4, 3, 2], 61)
    for y in (0, 7, 8, 15):
        for x in range(16):
            put(image, x, y, '#5A5A62' if y in (0, 8) else '#26262B')
    for y in range(16):
        put(image, 1, y, '#55555C')
    return image


# -- tavern -----------------------------------------------------------------------------------------

def barrel_end():
    image = blank()
    rand = random.Random(71)
    for y in range(16):
        for x in range(16):
            plank = y // 4
            color = ['#B07E4A', '#A27041', '#B88752', '#9A693B'][(plank + (1 if rand.random() < .15 else 0)) % 4]
            if y % 4 == 3:
                color = '#6E4A2A'
            put(image, x, y, color)
    for y in range(16):
        for x in range(16):
            d = ((x + .5 - 8) ** 2 + (y + .5 - 8) ** 2) ** .5
            if 6.9 <= d <= 8.2:
                put(image, x, y, '#3C3C42')
            elif 6.2 <= d < 6.9:
                put(image, x, y, '#5A5A62')
    apple = """
................
................
................
................
................
.......L........
......LgL.......
.....rRrrr......
....rRRrrrr.....
....rRrrrrd.....
....rrrrrrd.....
.....rrrrd......
......rdd.......
................
................
................
"""
    return raster(apple, {'L': '#5E9A3A', 'g': '#6B4A2A', 'r': '#C33A2E', 'R': '#E6705E', 'd': '#8E2A22'}, image)


def mug():
    image = noise(['#E9DFC9', '#DED2B8', '#F2EAD8'], [5, 3, 2], 81)
    for x in range(16):
        put(image, x, 4, '#8E5A36'); put(image, x, 5, '#A86C42')
    return image


def cider_top():
    return raster("""
oooooooooooooooo
owwwwwwwwwwwwwwo
owfwwfwwwfwwfwwo
owwaAaaaAaaaawwo
owfaAAaaaaAaawfo
owwaaaAaaaaAawwo
owwAaaaaAaaaawwo
owfaaAaaaaaAawfo
owwaAaaaAaaaawwo
owwaaaAaaaaAawwo
owfAaaaaaAaaawfo
owwaaAaaaaaAawwo
owfwwfwwwfwwfwwo
owwwwwwwwwwwwwwo
owwwwwwwwwwwwwwo
oooooooooooooooo
""", {'o': '#DED2B8', 'w': '#F4E9D0', 'f': '#E8D9B5', 'a': '#D9962E', 'A': '#E8AE4A'})


def cabinet_front():
    return raster("""
DDDDDDDDDDDDDDDD
DppppppDDppppppD
DpddddpDDpddddpD
DpdssdpDDpdssdpD
DpdssdpDDpdssdpD
DpdssdpDDpdssdpD
DpdssbpDDbdssdpD
DpdssdpDDpdssdpD
DpdssdpDDpdssdpD
DpdssdpDDpdssdpD
DpddddpDDpddddpD
DppppppDDppppppD
DDDDDDDDDDDDDDDD
DppppppppppppppD
DpddddddddddddpD
DDDDDDDDDDDDDDDD
""", {'D': '#4A3420', 'p': '#7A5A34', 'd': '#694D2C', 's': '#8A6A40', 'b': '#E0B85A'})


# -- apothecary -------------------------------------------------------------------------------------

def vat_side():
    image = staves(False, 91)
    return shade(image, .92)


def herbs():
    return noise(['#4E7A36', '#6E9A48', '#5A8A3E', '#8BBE5A', '#9A5AB0', '#E8C84A', '#3E6A2E'], [6, 5, 5, 2, 1, 1, 3], 101)


def bottle():
    return raster("""
................
......cCCc......
......cLLc......
......oggo......
......ohgo......
.....ohhgno.....
....ohhgggno....
...ohSSttttno...
..ohSSttttttno..
..ohSttTtttdno..
..ohSttTttdddo..
..onttttttddno..
...ondttddddo...
....onndddno....
.....oooooo.....
................
""", {'o': '#466779', 'n': '#749CAE', 'g': '#A7C8D5', 'h': '#D9EDF0', 'c': '#7C4930', 'C': '#BC7850', 'L': '#E3A07A',
      'S': '#B6E08A', 't': '#6DB36B', 'T': '#8FD07A', 'd': '#4E8A4A'})


def small_bottle():
    """A little 5x7 bottle of green tonic (columns 5-9, rows 7-13) for the press's drip card."""
    return raster("""
................
................
................
................
................
................
................
.......c........
......ogo.......
.....ohgto......
.....ohtTo......
.....ottdo......
.....otddo......
......ooo.......
................
................
""", {'o': '#466779', 'h': '#D9EDF0', 'g': '#A7C8D5', 'c': '#7C4930', 't': '#6DB36B', 'T': '#8FD07A', 'd': '#4E8A4A'})


# -- painter ----------------------------------------------------------------------------------------

def linen(seed=111):
    image = noise(['#EEE5CF', '#E6DCC2', '#F4EDDA', '#DDD2B6'], [6, 4, 3, 1], seed)
    for y in range(16):
        for x in range(16):
            if (x + y) % 4 == 0:
                r, g, b, a = image.getpixel((x, y)); image.putpixel((x, y), (r - 8, g - 8, b - 10, a))
    return image


def canvas_back():
    image = linen(113)
    for i in range(16):
        for j in (1, 14):
            put(image, i, j, '#9C7A4E'); put(image, j, i, '#9C7A4E')
        put(image, i, 8, '#B08A5A')
    return image


ART_PALETTE = {
    'a': '#F7B267', 'b': '#F48C5A', 'c': '#E0607E', 'd': '#9A5AA8', 'e': '#5B3A7A', 's': '#FFE38A', 'S': '#FFF3C4',
    'g': '#5E9A48', 'G': '#3E7A36', 'h': '#2E5A2A', 'k': '#86B85A', 'w': '#EAF4FA', 'W': '#FFFFFF', 'm': '#8C96A6',
    'M': '#6A7486', 'l': '#5C8FC9', 'L': '#3E6FA8', 'n': '#2A4E86', 'N': '#1C2E5A', 'y': '#E8C84A', 'o': '#2A2A30',
    'r': '#C93A2E', 'R': '#E6705E', 'p': '#F4A7C0', 'P': '#E07AA0', 'v': '#7A4A9A', 't': '#8E5A36', 'T': '#6B4428',
    'u': '#B98A5A', 'f': '#E9C8A0', 'F': '#D4A57A', 'x': '#1A1A20', 'j': '#4A7A3A', 'q': '#C8D8E8', 'i': '#FFD34A',
    'z': '#3A5A2A', 'Z': '#A8D86A', '_': '#EEE5CF',
}


def canvas(art):
    """The easel's canvas. 0 blank, 1 a charcoal sketch, 2-8 finished paintings (12x14 at columns 2-13, rows 1-14)."""
    image = linen(115 + art)
    if art == 0:
        return image
    if art == 1:
        sketch = """
................
................
................
.........xxx....
........x...x...
........x...x...
.........xxx....
................
................
.......xx.......
.....xx..xx..x..
...xx......xx.x.
..x............x
................
....x..x..x..x..
................
"""
        return raster(sketch, {'x': '#6E6A62'}, image)
    paintings = [
        # 2: sunset over the hills
        """
................
..dddddddddddd..
..cdccddccddcc..
..cccccccccccc..
..bbbbbbsSbbbb..
..bbbbbssSSbbb..
..aaaaasssSaaa..
..aaaaaaaaaaaa..
..aaggaaaaaggg..
..gggggaaaggGG..
..GgggGggggGGG..
..GGhGGGgGGGhG..
..hGGGhGGGGhGG..
..hhhhhhhhhhhh..
..hhhzhhhhzhhh..
................
""",
        # 3: a mountain lake
        """
................
..llllllllllll..
..lllWWllllqll..
..llqllllllllll.
..lllllMwllllll.
..lllllMMwlllll.
..llllMMMMwllll.
..lllMMMMMMwlll.
..GllMMMMMMMMGl.
..GGGjGGjGGGjGG.
..LLLLlLLLLlLLL.
..LlLLLLwLLLLlL.
..LLLlLLLLLLLLL.
..nnLnnnnLnnnnn.
..nnnnnnnnnnnnn.
................
""",
        # 4: the village at night
        """
................
..NNNNNNNNNNNN..
..NNWNNNNNNSSN..
..NNNNNWNNNSSN..
..NWNNNNNNNNNN..
..NNNNNNNNWNNN..
..NNNNoNNNNNNN..
..NNNoooNNNooN..
..NNooooNNooooN.
..NoiooioNoioo..
..NooooooNoooo..
..NoioiooNooio..
..zzzzzzzzzzzz..
..zhzzhzzzhzzh..
..hhhhhhhhhhhh..
................
""",
        # 5: flowers in a vase
        """
................
..eeeeeeeeeeee..
..eeerReeeeeee..
..eeRrrepPeeee..
..eerRreppPeye..
..eeerjeePeyye..
..eeeejeejeyee..
..eeeeejjjjeee..
..eeeeeLLLeeee..
..eeeeLlllLeee..
..eeeeLlwlLeee..
..eeeeLlllLeee..
..eeeeeLLLeeee..
..tttttttttttt..
..TTTTTTTTTTTT..
................
""",
        # 6: portrait of a neighbor
        """
................
..dddddddddddd..
..ddddTTTTdddd..
..dddTTTTTTddd..
..dddFffffFddd..
..dddfoffofddd..
..dddTTTTTTddd..
..dddfffFfffdd..
..ddddffFFffdd..
..ddddffFFfddd..
..dddddfffdddd..
..ddggggggggdd..
..dgggGggGgggd..
..dggggGGggggd..
..gggggggggggg..
................
""",
        # 7: a ship at sea
        """
................
..llllllllllll..
..lllwwllllllll.
..llllllltllll..
..lllllWWtllll..
..llllWWWtWlll..
..lllWWWWtWWll..
..llWWWWWtWWWl..
..lllllllttlll..
..lluuuuuuuuul..
..LllTTTTTTTll..
..LLLLwLLLLLwL..
..LlLLLLLwLLLL..
..nnnLnnnnnLnn..
..nnnnnnnnnnnn..
................
""",
        # 8: a creeper in the meadow
        """
................
..llllllllllll..
..llsSlllllWWl..
..lssslllllWWl..
..llllgggglll...
..lllgkgkgglll..
..lllgxxggxgll..
..lllgxxggxgll..
..lllggxxgggll..
..lllgxxxxggll..
..lllgxggxggll..
..kkkkggggkkkk..
..kZkkkZkkkkZk..
..gggggkggggkg..
..gGggggGggggg..
................
""",
    ]
    return raster(paintings[art - 2], ART_PALETTE, image)


def paint_pots():
    image = blank()
    colors = ['#C93A2E', '#3E6FB8', '#E8C84A', '#5E9A48', '#F4EDDA']
    for i, c in enumerate(colors):
        rect(image, i * 3, 0, i * 3 + 2, 15, c)
        for y in range(16):
            put(image, i * 3 + 2, y, '#6B4428')
    return image


# -- bard -------------------------------------------------------------------------------------------

def sheet_music():
    """A page of parchment with two staves of notes (rows 3-12 show on the stand)."""
    return raster("""
pppppppppppppppp
pPPPPPPPPPPPPPPp
pPPPPPPPPPPPPPPp
pPPPPPPPPPPPPPPp
pPPPPPnPPPPPPnPp
pPlllllnllllnnlp
pPPPPPnPPPnPnPPp
pPllnnlnlllnlllp
pPPnnPPPPnnPPPPp
pPPPPPPPPnnPPPPp
pPllllllllllnllp
pPPPPnPPPPPPnPPp
pPlllnlllllnnllp
pPPPnnPPPPnnPPPp
pPPPnnPPPPPPPPPp
pppppppppppppppp
""", {'p': '#C9B88E', 'P': '#EFE3C0', 'l': '#9A8768', 'n': '#2A2420'})


# -- tailor -----------------------------------------------------------------------------------------

def cloth(base, stripe, seed):
    image = noise([base, shade_hex(base, .9), shade_hex(base, 1.08)], [6, 3, 2], seed)
    for x in range(16):
        put(image, x, 3, stripe); put(image, x, 12, stripe)
    return image


def shade_hex(h, f):
    r, g, b, _ = rgb(h)
    return '#%02X%02X%02X' % (min(255, int(r * f)), min(255, int(g * f)), min(255, int(b * f)))


def bolt_end(base):
    image = blank()
    for y in range(16):
        for x in range(16):
            d = ((x + .5 - 8) ** 2 + (y + .5 - 8) ** 2) ** .5
            put(image, x, y, shade_hex(base, .75 + .1 * (int(d * 1.3) % 3)))
    rect(image, 7, 7, 8, 8, '#4A3420')
    return image


def runner():
    """A teal table runner with a cream stitched border."""
    image = noise(['#3E7F8A', '#377480', '#468A95'], [6, 3, 2], 121)
    for i in range(16):
        for j in (0, 15):
            put(image, i, j, '#2E5E66'); put(image, j, i, '#2E5E66')
        if i % 2 == 0:
            for j in (1, 14):
                put(image, i, j, '#E8DCC0'); put(image, j, i, '#E8DCC0')
    for x, y in [(5, 5), (10, 5), (5, 10), (10, 10), (7, 7), (8, 8), (7, 8), (8, 7)]:
        put(image, x, y, '#E8C84A')
    return image


def spool_side():
    image = blank()
    for y in range(16):
        for x in range(16):
            put(image, x, y, '#C93A2E' if (x + y // 2) % 3 else '#A82E24')
    for x in range(16):
        put(image, x, 0, '#B98A5A'); put(image, x, 1, '#9A6F44'); put(image, x, 14, '#9A6F44'); put(image, x, 15, '#B98A5A')
    return image


def pincushion():
    image = noise(['#C93A2E', '#B8342A', '#D9584A'], [5, 3, 2], 131)
    for x, y in [(3, 3), (8, 2), (12, 5), (5, 9), (10, 11), (13, 13)]:
        put(image, x, y, '#E8E8F0'); put(image, x + 1, y, '#9A9AA6')
    return image


def scissors():
    return raster("""
................
................
................
.....h......h...
.....hH....Hh...
......hH..Hh....
.......hHHh.....
........gg......
.......oggo.....
......oo..oo....
.....o......o...
.....o......o...
......oo..oo....
................
................
................
""", {'h': '#C8CCD4', 'H': '#F0F2F6', 'g': '#8A8E96', 'o': '#2A2A30'})


# -- carpenter --------------------------------------------------------------------------------------

def saw_blade():
    image = blank()
    for y in range(16):
        for x in range(16):
            d = ((x + .5 - 8) ** 2 + (y + .5 - 8) ** 2) ** .5
            angle = __import__('math').atan2(y + .5 - 8, x + .5 - 8)
            tooth = (int((angle + 3.1416) / (2 * 3.1416) * 16) % 2) == 0
            if d <= 1.4:
                put(image, x, y, '#2A2A30')
            elif d <= 2.2:
                put(image, x, y, '#6E6E77')
            elif d <= 6.6:
                put(image, x, y, '#BFC4CC' if (x - y) % 7 else '#E4E8EE')
            elif d <= 7.6 and tooth:
                put(image, x, y, '#8C9098')
    for x, y in [(5, 4), (4, 5), (4, 6)]:
        put(image, x, y, '#F4F6FA')
    return image


def sawdust():
    return noise(['#E3C994', '#D6B97E', '#EED9AA', '#C9A86E'], [5, 4, 3, 1], 141)


# -- scholar ----------------------------------------------------------------------------------------

def archives_front():
    """Pigeonholes of scrolls, ledgers and boxes; rows divided by shelf shadows."""
    return raster("""
xxxxxxxxxxxxxxxx
xSsxBbxRrxSsxGgx
xsSxBbxRrxsSxGgx
xSsxBbxRrxSsxGgx
xnnxBbxRrxnnxGgx
xxxxxxxxxxxxxxxx
xVvPpxYyyyyxSsSx
xVvPpxYyyyyxsSsx
xVvPpxYyyyyxSnSx
xVvPpxYyyyyxsSsx
xxxxxxxxxxxxxxxx
xcCccCxUuxSsSsxx
xcCccCxUuxsSsSxx
xcCccCxUuxnSnSxx
xccccccUuxSsSsxx
xxxxxxxxxxxxxxxx
""", {'x': '#241A12', 'S': '#EFE4C8', 's': '#D8CAA6', 'n': '#C93A2E', 'B': '#6B3A7A', 'b': '#7E4A8E',
      'R': '#8E2A22', 'r': '#A8392E', 'G': '#2E5E46', 'g': '#3E7A5A', 'V': '#2A4E86', 'v': '#3E6FA8',
      'P': '#8E5A36', 'p': '#A86C42', 'Y': '#B8923A', 'y': '#D4AE52', 'c': '#7A5A34', 'C': '#9A7446',
      'U': '#5A3A2A', 'u': '#7A5240'})


def ledger_open():
    return raster("""
................
................
................
.cppppppcppppppc
.cPllllPcPllllPc
.cppppppcppppppc
.cPlllllcPlllllc
.cppppppcppppppc
.cPllllPcPlllPPc
.cppppppcppppppc
.cPlllllcrPllllc
.cppppppcrppppPc
.ccccccccrcccccc
................
................
................
""", {'c': '#6B3A22', 'p': '#F2E8CC', 'P': '#E2D6B4', 'l': '#8A7656', 'r': '#C93A2E'})


def candle():
    return raster("""
................
................
................
................
.......f........
......fFf.......
.......w........
......ccc.......
......cCc.......
......cCc.......
......cCc.......
......cCc.......
......cCc.......
......cCc.......
................
................
""", {'f': '#FF9A2E', 'F': '#FFE066', 'w': '#2A2420', 'c': '#D9CBA0', 'C': '#EDE2C4'})


# -- the catalog ------------------------------------------------------------------------------------

def textures():
    """Every texture the workstations use, by name (written to textures/block/workstation/<name>.png)."""
    t = {
        'iron': iron(), 'brass': brass(), 'rope': rope(), 'burlap': burlap(), 'burlap_plain': burlap(27, False), 'straw': straw(),
        'dummy_face': dummy_face(), 'dummy_chest': dummy_chest(), 'target_face': target_face(), 'arrow': arrow(),
        'stove_front': stove_front(False), 'stove_front_lit': stove_front(True), 'stove_bricks': stove_bricks(), 'stove_top': stove_top(),
        'pot_side': pot_side(), 'stew': stew(), 'copper': copper(), 'pipe': pipe(),
        'staves_h': staves(True), 'staves_v': staves(False), 'barrel_end': barrel_end(), 'mug': mug(), 'cider_top': cider_top(),
        'cabinet_front': cabinet_front(), 'vat_side': vat_side(), 'herbs': herbs(), 'bottle': bottle(), 'small_bottle': small_bottle(),
        'canvas_back': canvas_back(), 'paint_pots': paint_pots(), 'sheet_music': sheet_music(),
        'cloth_wine': cloth('#8E3A4E', '#E8C84A', 151), 'cloth_mustard': cloth('#C9A23A', '#5A3A22', 152), 'bolt_wine': bolt_end('#8E3A4E'),
        'bolt_mustard': bolt_end('#C9A23A'), 'runner': runner(), 'spool': spool_side(), 'pincushion': pincushion(), 'scissors': scissors(),
        'saw_blade': saw_blade(), 'sawdust': sawdust(), 'archives_front': archives_front(), 'ledger_open': ledger_open(), 'candle': candle(),
    }
    for art in range(9):
        t[f'canvas_{art}'] = canvas(art)
    return t
