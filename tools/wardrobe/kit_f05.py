"""Small shared helpers for the healers, faith and learning batch (tf/bf 161-185).

Only the mechanics live here: little objects that ride the stride below a girdle, objects fixed on
the chest, bead strings, glass and lap panels on a skirt. Each garment keeps its own identity
(what hangs, where, and how it is decorated) in its own module.
"""
from __future__ import annotations

from kit_female import OVER_BACK, OVER_FRONT, SKIRT_FRONT
from paint import k, solid


def dangle(g, pid: str, x: float, y: float, size, role: str = "M", base: int = 3, texture: str = "smooth",
           top: float = 9.0, seed: int = 0, back: bool = False, edge: bool = True):
    """A small object hung below the waist from a girdle hinge at (x, top): it rides the stride in front
    of (or behind) every over-layer, so it never cuts through a skirt or apron. y is how far below the
    hinge its top edge hangs."""
    w, h, d = size
    if back:
        box = g.piece(pid, "TORSO", (-w / 2, y, .1), size, pivot=(x, top, OVER_BACK + 1.1), motion="flap_back")
    else:
        box = g.piece(pid, "TORSO", (-w / 2, y, -.1 - (d - 1)), size, pivot=(x, top, OVER_FRONT - .1),
                      motion="flap_front")
    solid(box, role, texture, seed, base, edge=edge)
    return box


def fixed(g, pid: str, center, size, role: str = "M", base: int = 3, texture: str = "smooth", seed: int = 0,
          rotation=(0, 0, 0), inflate: float = 0.0, edge: bool = True):
    """A still object on the torso (badges, books, jars on a belt) centred on `center` (x, y, z)."""
    w, h, d = size
    box = g.piece(pid, "TORSO", (-w / 2, -h / 2, -d / 2), size, pivot=center, rotation=rotation, inflate=inflate)
    solid(box, role, texture, seed, base, edge=edge)
    return box


def beads(face, x: int, y0: int, y1: int, a: str, b: str, every: int = 2, gaud: str | None = None, decade: int = 0):
    """A string of beads down a column: a/b alternate; with `decade`, every n-th bead is a larger gaud."""
    for i, y in enumerate(range(y0, y1 + 1)):
        key = a if i % every == 0 else b
        if gaud and decade and i % decade == decade - 1:
            key = gaud
        face.set(x, y, key)


def glass(box, role: str = "S", base: int = 4, fill: str | None = None, fill_from: int = 1):
    """Paint a small glass vessel: a pale body with a lit stripe and optional contents from row fill_from."""
    for face in box.sides:
        for y in range(face.h):
            face.hline(0, face.w - 1, y, k(role, base - (1 if y == face.h - 1 else 0)))
            if fill and y >= fill_from:
                face.hline(0, face.w - 1, y, fill)
        face.set(0, 0, k(role, min(4, base + 1)))
    box.top.fill(k(role, base))


def lap_panel(g, top: float, pid: str, y: float, h: int, width: int, role: str, base: int = 2, texture: str = "weave",
              seed: int = 0, x: float = 0.0):
    """A panel sewn on the front of a skirt (lap guards, pocket bands): shares the skirt's hinge and
    sits a hair in front of its front panel, under any top's over-layer."""
    box = g.piece(pid, "TORSO", (-width / 2 + x, y, -.1), (width, h, 1), pivot=(0, top, SKIRT_FRONT), motion="flap_front",
                  inflate=.02)
    solid(box, role, texture, seed, base)
    return box
