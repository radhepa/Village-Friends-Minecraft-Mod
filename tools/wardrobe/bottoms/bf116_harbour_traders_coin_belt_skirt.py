"""Harbour Trader's Coin-Belt Skirt: a long overskirt parted at the front over a banded underskirt, a broad
coin belt studded with pennies round the hips with two heavy purses hanging, over pointed shoes."""
from kit_female import pleats, shoes, skirt, trim, waist_belt
from paint import fabric, solid

META = {
    "name": "Harbour Trader's Coin-Belt Skirt",
    "gender": "female",
    "description": "A long overskirt parted over a banded underskirt, a broad coin-studded belt with two heavy purses, and pointed shoes.",
    "tags": ["tailored", "long_skirt", "skirt"],
}

SEED = 53195


def build(g):
    s = skirt(g, "P", "weave", SEED, top=9.6, length=12, flare=6, folds=False)
    f = s.front.front
    fabric(f, "S", "weave", SEED + 1, 3, 3, 1, 4, f.h - 1)           # the underskirt showing between
    for y in range(3, f.h - 1, 3):
        f.hline(3, 6, y, "S2")                                       # its sewn bands
    f.vline(2, 1, f.h - 1, "P3"), f.vline(7, 1, f.h - 1, "P3")      # the overskirt's faced edges
    f.vline(1, 2, f.h - 2, "P1"), f.vline(8, 2, f.h - 2, "P1")
    trim(f, f.h - 1, "line", "A2", x0=3, x1=6)
    pleats(s.back.back, "P", 2, 3, y0=2, lit=True)
    for face in s.faces:
        face.hline(0, face.w - 1, face.h - 1, "P1")
    f.hline(3, 6, f.h - 1, "A2")
    belt = waist_belt(g, "waist_coin_belt", 9.2, role="L", base=2, height=2, buckle="M")
    for face in belt.sides:
        for x in range(1, face.w, 3):
            face.set(x, 1, "M4")                                     # pennies riveted on
    for i, x in enumerate((-1.2, 3.2)):
        purse = g.piece(f"waist_purse_{i}", "TORSO", (-1, 1.4, -1.2), (2, 3, 1), pivot=(x, 9.6, -3.1), motion="flap_front",
                        inflate=.1)
        solid(purse, "L", "leather", SEED + 2 + i, 1)
        purse.front.hline(0, 1, 0, "L3")
        purse.front.set(0, 1, "M3") if i == 0 else purse.front.set(1, 1, "M3")
        purse.top.fill("M3")                                         # its mouth stuffed with coin
        purse.top.set(0, 0, "M4")
    shoes(g, "pointed", "K", 2, toe="K3")
