"""Garment building blocks shared by tops and bottoms: bodies, sleeves, belts, flaps, legs, boots.

Each helper paints key colors only and returns the boxes it created so a module can add its own
details on top. Keep anything that defines a garment's identity in the garment's own module.
"""
from __future__ import annotations

from paint import cap, fabric, grid, k, solid, strip_fabric

SIDES = ("right", "left")


def arm_bone(side: str) -> str:
    return "RIGHT_ARM" if side == "right" else "LEFT_ARM"


def leg_bone(side: str) -> str:
    return "RIGHT_LEG" if side == "right" else "LEFT_LEG"


def arm_x(side: str) -> float:
    """x of the arm box's corner in arm-local space (wide arms)."""
    return -3.0 if side == "right" else -1.0


# -- tops ------------------------------------------------------------------------------------
def body(g, role: str, texture: str = "weave", seed: int = 0, base: int = 2, layer: str = "body", rows=None):
    """Torso cloth on the base body (or the jacket overlay), with lit shoulders."""
    box = g.part(layer)
    y0, y1 = rows if rows else (0, box.h - 1)
    strip_fabric(box, role, texture, seed, base, y0, y1)
    if y0 == 0:
        fabric(box.top, role, texture, seed, base + 1)
    if y1 == box.h - 1:
        fabric(box.bottom, role, texture, seed + 1, base - 1)
    return box


def neckline(face, style: str, role: str, base: int = 2):
    """Necklines on a body/jacket front: round, v, laced, keyhole, square, collarless."""
    if style == "round":
        for x in (3, 4):
            face.clear(x, 0)
        face.set(2, 0, k(role, base - 1)), face.set(5, 0, k(role, base - 1))
    elif style == "v":
        for x, y in [(2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (3, 2), (4, 2), (4, 3)]:
            face.clear(x, y)
        for x, y in [(1, 0), (2, 1), (2, 2), (3, 3)]:
            face.set(x, y, k(role, base + 1))
        for x, y in [(6, 0), (5, 1), (5, 2)]:
            face.set(x, y, k(role, base - 1))
    elif style == "laced":
        for x, y in [(3, 0), (4, 0), (3, 1), (4, 1), (4, 2)]:
            face.clear(x, y)
        face.set(3, 2, "L2"), face.set(3, 3, "L3"), face.set(4, 3, "L2")
        face.set(2, 0, k(role, base + 1)), face.set(5, 0, k(role, base - 1))
    elif style == "keyhole":
        for x in (3, 4):
            face.clear(x, 0)
        face.clear(3, 1)
        face.set(4, 1, k(role, base - 1)), face.set(3, 2, k(role, base - 1))
    elif style == "square":
        for x in range(2, 6):
            face.clear(x, 0)
        face.hline(2, 5, 1, k(role, base + 1))


def sleeves(g, role: str, texture: str = "weave", seed: int = 0, base: int = 2, rows=(0, 11), layer: str = "arm",
            cuff: str | None = None, cuff_row: int | None = None):
    """Both sleeves from rows[0] to rows[1]; an optional cuff key band; returns the two boxes."""
    boxes = []
    for side in SIDES:
        box = g.part(f"{side}_{layer}")
        strip_fabric(box, role, texture, seed + (side == "left"), base, rows[0], rows[1])
        if rows[0] == 0:
            fabric(box.top, role, texture, seed, base + 1)
        if cuff:
            box.strip.hline(0, box.strip.w - 1, rows[1] if cuff_row is None else cuff_row, cuff)
        boxes.append(box)
    return boxes


def roll(g, role: str, y: float, base: int = 3, prefix: str = "sleeve_roll", accent: str | None = None):
    """A rolled sleeve ring around each arm at arm-local height y."""
    for side in SIDES:
        ring = g.piece(f"{side}_{prefix}", arm_bone(side), (arm_x(side) - .45, y, -2.45), (5, 2, 5))
        solid(ring, role, "weave", 7 + (side == "left"), base)
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, k(role, base + 1))
            face.hline(0, face.w - 1, 1, k(role, base - 1))
            if accent:
                face.set(face.w // 2, 1, accent)


def belt(g, pid: str, y: float = 9.6, role: str = "L", base: int = 2, height: int = 2, buckle: str | None = "M",
         inflate: float = .05):
    """A belt ring around the waist; tops use their own id, bottoms prefix it with 'waist'."""
    box = g.piece(pid, "TORSO", (-4.6, y, -2.6), (9, height, 5), inflate=inflate)
    solid(box, role, "leather" if role == "L" else "weave", 31, base, edge=False)
    for face in box.sides:
        face.hline(0, face.w - 1, 0, k(role, base + 1))
    if buckle and height >= 2:
        grid(box.front, 3, 0, ["mmm", "m.m"], {"m": k(buckle, 3)})
        box.front.set(4, 1, k(role, base - 2))
    elif buckle:
        box.front.set(4, 0, k(buckle, 3))
    return box


def pouch(g, pid: str, pivot, size=(2, 3, 2), role: str = "L", flap: str | None = None, rotation=(0, 0, 0)):
    w, h, d = size
    box = g.piece(pid, "TORSO", (-w / 2, 0, -d / 2), size, pivot=pivot, rotation=rotation)
    solid(box, role, "leather", 41, 2)
    cap(box, role, top_delta=1)
    for face in box.sides:
        face.hline(0, face.w - 1, 0, k(role, 3))
    if flap:
        box.front.set(w // 2, 1, flap)
    return box


def flaps(g, prefix: str, length: int, role: str, texture: str = "weave", seed: int = 0, width: int = 9, base: int = 2,
          hem: str | None = None, top: float = 11.4, front_z: float = -2.85, back_z: float = 1.85, slit: bool = False):
    """Front/back skirt panels that follow the stride; returns (front_face, back_face)."""
    faces = []
    for name, z, motion, face_name in (("front", front_z, "flap_front", "front"), ("back", back_z, "flap_back", "back")):
        panel = g.piece(f"{prefix}_{name}", "TORSO", (-width / 2, 0, 0), (width, length, 1), pivot=(0, top, z), motion=motion)
        solid(panel, role, texture, seed + (name == "back"), base)
        face = getattr(panel, face_name)
        face.hline(0, width - 1, 0, k(role, base + 1))
        if hem:
            face.hline(0, width - 1, length - 1, hem)
        if slit:
            face.vline(width // 2, 1, length - 1, k(role, base - 2))
        faces.append(face)
    return faces


def side_panels(g, prefix: str, length: int, role: str, texture: str = "weave", hem: str | None = None, top: float = 11.4):
    for name, x in (("right", -5.0), ("left", 4.0)):
        panel = g.piece(f"{prefix}_{name}", "TORSO", (0, 0, -2), (1, length, 4), pivot=(x, top, 0))
        solid(panel, role, texture, 51, 2)
        if hem:
            for face in panel.sides:
                face.hline(0, face.w - 1, length - 1, hem)


def collar(g, pid: str, role: str, texture: str = "weave", base: int = 2, height: int = 2, y: float = -1.0, inflate: float = .06):
    box = g.piece(pid, "TORSO", (-4.5, y, -2.6), (9, height, 5), inflate=inflate)
    solid(box, role, texture, 61, base)
    fabric(box.top, role, texture, 61, base + 1)
    for face in box.sides:
        face.hline(0, face.w - 1, 0, k(role, base + 1))
    return box


# -- bottoms ---------------------------------------------------------------------------------
def legs(g, role: str, texture: str = "twill", seed: int = 0, base: int = 2, rows=(0, 9), crease: bool = True):
    """Both trouser legs; a pressed crease down the front; returns the leg boxes."""
    boxes = []
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, role, texture, seed + (side == "left"), base, rows[0], rows[1])
        if rows[0] == 0:
            fabric(leg.top, role, texture, seed, base)
        if crease:
            leg.front.vline(1 if side == "right" else 2, rows[0] + 1, rows[1], k(role, base + 1))
        boxes.append(leg)
    return boxes


def waistband(g, role: str, texture: str = "twill", seed: int = 0, base: int = 2, rows=(9, 11)):
    body = g.part("body")
    strip_fabric(body, role, texture, seed, base, rows[0], rows[1])
    for face in body.sides:
        face.hline(0, face.w - 1, rows[0], k(role, base + 1))
    fabric(body.bottom, role, texture, seed + 1, base - 1)
    return body


def footwear(g, style: str = "boot", top: int = 9, role: str = "L", base: int = 2, toe: str | None = None, sole: str = "K1"):
    """Shoes or boots on the base leg and a chunkier overlay. Styles: boot, shoe, turnshoe, clog."""
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        texture = "smooth" if style in ("shoe", "clog") else "leather"
        strip_fabric(leg, role, texture, 71, base - (1 if style == "shoe" else 0), top, 11)
        for face in pants.sides:
            fabric(face, role, texture, 72, base, 0, top, face.w, 12 - top)
            face.hline(0, face.w - 1, top, k(role, base + 1))
            face.hline(0, face.w - 1, 11, sole)
        if style == "clog":
            for face in pants.sides:
                face.hline(0, face.w - 1, 10, k(role, base + 1))
        pants.front.hline(0, 3, 11, toe or k(role, base + 1))
        leg.bottom.fill(sole), pants.bottom.fill("K0")


def stockings(g, role: str, rows, stripe: str | None = None, base: int = 3):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for y in range(rows[0], rows[1] + 1):
            key = stripe if stripe and (y - rows[0]) % 2 else k(role, base)
            leg.strip.hline(0, leg.strip.w - 1, y, key)


def leg_ring(g, prefix: str, y: float, role: str, base: int = 3, size=(5, 2, 5), texture: str = "weave", inflate: float = 0):
    """A ring around each lower leg: cuffs, boot tops, fur, gathers."""
    w, h, d = size
    rings = []
    for side in SIDES:
        ring = g.piece(f"{side}_{prefix}", leg_bone(side), (-w / 2, y, -d / 2), size, inflate=inflate)
        solid(ring, role, texture, 81 + (side == "left"), base)
        rings.append(ring)
    return rings
