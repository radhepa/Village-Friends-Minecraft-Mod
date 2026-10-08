"""Authored 16px sprites for the tavern's three dishes, in the style of tools/item_sprites.py:
native pixel patterns, a dark outline per material, stepped palettes, light from the top left and
no antialiasing. The Ploughman's Lunch is a little still life, so it is drawn as layers (board,
then the food at the back, then the food in front), each its own pattern and palette.

    python tools/tavern/sprites.py            # write textures/item, models/item and items/ for the dishes
    python tools/tavern/sprites.py --check    # verify the compiled files match the patterns
    python tools/tavern/sprites.py --preview  # build/previews/tavern_items.png, 8x, beside the existing food

Never hand-edit the PNG or JSON; change the patterns here and rerun.
"""
import io
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from item_sprites import raster, item_sprite  # noqa: E402

PROJECT = Path(__file__).resolve().parents[2]
ASSETS = PROJECT / 'src/main/resources/assets/villagefriends'
NS = 'villagefriends'


def layered(*layers):
    """Draws (pattern, palette, x, y) layers back to front; '.' is transparent in each."""
    image = Image.new('RGBA', (16, 16))
    for pattern, palette, x, y in layers:
        piece = raster(pattern, palette)
        canvas = Image.new('RGBA', (16, 16))
        canvas.paste(piece, (x, y))
        image = Image.alpha_composite(image, canvas)
    return image


# -- Ploughman's Lunch: bread, a wedge of cheese, an apple and a pickle on a board -------------------

BOARD = """
.oooooooooooooo.
oWWWWwWWWWWwWWWo
oWwwWwwwwWwwwwwo
oeeeeeeeeeeeeeEo
.oEEEEEEEEEEEEo.
..oooooooooooo..
"""
OAK = {'o': '4A301C', 'W': 'C99A5B', 'w': 'AD7F45', 'e': '8A5D31', 'E': '6B4423'}
HUNK = """
...ooo..
..oHHHo.
.oHHhhho
oHhhhhCo
ohhhhCCo
ohhmCSCo
ommmCCCo
.oooooo.
"""
CRUST = {'o': '4A2E14', 'H': 'C98C4A', 'h': 'A96D33', 'm': '84502A', 'C': 'F0DBA8', 'S': 'D2B47E'}
APPLE = """
...kg.
.ookoo
oSRRRo
oSRRro
oRRrro
.orro.
..oo..
"""
FRUIT = {'o': '4E1A14', 'S': 'F2A08C', 'R': 'D8443A', 'r': 'A52C27', 'k': '5A3A1E', 'g': '6FA040'}
WEDGE = """
.......oo.
.....ooYZo
...ooYYYZo
.ooYYYYyZo
oYYYYyyyZo
oyyyyyyyZo
oyhyyyhyZo
oyyyhyyyZo
.oooooooo.
"""
CHEESE = {'o': '6B4E1C', 'Y': 'FCEB9E', 'y': 'F2CD62', 'h': 'C99E3E', 'Z': 'D0973A'}
PICKLE = """
.oooo.
oPpPvo
.ovvo.
"""
GHERKIN = {'o': '2E3B16', 'P': 'A9C46A', 'p': '7E9E42', 'v': '5B7A2C'}


def ploughmans_lunch():
    return layered((BOARD, OAK, 0, 9), (APPLE, FRUIT, 5, 0), (HUNK, CRUST, 0, 3), (WEDGE, CHEESE, 6, 3), (PICKLE, GHERKIN, 1, 9))


# -- Shepherd's Pie: an earthenware dish, a ridged mashed-potato top, gravy bubbling at the edge -----

PIE = """
................
................
................
.....oooooo.....
...ooYBYYByoo...
..oyuuyuuyuuyo..
.oYYBYYyYBYYyyo.
.ouyuuyuuyuuyuo.
oTgYYyYYyYyyygto
oTtgGgggggggGtto
oTTTTTttttttttqo
.oKKKkkkkkkkkqo.
..oKKkkkkkkqqo..
...oooooooooo...
................
................
"""
DISH = {'o': '3E2214', 'Y': 'FBEDC0', 'y': 'EAD08E', 'u': 'C4A05A', 'B': 'DDA651', 'g': '6B3A1E', 'G': 'A0602F',
        'T': 'DC8A5C', 't': 'B9653E', 'K': 'A9542F', 'k': '8C4325', 'q': '66301A'}


# -- Apple Tart: a small round tart, a lattice of pastry over apple ----------------------------------

TART = """
................
................
................
................
.....oooooo.....
...ooCcCcCcoo...
..oCALaLaLaLCo..
.oCcLaAaLaarcdo.
.oCcaLaLrLaLcdo.
..oCcCcCcCcdco..
..ocdcdcdcdcdo..
...oddddddddo...
....oooooooo....
................
................
................
"""
PASTRY = {'o': '5A3418', 'C': 'E9BC68', 'c': 'C98F3D', 'd': '9A6128', 'L': 'F3D58C', 'l': 'D9A955',
          'a': 'D9862F', 'A': 'F0B44C', 'r': 'A4521E'}


SPRITES = {
    'ploughmans_lunch': ploughmans_lunch,
    'shepherds_pie': lambda: raster(PIE, DISH),
    'apple_tart': lambda: raster(TART, PASTRY),
}


# -- compiling --------------------------------------------------------------------------------------

def dump(data):
    return (json.dumps(data, indent=2) + '\n').encode()


def outputs():
    files = {}
    for name, sprite in SPRITES.items():
        buffer = io.BytesIO(); sprite().save(buffer, 'PNG')
        files[ASSETS / f'textures/item/{name}.png'] = buffer.getvalue()
        files[ASSETS / f'models/item/{name}.json'] = dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': f'{NS}:item/{name}'}})
        files[ASSETS / f'items/{name}.json'] = dump({'model': {'type': 'minecraft:model', 'model': f'{NS}:item/{name}'}})
    return files


def write():
    for path, data in outputs().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(f'Tavern dishes: {len(SPRITES)} sprites.')


def check():
    def same(path, data):
        if not path.exists():
            return False
        current = path.read_bytes()
        return current == data if path.suffix == '.png' else current.replace(b'\r\n', b'\n') == data
    bad = [str(p.relative_to(PROJECT)) for p, data in outputs().items() if not same(p, data)]
    if bad:
        print('Out of date (run tools/tavern/sprites.py):\n  ' + '\n  '.join(bad)); sys.exit(1)
    print('Tavern dishes are up to date.')


def preview():
    """Each dish at 8x with 1x and 2x thumbnails under it, then the existing food for comparison."""
    tiles = [(name, sprite()) for name, sprite in SPRITES.items()]
    tiles += [(f'{name} (existing)', item_sprite(name)) for name in ('fresh_village_bread', 'hearty_stew', 'mug_of_cider')]
    big, pad = 128, 16
    sheet = Image.new('RGB', (len(tiles) * (big + pad) + pad, big + 96), '#8BA9C4')
    draw = ImageDraw.Draw(sheet)
    for n, (name, image) in enumerate(tiles):
        x = pad + n * (big + pad)
        sheet.paste(image.resize((big, big), Image.NEAREST), (x, 20), image.resize((big, big), Image.NEAREST))
        sheet.paste(image, (x, big + 32), image)
        sheet.paste(image.resize((32, 32), Image.NEAREST), (x + 24, big + 32), image.resize((32, 32), Image.NEAREST))
        draw.text((x, 4), name, fill='#14202C')
    dest = PROJECT / 'build/previews/tavern_items.png'
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest)
    print(dest)


if __name__ == '__main__':
    if '--check' in sys.argv: check()
    elif '--preview' in sys.argv: preview()
    else: write()
