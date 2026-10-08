"""Shared helpers for the soldiers, watch and arms batch (tops t196-t220, bottoms b196-b220).

Straps, plate lames, lamellar, rivets, hanging props that ride the stride, and a few small
weapons and fittings. Like kit.py, everything paints key colors only and returns what it
creates, so each module keeps its own identity (its cut, trim and props) to itself.
"""
from __future__ import annotations

from kit import SIDES, arm_bone, leg_bone
from paint import k, rnd, solid


# -- straps and patterns ---------------------------------------------------------------------
def diag(face, x0, y0, x1, y1, keys, every: int = 0, stud: str | None = None):
    """A thick diagonal band: keys[j] is painted j texels right of the line. Optional studs."""
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(steps + 1):
        x = round(x0 + (x1 - x0) * i / steps)
        y = round(y0 + (y1 - y0) * i / steps)
        for j, key in enumerate(keys):
            face.set(x + j, y, key)
        if stud and every and i % every == every // 2:
            face.set(x, y, stud)


def baldric(g, shoulder: str = "right", role: str = "L", base: int = 2, rows: int = 10, layer: str = "jacket",
            stud: str | None = None, every: int = 3):
    """A two-texel strap over one shoulder to the opposite hip: jacket front, shoulder top and back."""
    box = g.part(layer)
    keys = [k(role, base + 1), k(role, base - 1)]
    right = shoulder == "right"
    fx0, fx1 = (0, 6) if right else (6, 0)
    bx0, bx1 = (6, 0) if right else (0, 6)
    diag(box.front, fx0, 0, fx1, rows, keys, every, stud)
    diag(box.back, bx0, 0, bx1, rows, keys, every, stud)
    tx = 0 if right else 6
    for y in range(box.top.h):
        box.top.set(tx, y, keys[0]), box.top.set(tx + 1, y, keys[1])
    return box


def lames(face, y0: int, y1: int, role: str = "M", base: int = 2, step: int = 2, rivet: str | None = None,
          rivet_step: int = 3, x0: int = 0, x1: int | None = None):
    """Horizontal plate lames: a lit upper edge and a shaded lower edge on each lame."""
    x1 = face.w - 1 if x1 is None else x1
    for y in range(y0, y1 + 1):
        r = (y - y0) % step
        key = k(role, base + 1) if r == 0 else k(role, base - 1) if r == step - 1 else k(role, base)
        face.hline(x0, x1, y, key)
        if rivet and r == 0 and step > 1:
            for x in range(x0 + 1, x1 + 1, rivet_step):
                face.set(x, y, rivet)


def lamellar(face, rows=None, role: str = "M", base: int = 2, lace: str = "L1", ox: int = 0):
    """Rows of small laced plates: each lamella a texel wide and two tall, a lacing row between."""
    for y in rows if rows is not None else range(face.h):
        band, r = y // 3, y % 3
        for x in range(face.w):
            c = (x + ox + band) % 2
            if r == 2:
                key = lace if c == 0 else k(role, base - 1)
            elif r == 0:
                key = k(role, base + 1) if c == 0 else k(role, base)
            else:
                key = k(role, base) if c == 0 else k(role, base - 1)
            face.set(x, y, key)


def stitch_box(face, x0, y0, w, h, key):
    """A stitched outline (patches, pockets, plates)."""
    face.hline(x0, x0 + w - 1, y0, key), face.hline(x0, x0 + w - 1, y0 + h - 1, key)
    face.vline(x0, y0, y0 + h - 1, key), face.vline(x0 + w - 1, y0, y0 + h - 1, key)


def qrows(face, role: str, base: int = 2, step: int = 2, rows=None, offset: int = 0):
    """Horizontal quilted channels: a stitched (shaded) row every `step` rows, a puffed row above it."""
    for y in rows if rows is not None else range(face.h):
        r = (y + offset) % step
        key = k(role, base - 1) if r == step - 1 else k(role, base + 1) if r == 0 and step > 2 else k(role, base)
        face.hline(0, face.w - 1, y, key)


def patch(face, x0: int, y0: int, w: int, h: int, role: str, base: int = 2, stitch: str | None = None):
    """A sewn-on patch: flat cloth with a lit top edge and a stitched or shaded border."""
    face.rect(x0, y0, w, h, k(role, base))
    face.hline(x0, x0 + w - 1, y0, k(role, base + 1))
    edge = stitch or k(role, base - 1)
    face.hline(x0, x0 + w - 1, y0 + h - 1, edge)
    face.vline(x0 + w - 1, y0, y0 + h - 1, edge)


def plates_grid(face, role: str = "M", base: int = 2, cell: int = 2, cord: str = "S3", ox: int = 0, oy: int = 0,
                rows=None):
    """Jack of plates: small square plates quilted between cloth, a cord crossing at every corner."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            gx, gy = (x + ox) % cell, (y + oy) % cell
            if gx == 0 and gy == 0:
                key = cord
            elif gy == 0 or gx == 0:
                key = k(role, base - 1)
            else:
                key = k(role, base + (1 if (gx, gy) == (1, 1) else 0))
            face.set(x, y, key)


def mud(face, seed: int, rows, key_light: str = "L1", key_dark: str = "L0", start: float = .05, end: float = .45):
    """Mud thickening toward the lower rows: sparse specks up top, caked near the bottom."""
    rows = list(rows)
    for i, y in enumerate(rows):
        density = start + (end - start) * i / max(1, len(rows) - 1)
        for x in range(face.w):
            r = rnd(x + face.x0, y + face.y0, seed)
            if r < density * .5:
                face.set(x, y, key_dark)
            elif r < density:
                face.set(x, y, key_light)


# -- props -----------------------------------------------------------------------------------
def hanging(g, pid: str, x: float, y: float, size, role: str, base: int = 2, texture: str = "plain", seed: int = 0,
            top: float = 10.6, z: float = -2.85, dz: float = 0.0, front: bool = True, rotation=(0, 0, 0)):
    """A prop hung in front of (or behind) the hips that rides the stride like a hem flap.

    It shares the flap pivot (0, top, z), so it swings with the leading (or trailing) leg instead
    of clipping through it. (x, y) is the prop's top centre in torso space.
    """
    w, h, d = size
    oz = (-d + dz) if front else (1 + dz)
    box = g.piece(pid, "TORSO", (x - w / 2, y - top, oz), size, pivot=(0, top, z), rotation=rotation,
                  motion="flap_front" if front else "flap_back")
    solid(box, role, texture, seed, base)
    return box


def leg_prop(g, pid: str, side: str, origin, size, role: str, base: int = 2, texture: str = "plain", seed: int = 0,
             pivot=(0, 0, 0), rotation=(0, 0, 0), inflate: float = 0.0):
    """A cuboid on one leg bone with an explicit origin (boot tops, splints, spurs, pockets)."""
    box = g.piece(f"{side}_{pid}", leg_bone(side), origin, size, pivot=pivot, rotation=rotation, inflate=inflate)
    solid(box, role, texture, seed, base)
    return box


def pole(g, pid: str, pivot, length: int, role: str = "L", base: int = 2, rotation=(0, 0, 0), bone: str = "TORSO",
         thick: int = 1, seed: int = 0):
    """A straight shaft hanging down from its pivot (rotate it to lean): spear, banner pole, rod."""
    box = g.piece(pid, bone, (-thick / 2, 0, -thick / 2), (thick, length, thick), pivot=pivot, rotation=rotation)
    solid(box, role, "plain", seed, base, edge=False)
    for face in box.sides:
        face.vline(face.w - 1, 0, length - 1, k(role, base - 1))
    return box


def split_flaps(g, prefix: str, length: int, role: str, texture: str = "weave", seed: int = 0, base: int = 2,
                top: float = 10.8, half: int = 4, gap: float = .5, front_z: float = -2.85, back_z: float = 1.85,
                hem: str | None = None):
    """A riding skirt split front and back: four half panels that follow the stride. Returns their outer faces."""
    faces = []
    for name, z, motion, face_name in (("front", front_z, "flap_front", "front"), ("back", back_z, "flap_back", "back")):
        for side, x0 in (("right", -half - gap / 2), ("left", gap / 2)):
            panel = g.piece(f"{prefix}_{name}_{side}", "TORSO", (x0, 0, 0), (half, length, 1), pivot=(0, top, z),
                            motion=motion)
            solid(panel, role, texture, seed + len(faces), base)
            face = getattr(panel, face_name)
            face.hline(0, half - 1, 0, k(role, base + 1))
            if hem:
                face.hline(0, half - 1, length - 1, hem)
            faces.append(face)
    return faces


def round_shield(g, prefix: str, cx: float, cy: float, z: float, radius: int = 5, role: str = "P", base: int = 2,
                 rim: str = "L", seed: int = 0, rotation=(0, 0, 0), bone: str = "TORSO"):
    """A round shield built from three stepped slabs (a chunky disc) facing backward, with a domed boss.

    (cx, cy) is the centre in bone space and z the slab's front (body-side) plane; the painted face is the
    back face. Returns (slabs, boss).
    """
    r = radius
    slabs = []
    for i, (w, h) in enumerate(((2 * r, 2 * r - 4), (2 * r - 2, 2 * r - 2), (2 * r - 4, 2 * r))):
        slab = g.piece(f"{prefix}_{i}", bone, (cx - w / 2, cy - h / 2, 0), (w, h, 1), pivot=(0, 0, z),
                       rotation=rotation)
        solid(slab, role, "plain", seed + i, base, edge=False)
        slabs.append(slab)
    boss = g.piece(f"{prefix}_boss", bone, (cx - 1, cy - 1, 1), (2, 2, 1), pivot=(0, 0, z), rotation=rotation)
    solid(boss, "M", "smooth", seed + 5, 3, edge=False)
    boss.back.set(0, 0, "M4"), boss.back.set(1, 1, "M1")
    return slabs, boss


def spur(g, side: str, y: float = 10.4, rowel: bool = True, seed: int = 0, z: float = 2.25):
    """A spur at the heel: a strap round the ankle is painted by the module; this adds the neck and rowel."""
    neck = g.piece(f"{side}_spur", leg_bone(side), (-.5, 0, 0), (1, 1, 2), pivot=(0, y, z))
    solid(neck, "M", "smooth", seed, 3, edge=False)
    if rowel:
        star = g.piece(f"{side}_spur_rowel", leg_bone(side), (-.5, -1, 1.6), (1, 3, 1), pivot=(0, y, z), inflate=.02)
        solid(star, "M", "smooth", seed + 1, 3, edge=False)
        for face in star.sides:
            face.set(0, 0, "M4"), face.set(0, 1, "M1"), face.set(0, 2, "M4")
        return neck, star
    return neck, None


def chain(box, light: str = "M3", dark: str = "M1"):
    """Paint a 1-texel-wide cuboid as chain links."""
    for face in box.sides:
        for y in range(face.h):
            face.hline(0, face.w - 1, y, light if y % 2 == 0 else dark)


def key_shape(box, bit: str = "M1"):
    """A hanging key: a ring bow at the top, a bit at the foot."""
    for face in box.sides:
        face.set(0, 0, "M4")
        face.set(face.w - 1, face.h - 1, bit)


def sides_of(side: str):
    """(outer, inner) face names of a right/left limb."""
    return ("right", "left") if side == "right" else ("left", "right")


__all__ = ["SIDES", "arm_bone", "baldric", "chain", "diag", "hanging", "key_shape", "lamellar", "lames", "leg_prop",
           "mud", "patch", "plates_grid", "pole", "qrows", "round_shield", "sides_of", "split_flaps", "spur",
           "stitch_box"]
