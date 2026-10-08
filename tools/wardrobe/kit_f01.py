"""Small helpers for the women's farm, dairy and field batch (tf/bf 061-085).

Wicker, bundles of stalks, wooden handles, round produce and twisted straw bands. They paint key
colors only and return the boxes they create; each garment keeps its own identity in its module.
"""
from __future__ import annotations

from paint import k, rnd, solid


def wicker(face, role: str = "L", base: int = 2, x0: int = 0, y0: int = 0, w: int | None = None,
           h: int | None = None, offset: int = 0):
    """Basket weave: rows of weavers passing over and under the stakes, two texels per step."""
    w = face.w - x0 if w is None else w
    h = face.h - y0 if h is None else h
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            row = (y - y0) // 2
            over = ((x - x0 + offset + row * 2) // 2) % 2 == 0
            top = (y - y0) % 2 == 0
            s = base + (1 if over and top else 0) - (0 if over else 1)
            face.set(x, y, k(role, s))


def stalks(face, role: str = "S", base: int = 2, seed: int = 0, y0: int = 0, y1: int | None = None, nodes: bool = True):
    """Parallel stalks running down a face: each column keeps its own tone, with a few joints."""
    y1 = face.h - 1 if y1 is None else y1
    for x in range(face.w):
        tone = rnd(x + face.x0, 3, seed)
        s = base + (1 if tone > .62 else 0) - (1 if tone < .28 else 0)
        for y in range(y0, y1 + 1):
            key = k(role, s)
            if nodes and (y + int(tone * 7)) % 6 == 0:
                key = k(role, s - 1)
            face.set(x, y, key)


def cut_ends(face, role: str = "S", base: int = 2):
    """The cut end of a bundle: rings of hollow stalks."""
    for y in range(face.h):
        for x in range(face.w):
            face.set(x, y, k(role, base - 1) if (x + y) % 2 else k(role, base + 1))


def bundle(g, pid: str, bone: str, pivot, size, rotation=(0, 0, 0), role: str = "S", base: int = 2, seed: int = 0,
           ties=(), tie: str = "L2", head_rows: int = 0, head=("M3", "M4"), motion: str = "none", origin=None):
    """A tied bundle of stalks (sheaves, rushes, flax, thatching straw); the head is the top rows."""
    w, h, d = size
    box = g.piece(pid, bone, origin or (-w / 2, -h / 2, -d / 2), size, pivot=pivot, rotation=rotation, motion=motion)
    for f in box.sides:
        stalks(f, role, base, seed + f.x0)
    cut_ends(box.top, role, base)
    cut_ends(box.bottom, role, base - 1)
    if head_rows:
        for f in box.sides:
            for y in range(head_rows):
                for x in range(f.w):
                    f.set(x, y, head[(x + y) % 2])
        for y in range(box.top.h):
            for x in range(box.top.w):
                box.top.set(x, y, head[(x + y + 1) % 2])
    for y in ties:
        for f in box.sides:
            f.hline(0, f.w - 1, y, tie)
    return box


def handle(g, pid: str, bone: str, pivot, length: int, rotation=(0, 0, 0), role: str = "L", base: int = 3,
           origin=None, motion: str = "none", seed: int = 0):
    """A wooden handle or stick, one texel thick, with a quiet grain."""
    box = g.piece(pid, bone, origin or (-.5, -length / 2, -.5), (1, length, 1), pivot=pivot, rotation=rotation,
                  motion=motion)
    solid(box, role, "smooth", seed, base, edge=False)
    for f in box.sides:
        for y in range(f.h):
            if (y + (f.x0 % 3)) % 4 == 0:
                f.set(0, y, k(role, base - 1))
    return box


def produce(g, pid: str, bone: str, pivot, size: int = 2, role: str = "A", base: int = 2, stem: str | None = "L1",
            rotation=(0, 0, 0), motion: str = "none", origin=None, seed: int = 0):
    """A round fruit, egg or root: a lit shoulder, a shaded underside and an optional stem on top."""
    s = size
    box = g.piece(pid, bone, origin or (-s / 2, -s / 2, -s / 2), (s, s, s), pivot=pivot, rotation=rotation,
                  motion=motion)
    solid(box, role, "plain", seed, base, edge=False)
    for f in box.sides:
        f.set(0, 0, k(role, base + 1))
        f.set(s - 1, s - 1, k(role, base - 1))
    box.top.fill(k(role, base + 1))
    box.bottom.fill(k(role, base - 1))
    if stem:
        box.top.set(s // 2, s // 2, stem)
    return box


def twist(face, y: int, a: str = "S2", b: str = "S1", x0: int = 0, x1: int | None = None, rows: int = 2):
    """A twisted straw band across a face: diagonal strands alternating light and dark."""
    x1 = face.w - 1 if x1 is None else x1
    for dy in range(rows):
        for x in range(x0, x1 + 1):
            face.set(x, y + dy, a if (x + dy) % 2 == 0 else b)
