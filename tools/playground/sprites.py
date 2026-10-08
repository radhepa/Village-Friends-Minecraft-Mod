"""Authored 16px sprite for the children's leather ball, in the style of tools/item_sprites.py: native
pixel pattern, a dark outline, stepped palette, light from the top left and no antialiasing. A stitched
ball of red and cream leather panels, the kind a village cobbler sews from offcuts.

    python tools/playground/sprites.py            # write textures/item, models/item and items/ for the ball
    python tools/playground/sprites.py --check    # verify the compiled files match the pattern
    python tools/playground/sprites.py --preview  # build/previews/playground_items.png, 8x

Never hand-edit the PNG or JSON; change the pattern here and rerun.
"""
import io
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from item_sprites import raster  # noqa: E402

PROJECT = Path(__file__).resolve().parents[2]
ASSETS = PROJECT / 'src/main/resources/assets/villagefriends'
NS = 'villagefriends'

BALL = """
................
................
.....oooooo.....
...ooHRRssCoo...
..oHRRRsCCCcco..
..oRRRsCCCccco..
.oRRRRsCCcccsro.
.oRRRrsscccsrro.
.ossssrrssssrro.
.oCCcsrrrrsRrro.
.oCccsrrrsRRrdo.
..occcsrsRRrdo..
..occcsssRrddo..
...oocdddrdoo...
.....oooooo.....
................
"""
LEATHER = {'o': '3A1F14', 'H': 'E9876A', 'R': 'C4472F', 'r': '96311F', 'd': '6E2216',
           'C': 'F2E2BC', 'c': 'D3BD8E', 's': '5B3A26'}
SPRITES = {'leather_ball': lambda: raster(BALL, LEATHER)}


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
    print(f'Playground: {len(SPRITES)} sprite.')


def check():
    def same(path, data):
        if not path.exists():
            return False
        current = path.read_bytes()
        return current == data if path.suffix == '.png' else current.replace(b'\r\n', b'\n') == data
    bad = [str(p.relative_to(PROJECT)) for p, data in outputs().items() if not same(p, data)]
    if bad:
        print('Out of date (run tools/playground/sprites.py):\n  ' + '\n  '.join(bad)); sys.exit(1)
    print('Playground sprites are up to date.')


def preview():
    image = SPRITES['leather_ball']()
    sheet = Image.new('RGB', (200, 180), '#8BA9C4')
    big = image.resize((128, 128), Image.NEAREST)
    sheet.paste(big, (16, 20), big)
    sheet.paste(image, (160, 40), image)
    ImageDraw.Draw(sheet).text((16, 4), 'leather_ball', fill='#14202C')
    dest = PROJECT / 'build/previews/playground_items.png'
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest)
    print(dest)


if __name__ == '__main__':
    if '--check' in sys.argv: check()
    elif '--preview' in sys.argv: preview()
    else: write()
