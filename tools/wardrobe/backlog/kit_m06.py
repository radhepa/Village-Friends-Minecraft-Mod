"""Shared helpers for the m06 batch of men's court and town wear (tops t246-t270, bottoms b246-b270).

Close-fitting hose, long robe skirts, chain links, fur facings and fleece. Like kit.py, every helper
paints key colors only and returns what it creates; a garment's identity (its badge, chain, props or
cut) stays in its own module.
"""
from __future__ import annotations

from kit import SIDES, flaps, waistband
from kit_male import blk
from paint import fabric, k, rnd, strip_fabric


# -- bottoms ---------------------------------------------------------------------------------
def hose(g, role: str, seed: int, base: int = 2, texture: str = "weave", rows=(0, 9), waist: bool = True):
    """Close hose: no crease, a shaded back seam and inseam, and the hose's own waistband."""
    legs = []
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, role, texture, seed + (side == "left"), base, rows[0], rows[1])
        if rows[0] == 0:
            fabric(leg.top, role, texture, seed, base)
        leg.back.vline(1 if side == "right" else 2, rows[0], rows[1], k(role, base - 1))
        inner = leg.left if side == "right" else leg.right
        inner.vline(1 if side == "right" else 2, rows[0], rows[1], k(role, base - 1))
        legs.append(leg)
    if waist:
        waistband(g, role, texture, seed + 2, base)
    return legs


def lower_legs(g, role: str, seed: int, base: int = 2, texture: str = "weave", rows=(6, 9), overlay: bool = False):
    """Recolor a band of both legs (stockings below breeches, canions, boot shafts)."""
    for side in SIDES:
        strip_fabric(g.part(f"{side}_leg"), role, texture, seed + (side == "left"), base, rows[0], rows[1])
        if overlay:
            strip_fabric(g.part(f"{side}_pants"), role, texture, seed + 3 + (side == "left"), base, rows[0], rows[1])


# -- tops ------------------------------------------------------------------------------------
def robe_skirts(g, prefix: str, length: int, role: str, texture: str, seed: int, base: int = 2, top: float = 10.8,
                side_len: int | None = None, width: int = 9):
    """Long gown skirts: front/back panels at the hem planes that follow the stride, plus side panels."""
    front, back = flaps(g, prefix, length, role, texture, seed, width=width, base=base, top=top)
    sides = []
    for name, x in (("right", -4.5), ("left", 4.5)):
        sides.append(blk(g, f"{prefix}_{name}", (x, top, 0), (1, side_len or length - 1, 4), role, base, texture,
                         seed + 2))
    return front, back, sides


# -- cloth and metal patterns ----------------------------------------------------------------
def chain_links(box, a: str = "M3", b: str = "M1"):
    """Paint a cuboid as a run of chunky links: alternating lit and shaded texels."""
    for f in box.faces:
        for y in range(f.h):
            for x in range(f.w):
                f.set(x, y, a if (x + y) % 2 == 0 else b)


def fur_patch(face, x0: int, y0: int, w: int, h: int, role: str = "S", seed: int = 0, base: int = 3):
    """Soft fur in slanted locks over a rectangle (facings, cuffs, hems)."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            lock = (x + face.x0 + (y + face.y0) // 2) % 3
            r = rnd(x + face.x0, y + face.y0, seed)
            key = k(role, base + 1) if lock == 0 and r < .6 else k(role, base - 1) if lock == 2 and r < .25 else k(role, base)
            face.set(x, y, key)


def fleece(face, role: str = "S", base: int = 3, rows=None, cols=None):
    """Tight fleece curls: 2x2 cells with a lit crown and a shaded underside, rows offset."""
    for y in rows if rows is not None else range(face.h):
        for x in cols if cols is not None else range(face.w):
            gx, gy = (x + face.x0 + (y // 2) % 2) % 2, y % 2
            face.set(x, y, k(role, base + 1) if (gx, gy) == (0, 0) else k(role, base - 1) if (gx, gy) == (1, 1)
                     else k(role, base))


def brocade(face, role: str = "P", thread: str = "M2", motif: str = "A2", base: int = 2, ox: int = 0, rows=None):
    """Ogival brocade: a lattice of gold thread enclosing a small pomegranate in each cell."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            cx, cy = (x + ox + face.x0) % 6, y % 8
            row_shift = 3 if (y // 8) % 2 else 0
            cx = (x + ox + face.x0 + row_shift) % 6
            if (cy in (0, 1) and cx == 0) or (cy in (2, 6) and cx in (1, 5)) or (cy in (3, 4, 5) and cx == 0) and False:
                key = thread
            elif cy == 0 and cx in (2, 3):
                key = thread
            elif cy in (1, 7) and cx in (1, 4):
                key = thread
            elif cy in (2, 6) and cx in (0, 5):
                key = thread
            elif cy in (3, 4, 5) and cx == 0:
                key = thread
            elif cy == 4 and cx in (2, 3):
                key = motif
            elif cy == 3 and cx in (2, 3):
                key = k(motif[0], int(motif[1]) + 1)
            else:
                key = k(role, base)
            face.set(x, y, key)
