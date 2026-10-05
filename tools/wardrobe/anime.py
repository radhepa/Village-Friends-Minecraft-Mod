"""Anime-inspired hair: clean cel shading, a bright 'angel ring' of sheen and tapered, pointed locks.

Faces are kept clear by the compiler: a fringe in front of the face may reach the brows (y >= -5.02
must stay outside |x| < 3), sidelocks hang outside the cheeks at |x| >= ~3.8.
"""
from __future__ import annotations

from paint import k, rnd


def cel_face(face, seed: int, base: int = 2, ring: int | None = None, clump: int = 3, tip_dark: bool = True):
    """Big flat strand clumps separated by thin shade lines, a broken sheen band, darker tips."""
    off = int(rnd(seed, 1) * clump)
    for y in range(face.h):
        for x in range(face.w):
            s = base
            if (x + off) % clump == 0 and y > 0:
                s -= 1
            if ring is not None and y in (ring, ring + 1) and (x + off) % clump != 0:
                s = base + (2 if y == ring and rnd(x, y, seed) > .25 else 1)
            if tip_dark and y == face.h - 1 and face.h > 2:
                s = min(s, base - 1)
            face.set(x, y, k("H", s))


def cel_box(box, seed: int, base: int = 2, ring: int | None = None, top_delta: int = 1, clump: int = 3):
    for f in box.sides:
        cel_face(f, seed + f.x0, base, ring, clump)
    for y in range(box.top.h):
        for x in range(box.top.w):
            box.top.set(x, y, k("H", base + top_delta - (1 if (x + y) % clump == 0 else 0)))
    box.bottom.fill(k("H", base - 2))


def lock(g, pid: str, pivot, rotation=(0, 0, 0), segments=((3, 3), (2, 2), (1, 1)), depth: int = 1, seed: int = 0,
         base: int = 2, ring: int | None = 1, motion: str = "none", z_offset: float = 0):
    """A tapered, pointed lock hanging along its local +y from the pivot: wide root to fine tip."""
    y = 0.0
    boxes = []
    for i, (w, h) in enumerate(segments):
        box = g.piece(f"{pid}_{i}" if len(segments) > 1 else pid, "HEAD", (-w / 2, y, -depth / 2 + z_offset), (w, h, depth),
                      pivot=pivot, rotation=rotation, motion=motion)
        cel_box(box, seed + i * 7, base, ring if i == 0 else None, top_delta=1 if i == 0 else 0)
        y += h
        boxes.append(box)
    return boxes


def spike(g, pid: str, pivot, rotation=(0, 0, 0), segments=((3, 2), (2, 2), (1, 1)), depth: int = 2, seed: int = 0, base: int = 2):
    """An upward spike (grows along local -y), for crowns."""
    y = 0.0
    for i, (w, h) in enumerate(segments):
        y -= h
        box = g.piece(f"{pid}_{i}", "HEAD", (-w / 2, y, -depth / 2), (w, h, depth), pivot=pivot, rotation=rotation)
        cel_box(box, seed + i * 5, base + (1 if i == len(segments) - 1 else 0), None, top_delta=2)


def bangs(g, prefix: str, specs, seed: int = 0, base: int = 2, z: float = -4.35):
    """Pointed fringe: specs are (x, segments, rz). Central locks must stay above the eyes."""
    for i, (x, segments, rz) in enumerate(specs):
        lock(g, f"{prefix}_{i}", (x, -8.55, z), (-10, 0, rz), segments, 1, seed + i * 13, base, ring=0)


def sidelocks(g, prefix: str, length: int, seed: int = 0, base: int = 2, z: float = -3.3, x: float = 4.3, flare: float = 4,
              width: int = 2, taper: bool = True):
    """Long face-framing locks in front of the ears, ending in points."""
    for side, sign in (("right", -1), ("left", 1)):
        segs = [(width, length - 2), (1, 2)] if taper else [(width, length)]
        lock(g, f"{prefix}_{side}", (x * sign, -7.6, z), (0, 0, -flare * sign), segs, 1, seed + (sign > 0) * 31, base, ring=1)


def back_fan(g, prefix: str, specs, seed: int = 0, base: int = 2, z: float = 4.25, motion: str = "none"):
    """Locks hanging down the back of the head: specs are (x, segments, rz, rx)."""
    for i, (x, segments, rz, rx) in enumerate(specs):
        lock(g, f"{prefix}_{i}", (x, -7.6, z), (rx, 0, rz), segments, 1, seed + i * 11, base, ring=1, motion=motion)


def ring_shell(g, seed: int, base: int = 2, side_rows: int = 4, back_rows: int = 7, ring_row: int = 1):
    """Hat-layer hair with a clean sheen band, for anime styles."""
    hat = g.part("hat")
    for y in range(8):
        for x in range(8):
            hat.top.set(x, y, k("H", base + 1 - (1 if (x + y * 3) % 5 == 0 else 0)))
    for face, rows in ((hat.back, back_rows), (hat.right, side_rows), (hat.left, side_rows)):
        sub = type(face)(face.layer, face.x0, face.y0, face.w, rows, face.name)
        cel_face(sub, seed + face.x0, base, ring_row, tip_dark=False)
        for x in range(face.w):
            if rnd(x, rows, seed) < .55 and rows < 8:
                face.set(x, rows, k("H", base - 1))
    hat.front.hline(0, 7, 0, k("H", base))
    return hat
