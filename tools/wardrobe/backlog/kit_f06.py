"""Helpers for the f06 batch: women's noble court and town wear (tf186-tf210, bf186-bf210).

Small building blocks only: a generic prop cuboid, girdle charms that ride the stride in front of
any skirt, a floor train, bows, and the two woven patterns shared by a top and its skirt (cut
velvet and tablet weave). Each garment keeps its own identity in its own module.
"""
from __future__ import annotations

from kit_female import OVER_FRONT, OVER_TOP_MAX, SKIRT_BACK, SKIRT_FRONT
from paint import k, solid
from wardrobe import Face

HANG_Z = OVER_FRONT - .15          # girdle charms hang in front of every skirt and over-layer
BOTTOM_HANG_Z = SKIRT_FRONT - .12  # a bottom's own panels/charms: in front of its skirt, behind top over-layers


def prop(g, pid: str, size, pivot, role: str = "M", base: int = 3, texture: str = "smooth", seed: int = 0,
         bone: str = "TORSO", origin=None, rotation=(0, 0, 0), motion: str = "none", inflate: float = 0.0,
         edge: bool = False, scale=None):
    """A fully painted cuboid; by default centred on its pivot in x and z, hanging down from it."""
    w, h, d = size
    o = origin if origin is not None else (-w / 2, 0, -d / 2)
    box = g.piece(pid, bone, o, size, pivot=pivot, rotation=rotation, motion=motion, inflate=inflate, scale=scale)
    solid(box, role, texture, seed, base, edge=edge)
    return box


def charm(g, pid: str, x: float, size, drop: float = 0.0, role: str = "M", base: int = 3, texture: str = "smooth",
          seed: int = 0, top: float = 8.8, ox: float = 0.0, dz: float = 0.0, rotation=(0, 0, 0), inflate: float = 0.0,
          edge: bool = False, z: float = HANG_Z, motion: str = "flap_front"):
    """Something hung from a girdle at (x, top): it rides the leading leg like an apron, so a stride never
    pushes a skirt through it. `drop` is the gap from the hinge to the item's top; the item's back face
    sits one texel behind the hinge plane."""
    w, h, d = size
    top = min(top, OVER_TOP_MAX)
    return prop(g, pid, size, (x, top, z), role, base, texture, seed, origin=(-w / 2 + ox, drop, 1 - d + dz),
                rotation=rotation, motion=motion, inflate=inflate, edge=edge)


def train(g, pid: str, top: float, y: float, width: int, depth: int, role: str = "P", texture: str = "velvet",
          seed: int = 0, base: int = 2):
    """A train lying on the floor behind a skirt, hinged with the back panel so it rides the trailing leg.
    `y` is the drop from the hinge to the train (top + y + 1 should be about 23.6, the floor)."""
    box = g.piece(pid, "TORSO", (-width / 2, y, 1), (width, 1, depth), pivot=(0, top, SKIRT_BACK), motion="flap_back")
    solid(box, role, texture, seed, base)
    return box


def bow(g, pid: str, pivot, role: str = "A", base: int = 2, bone: str = "TORSO", width: int = 3,
        tails: int = 0, motion: str = "none", tail_motion: str = "sway"):
    """A ribbon bow: two loops and a knot, with optional hanging tails. Returns the loop box."""
    loops = g.piece(f"{pid}", bone, (-width / 2, -.5, -.5), (width, 1, 1), pivot=pivot, motion=motion)
    solid(loops, role, "plain", 56990, base, edge=False)
    for f in loops.sides:
        f.set(0, 0, k(role, base + 1)), f.set(f.w - 1, 0, k(role, base + 1))
    loops.front.set(width // 2, 0, k(role, base - 1))
    knot = g.piece(f"{pid}_knot", bone, (-.5, -.5, -.6), (1, 1, 1), pivot=pivot, inflate=.08, motion=motion)
    solid(knot, role, "plain", 56991, base - 1, edge=False)
    knot.front.set(0, 0, k(role, base))
    if tails:
        for i, (dx, rz) in enumerate(((-.5, 12), (.5, -12))):
            t = g.piece(f"{pid}_tail{i}", bone, (-.5, 0, -.5), (1, tails, 1), pivot=(pivot[0] + dx, pivot[1] + .3, pivot[2]),
                        rotation=(0, 0, rz), motion=tail_motion)
            solid(t, role, "plain", 56992 + i, base)
            t.strip.hline(0, t.strip.w - 1, tails - 1, k(role, base - 1))
    return loops


# -- woven patterns shared by a top and its skirt ------------------------------------------------
# Cut velvet: raised pile (lit) standing out of a voided ground in a curling leaf-and-scroll repeat.
CUT_VELVET = [
    "..vvv...",
    ".v...v..",
    "v..p..v.",
    "v.ppp.v.",
    ".v.p.v..",
    "..v.v...",
    "...v....",
    "...v....",
]


def cut_velvet(face: Face, role: str = "P", base: int = 2, x0: int = 0, y0: int = 0, w: int | None = None,
               h: int | None = None, gold: str | None = None, offset: int = 0):
    """Pile cloth with a voided pattern: 'v' is the cut-away ground (deep), 'p' a gilt or lit bud."""
    w = face.w - x0 if w is None else w
    h = face.h - y0 if h is None else h
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            gx, gy = x + face.x0 + offset, y
            row = (gy // 8) % 2
            ch = CUT_VELVET[gy % 8][(gx + row * 4) % 8]
            if ch == "v":
                key = k(role, base - 2)
            elif ch == "p":
                key = gold or k(role, base + 2)
            else:
                key = k(role, base + (1 if (gx + gy) % 7 == 0 else 0))
            face.set(x, y, key)


# Tablet weave: a four-row band with framing threads and a running diamond chain between them.
TABLET = ["eeee", "a.b.", ".ab.", "eeee"]
TABLET_ALT = ["eeee", "ab..", "..ab", "eeee"]


def tablet_band(face: Face, y: int, a: str = "A2", b: str = "M3", ground: str = "S3", edge: str = "K1",
                x0: int = 0, x1: int | None = None, alt: bool = False, offset: int = 0):
    """A tablet-woven band four rows deep starting at row y; returns the rows used."""
    rows = TABLET_ALT if alt else TABLET
    x1 = face.w - 1 if x1 is None else x1
    for dy, row in enumerate(rows):
        for x in range(x0, x1 + 1):
            ch = row[(x + face.x0 + offset) % 4]
            face.set(x, y + dy, {"e": edge, "a": a, "b": b, ".": ground}[ch])
    return len(rows)


def tablet_column(face: Face, x: int, y0: int, y1: int, a: str = "A2", b: str = "M3", ground: str = "S3",
                  edge: str = "K1"):
    """A tablet-woven strip running down two columns (x, x+1) between framing threads at x-1 and x+2."""
    for y in range(y0, y1 + 1):
        face.set(x - 1, y, edge), face.set(x + 2, y, edge)
        phase = y % 4
        face.set(x, y, a if phase in (0, 1) else ground)
        face.set(x + 1, y, b if phase in (2, 3) else ground)
        if phase == 1:
            face.set(x + 1, y, a)
        if phase == 3:
            face.set(x, y, b)
