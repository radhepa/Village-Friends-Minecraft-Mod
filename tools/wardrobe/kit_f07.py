"""Small helpers for the women's travel, wilderness and road wardrobe (tf/bf 211-235).

Props, wicker, rope, straps and road wear that several of these pieces share. Every helper paints
key colors only and returns what it built; each piece keeps its own identity in its own module.
"""
from __future__ import annotations

from kit import SIDES
from kit_female import OVER_FRONT
from paint import fabric, k, line, rnd, solid
from wardrobe import shade


def prop(g, pid: str, bone: str, origin, size, pivot=(0, 0, 0), role: str = "L", texture: str = "smooth",
         seed: int = 0, base: int = 2, rotation=(0, 0, 0), motion: str = "none", inflate: float = 0.0,
         edge: bool = True):
    """One fully painted cuboid prop; returns its box for details."""
    box = g.piece(pid, bone, origin, size, pivot=pivot, rotation=rotation, motion=motion, inflate=inflate)
    solid(box, role, texture, seed, base, edge=edge)
    return box


def front_hung(g, pid: str, x: float, origin, size, role: str = "L", texture: str = "smooth", seed: int = 0,
               base: int = 2, top: float = 9.0, inflate: float = 0.0, z: float | None = None):
    """A prop hung from the waist in front of any skirt, riding the stride with the leading leg."""
    return prop(g, pid, "TORSO", origin, size, pivot=(x, top, OVER_FRONT - .1 if z is None else z), role=role,
                texture=texture, seed=seed, base=base, motion="flap_front", inflate=inflate)


def wicker(face, role: str = "L", base: int = 2, seed: int = 0):
    """Basket weave: stakes and weavers alternating every two texels."""
    for y in range(face.h):
        for x in range(face.w):
            over = ((x + face.x0) // 2 + y // 2) % 2 == 0
            s = base + (1 if over and y % 2 == 0 else 0) - (0 if over else 1)
            if rnd(x + face.x0, y + face.y0, seed) > .97:
                s -= 1
            face.set(x, y, k(role, s))


def wicker_box(box, role: str = "L", base: int = 2, seed: int = 0, rim: bool = True):
    for face in box.sides:
        wicker(face, role, base, seed)
        if rim:
            face.hline(0, face.w - 1, 0, k(role, base + 2))
            face.hline(0, face.w - 1, face.h - 1, k(role, base - 1))
    fabric(box.top, role, "plain", seed, base - 1)
    fabric(box.bottom, role, "plain", seed + 1, base - 1)


def rope(face, x0: int, y0: int, x1: int, y1: int, role: str = "S", base: int = 2):
    """A twisted cord: alternating light and shade along a line."""
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err, i = dx + dy, 0
    while True:
        face.set(x0, y0, k(role, base + (1 if i % 2 == 0 else -1)))
        if x0 == x1 and y0 == y1:
            return
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy
        i += 1


def rope_box(box, role: str = "S", base: int = 2):
    """A rope or cord cuboid: diagonal twists on every side."""
    for face in box.sides:
        for y in range(face.h):
            for x in range(face.w):
                face.set(x, y, k(role, base + 1) if (x + y + face.x0) % 3 == 0 else k(role, base - 1)
                         if (x + y + face.x0) % 3 == 2 else k(role, base))
    box.top.fill(k(role, base)), box.bottom.fill(k(role, base - 1))


def strap(face, x0: int, y0: int, x1: int, y1: int, key: str = "L2", edge: str | None = None):
    """A strap drawn as a line; an optional second, darker line under it gives it width."""
    if edge:
        line(face, x0, y0 + 1, x1, y1 + 1, edge)
    line(face, x0, y0, x1, y1, key)


def dust(face, rows: int = 3, delta: int = 1, y_end: int | None = None):
    """Road dust settling toward a hem: solid lighter rows with one checkered row fading into the cloth."""
    y_end = face.h - 1 if y_end is None else y_end
    for i in range(rows):
        y = y_end - i
        for x in range(face.w):
            if i == rows - 1 and (x + face.x0 + y) % 2:
                continue
            cur = face.get(x, y)
            if cur:
                face.set(x, y, shade(cur, delta))


def patch(face, x: int, y: int, w: int, h: int, key: str, stitch: str = "K2"):
    """A square patch with a running stitch round its edge."""
    face.rect(x, y, w, h, key)
    for xx in range(x, x + w):
        if (xx - x) % 2 == 0:
            face.set(xx, y, stitch), face.set(xx, y + h - 1, stitch)
    for yy in range(y, y + h):
        if (yy - y) % 2 == 1:
            face.set(x, yy, stitch), face.set(x + w - 1, yy, stitch)


def legs_both(g, fn):
    """fn(side, leg_box, pants_box) for both legs."""
    for side in SIDES:
        fn(side, g.part(f"{side}_leg"), g.part(f"{side}_pants"))
