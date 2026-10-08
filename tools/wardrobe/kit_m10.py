"""Helpers for the everyday village basics batch (tops t346-t370, bottoms b346-b370).

Small brushes and props these plain garments share: sewn patches, channel quilting, cable knit,
hanging tie ends and loose cuff rings. Like kit.py, everything paints key colors only and returns
what it creates; each garment keeps its own identity (cut, collar, closure) in its own module.
"""
from __future__ import annotations

from kit import SIDES, arm_bone, arm_x, leg_bone
from paint import fabric, k, solid


def patch(face, x0: int, y0: int, w: int, h: int, role: str, base: int = 2, texture: str = "weave", seed: int = 0,
          stitch: str | None = None):
    """A sewn-on patch: its own cloth, a lit top edge, a shaded lower edge and running stitches at the sides."""
    fabric(face, role, texture, seed, base, x0, y0, w, h)
    face.hline(x0, x0 + w - 1, y0, k(role, base + 1))
    face.hline(x0, x0 + w - 1, y0 + h - 1, k(role, base - 1))
    if stitch:
        for y in range(y0, y0 + h, 2):
            face.set(x0, y, stitch), face.set(x0 + w - 1, y + 1 if y + 1 < y0 + h else y, stitch)


def channels(face, role: str, base: int = 2, period: int = 3, vertical: bool = False, rows=None, cols=None,
             offset: int = 0):
    """Channel quilting: a stitched seam every `period` texels, the puffed tube between it catching a few glints."""
    for y in rows if rows is not None else range(face.h):
        for x in cols if cols is not None else range(face.w):
            along, across = (y, x) if vertical else (x, y)
            p = (across + offset) % period
            glint = p == 1 and (along + (across + offset) // period) % 3 == 0
            face.set(x, y, k(role, base - 1) if p == 0 else k(role, base + 1) if glint else k(role, base))


def cable(face, x: int, y0: int, y1: int, role: str = "P", base: int = 2):
    """A two-stitch cable twisting down columns x and x + 1, sunk between purl columns."""
    for y in range(y0, y1 + 1):
        lit = (y // 2) % 2
        face.set(x, y, k(role, base + 1) if lit else k(role, base))
        face.set(x + 1, y, k(role, base) if lit else k(role, base + 1))
        face.set(x - 1, y, k(role, base - 1)), face.set(x + 2, y, k(role, base - 1))


def tie(g, pid: str, bone: str, pivot, role: str = "A", length: int = 2, base: int = 2, seed: int = 0,
        rotation=(0, 0, 0), motion: str = "sway"):
    """A short hanging tie end (lace, drawstring, cord or garter tail)."""
    box = g.piece(pid, bone, (-.5, 0, -.5), (1, length, 1), pivot=pivot, rotation=rotation, motion=motion)
    solid(box, role, "plain", seed, base, edge=False)
    box.strip.hline(0, box.strip.w - 1, length - 1, k(role, base - 1))
    return box


def arm_ring(g, pid: str, side: str, y: float, size, role: str, base: int = 2, texture: str = "weave", seed: int = 0,
             out: float = .5, dz: float = 0.0, inflate: float = 0.0):
    """A loose ring round one arm, pushed outward so its inner face stays clear of the torso.

    The bottom face is painted deep, so a wide ring reads as an open sleeve end.
    """
    w, h, d = size
    cx = arm_x(side) + 2.0 + (-out if side == "right" else out)
    box = g.piece(pid, arm_bone(side), (cx - w / 2, y, -d / 2 + dz), size, inflate=inflate)
    solid(box, role, texture, seed, base)
    box.bottom.fill(k(role, base - 2))
    return box


def leg_ring(g, pid: str, side: str, y: float, size, role: str, base: int = 2, texture: str = "weave", seed: int = 0,
             dx: float = 0.0, dz: float = 0.0, inflate: float = 0.0, open_bottom: bool = True):
    """A ring round one leg (cuffs, gathers, boot tops); optionally an open, deep-shaded bottom."""
    w, h, d = size
    box = g.piece(pid, leg_bone(side), (-w / 2 + dx, y, -d / 2 + dz), size, inflate=inflate)
    solid(box, role, texture, seed, base)
    if open_bottom:
        box.bottom.fill(k(role, base - 2))
    return box


def outer(box, side: str):
    """The outward-facing side face of a limb box."""
    return box.right if side == "right" else box.left


def inner(box, side: str):
    return box.left if side == "right" else box.right


__all__ = ["SIDES", "patch", "channels", "cable", "tie", "arm_ring", "leg_ring", "outer", "inner"]
