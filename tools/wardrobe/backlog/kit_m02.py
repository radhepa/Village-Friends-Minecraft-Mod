"""Shared helpers for the craft-guild batch (men's tops and bottoms 146-170).

Small geometry and layout helpers only: hanging bars, open rings, apron bibs and apron panels.
Each garment keeps its identity (its tools, stains, trims and props) in its own module.
"""
from __future__ import annotations

from paint import fabric, k, line, solid


def bar(g, pid: str, pivot, size, role: str, base: int = 2, texture: str = "plain", seed: int = 0,
        bone: str = "TORSO", rotation=(0, 0, 0), motion: str = "none", anchor: str = "top", inflate: float = 0.0,
        edge: bool = False, offset=(0, 0, 0)):
    """A painted cuboid hung from its pivot (anchor 'top'), standing on it ('bottom') or centred on it ('centre').

    `offset` shifts the box away from the pivot, so several parts can share one pivot and swing as one prop.
    """
    w, h, d = size
    oy = {"top": 0, "bottom": -h, "centre": -h / 2}[anchor]
    ox, dy, oz = offset
    box = g.piece(pid, bone, (-w / 2 + ox, oy + dy, -d / 2 + oz), size, pivot=pivot, rotation=rotation,
                  motion=motion, inflate=inflate)
    solid(box, role, texture, seed, base, edge=edge)
    return box


def hoop(g, pid: str, pivot, size, role: str, base: int = 2, seed: int = 0, bone: str = "TORSO", rotation=(0, 0, 0),
         motion: str = "none", offset=(0, 0, 0), depth: int = 1, texture: str = "smooth"):
    """An open ring of four bars (outer w x h) facing forward, hung from its pivot; returns [top, bottom, right, left]."""
    w, h = size
    ox, oy, oz = offset
    specs = (("top", (-w / 2, 0), (w, 1)), ("bottom", (-w / 2, h - 1), (w, 1)),
             ("right", (-w / 2, 1), (1, h - 2)), ("left", (w / 2 - 1, 1), (1, h - 2)))
    bars = []
    for i, (name, (x, y), (bw, bh)) in enumerate(specs):
        b = g.piece(f"{pid}_{name}", bone, (x + ox, y + oy, -depth / 2 + oz), (bw, bh, depth), pivot=pivot,
                    rotation=rotation, motion=motion)
        solid(b, role, texture, seed + i, base, edge=False)
        fabric(b.top, role, texture, seed + i, base + 1)
        bars.append(b)
    return bars


def bib(jacket, role: str, texture: str, seed: int, x0: int = 1, x1: int = 6, y0: int = 2, y1: int = 11,
        base: int = 2, straps: str = "cross", strap: str | None = None):
    """An apron bib on the jacket front from row y0 down, hung from shoulder straps.

    straps: 'cross' (crossed on the back), 'neck' (a neck loop and a waist tie) or 'straight'.
    """
    f, b, top = jacket.front, jacket.back, jacket.top
    fabric(f, role, texture, seed, base, x0, y0, x1 - x0 + 1, y1 - y0 + 1)
    f.hline(x0, x1, y0, k(role, base + 1))
    sk = strap or k(role, base - 1)
    if y0 > 0:
        f.vline(x0, 0, y0 - 1, sk), f.vline(x1, 0, y0 - 1, sk)
    for y in range(top.h):
        top.set(x0, y, sk), top.set(x1, y, sk)
    bx0, bx1 = 7 - x1, 7 - x0
    if straps == "cross":
        line(b, bx0, 0, bx1, 9, sk), line(b, bx1, 0, bx0, 9, sk)
    elif straps == "straight":
        b.vline(bx0, 0, 9, sk), b.vline(bx1, 0, 9, sk)
    if straps in ("cross", "straight", "neck"):
        b.hline(0, 7, 9, sk)
        for side in (jacket.right, jacket.left):
            side.hline(0, side.w - 1, 9, sk)
    return f


def apron_panel(g, pid: str, width: int, length: int, role: str, texture: str = "weave", seed: int = 0,
                base: int = 2, top: float = 10.4, z: float = -3.15, x: float = 0.0, motion: str = "flap_front"):
    """An apron skirt hanging in front of the legs; it lies over any skirt panel (z -3.15) and follows the stride."""
    panel = g.piece(pid, "TORSO", (-width / 2, 0, 0), (width, length, 1), pivot=(x, top, z), motion=motion)
    solid(panel, role, texture, seed, base)
    panel.front.hline(0, width - 1, 0, k(role, base + 1))
    return panel


def dashes(face, x0: int, x1: int, y: int, key: str, step: int = 2, start: int = 0):
    """A running stitch: every `step`-th texel along a row."""
    for x in range(x0 + start, x1 + 1, step):
        face.set(x, y, key)


def vdashes(face, x: int, y0: int, y1: int, key: str, step: int = 2, start: int = 0):
    for y in range(y0 + start, y1 + 1, step):
        face.set(x, y, key)
