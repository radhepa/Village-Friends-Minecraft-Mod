"""Helpers shared by batch m08 (men's tops and bottoms t/b 296-320, the wider medieval world).

Small, generic shapes only: coat skirts with side panels, crossed collars, roundels, pleats,
hanging tails and tassels. Every helper paints key colors and returns what it creates, so each
garment keeps its own identity (trim, cut and props) in its own module.
"""
from __future__ import annotations

from paint import k, solid


# -- painting ----------------------------------------------------------------------------------
ROUNDEL = [".aa.",
           "abba",
           "abba",
           ".aa."]


def roundel(face, x0: int, y0: int, ring: str, fill: str, core: str | None = None):
    """A 4x4 woven roundel (orbiculus): a ring, a filled middle and an optional core texel."""
    for dy, row in enumerate(ROUNDEL):
        for dx, ch in enumerate(row):
            if ch == "a":
                face.set(x0 + dx, y0 + dy, ring)
            elif ch == "b":
                face.set(x0 + dx, y0 + dy, fill)
    if core:
        face.set(x0 + 1, y0 + 1, core), face.set(x0 + 2, y0 + 2, core)


def pleats(face, role: str, base: int = 2, rows=None, period: int = 2, x0: int = 0, x1: int | None = None, ox: int = 0):
    """Pressed vertical pleats: a lit fold, then shaded valleys, repeating every `period` texels."""
    x1 = face.w - 1 if x1 is None else x1
    for y in rows if rows is not None else range(face.h):
        for x in range(x0, x1 + 1):
            p = (x + ox) % period
            face.set(x, y, k(role, base + 1) if p == 0 else k(role, base - 1) if p == period - 1 else k(role, base))


def crossed_collar(face, band: str, edge: str, x_top: int = 5, y_end: int = 6, width: int = 2):
    """A crossed (wrap) collar: a band from the wearer's left neck down to the wearer's right side.

    On a front face x runs from the wearer's right to left, so the band starts at x_top on row 0
    and steps toward x 0, reaching it at y_end. `edge` lines the band's lower, overlapping side.
    """
    for y in range(face.h):
        if y > y_end + width:
            break
        x = round(x_top - x_top * min(y, y_end) / max(1, y_end))
        for i in range(width):
            if y - i >= 0:
                face.set(x + i, y, band)
        if x > 0:
            face.set(x - 1, y, edge)


def brocade(face, role: str, base: int = 2, cell: int = 6, ox: int = 0, oy: int = 0, core: str | None = None, rows=None):
    """Sparse woven medallions: a small lit diamond with a dark (or accent) heart on every cell,
    alternate rows of cells offset by half a cell. Leaves the ground cloth untouched elsewhere."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            row = (y + oy) // cell
            gx, gy = (x + ox + (cell // 2) * (row % 2)) % cell, (y + oy) % cell
            c = cell // 2
            if (gx, gy) == (c, c):
                face.set(x, y, core or k(role, base - 1))
            elif abs(gx - c) + abs(gy - c) == 1:
                face.set(x, y, k(role, base + 1))


def fringe(face, y: int, a: str, b: str):
    """A knotted fringe along one row: alternating strands."""
    for x in range(face.w):
        face.set(x, y, a if x % 2 == 0 else b)


# -- 3D ----------------------------------------------------------------------------------------
def coat_skirt(g, prefix: str, length: int, role: str, texture: str = "weave", seed: int = 0, base: int = 2,
               top: float = 10.8, width: int = 9, sides: bool = True, side_len: int | None = None,
               hem: str | None = None, side_z: float = 0.0):
    """A top's coat skirt: front/back panels on the stride planes plus still side panels.

    Returns (front_face, back_face, [right_box, left_box]).
    """
    faces = []
    for name, z, motion, face_name in (("front", -2.85, "flap_front", "front"), ("back", 1.85, "flap_back", "back")):
        panel = g.piece(f"{prefix}_{name}", "TORSO", (-width / 2, 0, 0), (width, length, 1), pivot=(0, top, z),
                        motion=motion)
        solid(panel, role, texture, seed + (name == "back"), base)
        face = getattr(panel, face_name)
        face.hline(0, width - 1, 0, k(role, base + 1))
        if hem:
            for f in panel.sides:
                f.hline(0, f.w - 1, length - 1, hem)
        faces.append(face)
    boxes = []
    if sides:
        for name, x in (("right", -4.5), ("left", 4.5)):
            box = g.piece(f"{prefix}_{name}", "TORSO", (-.5, 0, -2), (1, side_len or length - 1, 4), pivot=(x, top, side_z))
            solid(box, role, texture, seed + 2 + (name == "left"), base)
            if hem:
                for f in box.sides:
                    f.hline(0, f.w - 1, box.strip.h - 1, hem)
            boxes.append(box)
    return faces[0], faces[1], boxes


def tassel(g, pid: str, pivot, role: str = "A", length: int = 2, cord: str | None = None, bone: str = "TORSO",
           rotation=(0, 0, 0), base: int = 3):
    """A cord-hung tassel that sways: one texel of cord, then a bushier tassel head."""
    t = g.piece(pid, bone, (-.5, 0, -.5), (1, length + 1, 1), pivot=pivot, rotation=rotation, motion="sway")
    solid(t, role, "plain", 0, base, edge=False)
    t.strip.hline(0, t.strip.w - 1, 0, cord or k(role, base - 1))
    t.strip.hline(0, t.strip.w - 1, length, k(role, base - 2))
    for x in range(0, t.strip.w, 2):
        t.strip.set(x, length - 1, k(role, base + 1))
    return t


def hanging_tail(g, pid: str, pivot, size, role: str, texture: str = "weave", seed: int = 0, base: int = 2,
                 rotation=(0, 0, 0), motion: str = "sway"):
    """A flat cloth tail (sash end, stole, ribbon) hanging from its pivot."""
    w, h, d = size
    t = g.piece(pid, "TORSO", (-w / 2, 0, -d / 2), size, pivot=pivot, rotation=rotation, motion=motion)
    solid(t, role, texture, seed, base, edge=False)
    return t
