"""Helpers for the m05 batch (men's clergy, learning and healing, t/b 221-245).

Long gowns that lie over skirts, close hose, soft shoes, diagonal straps and swinging cords.
Like kit.py these paint key colors only and return what they create; each garment keeps its
own identity (props, trims, closures) in its own module.
"""
from __future__ import annotations

from kit import SIDES, leg_bone
from paint import fabric, k, line, solid, strip_fabric


# -- tops --------------------------------------------------------------------------------------
def over_panels(g, prefix: str, length: int, role: str, texture: str = "weave", seed: int = 0, base: int = 2,
                top: float = 10.6, width: int = 10, sides: bool = True, side_len: int | None = None,
                front_z: float = -3.15, back_z: float = 2.15, side_x: float = 5.35):
    """Gown skirts that hang over a bottom's skirt (z -3.15 / 2.15), plus optional side panels.

    Returns (front_face, back_face, side_boxes); faces are the outward ones."""
    faces = []
    for name, z, motion, face_name in (("front", front_z, "flap_front", "front"), ("back", back_z, "flap_back", "back")):
        panel = g.piece(f"{prefix}_{name}", "TORSO", (-width / 2, 0, 0), (width, length, 1), pivot=(0, top, z),
                        motion=motion)
        solid(panel, role, texture, seed + (name == "back"), base)
        face = getattr(panel, face_name)
        face.hline(0, width - 1, 0, k(role, base + 1))
        faces.append(face)
    side_boxes = []
    if sides:
        for name, x in (("right", -side_x), ("left", side_x - 1)):
            panel = g.piece(f"{prefix}_{name}", "TORSO", (0, 0, -2), (1, side_len or max(1, length - 1), 4),
                            pivot=(x, top, 0))
            solid(panel, role, texture, seed + 2, base)
            side_boxes.append(panel)
    return faces[0], faces[1], side_boxes


def strap(g, key: str = "L2", shade_key: str = "L1", from_side: str = "left", low: int = 10):
    """A strap worn bandolier-wise: from one shoulder across the chest to the other hip, and the same behind.

    `from_side` is the wearer's shoulder it rests on. Painted on the jacket overlay."""
    jacket = g.part("jacket")
    f, b = jacket.front, jacket.back
    if from_side == "left":      # wearer's left is the right of the front face as we look at it
        line(f, 6, 0, 1, low, key), line(f, 7, 0, 2, low, shade_key)
        line(b, 1, 0, 6, low, key), line(b, 0, 0, 5, low, shade_key)
        jacket.top.vline(6, 0, 3, key)
    else:
        line(f, 1, 0, 6, low, key), line(f, 0, 0, 5, low, shade_key)
        line(b, 6, 0, 1, low, key), line(b, 7, 0, 2, low, shade_key)
        jacket.top.vline(1, 0, 3, key)
    return jacket


def cord_end(g, pid: str, pivot, length: int, role: str, base: int = 2, seed: int = 0, knots=(), tassel: str | None = None,
             rotation=(0, 0, 0), bone: str = "TORSO"):
    """A swinging 1x1 cord end (cincture tails, ribbons, thongs) with optional knots and a tassel tip."""
    end = g.piece(pid, bone, (-.5, 0, -.5), (1, length, 1), pivot=pivot, rotation=rotation, motion="sway")
    solid(end, role, "plain", seed, base)
    for y in knots:
        end.strip.hline(0, end.strip.w - 1, y, k(role, base - 1))
    if tassel:
        end.strip.hline(0, end.strip.w - 1, length - 1, tassel)
        end.bottom.fill(tassel)
    return end


# -- bottoms -------------------------------------------------------------------------------------
def hose(g, role: str, base: int = 2, texture: str = "weave", seed: int = 0, end: int = 9, back_seam: bool = True):
    """Close-fitting hose to row `end`: a seam up the back of each leg and a soft inner shadow."""
    legs = []
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, role, texture, seed + (side == "left"), base, 0, end)
        fabric(leg.top, role, texture, seed, base)
        if back_seam:
            leg.back.vline(1 if side == "right" else 2, 1, end, k(role, base - 1))
        inner = leg.left if side == "right" else leg.right
        inner.vline(1, 0, end, k(role, base - 1))
        legs.append(leg)
    return legs


def soft_shoes(g, role: str = "L", base: int = 2, top: int = 10, sole: str = "K1", strap: str | None = None,
               cuff: str | None = None):
    """Low soft leather shoes on the leg and pants layers; an optional instep strap and turned cuff."""
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, role, "smooth", 71, base - 1, top, 11)
        for face in pants.sides:
            fabric(face, role, "smooth", 72, base, 0, top, face.w, 12 - top)
            face.hline(0, face.w - 1, top, cuff or k(role, base + 1))
            face.hline(0, face.w - 1, 11, sole)
        if strap:
            pants.front.hline(0, 3, top + (1 if top < 10 else 0), strap)
        leg.bottom.fill(sole), pants.bottom.fill("K0")


def leg_prop(g, pid: str, side: str, pivot, size, role: str, base: int = 2, texture: str = "plain", seed: int = 0,
             rotation=(0, 0, 0)):
    """A cuboid hung on one leg bone, centred on its pivot in x and z with its top at the pivot."""
    w, h, d = size
    box = g.piece(pid, leg_bone(side), (-w / 2, 0, -d / 2), size, pivot=pivot, rotation=rotation)
    solid(box, role, texture, seed, base)
    return box


TIDE = (1, 0, 0, 1, 2, 1, 1, 0, 1, 2, 2, 1)


def grime(face, key: str, y0: int, y1: int, ox: int = 0, speck: str | None = None):
    """Dirt rising from a hem: solid up to a gently uneven tide line between rows y0 and y1, a stray speck above.

    Calm and structured (road dust, mud, soot, wet) rather than random noise."""
    for x in range(face.w):
        edge = min(y1, y0 + TIDE[(x + ox) % len(TIDE)])
        for y in range(edge, y1 + 1):
            face.set(x, y, key)
        if (x + ox) % 7 == 3 and edge - 2 >= 0:
            face.set(x, edge - 2, speck or key)


def knee_patch(face, x0: int, y0: int, key: str, lit: str, w: int = 2, h: int = 2):
    """A worn or stained patch over the knee: a soft block with one lit texel."""
    face.rect(x0, y0, w, h, key)
    face.set(x0, y0, lit)


def dust(face, key: str, seed: int, rows, density_top: float = .05, density_bottom: float = .3):
    """Dust or mud that thickens toward the ground: denser on lower rows."""
    from paint import rnd
    rows = list(rows)
    for i, y in enumerate(rows):
        d = density_top + (density_bottom - density_top) * i / max(1, len(rows) - 1)
        for x in range(face.w):
            if rnd(x + face.x0, y + face.y0, seed) < d:
                face.set(x, y, key)
