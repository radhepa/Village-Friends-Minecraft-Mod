"""Designs, compiles and previews the village Notice Board (four models, one per `notes` state).

The board is built like the workstations in tools/workstations/workstations.py and reuses its
Model, auto_uv and render: two spruce posts on stone footings, a cork board in a plank frame with
a little shelf, a pitched shingle cap, and parchment notices held on with colored pins. Wood and
stone come from vanilla textures; the cork, shingles, notices, pins and inkwell are hand-authored
pixel art below (using paint.py's helpers). One texel is always 1/16 block, and the front faces
north (the blockstate turns it by `facing`).

The block state `notes` (0-3) is how many notices are pinned up, so players can see from afar
that there's work posted: 0 is a bare board with a couple of empty pins and a torn corner, 3 is
crowded.

    python tools/notice_board/notice_board.py            # write models, blockstate, item definition, textures
    python tools/notice_board/notice_board.py --check    # verify the compiled files match the design
    python tools/notice_board/notice_board.py --preview  # build/previews/notice_board.png (every state, front and back)
    python tools/notice_board/notice_board.py --boxes    # print the collision boxes for VillageBlocks.java

Never hand-edit the compiled JSON or PNG; change this file and rerun.
"""
import io
import json
import random
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'workstations'))
import workstations as ws  # noqa: E402
from paint import blank, noise, put, raster, rect, rgb  # noqa: E402

PROJECT = ws.PROJECT
ASSETS = ws.ASSETS
NS = ws.NS
NAME = 'notice_board'
TEXTURES = f'block/{NAME}'        # our textures live in textures/block/notice_board/
PARTICLE = 'mc:spruce_planks'
STATES = range(4)
ITEM_STATE = 2
# Collision in the north-facing coordinates VillageBlocks.java uses, in whole texels so
# tools/create_foundation_assets.py can still read them: the posts, the board with its shelf, the cap.
BOXES = [[1, 0, 7, 3, 16, 9], [13, 0, 7, 15, 16, 9], [3, 2, 6, 13, 14, 9], [0, 14, 5, 16, 16, 11]]
# Files of the old placeholder board, removed when this tool writes.
STALE = [ASSETS / f'textures/block/{NAME}.png', ASSETS / f'models/block/{NAME}.json']


class Model(ws.Model):
    """A workstation Model whose own textures live in textures/block/notice_board/. Each element
    remembers the `layer` it was added on: 0 for the board, then one layer per thing set in front of
    it, nearest last (only the preview uses layers)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer, self.layers = 0, []

    def tex(self, key):
        ref = key.replace(':', '_')
        self.textures[ref] = f'minecraft:block/{key[3:]}' if key.startswith('mc:') else f'{NS}:{TEXTURES}/{key}'
        return '#' + ref

    def box(self, *args, **kwargs):
        super().box(*args, **kwargs)
        self.layers.append(self.layer)
        return self


# -- the art ----------------------------------------------------------------------------------------

def cork():
    """Warm speckled cork, shaded under the frame, with a few old pin holes."""
    image = noise(['#B4855A', '#AA7C50', '#BD8F63', '#A37549', '#C69A6C'], [6, 5, 4, 2, 1], 201)
    for x, y in [(2, 3), (5, 10), (9, 5), (12, 12), (7, 14), (13, 7), (11, 2)]:
        put(image, x, y, '#7A5434')
    for i in range(16):  # the shadow of the frame
        for x, y in ((i, 2), (12, i), (3, i)):
            r, g, b, a = image.getpixel((x, y)); image.putpixel((x, y), (int(r * .86), int(g * .86), int(b * .86), a))
    return image


def shingles():
    """Russet wooden shingles in staggered courses two texels deep, each with a dark foot, and a few
    spots of moss. Texture-down is down the slope."""
    image = blank()
    tones = ['#8E4632', '#9C5038', '#A65A3E', '#874230']
    rand = random.Random(211)
    for course in range(8):
        offset = (course % 2) * 2
        for x in range(16):
            tone = tones[((x + offset) // 4 * 3 + course * 5 + rand.randrange(2)) % 4]
            gap = (x + offset) % 4 == 3
            put(image, x, course * 2, '#5E2A1E' if gap else ('#B86A4A' if (x + offset) % 4 == 0 else tone))
            put(image, x, course * 2 + 1, '#4E2218' if gap else '#6A3022')
    for x, y in [(5, 2), (6, 2), (12, 8), (2, 12), (3, 12), (9, 14)]:
        put(image, x, y, '#6E7E3A')
    return image


NOTE_COLORS = {
    'P': '#F4E8C8', 'p': '#D9C597', 'i': '#5E4B3A', 'j': '#A8946F', 'r': '#B8433A',
    'K': '#F8CBD6', 'k': '#DE9CB0', 'B': '#CDE2F2', 'b': '#98B8D4',
    'S': '#6E7C8C', 's': '#E4EAF0', 'g': '#D19E32', 'h': '#6B4428',
    'y': '#EDC64E', 'Y': '#B8862A', 't': '#7A4E26',
    'F': '#FBF8EE', 'f': '#D8D2C2', 'q': '#2A2A30', 'w': '#E8E0CC',
}
# The notices, one atlas. Row 0 of each notice is where its pin goes.
#   A  a cream "help wanted": a red heading and two lines of handwriting (6x7, columns 0-5)
#   B  a pink one with a sword, for monster trouble (5x7, columns 6-10)
#   C  a pale blue one with a tied wheat sheaf, for help with the harvest (5x7, columns 11-15)
#   D  the torn corner of a notice someone took (3x2 at 0,8)
#   E  a quill (1.5x5 at 14,9; its inked nib dips into the inkwell)
#   F  blank notices for the stack on the shelf: cream, pink and blue (3x1 rows at 0,11-13)
NOTICES = """
PPPPPPKKKKKBBBBB
PrrrrPKKsKKByByB
PPPPPPKKSKKBYyYB
PiijiPKKSKKBBYBB
PPPPPPKgggKBBtBB
PjiiPPKKhKKBYBYB
ppppppkkkkkbbbbb
................
PPp.............
pp............Ff
..............Ff
PPPwww........Fw
KKKk..........F.
BBBb..........q.
................
................
"""


def notices():
    return raster(NOTICES, NOTE_COLORS)


# Pins: red, blue, yellow and green, in 4x4 cells along the top row. Each cell's top-left 2x2 is
# the head as seen from the front (lit from the top left); the rest is the plain color for its sides.
PIN_CELLS = {'red': 0, 'blue': 4, 'yellow': 8, 'green': 12}


def pins():
    image = blank()
    for (light, mid, dark), x0 in zip([('#FF9A8A', '#D8382C', '#8E1E18'), ('#A8D0FF', '#3A78D8', '#1E3E86'),
                                       ('#FFF4A8', '#E8C030', '#9A7414'), ('#B4ECA6', '#4AA83E', '#22601C')], (0, 4, 8, 12)):
        rect(image, x0, 0, x0 + 3, 3, mid)
        put(image, x0, 0, light); put(image, x0 + 1, 1, dark)
    return image


def inkwell():
    """A squat inkwell of dark blue glass with a glint (rows 2-4), black ink seen from above (row 1)."""
    return raster("""
oooooooooooooooo
oxxxxxxxxxxxxxxo
oNnhnnNnnNnhnnNo
oNnhnnNnnNnhnnNo
oNnnnnNnnNnnnnNo
oNNNNNNNNNNNNNNo
oooooooooooooooo
................
................
................
................
................
................
................
................
................
""", {'o': '#1E2433', 'x': '#0E0E14', 'N': '#2A3A5E', 'n': '#3A5286', 'h': '#9AB8E8'})


def textures():
    return {'cork': cork(), 'shingles': shingles(), 'notices': notices(), 'pins': pins(), 'inkwell': inkwell()}


# -- the design -------------------------------------------------------------------------------------

ROOF_ANGLE = 22.5
CORK_FRONT = 7.5   # z of the cork's face (it spans x 3-13, y 3-14); notices sit just in front of it

# Notices per state: atlas region (u, v, width, height), where its top-left corner goes as you face
# the board (`left` from the board's left edge, so x = 16 - left; `top` in y), its tilt in degrees
# and its pin. Later notices overlap earlier ones.
A = (0, 0, 6, 7)
B = (6, 0, 5, 7)
C = (11, 0, 5, 7)
LAYOUTS = {
    0: [],
    1: [(A, 5, 12.75, -5, 'red')],
    2: [(A, 3.5, 13.25, -5, 'red'), (B, 8, 12.5, 7, 'blue')],
    3: [(A, 3.25, 13.75, -5, 'red'), (B, 8, 13.25, 7, 'blue'), (C, 4.75, 10, -4, 'yellow')],
}
# A bare board still has a couple of empty pins (left, top, color), one holding a torn corner.
BARE_PINS = [(6, 12, 'green'), (10.5, 8.5, 'red')]


def note(m, region, left, top, tilt, color, depth):
    u0, v0, w, h = region
    x0, x1 = 16 - left - w, 16 - left
    z = CORK_FRONT - .1 - .1 * depth  # a tenth of a texel apart, so they never z-fight
    pin_x, pin_y = 16 - left - w / 2, top - .5
    rot = ('z', tilt, [pin_x, pin_y, z]) if tilt else None
    # A hair of thickness so the card only shows from the front, as a single face does in game.
    m.box([x0, top - h, z], [x1, top, z + .01], 'notices', uv={'north': [u0, v0, u0 + w, v0 + h]}, only=('north',), rot=rot)
    pin(m, pin_x, pin_y, z, color)


def pin(m, x, y, z, color):
    u = PIN_CELLS[color]
    side = [u + 2, 2, u + 2.75, 2.625]
    layer, m.layer = m.layer, m.layer + .5  # a pin sits on its paper
    m.box([x - .375, y - .375, z - .625], [x + .375, y + .375, z], 'pins', skip=('south',),
          uv={'north': [u, 0, u + 2, 2], 'up': side, 'down': side, 'east': side, 'west': side})
    m.layer = layer


def notice_board(notes):
    m = Model(f'{NAME}_{notes}', BOXES, gui=.6, gui_y=-1)
    # Two spruce posts on little stone footings.
    for x in (1, 13):
        m.box([x - .5, 0, 6.5], [x + 2.5, 1.5, 9.5], 'mc:cobblestone', skip=('down',))
        m.box([x, 1.5, 7], [x + 2, 16, 9], 'mc:spruce_log', skip=('up', 'down'))
    # The cork board in its frame: a lintel beam on top, a shelf below, planks and battens behind.
    m.box([3, 3, CORK_FRONT], [13, 14, 8.5], {'north': 'cork', '*': 'mc:spruce_planks'}, skip=('up', 'down', 'east', 'west'))
    m.box([.5, 14, 6.75], [15.5, 16, 9.25], {'east': 'mc:stripped_spruce_log_top', 'west': 'mc:stripped_spruce_log_top', '*': 'mc:stripped_spruce_log'},
          skip=('up',), face_rot={'north': 90, 'south': 90, 'down': 90},
          uv={'north': [7, .5, 9, 15.5], 'south': [7, .5, 9, 15.5], 'down': [7, .5, 9.5, 15.5], 'east': [6.75, 7, 9.25, 9], 'west': [6.75, 7, 9.25, 9]})
    m.box([2.5, 2, 5.75], [13.5, 3, 9], 'mc:spruce_planks')
    for y in (4.5, 11):
        m.box([1, y, 9], [15, y + 1.5, 9.75], 'mc:dark_oak_planks')
    # A pitched cap of shingles under a dark oak ridge; texture-down runs down each slope.
    origin = [8, 17, 8]
    roof = {'up': 'shingles', 'down': 'mc:spruce_planks', '*': 'mc:dark_oak_planks'}
    m.box([0, 16, 4.5], [16, 17, 8], roof, uv={'up': [0, 8, 16, 4.5]}, rot=('x', -ROOF_ANGLE, origin))
    m.box([0, 16, 8], [16, 17, 11.5], roof, uv={'up': [0, 4.5, 16, 8]}, rot=('x', ROOF_ANGLE, origin))
    m.box([0, 16.6, 7.25], [16, 17.6, 8.75], 'mc:dark_oak_planks', skip=('down',))
    # On the shelf: a stack of blank notices, and an inkwell with a quill for signing up.
    m.layer = 9
    for n, (x, row) in enumerate(((8.5, 13), (8.875, 12), (8.625, 11))):
        y = 3 + n * .25
        m.box([x, y, 6.25], [x + 2.5, y + .25, 7.25], 'notices', skip=('down',),
              uv={'up': [0, row, 2.5, row + 1], 'north': [.5, row, 3, row + .25], 'south': [.5, row, 3, row + .25],
                  'east': [3, row, 4, row + .25], 'west': [3, row, 4, row + .25]})
    m.box([4.25, 3, 6.25], [5.75, 4.25, 7.5], 'inkwell', skip=('down',),
          uv={'up': [4, 1, 5.5, 2.25], 'north': [2, 2, 3.5, 3.25], 'east': [2, 2, 3.25, 3.25], 'west': [2, 2, 3.25, 3.25]})
    m.plane([4.25, 3.75, 6.9], [5.75, 8.75, 6.9], 'notices', [14, 9, 15.5, 14], ('north', 'south'), rot=('z', 20, [5, 3.75, 6.9]))
    # The notices, or on a bare board, empty pins and the corner of a notice someone took.
    if notes == 0:
        z = CORK_FRONT - .1
        m.layer = 1
        m.box([8.5, 10, z], [11.5, 12, z + .01], 'notices', uv={'north': [0, 8, 3, 10]}, only=('north',), rot=('z', 12, [10, 11.5, z]))
        for left, top, color in BARE_PINS:
            pin(m, 16 - left, top - .5, z, color)
    for depth, (region, left, top, tilt, color) in enumerate(LAYOUTS[notes]):
        m.layer = 1 + depth
        note(m, region, left, top, tilt, color, depth)
    m.layer = 0
    return m


def designs():
    return [notice_board(n) for n in STATES]


def blockstate(models):
    variants = {}
    for facing, y in ws.ROTATION:
        for notes, model in zip(STATES, models):
            variants[f'facing={facing},notes={notes}'] = {'model': f'{NS}:block/{model.name}', 'y': y}
    return {'variants': variants}


def encode(data):
    return (json.dumps(data, indent=1) + '\n').encode()


def outputs():
    """Every compiled file: path -> bytes."""
    files = {}
    for key, image in textures().items():
        buffer = io.BytesIO(); image.save(buffer, 'PNG')
        files[ASSETS / f'textures/{TEXTURES}/{key}.png'] = buffer.getvalue()
    models = designs()
    for model in models:
        files[ASSETS / f'models/block/{model.name}.json'] = encode(model.json(PARTICLE))
    files[ASSETS / f'blockstates/{NAME}.json'] = encode(blockstate(models))
    files[ASSETS / f'items/{NAME}.json'] = encode({'model': {'type': 'minecraft:model', 'model': f'{NS}:block/{NAME}_{ITEM_STATE}'}})
    return files


def write():
    for path, data in outputs().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    for old in STALE:
        if old.exists():
            old.unlink()  # the old placeholder board
    print(f'Notice board: {len(STATES)} models, {len(textures())} textures.')


def check():
    def same(path, data):
        # Git may check text files out with CRLF line endings; compare them line by line.
        if not path.exists():
            return False
        current = path.read_bytes()
        return current == data if path.suffix == '.png' else current.replace(b'\r\n', b'\n') == data
    bad = [str(p.relative_to(PROJECT)) for p, data in outputs().items() if not same(p, data)]
    bad += [f'{p.relative_to(PROJECT)} (the old placeholder; delete it)' for p in STALE if p.exists()]
    if bad:
        print('Out of date (run tools/notice_board/notice_board.py):\n  ' + '\n  '.join(bad)); sys.exit(1)
    painted = textures()
    for model in designs():
        for texture in model.textures.values():
            assert texture.startswith('minecraft:') or texture.rsplit('/', 1)[1] in painted, (model.name, texture)
        for e in model.elements:
            for c in e['from'] + e['to']:
                assert -16 <= c <= 32, (model.name, e)
            if 'rotation' in e:
                assert -45 <= e['rotation']['angle'] <= 45, (model.name, e)
            for face in e['faces'].values():
                assert all(0 <= c <= 16 for c in face['uv']), (model.name, e['from'], face)
    for notes, layout in LAYOUTS.items():
        for i, (region, left, top, _, _) in enumerate(layout):
            pin_left, pin_top = left + region[2] / 2, top - .5
            for later, l2, t2, _, _ in layout[i + 1:]:
                inside = l2 - .75 <= pin_left <= l2 + later[2] + .75 and t2 - later[3] - .75 <= pin_top <= t2 + .75
                assert not inside, f'notes={notes}: a later notice covers the pin of notice {i}'
    for box in BOXES:
        assert all(0 <= c <= 16 and c == int(c) for c in box) and box[0] < box[3] and box[1] < box[4] and box[2] < box[5], box
    print('Notice board is up to date.')


def boxes():
    rows = ','.join('{' + ','.join(f'{c:g}' for c in b) + '}' for b in BOXES)
    print(f'add("{NAME}", false, new double[][]{{{rows}}}, FoundationEntityBlock.Kind.NOTICE_BOARD);')


# -- preview ----------------------------------------------------------------------------------------

def vanilla_textures(keys):
    """Vanilla block textures from the Loom cache. (workstations.vanilla_textures only loads the
    ones the workstations use.) Anything missing becomes flat wood so the preview still renders."""
    found = {}
    jars = sorted(Path.home().glob('.gradle/caches/fabric-loom/*/minecraft-client.jar'))
    if jars:
        with zipfile.ZipFile(jars[-1]) as jar:
            names = set(jar.namelist())
            for key in keys:
                entry = f'assets/minecraft/textures/{key.split(":", 1)[1]}.png'
                if entry in names:
                    found[key] = Image.open(io.BytesIO(jar.read(entry))).convert('RGBA').crop((0, 0, 16, 16))
    for key in keys:
        found.setdefault(key, Image.new('RGBA', (16, 16), rgb('#7A5A3A')))
    return found


def layer(model, n):
    part = Model(model.name, model.boxes)
    part.textures = model.textures
    part.elements = [e for e, k in zip(model.elements, model.layers) if k == n]
    return part


def picture(model, painted, scale, view, front):
    """workstations.render, one layer at a time: its painter's sort can't put small things (pins,
    the inkwell) in front of a big face (the cork), nor order overlapping notices. From the front,
    each notice with its pin and then the things on the shelf are drawn over the board in the
    order they sit; from behind they're left out, since the board hides them."""
    image = ws.render(layer(model, 0), painted, scale=scale, view=view)
    for n in sorted(set(model.layers) - {0}) if front else ():
        image.alpha_composite(ws.render(layer(model, n), painted, scale=scale, view=view))
    return image


def preview():
    models = designs()
    painted = {f'{NS}:{TEXTURES}/{k}': v for k, v in textures().items()}
    painted.update(vanilla_textures({t for m in models for t in m.textures.values() if t.startswith('minecraft:')}))
    tile, label, scale = 360, 22, 18
    sheet = Image.new('RGB', (tile * len(models), 2 * (tile + label)), '#7FA7C9')
    draw = ImageDraw.Draw(sheet)
    for n, model in enumerate(models):
        for row, view in enumerate(((1, .9, -1.15), (-1, .9, 1.15))):
            image = picture(model, painted, scale, view, front=row == 0)
            image = image.crop(image.getbbox())
            x = n * tile + (tile - image.width) // 2
            y = row * (tile + label) + label + (tile - image.height) // 2
            sheet.paste(image, (x, y), image)
            draw.text((n * tile + 8, row * (tile + label) + 5), f'notes={n}, ' + ('front' if row == 0 else 'back'), fill='#10202E')
    dest = PROJECT / 'build/previews/notice_board.png'
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest)
    print(dest)


if __name__ == '__main__':
    if '--check' in sys.argv: check()
    elif '--preview' in sys.argv: preview()
    elif '--boxes' in sys.argv: boxes()
    else: write()
