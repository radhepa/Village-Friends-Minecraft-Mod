"""Small helpers shared by the everyday village basics (tf/bf 286-310).

Each piece keeps its own identity in its module; these only place and paint the little things that
several of them need: props riding a skirt panel, frills round the wrists, and short hanging cords.
"""
from __future__ import annotations

from kit_female import SKIRT_BACK, SKIRT_FRONT, arm_rings
from paint import k, solid


def panel_prop(g, pid: str, s, x: float, y: float, size, back: bool = False, role: str = "M", base: int = 3,
               texture: str = "smooth", seed: int = 0, gap: float = .02):
    """A small cuboid sewn onto a skirt panel (buttons, toggles, tabs). It shares the panel's hinge and
    motion so it rides the stride with it. x is the centre across the panel, y the top below the hinge."""
    w, h, d = size
    z = 1 + gap if back else -d - gap
    box = g.piece(pid, "TORSO", (x - w / 2, y, z), size, pivot=(0, s.top, SKIRT_BACK if back else SKIRT_FRONT),
                  motion="flap_back" if back else "flap_front")
    solid(box, role, texture, seed, base, edge=False)
    return box


def frills(g, prefix: str, y: float, role: str = "S", base: int = 3, size: int = 5, h: int = 1, inflate: float = .1):
    """A gathered frill round each wrist or elbow: alternating lit and shaded folds."""
    boxes = arm_rings(g, prefix, y, h, size, inflate=inflate)
    for box in boxes:
        solid(box, role, "plain", 61, base, edge=False)
        for face in box.sides:
            for x in range(face.w):
                face.vline(x, 0, face.h - 1, k(role, base + 1) if x % 2 == 0 else k(role, base - 1))
        box.bottom.fill(k(role, base - 2))
    return boxes


def cord(g, pid: str, pivot, length: int, role: str = "A", base: int = 2, end: str | None = None,
         rotation=(0, 0, 0), motion: str = "none", bone: str = "TORSO"):
    """A thin hanging cord or ribbon end, one texel square; `end` keys its tip (an aglet, a tassel)."""
    box = g.piece(pid, bone, (-.5, 0, -.5), (1, length, 1), pivot=pivot, rotation=rotation, motion=motion)
    solid(box, role, "plain", 67, base, edge=False)
    for face in box.sides:
        for y in range(1, length, 2):
            face.set(0, y, k(role, base - 1))
    if end:
        box.strip.hline(0, box.strip.w - 1, length - 1, end)
        box.bottom.fill(end)
    return box


def lambswool(face, seed: int = 0, role: str = "S"):
    """Lambswool or fleece: tight little curls rather than long fur."""
    for y in range(face.h):
        for x in range(face.w):
            gx, gy = x + face.x0, y + face.y0
            ring = (gx + 2 * (gy // 2) + seed) % 3
            face.set(x, y, k(role, 4 if ring == 0 and gy % 2 == 0 else 2 if ring == 2 else 3))
