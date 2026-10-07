"""Designs, compiles and previews the ten profession workstations (eleven blocks).

Each workstation is a small program of cuboids, like the village building designs: wood and stone
come from vanilla textures so the stations sit naturally in a village; everything with character
(the dummy's stitched face, the target's rings, the oven door, the barrel's apple brand, sheet music,
the paintings on the easel) is hand-authored pixel art in paint.py. One texel is always 1/16 block.

    python tools/workstations/workstations.py            # write models, blockstates, item models, textures
    python tools/workstations/workstations.py --check    # verify the compiled files match the designs
    python tools/workstations/workstations.py --preview  # isometric previews in build/previews/workstations.png
    python tools/workstations/workstations.py --boxes    # print the collision boxes for VillageBlocks.java

Never hand-edit the compiled JSON or PNG; change the design or paint.py and rerun.
"""
import io
import json
import math
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paint  # noqa: E402

PROJECT = Path(__file__).resolve().parents[2]
ASSETS = PROJECT / 'src/main/resources/assets/villagefriends'
NS = 'villagefriends'
FACES = ('north', 'south', 'east', 'west', 'up', 'down')


class Model:
    def __init__(self, name, boxes, gui=0.625, gui_y=0.0):
        self.name, self.boxes, self.elements, self.textures = name, boxes, [], {}
        self.gui, self.gui_y = gui, gui_y

    def tex(self, key):
        """'mc:spruce_planks' is a vanilla texture; anything else is one of ours from paint.py."""
        ref = key.replace(':', '_')
        self.textures[ref] = f'minecraft:block/{key[3:]}' if key.startswith('mc:') else f'{NS}:block/workstation/{key}'
        return '#' + ref

    def box(self, frm, to, tex, uv=None, skip=(), rot=None, light=0, face_rot=None, only=None):
        """A cuboid. tex is one texture for every face or a dict by face ('*' for the rest)."""
        faces = {}
        for face in (only or FACES):
            if face in skip:
                continue
            key = tex.get(face, tex.get('*')) if isinstance(tex, dict) else tex
            if key is None:
                continue
            entry = {'texture': self.tex(key), 'uv': list((uv or {}).get(face) or auto_uv(face, frm, to))}
            if face_rot and face in face_rot:
                entry['rotation'] = face_rot[face]
            faces[face] = entry
        element = {'from': list(frm), 'to': list(to), 'faces': faces}
        if rot:
            axis, angle, origin = rot
            element['rotation'] = {'origin': list(origin), 'axis': axis, 'angle': angle}
        if light:
            element['light_emission'] = light
        self.elements.append(element)
        return self

    def plane(self, frm, to, tex, uv, axis_faces, rot=None, light=0):
        """A flat cutout card (zero thickness), visible from both sides."""
        return self.box(frm, to, tex, uv={f: uv for f in axis_faces}, only=axis_faces, rot=rot, light=light)

    def json(self, particle):
        textures = dict(self.textures)
        textures['particle'] = textures.get(particle.replace(':', '_'), f'{NS}:block/workstation/{particle}') if not particle.startswith('mc:') else f'minecraft:block/{particle[3:]}'
        return {
            'parent': 'minecraft:block/block',
            'textures': textures,
            'elements': self.elements,
            'display': {
                'gui': {'rotation': [30, 225, 0], 'translation': [0, self.gui_y, 0], 'scale': [self.gui] * 3},
                'ground': {'rotation': [0, 0, 0], 'translation': [0, 3, 0], 'scale': [0.25] * 3},
                'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [self.gui * .8] * 3},
                'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [0.375 * self.gui / .625] * 3},
                'firstperson_righthand': {'rotation': [0, 45, 0], 'translation': [0, 0, 0], 'scale': [0.4 * self.gui / .625] * 3},
                'firstperson_lefthand': {'rotation': [0, 225, 0], 'translation': [0, 0, 0], 'scale': [0.4 * self.gui / .625] * 3},
            },
        }


def auto_uv(face, frm, to):
    """Vanilla's default UVs, shifted a whole block when an element pokes above or beside the block."""
    x1, y1, z1 = frm
    x2, y2, z2 = to
    u1, v1, u2, v2 = {
        'down': (x1, 16 - z2, x2, 16 - z1), 'up': (x1, z1, x2, z2),
        'north': (16 - x2, 16 - y2, 16 - x1, 16 - y1), 'south': (x1, 16 - y2, x2, 16 - y1),
        'west': (z1, 16 - y2, z2, 16 - y1), 'east': (16 - z2, 16 - y2, 16 - z1, 16 - y1),
    }[face]

    def fit(a, b):
        while min(a, b) < 0:
            a, b = a + 16, b + 16
        while max(a, b) > 16:
            a, b = a - 16, b - 16
        if min(a, b) < 0:  # straddles a block edge: take it from the top-left of the texture
            size = abs(b - a)
            return (0, size) if a <= b else (size, 0)
        return a, b
    u1, u2 = fit(u1, u2)
    v1, v2 = fit(v1, v2)
    return [round(u1, 4), round(v1, 4), round(u2, 4), round(v2, 4)]


# -- the designs ------------------------------------------------------------------------------------

def training_dummy():
    m = Model('training_dummy', [[1, 0, 1, 15, 3, 15], [6, 3, 6, 10, 16, 10], [4, 10, 5, 12, 16, 11]], gui=.42, gui_y=-2)
    m.box([1, 0, 7], [15, 2, 9], 'mc:spruce_planks')
    m.box([7, 0, 1], [9, 2, 15], 'mc:spruce_planks')
    m.box([6, 0, 6], [10, 3, 10], {'up': 'mc:spruce_log_top', '*': 'mc:spruce_log'})
    m.box([7, 3, 7], [9, 10, 9], 'mc:spruce_log', skip=('up', 'down'))
    # A straw-stuffed burlap body with a painted bullseye, a rope belt and stubby arms.
    m.box([4, 10, 5], [12, 20, 11], {'north': 'dummy_chest', '*': 'burlap'},
          uv={'north': [4, 0, 12, 10], 'south': [4, 0, 12, 10], 'east': [5, 0, 11, 10], 'west': [5, 0, 11, 10]})
    m.box([3.75, 12, 4.75], [12.25, 13, 11.25], 'rope', skip=('up', 'down'))
    m.box([0, 16, 6.5], [4, 19.5, 9.5], 'burlap_plain', skip=('east',))
    m.box([12, 16, 6.5], [16, 19.5, 9.5], 'burlap_plain', skip=('west',))
    m.box([-1.5, 16.25, 6.75], [0, 19.25, 9.25], 'straw', skip=('east',))
    m.box([16, 16.25, 6.75], [17.5, 19.25, 9.25], 'straw', skip=('west',))
    m.box([3.75, 20, 4.25], [12.25, 21, 11.75], 'rope', skip=('down',))
    # A sack head with stitched eyes, wearing an old iron pot for a helmet.
    m.box([4, 20.5, 4.5], [12, 27, 11.5], {'north': 'dummy_face', '*': 'burlap_plain'}, skip=('up', 'down'))
    m.box([3.5, 26.5, 4], [12.5, 28.5, 12], 'iron')
    m.box([7, 28.5, 7.5], [9, 29.5, 9.5], 'iron', skip=('down',))
    return m


def archery_target():
    m = Model('archery_target', [[1, 0, 6, 15, 16, 9], [2, 0, 9, 14, 3, 11]], gui=.62)
    for x in (2, 12):
        m.box([x, 0, 9], [x + 2, 15, 11], 'mc:stripped_spruce_log', skip=('down',))
    m.box([2, 1.5, 9.5], [14, 3, 10.5], 'mc:stripped_spruce_log', skip=('down',))
    # A back prop braces the frame.
    m.box([7.25, 0, 10], [8.75, 14, 11.5], 'mc:stripped_spruce_log', rot=('x', -22.5, [8, 14, 10]))
    # The straw boss with painted rings, centered at x=8, y=9 on its face.
    m.box([1, 2, 6], [15, 16, 9], {'north': 'target_face', '*': 'straw'})
    # Two arrows stuck in the rings.
    for x, y in ((4.5, 12), (10.25, 7.25)):
        m.box([x, y, 3], [x + .5, y + .5, 6], 'arrow', uv={'east': [0, 7, 3, 7.5], 'west': [0, 7, 3, 7.5], 'up': [0, 7, .5, 10], 'down': [0, 7, .5, 10]}, skip=('south',))
        m.box([x - .75, y, 3], [x + 1.25, y + .5, 4], 'arrow', uv={'north': [11, 6, 13, 6.5], 'east': [13, 6, 14, 6.5], 'west': [13, 6, 14, 6.5], 'up': [11, 6, 13, 7], 'down': [11, 6, 13, 7], 'south': [11, 6, 13, 6.5]})
    return m


def kitchen_stove(lit):
    m = Model('kitchen_stove_lit' if lit else 'kitchen_stove', [[0, 0, 1, 16, 13, 16], [2, 13, 4, 8, 16, 10], [11, 13, 11, 14, 16, 14]], gui=.55, gui_y=-1)
    m.box([0, 0, 1], [16, 13, 16], {'north': 'stove_front', 'up': 'stove_top', '*': 'stove_bricks'}, uv={'north': [0, 0, 16, 13]})
    if lit:  # The firebox glows through its grate.
        m.box([4, 2, .9], [12, 7, 1], 'stove_front_lit', uv={'north': [4, 6, 12, 11]}, only=('north',), light=13)
    # A towel on the rail.
    m.box([1, 10.5, 0], [15, 11.25, .75], 'brass', skip=('south',))
    m.box([2.5, 6.5, .25], [6, 10.5, .75], 'cloth_wine', skip=('south',))
    # A stew pot and a copper kettle on the cooktop, and the chimney pipe behind.
    m.box([2, 13, 4], [8, 17, 10], {'up': 'stew', '*': 'pot_side'}, skip=('down',))
    m.box([1.25, 15, 6.5], [2, 16, 7.5], 'iron')
    m.box([8, 15, 6.5], [8.75, 16, 7.5], 'iron')
    m.box([10, 13, 3.5], [14, 16.5, 7.5], 'copper', skip=('down',))
    m.box([11.5, 16.5, 5], [12.5, 17.25, 6], 'brass', skip=('down',))
    m.box([14, 14.25, 5], [15.75, 15, 6], 'copper')
    m.box([11, 17, 5.25], [13, 17.5, 5.75], 'iron')
    m.box([10.5, 13, 10.5], [14.5, 14, 14.5], 'iron', skip=('down',))
    m.box([11, 14, 11], [14, 24, 14], 'pipe', skip=('down',), uv={f: [0, 0, 3, 10] for f in ('north', 'south', 'east', 'west')})
    return m


def drinks_barrel():
    m = Model('drinks_barrel', [[1, 0, 1, 15, 15, 15]], gui=.62)
    for z in (2.5, 11.5):  # cradle
        m.box([1, 0, z], [15, 2.5, z + 2], 'mc:spruce_planks')
        for x in (2, 12.5):
            m.box([x, 2.5, z], [x + 1.5, 4, z + 2], 'mc:spruce_planks', skip=('down',))
    # The barrel on its side: an octagon from three pieces so its ends tile cleanly.
    m.box([4, 1.5, 1], [12, 14.5, 15], {'north': 'barrel_end', 'south': 'barrel_end', 'up': 'staves_v', 'down': 'staves_v', '*': 'staves_h'})
    m.box([2, 3, 1], [4, 13, 15], {'north': 'barrel_end', 'south': 'barrel_end', 'up': 'staves_v', 'down': 'staves_v', '*': 'staves_h'}, skip=('east',))
    m.box([12, 3, 1], [14, 13, 15], {'north': 'barrel_end', 'south': 'barrel_end', 'up': 'staves_v', 'down': 'staves_v', '*': 'staves_h'}, skip=('west',))
    # A brass spigot, and a mug of cider waiting on top.
    m.box([7.25, 5.25, 0], [8.75, 6.75, 1], 'brass', skip=('south',))
    m.box([7.5, 4, .25], [8.5, 5.25, 1], 'brass', skip=('south',))
    m.box([7.75, 6.75, .4], [8.25, 8.5, .9], 'brass')
    m.box([9, 14.5, 5], [12, 17.5, 8], {'up': 'cider_top', '*': 'mug'}, uv={'up': [1, 1, 4, 4]}, skip=('down',))
    m.box([12, 15.25, 6], [12.75, 16.75, 7], 'mug')
    return m


def tap_stand():
    m = Model('tap_stand', [[1, 0, 2, 15, 10, 14], [4, 10, 5, 12, 16, 13]], gui=.6, gui_y=-.5)
    m.box([1, 0, 2], [15, 9, 14], {'north': 'cabinet_front', '*': 'mc:spruce_planks'}, uv={'north': [1, 0, 15, 9]})
    m.box([.5, 9, 1.5], [15.5, 10, 14.5], 'mc:dark_oak_planks')
    # A copper coffee urn with a brass band, lid and tap.
    m.box([4, 10, 5], [12, 11, 13], 'brass', skip=('down',))
    m.box([4.5, 11, 5.5], [11.5, 12, 12.5], 'copper', skip=('down',))
    m.box([4, 12, 5], [12, 16, 13], 'copper')
    m.box([4.5, 16, 5.5], [11.5, 17, 12.5], 'copper', skip=('down',))
    m.box([5.5, 17, 6.5], [10.5, 17.75, 11.5], 'brass', skip=('down',))
    m.box([6, 17.75, 7], [10, 18.5, 11], 'copper', skip=('down',))
    m.box([7.5, 18.5, 8.5], [8.5, 19.5, 9.5], 'brass', skip=('down',))
    for x in (3, 12):  # carrying handles
        m.box([x, 13, 8.5], [x + 1, 15.5, 9.5], 'brass')
    m.box([7.25, 12, 3.5], [8.75, 13.25, 5], 'brass', skip=('south',))
    m.box([7.5, 11, 3.75], [8.5, 12, 4.5], 'brass')
    m.box([7.75, 13.25, 4], [8.25, 14.75, 4.5], 'brass')
    m.box([6, 10, 2], [10, 10.5, 4.5], 'iron', skip=('down',))
    m.box([12.5, 10, 2.5], [14.5, 12.5, 4.5], {'up': 'cider_top', '*': 'mug'}, uv={'up': [1, 1, 3, 3]}, skip=('down',))
    return m


def alchemical_press():
    m = Model('alchemical_press', [[.5, 0, .5, 15.5, 2, 15.5], [1.5, 2, 6, 3.5, 16, 10], [12.5, 2, 6, 14.5, 16, 10], [3.5, 2, 3.5, 12.5, 9, 12.5]], gui=.58, gui_y=-1)
    m.box([.5, 0, .5], [15.5, 2, 15.5], 'mc:polished_andesite')
    for x in (1.5, 12.5):
        m.box([x, 2, 6], [x + 2, 15, 10], 'mc:stripped_dark_oak_log', skip=('down',))
    m.box([1, 15, 5.5], [15, 17, 10.5], 'mc:dark_oak_planks')
    # The screw, its turning bar and the press plate squeezing a vat of herbs.
    m.box([7, 9, 7], [9, 15, 9], 'iron', skip=('up', 'down'))
    m.box([7, 17, 7], [9, 18.5, 9], 'iron', skip=('down',))
    m.box([3, 18, 7.5], [13, 19, 8.5], 'mc:stripped_dark_oak_log')
    for x in (2.25, 12.75):
        m.box([x, 17.75, 7.25], [x + 1, 19.25, 8.75], 'brass')
    m.box([4, 8, 4], [12, 9, 12], 'iron')
    m.box([4.25, 7.5, 4.25], [11.75, 8, 11.75], 'herbs', skip=('down',))
    m.box([3.5, 2, 3.5], [12.5, 7.5, 12.5], {'up': 'herbs', '*': 'vat_side'}, skip=('down',))
    # Tonic drips down a spout into a bottle.
    m.box([7, 2.5, 1.5], [9, 3.5, 3.5], 'mc:dark_oak_planks', skip=('down',))
    m.plane([4.5, 2, 2.25], [9.5, 9, 2.25], 'small_bottle', [5, 7, 10, 14], ('north', 'south'), rot=('y', 45, [7, 2, 2.25]))
    m.plane([4.5, 2, 2.25], [9.5, 9, 2.25], 'small_bottle', [5, 7, 10, 14], ('north', 'south'), rot=('y', -45, [7, 2, 2.25]))
    return m


def easel_canvas(art):
    m = Model(f'easel_canvas_art{art}', [[2, 0, 4, 14, 16, 8.5], [7, 0, 9, 9, 3, 13]], gui=.42, gui_y=-2)
    for x in (3, 11.5):
        m.box([x, 0, 7], [x + 1.5, 16, 8.5], 'mc:stripped_spruce_log')
        m.box([x, 16, 7], [x + 1.5, 25, 8.5], 'mc:stripped_spruce_log', skip=('down',))
    for lo, hi in ((0, 16), (16, 23)):
        m.box([7.25, lo, 9], [8.75, hi, 10.5], 'mc:stripped_spruce_log', rot=('x', 12, [8, 23, 9.75]))
    m.box([3, 4, 7.25], [13, 5, 8.25], 'mc:stripped_spruce_log')
    m.box([1.5, 8, 4], [14.5, 9, 7], 'mc:spruce_planks')
    # The canvas itself: blank, a sketch, or one of seven paintings.
    m.box([2, 9, 5.5], [14, 23, 6.5], {'north': f'canvas_{art}', 'south': 'canvas_back', '*': 'canvas_back'},
          uv={'north': [2, 1, 14, 15], 'south': [2, 1, 14, 15], 'east': [0, 1, 1, 15], 'west': [0, 1, 1, 15], 'up': [2, 0, 14, 1], 'down': [2, 0, 14, 1]})
    m.box([7, 23, 5.25], [9, 24.5, 6.75], 'mc:stripped_spruce_log')
    for (x0, u) in ((2.5, 0), (4, 3), (12, 6)):
        m.box([x0, 9, 4.25], [x0 + 1, 10, 5.25], 'paint_pots', uv={f: [u, 0, u + 1, 1] for f in FACES}, skip=('down',))
    return m


def music_stand():
    m = Model('music_stand', [[6.5, 0, 6.5, 9.5, 16, 9.5], [2, 11, 6, 14, 16, 9]], gui=.5, gui_y=-1.5)
    m.box([7, 0, 7], [9, 2.5, 9], 'iron')
    for angle in (0, 120, -120):
        m.box([7.5, 0, 1.5], [8.5, 1, 8], 'iron', rot=('y', angle, [8, 0, 8]), skip=('down',))
    m.box([7.5, 2.5, 7.5], [8.5, 16, 8.5], 'brass', skip=('up', 'down'))
    m.box([7.5, 16, 7.5], [8.5, 17, 8.5], 'brass', skip=('down',))
    # A tilted desk holding sheet music, with a lip to stop it sliding off.
    tilt = ('x', 22.5, [8, 13, 8])
    m.box([2, 13, 7.5], [14, 23, 8.5], {'north': 'sheet_music', '*': 'mc:dark_oak_planks'},
          uv={'north': [2, 3, 14, 13], 'south': [2, 3, 14, 13], 'east': [7, 3, 8, 13], 'west': [7, 3, 8, 13]}, rot=tilt)
    m.box([2, 12, 6], [14, 13.5, 8.5], 'mc:dark_oak_planks', rot=tilt)
    # A candle on a little arm for evening performances.
    m.box([13.5, 16, 7.5], [15.5, 16.5, 8.5], 'brass')
    m.box([14, 16.5, 7.5], [15, 19, 8.5], 'candle', uv={f: [6, 7, 7, 9.5] for f in FACES})
    m.plane([13.75, 19, 8], [15.25, 20.5, 8], 'candle', [5.25, 4, 6.75, 5.5], ('north', 'south'), light=12)
    return m


def sewing_table():
    m = Model('sewing_table', [[0, 11, 0, 16, 13, 16], [1, 0, 1, 3, 11, 3], [13, 0, 1, 15, 11, 3], [1, 0, 13, 3, 11, 15], [13, 0, 13, 15, 11, 15], [1, 3, 1, 15, 4, 15]], gui=.62)
    m.box([0, 11, 0], [16, 13, 16], 'mc:oak_planks')
    for x in (1, 13):
        for z in (1, 13):
            m.box([x, 0, z], [x + 2, 11, z + 2], 'mc:stripped_oak_log', skip=('up',))
    m.box([1, 3, 1], [15, 4, 15], 'mc:oak_planks')
    # Bolts of wine and mustard cloth on the shelf.
    for z, color in ((2, 'wine'), (9.5, 'mustard')):
        m.box([2, 4, z], [14, 7, z + 3.5], {'east': f'bolt_{color}', 'west': f'bolt_{color}', '*': f'cloth_{color}'},
              uv={'east': [6.25, 6.5, 9.75, 9.5], 'west': [6.25, 6.5, 9.75, 9.5]}, skip=('down',))
    # On top: a teal runner, a spool of red thread, a pincushion and a folded stack of cloth.
    m.box([3, 13, 1], [13, 13.25, 15], 'runner', uv={'up': [3, 1, 13, 15]}, skip=('down',))
    m.box([11.5, 13.25, 10.5], [13.5, 16, 12.5], {'up': 'mc:oak_planks', '*': 'spool'}, uv={f: [0, 0, 2, 2.75] for f in ('north', 'south', 'east', 'west')}, skip=('down',))
    m.box([2.5, 13.25, 10.5], [5.5, 15, 13.5], 'pincushion', skip=('down',))
    m.box([5.5, 13.25, 3], [10.5, 14.25, 7.5], 'cloth_mustard', skip=('down',))
    m.box([6, 14.25, 3.5], [10, 15, 7], 'cloth_wine', skip=('down',))
    return m


def sawmill():
    m = Model('sawmill', [[0, 10, 2, 16, 12, 14], [1, 0, 3, 3, 10, 5], [13, 0, 3, 15, 10, 5], [1, 0, 11, 3, 10, 13], [13, 0, 11, 15, 10, 13]], gui=.6)
    m.box([0, 10, 2], [16, 12, 14], 'mc:spruce_planks')
    for x in (1, 13):
        for z in (3, 11):
            m.box([x, 0, z], [x + 2, 10, z + 2], 'mc:stripped_spruce_log', skip=('up',))
    for z in (3.5, 11.5):
        m.box([3, 2, z], [13, 3, z + 1], 'mc:stripped_spruce_log')
    # A round saw blade standing through a slot in the bench, on an iron axle.
    m.plane([8, 4.5, .5], [8, 19.5, 15.5], 'saw_blade', [.5, .5, 15.5, 15.5], ('east', 'west'))
    m.box([7, 11, 7], [9, 13, 9], 'iron', skip=('down',))
    # A log being cut, a stack of planks and a heap of sawdust.
    m.box([1.5, 12, 5], [6.5, 16, 10], {'east': 'mc:oak_log_top', 'west': 'mc:oak_log_top', '*': 'mc:oak_log'},
          face_rot={'north': 90, 'south': 90, 'up': 90}, skip=('down',))
    m.box([10, 12, 10], [15, 13, 13], 'mc:oak_planks', skip=('down',))
    m.box([10.5, 13, 10.5], [14.5, 14, 12.5], 'mc:oak_planks', skip=('down',))
    m.box([9.5, 12, 3.5], [13, 12.5, 8], 'sawdust', skip=('down',))
    return m


def archives():
    m = Model('archives', [[0, 0, 0, 16, 16, 16]], gui=.62)
    m.box([0, 0, 15], [16, 16, 16], 'mc:dark_oak_planks')
    for x in (0, 15):
        m.box([x, 0, 0], [x + 1, 16, 15], 'mc:dark_oak_planks')
    m.box([1, 15, 0], [15, 16, 15], 'mc:dark_oak_planks')
    m.box([1, 0, 0], [15, 1, 15], 'mc:dark_oak_planks')
    for y in (5, 10):
        m.box([1, y, 0], [15, y + 1, 15], 'mc:dark_oak_planks')
    # Pigeonholes of scrolls, ledgers and boxes, set back behind the shelves.
    m.box([1, 1, 3], [15, 15, 4], 'archives_front', uv={'north': [1, 1, 15, 15]}, only=('north',))
    m.box([11.5, 11.25, 2], [13.5, 13.25, 3], {'north': 'archives_front', '*': 'archives_front'}, uv={f: [1, 1, 3, 3] for f in FACES})
    m.box([2.5, 1, 1.5], [6.5, 4.5, 3], 'archives_front', uv={f: [1, 11, 5, 14.5] for f in FACES})
    # An open ledger and a candle on top.
    m.box([2, 16, 3.5], [11, 16.5, 10.5], {'up': 'ledger_open', '*': 'mc:dark_oak_planks'}, uv={'up': [1.5, 4, 10.5, 11]}, skip=('down',))
    m.box([12, 16, 11], [13, 19, 12], 'candle', uv={f: [6, 7, 7, 10] for f in FACES})
    m.plane([11.75, 19, 11.5], [13.25, 20.5, 11.5], 'candle', [5.75, 4, 7.25, 5.5], ('north', 'south'), light=12)
    return m


def designs():
    return {
        'training_dummy': [training_dummy()],
        'archery_target': [archery_target()],
        'kitchen_stove': [kitchen_stove(False), kitchen_stove(True)],
        'drinks_barrel': [drinks_barrel()],
        'tap_stand': [tap_stand()],
        'alchemical_press': [alchemical_press()],
        'easel_canvas': [easel_canvas(art) for art in range(9)],
        'music_stand': [music_stand()],
        'sewing_table': [sewing_table()],
        'sawmill': [sawmill()],
        'archives': [archives()],
    }


PARTICLES = {'training_dummy': 'burlap', 'archery_target': 'straw', 'kitchen_stove': 'stove_bricks', 'drinks_barrel': 'staves_h',
             'tap_stand': 'copper', 'alchemical_press': 'mc:polished_andesite', 'easel_canvas': 'canvas_back', 'music_stand': 'brass',
             'sewing_table': 'mc:oak_planks', 'sawmill': 'mc:spruce_planks', 'archives': 'mc:dark_oak_planks'}
ROTATION = [('north', 0), ('east', 90), ('south', 180), ('west', 270)]


def blockstate(name, models):
    variants = {}
    for facing, y in ROTATION:
        if name == 'kitchen_stove':
            for lit in ('false', 'true'):
                variants[f'facing={facing},lit={lit}'] = {'model': f'{NS}:block/{models[lit == "true"].name}', 'y': y}
        elif name == 'easel_canvas':
            for art, model in enumerate(models):
                variants[f'art={art},facing={facing}'] = {'model': f'{NS}:block/{model.name}', 'y': y}
        else:
            variants[f'facing={facing}'] = {'model': f'{NS}:block/{models[0].name}', 'y': y}
    return {'variants': variants}


def outputs():
    """Every compiled file: path -> bytes."""
    files = {}
    for key, image in paint.textures().items():
        buffer = io.BytesIO(); image.save(buffer, 'PNG')
        files[ASSETS / f'textures/block/workstation/{key}.png'] = buffer.getvalue()
    for name, models in designs().items():
        for model in models:
            files[ASSETS / f'models/block/{model.name}.json'] = (json.dumps(model.json(PARTICLES[name]), indent=1) + '\n').encode()
        files[ASSETS / f'blockstates/{name}.json'] = (json.dumps(blockstate(name, models), indent=1) + '\n').encode()
        item_model = models[0].name if name != 'easel_canvas' else 'easel_canvas_art5'
        files[ASSETS / f'items/{name}.json'] = (json.dumps({'model': {'type': 'minecraft:model', 'model': f'{NS}:block/{item_model}'}}, indent=1) + '\n').encode()
    return files


def write():
    files = outputs()
    for path, data in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    stale = ASSETS / 'textures/block'
    for name in designs():
        old = stale / f'{name}.png'
        if old.exists():
            old.unlink()  # the old single-texture art
    print(f'Workstations: {len(designs())} blocks, {sum(len(m) for m in designs().values())} models, {len(paint.textures())} textures.')


def check():
    bad = [str(p.relative_to(PROJECT)) for p, data in outputs().items() if not p.exists() or p.read_bytes() != data]
    if bad:
        print('Out of date (run tools/workstations/workstations.py):\n  ' + '\n  '.join(bad)); sys.exit(1)
    for name, models in designs().items():
        for model in models:
            for e in model.elements:
                for c in e['from'] + e['to']:
                    assert -16 <= c <= 32, (model.name, e)
                for face in e['faces'].values():
                    u1, v1, u2, v2 = face['uv']
                    assert all(0 <= c <= 16 for c in (u1, v1, u2, v2)), (model.name, e['from'], face)
    print('Workstations are up to date.')


def boxes():
    for name, models in designs().items():
        rows = ','.join('{' + ','.join(f'{c:g}' for c in b) + '}' for b in models[0].boxes)
        print(f'station("{name}", ..., new double[][]{{{rows}}});')


# -- preview ----------------------------------------------------------------------------------------

def vanilla_textures():
    jars = sorted(Path.home().glob('.gradle/caches/fabric-loom/*/minecraft-client.jar'))
    if not jars:
        return {}
    textures = {}
    with zipfile.ZipFile(jars[-1]) as jar:
        for entry in jar.namelist():
            if entry.startswith('assets/minecraft/textures/block/') and entry.endswith('.png'):
                textures['minecraft:block/' + entry.rsplit('/', 1)[1][:-4]] = entry
        cache = {}
        for key, entry in textures.items():
            cache[key] = entry
        loaded = {}
        def load(key):
            if key not in loaded:
                loaded[key] = Image.open(io.BytesIO(jar.read(cache[key]))).convert('RGBA').crop((0, 0, 16, 16))
            return loaded[key]
        wanted = set()
        for models in designs().values():
            for m in models:
                wanted.update(v for v in m.textures.values() if v.startswith('minecraft:'))
        return {k: load(k) for k in wanted if k in cache}


def rotate(point, rot):
    if not rot:
        return point
    axis, angle, origin = rot['axis'], math.radians(rot['angle']), rot['origin']
    x, y, z = (point[i] - origin[i] for i in range(3))
    c, s = math.cos(angle), math.sin(angle)
    if axis == 'x': y, z = y * c - z * s, y * s + z * c
    elif axis == 'y': x, z = x * c + z * s, -x * s + z * c
    else: x, y = x * c - y * s, x * s + y * c
    return (x + origin[0], y + origin[1], z + origin[2])


CORNERS = {  # face -> corners in order (top-left, top-right, bottom-right, bottom-left) as seen on the texture
    'north': lambda a, b: [(b[0], b[1], a[2]), (a[0], b[1], a[2]), (a[0], a[1], a[2]), (b[0], a[1], a[2])],
    'south': lambda a, b: [(a[0], b[1], b[2]), (b[0], b[1], b[2]), (b[0], a[1], b[2]), (a[0], a[1], b[2])],
    'west': lambda a, b: [(a[0], b[1], a[2]), (a[0], b[1], b[2]), (a[0], a[1], b[2]), (a[0], a[1], a[2])],
    'east': lambda a, b: [(b[0], b[1], b[2]), (b[0], b[1], a[2]), (b[0], a[1], a[2]), (b[0], a[1], b[2])],
    'up': lambda a, b: [(a[0], b[1], a[2]), (b[0], b[1], a[2]), (b[0], b[1], b[2]), (a[0], b[1], b[2])],
    'down': lambda a, b: [(a[0], a[1], b[2]), (b[0], a[1], b[2]), (b[0], a[1], a[2]), (a[0], a[1], a[2])],
}
NORMALS = {'north': (0, 0, -1), 'south': (0, 0, 1), 'west': (-1, 0, 0), 'east': (1, 0, 0), 'up': (0, 1, 0), 'down': (0, -1, 0)}
SHADE = {'up': 1.0, 'down': .5, 'north': .8, 'south': .8, 'east': .6, 'west': .6}


def render(model, textures, scale=14, view=(1, .9, -1.15)):
    """An orthographic view of a model, painter-sorted; good enough to judge proportions and art."""
    c = [v / math.sqrt(sum(w * w for w in view)) for v in view]
    f = [-v for v in c]
    right = [f[1] * 0 - f[2] * 1, f[2] * 0 - f[0] * 0, f[0] * 1 - f[1] * 0]
    n = math.sqrt(sum(v * v for v in right)); right = [v / n for v in right]
    up = [right[1] * f[2] - right[2] * f[1], right[2] * f[0] - right[0] * f[2], right[0] * f[1] - right[1] * f[0]]
    size = 40 * scale
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    quads = []
    for e in model.elements:
        for face, spec in e['faces'].items():
            corners = [rotate(p, e.get('rotation')) for p in CORNERS[face](e['from'], e['to'])]
            normal = rotate(tuple(o + d for o, d in zip((0, 0, 0), NORMALS[face])), e.get('rotation') and {**e['rotation'], 'origin': [0, 0, 0]})
            facing = sum(a * b for a, b in zip(normal, c))
            if facing <= 1e-6 and not (e['from'][0] == e['to'][0] or e['from'][1] == e['to'][1] or e['from'][2] == e['to'][2]):
                continue
            depth = sum(sum(p[i] for p in corners) / 4 * c[i] for i in range(3))
            thin = min(abs(e['to'][i] - e['from'][i]) for i in range(3))
            if thin < .25 and e['from'] != e['to']:
                depth += 1.5  # decals and cards sit on top of the surface behind them
            quads.append((depth, face, corners, spec, e.get('light_emission', 0)))
    quads.sort(key=lambda q: q[0])

    def project(p):
        x, y, z = p[0] - 8, p[1] - 8, p[2] - 8
        sx = (x * right[0] + y * right[1] + z * right[2]) * scale + size / 2
        sy = -(x * up[0] + y * up[1] + z * up[2]) * scale + size * .58
        return sx, sy
    for depth, face, corners, spec, light in quads:
        tex = textures[model.textures[spec['texture'][1:]]]
        u1, v1, u2, v2 = spec['uv']
        rot = spec.get('rotation', 0) // 90
        tl, tr, br, bl = corners
        for _ in range(rot):
            tl, tr, br, bl = bl, tl, tr, br
        w, h = abs(u2 - u1), abs(v2 - v1)
        steps_u, steps_v = max(1, math.ceil(w)), max(1, math.ceil(h))
        for j in range(steps_v):
            for i in range(steps_u):
                a0, a1, b0, b1 = i / steps_u, (i + 1) / steps_u, j / steps_v, (j + 1) / steps_v
                u = u1 + (u2 - u1) * (a0 + a1) / 2; v = v1 + (v2 - v1) * (b0 + b1) / 2
                px = tex.getpixel((min(15, max(0, int(u))), min(15, max(0, int(v)))))
                if px[3] < 128:
                    continue
                k = 1 if light else SHADE[face]
                color = (int(px[0] * k), int(px[1] * k), int(px[2] * k), 255)
                def at(a, b):
                    top = [tl[t] + (tr[t] - tl[t]) * a for t in range(3)]
                    bottom = [bl[t] + (br[t] - bl[t]) * a for t in range(3)]
                    return project([top[t] + (bottom[t] - top[t]) * b for t in range(3)])
                draw.polygon([at(a0, b0), at(a1, b0), at(a1, b1), at(a0, b1)], fill=color)
    return image


def preview():
    textures = {f'{NS}:block/workstation/{k}': v for k, v in paint.textures().items()}
    textures.update(vanilla_textures())
    tiles = []
    for name, models in designs().items():
        for model in (models if name != 'easel_canvas' else [models[0], models[1], models[2], models[5], models[8]]):
            tiles.append((model.name, render(model, textures), render(model, textures, view=(-1, .9, 1.15))))
    cols = 4
    tile = 40 * 14
    sheet = Image.new('RGB', (cols * tile, ((len(tiles) + cols - 1) // cols) * (tile // 2 + 30)), '#7FA7C9')
    draw = ImageDraw.Draw(sheet)
    for n, (name, front, back) in enumerate(tiles):
        x, y = (n % cols) * tile, (n // cols) * (tile // 2 + 30)
        sheet.paste(front.resize((tile // 2, tile // 2)), (x, y + 24), front.resize((tile // 2, tile // 2)))
        sheet.paste(back.resize((tile // 2, tile // 2)), (x + tile // 2, y + 24), back.resize((tile // 2, tile // 2)))
        draw.text((x + 8, y + 6), name, fill='#10202E')
    dest = PROJECT / 'build/previews/workstations.png'
    dest.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest)
    for name, front, back in tiles:
        front.save(PROJECT / f'build/previews/workstation-{name}.png')
    print(dest)


if __name__ == '__main__':
    if '--check' in sys.argv: check()
    elif '--preview' in sys.argv: preview()
    elif '--boxes' in sys.argv: boxes()
    else: write()
