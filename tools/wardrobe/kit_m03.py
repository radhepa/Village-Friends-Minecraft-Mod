"""Shared helpers for the men's river, coast and sea pieces (tops t171-t195, bottoms b171-b195).

Rope, wet and glossy cloth, salt or sand dust, knitted stockings and plain low shoes. Like kit.py,
every helper paints key colors only and returns what it creates; each garment keeps its own
signature (props, trims, silhouette) in its own module.
"""
from __future__ import annotations

from kit import SIDES, leg_bone
from paint import fabric, k, rnd, solid, strip_fabric


# -- surfaces --------------------------------------------------------------------------------
def rope(face, role: str = "S", base: int = 2, ox: int = 0, rows=None, cols=None):
    """Laid three-strand rope: diagonal lit, mid and shaded strands."""
    for y in rows if rows is not None else range(face.h):
        for x in cols if cols is not None else range(face.w):
            p = (x + ox + y) % 3
            face.set(x, y, k(role, base + 1 if p == 0 else base if p == 1 else base - 1))


def rope_box(box, role: str = "S", base: int = 2):
    for face in box.faces:
        rope(face, role, base, ox=face.x0)
    return box


def gloss(face, role: str, base: int = 2, seed: int = 0, rows=None, cols=None, glint: float = .05, crease: int = 6):
    """Oilcloth or tarred canvas: smooth stiff cloth, sparse wet glints and a stiff crease every few rows."""
    for y in rows if rows is not None else range(face.h):
        for x in cols if cols is not None else range(face.w):
            r = rnd(x + face.x0, y + face.y0, seed)
            s = base + 2 if r < glint else base + 1 if r < glint * 2.4 else base
            if crease and (y + face.y0) % crease == crease - 2:
                s = base - 1
            face.set(x, y, k(role, s))


def speckle(face, keys, seed: int, density: float = .1, rows=None, cols=None):
    """Sparse dust in a few keys: salt, sand, sawdust, oakum fluff."""
    for y in rows if rows is not None else range(face.h):
        for x in cols if cols is not None else range(face.w):
            r = rnd(x + face.x0, y + face.y0, seed)
            if r < density:
                face.set(x, y, keys[int(r / density * len(keys)) % len(keys)])


def soak(face, role: str, rows, base: int = 2, seed: int = 0):
    """Water wicking up from a hem: each lower row a shade darker, a ragged top edge and a few wet glints."""
    rows = list(rows)
    for i, y in enumerate(rows):
        depth = len(rows) - i
        for x in range(face.w):
            s = base - min(2, (depth + 1) // 2)
            if i == 0 and rnd(x + face.x0, y, seed) < .5:
                s = base - 1
            elif rnd(x + face.x0, y + face.y0, seed + 3) < .07:
                s += 2
            face.set(x, y, k(role, s))


def drips(face, cols, y0: int, key: str, seed: int = 0, longest: int = 3):
    """Short drip runs falling from row y0 in the given columns."""
    for x in cols:
        n = 1 + int(rnd(x + face.x0, y0, seed) * longest)
        face.vline(x, y0, y0 + n - 1, key)


# -- props -----------------------------------------------------------------------------------
def coil(g, pid: str, pivot, size, role: str = "S", base: int = 2, bone: str = "TORSO", rotation=(0, 0, 0),
         motion: str = "none", origin=None):
    """A hank of coiled rope: stacked turns with lit tops and shaded gaps, a dark eye on the flat faces."""
    w, h, d = size
    box = g.piece(pid, bone, origin if origin is not None else (-w / 2, 0, -d / 2), size, pivot=pivot,
                  rotation=rotation, motion=motion)
    for face in box.sides:
        for y in range(face.h):
            for x in range(face.w):
                face.set(x, y, k(role, base + 1 if y % 2 == 0 else base - 1 if (x + y // 2) % 3 == 0 else base))
    for face in (box.top, box.bottom):
        face.fill(k(role, base))
        if face.w >= 3 and face.h >= 3:
            face.set(face.w // 2, face.h // 2, k(role, base - 2))
    return box


# -- legs ------------------------------------------------------------------------------------
def knit_stockings(g, role: str, rows, base: int = 3, seed: int = 0):
    """Knitted wool stockings on the bare leg: soft stitch columns and a darker seam up the back."""
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, role, "knit", seed + (side == "left"), base, rows[0], rows[1])
        leg.back.vline(1 if side == "right" else 2, rows[0], rows[1], k(role, base - 1))


def low_shoes(g, role: str = "L", base: int = 2, top: int = 10, sole: str = "K1", buckle: str | None = None,
              seed: int = 0):
    """Plain low shoes: a lit throat edge, a dark sole, an optional buckle on the instep."""
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, role, "smooth", seed + 1, base - 1, top, 11)
        for face in pants.sides:
            fabric(face, role, "smooth", seed + 2, base, 0, top, face.w, 12 - top)
            face.hline(0, face.w - 1, top, k(role, base + 1))
            face.hline(0, face.w - 1, 11, sole)
        if buckle:
            pants.front.set(1, top, buckle), pants.front.set(2, top, buckle)
        leg.bottom.fill(sole), pants.bottom.fill("K0")


def leg_piece(g, pid: str, side: str, origin, size, role: str, base: int = 2, texture: str = "plain", seed: int = 0,
              pivot=(0, 0, 0), rotation=(0, 0, 0), inflate: float = 0.0, motion: str = "none"):
    """A fully painted cuboid on one leg bone with an explicit origin (for asymmetric props)."""
    box = g.piece(f"{side}_{pid}", leg_bone(side), origin, size, pivot=pivot, rotation=rotation, inflate=inflate,
                  motion=motion)
    solid(box, role, texture, seed, base)
    return box
