"""Shared extras for the f04 women's batch (warriors, guards and hunters, tf/bf 136-160).

Small geometry helpers for props that ride the stride (hip props), long shafts slung across the
back (spears, javelins, banner poles), a sword in its scabbard, and a few armour and cloth surfaces
(lamellae, plate lames, horizontal quilting, mud). Every helper paints key colors only and returns
what it built; each piece keeps its own identity in its module.
"""
from __future__ import annotations

import math

from paint import k, rnd, solid

FRONT_Z, BACK_Z = -2.35, 2.35     # hip props: back face just outside the jacket, in front of any over-layer
SLING_Z = 3.25                    # long props slung across the back: clear of the jacket and the swinging arms


class Rod:
    """A straight line on a bone from p0 to p1 (x, y in bone space) at depth z, for slung shafts and the like.

    `piece` places a box centred on the line: it starts `t` texels from p0 and runs `size[1]` texels on toward
    p1; `dx` shifts it across the line (toward the wearer's left when p1 is above p0) and `dz` in depth.
    """

    def __init__(self, g, p0, p1, z: float = SLING_Z, bone: str = "TORSO", motion: str = "none", tilt: float = 0.0):
        self.g, self.p0, self.z, self.bone, self.motion, self.tilt = g, p0, z, bone, motion, tilt
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        self.length = math.hypot(dx, dy)
        self.rz = round(math.degrees(math.atan2(dx, -dy)), 2)

    def at(self, t: float, dx: float = 0.0):
        """Bone-space (x, y) of the point t texels along the rod, dx across it."""
        a = math.radians(self.rz)
        return (self.p0[0] + dx * math.cos(a) + t * math.sin(a), self.p0[1] + dx * math.sin(a) - t * math.cos(a))

    def piece(self, pid: str, t: float, size, dx: float = 0.0, dz: float = 0.0, inflate: float = 0.0):
        w, h, d = size
        return self.g.piece(pid, self.bone, (dx - w / 2, -t - h, dz - d / 2), size, pivot=(self.p0[0], self.p0[1], self.z),
                            rotation=(self.tilt, 0, self.rz), motion=self.motion, inflate=inflate)

    def shaft(self, pid: str, t0: float, t1: float, role: str = "L", base: int = 2, seed: int = 0, width: int = 1,
              grain: bool = True):
        """A wooden shaft from t0 to t1 along the rod, with a lit grain line."""
        box = self.piece(pid, t0, (width, int(round(t1 - t0)), 1))
        solid(box, role, "smooth", seed, base, edge=False)
        if grain:
            for f in (box.front, box.back):
                f.vline(0, 0, f.h - 1, k(role, base + 1))
                for y in range(2, f.h, 5):
                    f.set(0, y, k(role, base - 1))
        return box


# -- props -------------------------------------------------------------------------------------
def front_prop(g, pid: str, x: float, size, drop: float = 0.0, top: float = 9.0, z: float = FRONT_Z,
               motion: str = "flap_front", rotation=(0, 0, 0)):
    """A box hung in front of the hips from a hinge at the belt; it rides the leading leg."""
    w, h, d = size
    return g.piece(pid, "TORSO", (-w / 2, drop, -d), size, pivot=(x, top, z), motion=motion, rotation=rotation)


def back_prop(g, pid: str, x: float, size, drop: float = 0.0, top: float = 9.0, z: float = BACK_Z,
              motion: str = "flap_back", rotation=(0, 0, 0)):
    """A box hung behind the hips from a hinge at the belt; it rides the trailing leg."""
    w, h, d = size
    return g.piece(pid, "TORSO", (-w / 2, drop, 0), size, pivot=(x, top, z), motion=motion, rotation=rotation)


def shaft(g, pid: str, pivot, up: float, down: float = 0.0, rotation=(0, 0, 0), x: float = 0.0, width: int = 1,
          depth: int = 1, role: str = "L", base: int = 2, texture: str = "smooth", seed: int = 0, motion: str = "none"):
    """A straight shaft through `pivot`, `up` texels above it and `down` below (before rotation)."""
    box = g.piece(pid, "TORSO", (x - width / 2, -up, -depth / 2), (width, int(up + down), depth), pivot=pivot,
                  rotation=rotation, motion=motion)
    solid(box, role, texture, seed, base, edge=False)
    return box


def sword(g, prefix: str, pivot, rotation, blade: int = 9, seed: int = 0, scabbard: str = "L", grip: str = "L",
          chape: bool = True, motion: str = "none"):
    """A sheathed sword hung from `pivot`: hilt above it (local -y), scabbard below. Returns (scabbard, guard)."""
    sc = g.piece(f"{prefix}_scabbard", "TORSO", (-.5, 0, -.5), (1, blade, 1), pivot=pivot, rotation=rotation,
                 motion=motion)
    solid(sc, scabbard, "leather", seed, 1)
    for face in sc.sides:
        face.set(0, 0, "M3")
        face.set(0, 2, k(scabbard, 2))
        if chape:
            face.set(0, blade - 1, "M2")
    guard = g.piece(f"{prefix}_guard", "TORSO", (-1.5, -1, -.5), (3, 1, 1), pivot=pivot, rotation=rotation,
                    motion=motion)
    solid(guard, "M", "smooth", seed + 1, 3, edge=False)
    guard.front.set(1, 0, "M4"), guard.back.set(1, 0, "M4")
    hilt = g.piece(f"{prefix}_grip", "TORSO", (-.5, -4, -.5), (1, 3, 1), pivot=pivot, rotation=rotation,
                   motion=motion)
    solid(hilt, grip, "plain", seed + 2, 2, edge=False)
    hilt.strip.hline(0, hilt.strip.w - 1, 0, "M3")                   # pommel
    hilt.strip.hline(0, hilt.strip.w - 1, 2, k(grip, 1))
    hilt.top.fill("M4")
    return sc, guard


# -- surfaces ----------------------------------------------------------------------------------
def lamellae(face, base: int = 2, lace: str = "L2", lace_hi: str = "L3", x0: int = 0, y0: int = 0, y1=None,
             role: str = "M"):
    """Lamellar armour: rows of narrow plates two texels tall, laced together in horizontal bands."""
    y1 = face.h - 1 if y1 is None else y1
    for y in range(y0, y1 + 1):
        r, row = (y - y0) % 3, (y - y0) // 3
        for x in range(x0, face.w):
            gap = (x + face.x0 + row) % 2 == 1
            if r == 0:
                face.set(x, y, k(role, base + 1))                    # the lit top edge of a row of plates
            elif r == 1:
                face.set(x, y, k(role, base - 1) if gap else k(role, base))
            else:
                face.set(x, y, lace_hi if not gap else lace)         # the lacing that binds the row


def lames(face, role: str = "M", base: int = 3, step: int = 2, y0: int = 0, y1=None, x0: int = 0, x1=None):
    """Overlapping plate lames: a lit upper edge over a shaded lower edge on every lame."""
    y1 = face.h - 1 if y1 is None else y1
    x1 = face.w - 1 if x1 is None else x1
    for y in range(y0, y1 + 1):
        r = (y - y0) % step
        key = k(role, base + 1) if r == 0 else k(role, base - 1) if r == step - 1 else k(role, base)
        face.hline(x0, x1, y, key)


def quilt_rows(face, role: str, base: int = 2, step: int = 2, y0: int = 0, y1=None, x0: int = 0, x1=None):
    """Horizontal channel quilting: a stitched row every `step` texels, puffed cloth between."""
    y1 = face.h - 1 if y1 is None else y1
    x1 = face.w - 1 if x1 is None else x1
    for y in range(y0, y1 + 1):
        r = (y - y0) % step
        if r == 0:
            face.hline(x0, x1, y, k(role, base - 1))
        elif r == 1 and step > 2:
            face.hline(x0, x1, y, k(role, base + 1))


def mud(face, seed: int, y0: int, y1=None, key: str = "L0", wet: str = "L1", density: float = .5):
    """Mud thrown up from the road: thick at the bottom edge and thinning upward in small clots."""
    y1 = face.h - 1 if y1 is None else y1
    span = max(1, y1 - y0)
    for y in range(y0, y1 + 1):
        depth = (y - y0) / span
        for x in range(face.w):
            r = rnd(x + face.x0, y + face.y0, seed)
            if y == y1 or r < density * depth * depth:
                face.set(x, y, key if r < .5 or y == y1 else wet)


def rivet_row(face, y: int, key: str = "M3", step: int = 2, start: int = 0, x1=None):
    x1 = face.w - 1 if x1 is None else x1
    for x in range(start, x1 + 1, step):
        face.set(x, y, key)
