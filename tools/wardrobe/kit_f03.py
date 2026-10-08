"""Shared helpers for the river, coast and market batch (tf/bf 111-135): wicker, rope, netting, wet
hems and props hung from the waist. Every helper paints key colors only and returns what it built;
each garment keeps its own identity in its own module.
"""
from __future__ import annotations

from kit_female import OVER_FRONT
from paint import fabric, k, rnd, solid
from wardrobe import shade


def wicker(face, role: str = "L", base: int = 2, x0: int = 0, y0: int = 0, w: int | None = None, h: int | None = None):
    """Basketwork: dark upright stakes every third column, weavers passing over and under them in rows."""
    w = face.w - x0 if w is None else w
    h = face.h - y0 if h is None else h
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            col = (x + face.x0) % 3
            if col == 0:
                key = k(role, base - 1)
            else:
                key = k(role, base + 1) if (col == 1) == (y % 2 == 0) else k(role, base)
            face.set(x, y, key)


def basket(g, pid: str, bone: str, origin, size, pivot, role: str = "L", base: int = 2, rotation=(0, 0, 0),
           motion: str = "none", inside: str | None = None):
    """A woven basket: wicker sides with a lit rim, a dark open top (or `inside`) and a shaded base."""
    box = g.piece(pid, bone, origin, size, pivot=pivot, rotation=rotation, motion=motion)
    for f in box.sides:
        wicker(f, role, base)
        f.hline(0, f.w - 1, 0, k(role, base + 2))
        f.hline(0, f.w - 1, f.h - 1, k(role, base - 1))
    box.top.fill(inside or k(role, 0))
    for x in range(box.top.w):
        box.top.set(x, 0, k(role, base + 1)), box.top.set(x, box.top.h - 1, k(role, base + 1))
    for y in range(box.top.h):
        box.top.set(0, y, k(role, base + 1)), box.top.set(box.top.w - 1, y, k(role, base + 1))
    box.bottom.fill(k(role, base - 1))
    return box


def rope(face, role: str = "S", base: int = 2, x0: int = 0, y0: int = 0, w: int | None = None, h: int | None = None,
         across: bool = False):
    """Laid rope: twisted strands as short diagonals. `across` twists for a rope running sideways."""
    w = face.w - x0 if w is None else w
    h = face.h - y0 if h is None else h
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            d = (x + y) % 3 if across else (x - y) % 3
            face.set(x, y, k(role, base + 1 if d == 0 else base if d == 1 else base - 1))


def rope_box(box, role: str = "S", base: int = 2, across: bool = False):
    for f in box.sides:
        rope(f, role, base, across=across)
    fabric(box.top, role, "plain", 0, base + 1)
    fabric(box.bottom, role, "plain", 1, base - 1)


def net(face, twine: str = "S3", gap: str = "K2", step: int = 3, x0: int = 0, y0: int = 0, w: int | None = None,
        h: int | None = None, knot: str | None = None, phase: int = 0):
    """Diamond fishing net: a twine lattice over dark gaps, with an optional knot where strands cross."""
    w = face.w - x0 if w is None else w
    h = face.h - y0 if h is None else h
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            a, b = (x + y + phase) % step == 0, (x - y + phase) % step == 0
            key = (knot or twine) if a and b else twine if a or b else gap
            face.set(x, y, key)


def net_box(box, twine: str = "S3", gap: str = "K2", step: int = 3, knot: str | None = None):
    for f in box.faces:
        net(f, twine, gap, step, knot=knot, phase=f.x0)


def wet_hem(face, rows: int, seed: int, x0: int = 0, x1: int | None = None, deep_rows: int = 1):
    """Soak the lower rows of a face: a ragged tide line, everything below it a shade darker,
    the last `deep_rows` darker still."""
    x1 = face.w - 1 if x1 is None else x1
    top = face.h - rows
    for x in range(x0, x1 + 1):
        edge = top + (1 if rnd(x + face.x0, 3, seed) < .35 else 0) - (1 if rnd(x + face.x0, 5, seed) < .25 else 0)
        for y in range(max(0, edge), face.h):
            cur = face.get(x, y)
            if cur and cur[0] != "X":
                face.set(x, y, shade(cur, -2 if y >= face.h - deep_rows else -1))


def front_prop(g, pid: str, x: float, size, y: float = 0.0, role: str = "L", base: int = 2, texture: str = "smooth",
               seed: int = 0, top: float = 9.0, rotation=(0, 0, 0), edge: bool = True):
    """A prop hung from the waist in front of any skirt or apron; it rides the leading leg."""
    w, h, d = size
    box = g.piece(pid, "TORSO", (-w / 2, y, -.2 - (d - 1)), size, pivot=(x, top, OVER_FRONT), motion="flap_front",
                  rotation=rotation)
    solid(box, role, texture, seed, base, edge=edge)
    return box


def cord(face, x0: int, y0: int, x1: int, y1: int, key: str):
    """A thin cord or strap drawn between two points (a straight line in face pixels)."""
    from paint import line
    line(face, x0, y0, x1, y1, key)
