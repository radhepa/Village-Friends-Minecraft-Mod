"""Designs, compiles and previews the tavern furniture: a trestle table, a spindle-back chair, a bar
stool and an upholstered fireside armchair.

Built on the workstation model kit (tools/workstations/workstations.py): each piece is a small program
of cuboids, wood comes from vanilla textures, and the armchair's painted cloth is pixel art below.
One texel is always 1/16 block. Designs face north, the way the sitter faces: the front is toward -Z
and backrests sit on the south side (+Z). The blockstates turn them like every other directional block
(north y=0, east 90, south 180, west 270), so FoundationBlock's rotated collision boxes line up.

    python tools/tavern/furniture.py            # write models, blockstates, item models, textures
    python tools/tavern/furniture.py --check    # verify the compiled files (and TavernBlocks.java's boxes) match
    python tools/tavern/furniture.py --preview  # build/previews/tavern_furniture.png and tavern_scene.png
    python tools/tavern/furniture.py --boxes    # print the collision boxes for TavernBlocks.java

Never hand-edit the compiled JSON or PNG; change the design here and rerun.
"""
import io
import json
import math
import re
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'workstations'))
import paint  # noqa: E402
import workstations as kit  # noqa: E402

PROJECT, ASSETS, NS = kit.PROJECT, kit.ASSETS, kit.NS
JAVA = PROJECT / 'src/main/java/dev/villagefriends/tavern/TavernBlocks.java'
put, rect, noise, rgb = paint.put, paint.rect, paint.noise, paint.rgb


class Model(kit.Model):
    """The workstation Model, with our own textures under block/tavern/.

    'mc:dark_oak_planks' is vanilla, 'ws:iron' borrows a workstation texture, anything else is
    painted below and lands in textures/block/tavern/.
    """
    def tex(self, key):
        ref = key.replace(':', '_')
        if key.startswith('mc:'):
            self.textures[ref] = f'minecraft:block/{key[3:]}'
        elif key.startswith('ws:'):
            self.textures[ref] = f'{NS}:block/workstation/{key[3:]}'
        else:
            self.textures[ref] = f'{NS}:block/tavern/{key}'
        return '#' + ref

    def json(self, particle):
        data = super().json(particle)
        data['textures']['particle'] = self.textures[particle.replace(':', '_')]
        return data


# -- painted cloth ----------------------------------------------------------------------------------
# A deep, warm madder red with a quilted diamond lattice, brass nailhead trim and buttoned tufting.
# Every pattern repeats every 8 texels, so faces tile seamlessly across the chair.

RED = {'k': '#2C0B09', 'D': '#4A1411', 'd': '#661C17', 'm': '#7E261E', 'n': '#882B21', 'h': '#9C3627', 'H': '#B34A34'}
TACK, TACK_LIGHT, TACK_DARK = '#D8AD48', '#F3D57E', '#8A6420'


def cloth(seed=7):
    """The plain upholstery: a faint quilted lattice with a little flower in each diamond."""
    image = noise([RED['m'], RED['n']], [5, 2], seed)
    for y in range(16):
        for x in range(16):
            a, b = (x + y) % 8, (x - y) % 8
            if a == 0 or b == 0:
                put(image, x, y, RED['d'])
            elif a == 4 and b == 4:
                put(image, x, y, RED['h'])
            elif abs(a - 4) == 1 and abs(b - 4) == 1:
                put(image, x, y, RED['n'])
    return image


def cloth_tacks():
    """Cloth with a row of brass nailheads along its top edge (row 1), for the fronts and sides."""
    image = cloth(seed=8)
    for x in range(16):
        put(image, x, 0, RED['d'])
        put(image, x, 1, TACK if x % 2 == 0 else RED['m'])
        put(image, x, 2, RED['D'] if x % 2 == 0 else RED['n'])
    for x in range(0, 16, 4):
        put(image, x, 1, TACK_LIGHT)
    return image


def tufted():
    """Buttoned tufting for the inside of the back (one face, u 2..14, v 2..14, so it needn't tile):
    buttons on a 6-texel diamond lattice, each puff lit from the top left and shaded to the bottom right."""
    image = cloth(seed=13)
    for y in range(2, 14):
        for x in range(2, 14):
            a, b = (x + y + 1) % 6, (x - y + 3) % 6
            if a == 0 and b == 0:
                color = RED['k']
            elif a == 0 or b == 0:
                color = RED['D']
            else:  # brightest in the middle of the puff, lit on its top-left side
                level = 2 - (abs(a - 3) + abs(b - 3)) / 2 + (3 - a) / 2
                color = RED['H'] if level >= 2 else RED['h'] if level >= 1.5 else RED['n'] if level >= .5 else RED['m'] if level >= 0 else RED['d']
            put(image, x, y, color)
    return image


def cushion():
    """The seat cushion's top (used at u 2..14, v 1..13): piping round the edge, a soft puff in the middle."""
    image = cloth(seed=9)
    x0, y0, x1, y1 = 2, 1, 13, 12
    for x in range(x0, x1 + 1):
        put(image, x, y0, RED['H']); put(image, x, y1, RED['D'])
        put(image, x, y0 + 1, RED['d']); put(image, x, y1 - 1, RED['d'])
    for y in range(y0, y1 + 1):
        put(image, x0, y, RED['H']); put(image, x1, y, RED['D'])
        if y0 < y < y1:
            put(image, x0 + 1, y, RED['d']); put(image, x1 - 1, y, RED['d'])
    put(image, x1, y0, RED['h']); put(image, x0, y1, RED['h'])
    for x, y in ((5, 4), (6, 4), (4, 5), (5, 5)):
        put(image, x, y, RED['h'])
    return image


def piping():
    """A cushion's 2px edge: the lit cord on top, the cloth falling away below."""
    image = cloth(seed=10)
    for x in range(16):
        put(image, x, 0, RED['H'] if x % 3 else RED['h'])
        put(image, x, 1, RED['d'])
    return image


def roll_end():
    """The scrolled front of a padded arm (3x2 at u 0..3, v 0..2), framed in nailheads (v 2..)."""
    image = cloth(seed=11)
    for x, y, c in ((0, 0, RED['h']), (1, 0, RED['H']), (2, 0, RED['h']), (0, 1, RED['d']), (1, 1, RED['k']), (2, 1, RED['d'])):
        put(image, x, y, c)
    return image


def tack_column():
    """The front edge of an arm or wing (2 wide): nailheads running down it."""
    image = cloth(seed=12)
    for y in range(16):
        put(image, 0, y, TACK if y % 2 == 0 else RED['D'])
        put(image, 1, y, RED['n'] if y % 2 == 0 else RED['m'])
        put(image, 2, y, TACK if y % 2 == 0 else RED['D'])
        if y % 4 == 0:
            put(image, 0, y, TACK_LIGHT); put(image, 2, y, TACK_LIGHT)
    return image


def textures():
    return {'cloth': cloth(), 'cloth_tacks': cloth_tacks(), 'tufted': tufted(), 'cushion': cushion(),
            'piping': piping(), 'roll_end': roll_end(), 'tack_column': tack_column()}


# -- the designs ------------------------------------------------------------------------------------
# Collision boxes are the first argument of each Model and must match TavernBlocks.java (--check).

def tavern_table():
    """A pedestal trestle on a cross foot. Nothing reaches the edges below the top, so a row of
    tables reads as one long board instead of doubling up legs at the joins."""
    m = Model('tavern_table', [[0, 12, 0, 16, 14, 16], [6, 0, 6, 10, 12, 10], [2, 0, 6, 14, 2, 10], [6, 0, 2, 10, 2, 14]], gui=.6)
    top, post, beam = 'mc:dark_oak_planks', 'mc:dark_oak_log', 'mc:stripped_dark_oak_log'
    m.box([0, 12, 0], [16, 14, 16], top)
    # A cross of bearers under the top, stepping down into the pedestal like corbels.
    m.box([1, 10.5, 7], [15, 12, 9], beam, skip=('up',))
    m.box([7, 10.5, 1], [9, 12, 7], beam, skip=('up', 'south'))
    m.box([7, 10.5, 9], [9, 12, 15], beam, skip=('up', 'north'))
    m.box([4, 9.5, 6.5], [12, 10.5, 9.5], beam, skip=('up',))
    m.box([6.5, 9.5, 4], [9.5, 10.5, 6.5], beam, skip=('up', 'south'))
    m.box([6.5, 9.5, 9.5], [9.5, 10.5, 12], beam, skip=('up', 'north'))
    m.box([6, 3, 6], [10, 9.5, 10], post, skip=('up', 'down'))
    # The cross foot: a raised hub and four toes that step down to the floor.
    m.box([5.5, 0, 5.5], [10.5, 3, 10.5], beam, skip=('down',))
    m.box([2, 0, 6.5], [5.5, 1.5, 9.5], beam, skip=('east', 'down'))
    m.box([10.5, 0, 6.5], [14, 1.5, 9.5], beam, skip=('west', 'down'))
    m.box([6.5, 0, 2], [9.5, 1.5, 5.5], beam, skip=('south', 'down'))
    m.box([6.5, 0, 10.5], [9.5, 1.5, 14], beam, skip=('north', 'down'))
    m.box([3.5, 1.5, 7], [5.5, 2.25, 9], beam, skip=('east', 'down'))
    m.box([10.5, 1.5, 7], [12.5, 2.25, 9], beam, skip=('west', 'down'))
    m.box([7, 1.5, 3.5], [9, 2.25, 5.5], beam, skip=('south', 'down'))
    m.box([7, 1.5, 10.5], [9, 2.25, 12.5], beam, skip=('north', 'down'))
    return m


def tavern_chair():
    """A spindle-back chair: turned posts with finials, three spindles under an arched crest rail."""
    m = Model('tavern_chair', [[2, 6, 2, 14, 8, 14], [2, 0, 2, 4, 6, 4], [12, 0, 2, 14, 6, 4], [2, 0, 12, 4, 6, 14], [12, 0, 12, 14, 6, 14], [2, 8, 12, 14, 16, 14]], gui=.55, gui_y=-1)
    leg, seat = 'mc:stripped_spruce_log', 'mc:spruce_planks'
    for x in (2, 12):
        m.box([x, 0, 2], [x + 2, 6, 4], leg, skip=('up',))
        m.box([x, 0, 12], [x + 2, 6, 14], leg, skip=('up',))
        m.box([x, 8, 12], [x + 2, 16.5, 14], leg, skip=('down',))
        m.box([x + .5, 16.5, 12.5], [x + 1.5, 17.5, 13.5], leg, skip=('down',))
        m.box([x + .5, 2, 4], [x + 1.5, 3, 12], leg, skip=('north', 'south'))
    m.box([4, 3.5, 2.5], [12, 4.5, 3.5], leg, skip=('east', 'west'))
    m.box([4, 2, 12.5], [12, 3, 13.5], leg, skip=('east', 'west'))
    m.box([2, 6, 2], [14, 8, 14], seat)
    for x in (5, 7.5, 10):
        m.box([x, 8, 12.5], [x + 1, 13.5, 13.5], leg, skip=('up', 'down'))
    m.box([4, 13.5, 12.25], [12, 16, 13.75], seat, skip=('east', 'west'))
    m.box([5.5, 16, 12.25], [10.5, 16.75, 13.75], seat, skip=('down',))
    return m


def bar_stool():
    """A round seat on a turned post, with an iron foot ring and a cross foot."""
    m = Model('bar_stool', [[3, 9, 3, 13, 11, 13], [5, 0, 5, 11, 9, 11]], gui=.62)
    seat, side, wood, ring = 'mc:stripped_spruce_log_top', 'mc:spruce_planks', 'mc:stripped_spruce_log', 'ws:iron'
    top = {'up': seat, 'down': seat, '*': side}
    # The seat is an octagon in five pieces, so no two faces overlap.
    m.box([4, 9, 4], [12, 11, 12], top)
    m.box([3, 9, 5], [4, 11, 11], top, skip=('east',))
    m.box([12, 9, 5], [13, 11, 11], top, skip=('west',))
    m.box([5, 9, 3], [11, 11, 4], top, skip=('south',))
    m.box([5, 9, 12], [11, 11, 13], top, skip=('north',))
    m.box([6, 8, 6], [10, 9, 10], wood, skip=('up',))
    m.box([7, 1.5, 7], [9, 8, 9], wood, skip=('up', 'down'))
    # The foot ring on four spokes.
    m.box([5, 4, 5], [11, 5, 6], ring)
    m.box([5, 4, 10], [11, 5, 11], ring)
    m.box([5, 4, 6], [6, 5, 10], ring, skip=('north', 'south'))
    m.box([10, 4, 6], [11, 5, 10], ring, skip=('north', 'south'))
    m.box([6, 4.25, 7.75], [7, 4.75, 8.25], ring, skip=('east', 'west'))
    m.box([9, 4.25, 7.75], [10, 4.75, 8.25], ring, skip=('east', 'west'))
    m.box([7.75, 4.25, 6], [8.25, 4.75, 7], ring, skip=('north', 'south'))
    m.box([7.75, 4.25, 9], [8.25, 4.75, 10], ring, skip=('north', 'south'))
    # A cross foot.
    m.box([6.5, 0, 6.5], [9.5, 1.5, 9.5], wood, skip=('down',))
    m.box([5, 0, 7.25], [6.5, 1, 8.75], wood, skip=('east', 'down'))
    m.box([9.5, 0, 7.25], [11, 1, 8.75], wood, skip=('west', 'down'))
    m.box([7.25, 0, 5], [8.75, 1, 6.5], wood, skip=('south', 'down'))
    m.box([7.25, 0, 9.5], [8.75, 1, 11], wood, skip=('north', 'down'))
    return m


def fireside_armchair():
    """A wingback armchair: padded rolled arms, a buttoned back, a piped cushion, brass nailheads
    and four short dark-oak feet."""
    m = Model('fireside_armchair', [[1, 0, 1, 15, 8, 15], [0, 0, 1, 2, 12, 16], [14, 0, 1, 16, 12, 16], [2, 8, 13, 14, 16, 16]], gui=.5, gui_y=-1.5)
    foot = 'mc:stripped_dark_oak_log'
    for x in (.5, 13.5):
        for z in (1.5, 13.5):
            m.box([x, 0, z], [x + 2, 2, z + 2], foot, skip=('up',))
    for left in (True, False):
        x0, x1 = (0, 2) if left else (14, 16)
        outer = 'west' if left else 'east'
        # The arm panel, nailheads down its front and along the top of its outside.
        m.box([x0, 2, 1], [x1, 10, 16], {'north': 'tack_column', outer: 'cloth_tacks', '*': 'cloth'},
              uv={'north': [1, 0, 3, 8] if left else [0, 0, 2, 8], outer: [1, 0, 16, 8] if left else [0, 0, 15, 8]}, skip=('up',))
        # The padded roll on top, a little wider than the panel.
        r0, r1 = (0, 3) if left else (13, 16)
        m.box([r0, 10, 1], [r1, 12, 16], {'north': 'roll_end', '*': 'cloth'}, uv={'north': [0, 0, 3, 2]})
        # The wing, curving back as it rises.
        for y0, y1, z0 in ((12, 15, 10.5), (15, 17.5, 11.5), (17.5, 19.5, 13)):
            m.box([x0, y0, z0], [x1, y1, 16], {'north': 'tack_column', '*': 'cloth'},
                  uv={'north': [1, 0, 3, y1 - y0] if left else [0, 0, 2, y1 - y0]}, skip=('down',) if y0 > 12 else ())
    # The base (nailheads under the cushion), the cushion and the buttoned back.
    m.box([2, 2, 1.5], [14, 6, 13], {'north': 'cloth_tacks', '*': 'cloth'}, uv={'north': [2, 0, 14, 4]}, skip=('east', 'west', 'south', 'up'))
    m.box([2, 6, 1], [14, 8, 13], {'up': 'cushion', 'north': 'piping', '*': 'cloth'}, uv={'north': [2, 0, 14, 2]}, skip=('east', 'west', 'south'))
    m.box([2, 2, 13], [14, 8, 16], {'south': 'cloth_tacks', '*': 'cloth'}, uv={'south': [2, 6, 14, 0]}, skip=('north', 'east', 'west'))
    m.box([2, 8, 13], [14, 20, 16], {'north': 'tufted', '*': 'cloth'}, uv={'north': [2, 2, 14, 14]}, skip=('down',))
    m.box([3.5, 20, 13.5], [12.5, 21, 16], 'cloth', skip=('down',))
    m.box([5.5, 21, 14], [10.5, 21.5, 16], 'cloth', skip=('down',))
    return m


def designs():
    return {m.name: m for m in (tavern_table(), tavern_chair(), bar_stool(), fireside_armchair())}


PARTICLES = {'tavern_table': 'mc:dark_oak_planks', 'tavern_chair': 'mc:spruce_planks', 'bar_stool': 'mc:spruce_planks', 'fireside_armchair': 'cloth'}
SOUNDS = {'fireside_armchair': 'WOOL'}


# -- compiling --------------------------------------------------------------------------------------

def blockstate(name):
    return {'variants': {f'facing={facing}': {'model': f'{NS}:block/{name}', 'y': y} for facing, y in kit.ROTATION}}


def dump(data, indent=2):
    return (json.dumps(data, indent=indent) + '\n').encode()


def outputs():
    """Every compiled file: path -> bytes."""
    files = {}
    for key, image in textures().items():
        buffer = io.BytesIO(); image.save(buffer, 'PNG')
        files[ASSETS / f'textures/block/tavern/{key}.png'] = buffer.getvalue()
    for name, model in designs().items():
        files[ASSETS / f'models/block/{name}.json'] = dump(model.json(PARTICLES[name]), 1)
        files[ASSETS / f'blockstates/{name}.json'] = dump(blockstate(name))
        files[ASSETS / f'models/item/{name}.json'] = dump({'parent': f'{NS}:block/{name}'})
        files[ASSETS / f'items/{name}.json'] = dump({'model': {'type': 'minecraft:model', 'model': f'{NS}:item/{name}'}})
    return files


def write():
    for path, data in outputs().items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    print(f'Tavern furniture: {len(designs())} blocks, {len(textures())} textures.')


def java_boxes():
    """The collision boxes TavernBlocks.java registers, by block name."""
    source = JAVA.read_text(encoding='utf-8')
    found = {}
    for name, body in re.findall(r'add\("(\w+)",\s*new double\[\]\[\]\{(.*?)\},\s*SoundType', source):
        found[name] = [[float(c) for c in row.split(',')] for row in re.findall(r'\{([^{}]*)\}', body)]
    return found


def check():
    def same(path, data):
        # Git may check text files out with CRLF line endings; compare them line by line.
        if not path.exists():
            return False
        current = path.read_bytes()
        return current == data if path.suffix == '.png' else current.replace(b'\r\n', b'\n') == data
    problems = [f'out of date: {p.relative_to(PROJECT)}' for p, data in outputs().items() if not same(p, data)]
    painted, borrowed = set(textures()), set(paint.textures())
    java = java_boxes()
    for name, model in designs().items():
        if java.get(name) != [[float(c) for c in b] for b in model.boxes]:
            problems.append(f'{name}: TavernBlocks.java boxes {java.get(name)} differ from the design (run --boxes)')
        for e in model.elements:
            for c in e['from'] + e['to']:
                assert -16 <= c <= 32, (name, e)
            for face in e['faces'].values():
                assert all(0 <= c <= 16 for c in face['uv']), (name, e['from'], face)
        for path in model.textures.values():
            key = path.rsplit('/', 1)[1]
            if path.startswith(f'{NS}:block/tavern/') and key not in painted or path.startswith(f'{NS}:block/workstation/') and key not in borrowed:
                problems.append(f'{name}: missing texture {path}')
    if problems:
        print('Run tools/tavern/furniture.py:\n  ' + '\n  '.join(problems)); sys.exit(1)
    print('Tavern furniture is up to date.')


def boxes():
    for name, model in designs().items():
        rows = ','.join('{' + ','.join(f'{c:g}' for c in b) + '}' for b in model.boxes)
        print(f'add("{name}", new double[][]{{{rows}}}, SoundType.{SOUNDS.get(name, "WOOD")});')


# -- preview ----------------------------------------------------------------------------------------
# workstations.render draws one model; a scene is just a model-like bag of elements, turned the way
# the blockstates turn them and shrunk to fit the canvas.

class Missing(dict):
    def __missing__(self, key):
        return Image.new('RGBA', (16, 16), (150, 110, 70, 255))


def preview_textures(models):
    found = Missing({f'{NS}:block/tavern/{k}': v for k, v in textures().items()})
    found.update({f'{NS}:block/workstation/{k}': v for k, v in paint.textures().items()})
    jars = sorted(Path.home().glob('.gradle/caches/fabric-loom/*/minecraft-client.jar'))
    wanted = {v for m in models for v in m.textures.values() if v.startswith('minecraft:')}
    if jars:
        with zipfile.ZipFile(jars[-1]) as jar:
            for key in wanted:
                try:
                    found[key] = Image.open(io.BytesIO(jar.read(f'assets/minecraft/textures/{key[10:]}.png'))).convert('RGBA').crop((0, 0, 16, 16))
                except KeyError:
                    pass
    return found


FLOOR = 'mc:oak_planks'
TURN = {'north': 'east', 'east': 'south', 'south': 'west', 'west': 'north', 'up': 'up', 'down': 'down'}
SIDE = {'west': (0, False), 'east': (0, True), 'down': (1, False), 'up': (1, True), 'north': (2, False), 'south': (2, True)}


def corners(face, frm, to, spec):
    """A face's corners as kit.render draws them (top-left, top-right, bottom-right, bottom-left of the texture)."""
    tl, tr, br, bl = kit.CORNERS[face](frm, to)
    for _ in range(spec.get('rotation', 0) // 90):
        tl, tr, br, bl = bl, tl, tr, br
    return tl, tr, br, bl


def diced(model, step=1):
    """The model cut into pieces at most `step` texels across, keeping only the outside faces and
    their share of the UVs. kit.render sorts whole faces by their middles, which draws a big face
    (a table top) over smaller things in front of it; small pieces sort correctly."""
    out = Scene()
    out.textures = dict(model.textures)
    for e in model.elements:
        lo, hi = e['from'], e['to']
        cuts = []
        for i in range(3):
            n = max(1, math.ceil((hi[i] - lo[i]) / step - 1e-9))
            cuts.append([lo[i] + (hi[i] - lo[i]) * k / n for k in range(n + 1)])
        for i in range(len(cuts[0]) - 1):
            for j in range(len(cuts[1]) - 1):
                for k in range(len(cuts[2]) - 1):
                    a = [cuts[0][i], cuts[1][j], cuts[2][k]]
                    b = [cuts[0][i + 1], cuts[1][j + 1], cuts[2][k + 1]]
                    faces = {}
                    for face, spec in e['faces'].items():
                        axis, high = SIDE[face]
                        if (b if high else a)[axis] != (hi if high else lo)[axis]:
                            continue  # a cut inside the element
                        ptl, ptr, _, pbl = corners(face, lo, hi, spec)
                        stl, str_, _, sbl = corners(face, a, b, spec)

                        def along(p, end):
                            d = [end[t] - ptl[t] for t in range(3)]
                            n2 = sum(c * c for c in d)
                            return sum((p[t] - ptl[t]) * d[t] for t in range(3)) / n2 if n2 else 0
                        u1, v1, u2, v2 = spec['uv']
                        uv = [u1 + (u2 - u1) * along(stl, ptr), v1 + (v2 - v1) * along(stl, pbl),
                              u1 + (u2 - u1) * along(str_, ptr), v1 + (v2 - v1) * along(sbl, pbl)]
                        faces[face] = dict(spec, uv=uv)
                    if faces:
                        out.elements.append({**e, 'from': a, 'to': b, 'faces': faces})
    return out


def turned(element, quarters):
    """An element as a blockstate's y rotation of 90 * quarters places it (north turns to east)."""
    e = json.loads(json.dumps(element))
    for _ in range(quarters):
        (x1, y1, z1), (x2, y2, z2) = e['from'], e['to']
        e['from'], e['to'] = [16 - z2, y1, x1], [16 - z1, y2, x2]
        faces = {}
        for face, spec in e['faces'].items():
            if face in ('up', 'down'):  # their textures turn with the model (no uvlock)
                spec['rotation'] = (spec.get('rotation', 0) + (270 if face == 'up' else 90)) % 360
            faces[TURN[face]] = spec
        e['faces'] = faces
        if 'rotation' in e:
            r = e['rotation']
            ox, oy, oz = r['origin']
            r['origin'] = [16 - oz, oy, ox]
            if r['axis'] == 'x':
                r['axis'] = 'z'
            elif r['axis'] == 'z':
                r['axis'], r['angle'] = 'x', -r['angle']
    return e


class Scene:
    def __init__(self):
        self.elements, self.textures = [], {}

    def place(self, model, x, z, facing='north'):
        for e in diced(model).elements:
            e = turned(e, [f for f, _ in kit.ROTATION].index(facing))
            for key in ('from', 'to'):
                e[key] = [e[key][0] + 16 * x, e[key][1], e[key][2] + 16 * z]
            if 'rotation' in e:
                o = e['rotation']['origin']
                e['rotation']['origin'] = [o[0] + 16 * x, o[1], o[2] + 16 * z]
            self.elements.append(e)
        self.textures.update(model.textures)
        return self

    def shrink(self, k, center):
        def fit(p):
            return [8 + (p[i] - center[i]) * k for i in range(3)]
        for e in self.elements:
            e['from'], e['to'] = fit(e['from']), fit(e['to'])
            if 'rotation' in e:
                e['rotation']['origin'] = fit(e['rotation']['origin'])
        return self


def scene():
    """A long table of three with chairs down both sides, a stool at its head and two armchairs facing it."""
    d = designs()
    floor = Model('floor', [])
    for x in range(-1, 6):
        for z in range(-1, 3):
            floor.box([16 * x, -1, 16 * z], [16 * x + 16, 0, 16 * z + 16], FLOOR, uv={'up': [0, 0, 16, 16]}, only=('up',))
    s = Scene().place(floor, 0, 0)
    for x in range(3):
        s.place(d['tavern_table'], x, 0)
        s.place(d['tavern_chair'], x, -1, 'south')  # north of the table, facing it
        s.place(d['tavern_chair'], x, 1, 'north')   # south of the table, facing it
    s.place(d['bar_stool'], -1, 0, 'east')
    s.place(d['fireside_armchair'], 4, 0, 'west')
    s.place(d['fireside_armchair'], 4, 1, 'west')
    return s.shrink(.36, (48, 8, 16))


def preview():
    models = list(designs().values())
    found = preview_textures(models + [Model('floor', []).box([0, 0, 0], [1, 1, 1], FLOOR)])
    dest = PROJECT / 'build/previews'
    dest.mkdir(parents=True, exist_ok=True)
    tile = 360
    sheet = Image.new('RGB', (tile * 4, (tile + 24) * 2), '#7FA7C9')
    draw = ImageDraw.Draw(sheet)
    for n, model in enumerate(models):
        front, back = kit.render(diced(model), found), kit.render(diced(model), found, view=(-1, .9, 1.15))
        front.save(dest / f'tavern-{model.name}.png')
        x, y = (n % 2) * tile * 2, (n // 2) * (tile + 24)
        for i, view in enumerate((front, back)):
            small = view.resize((tile, tile))
            sheet.paste(small, (x + i * tile, y + 24), small)
        draw.text((x + 8, y + 6), f'{model.name}  (front from the north-east, back from the south-west)', fill='#10202E')
    sheet.save(dest / 'tavern_furniture.png')
    views = [kit.render(scene(), found, scale=22), kit.render(scene(), found, scale=22, view=(-1, .9, 1.15))]
    board = Image.new('RGB', (views[0].width * 2, views[0].height), '#7FA7C9')
    for i, view in enumerate(views):
        board.paste(view, (i * view.width, 0), view)
    ImageDraw.Draw(board).text((10, 8), 'north-east view  |  south-west view  (chairs face the table; the stool faces east, the armchairs west)', fill='#10202E')
    board.save(dest / 'tavern_scene.png')
    print(dest / 'tavern_furniture.png')
    print(dest / 'tavern_scene.png')


if __name__ == '__main__':
    if '--check' in sys.argv: check()
    elif '--preview' in sys.argv: preview()
    elif '--boxes' in sys.argv: boxes()
    else: write()
