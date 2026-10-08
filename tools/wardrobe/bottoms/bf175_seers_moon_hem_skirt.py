"""Seer's Moon-Hem Skirt: a long dark skirt with a hem band embroidered with the moon's phases, from
dark to full and back, above an edge cut in soft scallops."""
from kit_female import shoes, skirt
from paint import grid

META = {
    "name": "Seer's Moon-Hem Skirt",
    "gender": "female",
    "description": "A long dark skirt with the moon's phases embroidered round the hem, dark to full and back, above a scalloped edge.",
    "tags": ["whimsical", "skirt", "long_skirt"],
}

# Moon phases in 3x3 cells: new, waxing crescent, half, gibbous, full, then back again.
PHASES = [
    [".o.", "o.o", ".o."],
    [".m.", "..m", ".m."],
    [".m.", ".mm", ".m."],
    [".m.", "mmm", ".m."],
    [".m.", "mbm", ".m."],
    [".m.", "mmm", ".m."],
    [".m.", "mm.", ".m."],
    [".m.", "m..", ".m."],
]


def moon_band(face, y0, offset=0):
    """A dark band three rows high, the phases marching round it one cell every four texels."""
    for y in range(y0 - 1, y0 + 4):
        face.hline(0, face.w - 1, y, "P0")
    face.hline(0, face.w - 1, y0 - 1, "M2"), face.hline(0, face.w - 1, y0 + 3, "M2")
    for i, x in enumerate(range(0, face.w, 4)):
        grid(face, x, y0, PHASES[(i + offset) % len(PHASES)], {"m": "S4", "b": "M4", "o": "K3"})


def scallops(face):
    """A soft scalloped edge: every third texel dips."""
    for x in range(face.w):
        face.set(x, face.h - 1, "P0" if x % 3 == 2 else "P2")


def build(g):
    s = skirt(g, "P", "velvet", 55411, base=1, top=9.8, length=12, back_length=12, flare=6, folds=True, gather=False)
    for i, face in enumerate(s.wide_faces):
        moon_band(face, face.h - 5, offset=i * 3)
        scallops(face)
    for box in (s.right, s.left):
        outer = box.right if box is s.right else box.left
        moon_band(outer, outer.h - 5, offset=2)
        scallops(outer)
    shoes(g, "pointed", "K", 2)
