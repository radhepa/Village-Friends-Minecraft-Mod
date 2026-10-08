"""Birthday and celebration assets: three items and the party hat.

Writes
  assets/villagefriends/textures/item/{birthday_card,sealed_letter,birthday_cake_slice}.png
      with their item models (minecraft:item/generated) and item definitions
  data/villagefriends/recipe/birthday_card.json   paper + any dye (residents hand out the other two)
  assets/villagefriends/lang/en_us.json            merges in the three item names, leaving every other key alone
  assets/villagefriends/textures/entity/party_hat.png

The item sprites are 16px ASCII rasters with a dark outline and a stepped palette, like the Village
Ledger in tools/social_assets.py, lit from the top left.

The party hat texture is a contract with the Java renderer (PartyHatLayer): x 0-11, y 0-15 is the
cone's surface unrolled (u runs around the cone, v from the tip at y=0 to the brim at y=15), with
the brim band on the bottom two rows; x 12-15, y 0-3 is the pompom; everything else is transparent.

  python tools/celebration_assets.py            write everything
  python tools/celebration_assets.py --check    verify the written files match
  python tools/celebration_assets.py --preview  also write build/previews/celebration_items.png
"""
import io
import json
import math
import os
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(__file__))
from item_sprites import raster  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), '..', 'src', 'main', 'resources')
ASSETS = os.path.join(ROOT, 'assets', 'villagefriends')
NS = 'villagefriends'
NAMES = {
    'birthday_card': 'Birthday Card',
    'sealed_letter': 'Sealed Letter',
    'birthday_cake_slice': 'Slice of Birthday Cake',
}

# A folded card standing a little open: a pink front with a heart and a row of gold dots, the cream
# inside page showing at the right, the fold down the left.
CARD = """
................
................
.ooooooooooo....
.oFKKKKKKKKoo...
.oFKKKKKKKKkCo..
.oFKRRKRRKKkCo..
.oFRwRRRRrKkCo..
.oFRRRRRrrKkCo..
.oFKRRRrrKKkCo..
.oFKKRrdKKKkCo..
.oFKKKdKKKKkCo..
.oFKKKKKKKKkCo..
.oFKgKgKgKKkCo..
.oFkkkkkkkkkCo..
.oooooooooooco..
............oo..
"""
CARD_COLORS = {'o': '4A2232', 'F': 'D9789A', 'K': 'F6B3C8', 'k': 'E58FAC', 'w': 'FFE4EC',
               'R': 'F0566E', 'r': 'D3304A', 'd': '9E2238', 'g': 'E8B844', 'C': 'FBF1DC', 'c': 'D9C4A0'}

# A cream envelope, its flap folded to a point and sealed with red wax.
LETTER = """
................
................
................
oooooooooooooooo
oCfCCCCCCCCCCfCo
oCCfCCCCCCCCfCCo
oCCCfCCCCCCfCCCo
oCCCCfCCCCfCCCCo
oCCCCCfrrfCCCCCo
oCCCCrRrrrrCCCCo
oCCCCrrrrrxCCCCo
oCCCCCrrxxCCCCCo
oddddddddddddddo
oooooooooooooooo
................
................
"""
LETTER_COLORS = {'o': '5A4430', 'C': 'F6EBD0', 'f': 'CBB38A', 'd': 'DCC79E',
                 'r': 'C7283C', 'R': 'F2707E', 'x': '7E1424'}

# A wedge of cake seen from above and to the side: white frosting with sprinkles on top, a pink
# layer between two sponge layers on the cut face, and a striped candle at the back.
CAKE = """
...........f....
..........fFf...
..........fFf...
...........y....
..........oPo...
..........oWo...
..........oPo...
.......ooooWooo.
.....ooWWWWWWWwo
...ooWWbWWWKWWwo
.ooWWWWWWWgWWwWo
oWWwWWwWWWwWwSso
oSSSSSSSSSSSSsso
oKKKKKKKKKKKKkko
oSSSSSSSSSSSSsso
oooooooooooooooo
"""
CAKE_COLORS = {'o': '5A3A2E', 'W': 'FFFBF4', 'w': 'E2D6D0', 'S': 'F2CF86', 's': 'D6AC62',
               'K': 'F48FB1', 'k': 'D46E92', 'b': '7FC8E8', 'g': 'F2C94C',
               'P': 'F27BA0', 'y': '3A2A20', 'f': 'FF9A2E', 'F': 'FFE066'}

ITEMS = {'birthday_card': (CARD, CARD_COLORS), 'sealed_letter': (LETTER, LETTER_COLORS),
         'birthday_cake_slice': (CAKE, CAKE_COLORS)}


def item(name):
    pattern, palette = ITEMS[name]
    return raster(pattern, palette)


# -- the party hat ----------------------------------------------------------------------------------

HAT_STRIPES = [(0xF7, 0x8F, 0xB3), (0xFB, 0xE3, 0x8A), (0x7F, 0xD6, 0xC2)]  # pink, butter yellow, mint
HAT_DOTS = [(2, 3), (8, 4), (5, 7), (11, 8), (1, 10), (7, 11), (4, 13)]
POMPOM = """
CWWC
WWWc
WWcc
Cccs
"""


def party_hat():
    image = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for v in range(16):
        for u in range(12):
            # Diagonal stripes two texels wide; the period (6) divides the 12 texels around the cone,
            # so they meet seamlessly at the back and spiral up to the tip.
            r, g, b = HAT_STRIPES[((u + v) % 6) // 2]
            if (u, v) in HAT_DOTS:
                r, g, b = 255, 255, 255
            if v >= 14:  # the brim band
                r, g, b = int(r * .8), int(g * .8), int(b * .8)
            image.putpixel((u, v), (r, g, b, 255))
    colors = {'W': (0xFF, 0xFB, 0xF0), 'C': (0xF3, 0xEC, 0xDC), 'c': (0xE6, 0xDA, 0xC2), 's': (0xD2, 0xC4, 0xA8)}
    for y, row in enumerate(POMPOM.strip('\n').splitlines()):
        for x, ch in enumerate(row):
            image.putpixel((12 + x, y), colors[ch] + (255,))
    return image


# -- writing ----------------------------------------------------------------------------------------

def encode(data):
    return (json.dumps(data, indent=2) + '\n').encode()


def png(image):
    buffer = io.BytesIO(); image.save(buffer, 'PNG')
    return buffer.getvalue()


def outputs():
    """Every file this tool owns outright: path -> bytes (the shared lang file is merged separately)."""
    files = {}
    for name in NAMES:
        files[os.path.join(ASSETS, 'textures', 'item', f'{name}.png')] = png(item(name))
        files[os.path.join(ASSETS, 'models', 'item', f'{name}.json')] = encode(
            {'parent': 'minecraft:item/generated', 'textures': {'layer0': f'{NS}:item/{name}'}})
        files[os.path.join(ASSETS, 'items', f'{name}.json')] = encode(
            {'model': {'type': 'minecraft:model', 'model': f'{NS}:item/{name}'}})
    files[os.path.join(ROOT, 'data', NS, 'recipe', 'birthday_card.json')] = encode(
        {'type': 'minecraft:crafting_shapeless', 'category': 'misc', 'result': {'id': f'{NS}:birthday_card', 'count': 1},
         'ingredients': ['minecraft:paper', '#minecraft:dyes']})
    files[os.path.join(ASSETS, 'textures', 'entity', 'party_hat.png')] = png(party_hat())
    return files


LANG = os.path.join(ASSETS, 'lang', 'en_us.json')


def merged_lang():
    """The language file with our names merged in: other keys keep their values and order (ours are
    added at the end or updated in place), in the file's own style (2-space indent, its line endings)."""
    raw = open(LANG, 'rb').read() if os.path.exists(LANG) else b'{}\n'
    data = json.loads(raw.decode('utf-8'))
    for key, title in NAMES.items():
        data[f'item.{NS}.{key}'] = title
    text = (json.dumps(data, indent=2) + '\n').encode()
    return raw, text.replace(b'\n', b'\r\n') if b'\r\n' in raw else text


def write():
    for path, data in outputs().items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(data)
    raw, lang = merged_lang()
    if lang != raw:
        with open(LANG, 'wb') as f:
            f.write(lang)
    print(f'Celebration assets: {len(NAMES)} items, the party hat, 1 recipe.')


def check():
    def same(path, data):
        if not os.path.exists(path):
            return False
        current = open(path, 'rb').read()
        return current == data if path.endswith('.png') else current.replace(b'\r\n', b'\n') == data
    bad = [os.path.relpath(p, ROOT) for p, data in outputs().items() if not same(p, data)]
    raw, lang = merged_lang()
    if raw.replace(b'\r\n', b'\n') != lang.replace(b'\r\n', b'\n'):
        bad.append(os.path.relpath(LANG, ROOT) + ' (item names missing)')
    if bad:
        print('Out of date (run tools/celebration_assets.py):\n  ' + '\n  '.join(bad)); sys.exit(1)
    hat = party_hat()
    for y in range(16):
        for x in range(16):
            alpha = hat.getpixel((x, y))[3]
            assert alpha == (255 if x < 12 or y < 4 else 0), ('party hat layout', x, y)
    print('Celebration assets are up to date.')


# -- preview ----------------------------------------------------------------------------------------

def hat_on_cone(texture, size=96):
    """A rough front view of the texture wrapped on a cone, to judge the stripes (the Java renderer's
    exact mapping may differ): the front half of the cone shows u 3..9, pompom on the tip."""
    image = Image.new('RGBA', (size, size + 12), (0, 0, 0, 0))
    top, height, radius = 14, size - 14, size * .32
    for py in range(top, top + height):
        t = (py - top + .5) / height            # 0 at the tip, 1 at the brim
        r = radius * t
        for px in range(size):
            dx = px + .5 - size / 2
            if r <= 0 or abs(dx) > r:
                continue
            angle = math.asin(dx / r)             # -90..90 degrees across the front
            u = int((angle / (2 * math.pi) + .5) * 12) % 12
            v = min(15, int(t * 16))
            c = texture.getpixel((u, v))
            light = .78 + .22 * math.cos(angle + .5)
            image.putpixel((px, py), (int(c[0] * light), int(c[1] * light), int(c[2] * light), 255))
    pom = texture.crop((12, 0, 16, 4)).resize((20, 20), Image.NEAREST)
    image.alpha_composite(pom, (size // 2 - 10, 2))
    return image


def preview():
    zoom, cell = 10, 200
    sheet = Image.new('RGBA', (cell * 5, cell + 70), (0x8B, 0x8B, 0x8B, 255))
    draw = ImageDraw.Draw(sheet)
    shown = [(name, item(name)) for name in NAMES] + [('party_hat (texture)', party_hat())]
    for n, (label, image) in enumerate(shown):
        x = n * cell + (cell - 16 * zoom) // 2
        if label.startswith('party_hat'):
            for gy in range(16):  # a checkerboard shows the transparent part of the texture
                for gx in range(16):
                    shade = (0xC6, 0xC6, 0xC6, 255) if (gx + gy) % 2 else (0xA8, 0xA8, 0xA8, 255)
                    draw.rectangle((x + gx * zoom, 10 + gy * zoom, x + gx * zoom + zoom - 1, 10 + gy * zoom + zoom - 1), fill=shade)
        sheet.alpha_composite(image.resize((16 * zoom, 16 * zoom), Image.NEAREST), (x, 10))
        sheet.alpha_composite(image, (n * cell + 12, cell + 14))                       # actual size
        sheet.alpha_composite(image.resize((32, 32), Image.NEAREST), (n * cell + 36, cell + 6))  # 2x, inventory scale
        draw.text((n * cell + 80, cell + 18), label, fill='#1E1E1E')
    sheet.alpha_composite(hat_on_cone(party_hat(), 150), (4 * cell + 25, 20))
    draw.text((4 * cell + 50, cell + 40), 'approx. on a cone', fill='#1E1E1E')
    out = os.path.join(os.path.dirname(__file__), '..', 'build', 'previews', 'celebration_items.png')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    sheet.save(out)
    print('preview', os.path.normpath(out))


if __name__ == '__main__':
    if '--check' in sys.argv:
        check()
    else:
        write()
        if '--preview' in sys.argv:
            preview()
