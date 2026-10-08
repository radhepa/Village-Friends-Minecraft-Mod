"""Governess's Sober Skirt: a narrow, straight floor-length skirt in plain dark wool with two thin black
guards above the hem and a buttoned placket down the left hip, over plain black shoes."""
from kit_female import shoes, skirt

META = {
    "name": "Governess's Sober Skirt",
    "gender": "female",
    "description": "A narrow straight skirt of plain dark wool with two thin black guards and a buttoned placket at the hip.",
    "tags": ["tailored", "simple", "skirt", "long_skirt", "slim"],
}


def build(g):
    s = skirt(g, "P", "plain", 55291, base=1, top=9.8, length=12, back_length=12, flare=2, folds=False, gather=False)
    for face in s.wide_faces:
        face.vline(3, 2, face.h - 1, "P0"), face.vline(6, 2, face.h - 1, "P0")
        face.vline(4, 3, face.h - 2, "P2")
    s.band(4, "line", "K1", from_bottom=True)
    s.band(2, "line", "K1", from_bottom=True)
    s.hem("P0")
    # The buttoned placket on the left hip.
    placket = s.left.left
    placket.vline(2, 0, 5, "P0")
    for y in range(0, 6, 2):
        placket.set(2, y, "M3")
    shoes(g, "shoe", "K", 2)
