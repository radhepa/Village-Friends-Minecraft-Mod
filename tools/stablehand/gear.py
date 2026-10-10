"""Horse gear: the data table Java reads (stablehand/gear.json), the equipment layers and entity textures
vanilla's horse renderers draw, the item sprites, models and definitions, the recipes, the caparison dye recipe
and the cauldron tag.

Each row is one item. `kind` barding goes in the BODY slot (horse armor), `kind` tack in the SADDLE slot.
Barding: armor `defense`, `toughness`, `knockback` resistance, `enchantability` and the `repair` item tag;
`dyeable` cloth with its `undyed` colour (signed ARGB). Tack: `columns` of pack slots it gives (3 slots
each; the vanilla mount screen fits at most 5), `bond_ride` (how much faster riding grows the bond) and
`calm` (how much steadier the horse is near monsters). `animals` says which of horse, donkey and mule may
wear it.

The lance is vanilla's kinetic spear with its own numbers (Item.Properties.spear order, then the attack
reach): damage needs at least `damage_threshold` blocks per second of closing speed, so it lands only from
a galloping horse (a sprinting player makes about 5.6).

Art. Vanilla draws barding with the `horse_body` layer on the adult horse model (UV below, from
AbstractEquineModel.createBodyMesh) and tack with the saddle layers on EquineSaddleModel (the saddle box,
head straps, bit rings and reins; donkeys and mules add two chest boxes that this layer always draws, so the
pack saddle paints them as panniers). Every texture is painted here from scratch on that UV contract with
the stepped palettes below, light from the top, seeded noise (deterministic: --check compares bytes):
`--preview` writes build/previews/stablehand_gear*.png, the UV nets with every face outlined, a rough side
view of the horse wearing each piece, and the item sprites at 8x.

Never hand-edit an output; change the rows or the painters here and rerun tools/stablehand/stablehand.py.
"""
from PIL import Image, ImageDraw

from kit import ASSETS, DATA, NS, TABLES, dump, item_files, merge_tag, png_bytes, raster

CLOTH_RED = -6537410  # 0x9C3F3E with full alpha, as a signed int

GEAR = [
    # id, kind, slot, animals, defense, toughness, knockback, enchantability, repair, dyeable, undyed, columns, bond_ride, calm
    ('caparison', 'barding', 'body', ['horse'], 2, 0, 0, 15, 'minecraft:wool', True, CLOTH_RED, 0, 1.0, 0),
    ('leather_barding', 'barding', 'body', ['horse'], 4, 0, 0, 15, 'minecraft:repairs_leather_armor', False, 0, 0, 1.0, 0),
    ('mail_barding', 'barding', 'body', ['horse'], 6, 0, 0, 12, 'minecraft:repairs_chain_armor', False, 0, 0, 1.0, 0),
    ('plate_barding', 'barding', 'body', ['horse'], 10, 2, 0.1, 9, 'minecraft:repairs_iron_armor', False, 0, 0, 1.0, 0),
    ('saddlebags', 'tack', 'saddle', ['horse'], 0, 0, 0, 0, '', False, 0, 2, 1.0, 0),
    ('bridle', 'tack', 'saddle', ['horse', 'donkey', 'mule'], 0, 0, 0, 0, '', False, 0, 0, 1.5, 1),
    ('pack_saddle', 'tack', 'saddle', ['donkey', 'mule'], 0, 0, 0, 0, '', False, 0, 5, 1.0, 0),
]
FIELDS = ['id', 'kind', 'slot', 'animals', 'defense', 'toughness', 'knockback', 'enchantability', 'repair', 'dyeable',
          'undyed', 'columns', 'bond_ride', 'calm']
NAMES = {'caparison': 'Caparison', 'leather_barding': 'Leather Barding', 'mail_barding': 'Mail Barding',
         'plate_barding': 'Plate Barding', 'saddlebags': 'Saddlebags', 'bridle': 'Bridle', 'pack_saddle': 'Pack Saddle'}

LANCE = {'id': 'jousting_lance', 'name': 'Jousting Lance', 'material': 'iron', 'attack_duration': 1.25, 'damage_multiplier': 1.6,
         'delay': 0.75, 'dismount_time': 3.0, 'dismount_threshold': 9.0, 'knockback_time': 8.0, 'knockback_threshold': 7.0,
         'damage_time': 10.0, 'damage_threshold': 7.0, 'reach': [2.0, 5.0, 2.0, 7.0, 0.125, 0.5]}

SADDLE_LAYERS = {'horse': 'horse_saddle', 'donkey': 'donkey_saddle', 'mule': 'mule_saddle'}


def table():
    rows = []
    for row in GEAR:
        g = dict(zip(FIELDS, row))
        assert g['kind'] in ('barding', 'tack') and g['slot'] == ('body' if g['kind'] == 'barding' else 'saddle'), g['id']
        assert set(g['animals']) <= {'horse', 'donkey', 'mule'} and 0 <= g['columns'] <= 5, g['id']
        rows.append(g)
    return {'gear': rows, 'lance': {k: v for k, v in LANCE.items() if k != 'name'}}


# -- palettes: stepped tones, darkest first ----------------------------------------------------------------

def tones(*hexes):
    return [tuple(bytes.fromhex(h)) + (255,) for h in hexes]


CLOTH = tones('8A8A8A', 'A6A6A6', 'C0C0C0', 'D8D8D8', 'EEEEEE', 'FAFAFA')  # greyscale: the dye tints it
GOLD = tones('5C3F0E', '8E6418', 'BD8E2A', 'E0B647', 'F6DE85')
CREAM = tones('B9AC8A', 'D8CDAE', 'EFE7D0', 'FBF6E6')
LEATHER = tones('2E1A0F', '4B2B18', '693D22', '86532E', 'A26B3B', 'BE8650')
STITCH = tones('D9B987')[0]
BRASS = tones('5E4512', '94701F', 'C59E39', 'EBCB6A')
STEEL = tones('1E2228', '363C45', '545D69', '76818E', '9AA5B1', 'C1CAD3', 'E6ECF0')
MAIL = tones('262A30', '444B54', '67707B', '8F98A3', 'BCC4CC')
SADDLE = tones('26150C', '3E2214', '5A321C', '784627', '955C33', 'B07644')
TAN = tones('4A3018', '6F4A26', '936536', 'B48248', 'D2A262')
WOOD = tones('3F2715', '5E3D22', '7E552F', '9E6F3E', 'BE8C55')
ROPE = tones('5B4A2E', '826C45', 'A88F5F', 'CBB283', 'E6D3A8')
CANVAS = tones('6D6553', '8F8670', 'B0A68C', 'CFC6AA', 'E7DFC6')
WICKER = tones('4E3618', '71502A', '93703C', 'B39051', 'CFB06C')
WOOL = tones('4C1F1A', '73302A', '96433A', 'B4614F')  # the pack pad's madder-red stripes


# -- the UV contract ----------------------------------------------------------------------------------------
# A model box with texture offset (u, v) and size w x h x d unwraps into six faces. Local coordinates used by the
# painters: on the sides `a` counts from the FRONT of the animal (so one painter does both flanks, mirrored), on
# the top and bottom `a` runs across and `b` counts from the front, and `b` is always rows from the top on the
# four side faces. Verified against Minecraft's ModelPart.Cube: the top face's first texture row is the rear,
# the right side's first column is the rear, the left side's first column is the front.

def box(u, v, w, h, d):
    return {'top': (u + d, v, w, d), 'bottom': (u + d + w, v, w, d), 'right': (u, v + d, d, h),
            'front': (u + d, v + d, w, h), 'left': (u + d + w, v + d, d, h), 'back': (u + 2 * d + w, v + d, w, h)}


# Adult horse (horse_body layer).
BODY = box(0, 32, 10, 10, 22)
NECK = box(0, 35, 4, 12, 7)
HEAD = box(0, 13, 6, 5, 7)
MOUTH = box(0, 25, 4, 5, 5)
EARS = box(19, 16, 2, 3, 1)
LEGS = box(48, 21, 4, 11, 4)
MANE = box(56, 36, 2, 16, 2)
TAIL = box(42, 36, 3, 14, 4)
HORSE_PARTS = {'body': BODY, 'neck': NECK, 'head': HEAD, 'mouth': MOUTH, 'ears': EARS, 'legs': LEGS, 'mane': MANE, 'tail': TAIL}
# EquineSaddleModel (the saddle layers); the chest boxes exist only on donkeys and mules.
SADDLE_BOX = box(26, 0, 10, 9, 9)
HEAD_STRAPS = box(1, 1, 6, 5, 6)
NOSEBAND = box(19, 0, 4, 5, 2)
BIT = box(29, 5, 1, 2, 2)
REINS = {'right': (32, 18, 16, 3), 'left': (48, 18, 16, 3)}  # a flat 0 x 3 x 16 box: only its two sides exist
CHEST = box(26, 21, 8, 8, 3)
SADDLE_PARTS = {'saddle': SADDLE_BOX, 'head straps': HEAD_STRAPS, 'noseband': NOSEBAND, 'bit': BIT, 'chest': CHEST}


def put(img, rect, face, a, b, color):
    """One pixel in a face's local coordinates (see above); out of range or None is ignored."""
    x, y, w, h = rect
    if color is None or not (0 <= a < w and 0 <= b < h):
        return
    if face == 'right':
        px, py = x + w - 1 - a, y + b
    elif face in ('top', 'bottom'):
        px, py = x + a, y + h - 1 - b
    else:
        px, py = x + a, y + b
    img.putpixel((px, py), color)


def paint(img, part, faces, fn):
    """Paints `fn(face, a, b, w, h) -> colour or None` over the named faces of a part, in local coordinates."""
    for face in faces:
        rect = part[face]
        for b in range(rect[3]):
            for a in range(rect[2]):
                put(img, rect, face, a, b, fn(face, a, b, rect[2], rect[3]))


SIDES = ('right', 'left')
AROUND = ('right', 'front', 'left', 'back')
ALL = ('top', 'bottom') + AROUND


def noise(x, y, seed=0):
    """A deterministic 0..1 value per pixel (integer hash; no global random state)."""
    n = (x * 374761393 + y * 668265263 + seed * 2246822519) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535


def pick(palette, level):
    return palette[max(0, min(len(palette) - 1, level))]


def canvas():
    return Image.new('RGBA', (64, 64))


FACE = {'top': 11, 'bottom': 23, 'right': 37, 'front': 41, 'left': 53, 'back': 67}


def grain(palette, face, a, b, level, seed=0, rough=(.85, .12)):
    """A palette tone with seeded speckle: a step lighter above rough[0], a step darker below rough[1]."""
    n = noise(a, b, FACE.get(face, 0) + seed)
    return pick(palette, level + (1 if n > rough[0] else 0) - (1 if n < rough[1] else 0))


# -- barding (horse_body layer) -----------------------------------------------------------------------------

def caparison():
    """The dyeable cloth: greyscale, so the dye (or the undyed red) tints it. Hangs in vertical folds over the body,
    neck and upper legs, a hood over the head with eye holes and ear covers, the nose left bare, a dagged hem."""
    img = canvas()

    def cloth(face, a, b, level):
        return grain(CLOTH, face, a, b, level, 1, (.88, .07))

    def fold(a):
        return [1, 2, 4, 3, 3][a % 5]

    def body(face, a, b, w, h):
        if face == 'bottom':
            return None
        if face == 'top':
            return cloth(face, a, b, 3 if a in (0, w - 1) else 4)
        return cloth(face, a, b, fold(a + (2 if face in SIDES else 0)) + (1 if b == 0 else 0) - (1 if b >= h - 3 else 0))
    paint(img, BODY, ALL, body)

    def neck(face, a, b, w, h):
        if face in ('top', 'bottom'):
            return None
        return cloth(face, a, b, (fold(a + b // 5) if face in SIDES else 3) - (1 if b >= h - 2 else 0))
    paint(img, NECK, ALL, neck)

    def head(face, a, b, w, h):
        if face == 'front':
            return None
        if face in SIDES and a in (2, 3) and b == 1:
            return None  # eye holes
        return cloth(face, a, b, {'top': 4, 'bottom': 2}.get(face, 3))
    paint(img, HEAD, ALL, head)
    paint(img, EARS, ALL, lambda face, a, b, w, h: cloth(face, a, b, 4 if face == 'top' else 3))

    def mouth(face, a, b, w, h):
        if face == 'top':
            return cloth(face, a, b, 4) if b >= 2 else None
        if face in SIDES:
            return cloth(face, a, b, 3) if a >= 2 and b <= 3 else None
        return None
    paint(img, MOUTH, ALL, mouth)

    def skirt(face, a, b, w, h):
        if b < 3:
            return cloth(face, a, b, fold(a) - (1 if b == 2 else 0))
        return cloth(face, a, b, 2) if b == 3 and a % 2 == 0 else None
    paint(img, LEGS, AROUND, skirt)
    return img


def caparison_overlay():
    """What the dye leaves alone: gold braid on the hems, the hood's edges and eye rims, and a pale cross on each shoulder."""
    img = canvas()

    def braid(a):
        return GOLD[3] if a % 2 == 0 else GOLD[2]

    def cross(a, b):
        vertical, across = a in (3, 4) and 1 <= b <= 8, 1 <= a <= 6 and b in (3, 4)
        if not (vertical or across):
            return None
        if b == 1 or (b == 3 and not vertical):
            return CREAM[3]
        if b == 8 or (b == 4 and not vertical) or (a == 4 and b > 4):
            return CREAM[1]
        return CREAM[2]

    def body(face, a, b, w, h):
        if face in ('top', 'bottom'):
            return None
        if b == h - 1:
            return braid(a)
        return cross(a, b) if face in SIDES else None
    paint(img, BODY, ALL, body)
    paint(img, NECK, SIDES, lambda face, a, b, w, h: braid(b) if a == w - 1 else None)
    rims = {(1, 1), (4, 1), (2, 0), (3, 0), (2, 2), (3, 2)}
    paint(img, HEAD, SIDES, lambda face, a, b, w, h: GOLD[3] if (a, b) in rims else None)

    def mouth(face, a, b, w, h):
        if face == 'top':
            return braid(a) if b == 2 else None
        return GOLD[2] if face in SIDES and a == 2 and b <= 3 else None
    paint(img, MOUTH, ('top',) + SIDES, mouth)
    paint(img, LEGS, AROUND, lambda face, a, b, w, h: braid(a) if b == 2 else None)
    return img


def leather_barding():
    """Boiled leather: stitched flank panels, a breastplate strap with a brass buckle, a crupper, lamed crinet
    on the neck and a chanfron with a brass boss. Ears, legs and nose stay bare."""
    img = canvas()

    def hide(face, a, b, level):
        return grain(LEATHER, face, a, b, level, 2)

    def body(face, a, b, w, h):
        if face == 'bottom':
            return pick(LEATHER, 2 if b == 9 else 1) if b in (9, 10) else None  # the girth strap
        if face == 'top':
            if a in (0, w - 1):
                return LEATHER[2]
            return STITCH if a in (1, w - 2) and b % 2 == 0 else hide(face, a, b, 4)
        if b == h - 1:
            return LEATHER[1]
        if b in (1, h - 3) and a % 2 == 0:
            return STITCH
        if face in SIDES and a in (7, 15):
            return LEATHER[1]
        if face == 'front' and b in (3, 4):
            return BRASS[3 if b == 3 else 1] if a in (4, 5) else LEATHER[2 if b == 3 else 1]
        if face == 'back' and b == 2 and a in (2, 7):
            return BRASS[3]
        return hide(face, a, b, 4 if b == 0 else 3 if b < 6 else 2)
    paint(img, BODY, ALL, body)

    def neck(face, a, b, w, h):
        if face in ('top', 'bottom'):
            return None
        k = b % 3
        if face == 'front':
            return LEATHER[1] if k == 2 else hide(face, a, b, 2)
        if k == 1 and a == 1:
            return STITCH
        return LEATHER[4] if k == 0 else LEATHER[1] if k == 2 else hide(face, a, b, 3)
    paint(img, NECK, ALL, neck)

    def head(face, a, b, w, h):
        if face == 'top':
            if (a, b) == (2, 3):
                return BRASS[3]
            if (a, b) == (3, 3):
                return BRASS[2]
            if a in (2, 3) and b in (2, 4):
                return BRASS[1]
            return LEATHER[1] if a in (0, w - 1) or b in (0, h - 1) else hide(face, a, b, 4)
        if face in SIDES:
            if b == 0:
                return LEATHER[2]
            return LEATHER[1] if a == 5 and b <= 3 else None
        return None
    paint(img, HEAD, ('top',) + SIDES, head)

    def mouth(face, a, b, w, h):
        if face == 'top':
            return None if b == 0 else LEATHER[1] if a in (0, w - 1) else hide(face, a, b, 4)
        return LEATHER[2] if a >= 3 and b == 0 else None
    paint(img, MOUTH, ('top',) + SIDES, mouth)
    return img


def mail(face, a, b, light, seed=3):
    """Riveted rings: a staggered 2 x 2 motif (bright ring top, mid sides, dark gap) on a top-lit ramp."""
    ta, tb = (a + (b // 2) % 2) % 2, b % 2
    level = {(0, 0): light + 1, (1, 0): light, (0, 1): light, (1, 1): light - 2}[(ta, tb)]
    return grain(MAIL, face, a, b, level, seed, (.9, .05))


def mail_barding():
    """A mail trapper over body, neck and upper legs with leather edging, and a mail hood with eye holes."""
    img = canvas()

    def body(face, a, b, w, h):
        if face == 'bottom':
            return pick(LEATHER, 2 if b == 9 else 1) if b in (9, 10) else None
        if face == 'top':
            return LEATHER[2] if a in (0, w - 1) else mail(face, a, b, 3)
        if b == h - 1:
            return LEATHER[2] if a % 3 else LEATHER[1]
        return mail(face, a, b, 3 if b < 4 else 2)
    paint(img, BODY, ALL, body)
    paint(img, NECK, AROUND, lambda face, a, b, w, h: mail(face, a, b, 3 if b < 6 else 2))

    def head(face, a, b, w, h):
        if face == 'front' or (face in SIDES and (b > 3 or (a in (2, 3) and b == 1))):
            return None
        return mail(face, a, b, 3)
    paint(img, HEAD, ALL, head)

    def mouth(face, a, b, w, h):
        if face == 'top':
            return mail(face, a, b, 3) if b >= 2 else None
        return mail(face, a, b, 2) if face in SIDES and a >= 2 and b <= 3 else None
    paint(img, MOUTH, ('top',) + SIDES, mouth)
    paint(img, LEGS, AROUND, lambda face, a, b, w, h: mail(face, a, b, 2) if b < 3 else LEATHER[2] if b == 3 else None)
    return img


def steel(a, b, w, h, ridge=None, rivets=()):
    """One steel plate in local coordinates: lit top edge, darker bottom rim, bevelled sides, an optional
    raised ridge down column `ridge` (lit) and `ridge + 1` (shaded), and rivet heads."""
    if (a, b) in rivets:
        return STEEL[6]
    level = 5 if b == 0 else 1 if b == h - 1 else 4 - (b * 3) // h
    if a == 0 or a == w - 1:
        level -= 1
    if ridge is not None and a == ridge:
        level += 1
    if ridge is not None and a == ridge + 1:
        level -= 1
    if (a + b) % 7 == 2 and 0 < b < h - 1:
        level += 1  # a glint across the plate
    return pick(STEEL, level)


def plate_barding():
    """Full plate: chanfron with a ridge and rivets, a lamed criniere down the neck, peytral, flanchards and
    crupper over the body with the saddle's place left in leather, and a mail fringe on the upper legs."""
    img = canvas()

    def body(face, a, b, w, h):
        if face == 'bottom':
            return pick(LEATHER, 2 if b == 9 else 1) if b in (9, 10) else None
        if face == 'top':
            if 7 <= b <= 15:
                return grain(LEATHER, face, a, b, 3, 4)  # under the saddle
            lb, lh = (6 - b, 7) if b < 7 else (b - 16, 6)
            return steel(a, lb, w, lh, ridge=4)
        if face in SIDES:
            start, size = (0, 8) if a < 8 else (8, 7) if a < 15 else (15, 7)
            corners = {(1, 1), (size - 2, 1), (1, h - 2), (size - 2, h - 2)}
            return steel(a - start, b, size, h, rivets=corners)
        if face == 'front':
            boss = {(4, 4): STEEL[6], (5, 4): STEEL[5], (4, 5): STEEL[4], (5, 5): STEEL[2]}
            if (a, b) in boss:
                return boss[(a, b)]
        return steel(a, b, w, h, ridge=4, rivets={(1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)})
    paint(img, BODY, ALL, body)

    def lames(a, b, w):
        k = b % 3
        if k == 1 and a in (1, w - 2):
            return STEEL[6]
        return pick(STEEL, (5 if k == 0 else 3 if k == 1 else 1) - (1 if a in (0, w - 1) and k != 2 else 0))

    def neck(face, a, b, w, h):
        if face in ('top', 'bottom'):
            return None
        return mail(face, a, b, 2) if face == 'front' else lames(a, b, w)
    paint(img, NECK, ALL, neck)

    def head(face, a, b, w, h):
        if face == 'top':
            if a in (2, 3) and b == 3:
                return STEEL[6] if a == 2 else STEEL[4]
            return steel(a, h - 1 - b, w, h, ridge=2, rivets={(1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)})
        if face in SIDES:
            if b == 1 and a in (2, 3):
                return None  # the eye
            if b == 1 and a in (1, 4):
                return STEEL[1]
            return steel(a, b, w, 3) if b <= 1 or (b == 2 and a >= 4) else None
        return steel(a, b, w, h) if face == 'back' else None
    paint(img, HEAD, ALL, head)

    def mouth(face, a, b, w, h):
        if face == 'top':
            return STEEL[2] if b == 0 else steel(a, h - 1 - b, w, h, ridge=1)
        return steel(a, b, w, 2) if face in SIDES and a >= 2 and b <= 1 else None
    paint(img, MOUTH, ('top',) + SIDES, mouth)
    paint(img, LEGS, AROUND, lambda face, a, b, w, h: mail(face, a, b, 2) if b < 2 else LEATHER[2] if b == 2 else None)
    return img


# -- tack (the saddle layers) -------------------------------------------------------------------------------

def headgear(img, strap, ring, stud):
    """Head straps on EquineSaddleModel: crownpiece, browband with a stud, cheekpieces and throatlatch on the head
    box, a noseband round the muzzle, the bit rings, and the reins (drawn only while ridden). `strap` is a tone
    ramp (leather or rope), `ring` the bit's ramp, `stud` the browband's."""
    def straps(face, a, b, w, h):
        if face == 'top':
            if b == h - 1:
                return strap[3] if a % 2 == 0 else strap[2]  # crownpiece, just in front of the ears
            if b == 3:
                return stud[3] if a == 2 else stud[2] if a == 3 else strap[2]  # browband
            return None
        if face == 'bottom':
            return strap[1] if b == h - 1 else None  # throatlatch
        if face in SIDES:
            if a == w - 1:
                return strap[2] if b % 2 == 0 else strap[1]  # cheekpiece
            if b == 0 and a >= 3:
                return stud[2] if a == 4 else strap[2]
        return None
    paint(img, HEAD_STRAPS, ALL, straps)

    def noseband(face, a, b, w, h):
        if face in ('top', 'bottom'):
            return strap[3 if face == 'top' else 1] if b == 0 else None
        if face in SIDES:
            return strap[2] if a == 0 else strap[1] if b >= 3 else None
        return None
    paint(img, NOSEBAND, ALL, noseband)
    paint(img, BIT, ALL, lambda face, a, b, w, h: ring[4] if face == 'top' else ring[2] if face == 'bottom' else ring[3 if b == 0 else 2])
    sag = [0, 0, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 0, 0]
    for face, (x, y, w, h) in REINS.items():
        for a in range(16):
            px = x + (w - 1 - a if face == 'right' else a)
            img.putpixel((px, y + sag[a]), strap[3] if a % 4 == 1 else strap[2])


def bridle():
    """Only the head straps and reins, in dark bridle leather with a steel bit: the seat stays bare (ride bareback)."""
    img = canvas()
    headgear(img, SADDLE, STEEL[1:], BRASS)
    return img


def saddlebags():
    """A riding saddle (pommel, seat with a seam, rolled cantle, flaps with stirrups) with a tan leather bag
    buckled behind each flap, plus the bridle."""
    img = canvas()

    def saddle(face, a, b, w, h):
        if face == 'top':
            edge = a in (0, w - 1)
            if b == 0 or b == h - 1:
                return SADDLE[1 if edge else 2]
            if b == 1:
                return SADDLE[2 if edge else 4]
            if b == h - 2:
                return SADDLE[3 if edge else 5]  # the cantle's lit roll
            if edge:
                return SADDLE[2]
            return SADDLE[3] if a in (4, 5) and b % 2 else grain(SADDLE, face, a, b, 4, 5)
        if face in SIDES:
            if a <= 4 and b <= 4:  # the flap
                if a == 0 or b == 4:
                    return SADDLE[1]
                if b == 1 and a % 2:
                    return TAN[4]  # stitches
                return SADDLE[4] if b == 0 else grain(SADDLE, face, a, b, 3, 6)
            if a == 2 and b in (5, 6):
                return SADDLE[1]  # stirrup leather
            if (a, b) in ((1, 7), (3, 7)):
                return STEEL[4]
            if b == 8 and 1 <= a <= 3:
                return STEEL[3 if a == 2 else 2]
            if a == 6 and b <= 1:
                return SADDLE[1]  # the bag's strap up to the cantle
            if 5 <= a <= 8 and 2 <= b <= 8:
                return bag(a - 5, b - 2, face)
            return SADDLE[2] if b == 0 else None
        if face in ('front', 'back'):
            return SADDLE[2] if b == 0 else None
        return None

    def bag(a, b, face):
        if b == 0:
            return TAN[4]
        if b == 1:
            return BRASS[3] if a == 1 else BRASS[2] if a == 2 else TAN[3]
        if b == 2:
            return TAN[1]  # the flap's shadow
        if b == 6 or a == 3:
            return TAN[1]
        return TAN[2] if a == 0 else grain(TAN, face, a, b, 3, 7)
    paint(img, SADDLE_BOX, ALL, saddle)
    headgear(img, SADDLE, STEEL[1:], BRASS)
    return img


def pack_saddle():
    """A wooden sawbuck on a striped wool pad with a rolled canvas bundle lashed on top, a rope cinch, wicker
    panniers on both flanks (the donkey and mule saddle layers always draw their chest boxes, so these show
    whether or not the animal has a chest), and a rope halter with a lead."""
    img = canvas()

    def frame(face, a, b, w, h):
        if face == 'top':
            if a in (0, w - 1):
                return WOOL[2] if b % 2 else WOOL[3]
            if b in (0, h - 1):
                return WOOD[3] if 1 <= a <= w - 2 else WOOD[1]
            if a in (1, w - 2):
                return WOOD[4] if b in (1, h - 2) else WOOD[2]
            if b in (2, h - 3):
                return ROPE[3] if a % 2 else ROPE[2]
            return CANVAS[[1, 3, 4, 3, 2, 1][a - 2]]  # the roll, lit across its top
        if face in SIDES:
            if b <= 2 and a in (0, 1, w - 2, w - 1):
                return WOOD[3] if b == 0 else WOOD[2] if (a + b) % 2 else WOOD[1]  # the bucks' legs
            if b <= 5:
                if (a + b) % 5 == 0:
                    return ROPE[3]  # lashing
                return WOOL[3] if b <= 1 else CANVAS[3] if b <= 3 else WOOL[1 if b == 5 else 2]
            if a == 4:
                return ROPE[2] if b % 2 else ROPE[3]  # the cinch
            return None
        if face in ('front', 'back'):
            return WOOD[2] if b == 0 else None
        return None
    paint(img, SADDLE_BOX, ALL, frame)

    def pannier(face, a, b, w, h):
        if face == 'top':
            return ROPE[2] if a in (2, 5) else CANVAS[2] if b in (0, h - 1) else CANVAS[4]
        if face in ('back', 'bottom'):
            return WICKER[1]
        if b == 0:
            return WICKER[4]
        if b == h - 1 or a in (0, w - 1):
            return WICKER[1]
        if face == 'front' and a in (3, 4) and b <= 2:
            return LEATHER[2] if b < 2 else BRASS[2]  # the strap up to the frame
        return WICKER[3] if (a + (b % 2) * 2) % 4 < 2 else WICKER[2]
    paint(img, CHEST, ALL, pannier)
    headgear(img, ROPE, STEEL[1:], [ROPE[0], ROPE[1], ROPE[3], ROPE[4]])
    return img


# -- item sprites (16 px, house style: dark outline, stepped palettes, light from the top left) -------------------

SADDLEBAGS = """
................
................
.oo..........oo.
oHho........oHmo
ohmho......oHhmo
.ohhHooooooHhmo.
.ohhhHHHHHHhmdo.
..oommmmmmmmdo..
.ooooodmmmmdo...
oBBBBodmmmdo....
oBbKbooddddo....
occccoo.oso.....
obbbbo..oso.....
obbbco.osSso....
.oooo..os.so....
.......ooooo....
"""
SADDLE_ITEM = {'o': '26150C', 'H': 'B07644', 'h': '955C33', 'm': '784627', 'd': '5A321C',
               'B': 'D2A262', 'b': 'B48248', 'c': '936536', 'K': 'EBCB6A', 's': '9AA5B1', 'S': 'E6ECF0'}
BRIDLE = """
................
.....oooo.......
....ohhhmo......
...oho..odo.....
..okKo...oKko...
..oho.....odo...
..oho.....odo...
..oho.....odo...
..ohho...oddo...
...ohhoooddo....
..ooohhmddooo...
.oSSo.ooo.oSSo..
.oS.so...oS.so..
..oso.....osoo..
...........ohho.
............ooo.
"""
BRIDLE_ITEM = {'o': '26150C', 'h': '955C33', 'm': '784627', 'd': '5A321C', 'k': 'C59E39', 'K': 'EBCB6A',
               's': '76818E', 'S': 'C1CAD3'}
PACK_SADDLE = """
................
.......oo.......
......oWWo......
.....oWwwWo.....
....oWwoowWo....
...oRRRRRRRRo...
..oRVVVVVVVVRo..
.oRrrrrrrrrrrRo.
oLLLLLo..oLLLLLo
obBbBbo..obBbBbo
oBbBbBo..oBbBbBo
obBbBbo..obBbBbo
oBbBbBo..oBbBbBo
occccco..occccco
.ooooo....ooooo.
................
"""
PACK_ITEM = {'o': '2E1D10', 'W': 'BE8C55', 'w': '7E552F', 'R': 'B4614F', 'r': '73302A', 'V': 'E7DFC6',
             'L': 'CFB06C', 'B': 'B39051', 'b': '93703C', 'c': '71502A'}

# The barding family shares one silhouette: a horse's head and neck facing left, eye 'e', nostril 'n'.
HEAD_MASK = """
.........o.o....
........oxoxo...
.......oxxxxxo..
......oxxxxxxxo.
.....oxexxxxxxo.
....oxxxxxxxxxxo
...oxxxxxxxxxxxo
..oxxxxxxxxxxxxo
.oxxxxxxxxxxxxxo
onxxxxooxxxxxxxo
oxxxxo..oxxxxxxo
.oooo...oxxxxxxo
........oxxxxxxo
.......oxxxxxxxo
.......oxxxxxxxo
.......ooooooooo
"""
DARK = tones('17120F')[0]
COAT = tones('5C3A22', '7A4E2E')


def bevelled(mask, fill):
    """A sprite from a mask ('o' outline, 'x' inside, other letters marks) with each inside pixel's light from the
    top left: `fill(ch, x, y, edge)` gets edge > 0 on lit edges, < 0 on shaded ones, 0 inside."""
    rows = mask.strip('\n').splitlines()
    image = Image.new('RGBA', (16, 16))

    def empty(x, y):
        return not (0 <= y < len(rows) and 0 <= x < len(rows[y])) or rows[y][x] in '.o'
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch == '.':
                continue
            edge = 0 if ch == 'o' else int(empty(x, y - 1)) + int(empty(x - 1, y)) - int(empty(x, y + 1)) - int(empty(x + 1, y))
            color = fill(ch, x, y, edge)
            if color:
                image.putpixel((x, y), color)
    return image


def neck(x, y):
    return y >= 9 and x >= 8


def chanfron(x, y):
    """The band down the front of the face, from the forehead to the nose."""
    return not neck(x, y) and 10 <= x + y <= 12


def caparison_sprite(overlay=False):
    """The hooded cloth (greyscale, tinted by the item's dye), or its untinted layer: gold trim, the eye rim,
    a pale cross on the neck and the bare nose below the hood."""
    def fill(ch, x, y, edge):
        nose = x <= 2 and y >= 8
        if overlay:
            if ch == 'n':
                return DARK
            if nose and ch == 'x':
                return COAT[1 if edge > 0 else 0]
            if (x, y) in ((6, 4), (8, 4), (7, 3), (7, 5)) or (ch == 'x' and x + y == 11 and x == 3):
                return GOLD[3]
            if ch == 'x' and (y == 14 or (x == 3 and y >= 8) or (x + y == 11 and 3 <= x <= 4)):
                return GOLD[3] if (x + y) % 2 else GOLD[2]
            if (x == 11 and 10 <= y <= 13) or (y == 11 and 10 <= x <= 12):
                return CREAM[3] if y <= 11 else CREAM[1]
            return None
        if ch in 'en' or nose:
            return DARK if ch == 'e' else None
        if ch == 'o':
            return CLOTH[0]
        return pick(CLOTH, 3 + edge + (-1 if neck(x, y) and (x + y // 3) % 4 == 0 else 0))
    return bevelled(HEAD_MASK, fill)


def barding_sprite(kind):
    """The leather, mail or plate barding icon on the shared head silhouette."""
    def fill(ch, x, y, edge):
        if ch in 'en':
            return DARK
        if kind == 'leather':
            if ch == 'o':
                return LEATHER[0]
            if (x, y) == (9, 3):
                return BRASS[3]
            if (x + y == 13 and not neck(x, y) and x % 2) or (neck(x, y) and y in (11, 13) and x % 2):
                return STITCH
            return pick(LEATHER, 3 + edge - (1 if neck(x, y) and y in (10, 12) else 0))
        if kind == 'mail':
            if ch == 'o':
                return MAIL[0]
            if y == 14 or (chanfron(x, y) and x + y == 10):
                return LEATHER[2]
            return mail('icon', x, y, 2 + max(0, edge))
        if ch == 'o':
            return STEEL[0]
        if (x, y) in ((6, 5), (4, 7), (9, 2)):
            return STEEL[6]
        if neck(x, y):
            return pick(STEEL, (5 if y % 2 else 2) + (1 if edge > 0 else 0))
        if chanfron(x, y):
            return pick(STEEL, 4 + (1 if x + y == 11 else 0) + max(0, edge))
        return mail('icon', x, y, 2)
    return bevelled(HEAD_MASK, fill)


# The lance: an ash shaft with a steel tip, a red-and-white pennon below the tip, a steel vamplate (the round
# hand guard) and a leather grip. The icon points up and right like vanilla's spears; the held texture is
# 32 px (the size of vanilla's iron_spear_in_hand) and points up and left, as vanilla's held spears do.
LANCE_PALETTE = {'o': '2A1E14', 's': '76818E', 'S': 'C1CAD3', 'Z': 'E6ECF0', 'W': 'E3CFA0', 'w': 'BFA474', 'v': '8C7350',
                 'R': 'C43A2E', 'r': '8E2620', 'P': 'F2EBDD', 'V': '9AA5B1', 'g': '693D22', 'G': '955C33'}
LANCE_ICON = """
..............oo
.............oZo
............oSZo
...........oSso.
..........oWso..
...ooo...oWwo...
..oPRPo.oWwo....
...oRPRoWwo.....
....orRWwo......
.....oWwo.......
...ooWwo........
..oVSVo.........
.oVSVVo.........
.oVVsoo.........
.ogGo...........
.oo.............
"""


def lance_in_hand():
    """The held lance, 32 px, tip at the top left. Along the diagonal (s = x + y, 0 at the tip): a leaf-shaped
    steel point, the ash shaft three pixels thick (lit on its upper side), a two-tailed pennon, the vamplate
    flaring towards the tip, a leather-wrapped grip and a steel butt cap."""
    p = {k: tuple(bytes.fromhex(v)) + (255,) for k, v in LANCE_PALETTE.items()}
    img = Image.new('RGBA', (32, 32))
    tip = [0, 0, 1, 1, 1, 2, 2, 2, 2, 1, 1, 1, 1]
    for y in range(32):
        for x in range(32):
            s, d = x + y, x - y
            color = None
            if s < len(tip) and abs(d) <= tip[s]:
                color = p['Z'] if d > 0 or (d == 0 and s < 8) else p['S'] if d == 0 else p['s']
            elif 13 <= s <= 39 and abs(d) <= 1:
                color = p['W'] if d > 0 else p['w'] if d == 0 else p['v']
                if d == 0 and s % 9 == 4:
                    color = p['v']  # grain
            elif 16 <= s <= 26 and -2 - min(s - 15, 27 - s, 4) <= d <= -2 and not (s == 21 and d <= -5):
                color = p['P'] if s <= 18 or s >= 24 else p['R'] if d > -4 else p['r']
            elif 40 <= s <= 45 and abs(d) <= (4 if s <= 41 else 3 if s <= 43 else 2):
                color = p['Z'] if s == 40 else p['S'] if d > 0 else p['V'] if d == 0 else p['s']
            elif 46 <= s <= 56 and abs(d) <= 1:
                color = p['G'] if (s // 2) % 2 else p['g']
            elif 57 <= s <= 62 and abs(d) <= (1 if s <= 60 else 0):
                color = p['S'] if d > 0 else p['V'] if d == 0 else p['s']
            if color:
                img.putpixel((x, y), color)
    return img


# -- files -----------------------------------------------------------------------------------------------------

def equipment(g):
    """The equipment asset: barding draws on horse_body (caparison: the dyed cloth, then its untinted trim);
    tack on the saddle layer of every animal that may wear it."""
    own = f'{NS}:{g["id"]}'
    if g['kind'] == 'barding':
        layer = {'texture': own}
        if g['dyeable']:
            layer['dyeable'] = {'color_when_undyed': g['undyed']}
        layers = [layer] + ([{'texture': own + '_overlay'}] if g['dyeable'] else [])
        return {'layers': {'horse_body': layers}}
    return {'layers': {SADDLE_LAYERS[a]: [{'texture': own}] for a in g['animals']}}


ENTITY_ART = {'caparison': caparison, 'leather_barding': leather_barding, 'mail_barding': mail_barding,
              'plate_barding': plate_barding, 'saddlebags': saddlebags, 'bridle': bridle, 'pack_saddle': pack_saddle}
ITEM_ART = {'saddlebags': lambda: raster(SADDLEBAGS, SADDLE_ITEM), 'bridle': lambda: raster(BRIDLE, BRIDLE_ITEM),
            'pack_saddle': lambda: raster(PACK_SADDLE, PACK_ITEM), 'leather_barding': lambda: barding_sprite('leather'),
            'mail_barding': lambda: barding_sprite('mail'), 'plate_barding': lambda: barding_sprite('plate')}

# Shaped recipes (category equipment). Vanilla ids are checked against 26.3 by stablehand.py --check.
RECIPES = {
    'bridle': ([' L ', 'LNL', ' S '], {'L': 'minecraft:leather', 'N': 'minecraft:iron_nugget', 'S': 'minecraft:string'}),
    'saddlebags': (['LSL', 'B B'], {'L': 'minecraft:leather', 'S': 'minecraft:saddle', 'B': '#minecraft:bundles'}),
    'pack_saddle': (['SLS', 'BLB'], {'S': 'minecraft:stick', 'L': 'minecraft:leather', 'B': 'minecraft:barrel'}),
    'caparison': (['W W', 'WSW', 'W W'], {'W': '#minecraft:wool', 'S': 'minecraft:string'}),
    'leather_barding': (['LSL', 'LLL', 'LSL'], {'L': 'minecraft:leather', 'S': 'minecraft:string'}),
    'mail_barding': (['C C', 'III', 'C C'], {'C': 'minecraft:iron_chain', 'I': 'minecraft:iron_ingot'}),
    'plate_barding': (['IBI', 'ILI', 'I I'], {'I': 'minecraft:iron_ingot', 'B': 'minecraft:iron_block', 'L': f'{NS}:leather_barding'}),
    'jousting_lance': (['  I', ' S ', 'SL '], {'I': 'minecraft:iron_ingot', 'S': 'minecraft:stick', 'L': 'minecraft:leather'}),
}


def recipe(name):
    pattern, key = RECIPES[name]
    return dump({'type': 'minecraft:crafting_shaped', 'category': 'equipment', 'result': {'id': f'{NS}:{name}', 'count': 1},
                 'pattern': pattern, 'key': key})


def item_model(name, layers):
    return dump({'parent': 'minecraft:item/generated', 'textures': {f'layer{i}': f'{NS}:item/{t}' for i, t in enumerate(layers)}})


def outputs():
    files = {TABLES / 'gear.json': dump(table())}
    rows = table()['gear']
    for g in rows:
        files[ASSETS / f'equipment/{g["id"]}.json'] = dump(equipment(g))
        art = png_bytes(ENTITY_ART[g['id']]())
        layers = ['horse_body'] if g['kind'] == 'barding' else [SADDLE_LAYERS[a] for a in g['animals']]
        for layer in layers:
            files[ASSETS / f'textures/entity/equipment/{layer}/{g["id"]}.png'] = art
        files[DATA / f'{NS}/recipe/{g["id"]}.json'] = recipe(g['id'])
        if g['id'] in ITEM_ART:
            files.update(item_files(g['id'], ITEM_ART[g['id']]()))
    files[ASSETS / 'textures/entity/equipment/horse_body/caparison_overlay.png'] = png_bytes(caparison_overlay())
    # The caparison item: a white cloth layer tinted by its dye (red when undyed) under an untinted trim layer.
    files[ASSETS / 'textures/item/caparison.png'] = png_bytes(caparison_sprite())
    files[ASSETS / 'textures/item/caparison_overlay.png'] = png_bytes(caparison_sprite(overlay=True))
    files[ASSETS / 'models/item/caparison.json'] = item_model('caparison', ['caparison', 'caparison_overlay'])
    files[ASSETS / 'items/caparison.json'] = dump({'model': {'type': 'minecraft:model', 'model': f'{NS}:item/caparison',
                                                             'tints': [{'type': 'minecraft:dye', 'default': CLOTH_RED}]}})
    files[DATA / f'{NS}/recipe/caparison_dyed.json'] = dump({'type': 'minecraft:crafting_dye', 'dye': '#minecraft:dyes', 'group': 'dyed_armor',
                                                             'result': {'id': f'{NS}:caparison'}, 'target': f'{NS}:caparison'})
    files[DATA / 'minecraft/tags/item/cauldron_can_remove_dye.json'] = merge_tag(DATA / 'minecraft/tags/item/cauldron_can_remove_dye.json',
                                                                                [f'{NS}:caparison'])
    # The lance: flat in the inventory, on the ground and in frames; held, the long 32 px texture on vanilla's spear model.
    lance = LANCE['id']
    files[ASSETS / f'textures/item/{lance}.png'] = png_bytes(raster(LANCE_ICON, LANCE_PALETTE))
    files[ASSETS / f'textures/item/{lance}_in_hand.png'] = png_bytes(lance_in_hand())
    files[ASSETS / f'models/item/{lance}.json'] = item_model(lance, [lance])
    files[ASSETS / f'models/item/{lance}_in_hand.json'] = dump({'parent': 'minecraft:item/spear_in_hand',
                                                                'textures': {'layer0': f'{NS}:item/{lance}_in_hand'}})
    files[ASSETS / f'items/{lance}.json'] = dump({'model': {
        'type': 'minecraft:select', 'property': 'minecraft:display_context',
        'cases': [{'when': ['gui', 'ground', 'fixed', 'on_shelf'], 'model': {'type': 'minecraft:model', 'model': f'{NS}:item/{lance}'}}],
        'fallback': {'type': 'minecraft:model', 'model': f'{NS}:item/{lance}_in_hand'}}, 'swap_animation_scale': 1.95})
    files[DATA / f'{NS}/recipe/{lance}.json'] = recipe(lance)
    return files


# -- preview (build/previews; reads vanilla textures from the client jar for comparison, never copies them) -------

def vanilla(path):
    import io
    import zipfile
    from stablehand import CLIENT_JAR
    try:
        with zipfile.ZipFile(CLIENT_JAR) as jar:
            return Image.open(io.BytesIO(jar.read('assets/minecraft/textures/' + path))).convert('RGBA')
    except (OSError, KeyError):
        return Image.new('RGBA', (64, 64), (200, 0, 200, 255))


def tinted(img, argb):
    r, g, b = (argb >> 16) & 255, (argb >> 8) & 255, argb & 255
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            pr, pg, pb, pa = px[x, y]
            px[x, y] = (pr * r // 255, pg * g // 255, pb * b // 255, pa)
    return out


def over(*layers):
    out = Image.new('RGBA', layers[0].size)
    for layer in layers:
        out = Image.alpha_composite(out, layer)
    return out


def uv_net(img, parts, scale=6):
    """The texture at `scale` x on a checker, every face of `parts` outlined and labelled."""
    size = img.width * scale
    sheet = Image.new('RGBA', (size, size))
    draw = ImageDraw.Draw(sheet)
    for y in range(0, size, scale * 4):
        for x in range(0, size, scale * 4):
            draw.rectangle((x, y, x + scale * 4 - 1, y + scale * 4 - 1), fill=(70, 74, 80, 255) if (x + y) // (scale * 4) % 2 else (88, 92, 98, 255))
    sheet = Image.alpha_composite(sheet, img.resize((size, size), Image.NEAREST))
    draw = ImageDraw.Draw(sheet)
    for name, part in parts.items():
        for face, (x, y, w, h) in part.items():
            if w and h:
                draw.rectangle((x * scale, y * scale, (x + w) * scale - 1, (y + h) * scale - 1), outline=(255, 230, 0, 255))
        x, y, _, _ = part['top']
        draw.text((x * scale + 2, y * scale + 1), name, fill=(255, 255, 255, 255))
    return sheet


# Right-side elevation, front to the right, in model pixels (necks drawn upright: a placement check, not a render).
HORSE_SIDE = [(LEGS, 2, 13), (LEGS, 20, 13), (BODY, 2, 3), (NECK, 19, -2), (MANE, 17, -7), (HEAD, 19, -7), (MOUTH, 26, -7), (EARS, 19, -9)]
TACK_SIDE = [(SADDLE_BOX, 7, 3), (HEAD_STRAPS, 20, -7), (NOSEBAND, 26, -7), (BIT, 28, -5)]


def side_view(coat, body_layers=(), tack=None, panniers=False, scale=6):
    sheet = Image.new('RGBA', (36 * scale, 30 * scale), (120, 150, 110, 255))
    def face(tex, part, x, y):
        fx, fy, w, h = part['right']
        piece = tex.crop((fx, fy, fx + w, fy + h)).resize((w * scale, h * scale), Image.NEAREST)
        sheet.alpha_composite(piece, (x * scale, (y + 10) * scale))
    for part, x, y in HORSE_SIDE:
        for tex in (coat,) + tuple(body_layers):
            face(tex, part, x, y)
    if tack is not None:
        for part, x, y in TACK_SIDE + ([(dict(CHEST, right=CHEST['front']), 3, 3)] if panniers else []):
            face(tack, part, x, y)
    return sheet


def preview():
    from kit import PROJECT
    out = PROJECT / 'build/previews'
    out.mkdir(parents=True, exist_ok=True)
    capa = tinted(caparison(), CLOTH_RED)
    body = {'caparison (undyed)': over(capa, caparison_overlay()), 'leather_barding': leather_barding(),
            'mail_barding': mail_barding(), 'plate_barding': plate_barding(), 'vanilla iron (reference)': vanilla('entity/equipment/horse_body/iron.png')}
    tack = {'saddlebags': saddlebags(), 'bridle': bridle(), 'pack_saddle': pack_saddle(),
            'vanilla saddle (reference)': vanilla('entity/equipment/horse_saddle/saddle.png')}
    nets = [(n, uv_net(t, HORSE_PARTS)) for n, t in body.items()] + [(n, uv_net(t, SADDLE_PARTS)) for n, t in tack.items()]
    sheet = Image.new('RGBA', (3 * 400, 3 * 410), (30, 32, 36, 255))
    for i, (name, net) in enumerate(nets):
        x, y = (i % 3) * 400, (i // 3) * 410
        sheet.alpha_composite(net, (x + 8, y + 20))
        ImageDraw.Draw(sheet).text((x + 8, y + 4), name, fill=(255, 255, 255, 255))
    sheet.save(out / 'stablehand_gear_uv.png')

    coat, donkey = vanilla('entity/horse/horse_brown.png'), vanilla('entity/horse/donkey.png')
    views = [('bare + saddlebags', side_view(coat, (), saddlebags())), ('caparison (red) + saddlebags', side_view(coat, (body['caparison (undyed)'],), saddlebags())),
             ('caparison dyed blue', side_view(coat, (over(tinted(caparison(), -12827478), caparison_overlay()),), bridle())),
             ('leather + bridle', side_view(coat, (leather_barding(),), bridle())), ('mail + saddlebags', side_view(coat, (mail_barding(),), saddlebags())),
             ('plate + saddlebags', side_view(coat, (plate_barding(),), saddlebags())), ('donkey + pack saddle', side_view(donkey, (), pack_saddle(), panniers=True))]
    sheet = Image.new('RGBA', (4 * 226, 2 * 200), (30, 32, 36, 255))
    for i, (name, view) in enumerate(views):
        x, y = (i % 4) * 226, (i // 4) * 200
        sheet.alpha_composite(view, (x + 5, y + 18))
        ImageDraw.Draw(sheet).text((x + 5, y + 3), name, fill=(255, 255, 255, 255))
    sheet.save(out / 'stablehand_gear_side.png')

    icons = [(g, Image.open(__import__('io').BytesIO(data))) for g, data in
             ((p.stem, d) for p, d in outputs().items() if p.parent.name == 'item' and p.suffix == '.png' and 'in_hand' not in p.stem and 'overlay' not in p.stem)]
    icons = [(n, over(tinted(i, CLOTH_RED), caparison_sprite(True)) if n == 'caparison' else i) for n, i in icons]
    icons.append(('caparison blue', over(tinted(caparison_sprite(), -12827478), caparison_sprite(True))))
    sheet = Image.new('RGBA', (5 * 150 + 300, 2 * 160), (139, 169, 196, 255))
    for i, (name, icon) in enumerate(icons):
        x, y = (i % 5) * 150, (i // 5) * 160
        sheet.alpha_composite(icon.resize((128, 128), Image.NEAREST), (x + 10, y + 22))
        ImageDraw.Draw(sheet).text((x + 10, y + 6), name, fill=(20, 32, 44, 255))
    sheet.alpha_composite(lance_in_hand().resize((256, 256), Image.NEAREST), (5 * 150 + 20, 30))
    ImageDraw.Draw(sheet).text((5 * 150 + 20, 10), 'jousting_lance_in_hand (32 px)', fill=(20, 32, 44, 255))
    sheet.save(out / 'stablehand_gear_items.png')
    print('gear previews:', ', '.join(str(out / n) for n in ('stablehand_gear_uv.png', 'stablehand_gear_side.png', 'stablehand_gear_items.png')))

