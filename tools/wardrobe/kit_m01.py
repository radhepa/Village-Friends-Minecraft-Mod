"""Shared helpers for the men's field, farm and orchard batch (tops t121-t145, bottoms b121-b145).

Small brushes and props that several farm pieces reuse: wicker, twisted rope and straw, mud and
stains, piebald hide, stitched patches and hanging tools. Like kit.py, everything paints key colors
only and returns what it creates; each garment keeps its own identity in its own module.
"""
from __future__ import annotations

from kit import SIDES, leg_bone
from paint import k, rnd, solid


# -- brushes ---------------------------------------------------------------------------------
def wicker(face, role: str = "L", base: int = 2, ox: int = 0, rows=None, rim: bool = True):
    """Basket weave: weavers passing over and under upright stakes, a lit rim on the top row."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            over = (x + ox + y) % 2 == 0
            face.set(x, y, k(role, base + 1 if over else base - 1 if (x + ox) % 2 else base))
    if rim and rows is None:
        face.hline(0, face.w - 1, 0, k(role, base + 2))


def twist(face, role: str = "S", base: int = 3, rows=None, ox: int = 0, period: int = 3):
    """Twisted rope or straw: slanted strands, a lit and a shaded twist per period."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            p = (x + ox + y) % period
            face.set(x, y, k(role, base + 1) if p == 0 else k(role, base - 1) if p == period - 1 else k(role, base))


def twisted_box(box, role: str = "S", base: int = 3, ox: int = 0):
    for face in box.sides:
        twist(face, role, base, ox=ox + face.x0)
    box.top.fill(k(role, base + 1)), box.bottom.fill(k(role, base - 1))


def value_noise(x: int, y: int, seed: int, cell: int = 4) -> float:
    """Smooth blobs: bilinear value noise on a coarse grid (for hide patches and stains)."""
    cx, cy = x // cell, y // cell
    fx, fy = (x % cell) / cell, (y % cell) / cell
    a, b = rnd(cx, cy, seed), rnd(cx + 1, cy, seed)
    c, d = rnd(cx, cy + 1, seed), rnd(cx + 1, cy + 1, seed)
    top, bot = a + (b - a) * fx, c + (d - c) * fx
    return top + (bot - top) * fy


def piebald(face, seed: int, light: str = "S", dark: str = "K", ox: int = 0, oy: int = 0, cell: int = 4,
            threshold: float = .5, rows=None, light_base: int = 4, dark_base: int = 1):
    """Black-and-white cow hide: soft-edged dark blots on a pale ground, short hair texture."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            v = value_noise(x + ox + face.x0, y + oy + face.y0, seed, cell)
            hair = (x + y) % 3 == 0
            if v < threshold:
                face.set(x, y, k(dark, dark_base + (1 if hair and v > threshold - .06 else 0)))
            else:
                face.set(x, y, k(light, light_base - (1 if hair else 0)))


def mud(face, seed: int, top: int, role: str = "L", base: int = 1, rows=None, splash: float = .18, ragged: bool = True):
    """Mud caked from row `top` down: a ragged upper edge, darker clods, and splashes above it."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            edge = top + (1 if ragged and rnd(x + face.x0, 3, seed) < .4 else 0) - (1 if ragged and rnd(x + face.x0, 5, seed) < .25 else 0)
            if y >= edge:
                r = rnd(x + face.x0, y + face.y0, seed + 1)
                face.set(x, y, k(role, base - 1 if r < .25 else base + 1 if r > .85 else base))
            elif y >= edge - 3 and rnd(x + face.x0, y + face.y0, seed + 2) < splash:
                face.set(x, y, k(role, base + (1 if rnd(x, y, seed + 3) < .5 else 0)))


def stains(face, key: str, seed: int, density: float = .12, rows=None, cols=None, cell: int = 3, blot: float = .78):
    """Splashed stains: soft blots plus a scatter of drops (grape, whey, wax, peat)."""
    for y in rows if rows is not None else range(face.h):
        for x in cols if cols is not None else range(face.w):
            v = value_noise(x + face.x0, y + face.y0, seed, cell)
            if v > blot or rnd(x + face.x0, y + face.y0, seed + 9) < density:
                face.set(x, y, key)


def patch(face, x0: int, y0: int, w: int, h: int, role: str, base: int = 2, stitch: str | None = None, texture=None):
    """A sewn-on patch: plain cloth with a dashed running stitch round its edge."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            edge = x in (x0, x0 + w - 1) or y in (y0, y0 + h - 1)
            if edge:
                face.set(x, y, stitch if stitch and (x + y) % 2 == 0 else k(role, base - 1))
            else:
                face.set(x, y, k(role, base + (1 if texture == "lit" and y == y0 + 1 else 0)))


def gathers(face, role: str, base: int, rows, ox: int = 0):
    """Gathered cloth: alternating lit and shaded pleat columns."""
    for y in rows:
        for x in range(face.w):
            face.set(x, y, k(role, base + 1 if (x + ox) % 2 == 0 else base - 1))


# -- props -----------------------------------------------------------------------------------
def rod(g, pid: str, pivot, length: int, role: str = "L", base: int = 3, rotation=(0, 0, 0), bone: str = "TORSO",
        seed: int = 0, motion: str = "none", thick: int = 1, end: str | None = None):
    """A straight wooden shaft centred on its pivot (handles, goads, stakes, crooks)."""
    box = g.piece(pid, bone, (-thick / 2, -length / 2, -thick / 2), (thick, length, thick), pivot=pivot,
                  rotation=rotation, motion=motion)
    solid(box, role, "plain", seed, base, edge=False)
    for face in box.sides:
        for y in range(1, length, 4):
            face.set(0, y, k(role, base - 1))                                        # grain knots
        face.set(face.w - 1, 0, k(role, base + 1))
    if end:
        box.strip.hline(0, box.strip.w - 1, 0, end)
        box.top.fill(end)
    return box


def hanging_basket(g, pid: str, pivot, size, role: str = "L", base: int = 2, bone: str = "TORSO", rotation=(0, 0, 0),
                   handle: bool = True, motion: str = "none"):
    """A wicker basket whose top centre sits at the pivot; an arched handle above it."""
    w, h, d = size
    box = g.piece(pid, bone, (-w / 2, 0, -d / 2), size, pivot=pivot, rotation=rotation, motion=motion)
    for face in box.sides:
        wicker(face, role, base, face.x0)
    box.top.fill(k(role, base - 2)), box.bottom.fill(k(role, base - 1))
    out = [box]
    if handle:
        # An arched handle: a bar across the top on two short uprights at the basket's ends.
        bar = g.piece(f"{pid}_handle", bone, (-w / 2 + .5, -2.2, -.5), (w - 1, 1, 1), pivot=pivot,
                      rotation=rotation, motion=motion)
        solid(bar, role, "plain", 0, base + 1, edge=False)
        bar.top.fill(k(role, base + 2))
        out.append(bar)
        for i, x in enumerate((-w / 2 + .5, w / 2 - 1.5)):
            post = g.piece(f"{pid}_handle_{i}", bone, (x, -1.2, -.5), (1, 1, 1), pivot=pivot, rotation=rotation,
                           motion=motion)
            solid(post, role, "plain", 0, base, edge=False)
            out.append(post)
    return out


def tuft(g, pid: str, pivot, size=(1, 1, 1), role: str = "S", base: int = 4, bone: str = "TORSO", rotation=(0, 0, 0),
         inflate: float = .05):
    """A little 3D wisp or tuft (fleece, straw, feathers): lit top, shaded under."""
    w, h, d = size
    box = g.piece(pid, bone, (-w / 2, -h / 2, -d / 2), size, pivot=pivot, rotation=rotation, inflate=inflate)
    solid(box, role, "plain", 0, base, edge=False)
    box.top.fill(k(role, min(4, base + 1)))
    box.bottom.fill(k(role, base - 2))
    for face in box.sides:
        face.set(0, face.h - 1, k(role, base - 1))
    return box


def leg_tube(g, pid: str, y: float, h: int, role: str, base: int = 2, texture: str = "leather", seed: int = 0,
             size_xz: int = 5, inflate: float = 0.0):
    """A cuboid around each lower leg from leg-local height y (gaiters, boot shafts, wraps)."""
    out = []
    for i, side in enumerate(SIDES):
        box = g.piece(f"{side}_{pid}", leg_bone(side), (-size_xz / 2, y, -size_xz / 2), (size_xz, h, size_xz),
                      inflate=inflate)
        solid(box, role, texture, seed + i, base)
        out.append(box)
    return out


def outer(box, side: str):
    """The outward-facing side of a leg or arm box."""
    return box.right if side == "right" else box.left


def inner(box, side: str):
    return box.left if side == "right" else box.right
