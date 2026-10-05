"""Shared pixel-art brushes for wardrobe modules. Everything paints key colors (role + shade)."""
from __future__ import annotations

from wardrobe import Box, Face, shade


def rnd(x: int, y: int, seed: int = 0) -> float:
    v = (x * 374761393 + y * 668265263 + seed * 2147483647) & 0xFFFFFFFF
    v = ((v ^ (v >> 13)) * 1274126177) & 0xFFFFFFFF
    v ^= v >> 16
    return (v & 0xFFFF) / 65536


def k(role: str, s: int) -> str:
    return f"{role}{max(0, min(4, s))}"


TEXTURES = ("plain", "weave", "twill", "knit", "rib", "quilt", "leather", "tweed", "velvet", "smooth")


def cloth_shade(texture: str, x: int, y: int, seed: int, base: int = 2) -> int:
    """Calm, structured cloth: textures come from weave patterns, not from random specks."""
    r = rnd(x, y, seed)
    s = base
    if texture == "weave":
        if (x + 2 * y) % 11 == 0 and r < .35:
            s -= 1
        elif r > .99:
            s += 1
    elif texture == "twill":
        if (x + y) % 6 == 0 and r < .3:
            s -= 1
        elif r > .99:
            s += 1
    elif texture == "knit":
        # Stocking stitch: soft V columns, one shaded texel per stitch.
        if x % 3 == 2 and y % 2 == 0:
            s -= 1
        elif x % 3 == 0 and y % 2 == 1 and r < .5:
            s += 1
    elif texture == "rib":
        s -= 1 if x % 2 == 1 else 0
    elif texture == "quilt":
        # Diamond quilting: stitched diagonals every six texels, puffed centres.
        if (x + y) % 6 == 0 or (x - y) % 6 == 0:
            s -= 1
        elif (x + y) % 6 == 3 and (x - y) % 6 == 3:
            s += 1
    elif texture == "leather":
        if r < .025:
            s -= 1
        elif r > .965:
            s += 1
    elif texture == "tweed":
        if r < .12:
            s -= 1
        elif r > .9:
            s += 1
    elif texture == "velvet":
        # Clean pile: a rare catch of light; garments add their own folds and seams.
        if r > .988:
            s += 1
    elif texture == "plain":
        if r < .012:
            s -= 1
        elif r > .99:
            s += 1
    return s


def fabric(face: Face, role: str, texture: str = "plain", seed: int = 0, base: int = 2,
           x0: int = 0, y0: int = 0, w: int | None = None, h: int | None = None, mask=None):
    """Fill a rectangle of a face with a textured cloth role."""
    w = face.w - x0 if w is None else w
    h = face.h - y0 if h is None else h
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            if mask is None or mask(x, y):
                face.set(x, y, k(role, cloth_shade(texture, x + face.x0, y + face.y0, seed, base)))


def strip_fabric(box: Box, role: str, texture: str = "plain", seed: int = 0, base: int = 2,
                 y0: int = 0, y1: int | None = None, mask=None):
    """Cloth around all four sides (the strip), rows y0..y1 inclusive."""
    y1 = box.h - 1 if y1 is None else y1
    fabric(box.strip, role, texture, seed, base, 0, y0, box.strip.w, y1 - y0 + 1, mask)


def cap(box: Box, role: str, top_delta: int = 1, bottom_delta: int = -1, texture="plain", seed=0, base=2):
    fabric(box.top, role, texture, seed, base + top_delta)
    fabric(box.bottom, role, texture, seed + 1, base + bottom_delta)


def solid(box: Box, role: str, texture: str = "plain", seed: int = 0, base: int = 2, edge: bool = True):
    """Fully painted 3D piece: textured sides, lit top, shaded bottom, darker lower edge."""
    strip_fabric(box, role, texture, seed, base)
    cap(box, role, texture=texture, seed=seed, base=base)
    if edge and box.h >= 3:
        box.strip.hline(0, box.strip.w - 1, box.h - 1, k(role, base - 1))


def band(box: Box, y: int, key: str, faces=("right", "front", "left", "back")):
    for f in faces:
        getattr(box, f).hline(0, getattr(box, f).w - 1, y, key)


def hem(box: Box, y: int, role: str, base: int = 2, faces=("right", "front", "left", "back")):
    """A raised two-row hem: light upper edge, shaded lower edge."""
    band(box, y, k(role, base + 1), faces)
    band(box, y + 1, k(role, base - 1), faces)


def dark_seams(box: Box, delta: int = -1, rows=None, faces=("right", "front", "left", "back")):
    """Darken the outer columns of the chosen side faces for roundness."""
    for name in faces:
        f = getattr(box, name)
        for y in (rows if rows is not None else range(f.h)):
            for x in (0, f.w - 1):
                cur = f.get(x, y)
                if cur:
                    f.set(x, y, shade(cur, delta))


def darken_rows(face: Face, rows, delta=-1):
    for y in rows:
        for x in range(face.w):
            cur = face.get(x, y)
            if cur:
                face.set(x, y, shade(cur, delta))


def button(face: Face, x: int, y: int, role="M", base=3):
    face.set(x, y, k(role, base))


def line(face: Face, x0, y0, x1, y1, key):
    """Bresenham line, inclusive."""
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        face.set(x0, y0, key)
        if x0 == x1 and y0 == y1:
            return
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def strip_line(box: Box, points, key):
    """Line on the side strip, wrapping around the cuboid; points in strip coordinates."""
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        steps = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(steps + 1):
            x = round(x0 + (x1 - x0) * i / max(1, steps))
            y = round(y0 + (y1 - y0) * i / max(1, steps))
            box.strip.set(x % box.strip.w, y, key)


# -- hair ------------------------------------------------------------------------------------
def hair_shade(x: int, y: int, h: int, seed: int, base: int = 2, sheen_row: int | None = None,
               clump: int = 2, root_dark: bool = False) -> int:
    """Strand clumps: each clump column gets a tone, gaps between clumps darken, ends darken."""
    c = (x + int(rnd(seed, 3) * 3)) // clump
    tone = rnd(c, 7, seed)
    s = base + (1 if tone > .72 else 0) - (1 if tone < .18 else 0)
    if (x + int(rnd(seed, 3) * 3)) % clump == 0 and rnd(x, y // 2, seed) < .45:
        s -= 1
    if root_dark and y == 0:
        s -= 1
    if y >= h - 1 and h > 2:
        s -= 1
    if sheen_row is not None and y == sheen_row and rnd(x, 11, seed) < .7:
        s = max(s, base + 2 if tone > .4 else base + 1)
    return s


def hair_face(face: Face, seed: int, base: int = 2, sheen_row: int | None = None, clump: int = 2,
              rows=None, cols=None, root_dark=False, fade_bottom=True):
    rows = range(face.h) if rows is None else rows
    cols = range(face.w) if cols is None else cols
    for y in rows:
        for x in cols:
            s = hair_shade(x + face.x0, y, face.h if fade_bottom else face.h + 9, seed, base, sheen_row, clump, root_dark)
            face.set(x, y, k("H", s))


def hair_box(box: Box, seed: int, base: int = 2, sheen_row: int | None = None, clump: int = 2,
             top_delta: int = 1, bottom_delta: int = -2, fade_bottom=True):
    """A solid lock of hair: strands down every side, glossy top, dark underside."""
    for f in box.sides:
        hair_face(f, seed + f.x0, base, sheen_row, clump, fade_bottom=fade_bottom)
    for y in range(box.top.h):
        for x in range(box.top.w):
            box.top.set(x, y, k("H", base + top_delta - (1 if rnd(x, y, seed + 5) < .2 else 0)))
    box.bottom.fill(k("H", base + bottom_delta))


def grid(face: Face, x0: int, y0: int, rows: list[str], legend: dict):
    """Stamp a small pixel pattern; '.' or ' ' leaves the pixel unchanged."""
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch in ".  ":
                continue
            face.set(x0 + dx, y0 + dy, legend[ch])


def mirror_grid(rows: list[str]) -> list[str]:
    return [row[::-1] for row in rows]


def rivets(face: Face, y: int, role: str = "M", step: int = 2, start: int = 0, base: int = 3):
    for x in range(start, face.w, step):
        face.set(x, y, k(role, base))


def scalp(g, seed: int, side_rows: int = 4, back_rows: int = 7, sideburn: int = 2, part: int | None = None,
          base: int = 2, shadow: bool = True):
    """Hair painted on the head itself: crown, back, sides with sideburns, hairline and its shadow."""
    head = g.part("head")
    hair_face(head.top, seed, base)
    if part is not None:
        head.top.vline(part, 0, 7, k("H", base - 2))
        head.top.vline(min(7, part + 1), 0, 7, k("H", base + 1))
    hair_face(head.back, seed + 1, base, rows=range(back_rows))
    if back_rows < 8:
        for x in range(8):
            if rnd(x, back_rows, seed) < .5:
                head.back.set(x, back_rows, k("H", base - 1))
    hair_face(head.right, seed + 2, base, rows=range(side_rows))
    hair_face(head.left, seed + 3, base, rows=range(side_rows))
    for y in range(side_rows, min(8, side_rows + sideburn)):
        head.right.set(7, y, k("H", base - 1)), head.left.set(0, y, k("H", base - 1))
    head.front.hline(0, 7, 0, k("H", base - 1))
    if shadow:
        for x in range(1, 7):
            head.front.set(x, 1, "X1")
    head.front.set(0, 1, k("H", base - 1)), head.front.set(7, 1, k("H", base - 1))


def shell(g, seed: int, side_rows: int = 2, back_rows: int = 5, base: int = 2, sheen: int | None = 1,
          front: list | None = None, top: bool = True):
    """Hair on the half-pixel hat layer: volume with ragged lower edges; `front` lists (x, y) fringe texels."""
    hat = g.part("hat")
    if top:
        hair_face(hat.top, seed, base + 1)
        hat.top.hline(0, 7, 7, k("H", base + 1))
    for face, rows in ((hat.back, back_rows), (hat.right, side_rows), (hat.left, side_rows)):
        if rows <= 0:
            continue
        hair_face(face, seed + face.x0, base, sheen_row=sheen if rows > 2 else None, rows=range(rows))
        if rows < 8:
            for x in range(face.w):
                if rnd(x, rows, seed + 7) < .5:
                    face.set(x, rows, k("H", base - 1))
    hat.front.hline(0, 7, 0, k("H", base))
    for x, y in front or []:
        hat.front.set(x, y, k("H", base - (1 if y > 1 else 0)))


def curls_face(face: Face, seed: int, base: int = 2):
    """Tight coils: 3x3 clusters with a bright core and shaded corners, rows of clusters offset."""
    cell = [[-1, 0, -1], [0, 1, 0], [-1, 0, 0]]
    for y in range(face.h):
        for x in range(face.w):
            row = y // 3
            shift = (row * 2 + seed) % 3
            col = (x + shift) // 3
            lx, ly = (x + shift) % 3, y % 3
            tone = rnd(col, row, seed)
            s = base + cell[ly][lx] + (1 if tone > .72 else 0) - (1 if tone < .2 else 0)
            face.set(x, y, k("H", s))


def curls_box(box: Box, seed: int, base: int = 2):
    for f in box.sides:
        curls_face(f, seed + f.x0, base)
    curls_face(box.top, seed + 3, base + 1)
    box.bottom.fill(k("H", base - 2))
