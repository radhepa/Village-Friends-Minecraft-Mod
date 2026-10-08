"""Shared helpers for the women's crafts-and-trades batch (tf/bf 086-110).

Small tools and props that hang from the girdle and ride the stride, hollow rings, bobbin lace,
silk sheen and straps across the body. Each piece keeps its own identity (its tools, trims and
cut) in its own module; these only remove repetition.
"""
from __future__ import annotations

from kit_female import OVER_FRONT
from paint import k, line, rnd, solid

HANG_Z = OVER_FRONT - .1        # hinge depth for tools hung at the girdle: in front of any skirt or apron
HANG_TOP = 9.0                  # the girdle line tools hang from


def prop(g, pid, bone, origin, size, pivot=(0, 0, 0), role="L", base=2, texture="smooth", seed=0,
         rotation=(0, 0, 0), motion="none", inflate=0.0, edge=False):
    """A solid little cuboid; returns its box so the module can paint its details."""
    box = g.piece(pid, bone, origin, size, pivot=pivot, rotation=rotation, motion=motion, inflate=inflate)
    solid(box, role, texture, seed, base, edge=edge)
    return box


def hung(g, pid, x, y, size, role="L", base=2, texture="smooth", seed=0, top=HANG_TOP, dx=0.0, rotation=(0, 0, 0),
         inflate=0.0, edge=False):
    """An object hanging at the girdle: its top is y texels below the hinge at (x, top). The back face
    stays just in front of any skirt or apron and the whole thing rides the leading leg."""
    w, h, d = size
    return prop(g, pid, "TORSO", (-w / 2 + dx, y, .9 - d), size, pivot=(x, top, HANG_Z), role=role, base=base,
                texture=texture, seed=seed, rotation=rotation, motion="flap_front", inflate=inflate, edge=edge)


def cord(g, pid, x, length, role="L", base=2, top=HANG_TOP, seed=0):
    """A one-texel cord or chain from the girdle line, riding the stride with what hangs from it."""
    box = hung(g, pid, x, 0, (1, length, 1), role, base, "plain", seed, top)
    box.strip.hline(0, box.strip.w - 1, 0, k(role, base + 1))
    return box


def back_prop(g, pid, origin, size, role="L", base=2, texture="smooth", seed=0, rotation=(0, 0, 0), z=2.55):
    """A still prop carried on the back: origin is relative to (0, 0, z) on the torso."""
    return prop(g, pid, "TORSO", origin, size, pivot=(0, 0, z), role=role, base=base, texture=texture, seed=seed,
                rotation=rotation)


def ring(g, prefix, cx, cy, w, h, z=2.6, role="M", base=2, rotation=(0, 0, 0), seed=0, thick=1):
    """A hollow upright ring (a hoop or frame) from four thin bars, in a plane parallel to the back.
    All bars share one pivot, so a rotation turns the whole ring."""
    bars = {
        "top": ((-w / 2, -h / 2, 0), (w, thick, 1)),
        "bottom": ((-w / 2, h / 2 - thick, 0), (w, thick, 1)),
        "right": ((-w / 2, -h / 2 + thick, 0), (thick, h - 2 * thick, 1)),
        "left": ((w / 2 - thick, -h / 2 + thick, 0), (thick, h - 2 * thick, 1)),
    }
    out = {}
    for name, (origin, size) in bars.items():
        box = prop(g, f"{prefix}_{name}", "TORSO", origin, size, pivot=(cx, cy, z), role=role, base=base,
                   seed=seed + len(out), rotation=rotation)
        for face in box.sides:
            face.hline(0, face.w - 1, 0, k(role, base + 1))
        out[name] = box
    return out


def lace(face, ground="S4", hole="S2", picot=True, x0=0, y0=0, w=None, h=None, phase=0):
    """Bobbin lace: a pale ground pricked with a staggered net of holes and a picot (scalloped) edge."""
    w = face.w - x0 if w is None else w
    h = face.h - y0 if h is None else h
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            dy = y - y0
            key = ground
            if dy % 2 == 1 and (x + phase + dy // 2) % 2 == 0:
                key = hole
            face.set(x, y, key)
    if picot and h > 1:
        for x in range(x0, x0 + w):
            face.set(x, y0 + h - 1, hole if (x + phase) % 2 else ground)


def sheen(face, role="P", base=2, period=7, phase=0, x0=0, y0=0, w=None, h=None, slope=1):
    """Silk catching the light: soft diagonal gleams with a shaded fold between them."""
    w = face.w - x0 if w is None else w
    h = face.h - y0 if h is None else h
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            d = (x + slope * y + phase + face.x0) % period
            s = base + 2 if d == 0 else base + 1 if d in (1, period - 1) else base - 1 if d == period // 2 else base
            face.set(x, y, k(role, s))


def strap(face, x0, y0, x1, y1, key, width=1, edge=None):
    """A strap or cord across a face as a (thick) line, with an optional lit edge above it."""
    for i in range(width):
        line(face, x0 + i, y0, x1 + i, y1, key)
    if edge:
        line(face, x0, y0 - 1, x1, y1 - 1, edge)


def specks(face, key, seed, density=.12, x0=0, y0=0, w=None, h=None, only_on=None):
    """Fine dust or spatter: sparse single texels (only over painted cloth)."""
    w = face.w - x0 if w is None else w
    h = face.h - y0 if h is None else h
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            cur = face.get(x, y)
            if cur and (only_on is None or cur[0] in only_on) and rnd(x + face.x0, y + face.y0, seed) < density:
                face.set(x, y, key)
