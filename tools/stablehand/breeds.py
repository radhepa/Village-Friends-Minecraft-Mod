"""Horse breeds: the data table Java reads (stablehand/breeds.json), the painted coats (an adult and a foal
texture per breed), and the Grooming Brush and Horse Whistle with their sprites and recipes.

Each row: stat ranges (vanilla wild horses: health 15-30, speed 0.1125-0.3375 where x42.16 is blocks per
second, jump 0.4-1.0), where the breed is picked (biome keyword and weight; `any` matches every biome),
extra biome spawns for places vanilla has no horses (keyword, weight, group size), vanilla markings drawn on
top of the coat, how many painted coats it has, and which village types keep it in their stables.

Biome keywords: plains (path has "plains", not "snowy"), meadow, forest, savanna, desert, badlands, taiga,
snowy (cold farm-animal biomes), windswept (path starts with "windswept"), any.

Coats are painted from scratch on the vanilla horse's 64x64 cube-net UV layout (the box table below, read
from AbstractEquineModel.createBodyMesh and BabyHorseModel.createBabyMesh with javap): every face of every box
is filled from the breed's stepped palette, lit from the top (darker belly and inner legs), with seeded hash
noise for the hair, so the output is the same bytes on every run. Vanilla's markings layer (white socks,
dots) still draws on top, so each coat must stay UV-correct; `--preview` draws the flat UV net of every coat
next to the vanilla horse with each face outlined and labelled.

Never hand-edit breeds.json or a coat PNG; change the rows or palettes here and rerun tools/stablehand/stablehand.py.
"""
import zlib
from pathlib import Path

from kit import ASSETS, DATA, NS, PROJECT, TABLES, dump, item_files, png_bytes, raster

BREEDS = [
    {'id': 'destrier', 'name': 'Destrier', 'health': [26, 34], 'speed': [0.20, 0.26], 'jump': [0.55, 0.75],
     'spawns': [('plains', 1)], 'extra_spawns': [], 'markings': ['none', 'white'], 'coats': 1, 'village': ['plains']},
    {'id': 'palfrey', 'name': 'Palfrey', 'health': [20, 26], 'speed': [0.24, 0.30], 'jump': [0.60, 0.80],
     'spawns': [('plains', 4), ('meadow', 3), ('forest', 2)], 'extra_spawns': [], 'markings': ['white', 'white_field'],
     'coats': 1, 'village': ['plains']},
    {'id': 'courser', 'name': 'Courser', 'health': [16, 22], 'speed': [0.29, 0.3375], 'jump': [0.70, 0.95],
     'spawns': [('plains', 2), ('savanna', 2)], 'extra_spawns': [], 'markings': ['none', 'white_dots'],
     'coats': 1, 'village': ['plains', 'savanna']},
    {'id': 'rouncey', 'name': 'Rouncey', 'health': [18, 26], 'speed': [0.20, 0.27], 'jump': [0.55, 0.80],
     'spawns': [('plains', 5), ('forest', 3), ('any', 3)], 'extra_spawns': [],
     'markings': ['none', 'white', 'white_field', 'white_dots', 'black_dots'], 'coats': 1, 'village': ['plains', 'taiga']},
    {'id': 'draft', 'name': 'Draft Horse', 'health': [28, 36], 'speed': [0.15, 0.20], 'jump': [0.40, 0.55],
     'spawns': [('plains', 1), ('forest', 1), ('taiga', 1)], 'extra_spawns': [], 'markings': ['none', 'white'],
     'coats': 1, 'village': ['plains', 'taiga', 'snowy']},
    {'id': 'desert', 'name': 'Desert Horse', 'health': [16, 22], 'speed': [0.28, 0.34], 'jump': [0.65, 0.90],
     'spawns': [('desert', 5), ('badlands', 3)], 'extra_spawns': [('desert', 2, 2, 3), ('badlands', 1, 2, 3)],
     'markings': ['none'], 'coats': 1, 'village': ['desert']},
    {'id': 'steppe_pony', 'name': 'Steppe Pony', 'health': [20, 26], 'speed': [0.22, 0.28], 'jump': [0.75, 1.00],
     'spawns': [('savanna', 4), ('windswept', 4)], 'extra_spawns': [('windswept', 2, 2, 4)], 'markings': ['none', 'black_dots'],
     'coats': 1, 'village': ['savanna']},
    {'id': 'fjord', 'name': 'Fjord Horse', 'health': [22, 28], 'speed': [0.18, 0.24], 'jump': [0.60, 0.80],
     'spawns': [('taiga', 4), ('snowy', 4)], 'extra_spawns': [('taiga', 2, 2, 4), ('snowy', 1, 2, 3)], 'markings': ['none'],
     'coats': 1, 'village': ['taiga', 'snowy']},
]
KEYWORDS = ['plains', 'meadow', 'forest', 'savanna', 'desert', 'badlands', 'taiga', 'snowy', 'windswept', 'any']
MARKINGS = ['none', 'white', 'white_field', 'white_dots', 'black_dots']

# -- coat palettes ---------------------------------------------------------------------------------------
# Ramps run dark to light and are hue-shifted (warmer and more saturated in the shadows), 3-6 steps each, as
# in tools/item_sprites.py. Flags: points (dark lower legs), feather (a light hair band above the hoof; heavy =
# taller), stripe (dorsal stripe in the mane's dark), mealy (pale belly and muzzle), sheen (fine gold glints),
# dapple (lighter rings on the flanks), two_tone (a cream mane and tail with a dark centre).
PALETTES = {
    'destrier': {  # black bay war horse: near-black coat, black points, grey-white feathering
        'coat': ['241813', '2F2019', '3B2A20', '4A3527', '5A4130', '6C4F3A'],
        'mane': ['0E0B0A', '17120F', '221B17', '30261F'], 'hoof': ['262321', '3A3532'],
        'muzzle': ['3A2A22', '4D3A2F', '61493B'], 'feather': ['9C9286', 'BDB4A7', 'DAD3C6'],
        'eye': ['0B0807', 'D9CFC0'], 'points': True, 'feather_rows': 2},
    'palfrey': {  # chestnut riding horse with a flaxen mane and tail
        'coat': ['5E2A12', '74361A', '8B4422', '9F532B', 'B36536', 'C47843'],
        'mane': ['A7854F', 'C1A065', 'D7B97F', 'EBD3A0'], 'hoof': ['4A3A2D', '675243'],
        'muzzle': ['4E2614', '653420', '7E4429'], 'eye': ['1E1009', 'EADFC9'], 'points': False},
    'courser': {  # dappled steel grey with dark legs, built for speed
        'coat': ['3F4246', '51555A', '65696E', '7A7E82', '909397', 'A7A9AC'],
        'mane': ['1F2023', '2C2E31', '3B3D41', '4D5054'], 'hoof': ['2A2826', '413D39'],
        'muzzle': ['2B2C2F', '3A3B3F', '4C4E52'], 'eye': ['111214', 'E2E0DA'], 'points': True, 'dapple': True},
    'rouncey': {  # everyday bay: brown coat, black mane, tail and lower legs
        'coat': ['452A19', '553420', '664027', '7A4D2F', '8E5C38', 'A26C43'],
        'mane': ['1C1714', '28201C', '362B25', '463830'], 'hoof': ['2F2A26', '48413B'],
        'muzzle': ['3A2519', '4C3122', '5F3F2D'], 'eye': ['140D09', 'E3D8C6'], 'points': True},
    'draft': {  # heavy dark bay with a pale grey muzzle and big white feathers
        'coat': ['3A2216', '4A2B1C', '5B3523', '6E412B', '824E34', '955C3E'],
        'mane': ['1B1512', '271F1B', '352A24', '45372F'], 'hoof': ['3B3530', '5A5149'],
        'muzzle': ['6B5A50', '857166', '9F8A7E'], 'feather': ['AEA596', 'CEC6B8', 'E8E2D6'],
        'eye': ['120C09', 'E6DDCF'], 'points': True, 'feather_rows': 3},
    'desert': {  # golden buckskin with black points and a fine metallic sheen
        'coat': ['8A6233', '9F743E', 'B3864B', 'C4985A', 'D3AA6D', 'DFBB83'],
        'mane': ['241A13', '33261C', '443428', '584535'], 'hoof': ['2C2520', '463C33'],
        'muzzle': ['3E2E22', '54402F', '6B533F'], 'eye': ['130D08', 'F2E6CC'], 'sheen': 'F2DCA4', 'points': True},
    'steppe_pony': {  # yellow dun: dark legs, upright dark mane, dorsal stripe, mealy muzzle and belly
        'coat': ['74552F', '876439', 'A07849', 'B48B57', 'C49C68', 'D1AD7C'],
        'mane': ['2B2119', '3A2D22', '4B3B2D', '5E4B3A'], 'hoof': ['2C2620', '443B32'],
        'muzzle': ['C9B48C', 'DCCBA6', 'EADDBE'], 'pale': ['C9B48C', 'DCCBA6', 'EADDBE'],
        'eye': ['150F0A', 'EFE4CB'], 'points': True, 'stripe': True, 'mealy': True},
    'fjord': {  # brown dun cream: two-tone mane and tail, dorsal stripe, light feathering
        'coat': ['8C7556', '9E8765', 'B09978', 'C1AB8B', 'D0BC9E', 'DDCBB0'],
        'mane': ['C9BCA2', 'DDD2BB', 'EEE6D4', 'F7F2E6'], 'centre': ['3A3027', '4E4135'],
        'hoof': ['3B332B', '574C41'], 'muzzle': ['7A6A56', '8F7D67', 'A6937C'],
        'feather': ['C6B9A0', 'DAD0BB', 'ECE5D6'], 'eye': ['16100B', 'F4EEE1'],
        'stripe': True, 'two_tone': True, 'feather_rows': 2},
}

# -- the vanilla horse's boxes on its 64x64 texture --------------------------------------------------------
# (part, texOffs u, v, size W, H, D). Adult: AbstractEquineModel.createBodyMesh; foal: BabyHorseModel.createBabyMesh
# (both checked with javap -c -p -constants against the 26.3 jar). The foal's ears sit in the unused top-left
# corner of its head's net.
ADULT = [
    ('body', 0, 32, 10, 10, 22), ('neck', 0, 35, 4, 12, 7), ('head', 0, 13, 6, 5, 7), ('mouth', 0, 25, 4, 5, 5),
    ('mane', 56, 36, 2, 16, 2), ('ear', 19, 16, 2, 3, 1), ('leg', 48, 21, 4, 11, 4), ('tail', 42, 36, 3, 14, 4),
]
BABY = [
    ('body', 0, 13, 8, 7, 14), ('tail', 24, 34, 3, 3, 8),
    ('leg', 0, 34, 3, 9, 3), ('leg', 12, 34, 3, 9, 3), ('leg', 0, 46, 3, 9, 3), ('leg', 12, 46, 3, 9, 3),
    ('neck', 30, 0, 4, 8, 4), ('head', 0, 0, 6, 4, 9), ('ear', 0, 4, 2, 3, 1), ('ear', 0, 0, 2, 3, 1),
]
SIDES = ('west', 'north', 'east', 'south')


def faces(u, v, w, h, d):
    """A box's six faces on its texture, name -> (x, y, width, height): the cube net ModelPart.Cube reads (top and
    bottom side by side in the first strip, then west, north, east and south)."""
    return {'top': (u + d, v, w, d), 'bottom': (u + d + w, v, w, d), 'west': (u, v + d, d, h),
            'north': (u + d, v + d, w, h), 'east': (u + d + w, v + d, d, h), 'south': (u + d + w + d, v + d, w, h)}


def surface(face, i, j, w, h, d):
    """Where texel (i, j) of a face sits on its box, as fractions: x (0 west to 1 east), y (0 top to 1 bottom) and
    z (0 front, the way the horse faces, to 1 back). Matches the vertex order of ModelPart.Cube's polygons."""
    if face == 'top':
        return (i + .5) / w, 0.0, 1 - (j + .5) / d
    if face == 'bottom':
        return (i + .5) / w, 1.0, 1 - (j + .5) / d
    if face == 'west':
        return 0.0, (j + .5) / h, 1 - (i + .5) / d
    if face == 'east':
        return 1.0, (j + .5) / h, (i + .5) / d
    if face == 'north':
        return (i + .5) / w, (j + .5) / h, 0.0
    return 1 - (i + .5) / w, (j + .5) / h, 1.0


def noise(x, y, seed):
    """Deterministic hash noise in 0..1 (no random module, so every run and Python version paints the same bytes)."""
    h = (x * 374761393 + y * 668265263 + seed * 362437) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFF) / 65535.0


def step(ramp, level, jitter=0.0):
    """A colour from a dark-to-light ramp for a light level 0..1, stepped (never blended), nudged by jitter."""
    i = round(level * (len(ramp) - 1) + jitter)
    return ramp[max(0, min(len(ramp) - 1, i))]


def light(face, fy):
    """Light from above, kept gentle because the game shades each face too: a back as bright as the top of the
    flanks, sides that darken toward the belly, a dark underside."""
    if face == 'top':
        return .74
    if face == 'bottom':
        return .2
    level = .74 - .38 * fy ** 1.3
    return level - (.05 if face == 'north' else .08 if face == 'south' else 0)


class Texel:
    """One texel being painted: its face, its place on the face (i, j) and on the box (fx, fy, fz), the box size
    and its pixel on the texture."""
    __slots__ = ('face', 'i', 'j', 'fx', 'fy', 'fz', 'w', 'h', 'd', 'x', 'y')

    def __init__(self, face, i, j, box, x, y):
        self.face, self.i, self.j, (self.w, self.h, self.d), self.x, self.y = face, i, j, box, x, y
        self.fx, self.fy, self.fz = surface(face, i, j, *box)

    @property
    def row(self):
        """Which row of the box's height this texel is on (the top face is row 0, the bottom face the last)."""
        return 0 if self.face == 'top' else self.h - 1 if self.face == 'bottom' else self.j


class Coat:
    """A breed's painted coat on the vanilla horse UV layout: the adult texture, or the foal's (a shade lighter, with a
    short fluffy mane on the neck because the foal model has no mane box)."""

    def __init__(self, breed, baby=False):
        self.p, self.baby = PALETTES[breed], baby
        self.seed = zlib.crc32(f'{breed}:{"foal" if baby else "adult"}'.encode()) & 0xFFFF
        self.lift = .07 if baby else 0.0
        # The dark used for the dorsal stripe and a two-tone mane's centre.
        self.dark = self.p.get('centre', self.p['mane'][:2])

    def paint(self):
        from PIL import Image
        image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
        for part, u, v, w, h, d in (BABY if self.baby else ADULT):
            shader = getattr(self, part)
            for face, (x0, y0, fw, fh) in faces(u, v, w, h, d).items():
                for j in range(fh):
                    for i in range(fw):
                        colour = shader(Texel(face, i, j, (w, h, d), x0 + i, y0 + j))
                        image.putpixel((x0 + i, y0 + j), tuple(bytes.fromhex(colour)) + (255,))
        return image

    def palette(self):
        """Every colour this coat may use (the painted texture must use no other)."""
        colours = set()
        for key, value in self.p.items():
            if isinstance(value, list):
                colours.update(value)
            elif key == 'sheen':
                colours.add(value)
        return colours

    # -- helpers ------------------------------------------------------------------------------------------
    def grain(self, t, amount=.55, salt=0):
        return (noise(t.x, t.y, self.seed + salt) - .5) * 2 * amount

    def hair(self, t, level, amount=.55):
        """Short coat hair: the coat ramp at a light level, with fine noise for texture."""
        return step(self.p['coat'], level + self.lift, self.grain(t, amount))

    def strands(self, t, ramp, level, along_y=True):
        """Long hair (mane, tail): streaks that run along the hair, lighter where the light falls."""
        streak = noise(t.x, 0 if along_y else t.y, self.seed + 3) - .5
        return step(ramp, level + .35 * streak + self.lift, (noise(t.x, t.y // 3, self.seed + 5) - .5) * .7)

    def dapple(self, t):
        """Light rings of a dapple grey: one jittered spot per 4x4 cell of the texture."""
        cx, cy = t.x // 4, t.y // 4
        ox, oy = int(noise(cx, cy, self.seed + 7) * 3), int(noise(cx, cy, self.seed + 11) * 3)
        dx, dy = t.x - (cx * 4 + ox), t.y - (cy * 4 + oy)
        return dx * dx + dy * dy <= 1 and noise(cx, cy, self.seed + 13) > .3

    def long_hair(self, t, level):
        """A mane or tail texel: plain strands, or for a two-tone mane the dark centre on the crest."""
        if self.p.get('two_tone') and t.face in ('top', 'south', 'north') and abs(t.fx - .5) < .2:
            return step(self.dark, .5, self.grain(t, .4, 9))
        return self.strands(t, self.p['mane'], level)

    # -- parts --------------------------------------------------------------------------------------------
    def body(self, t):
        p = self.p
        if p.get('stripe') and abs(t.fx - .5) < .15 and (t.face == 'top' or t.face == 'south' and t.fy < .3):
            return step(self.dark, .5, self.grain(t, .5, 1))
        if p.get('mealy') and (t.face == 'bottom' or t.face in SIDES and t.fy > .78):
            return step(p['pale'], .55 if t.face == 'bottom' else .3, self.grain(t, .5, 2))
        level = light(t.face, t.fy)
        if t.face in SIDES and t.fy < .12:
            level += .08  # the light catching the line of the back
        if t.face == 'south' and t.fy < .45 and abs(t.fx - .5) < .2:
            level -= .1  # shadow under the tail
        if p.get('dapple') and t.face in ('top', 'west', 'east') and t.fy < .7 and self.dapple(t):
            level += .2
        if p.get('sheen') and t.face in ('top', 'west', 'east') and t.fy < .6 and noise(t.x, t.y, self.seed + 4) > .9:
            return p['sheen']
        return self.hair(t, level)

    def neck(self, t):
        back = t.fz > (.7 if self.baby else .8)
        if t.face in ('south', 'top') or t.face in ('west', 'east') and back and t.fy < .9:
            if self.baby and t.face == 'south' and self.p.get('two_tone') and abs(t.fx - .5) < .3:
                return step(self.dark, .5, self.grain(t, .4, 9))
            return self.strands(t, self.p['mane'], .55 if t.face != 'west' else .45)
        level = .74 - .14 * t.fy if t.face in ('west', 'east') else .6 if t.face == 'north' else .3
        return self.hair(t, level)

    def mane(self, t):
        level = .7 if t.face in ('south', 'top') else .45 if t.face == 'north' else .58 - .2 * t.fy
        return self.long_hair(t, level)

    def tail(self, t):
        level = .65 if t.face == 'top' else .35 if t.face == 'bottom' else .6 - .3 * t.fy
        if self.baby:  # the foal's tail is a short tuft that runs backwards (along z), lit from above
            level = .7 if t.face == 'top' else .3 if t.face == 'bottom' else .5
        return self.long_hair(t, level)

    def eye(self, t, pupil, glint):
        """The eye's two texels on a side face of the head: a dark pupil with a pale catchlight behind it."""
        if t.face not in ('west', 'east') or t.j != 1:
            return None
        i_pupil = round((1 - pupil) * t.d - .5) if t.face == 'west' else round(pupil * t.d - .5)
        i_glint = round((1 - glint) * t.d - .5) if t.face == 'west' else round(glint * t.d - .5)
        return self.p['eye'][0] if t.i == i_pupil else self.p['eye'][1] if t.i == i_glint else None

    def head(self, t):
        p, m = self.p, self.p['muzzle']
        eye = self.eye(t, .61, .72) if self.baby else self.eye(t, .36, .5)
        if eye:
            return eye
        # The forelock: mane hair on top of the head, between the ears.
        if t.face == 'top' and t.fz > (.75 if self.baby else .55) and abs(t.fx - .5) < .2:
            return self.strands(t, p['mane'], .6)
        if self.baby:  # the foal's head box carries its whole face: muzzle in front, nostrils, mouth line
            if t.face == 'north' and t.j == 1 and t.i in (1, t.w - 2):
                return m[0]
            if t.face in ('west', 'east') and t.j == 2 and t.fz < .3:
                return m[0]
            if t.fz < .34 or t.face == 'north':
                return step(m, light(t.face, t.fy) + .05, self.grain(t, .4, 6))
        level = light(t.face, t.fy) + (.05 if t.face in ('west', 'east') else 0)
        return self.hair(t, level - (.1 if t.face == 'bottom' else 0))

    def mouth(self, t):
        m = self.p['muzzle']
        if t.face == 'north' and t.j == 1 and t.i in (0, t.w - 1):
            return m[0]  # nostrils
        if t.face in ('west', 'east') and t.j == 3 and t.fz < .55:
            return m[0]  # the line of the mouth
        if t.fz < .6 or t.face in ('north', 'bottom'):
            return step(m, light(t.face, t.fy) + .08, self.grain(t, .4, 6))
        return self.hair(t, light(t.face, t.fy))

    def ear(self, t):
        if t.row == 0 and t.face != 'bottom':
            return self.strands(t, self.p['mane'], .35)  # dark tips
        if t.face == 'north':
            return step(self.p['muzzle'], .15, self.grain(t, .3, 8))  # the inside of the ear, in shadow
        return self.hair(t, light(t.face, t.fy) + .05)

    def leg(self, t):
        p, h, row = self.p, t.h, t.row
        hooves = 1 if self.baby else 2
        feathers = max(0, p.get('feather_rows', 0) - (1 if self.baby else 0))
        if t.face == 'bottom' or row >= h - hooves:
            return step(p['hoof'], .15 if t.face == 'bottom' else 1 if row == h - hooves and not self.baby else .4, self.grain(t, .3, 10))
        level = .8 if t.face == 'top' else (.55 if t.face == 'south' else .68) - .22 * t.fy - (.12 if t.face == 'east' else 0)
        top_feather = h - hooves - feathers
        if feathers and (row > top_feather or row == top_feather and noise(t.x, t.y, self.seed + 12) > .35):
            return step(p['feather'], level + .15, self.grain(t, .5, 11))  # feathering: long pale hair over the hoof
        lower = (4 if self.baby else 5) + (1 if noise(t.x, 0, self.seed + 14) > .5 else 0)
        if row >= lower:
            if p.get('points'):
                return self.strands(t, p['mane'], level)  # dark points
            return self.hair(t, level - .12)
        return self.hair(t, level)


def coat_name(breed, baby, coat=0):
    """The texture file of a coat, as HorseCoats asks for it: <breed>[_<n>][_baby].png."""
    return f'{breed}{f"_{coat}" if coat else ""}{"_baby" if baby else ""}'


def coats():
    """Every coat texture: {file name: image}, after checking each uses only its breed's palette."""
    out = {}
    for b in BREEDS:
        assert b['coats'] == 1, f"{b['id']}: paint its extra coats before raising 'coats'"
        for baby in (False, True):
            coat = Coat(b['id'], baby)
            image = coat.paint()
            used = {'%02X%02X%02X' % px[:3] for px in image.getdata() if px[3]}
            assert used <= coat.palette(), (b['id'], baby, used - coat.palette())
            out[coat_name(b['id'], baby)] = image
    return out


# -- the Grooming Brush and Horse Whistle (16px, outline + stepped palette, light from the top left) -----------
# A dandy brush on a short stick handle: a wooden back, then wheat-straw bristles that point away from the hand.
BRUSH = """
................
................
.........oo.....
........oWWo....
.......oWWwdo...
......oWWwwdDo..
.....oWwwwdDobo.
....oWwwwdDobBbo
...oLlwwdDobBbBo
..oLlldDDobBbBso
..olldDDobBbBso.
..oodDDobBbsso..
.oSoooobsbsso...
oSso...oooooo...
oso.............
.o..............
"""
BRUSH_COLOURS = {'o': '3B2416', 'W': 'D9A066', 'w': 'B98149', 'd': '8F5E30', 'D': '6B4422', 'S': '9C7444',
                 'B': 'E2C77E', 'b': 'C2A35A', 's': '8E7438', 'L': 'A0522D', 'l': '7A3B1F'}
# A pea whistle: an iron mouthpiece, a round copper chamber with its slot, and a cord loop to hang it by.
WHISTLE = """
................
..........sss...
.........s...s..
.........s...s..
..........s.s...
..........ooo...
........oohCcoo.
.ooooooohCCCccco
oIIIIIIkhCCcccco
oiIIIIIIcCccccco
oiiiiiiiocccccco
.oooooooocccccDo
.........occcDo.
..........oooo..
................
................
"""
WHISTLE_COLOURS = {'o': '2E1E16', 'h': 'F2B48A', 'C': 'E08A5A', 'c': 'B86A3F', 'D': '8A4A2A', 'k': '4A2414',
                   'I': 'E3E3E3', 'i': 'A8A8A8', 's': 'C9B48C'}
SPRITES = {'grooming_brush': lambda: raster(BRUSH, BRUSH_COLOURS), 'horse_whistle': lambda: raster(WHISTLE, WHISTLE_COLOURS)}
RECIPES = {
    # Wheat bristles bound with string to a stick.
    'grooming_brush': {'type': 'minecraft:crafting_shaped', 'category': 'equipment',
                       'result': {'id': f'{NS}:grooming_brush', 'count': 1}, 'pattern': ['  W', ' T ', 'S  '],
                       'key': {'S': 'minecraft:stick', 'T': 'minecraft:string', 'W': 'minecraft:wheat'}},
    'horse_whistle': {'type': 'minecraft:crafting_shapeless', 'category': 'equipment',
                      'result': {'id': f'{NS}:horse_whistle', 'count': 1},
                      'ingredients': ['minecraft:copper_ingot', 'minecraft:iron_nugget', 'minecraft:iron_nugget']},
}


def table():
    rows = []
    for b in BREEDS:
        assert all(k in KEYWORDS for k, _ in b['spawns']) and all(s[0] in KEYWORDS for s in b['extra_spawns']), b['id']
        assert all(m in MARKINGS for m in b['markings']), b['id']
        assert b['id'] in PALETTES, f"{b['id']} needs a palette"
        rows.append({'id': b['id'], 'name': b['name'], 'health': b['health'], 'speed': b['speed'], 'jump': b['jump'],
                     'spawns': [{'biome': k, 'weight': w} for k, w in b['spawns']],
                     'extra_spawns': [{'biome': k, 'weight': w, 'min': lo, 'max': hi} for k, w, lo, hi in b['extra_spawns']],
                     'markings': b['markings'], 'coats': b['coats'], 'village': b['village']})
    return {'breeds': rows}


def outputs():
    files = {TABLES / 'breeds.json': dump(table())}
    for name, image in coats().items():
        files[ASSETS / f'textures/entity/horse/{name}.png'] = png_bytes(image)
    for name, sprite in SPRITES.items():
        files.update(item_files(name, sprite()))
    for name, recipe in RECIPES.items():
        files[DATA / f'{NS}/recipe/{name}.json'] = dump(recipe)
    return files


# -- preview -------------------------------------------------------------------------------------------------
CLIENT_JAR = Path.home() / '.gradle/caches/fabric-loom/26.3/minecraft-client.jar'
PREVIEWS = PROJECT / 'build/previews'
SCALE = 6
PART_COLOURS = {'body': (230, 60, 60), 'neck': (60, 160, 230), 'head': (240, 200, 40), 'mouth': (240, 130, 30),
                'mane': (170, 80, 220), 'ear': (40, 200, 120), 'leg': (60, 220, 220), 'tail': (230, 90, 180)}


def vanilla(name):
    """A vanilla horse texture from the client jar, for comparison only (never copied into the repo)."""
    import io
    import zipfile
    from PIL import Image
    with zipfile.ZipFile(CLIENT_JAR) as jar:
        return Image.open(io.BytesIO(jar.read(f'assets/minecraft/textures/entity/horse/{name}.png'))).convert('RGBA')


def uv_net(image, boxes):
    """A texture at 6x on a checkerboard, every box face outlined in its part's colour and labelled where it fits."""
    from PIL import Image, ImageDraw
    size = 64 * SCALE
    sheet = Image.new('RGBA', (size, size))
    for y in range(0, size, 12):
        for x in range(0, size, 12):
            sheet.paste((205, 205, 205, 255) if (x + y) // 12 % 2 else (240, 240, 240, 255), (x, y, x + 12, y + 12))
    sheet.alpha_composite(image.resize((size, size), Image.NEAREST))
    draw = ImageDraw.Draw(sheet)
    for part, u, v, w, h, d in boxes:
        for face, (x, y, fw, fh) in faces(u, v, w, h, d).items():
            box = (x * SCALE, y * SCALE, (x + fw) * SCALE - 1, (y + fh) * SCALE - 1)
            draw.rectangle(box, outline=PART_COLOURS[part] + (255,))
            label = f'{part}.{face}'
            if fw * SCALE >= 6 * len(label) + 4 and fh * SCALE >= 14:
                draw.text((box[0] + 2, box[1] + 2), label, fill=(0, 0, 0, 255))
            elif fw * SCALE >= 12 and fh * SCALE >= 14:
                draw.text((box[0] + 2, box[1] + 2), face[0], fill=(0, 0, 0, 255))
    return sheet


def preview():
    from PIL import Image, ImageDraw
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    rows = [('vanilla horse_brown (reference)', vanilla('horse_brown'), vanilla('horse_brown_baby'))]
    images = coats()
    rows += [(b['name'], images[coat_name(b['id'], False)], images[coat_name(b['id'], True)]) for b in BREEDS]
    size, gap, title = 64 * SCALE, 16, 22
    sheet = Image.new('RGBA', (gap * 3 + size * 2, len(rows) * (size + title + gap) + gap), (40, 40, 44, 255))
    draw = ImageDraw.Draw(sheet)
    for r, (name, adult, baby) in enumerate(rows):
        top = gap + r * (size + title + gap)
        draw.text((gap, top), f'{name}: adult (left), foal (right)', fill=(255, 255, 255, 255))
        sheet.alpha_composite(uv_net(adult, ADULT), (gap, top + title))
        sheet.alpha_composite(uv_net(baby, BABY), (gap * 2 + size, top + title))
    sheet.save(PREVIEWS / 'stablehand_coats.png')
    items = Image.new('RGBA', (16 * 8 * len(SPRITES) + 8 * (len(SPRITES) + 1), 16 * 8 + 16), (40, 40, 44, 255))
    for k, sprite in enumerate(SPRITES.values()):
        items.alpha_composite(sprite().resize((128, 128), Image.NEAREST), (8 + k * 136, 8))
    items.save(PREVIEWS / 'stablehand_bond_items.png')
    print(f'breeds: {PREVIEWS.relative_to(PROJECT)}/stablehand_coats.png and stablehand_bond_items.png')

