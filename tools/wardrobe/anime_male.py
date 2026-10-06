"""Brushes for the male hairstyles from h31 on: clipped and faded scalps, combed plates, bending
locks, plaits and cornrows, twists, coils and ringlets, waves and ties.

They follow anime.py: clean cel shading, a sheen ring on the first segment of a lock, pointed
tips. Like kit.py and anime.py they paint key colors only and return the boxes they create, so a
module can add its own details on top. Faces stay clear the usual way: in front of the face a
lock within |x| < 3 must end above y = -5.02, and long locks hang at |x| >= 4.1.
"""
from __future__ import annotations

import math

from anime import cel_box, cel_face
from paint import k, rnd, solid
from wardrobe import rot_matrix

SIDES = (("right", -1), ("left", 1))
BAYER = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))


# -- scalp -------------------------------------------------------------------------------------
def clipped(face, seed: int, base: int = 1, rows=None, cols=None, density: float = 1.0, shadow: str = "X2"):
    """Close-clipped hair: an even tone with a few lighter flecks. Below density 1 an ordered
    dither turns texels into translucent shadow, so the skin shows through like stubble."""
    rows = range(face.h) if rows is None else rows
    cols = range(face.w) if cols is None else cols
    for y in rows:
        for x in cols:
            if (BAYER[y % 4][(x + face.x0) % 4] + .5) / 16 > density:
                face.set(x, y, shadow)
                continue
            f = rnd(x + face.x0, y + face.y0, seed + 5)
            face.set(x, y, k("H", base + (1 if f < .1 else 0)))


def fade(face, seed: int, top: int, bottom: int, base: int = 1, cols=None, start: float = .75, end: float = .1):
    """Rows top..bottom fade from clipped hair (density start) down to shadowed skin (density end)."""
    for y in range(top, bottom + 1):
        t = (y - top) / max(1, bottom - top)
        clipped(face, seed, base, rows=[y], cols=cols, density=start + (end - start) * t, shadow="X2" if t < .6 else "X1")


def clipped_scalp(g, seed: int, base: int = 1, side_rows: int = 6, back_rows: int = 7, fade_rows: int = 3,
                  sideburn: int = 1, top: bool = True, hairline: bool = True):
    """A close-clipped head: crown, sides and back clipped, the lowest rows fading to skin."""
    head = g.part("head")
    if top:
        clipped(head.top, seed, base + 1)
    for face, rows in ((head.right, side_rows), (head.left, side_rows), (head.back, back_rows)):
        full = max(0, rows - fade_rows)
        clipped(face, seed + face.x0, base, rows=range(full))
        if rows > full:
            fade(face, seed + face.x0, full, rows - 1, base)
    for y in range(side_rows, min(8, side_rows + sideburn)):
        head.right.set(7, y, k("H", base)), head.left.set(0, y, k("H", base))
    if hairline:
        head.front.hline(0, 7, 0, k("H", base))
        head.front.set(0, 1, k("H", base)), head.front.set(7, 1, k("H", base))
    return head


def shave(face, seed: int, rows, cols=None, density: float = .1):
    """Shaved skin: an even translucent shadow with a fine, regular dot of deeper stubble."""
    cols = range(face.w) if cols is None else cols
    for y in rows:
        for x in cols:
            dot = (BAYER[(y + seed) % 4][(x + face.x0) % 4] + .5) / 16 < density
            face.set(x, y, "X2" if dot else "X1")


# -- surfaces ----------------------------------------------------------------------------------
def combed_face(face, seed: int, base: int = 2, sheen: int | None = None, across_y: bool = False):
    """Hair combed one way: fine parallel comb lines and a broken sheen band across them.
    Lines run along the face's y unless across_y, then along x."""
    for y in range(face.h):
        for x in range(face.w):
            u, v = (y, x) if across_y else (x, y)
            s = base
            if u % 2 == 1 and rnd(u, v // 3, seed) < .65:
                s -= 1
            if sheen is not None and v == sheen and rnd(u, v, seed + 3) < .8:
                s = base + 1
            face.set(x, y, k("H", s))


def plait_face(face, seed: int, base: int = 2, across_y: bool = False, phase: int = 0):
    """A three-strand plait: two-texel bumps alternating sides, shaded crossings between them.
    The plait runs along the face's y, or along x when across_y."""
    n, length = (face.h, face.w) if across_y else (face.w, face.h)
    for a in range(length):
        q, r = divmod(a + phase, 2)
        for c in range(n):
            near = (q % 2 == 0) if n == 1 else ((c < n / 2) == (q % 2 == 0))
            s = base + (1 if near and r == 0 else 0) - (1 if not near and r == 1 else 0)
            x, y = (a, c) if across_y else (c, a)
            face.set(x, y, k("H", s))


def twist_face(face, seed: int, base: int = 2, period: int = 3, lean: int = 1):
    """A rope twist: diagonal light and dark bands wrapping round the strand."""
    off = int(rnd(seed, 2) * period)
    for y in range(face.h):
        for x in range(face.w):
            d = (x * lean + y + off) % period
            face.set(x, y, k("H", base + 1 if d == 0 else base - 1 if d == period - 1 else base))


def coil_face(face, seed: int, base: int = 2):
    """A springy coil: stacked loops, each a lit upper row over a shaded lower row."""
    off = int(rnd(seed, 4) * 2)
    for y in range(face.h):
        for x in range(face.w):
            upper = (y + off) % 2 == 0
            edge = x in (0, face.w - 1) and face.w > 2
            s = base + (1 if upper and not edge else 0) - (0 if upper else 1)
            face.set(x, y, k("H", s))


def loc_face(face, seed: int, base: int = 2):
    """A loc: matte felted rope with a soft swell every three texels."""
    off = int(rnd(seed, 8) * 3)
    for y in range(face.h):
        for x in range(face.w):
            r = (y + off) % 3
            s = base - (1 if r == 2 else 0) + (1 if r == 0 and rnd(x + face.x0, y, seed) < .6 else 0)
            face.set(x, y, k("H", s))


def ringlet_face(face, seed: int, base: int = 2):
    """A loose spiral curl: wide diagonal bands of light winding down the lock."""
    twist_face(face, seed, base, period=4, lean=1)


def wave_face(face, seed: int, base: int = 2, period: int = 6):
    """Waves down a lock: the lit strand swings from side to side as it falls."""
    phase = rnd(seed, 6) * period
    for y in range(face.h):
        c = (face.w - 1) / 2 + (face.w / 2) * math.sin(2 * math.pi * (y + phase) / period)
        for x in range(face.w):
            d = abs(x - c)
            s = base + 1 if d < .7 else base - 1 if d > face.w / 2 + .2 else base
            face.set(x, y, k("H", s))


def paint_sides(box, painter, seed: int, base: int = 2, top_delta: int = 1, bottom_delta: int = -1, **kw):
    """Run a face painter on the four sides; light top, shaded underside."""
    for f in box.sides:
        painter(f, seed + f.x0, base, **kw)
    box.top.fill(k("H", base + top_delta))
    for x in range(box.top.w):
        for y in range(box.top.h):
            if (x + y) % 3 == 0:
                box.top.set(x, y, k("H", base + top_delta - 1))
    box.bottom.fill(k("H", base + bottom_delta))
    return box


# -- pieces ------------------------------------------------------------------------------------
def clump(g, pid: str, pivot, size, rotation=(0, 0, 0), origin=None, seed: int = 0, base: int = 2,
          ring: int | None = None, top_delta: int = 1, clump_w: int = 3, motion: str = "none", inflate: float = 0):
    """One cel-shaded block of hair, by default hanging down from its pivot."""
    w, h, d = size
    origin = origin if origin is not None else (-w / 2, 0, -d / 2)
    box = g.piece(pid, "HEAD", origin, size, pivot=pivot, rotation=rotation, motion=motion, inflate=inflate)
    cel_box(box, seed, base, ring, top_delta, clump_w)
    return box


def plate(g, pid: str, pivot, size, rotation=(0, 0, 0), origin=None, seed: int = 0, base: int = 2,
          sheen: int | None = None, across: bool = False):
    """A flat combed lock lying on the head; its strands run front to back (or side to side when
    across), with comb lines and a sheen band on top."""
    w, h, d = size
    origin = origin if origin is not None else (-w / 2, -h, -d / 2)
    box = g.piece(pid, "HEAD", origin, size, pivot=pivot, rotation=rotation)
    cel_box(box, seed, base, None, top_delta=1)
    combed_face(box.top, seed, base + 1, sheen, across_y=across)
    return box


def taper(g, pid: str, pivot, rotation=(0, 0, 0), segments=((2, 3, 2), (1, 2, 1)), seed: int = 0, base: int = 2,
          ring: int | None = 1, up: bool = False, motion: str = "none", z_offset: float = 0.0, painter=None):
    """A pointed lock whose segments narrow in width and depth. It hangs along local +y, or rises
    along -y when up. All segments share the pivot, so a swaying lock moves as one."""
    y = 0.0
    boxes = []
    for i, (w, h, d) in enumerate(segments):
        oy = y - h if up else y
        box = g.piece(f"{pid}_{i}" if len(segments) > 1 else pid, "HEAD", (-w / 2, oy, -d / 2 + z_offset), (w, h, d),
                      pivot=pivot, rotation=rotation, motion=motion)
        if painter is not None:
            paint_sides(box, painter, seed + i * 7, base)
        else:
            tip = up and i == len(segments) - 1
            cel_box(box, seed + i * 7, base + (1 if tip else 0), ring if i == 0 else None, top_delta=1 if (i == 0 or up) else 0)
        y = oy if up else y + h
        boxes.append(box)
    return boxes


def chain(g, pid: str, start, segments, seed: int = 0, base: int = 2, ring: int | None = 1, painter=None,
          overlap: float = .4):
    """A lock that bends: each segment (w, h, d, (rx, ry, rz)) hangs from the end of the one before,
    for waves, flicks, curls and folded tails. Not for swaying pieces (each has its own pivot)."""
    px, py, pz = start
    boxes = []
    for i, (w, h, d, rot) in enumerate(segments):
        box = g.piece(f"{pid}_{i}", "HEAD", (-w / 2, 0, -d / 2), (w, h, d), pivot=(px, py, pz), rotation=rot)
        if painter is not None:
            paint_sides(box, painter, seed + i * 7, base)
        else:
            last = i == len(segments) - 1
            for f in box.sides:   # joints stay smooth; only the tip darkens
                cel_face(f, seed + i * 7 + f.x0, base, ring if i == 0 else None, tip_dark=last)
            box.top.fill(k("H", base + (1 if i == 0 else 0)))
            box.bottom.fill(k("H", base - (2 if last else 1)))
        m = rot_matrix(*rot)
        reach = h - (overlap if i < len(segments) - 1 else 0)
        px, py, pz = px + m[0][1] * reach, py + m[1][1] * reach, pz + m[2][1] * reach
        boxes.append(box)
    return boxes


def plait(g, pid: str, pivot, length: int, rotation=(0, 0, 0), width: int = 2, depth: int = 2, seed: int = 0,
          base: int = 2, tie_role: str | None = "L", tuft: int = 2, motion: str = "none", origin_y: float = 0.0):
    """A hanging braid in one piece, tied off with a band and ending in a pointed tuft. Every part
    shares the pivot so the braid swings as one."""
    boxes = []
    body = g.piece(f"{pid}", "HEAD", (-width / 2, origin_y, -depth / 2), (width, length, depth), pivot=pivot,
                   rotation=rotation, motion=motion)
    paint_sides(body, plait_face, seed, base)
    boxes.append(body)
    y = origin_y + length
    if tie_role:
        band = g.piece(f"{pid}_tie", "HEAD", (-width / 2, y, -depth / 2), (width, 1, depth), pivot=pivot, rotation=rotation,
                       inflate=.12, motion=motion)
        solid(band, tie_role, "leather" if tie_role == "L" else "smooth" if tie_role == "M" else "plain", seed + 1, 2, edge=False)
        boxes.append(band)
        y += 1
    if tuft:
        tw = max(1, width - 1) if width > 1 else 1
        end = g.piece(f"{pid}_tuft", "HEAD", (-tw / 2, y, -min(depth, tw) / 2), (tw, tuft, min(depth, tw)), pivot=pivot,
                      rotation=rotation, motion=motion)
        cel_box(end, seed + 2, base, None, top_delta=0)
        boxes.append(end)
    return boxes


def cornrow(g, pid: str, pivot, length: int, rotation=(0, 0, 0), width: int = 1, seed: int = 0, base: int = 2,
            phase: int = 0):
    """A braid lying flat on the scalp, running along its local z from the pivot backwards."""
    box = g.piece(pid, "HEAD", (-width / 2, -1, 0), (width, 1, length), pivot=pivot, rotation=rotation)
    plait_face(box.top, seed, base + 1, phase=phase)
    for f in (box.right, box.left):   # their x runs along the braid
        plait_face(f, seed, base, across_y=True, phase=phase)
    box.front.fill(k("H", base - 1)), box.back.fill(k("H", base - 1)), box.bottom.fill(k("H", base - 2))
    return box


def tie(g, pid: str, pivot, size, rotation=(0, 0, 0), origin=None, role: str = "L", inflate: float = .12,
        motion: str = "none", seed: int = 0):
    """A band, cord or ribbon wrap in an outfit role (leather by default) with a lit upper edge."""
    w, h, d = size
    origin = origin if origin is not None else (-w / 2, -h / 2, -d / 2)
    box = g.piece(pid, "HEAD", origin, size, pivot=pivot, rotation=rotation, inflate=inflate, motion=motion)
    texture = "leather" if role == "L" else "smooth" if role == "M" else "plain"
    solid(box, role, texture, seed, 2, edge=False)
    for f in box.sides:
        f.hline(0, f.w - 1, 0, k(role, 3))
    return box


def hat_ring(g, seed: int, base: int = 2, rows=None, ring_row: int = 1, faces=("back", "right", "left")):
    """Cel-shaded hat-layer hair on chosen faces and rows (a partial ring_shell), sheen ring included."""
    hat = g.part("hat")
    rows = rows or {}
    for name in faces:
        face = getattr(hat, name)
        n = rows.get(name, 4)
        sub = type(face)(face.layer, face.x0, face.y0, face.w, n, face.name)
        cel_face(sub, seed + face.x0, base, ring_row, tip_dark=False)
        if n < 8:
            for x in range(face.w):
                if rnd(x, n, seed) < .5:
                    face.set(x, n, k("H", base - 1))
    return hat
