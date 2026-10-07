"""Guarded Underskirt: a pale underskirt banded with three upright guards and a deep hem guard, over soft slippers."""
from kit_female import shoes, skirt

META = {
    "name": "Guarded Underskirt",
    "gender": "female",
    "description": "A pale underskirt trimmed with three upright velvet guards and a deep hem guard, over soft slippers.",
    "tags": ["fancy", "tailored", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "S", "weave", 15411, base=3, top=9.8, length=12, folds=False)
    for face in s.wide_faces:
        for x in (1, 4, 5, 8):
            face.vline(x, 1, face.h - 1, "P2")
        face.vline(4, 1, face.h - 1, "M3")
    s.band(2, "line", "P2", from_bottom=True)
    s.band(1, "line", "P2", from_bottom=True)
    s.band(0, "line", "P1", from_bottom=True)
    shoes(g, "slipper", "P", 2)
