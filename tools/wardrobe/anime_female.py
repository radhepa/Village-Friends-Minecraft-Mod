"""Building blocks for the female hairstyles: textured strands, plaits, buns, bows, flowers and ties.

Everything paints key colors only and returns the boxes it made, so a hairstyle module can add its
own details. Strands hang along their local +y from one pivot; every segment of a strand, braid or
tail shares that pivot so `sway` swings the whole chain together.

Textures (all paint every texel of a box):
  cel      clean anime clumps with a sheen ring (anime.cel_box)
  sleek    cel with wide clumps, for combed or glossy hair
  wave     soft horizontal wave bands
  ringlet  a helix wrapping around the box, for spiral curls and drills
  curl     tight 3x3 curl clusters (paint.curls_face)
  coil     small springy coils for afro-textured hair
  loc      rounded segments stacked down each loc
  plait    one braided lobe; flip alternates the lit side
  wet      dark, clinging clumps with sharp wet highlights
"""
from __future__ import annotations

from anime import cel_box
from paint import curls_face, k, rnd, solid
from wardrobe import rot_matrix

SIDES = (("right", -1), ("left", 1))


# -- textures --------------------------------------------------------------------------------
def _caps(box, base, top_delta=1, top=None):
    for y in range(box.top.h):
        for x in range(box.top.w):
            box.top.set(x, y, k("H", (base + top_delta) if top is None else top(x, y)))
    box.bottom.fill(k("H", base - 2))


def wave_face(face, seed, base=2, ring=None):
    """One wave per segment: a lit crest near the top, strand lines through the body, a shaded trough
    at the bottom. Segments that step side to side give the wave its silhouette."""
    off = int(rnd(seed, 2) * 3)
    crest = 0 if face.h <= 3 else 1
    for y in range(face.h):
        for x in range(face.w):
            s = base
            if (x + face.x0 + off) % 3 == 0:
                s -= 1
            if y == crest:
                s = base + (2 if ring is not None and rnd(x, y, seed) > .3 else 1)
            if face.h > 2 and y == face.h - 1:
                s = base - 1
            face.set(x, y, k("H", s))


def ringlet_strip(box, seed, base=2, period=4):
    """A coil: lit and shaded bands one row lower on each side in turn, so they spiral around the box."""
    off = int(rnd(seed, 4) * period)
    for i, f in enumerate(box.sides):
        for y in range(f.h):
            ph = (y + i + off) % period
            for x in range(f.w):
                s = base + (1 if ph == 0 else -1 if ph == period - 1 else 0)
                if ph == 0 and x == (f.w - 1 if i % 2 else 0) and f.w > 1:
                    s = base + 2
                f.set(x, y, k("H", s))


def coil_face(face, seed, base=2):
    for y in range(face.h):
        for x in range(face.w):
            r = rnd(x + face.x0, y, seed)
            s = base + (1 if (x + y) % 2 == 0 and r > .3 else 0) - (1 if (x + 2 * y) % 4 == 3 else 0)
            if r < .08:
                s = base - 1
            face.set(x, y, k("H", s))


def loc_face(face, seed, base=2):
    off = int(rnd(seed, 6) * 3)
    for y in range(face.h):
        for x in range(face.w):
            ph = (y + off + x) % 3
            s = base + (1 if ph == 0 else -1 if ph == 2 else 0)
            face.set(x, y, k("H", s))


def plait_face(face, base=2, flip=False):
    """One lobe of a braid: a lit strand crossing diagonally, shaded below it."""
    w, h = face.w, face.h
    for y in range(h):
        for x in range(w):
            xx = (w - 1 - x) if flip else x
            t = xx - y * (w / max(1, h))
            s = base + 1 if abs(t) < .6 else base if t > 0 else base - 1
            if y == h - 1 and xx == w - 1 and w > 1:
                s = base - 1
            face.set(x, y, k("H", s))


def wet_face(face, seed, base=2, ring=None):
    for y in range(face.h):
        for x in range(face.w):
            col = rnd(x + face.x0, 3, seed)
            s = base - 1 if col < .5 else base
            if col > .78:
                s = base + 1
            if ring is not None and y in (ring, ring + 1) and col > .4:
                s = base + 2
            if face.h > 2 and y == face.h - 1:
                s = base - 1
            face.set(x, y, k("H", s))


def paint(box, texture="cel", seed=0, base=2, ring=None, top_delta=1, flip=False):
    if texture in ("cel", "sleek", "fine"):
        cel_box(box, seed, base, ring, top_delta, clump={"cel": 3, "sleek": 4, "fine": 2}[texture])
    elif texture == "wave":
        for f in box.sides:
            wave_face(f, seed + f.x0, base, ring)
        _caps(box, base, top_delta)
    elif texture == "ringlet":
        ringlet_strip(box, seed, base)
        _caps(box, base, top_delta)
    elif texture == "curl":
        for f in box.sides:
            curls_face(f, seed + f.x0, base)
        curls_face(box.top, seed + 3, base + top_delta)
        box.bottom.fill(k("H", base - 2))
    elif texture == "coil":
        for f in box.sides + [box.top]:
            coil_face(f, seed + f.x0, base + (top_delta if f is box.top else 0))
        box.bottom.fill(k("H", base - 2))
    elif texture == "loc":
        for f in box.sides:
            loc_face(f, seed, base)
        _caps(box, base, top_delta)
    elif texture == "plait":
        for f in box.sides:
            plait_face(f, base, flip if f.name in ("front", "back") else not flip)
        _caps(box, base, 1)
    elif texture == "wet":
        for f in box.sides:
            wet_face(f, seed, base, ring)
        _caps(box, base, top_delta)
    else:
        raise ValueError(f"unknown hair texture {texture}")
    return box


# -- strands ---------------------------------------------------------------------------------
def strand(g, pid, pivot, rotation=(0, 0, 0), segments=((3, 3), (2, 2), (1, 1)), depth=1, seed=0, base=2, ring=1,
           motion="none", texture="cel", z=0.0, start=0.0, inflate=0.0):
    """A tapered lock along local +y from the pivot. A segment is (w, h) or (w, h, dx); dx shifts it
    sideways so a chain of segments can wave or curl in silhouette."""
    y = start
    boxes = []
    for i, seg in enumerate(segments):
        w, h = seg[0], seg[1]
        dx = seg[2] if len(seg) > 2 else 0
        d = seg[3] if len(seg) > 3 else depth
        box = g.piece(f"{pid}_{i}" if len(segments) > 1 else pid, "HEAD", (-w / 2 + dx, y, -d / 2 + z), (w, h, d),
                      pivot=pivot, rotation=rotation, motion=motion, inflate=inflate)
        paint(box, texture, seed + i * 7, base, ring if i == 0 else None, 1 if i == 0 else 0)
        y += h
        boxes.append(box)
    return boxes


def world(pivot, rotation, local):
    """Bone-local position of a point given in a piece's rotated frame."""
    m = rot_matrix(*rotation)
    return tuple(pivot[i] + sum(m[i][j] * local[j] for j in range(3)) for i in range(3))


def point(g, pid, pivot, rotation, y, w=2, depth=1, seed=0, base=2, texture="cel", dx=0.0, z=0.0, turn=45, span=None):
    """A diamond tip for a static lock: a w*w square turned 45 degrees in the lock's plane, centred at local
    (dx, y) and scaled so its width is `span`. Its lower half finishes the lock in a clean point. Swaying
    locks taper with segments instead, because a tip with its own pivot would not swing with them."""
    rx, ry, rz = rotation
    center = world(pivot, rotation, (dx, y, z))
    s = 1.0 if span is None else min(1.0, span / (w * 1.4142))
    box = g.piece(pid, "HEAD", (-w / 2, -w / 2, -depth / 2), (w, w, depth), pivot=center, rotation=(rx, ry, rz + turn),
                  scale=None if s == 1.0 else (s, s, 1))
    paint(box, texture, seed, base, None, 0)
    return box


def pointed(g, pid, pivot, rotation=(0, 0, 0), w=3, h=4, tip=2, depth=1, seed=0, base=2, ring=1, texture="cel", z=0.0):
    """A static lock with a diamond tip: one w*h body and a turned square, as wide as the body, finishing it."""
    body = strand(g, f"{pid}", pivot, rotation, ((w, h),), depth, seed, base, ring, "none", texture, z)
    tipbox = point(g, f"{pid}_tip", pivot, rotation, h - .15, tip, depth, seed + 5, base, texture, z=z, span=w)
    return body + [tipbox]


def fall(g, prefix, specs, seed=0, base=2, motion="none", texture="cel", depth=1, ring=1):
    """Several strands: specs are (x, y, z, segments, rx, rz). Vary them so a mass never reads as one slab."""
    out = []
    for i, (x, y, z, segments, rx, rz) in enumerate(specs):
        out += strand(g, f"{prefix}_{i}", (x, y, z), (rx, 0, rz), segments, depth, seed + i * 11, base, ring, motion, texture)
    return out


def fringe(g, prefix, specs, seed=0, base=2, z=-4.35, texture="cel", rx=-10, y=-8.55):
    """Bangs: specs are (x, segments, rz). Locks within |x| < 3 must end above y = -5."""
    out = []
    for i, (x, segments, rz) in enumerate(specs):
        out += strand(g, f"{prefix}_{i}", (x, y, z), (rx, 0, rz), segments, 1, seed + i * 13, base, 0, "none", texture)
    return out


def points(g, prefix, specs, seed=0, base=2, z=-4.35, texture="cel", rx=-10, y=-8.7):
    """Pointed bangs: specs are (x, w, h, tip, rz); each a w*h body ending in a diamond tip. Keep h + tip * .5 <= 3
    for locks within |x| < 3 so they end above the brows."""
    out = []
    for i, (x, w, h, tip, rz) in enumerate(specs):
        out += pointed(g, f"{prefix}_{i}", (x, y, z), (rx, 0, rz), w, h, tip, 1, seed + i * 13, base, 0, texture)
    return out


# -- braids, ties and buns -------------------------------------------------------------------
def tie(g, pid, pivot, rotation=(0, 0, 0), size=(2, 1, 2), y=0.0, role="A", base=2, motion="none", inflate=.12, x=0.0, z=0.0):
    w, h, d = size
    box = g.piece(pid, "HEAD", (-w / 2 + x, y, -d / 2 + z), size, pivot=pivot, rotation=rotation, inflate=inflate, motion=motion)
    solid(box, role, "plain", 0, base, edge=False)
    for f in box.sides:
        f.hline(0, f.w - 1, 0, k(role, base + 1))
    return box


# -- bent chains -----------------------------------------------------------------------------
def local(pivot, rotation, point):
    """A bone-local point expressed in a piece's rotated frame (the inverse of `world`)."""
    m = rot_matrix(*rotation)
    rel = [point[i] - pivot[i] for i in range(3)]
    return [sum(m[r][c] * rel[r] for r in range(3)) for c in range(3)]


def axis(rotation):
    """The direction a piece's local +y points after its rotation."""
    m = rot_matrix(*rotation)
    return [m[r][1] for r in range(3)]


def _step(at, rotation, dist):
    a = axis(rotation)
    return [at[i] + a[i] * dist for i in range(3)]


def link(g, pid, pivot, at, rotation, size, motion="none", dx=0.0, inflate=0.0):
    """A box whose top centre sits at bone-local point `at`, turned by `rotation` but pivoting on the chain's
    root `pivot`, so every link of a bent chain swings together."""
    w, h, d = size
    lx, ly, lz = local(pivot, rotation, at)
    return g.piece(pid, "HEAD", (lx - w / 2 + dx, ly, lz - d / 2), size, pivot=pivot, rotation=rotation, motion=motion,
                   inflate=inflate)


def curve(g, pid, pivot, segs, depth=1, seed=0, base=2, ring=1, motion="none", texture="cel", start=None, overlap=.5, ry=0.0):
    """A bent lock: segs are (w, h, rx, rz) or (w, h, rx, rz, d). Each segment leans its own way and starts
    where the last one ended, overlapping it a little so bends never open; all share the root pivot.
    Returns (boxes, end point, last rotation)."""
    at = list(start or pivot)
    boxes, rot = [], (0, ry, 0)
    for i, seg in enumerate(segs):
        w, h, rx, rz = seg[:4]
        d = seg[4] if len(seg) > 4 else depth
        rot = (rx, ry, rz)
        box = link(g, f"{pid}_{i}", pivot, at, rot, (w, h, d), motion)
        paint(box, texture, seed + i * 7, base, ring if i == 0 else None, 1 if i == 0 else 0)
        boxes.append(box)
        at = _step(at, rot, h - (overlap if i < len(segs) - 1 else 0))
    return boxes, at, rot


def plait_path(g, pid, pivot, angles, w=2, d=2, h=2, step=1.8, shift=.45, seed=0, base=2, motion="sway", start=None,
               ry=0.0, taper=None):
    """Braid lobes alternating side to side along a bent path: angles gives one (rx, rz) per lobe.
    Returns (boxes, end point, last rotation, last lobe width)."""
    at = list(start or pivot)
    boxes, rot, ww = [], (0, ry, 0), w
    for i, (rx, rz) in enumerate(angles):
        rot = (rx, ry, rz)
        ww = w if taper is None or i < taper else max(1, w - 1)
        box = link(g, f"{pid}_{i}", pivot, at, rot, (ww, h, d), motion, dx=shift if i % 2 == 0 else -shift)
        paint(box, "plait", seed + i, base, flip=bool(i % 2))
        boxes.append(box)
        at = _step(at, rot, step)
    return boxes, _step(at, rot, h - step), rot, ww


def finish(g, pid, pivot, at, rotation, w=2, d=2, tie_role="A", tail=((2, 2), (1, 1)), motion="sway", seed=0, base=2):
    """Tie off a braid or tail at `at`: an optional band in a palette role, then a pointed brush of hair."""
    boxes = []
    if tie_role:
        band = link(g, f"{pid}_tie", pivot, _step(at, rotation, -.3), rotation, (w, 1, d), motion, inflate=.12)
        solid(band, tie_role, "plain", 0, 2, edge=False)
        for f in band.sides:
            f.hline(0, f.w - 1, 0, k(tie_role, 3))
        boxes.append(band)
        at = _step(at, rotation, .7)
    for j, (tw, th) in enumerate(tail or ()):
        box = link(g, f"{pid}_tail_{j}", pivot, at, rotation, (tw, th, min(d, tw)), motion)
        paint(box, "cel", seed + 40 + j, base, None, 0)
        boxes.append(box)
        at = _step(at, rotation, th)
    return boxes


def braid(g, pid, pivot, rotation=(0, 0, 0), count=6, w=2, d=2, h=2, step=1.8, shift=.45, seed=0, base=2,
          motion="sway", taper=None, tie_role="A", tail=((2, 2), (1, 1))):
    """A straight plait hanging along `rotation` from the pivot, tied off with a pointed tail."""
    rx, ry, rz = rotation
    boxes, end, rot, ww = plait_path(g, pid, pivot, [(rx, rz)] * count, w, d, h, step, shift, seed, base, motion, ry=ry,
                                     taper=taper)
    return boxes + finish(g, pid, pivot, end, rot, ww, d, tie_role, tail, motion, seed, base)


def wrap_face(face, seed, base=2):
    """Hair wound around a bun: diagonal bands."""
    for y in range(face.h):
        for x in range(face.w):
            ph = (x + face.x0 + y + seed) % 3
            face.set(x, y, k("H", base + (1 if ph == 0 else -1 if ph == 2 else 0)))


def swirl_top(face, base=2):
    cx, cy = (face.w - 1) / 2, (face.h - 1) / 2
    for y in range(face.h):
        for x in range(face.w):
            r = max(abs(x - cx), abs(y - cy))
            face.set(x, y, k("H", base + 1 if int(r + (x > cx)) % 2 == 0 else base))


def bun(g, pid, pivot, rotation=(0, 0, 0), size=(4, 3, 4), seed=0, base=2, cap=True, texture="wrap", motion="none"):
    """A rounded bun: a wound core and a smaller cap on its local -y side, which faces outward."""
    w, h, d = size
    core = g.piece(pid, "HEAD", (-w / 2, -h / 2, -d / 2), size, pivot=pivot, rotation=rotation, motion=motion)
    boxes = [core]
    if texture == "wrap":
        for f in core.sides:
            wrap_face(f, seed + f.x0, base)
        swirl_top(core.top, base + 1)
        core.bottom.fill(k("H", base - 2))
    else:
        paint(core, texture, seed, base, None, 1)
    if cap:
        cw, cd = max(1, w - 2), max(1, d - 2)
        top = g.piece(f"{pid}_cap", "HEAD", (-cw / 2, -h / 2 - 1, -cd / 2), (cw, 1, cd), pivot=pivot, rotation=rotation, motion=motion)
        if texture == "wrap":
            for f in top.sides:
                wrap_face(f, seed + 9 + f.x0, base + 1)
            swirl_top(top.top, base + 2)
            top.bottom.fill(k("H", base - 1))
        else:
            paint(top, texture, seed + 9, base + 1, None, 1)
        boxes.append(top)
    return boxes


def braided_bun(g, pid, pivot, rotation=(0, 0, 0), size=(4, 2, 4), seed=0, base=2):
    """A plait coiled flat into a bun: a plaited ring and a raised plaited centre."""
    w, h, d = size
    ring = g.piece(pid, "HEAD", (-w / 2, -h / 2, -d / 2), size, pivot=pivot, rotation=rotation)
    for i, f in enumerate(ring.sides):
        plait_face(f, base, bool(i % 2))
    for y in range(ring.top.h):
        for x in range(ring.top.w):
            edge = x in (0, ring.top.w - 1) or y in (0, ring.top.h - 1)
            ring.top.set(x, y, k("H", base + (1 if (x + y) % 2 == 0 else 0) - (0 if edge else 1)))
    ring.bottom.fill(k("H", base - 2))
    cw, cd = max(1, w - 2), max(1, d - 2)
    mid = g.piece(f"{pid}_coil", "HEAD", (-cw / 2, -h / 2 - 1, -cd / 2), (cw, 1, cd), pivot=pivot, rotation=rotation)
    for i, f in enumerate(mid.sides):
        plait_face(f, base + 1, bool(i % 2))
    for y in range(mid.top.h):
        for x in range(mid.top.w):
            mid.top.set(x, y, k("H", base + 2 if (x + y) % 2 == 0 else base + 1))
    mid.bottom.fill(k("H", base - 1))
    return [ring, mid]


# -- ornaments (accent role, used sparingly) -------------------------------------------------
def bow(g, pid, center, facing="back", loop=(2, 2), spread=24, tails=0, tail_len=3, role="A", motion="none"):
    """A ribbon bow: a knot, two loops and optional hanging tails. facing: 'back' (loops along x,
    seen from behind), 'side' (loops along z, seen from the side) or 'up' (lying on a bun)."""
    cx, cy, cz = center
    lw, lh = loop
    boxes = [tie(g, f"{pid}_knot", center, size=(1, 1, 1), y=-.5, role=role, base=3, inflate=.15, motion=motion)]
    for name, s in (("r", -1), ("l", 1)):
        if facing == "back":
            origin, size, rot = ((0 if s > 0 else -lw), -lh / 2, -.5), (lw, lh, 1), (0, 0, -spread * s)
        elif facing == "side":
            origin, size, rot = (-.5, -lh / 2, (0 if s > 0 else -lw)), (1, lh, lw), (spread * s, 0, 0)
        else:
            origin, size, rot = ((0 if s > 0 else -lw), -.5, -lh / 2), (lw, 1, lh), (0, 0, spread * s)
        piv = (cx + (.4 * s if facing != "side" else 0), cy, cz + (.4 * s if facing == "side" else 0))
        box = g.piece(f"{pid}_loop_{name}", "HEAD", origin, size, pivot=piv, rotation=rot, motion=motion)
        solid(box, role, "plain", 0, 2, edge=False)
        for f in box.sides:
            f.hline(0, f.w - 1, 0, k(role, 3))
        if facing == "back":
            box.back.set(0 if s < 0 else lw - 1, lh - 1, k(role, 1))
        boxes.append(box)
    for i in range(tails):
        s = -1 if i == 0 else 1
        rot = (0, 0, -10 * s) if facing != "side" else (10 * s, 0, 0)
        box = g.piece(f"{pid}_tail_{i}", "HEAD", (-.5, .2, -.5), (1, tail_len, 1), pivot=(cx, cy, cz), rotation=rot, motion="sway")
        solid(box, role, "plain", 0, 2, edge=False)
        box.strip.hline(0, box.strip.w - 1, tail_len - 1, k(role, 1))
        boxes.append(box)
    return boxes


def flower(g, pid, center, facing="side", petal="A", core="S", size=3):
    """A small blossom: two square petal layers turned 45 degrees to each other and a bright core."""
    boxes = []
    for i, turn in enumerate((0, 45)):
        if facing == "side":
            origin, dims, rot = (-.5 + .15 * i, -size / 2, -size / 2), (1, size, size), (turn, 0, 0)
        else:
            origin, dims, rot = (-size / 2, -size / 2, -.5 - .15 * i), (size, size, 1), (0, 0, turn)
        box = g.piece(f"{pid}_petals_{i}", "HEAD", origin, dims, pivot=center, rotation=rot)
        solid(box, petal, "plain", 0, 3 - i, edge=False)
        boxes.append(box)
    c = tie(g, f"{pid}_core", center, size=(1, 1, 1), y=-.5, role=core, base=4, inflate=.1)
    boxes.append(c)
    return boxes


# -- scalp details ---------------------------------------------------------------------------
def swept_sides(g, ear_from=3, ear_depth=4, base=2):
    """For hair pulled back: after scalp(side_rows=8), bare the ear and jaw at the front of each side and keep
    the hair behind them combed to the nape, with a soft shaded edge where it is drawn back."""
    head = g.part("head")
    for face, front_is_high in ((head.right, True), (head.left, False)):
        for y in range(ear_from, 8):
            for x in range(8):
                dfront = 7 - x if front_is_high else x
                if dfront < ear_depth - (1 if y >= 6 else 0):
                    face.set(x, y, None)
                elif dfront == ear_depth - (1 if y >= 6 else 0):
                    face.set(x, y, k("H", base - 1))
def combed(face, columns, base=2, rows=None):
    """Combed lines: alternating light and shaded columns, for sleek pulled-back hair."""
    for y in (rows if rows is not None else range(face.h)):
        for x in columns:
            if 0 <= x < face.w:
                face.set(x, y, k("H", base + (1 if x % 2 else -1)))


def stubble(face, seed, rows, base=1, bare=.3):
    """Clipped hair: dark speckles with some skin showing through."""
    for y in rows:
        for x in range(face.w):
            r = rnd(x, y, seed + face.x0)
            face.set(x, y, None if r < bare else k("H", base - 1 if r < .6 else base))
