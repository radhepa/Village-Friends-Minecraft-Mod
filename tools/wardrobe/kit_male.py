"""Shared helpers for the male wardrobe expansion (tops t31+ and bottoms b31+).

Cloth patterns, fur, embroidery bands, lacing, small 3D props, hoods, capes, sleeve shapes,
skirt panels, leg wraps and footwear variants. Like kit.py, every helper paints key colors only
and returns what it creates, so a module adds its own identity details on top. A garment's
signature (its trim, lacing, props or silhouette) stays in its own module.
"""
from __future__ import annotations

from kit import SIDES, arm_bone, arm_x, leg_bone
from paint import fabric, k, rnd, solid, strip_fabric


# -- cloth patterns --------------------------------------------------------------------------
def tartan(face, ox: int = 0, oy: int = 0, ground: str = "P", stripe: str = "A", cell: int = 6, rows=None):
    """Sett of dark crossing bands with a thin accent over-check."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            gx, gy = (x + ox) % cell, (y + oy) % cell
            bx, by = gx < 2, gy < 2
            key = k(ground, 0) if bx and by else k(ground, 1) if bx or by else k(ground, 2)
            if (gx == cell - 2 or gy == cell - 2) and not (bx or by):
                key = k(stripe, 2)
            face.set(x, y, key)


def stripes(face, keys, width: int = 1, vertical: bool = False, offset: int = 0, rows=None, cols=None):
    """Bands cycling through keys, `width` texels each."""
    for y in rows if rows is not None else range(face.h):
        for x in cols if cols is not None else range(face.w):
            i = ((x if vertical else y) + offset) // width
            face.set(x, y, keys[i % len(keys)])


def check(face, a: str, b: str, size: int = 2, ox: int = 0, oy: int = 0, rows=None):
    """A chequer of two keys."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            face.set(x, y, a if ((x + ox) // size + (y + oy) // size) % 2 == 0 else b)


def herringbone(face, role: str, base: int = 2, ox: int = 0, rows=None):
    """Zig-zag twill: columns of diagonals that flip direction every three texels."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            col = (x + ox) // 3
            d = (x + ox + (y if col % 2 else -y)) % 4
            face.set(x, y, k(role, base - 1 if d == 0 else base))


def lozenge(face, role: str, base: int = 2, step: int = 4, line_key: str | None = None, ox: int = 0, rows=None):
    """Diamond lattice: stitched diagonals with lit centres (quilting or brocade)."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            a, b = (x + ox + y) % step, (x + ox - y) % step
            if a == 0 or b == 0:
                face.set(x, y, line_key or k(role, base - 1))
            elif a == step // 2 and b == step // 2:
                face.set(x, y, k(role, base + 1))
            else:
                face.set(x, y, k(role, base))


def ribbing(face, role: str, base: int = 2, rows=None, horizontal: bool = False):
    """Knitted ribs: alternating raised and sunken columns (or rows)."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            face.set(x, y, k(role, base - ((y if horizontal else x) % 2)))


def flecks(face, key: str, seed: int, density: float = .08, rows=None, cols=None):
    """Sparse single texels: flour dust, soot, wax drips, mud."""
    for y in rows if rows is not None else range(face.h):
        for x in cols if cols is not None else range(face.w):
            if rnd(x + face.x0, y + face.y0, seed) < density:
                face.set(x, y, key)


def fur_face(face, role: str = "S", seed: int = 0, base: int = 3, rows=None):
    """Soft fur tufts: a lit base with highlights and shaded roots."""
    for y in rows if rows is not None else range(face.h):
        for x in range(face.w):
            r = rnd(x + face.x0, y + face.y0, seed)
            face.set(x, y, k(role, base + 1) if r > .7 else k(role, base - 1) if r < .25 else k(role, base))


def fur(box, role: str = "S", seed: int = 0, base: int = 3):
    for face in box.faces:
        fur_face(face, role, seed, base)
    return box


# -- trims and fastenings --------------------------------------------------------------------
PATTERNS = {
    "zig": ["a.", ".a"],
    "dots": ["a."],
    "dash": ["aa."],
    "cross": [".a..", "aaa.", ".a.."],
    "diamond": [".a..", "a.a.", ".a.."],
    "vine": ["a..b..", ".ab.ba"],
    "step": ["aab.", "a.bb"],
    "wave": ["a...", ".a.a", "..a."],
}


def embroider(face, y: int, pattern: str = "zig", a: str = "A3", b: str = "A1", x0: int = 0, x1: int | None = None,
              shift: int = 0):
    """Stamp a repeating embroidery band whose top row is y; '.' keeps the cloth underneath."""
    x1 = face.w - 1 if x1 is None else x1
    for dy, row in enumerate(PATTERNS[pattern]):
        for x in range(x0, x1 + 1):
            ch = row[(x - x0 + shift) % len(row)]
            if ch == "a":
                face.set(x, y + dy, a)
            elif ch == "b":
                face.set(x, y + dy, b)


def lacing(face, x: int, y0: int, y1: int, a: str = "L3", b: str = "L1"):
    """Criss-cross lacing over two columns x and x + 1."""
    for y in range(y0, y1 + 1):
        face.set(x + y % 2, y, a)
        face.set(x + 1 - y % 2, y, b)


def buttons(face, x: int, y0: int, y1: int, step: int = 2, key: str = "M3"):
    for y in range(y0, y1 + 1, step):
        face.set(x, y, key)


def toggles(face, x: int, ys, key: str = "L3", loop: str = "L1"):
    """Horizontal wooden toggles with a dark loop beside each."""
    for y in ys:
        face.set(x, y, key), face.set(x + 1, y, key), face.set(x + 2, y, loop)


# -- small 3D props --------------------------------------------------------------------------
def blk(g, pid: str, pivot, size, role: str, base: int = 2, texture: str = "plain", seed: int = 0, bone: str = "TORSO",
        origin=None, rotation=(0, 0, 0), motion: str = "none", inflate: float = 0.0, edge: bool = True):
    """A fully painted cuboid centred on its pivot in x and z (top at the pivot)."""
    w, h, d = size
    o = origin if origin is not None else (-w / 2, 0, -d / 2)
    box = g.piece(pid, bone, o, size, pivot=pivot, rotation=rotation, inflate=inflate, motion=motion)
    solid(box, role, texture, seed, base, edge=edge)
    return box


def arm_blk(g, pid: str, side: str, y: float, size, role: str, base: int = 2, texture: str = "plain", seed: int = 0,
            dx: float = 0.0, dz: float = 0.0, inflate: float = 0.0, rotation=(0, 0, 0)):
    """A cuboid centred on one arm at arm-local height y (rings, cuffs, gauntlets, bracers)."""
    w, h, d = size
    cx = arm_x(side) + 2.0 + dx
    box = g.piece(pid, arm_bone(side), (cx - w / 2, y, -d / 2 + dz), size, rotation=rotation, inflate=inflate)
    solid(box, role, texture, seed, base)
    return box


def leg_blk(g, pid: str, side: str, y: float, size, role: str, base: int = 2, texture: str = "plain", seed: int = 0,
            dx: float = 0.0, dz: float = 0.0, inflate: float = 0.0, rotation=(0, 0, 0)):
    """A cuboid centred on one leg at leg-local height y (pads, cuffs, buckles, toes)."""
    w, h, d = size
    box = g.piece(pid, leg_bone(side), (-w / 2 + dx, y, -d / 2 + dz), size, rotation=rotation, inflate=inflate)
    solid(box, role, texture, seed, base)
    return box


# -- tops: hoods, capes, sleeves, sashes ------------------------------------------------------
def hood_down(g, role: str, texture: str = "weave", seed: int = 0, base: int = 2, pid: str = "hood", width: int = 7,
              y: float = -1.0, z: float = 2.9, tilt: float = 16, lining: str | None = None):
    """A lowered hood lying on the upper back; its lit opening faces up."""
    hood = g.piece(pid, "TORSO", (-width / 2, 0, 0), (width, 3, 2), pivot=(0, y, z), rotation=(tilt, 0, 0))
    solid(hood, role, texture, seed, base)
    fabric(hood.top, role, texture, seed, base + 1)
    hood.back.vline(width // 2, 1, 2, k(role, base - 1))
    hood.back.hline(0, width - 1, 0, k(role, base + 1))
    if lining:
        hood.top.hline(1, width - 2, 1, lining)
    return hood


def shoulder_cape(g, pid: str, role: str, texture: str = "weave", seed: int = 0, base: int = 2, length: int = 3,
                  width: int = 12, depth: int = 6, y: float = -.8, inflate: float = .04):
    """A short cape over both shoulders (mantlet, chaperon cape, tippet)."""
    cape = g.piece(pid, "TORSO", (-width / 2, y, -depth / 2 + .1), (width, length, depth), inflate=inflate)
    solid(cape, role, texture, seed, base)
    fabric(cape.top, role, texture, seed, base + 1)
    return cape


def back_drape(g, pid: str, role: str, length: int, texture: str = "weave", seed: int = 0, base: int = 2,
               width: int = 10, y: float = 1.0, z: float = 2.6, tilt: float = 5, motion: str = "none"):
    """A cloak's back panel hanging from the shoulders."""
    drape = g.piece(pid, "TORSO", (-width / 2, 0, 0), (width, length, 1), pivot=(0, y, z), rotation=(tilt, 0, 0),
                    motion=motion)
    solid(drape, role, texture, seed, base)
    return drape


def sleeve_shapes(g, pid: str, role: str, y: float, size, texture: str = "weave", seed: int = 0, base: int = 2,
                  inflate: float = .12, dz: float = 0.0):
    """One cuboid around each arm (bag sleeves, bell sleeves, puffs); returns [right, left]."""
    return [arm_blk(g, f"{side}_{pid}", side, y, size, role, base, texture, seed + i, dz=dz, inflate=inflate)
            for i, side in enumerate(SIDES)]


def tippets(g, role: str, length: int, y: float = 2.4, base: int = 2, seed: int = 0, key_end: str | None = None,
            pid: str = "tippet"):
    """Long streamers hanging from the elbows, swaying as the wearer walks."""
    out = []
    for i, side in enumerate(SIDES):
        x = arm_x(side) + (0.4 if side == "right" else 3.6)
        t = g.piece(f"{side}_{pid}", arm_bone(side), (-.5, 0, -.5), (1, length, 1), pivot=(x, y, 1.6), motion="sway")
        solid(t, role, "plain", seed + i, base)
        if key_end:
            t.strip.hline(0, t.strip.w - 1, length - 1, key_end)
        out.append(t)
    return out


def sash(g, pid: str, role: str, y: float = 9.2, height: int = 2, texture: str = "weave", seed: int = 0, base: int = 2,
         tails=((2.4, 0),), tail_len: int = 4, inflate: float = .06):
    """A cloth sash wound round the waist with knotted, swaying tails."""
    box = g.piece(pid, "TORSO", (-4.6, y, -2.6), (9, height, 5), inflate=inflate)
    solid(box, role, texture, seed, base, edge=False)
    for face in box.sides:
        face.hline(0, face.w - 1, 0, k(role, base + 1))
    for i, (x, rz) in enumerate(tails):
        tail = g.piece(f"{pid}_tail_{i}", "TORSO", (-.5, 0, -.5), (1, tail_len, 1), pivot=(x, y + height - .4, -2.8),
                       rotation=(0, 0, rz), motion="sway")
        solid(tail, role, texture, seed + 1 + i, base)
    return box


# -- bottoms: skirts, wraps, footwear ----------------------------------------------------------
def skirt_panels(g, prefix: str, length: int, role: str, texture: str = "weave", seed: int = 0, base: int = 2,
                 top: float = 10.6, width: int = 9, sides: bool = True, side_len: int | None = None):
    """Front/back skirt or kilt panels just outside a top's hem planes, plus optional side panels.

    Tops hang their hems at z -2.85/1.85; these sit at -2.95/1.95 so a tunic hem tucks behind.
    Returns (front_face, back_face, side_boxes).
    """
    faces, side_boxes = [], []
    for name, z, motion, face_name in (("front", -2.95, "flap_front", "front"), ("back", 1.95, "flap_back", "back")):
        panel = g.piece(f"{prefix}_{name}", "TORSO", (-width / 2, 0, 0), (width, length, 1), pivot=(0, top, z),
                        motion=motion)
        solid(panel, role, texture, seed + (name == "back"), base)
        faces.append(getattr(panel, face_name))
    if sides:
        for name, x in (("right", -5.1), ("left", 4.1)):
            panel = g.piece(f"{prefix}_{name}", "TORSO", (0, 0, -2), (1, side_len or max(1, length - 1), 4),
                            pivot=(x, top, 0))
            solid(panel, role, texture, seed + 2, base)
            side_boxes.append(panel)
    return faces[0], faces[1], side_boxes


def wraps(face, role: str, rows, base: int = 2, period: int = 4, slope: int = 1, edge: str | None = None):
    """Spiral leg bindings: diagonal bands winding round a leg strip."""
    for y in rows:
        for x in range(face.w):
            phase = (x + slope * y) % period
            if phase == 0:
                face.set(x, y, edge or k(role, base + 1))
            elif phase == period - 1:
                face.set(x, y, k(role, base - 1))
            else:
                face.set(x, y, k(role, base))


def bare_feet(g, rows=(10, 11)):
    """Leave the feet unpainted (skin shows) by clearing any cloth on those rows."""
    for side in SIDES:
        for part in (f"{side}_leg", f"{side}_pants"):
            box = g.part(part)
            for y in range(rows[0], rows[1] + 1):
                box.strip.hline(0, box.strip.w - 1, y, None)
            box.bottom.fill(None)


def toe_pieces(g, pid: str, size, role: str = "L", base: int = 2, texture: str = "smooth", seed: int = 0,
               y: float = 10.9, z: float = -2.2, rotation=(0, 0, 0), inflate: float = 0.0):
    """A cuboid in front of each foot (pointed toes, clog fronts, upturned tips)."""
    w, h, d = size
    out = []
    for i, side in enumerate(SIDES):
        box = g.piece(f"{side}_{pid}", leg_bone(side), (-w / 2, 0, -d), size, pivot=(0, y, z), rotation=rotation,
                      inflate=inflate)
        solid(box, role, texture, seed + i, base, edge=False)
        fabric(box.top, role, texture, seed + i, base + 1)
        out.append(box)
    return out


def leg_rings(g, pid: str, y: float, role: str, size=(5, 2, 5), base: int = 2, texture: str = "weave", seed: int = 0,
              inflate: float = 0.0):
    """A ring around each leg; returns [right, left]."""
    return [leg_blk(g, f"{side}_{pid}", side, y, size, role, base, texture, seed + i, inflate=inflate)
            for i, side in enumerate(SIDES)]
