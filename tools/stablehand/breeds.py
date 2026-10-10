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
     'spawns': [('plains', 1)], 'extra_spawns': [], 'markings': ['none', 'white'], 'coats': 2, 'village': ['plains']},
    {'id': 'palfrey', 'name': 'Palfrey', 'health': [20, 26], 'speed': [0.24, 0.30], 'jump': [0.60, 0.80],
     'spawns': [('plains', 4), ('meadow', 3), ('forest', 2)], 'extra_spawns': [], 'markings': ['white', 'white_field'],
     'coats': 2, 'village': ['plains']},
    {'id': 'courser', 'name': 'Courser', 'health': [16, 22], 'speed': [0.29, 0.3375], 'jump': [0.70, 0.95],
     'spawns': [('plains', 2), ('savanna', 2)], 'extra_spawns': [], 'markings': ['none', 'white_dots'],
     'coats': 2, 'village': ['plains', 'savanna']},
    {'id': 'rouncey', 'name': 'Rouncey', 'health': [18, 26], 'speed': [0.20, 0.27], 'jump': [0.55, 0.80],
     'spawns': [('plains', 5), ('forest', 3), ('any', 3)], 'extra_spawns': [],
     'markings': ['none', 'white', 'white_field', 'white_dots', 'black_dots'], 'coats': 2, 'village': ['plains', 'taiga']},
    {'id': 'draft', 'name': 'Draft Horse', 'health': [28, 36], 'speed': [0.15, 0.20], 'jump': [0.40, 0.55],
     'spawns': [('plains', 1), ('forest', 1), ('taiga', 1)], 'extra_spawns': [], 'markings': ['none', 'white'],
     'coats': 2, 'village': ['plains', 'taiga', 'snowy']},
    {'id': 'desert', 'name': 'Desert Horse', 'health': [16, 22], 'speed': [0.28, 0.34], 'jump': [0.65, 0.90],
     'spawns': [('desert', 5), ('badlands', 3)], 'extra_spawns': [('desert', 2, 2, 3), ('badlands', 1, 2, 3)],
     'markings': ['none'], 'coats': 2, 'village': ['desert']},
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
        'muzzle': ['3E2E22', '54402F', '6B533F'], 'eye': ['130D08', 'F2E6CC'], 'sheen': 'EECD8E', 'points': True},
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

# Extra coats (coat 1, 2...): whole palettes of their own, in the same keys. A row's `coats` must match.
VARIANTS = {
    'destrier': [{  # dapple grey, the knight's grey charger
        'coat': ['4A4C50', '5E6166', '75787D', '8D9094', 'A6A8AB', 'BEC0C2'],
        'mane': ['3A3B3E', '55575B', '7A7C80', '9EA0A3'], 'hoof': ['2E2C2A', '47433F'],
        'muzzle': ['2F3033', '404145', '55575B'], 'feather': ['B8B8B4', 'D2D2CE', 'E8E8E4'],
        'eye': ['0E0F11', 'E4E2DC'], 'dapple': True, 'feather_rows': 2}],
    'palfrey': [{  # palomino: gold with a white-cream mane
        'coat': ['9A6E2C', 'B08236', 'C4963F', 'D4A94E', 'E0BA62', 'EAC979'],
        'mane': ['D9CDB0', 'E7DDC4', 'F1EADA', 'F8F4EA'], 'hoof': ['5A4632', '7A634C'],
        'muzzle': ['7D5A2C', '94703A', 'AA854A'], 'eye': ['1E1309', 'EFE5CF']}],
    'courser': [{  # liver chestnut: dark red-brown all over
        'coat': ['3E1E10', '4E2615', '5F2F1B', '713922', '834429', '954F31'],
        'mane': ['2E160C', '3D1E11', '4C2717', '5C301D'], 'hoof': ['2E2622', '463B34'],
        'muzzle': ['341A0F', '452316', '572D1C'], 'eye': ['120A06', 'E2D5C0']}],
    'rouncey': [{  # sorrel: chestnut with a mane of the same red
        'coat': ['6A3216', '7E3E1D', '924A24', 'A5572C', 'B76535', 'C77440'],
        'mane': ['5A2A13', '70351A', '874222', '9E5029'], 'hoof': ['4A3B2E', '675243'],
        'muzzle': ['552815', '6B341C', '824124'], 'eye': ['1C0F08', 'E8DCC6']}],
    'draft': [{  # dark dapple grey with white feathers
        'coat': ['3C3E42', '4F5256', '63666B', '797C80', '8F9296', 'A5A8AB'],
        'mane': ['2A2B2E', '3A3C3F', '4D4F53', '616367'], 'hoof': ['3B3530', '5A5149'],
        'muzzle': ['2C2D30', '3B3C40', '4E5054'], 'feather': ['B5B6B2', 'D0D1CD', 'E8E8E5'],
        'eye': ['0F1012', 'E6E4DE'], 'dapple': True, 'feather_rows': 3}],
    'desert': [{  # flea-bitten grey: near-white with fine dark flecks and a dark skin muzzle
        'coat': ['8E8E8A', 'A2A29E', 'B5B5B1', 'C7C7C3', 'D8D8D4', 'E6E6E2'],
        'mane': ['6F6F6C', '868683', '9E9E9B', 'B6B6B3'], 'hoof': ['3A3633', '55504B'],
        'muzzle': ['4A4A4C', '5E5E60', '737375'], 'eye': ['141414', 'F2F0EA'], 'flecks': '6A5A4C'}],
}


def palettes(breed):
    """A breed's coats in order: its main palette, then its variants."""
    return [PALETTES[breed]] + VARIANTS.get(breed, [])

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

    def __init__(self, breed, baby=False, coat=0):
        self.p, self.baby = palettes(breed)[coat], baby
        self.seed = zlib.crc32(f'{breed}:{coat}:{"foal" if baby else "adult"}'.encode()) & 0xFFFF
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
            elif key in ('sheen', 'flecks'):
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
        if p.get('mealy') and (t.face == 'bottom' or t.face in SIDES and t.fy > .88):
            return step(p['pale'], .55 if t.face == 'bottom' else .3, self.grain(t, .5, 2))
        level = light(t.face, t.fy)
        if t.face in SIDES and t.fy < .12:
            level += .08  # the light catching the line of the back
        if t.face == 'south' and t.fy < .45 and abs(t.fx - .5) < .2:
            level -= .1  # shadow under the tail
        if p.get('dapple') and t.face in ('top', 'west', 'east') and t.fy < .7 and self.dapple(t):
            level += .2
        if p.get('sheen') and t.face in ('top', 'west', 'east') and t.fy < .6 and noise(t.x, t.y, self.seed + 4) > .955:
            return p['sheen']
        if p.get('flecks') and t.face in ('top', 'west', 'east', 'north', 'south') and noise(t.x, t.y, self.seed + 15) > .93:
            return p['flecks']
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
        assert b['coats'] == len(palettes(b['id'])), f"{b['id']}: 'coats' is {b['coats']} but it has {len(palettes(b['id']))} palettes"
        for n in range(b['coats']):
            for baby in (False, True):
                coat = Coat(b['id'], baby, n)
                image = coat.paint()
                used = {'%02X%02X%02X' % px[:3] for px in image.getdata() if px[3]}
                assert used <= coat.palette(), (b['id'], n, baby, used - coat.palette())
                out[coat_name(b['id'], baby, n)] = image
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
    rows += [(b['name'] + (f' (coat {n})' if n else ''), images[coat_name(b['id'], False, n)], images[coat_name(b['id'], True, n)])
             for b in BREEDS for n in range(b['coats'])]
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
    models(images)
    print(f'breeds: {PREVIEWS.relative_to(PROJECT)}/stablehand_coats.png, stablehand_coats_3d.png and stablehand_bond_items.png')


# -- 3D preview: every coat on the vanilla horse model, next to vanilla's own horse ------------------------------
# part: (parent, pivot, rotation in radians, [(uv, origin, size, mirrored)]), from the same two vanilla mesh methods,
# posed as setupAnim leaves a horse standing still (head and adult tail at 30 degrees, the foal's tail at -60).
TILT = 0.5235988


def horse_parts(baby):
    if baby:
        leg = [(3, 9, 3)]
        return {
            'body': (None, (0, 12.5, 0), (0, 0, 0), [((0, 13), (-4, -3.5, -7), (8, 7, 14), False)]),
            'tail': ('body', (0, -1, 7), (-2 * TILT, 0, 0), [((24, 34), (-1.5, -1.5, -1), (3, 3, 8), False)]),
            'left_hind_leg': (None, (2.4, 16, 5.4), (0, 0, 0), [((12, 46), (-1.5, -1, -1.5), leg[0], False)]),
            'right_hind_leg': (None, (-2.4, 16, 5.4), (0, 0, 0), [((0, 46), (-1.5, -1, -1.5), leg[0], False)]),
            'left_front_leg': (None, (2.4, 16, -5.4), (0, 0, 0), [((12, 34), (-1.5, -1, -1.5), leg[0], False)]),
            'right_front_leg': (None, (-2.4, 16, -5.4), (0, 0, 0), [((0, 34), (-1.5, -1, -1.5), leg[0], False)]),
            'head_parts': (None, (0, 10, -6), (TILT, 0, 0), [((30, 0), (-2, -6, -2), (4, 8, 4), False)]),
            'head': ('head_parts', (0, -6.0516, -.2951), (0, 0, 0), [((0, 0), (-3, -3.9484, -6.705), (6, 4, 9), False)]),
            'left_ear': ('head', (2, -4.2484, 1.9451), (0, 0, .2618), [((0, 4), (-1, -2.5, -.8), (2, 3, 1), False)]),
            'right_ear': ('head', (-2, -4.2484, 1.645), (0, 0, -.2618), [((0, 0), (-1, -2.5, -.5), (2, 3, 1), False)]),
        }
    leg = (48, 21)
    return {
        'body': (None, (0, 11, 5), (0, 0, 0), [((0, 32), (-5, -8, -17), (10, 10, 22), False)]),
        'tail': ('body', (0, -5, 2), (TILT, 0, 0), [((42, 36), (-1.5, 0, 0), (3, 14, 4), False)]),
        'head_parts': (None, (0, 4, -12), (TILT, 0, 0), [((0, 35), (-2.05, -6, -2), (4, 12, 7), False)]),
        'head': ('head_parts', (0, 0, 0), (0, 0, 0), [((0, 13), (-3, -11, -2), (6, 5, 7), False)]),
        'mane': ('head_parts', (0, 0, 0), (0, 0, 0), [((56, 36), (-1, -11, 5.01), (2, 16, 2), False)]),
        'upper_mouth': ('head_parts', (0, 0, 0), (0, 0, 0), [((0, 25), (-2, -11, -7), (4, 5, 5), False)]),
        'left_ear': ('head', (0, 0, 0), (0, 0, 0), [((19, 16), (.55, -13, 4), (2, 3, 1), False)]),
        'right_ear': ('head', (0, 0, 0), (0, 0, 0), [((19, 16), (-2.55, -13, 4), (2, 3, 1), False)]),
        'left_hind_leg': (None, (4, 14, 7), (0, 0, 0), [(leg, (-3, -1.01, -1), (4, 11, 4), True)]),
        'right_hind_leg': (None, (-4, 14, 7), (0, 0, 0), [(leg, (-1, -1.01, -1), (4, 11, 4), False)]),
        'left_front_leg': (None, (4, 14, -10), (0, 0, 0), [(leg, (-3, -1.01, -1.9), (4, 11, 4), True)]),
        'right_front_leg': (None, (-4, 14, -10), (0, 0, 0), [(leg, (-1, -1.01, -1.9), (4, 11, 4), False)]),
    }


def renderer():
    """The wardrobe's tiny box-UV renderer (Canvas, cube_quads), loaded by path as tools/pets/preview.py does."""
    import importlib.util
    import sys
    folder = Path(__file__).resolve().parents[1] / 'wardrobe'
    sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location('wardrobe_preview', folder / 'preview.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rotation(x, y, z):
    """ModelPart rotation (Z @ Y @ X)."""
    import math
    import numpy as np
    cx, sx, cy, sy, cz, sz = math.cos(x), math.sin(x), math.cos(y), math.sin(y), math.cos(z), math.sin(z)
    return (np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]) @ np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
            @ np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]]))


def draw_horse(P, canvas, tex, baby, cx, cy, scale, yaw, pitch=-12):
    import math
    import numpy as np
    parts = horse_parts(baby)
    view = rotation(math.radians(pitch), 0, 0) @ rotation(0, math.radians(yaw), 0)

    def transform(name):
        parent, pivot, angles, _ = parts[name]
        r = rotation(*angles)
        if parent is None:
            return (lambda v: np.array(pivot, float) + r @ v), r
        pf, pr = transform(parent)
        return (lambda v: pf(np.array(pivot, float) + r @ v)), pr @ r

    for name, (_, _, _, cubes) in parts.items():
        f, r = transform(name)
        for uv, origin, size, mirrored in cubes:
            middle = origin[0] + size[0] / 2
            for verts, uvs, normal in P.cube_quads(origin, size, uv, 0):
                if mirrored:  # ModelPart.Cube swaps min and max x: the same texture, reflected across the box
                    verts = [np.array((2 * middle - v[0], v[1], v[2])) for v in verts]
                    normal = (-normal[0], normal[1], normal[2])
                n = view @ (r @ np.array(normal, float))
                if n[2] >= -1e-6:
                    continue
                light = 0.58 + 0.30 * max(0, -n[1]) + 0.12 * max(0, -n[2]) + 0.06 * max(0, -n[0])
                pts = []
                for v in verts:
                    w = view @ (f(np.array(v, float)) - np.array((0, 24, 0)))
                    pts.append(np.array([cx + w[0] * scale, cy + w[1] * scale, w[2]]))
                canvas.quad(pts, uvs, tex, min(1.0, light))


def models(images):
    """build/previews/stablehand_coats_3d.png: each coat on the model from two sides, adult and foal."""
    import numpy as np
    from PIL import Image, ImageDraw
    P = renderer()
    rows = [('vanilla horse_brown', vanilla('horse_brown'), vanilla('horse_brown_baby'))]
    rows += [(b['name'] + (f' (coat {n})' if n else ''), images[coat_name(b['id'], False, n)], images[coat_name(b['id'], True, n)])
             for b in BREEDS for n in range(b['coats'])]
    cell_w, cell_h, scale = 230, 205, 5
    views = [(False, -125), (False, 55), (True, -125), (True, 55)]
    canvas = P.Canvas(cell_w * len(views), cell_h * len(rows), bg=(214, 222, 205))
    for r, (_, adult, baby) in enumerate(rows):
        for k, (is_baby, yaw) in enumerate(views):
            tex = np.array((baby if is_baby else adult).convert('RGBA'))
            draw_horse(P, canvas, tex, is_baby, cell_w * k + cell_w / 2, cell_h * r + cell_h - (25 if not is_baby else 40),
                       scale if not is_baby else scale * 1.25, yaw)
    sheet = Image.fromarray(np.clip(canvas.img, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(sheet)
    for r, (name, _, _) in enumerate(rows):
        draw.text((6, cell_h * r + 4), name, fill=(40, 40, 40))
    sheet.save(PREVIEWS / 'stablehand_coats_3d.png')

