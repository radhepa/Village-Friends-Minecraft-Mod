"""Building blocks for the female wardrobe: long skirts, bodices, lacing, sleeves, over-layers and trims.

Female residents wear the same wide-arm player mesh as everyone else, so femininity comes from the
cut: fitted bodices, laced fronts, chemise and puffed sleeves, aprons, overdresses and long skirts.
Every helper paints key colors only and returns what it built, so a module adds its own identity
(lacing, trim, embroidery, accessories) on top. Keep a piece's identity in its own module.

Depth rules that let any female top layer over any female bottom while the legs stride:

* Skirt panels (bottoms) hang from the hips: pivot y between SKIRT_TOP_MIN and SKIRT_TOP_MAX, front
  face z -2.95, back face z 2.95, and side panels just outside x +-5.1 that flare outward.
* Bottom waist pieces (belts, sashes, hip pouches) have ids starting with "waist", so a top that
  covers the waist hides them.
* Over-layers on tops (aprons, tabards, overdress and coat panels) hang in front of any skirt: front
  face z -3.15, back face z 3.15, hinged at or above y OVER_TOP_MAX. A flap hinged higher than the
  skirt keeps in front of it through the whole stride, so the two never cross.
* Belts, girdles and sashes on tops sit at the natural waist (y 7-9), above every skirt.
"""
from __future__ import annotations

from kit import SIDES, arm_bone, arm_x, footwear, leg_bone
from paint import cap, fabric, grid, k, rnd, solid, strip_fabric
from wardrobe import Face, shade

SKIRT_FRONT, SKIRT_BACK = -2.95, 1.95      # skirt panel boxes: front -2.95..-1.95, back 1.95..2.95
OVER_FRONT, OVER_BACK = -3.15, 2.15        # top over-layer boxes: front -3.15..-2.15, back 2.15..3.15
SKIRT_TOP_MIN, SKIRT_TOP_MAX = 9.2, 10.4
OVER_TOP_MAX = 9.2


# -- surfaces and patterns ---------------------------------------------------------------------
def sub(face: Face, x0: int, y0: int, w: int, h: int) -> Face:
    """A rectangular window of a face that paints like a face of its own."""
    return Face(face.layer, face.x0 + x0, face.y0 + y0, w, h, face.name)


def outer(box):
    """The four side faces of a box in strip order."""
    return [box.right, box.front, box.left, box.back]


# One- to three-row trim bands, repeated across a face. a/b are the trim keys, '.' keeps the cloth.
TRIMS = {
    "line": ["a"],
    "double": ["a", ".", "a"],
    "dots": ["a."],
    "dash": ["aa."],
    "pearls": ["ba"],
    "zigzag": ["a.", ".a"],
    "wave": ["a..a", ".aa."],
    "chevron": ["a...", ".a.a", "..a."],
    "diamond": [".a.", "aba", ".a."],
    "lozenge": ["..a..", ".aba.", "ab.ba", ".aba.", "..a.."],
    "checker": ["ab", "ba"],
    "braid": ["ab.", ".ba"],
    "cross": [".a..", "aaa.", ".a.."],
    "scallop": ["aaa.", "b..b"],
    "ricrac": ["a.a.", ".b.b"],
    "key": ["aaaa", "a..a", "a.aa"],
    "ladder": ["aaaa", "a..a"],
    "stitch": ["a.a.", "...."],
    "vine": [".a..", "abab", "..a."],
    "flowers": [".a...", "aba..", ".a.c."],
    "triangles": ["aaaa", ".aa."],
    "rope": ["ab", "ba", "ab"],
}


def trim(face: Face, y: int, style: str, a: str, b: str | None = None, x0: int = 0, x1: int | None = None,
         offset: int = 0, c: str | None = None):
    """Paint a trim band whose first row is y; returns the number of rows it used."""
    rows = TRIMS[style]
    x1 = face.w - 1 if x1 is None else x1
    keys = {"a": a, "b": b or shade(a, 1), "c": c or shade(a, -1)}
    for dy, row in enumerate(rows):
        for x in range(x0, x1 + 1):
            ch = row[(x + offset) % len(row)]
            if ch in keys:
                face.set(x, y + dy, keys[ch])
    return len(rows)


def band(box, y: int, style: str, a: str, b: str | None = None, c: str | None = None):
    """A trim band wrapped seamlessly around the four sides of a box (or a skin part)."""
    return trim(box.strip, y, style, a, b, c=c)


# Small embroidery motifs: a = main thread, b = highlight, c = stem/shadow, M = metal.
MOTIFS = {
    "flower": [".a.", "aba", ".a."],
    "rose": ["aa.", "aba", ".aa"],
    "tulip": ["a.a", "aaa", ".c."],
    "sprig": [".a.", "aca", ".c."],
    "leaf": [".a", "ac"],
    "star": [".a.", "aba", ".a."],
    "sun": ["a.a", ".b.", "a.a"],
    "bigsun": [".a.a.", "aabaa", ".bMb.", "aabaa", ".a.a."],
    "heart": ["a.a", "aaa", ".a."],
    "cross": [".a.", "aba", ".a.", ".a."],
    "diamond": [".a.", "aba", ".a."],
    "moon": [".aa", "a..", ".aa"],
    "knot": ["aba", "b.b", "aba"],
    "wheat": ["a.a", ".a.", "a.a", ".c."],
    "fish": ["a.a.", "abaa", "a.a."],
    "shell": [".a.", "aba", "aaa"],
    "lily": ["a.a", ".a.", "aba", ".c."],
    "acorn": [".c.", "aaa", ".a."],
    "bee": ["b.b", "aca", ".a."],
    "eye": [".a.", "aMa", ".a."],
    "rune": ["a.", "aa", "a.", "a."],
    "drop": [".a.", "aba", "aaa"],
    "bird": ["a...", ".aaa", "..a."],
    "berry": ["c.", "aa", "aa"],
    "spiral": ["aaa", "..a", "a.a", "aaa"],
}


def motif(face: Face, x: int, y: int, name: str, a: str = "A2", b: str | None = None, c: str | None = None,
          m: str = "M3"):
    grid(face, x, y, MOTIFS[name], {"a": a, "b": b or shade(a, 1), "c": c or "L2", "M": m})


def scatter(face: Face, name: str, a: str, b: str | None = None, step=(4, 4), x0: int = 0, y0: int = 0,
            y1: int | None = None, stagger: bool = True, c: str | None = None):
    """An all-over embroidered pattern: the motif repeated on a staggered grid."""
    h = len(MOTIFS[name])
    w = len(MOTIFS[name][0])
    y1 = face.h - 1 if y1 is None else y1
    row = 0
    for y in range(y0, y1 - h + 2, step[1]):
        shift = (step[0] // 2) if stagger and row % 2 else 0
        for x in range(x0 - step[0] + shift, face.w, step[0]):
            for dy, line in enumerate(MOTIFS[name]):
                for dx, ch in enumerate(line):
                    if ch == "." or not (0 <= x + dx < face.w):
                        continue
                    face.set(x + dx, y + dy, {"a": a, "b": b or shade(a, 1), "c": c or shade(a, -1), "M": "M3"}[ch])
        row += 1


def stripes(face: Face, keys, period: int = 2, vertical: bool = False, x0: int = 0, y0: int = 0,
            w: int | None = None, h: int | None = None, offset: int = 0):
    """Repeat a list of keys as stripes (horizontal by default)."""
    w = face.w - x0 if w is None else w
    h = face.h - y0 if h is None else h
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            i = ((x if vertical else y) + offset) // period
            key = keys[i % len(keys)]
            if key:
                face.set(x, y, key)


def checks(face: Face, a: str, b: str, size: int = 2, c: str | None = None, offset: int = 0):
    """Woven checks: a ground, b where one band crosses, c where two cross."""
    c = c or shade(b, -1)
    for y in range(face.h):
        for x in range(face.w):
            bx, by = ((x + offset) // size) % 2, (y // size) % 2
            face.set(x, y, c if bx and by else b if bx or by else a)


def tartan(face: Face, role: str = "P", line: str = "A2", offset: int = 0, period: int = 6):
    """A sett: dark crossing bands with a thin accent line, in the outfit's colors."""
    for y in range(face.h):
        for x in range(face.w):
            gx, gy = (x + offset) % period, y % period
            bx, by = gx < 2, gy < 2
            key = k(role, 0) if bx and by else k(role, 1) if bx or by else k(role, 2)
            if (gx == period - 2 or gy == period - 2) and not (bx or by):
                key = line
            face.set(x, y, key)


def pleats(face: Face, role: str, base: int = 2, step: int = 2, x0: int = 0, y0: int = 0, y1: int | None = None,
           lit: bool = True, offset: int = 0):
    """Knife pleats: a shaded fold every `step` columns with a lit edge beside it."""
    y1 = face.h - 1 if y1 is None else y1
    for x in range(x0, face.w):
        phase = (x - x0 + offset) % step
        if phase == 0:
            face.vline(x, y0, y1, k(role, base - 1))
        elif lit and phase == step - 1 and step > 2:
            face.vline(x, y0, y1, k(role, base + 1))


def gathers(face: Face, role: str, base: int = 2, y0: int = 0, y1: int = 1):
    """Gathered cloth under a band: short alternating folds."""
    for y in range(y0, y1 + 1):
        for x in range(face.w):
            face.set(x, y, k(role, base - 1) if (x + face.x0) % 2 else k(role, base + (1 if y == y0 else 0)))


def lozenges(face: Face, x0: int, y0: int, w: int, h: int, ground: str, line: str, dark: str | None = None):
    """A brocade panel: ground cloth under a diamond lattice, a darker pip in each diamond."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            dx, dy = x - x0, y - y0
            on = (dx + dy) % 4 == 0 or (dx - dy) % 4 == 0
            key = line if on else ground
            if dark and not on and (dx + dy) % 4 == 2 and (dx - dy) % 4 == 2:
                key = dark
            face.set(x, y, key)


def smocking(face: Face, role: str, base: int = 2, x0: int = 0, y0: int = 0, w: int | None = None, h: int = 3):
    """Honeycomb smocking: a lattice of tacked stitches."""
    w = face.w - x0 if w is None else w
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            d = (x + (y - y0) * 1) % 4 if (y - y0) % 2 == 0 else (x + 2) % 4
            face.set(x, y, k(role, base - 1) if d == 0 else k(role, base + 1) if d == 2 else k(role, base))


def fur(face: Face, role: str = "S", seed: int = 0, base: int = 3):
    """Soft fur tufts: highlights over shaded roots."""
    for y in range(face.h):
        for x in range(face.w):
            r = rnd(x + face.x0, y + face.y0, seed)
            face.set(x, y, k(role, base + 1) if r > .68 else k(role, base - 1) if r < .22 else k(role, base))


def fur_box(box, role: str = "S", seed: int = 0, base: int = 3):
    for f in box.faces:
        fur(f, role, seed, base)


def mail(face: Face, role: str = "M", base: int = 2, y0: int = 0, y1: int | None = None):
    """Riveted mail: rows of lit ring tops over shaded ring bottoms, each row offset by half a ring."""
    y1 = face.h - 1 if y1 is None else y1
    for y in range(y0, y1 + 1):
        for x in range(face.w):
            gx = x + face.x0
            if y % 2 == 0:
                face.set(x, y, k(role, base + 1) if gx % 2 == 0 else k(role, base))
            else:
                face.set(x, y, k(role, base - 1) if gx % 2 == 1 else k(role, base))


def quilt_lines(face: Face, role: str, base: int = 2, step: int = 2, x0: int = 0, y0: int = 0, y1: int | None = None):
    """Vertical channel quilting (gambesons and padded jacks)."""
    y1 = face.h - 1 if y1 is None else y1
    for x in range(x0, face.w):
        if (x - x0) % step == 0:
            face.vline(x, y0, y1, k(role, base - 1))
        elif (x - x0) % step == 1 and step > 2:
            face.vline(x, y0, y1, k(role, base + 1))


def dags(face: Face, y: int, role: str, base: int = 2, step: int = 2, style: str = "square"):
    """Dagged edge on a 3D piece's last rows: the cuts are drawn as deep shade."""
    for x in range(face.w):
        cut = (x % step) == step - 1
        if style == "square":
            face.set(x, y, k(role, base - 2) if cut else k(role, base))
        elif style == "leaf":
            face.set(x, y, k(role, base - 2) if cut else k(role, base + 1 if x % step == 0 else base))
            if y + 1 < face.h:
                face.set(x, y + 1, k(role, base - 2) if not (x % step == step // 2 - 1 or step == 2 and not cut) else k(role, base - 1))


def overlay_dags(face: Face, y: int, step: int = 2, depth: int = 1, phase: int = 0):
    """Dagged edge on a skin overlay (jacket, sleeve, pants): cut real gaps out of the last rows."""
    for x in range(face.w):
        if (x + phase) % step == step - 1:
            for d in range(depth):
                face.clear(x, y + d)


def splotch(face: Face, key: str, seed: int, count: int = 3, y0: int = 0, y1: int | None = None, size: int = 2):
    """A few deliberate stains (dye, flour, ale): small clustered blots, not noise."""
    y1 = face.h - 1 if y1 is None else y1
    for i in range(count):
        cx = int(rnd(i, 1, seed) * face.w)
        cy = y0 + int(rnd(i, 2, seed) * max(1, y1 - y0 + 1))
        for dx in range(size):
            for dy in range(size):
                if rnd(i * 7 + dx, dy, seed) < .75 and face.get(cx + dx, cy + dy):
                    face.set(cx + dx, cy + dy, key)


# -- necklines, chemises and bodices -----------------------------------------------------------
NECKS = {
    "round": [(3, 0), (4, 0)],
    "scoop": [(2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1)],
    "square": [(2, 0), (3, 0), (4, 0), (5, 0), (2, 1), (3, 1), (4, 1), (5, 1)],
    "deep_square": [(x, y) for x in range(2, 6) for y in range(3)],
    "wide": [(x, 0) for x in range(1, 7)],
    "boat": [(x, 0) for x in range(1, 7)] + [(3, 1), (4, 1)],
    "v": [(2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (3, 2), (4, 2), (4, 3)],
    "deep_v": [(x, 0) for x in range(1, 7)] + [(x, 1) for x in range(2, 6)] + [(3, 2), (4, 2), (3, 3), (4, 3)],
    "sweetheart": [(x, 0) for x in range(1, 7)] + [(1, 1), (2, 1), (5, 1), (6, 1)],
    "keyhole": [(3, 0), (4, 0), (3, 1)],
    "slit": [(3, 0), (4, 0), (4, 1), (4, 2)],
    "high": [],
}


def neck(face: Face, style: str, role: str, base: int = 2, edge: str | None = None):
    """Cut a neckline out of a body or jacket front; `edge` paints a finished edge just below it."""
    cut = NECKS[style]
    for x, y in cut:
        face.clear(x, y)
    if edge:
        cells = set(cut)
        for x, y in cut:
            for nx, ny in ((x, y + 1), (x - 1, y), (x + 1, y)):
                if (nx, ny) not in cells and face.inside(nx, ny) and face.get(nx, ny):
                    face.set(nx, ny, edge)
    return cut


def chemise(g, role: str = "S", base: int = 3, texture: str = "weave", seed: int = 0, neckline: str = "scoop",
            sleeve_rows=(0, 11), cuff: str | None = None, gather: bool = True, edge: str | None = None):
    """The linen shift worn under everything: torso, a gathered neckline and full sleeves."""
    body = g.part("body")
    strip_fabric(body, role, texture, seed, base)
    fabric(body.top, role, texture, seed, base + 1)
    fabric(body.bottom, role, texture, seed + 1, base - 1)
    neck(body.front, neckline, role, base, edge or k(role, base + 1))
    if gather:
        for face in (body.front, body.back):
            for x in range(face.w):
                if face.get(x, 1 if face is body.back else 2) and x % 2:
                    face.set(x, 1 if face is body.back else 2, k(role, base - 1))
    arms = []
    if sleeve_rows:
        for side in SIDES:
            arm = g.part(f"{side}_arm")
            strip_fabric(arm, role, texture, seed + 3 + (side == "left"), base, sleeve_rows[0], sleeve_rows[1])
            if sleeve_rows[0] == 0:
                fabric(arm.top, role, texture, seed, base + 1)
            if cuff:
                arm.strip.hline(0, arm.strip.w - 1, sleeve_rows[1], cuff)
            arms.append(arm)
    return body, arms


def bodice(g, role: str, texture: str = "weave", seed: int = 0, base: int = 2, rows=(1, 9), neckline: str | None = None,
           straps: bool = True, point: bool = False, layer: str = "jacket", edge: str | None = None,
           back_rows=None, seams: bool = True):
    """A fitted bodice over the chemise. With straps it covers the shoulders; a point dips at the waist."""
    box = g.part(layer)
    y0, y1 = rows
    by0, by1 = back_rows or rows
    for face, (a, b) in ((box.front, rows), (box.back, (by0, by1)), (box.right, rows), (box.left, rows)):
        fabric(face, role, texture, seed + face.x0, base, 0, a, face.w, b - a + 1)
    if straps and y0 > 0:
        for face in (box.front, box.back):
            for x in (0, 1, 6, 7):
                face.vline(x, 0, y0 - 1, k(role, base))
        for face in (box.right, box.left):
            face.hline(0, face.w - 1, 0, k(role, base))
            for y in range(1, y0):
                face.hline(0, face.w - 1, y, k(role, base))
        for x in (0, 1, 6, 7):
            box.top.vline(x, 0, box.top.h - 1, k(role, base + 1))
    elif y0 == 0:
        fabric(box.top, role, texture, seed, base + 1)
    if neckline:
        neck(box.front, neckline, role, base, edge)
    if point:
        box.front.hline(2, 5, y1 + 1, k(role, base - 1))
        box.front.hline(3, 4, y1 + 2, k(role, base - 1))
    if seams:
        for face in (box.right, box.left):
            face.vline(2, max(1, y0), y1, k(role, base - 1))
    for face in box.sides:
        face.hline(0, face.w - 1, y1 if face is not box.back else by1, k(role, base - 1))
    return box


def lacing(face: Face, x: int, y0: int, y1: int, style: str = "x", lace: str = "L3", under: str | None = "S3",
           eyelet: str | None = "M3", edge: str | None = None):
    """Front lacing in columns x and x+1, eyelets at x-1 and x+2.

    Styles: x (criss-cross over a gap), ladder (straight bars), spiral (one diagonal lace), tight (closed seam).
    """
    for y in range(y0, y1 + 1):
        i = y - y0
        if style == "x":
            face.set(x, y, lace if i % 2 == 0 else under or shade(lace, -2))
            face.set(x + 1, y, lace if i % 2 == 1 else under or shade(lace, -2))
        elif style == "ladder":
            key = lace if i % 2 == 0 else under or shade(lace, -2)
            face.set(x, y, key), face.set(x + 1, y, key)
        elif style == "spiral":
            face.set(x, y, lace if i % 2 == 0 else under or shade(lace, -2))
            face.set(x + 1, y, lace if i % 2 == 1 else shade(lace, -1))
        elif style == "tight":
            face.set(x, y, shade(lace, -1)), face.set(x + 1, y, lace if i % 2 == 0 else shade(lace, -1))
        if edge:
            face.set(x - 1, y, edge), face.set(x + 2, y, edge)
        if eyelet and i % 2 == 0:
            face.set(x - 1, y, eyelet), face.set(x + 2, y, eyelet)


def side_lacing(box, y0: int, y1: int, lace: str = "L3", under: str = "S3"):
    """Lacing up both sides of the torso (the right and left faces)."""
    for face in (box.right, box.left):
        for y in range(y0, y1 + 1):
            face.set(1, y, lace if (y - y0) % 2 == 0 else under)
            face.set(2, y, under if (y - y0) % 2 == 0 else lace)


def buttons(face: Face, x: int, y0: int, y1: int, key: str = "M3", step: int = 1, placket: str | None = None):
    for y in range(y0, y1 + 1):
        if placket:
            face.set(x, y, placket)
        if (y - y0) % step == 0:
            face.set(x, y, key)


# -- sleeves -----------------------------------------------------------------------------------
def arm_rings(g, prefix: str, y: float, h: int, size: int = 5, depth: int | None = None, inflate: float = 0.0,
              dz: float = 0.0, rotation=(0, 0, 0)):
    """A box around each arm at arm-local height y (shoulder top is y -2, wrist about y 9)."""
    boxes = []
    d = depth or size
    for side in SIDES:
        x = arm_x(side) - (size - 4) / 2
        rot = rotation if side == "right" else (rotation[0], -rotation[1], -rotation[2])
        boxes.append(g.piece(f"{side}_{prefix}", arm_bone(side), (x, y, -d / 2 + dz), (size, h, d), inflate=inflate,
                             rotation=rot))
    return boxes


def puffs(g, role: str, texture: str = "weave", seed: int = 0, base: int = 3, y: float = -2.4, h: int = 4,
          size: int = 5, prefix: str = "puff", band_key: str | None = None, slash: str | None = None):
    """Puffed shoulder sleeves: gathered folds, a lit crown and a band where they meet the arm."""
    boxes = arm_rings(g, prefix, y, h, size, inflate=.12)
    for box in boxes:
        solid(box, role, texture, seed, base)
        for face in box.sides:
            for x in range(face.w):
                if x % 2:
                    face.vline(x, 1, h - 2, k(role, base - 1))
                elif slash:
                    face.vline(x, 1, h - 2, slash)
            if band_key:
                face.hline(0, face.w - 1, h - 1, band_key)
        fabric(box.top, role, texture, seed, base + 1)
    return boxes


def bells(g, role: str, texture: str = "weave", seed: int = 0, base: int = 2, y: float = 4.0, h: int = 6,
          size: int = 6, prefix: str = "bell", lining: str | None = None, flare: float = 0):
    """Wide bell or trumpet sleeves hanging from the forearm; the open bottom shows the lining."""
    boxes = arm_rings(g, prefix, y, h, size, inflate=.05)
    for box in boxes:
        solid(box, role, texture, seed, base)
        box.bottom.fill(lining or k(role, base - 2))
    return boxes


def tippets(g, role: str, y: float = 3.5, length: int = 8, key_end: str | None = None, prefix: str = "tippet",
            width: int = 2):
    """Long streamers hanging behind the elbows (cotehardie tippets); they sway as she walks."""
    boxes = []
    for side in SIDES:
        x = arm_x(side) + (4 - width) / 2
        box = g.piece(f"{side}_{prefix}", arm_bone(side), (x, 0, 0), (width, length, 1), pivot=(0, y, 2.2), motion="sway")
        solid(box, role, "plain", 91 + (side == "left"), 2)
        if key_end:
            box.strip.hline(0, box.strip.w - 1, length - 1, key_end)
        boxes.append(box)
    return boxes


def cuffs(g, role: str, y: float = 8.0, h: int = 2, size: int = 5, prefix: str = "cuff", texture: str = "plain",
          base: int = 2, inflate: float = .05):
    boxes = arm_rings(g, prefix, y, h, size, inflate=inflate)
    for box in boxes:
        solid(box, role, texture, 95, base, edge=False)
        for face in box.sides:
            face.hline(0, face.w - 1, 0, k(role, base + 1))
    return boxes


# -- over-layers, belts, cloaks ----------------------------------------------------------------
def over_panel(g, pid: str, length: int, role: str, texture: str = "weave", seed: int = 0, base: int = 2,
               width: int = 10, top: float = 9.0, back: bool = False, x: float = 0.0, motion: bool = True,
               rotation=(0, 0, 0)):
    """One over-layer panel in front of (or behind) any skirt; returns its outward face."""
    if top > OVER_TOP_MAX:
        raise ValueError(f"{pid}: over-layers hinge at or above y {OVER_TOP_MAX}")
    z = OVER_BACK if back else OVER_FRONT
    mot = ("flap_back" if back else "flap_front") if motion else "none"
    box = g.piece(pid, "TORSO", (-width / 2, 0, 0), (width, length, 1), pivot=(x, top, z), motion=mot, rotation=rotation)
    solid(box, role, texture, seed, base)
    face = box.back if back else box.front
    face.hline(0, width - 1, 0, k(role, base + 1))
    return face


def over_flaps(g, prefix: str, length: int, role: str, texture: str = "weave", seed: int = 0, base: int = 2,
               width: int = 10, top: float = 9.0, back_length: int | None = None, hem: str | None = None):
    """Front and back over-layer panels (coat skirts, overdress panels, tabards); returns both faces."""
    f = over_panel(g, f"{prefix}_front", length, role, texture, seed, base, width, top)
    b = over_panel(g, f"{prefix}_back", back_length or length, role, texture, seed + 1, base, width, top, back=True)
    if hem:
        f.hline(0, f.w - 1, f.h - 1, hem)
        b.hline(0, b.w - 1, b.h - 1, hem)
    return f, b


def girdle(g, pid: str = "girdle", y: float = 7.6, role: str = "L", base: int = 2, height: int = 1,
           buckle: str | None = "M", texture: str | None = None, inflate: float = .05, wide: bool = False):
    """A belt at the natural waist, above every skirt. `wide` also encloses over-layer panels."""
    if wide:
        box = g.piece(pid, "TORSO", (-5.2, y, -3.25), (10, height, 6), inflate=inflate)
    else:
        box = g.piece(pid, "TORSO", (-4.6, y, -2.6), (9, height, 5), inflate=inflate)
    solid(box, role, texture or ("leather" if role == "L" else "weave"), 33, base, edge=False)
    for face in box.sides:
        face.hline(0, face.w - 1, 0, k(role, base + 1))
    if buckle:
        mid = box.front.w // 2
        if height >= 2:
            grid(box.front, mid - 1, 0, ["mmm", "m.m"], {"m": k(buckle, 3)})
        else:
            box.front.set(mid, 0, k(buckle, 3))
    return box


def hanging(g, pid: str, x: float, length: int, role: str = "L", base: int = 2, width: int = 1, top: float = 8.6,
            back: bool = False, end: str | None = None, texture: str = "plain"):
    """A girdle end, chain or ribbon hanging down the front (or back), riding the stride like an over-layer."""
    z = (OVER_BACK + .05) if back else (OVER_FRONT - .1)
    box = g.piece(pid, "TORSO", (-width / 2, 0, 0), (width, length, 1), pivot=(x, min(top, OVER_TOP_MAX), z),
                  motion="flap_back" if back else "flap_front")
    solid(box, role, texture, 97, base)
    if end:
        box.strip.hline(0, box.strip.w - 1, length - 1, end)
    return box


def cloak(g, prefix: str, role: str, texture: str = "weave", seed: int = 0, base: int = 2, width: int = 10,
          length: int = 11, tail: int = 0, top: float = -0.4, z: float = 2.55, tilt: float = 4.0):
    """A cloak down the back: a still upper part from the shoulders and an optional lower tail that rides
    the trailing leg. Returns (upper back face, tail back face or None)."""
    import math
    upper = g.piece(f"{prefix}_back", "TORSO", (-width / 2, 0, 0), (width, length, 1), pivot=(0, top, z),
                    rotation=(tilt, 0, 0))
    solid(upper, role, texture, seed, base)
    lower_face = None
    if tail:
        a = math.radians(tilt)
        py, pz = top + length * math.cos(a) - .15, z + length * math.sin(a)
        lower = g.piece(f"{prefix}_tail", "TORSO", (-width / 2, 0, 0), (width, tail, 1), pivot=(0, py, pz),
                        rotation=(tilt, 0, 0), motion="flap_back")
        solid(lower, role, texture, seed + 1, base)
        lower_face = lower.back
    return upper.back, lower_face


def mantle(g, pid: str, role: str, texture: str = "weave", seed: int = 0, base: int = 2, height: int = 4,
           width: int = 17, depth: int = 6, y: float = -.6, inflate: float = .04):
    """A shoulder cape over both arms (capelets, tippets, pelerines)."""
    box = g.piece(pid, "TORSO", (-width / 2, y, -depth / 2 + .2), (width, height, depth), inflate=inflate)
    solid(box, role, texture, seed, base)
    fabric(box.top, role, texture, seed, base + 1)
    return box


def hood_down(g, prefix: str, role: str, texture: str = "weave", seed: int = 0, base: int = 2, lining: str | None = None,
              point: int = 0):
    """A hood lying back on the shoulders, with an optional pointed tail (liripipe)."""
    hood = g.piece(f"{prefix}", "TORSO", (-3.5, 0, 0), (7, 3, 2), pivot=(0, -.5, 2.3), rotation=(14, 0, 0))
    solid(hood, role, texture, seed, base)
    fabric(hood.top, role, texture, seed, base + 1)
    if lining:
        hood.top.hline(0, 6, 1, lining)
        hood.top.hline(0, 6, 0, lining)
    hood.back.vline(3, 0, 2, k(role, base - 1))
    if point:
        tip = g.piece(f"{prefix}_point", "TORSO", (-1, 0, 0), (2, point, 1), pivot=(0, 2.0, 3.2), rotation=(10, 0, 0),
                      motion="sway")
        solid(tip, role, texture, seed + 2, base)
    return hood


def brooch(g, pid: str, pivot, size=(2, 2, 1), metal: str = "M", gem: str | None = "A2"):
    w, h, d = size
    box = g.piece(pid, "TORSO", (-w / 2, -h / 2, -d / 2), size, pivot=pivot, inflate=.04)
    solid(box, metal, "smooth", 99, 3, edge=False)
    if gem:
        box.front.set(w // 2, h // 2, gem)
    box.front.set(0, 0, k(metal, 4))
    return box


# -- legwear for skirts and trousers ------------------------------------------------------------
class Skirt:
    """What skirt() built: decorate `faces` (front, right, left, back panels as seen from outside)."""

    def __init__(self, front, back, right, left, top, length, back_length, side_length, role, base):
        self.front, self.back, self.right, self.left = front, back, right, left
        self.top, self.length, self.back_length, self.side_length = top, length, back_length, side_length
        self.role, self.base = role, base

    @property
    def faces(self):
        out = [self.front.front, self.back.back]
        if self.right:
            out += [self.right.right, self.left.left]
        return out

    @property
    def wide_faces(self):
        """Faces wide enough for patterns (front and back panels)."""
        return [self.front.front, self.back.back]

    def band(self, y: int, style: str, a: str, b: str | None = None, from_bottom: bool = False, c: str | None = None):
        """A trim around the skirt; with from_bottom, y counts up from each panel's hem."""
        for face in self.faces:
            yy = face.h - 1 - y if from_bottom else y
            trim(face, yy, style, a, b, c=c)
        for box in (self.right, self.left):
            if box:
                for face in (box.front, box.back):
                    yy = face.h - 1 - y if from_bottom else y
                    trim(face, yy, style, a, b, c=c)

    def hem(self, key: str, rows: int = 1):
        for face in self.faces:
            for r in range(rows):
                face.hline(0, face.w - 1, face.h - 1 - r, key)
        for box in (self.right, self.left):
            if box:
                for face in (box.front, box.back):
                    for r in range(rows):
                        face.hline(0, face.w - 1, face.h - 1 - r, key)

    def pleat(self, step: int = 2, y0: int = 1, lit: bool = True):
        for face in self.faces:
            pleats(face, self.role, self.base, step, y0=y0, lit=lit)

    def paint(self, fn, sides: bool = True):
        """fn(face) for every outward face; sides include the narrow edges of the side panels."""
        for face in self.faces:
            fn(face)
        if sides and self.right:
            for box in (self.right, self.left):
                fn(box.front), fn(box.back)


def skirt(g, role: str, texture: str = "weave", seed: int = 0, base: int = 2, top: float = 9.8, length: int = 12,
          back_length: int | None = None, side_length: int | None = None, width: int = 10, flare: float = 5,
          body_rows=(9, 11), inner: int | None = None, prefix: str = "skirt", sides: bool = True,
          gather: bool = True, folds: bool = True) -> Skirt:
    """A skirt from the hips: cloth on the hips and legs, front/back panels that ride the stride and
    flared side panels. Floor length is top 10 + length 12; knee length is about length 7."""
    if not (SKIRT_TOP_MIN <= top <= SKIRT_TOP_MAX):
        raise ValueError(f"skirt panels hang from y {SKIRT_TOP_MIN}..{SKIRT_TOP_MAX}")
    back_length = back_length or length
    side_length = side_length or min(length, back_length)
    body = g.part("body")
    strip_fabric(body, role, texture, seed, base, body_rows[0], body_rows[1])
    for face in body.sides:
        face.hline(0, face.w - 1, body_rows[0], k(role, base + 1))
    fabric(body.bottom, role, texture, seed + 1, base - 1)
    inner_base = base - 1 if inner is None else inner
    hem_y = top + min(length, back_length, side_length)
    last = min(11, int(hem_y - 12.5))
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        if last >= 0:
            strip_fabric(leg, role, texture, seed + 3, inner_base, 0, last)
            fabric(leg.top, role, texture, seed, inner_base)
    front = g.piece(f"{prefix}_front", "TORSO", (-width / 2, 0, 0), (width, length, 1), pivot=(0, top, SKIRT_FRONT),
                    motion="flap_front")
    back = g.piece(f"{prefix}_back", "TORSO", (-width / 2, 0, 0), (width, back_length, 1), pivot=(0, top, SKIRT_BACK),
                   motion="flap_back")
    solid(front, role, texture, seed + 5, base)
    solid(back, role, texture, seed + 6, base)
    right = left = None
    if sides:
        right = g.piece(f"{prefix}_right", "TORSO", (0, 0, -2.5), (1, side_length, 5), pivot=(-5.1, top, 0),
                        rotation=(0, 0, flare))
        left = g.piece(f"{prefix}_left", "TORSO", (-1, 0, -2.5), (1, side_length, 5), pivot=(5.1, top, 0),
                       rotation=(0, 0, -flare))
        solid(right, role, texture, seed + 7, base)
        solid(left, role, texture, seed + 8, base)
    s = Skirt(front, back, right, left, top, length, back_length, side_length, role, base)
    for face in s.faces:
        face.hline(0, face.w - 1, 0, k(role, base + 1))
        if gather:
            for x in range(face.w):
                if x % 2:
                    face.set(x, 1, k(role, base - 1))
    if folds:
        for face in s.wide_faces:
            for x in range(2, face.w - 1, 4):
                face.vline(x, 3, face.h - 3, k(role, base - 1))
                if face.h > 9:
                    face.vline(x + 1, 5, face.h - 4, k(role, base + 1))
    return s


def tier(g, s: Skirt, pid: str, y: int, h: int, role: str | None = None, texture: str = "weave", seed: int = 0,
         base: int | None = None, grow: int = 2, sides: bool = True, flare: float | None = None):
    """A wider flounce on the lower skirt: front/back boxes that share the panels' hinges, plus side boxes.
    Returns the outward faces [front, back, right, left]."""
    role = role or s.role
    base = s.base if base is None else base
    width = s.front.w + grow
    out = []
    for name, ref, z, mot in (("front", s.front, SKIRT_FRONT, "flap_front"), ("back", s.back, SKIRT_BACK, "flap_back")):
        box = g.piece(f"{pid}_{name}", "TORSO", (-width / 2, y, -.08 if name == "front" else .08), (width, h, 1),
                      pivot=(0, s.top, z), motion=mot, inflate=.04)
        solid(box, role, texture, seed + len(out), base)
        out.append(box.front if name == "front" else box.back)
    if sides and s.right:
        fl = flare if flare is not None else 7
        # Just outside the skirt's own side panels, hinged at the same point but flared a little more.
        for side, x, ox, rot in (("right", -5.1, -.4, fl), ("left", 5.1, -.6, -fl)):
            box = g.piece(f"{pid}_{side}", "TORSO", (ox, y, -2.7), (1, h, 5), pivot=(x, s.top, 0),
                          rotation=(0, 0, rot), inflate=.04)
            solid(box, role, texture, seed + 5, base)
            out.append(box.right if side == "right" else box.left)
    return out


def shoes(g, style: str = "turnshoe", role: str = "L", base: int = 2, top: int | None = None, toe: str | None = None,
          sole: str = "K1", accent: str | None = None):
    """Footwear for skirts and trousers. Styles: turnshoe, shoe, boot, clog (kit) plus pointed (poulaine),
    ankle (laced ankle boot), slipper (cloth), patten (wooden overshoe), sandal (straps on bare feet)."""
    if style in ("turnshoe", "shoe", "boot", "clog"):
        footwear(g, style, top=top if top is not None else {"boot": 8, "turnshoe": 10, "shoe": 10, "clog": 10}[style],
                 role=role, base=base, toe=toe, sole=sole)
        return
    if style == "pointed":
        footwear(g, "shoe", top=top or 10, role=role, base=base, toe=toe, sole=sole)
        for side in SIDES:
            tip = g.piece(f"{side}_shoe_point", leg_bone(side), (-1, 0, -2), (2, 1, 2), pivot=(0, 11.0, -2.1))
            solid(tip, role, "smooth", 61, base, edge=False)
            tip.top.set(0, 1, k(role, base + 1)), tip.top.set(1, 1, k(role, base + 1))
            tip.bottom.fill(sole)
    elif style == "ankle":
        footwear(g, "boot", top=top or 9, role=role, base=base, toe=toe, sole=sole)
        for side in SIDES:
            pants = g.part(f"{side}_pants")
            pants.front.set(1, (top or 9) + 1, accent or k(role, base + 2))
            pants.front.set(2, (top or 9) + 1, accent or k(role, base + 2))
            pants.front.set(1, (top or 9), k(role, base - 1)), pants.front.set(2, (top or 9), k(role, base - 1))
    elif style == "slipper":
        footwear(g, "turnshoe", top=top or 11, role=role, base=base, toe=toe, sole=sole)
    elif style == "patten":
        footwear(g, "turnshoe", top=top or 10, role=role, base=base, toe=toe, sole=sole)
        for side in SIDES:
            pat = g.piece(f"{side}_patten", leg_bone(side), (-2, 0, -2), (4, 1, 4), pivot=(0, 11.6, 0), inflate=.12)
            solid(pat, "L", "smooth", 62, 3, edge=False)
            pat.bottom.fill("L0")
            for face in pat.sides:
                face.set(0, 0, "M3"), face.set(face.w - 1, 0, "M3")
    elif style == "sandal":
        for side in SIDES:
            leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
            for face in pants.sides:
                face.hline(0, face.w - 1, 11, k(role, base - 1))
                face.set(1, 10, k(role, base)), face.set(2, 9, k(role, base))
            leg.strip.hline(0, leg.strip.w - 1, 11, k(role, base - 1))
            leg.bottom.fill(k(role, 0)), pants.bottom.fill(k(role, 0))
    else:
        raise ValueError(style)


def hose(g, role: str, rows=(0, 11), base: int = 2, texture: str = "knit", seed: int = 0, seam: bool = True):
    """Fitted knitted or cut-cloth hose on the bare leg."""
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, role, texture, seed + (side == "left"), base, rows[0], rows[1])
        if rows[0] == 0:
            fabric(leg.top, role, texture, seed, base)
        if seam:
            leg.back.vline(1 if side == "right" else 2, rows[0], rows[1], k(role, base - 1))


def leg_rings(g, prefix: str, y: float, h: int, size: int = 5, inflate: float = .04):
    """A box around each leg at leg-local height y (0 is the hip joint, 12 the sole)."""
    return [g.piece(f"{side}_{prefix}", leg_bone(side), (-size / 2, y, -size / 2), (size, h, size), inflate=inflate)
            for side in SIDES]


def leg_ring_fold(g, prefix: str, y: float, role: str = "L", base: int = 2, size: int = 5):
    """Folded-down boot or stocking tops: a lit upper edge over a shaded fold."""
    boxes = leg_rings(g, prefix, y, 2, size, .06)
    for box in boxes:
        solid(box, role, "leather" if role == "L" else "weave", 64, base, edge=False)
        for face in box.sides:
            face.hline(0, face.w - 1, 0, k(role, base + 2)), face.hline(0, face.w - 1, 1, k(role, base))
    return boxes


def stockings_row(g, role: str, y0: int, y1: int | None = None, base: int = 3):
    """Stockings showing between a hem and the shoes: rows y0..y1 of both bare legs."""
    y1 = y0 if y1 is None else y1
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for y in range(y0, y1 + 1):
            leg.strip.hline(0, leg.strip.w - 1, y, k(role, base))


def wraps(face: Face, y0: int, y1: int, role: str = "L", base: int = 2, step: int = 4):
    """Bands wound diagonally around the shin (winingas, puttees)."""
    for y in range(y0, y1 + 1):
        for x in range(face.w):
            d = (2 * y + x // 2) % step
            face.set(x, y, k(role, base + 1) if d == 0 else k(role, base) if d < step - 1 else k(role, base - 1))


def waist_belt(g, pid: str = "waist_belt", y: float = 9.4, role: str = "L", base: int = 2, height: int = 1,
               buckle: str | None = "M", texture: str | None = None):
    """A belt, cord or sash round a skirt's hips, outside the panels. Keep the id starting with 'waist'."""
    box = g.piece(pid, "TORSO", (-5.5, y, -3.05), (11, height, 6), inflate=.05)
    solid(box, role, texture or ("leather" if role == "L" else "weave"), 35, base, edge=False)
    for face in box.sides:
        face.hline(0, face.w - 1, 0, k(role, base + 1))
    if buckle:
        if height >= 2:
            grid(box.front, 4, 0, ["mmm", "m.m"], {"m": k(buckle, 3)})
        else:
            box.front.set(5, 0, k(buckle, 3))
    return box


def side_pouch(g, pid: str, side: str = "left", y: float = 9.6, size=(2, 3, 2), role: str = "L", flap: str | None = None,
               strap: bool = True):
    """A pouch hung from the hip beside the skirt (bottoms: name it waist_... so tops can hide it)."""
    w, h, d = size
    x = 5.5 + w / 2 if side == "left" else -5.5 - w / 2
    box = g.piece(pid, "TORSO", (-w / 2, 0, -d / 2), size, pivot=(x, y, -.4))
    solid(box, role, "leather", 63, 2)
    cap(box, role, top_delta=1)
    for face in box.sides:
        face.hline(0, face.w - 1, 0, k(role, 3))
    if flap:
        box.front.set(w // 2, 1, flap)
    return box
