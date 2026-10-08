"""Shared helpers for the travel, road, forest and mountain batch (tops t271-t295, bottoms b271-b295).

Small brushes and prop builders only: straps, stitched patches, graded dust, rope, round discs,
square coils and hafted tools. Each garment's identity (its cut, trade props and trim) stays in
its own module. Everything paints key colors and returns what it creates.
"""
from __future__ import annotations

from kit import SIDES, leg_bone
from paint import fabric, k, line, rnd, solid
from wardrobe import shade


# -- brushes ---------------------------------------------------------------------------------
def strap(face, x0: int, y0: int, x1: int, y1: int, key: str = "L2", edge: str | None = "L1"):
    """A two-texel diagonal strap: a main line with a darker edge line beside it."""
    if edge:
        line(face, x0 + 1, y0, x1 + 1, y1, edge)
    line(face, x0, y0, x1, y1, key)


def baldric(front, back, from_left: bool = True, key: str = "L2", edge: str | None = "L1", y1: int = 10):
    """A strap over one shoulder to the opposite hip, painted on a front and a back face.

    from_left: it rises from the wearer's left shoulder (front x 6, back x 1) to the right hip.
    """
    if from_left:
        strap(front, 6, 0, 0, y1, key, edge), strap(back, 0, 0, 6, y1, key, edge)
    else:
        strap(front, 0, 0, 6, y1, key, edge), strap(back, 6, 0, 0, y1, key, edge)


def patch(face, x0: int, y0: int, w: int, h: int, fill: str, stitch: str | None = None):
    """A sewn-on patch: a flat fill with a shaded lower and outer edge, and optional tacking
    stitches every other texel along its top edge."""
    dark = shade(fill, -1)
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            face.set(x, y, dark if y == y0 + h - 1 or x == x0 + w - 1 else fill)
    if stitch:
        for x in range(x0, x0 + w - 1, 2):
            face.set(x, y0, stitch)


def dust(face, key: str, seed: int, y0: int, y1: int, d0: float = .02, d1: float = .3, cols=None):
    """Dust, mud or chips that thicken toward row y1."""
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0)
        density = d0 + (d1 - d0) * t
        for x in cols if cols is not None else range(face.w):
            if rnd(x + face.x0, y + face.y0, seed) < density:
                face.set(x, y, key)


def rope_face(face, role: str = "S", base: int = 2):
    """Twisted rope: lit and shaded diagonal plies."""
    for y in range(face.h):
        for x in range(face.w):
            p = (x + y) % 3
            face.set(x, y, k(role, base + 1 if p == 0 else base - 1 if p == 2 else base))


def rope(box, role: str = "S", base: int = 2):
    for face in box.faces:
        rope_face(face, role, base)
    return box


# -- props -----------------------------------------------------------------------------------
def disc(g, pid: str, pivot, diameter: int, role: str, base: int = 2, depth: int = 1, bone: str = "TORSO",
         rotation=(0, 0, 0), texture: str = "smooth", seed: int = 0, motion: str = "none"):
    """A round flat disc (pan, wheel, shield boss) built as a plus of two boxes; returns (wide, tall).

    The disc faces the z axis, centred on the pivot. The tall box is inflated a hair so it wins
    where the two overlap.
    """
    n, m = diameter, diameter - 2
    wide = g.piece(f"{pid}_wide", bone, (-n / 2, -m / 2, -depth / 2), (n, m, depth), pivot=pivot,
                   rotation=rotation, motion=motion)
    tall = g.piece(f"{pid}_tall", bone, (-m / 2, -n / 2, -depth / 2), (m, n, depth), pivot=pivot,
                   rotation=rotation, inflate=.02, motion=motion)
    for box in (wide, tall):
        solid(box, role, texture, seed, base, edge=False)
    return wide, tall


def ring_marks(face, cx: float, cy: float, r: float, key: str, ox: int = 0, oy: int = 0):
    """Paint the texels of a face that lie on a circle of radius r around (cx, cy) in disc space."""
    for y in range(face.h):
        for x in range(face.w):
            d = ((x + ox + .5 - cx) ** 2 + (y + oy + .5 - cy) ** 2) ** .5
            if abs(d - r) < .5:
                face.set(x, y, key)


def coil(g, pid: str, pivot, size: int = 5, thick: int = 1, depth: int = 2, role: str = "S", base: int = 2,
         rotation=(0, 0, 0), bone: str = "TORSO", motion: str = "none", painter=rope, hang: bool = False):
    """A square ring of four bars (rope coil, snare, chain loop) standing in the x-y plane.

    Centred on the pivot, or hanging from it (hang=True) so a flap or sway motion swings it from its top.
    """
    s, t = size, thick
    dy = s / 2 if hang else 0
    bars = [("top", (-s / 2, -s / 2 + dy, -depth / 2), (s, t, depth)),
            ("bottom", (-s / 2, s / 2 - t + dy, -depth / 2), (s, t, depth)),
            ("right", (-s / 2, -s / 2 + t + dy, -depth / 2), (t, s - 2 * t, depth)),
            ("left", (s / 2 - t, -s / 2 + t + dy, -depth / 2), (t, s - 2 * t, depth))]
    out = []
    for name, origin, dims in bars:
        box = g.piece(f"{pid}_{name}", bone, origin, dims, pivot=pivot, rotation=rotation, motion=motion)
        painter(box, role, base)
        out.append(box)
    return out


def stick(g, pid: str, pivot, length: int, role: str = "L", base: int = 3, rotation=(0, 0, 0), bone: str = "TORSO",
          seed: int = 0, centered: bool = True, motion: str = "none", texture: str = "plain"):
    """A 1x1 haft or pole; centred on its pivot (or hanging from it when centered=False)."""
    y = -length / 2 if centered else 0
    box = g.piece(pid, bone, (-.5, y, -.5), (1, length, 1), pivot=pivot, rotation=rotation, motion=motion)
    solid(box, role, texture, seed, base, edge=False)
    for face in box.sides:
        for yy in range(face.h):
            if (yy + face.x0) % 4 == 0:
                face.set(0, yy, k(role, base - 1))                     # wood grain
    return box


def hang(g, pid: str, pivot, size, role: str, base: int = 2, texture: str = "plain", seed: int = 0,
         bone: str = "TORSO", rotation=(0, 0, 0)):
    """A small swinging thing hung by its top centre (cup, bell, tag, pelt)."""
    w, h, d = size
    box = g.piece(pid, bone, (-w / 2, 0, -d / 2), size, pivot=pivot, rotation=rotation, motion="sway")
    solid(box, role, texture, seed, base)
    return box


def leg_shell(g, pid: str, y: float, height: int, role: str, base: int = 2, texture: str = "weave", seed: int = 0,
              size: int = 5, inflate: float = 0.0):
    """A cuboid shell around each lower leg (gaiter, boot shaft, wrap); returns [right, left]."""
    out = []
    for i, side in enumerate(SIDES):
        # The left shell stands a hair proud so the two never z-fight where they meet between the knees.
        box = g.piece(f"{side}_{pid}", leg_bone(side), (-size / 2, y, -size / 2), (size, height, size),
                      inflate=inflate + .03 * i)
        solid(box, role, texture, seed + i, base)
        fabric(box.top, role, texture, seed + i, base + 1)
        out.append(box)
    return out


def outer(box, side: str):
    """The outward-facing side face of a leg or arm box."""
    return box.right if side == "right" else box.left


def inner(box, side: str):
    return box.left if side == "right" else box.right
