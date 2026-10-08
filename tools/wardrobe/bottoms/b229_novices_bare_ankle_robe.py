"""Novice's Bare-Ankle Robe: an undyed robe skirt grown short at the shin and let down with a paler band, over bare ankles and bare feet."""
from kit import SIDES, waistband
from kit_male import bare_feet, skirt_panels
from paint import strip_fabric

META = {
    "name": "Novice's Bare-Ankle Robe",
    "gender": "male",
    "description": "An undyed robe skirt he has already outgrown, let down once with a band of paler cloth and still stopping at mid-shin, over bare ankles and bare feet.",
    "tags": ["holy", "robe", "simple"],
    "rejects": ["armor"],
}


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "S", "weave", 35340 + (side == "left"), 2, 0, 5)       # linen braies under the robe
        leg.top.fill("S2")
        leg.strip.hline(0, leg.strip.w - 1, 5, "S1")
    bare_feet(g, rows=(6, 11))
    waistband(g, "S", "weave", 35342, base=3)
    front, back, sides = skirt_panels(g, "robe", 9, "S", "weave", 35343, base=3, top=10.6, side_len=8)
    for face in (front, back):
        for y in range(1, 6):                                              # running-stitch centre seam
            face.set(4, y, "S2" if y % 2 else "S3")
        face.vline(1, 1, 5, "S2"), face.vline(7, 1, 5, "S2")
        face.hline(0, 8, 6, "S1")                                          # the let-down seam
        face.hline(0, 8, 7, "S4"), face.hline(0, 8, 8, "S3")              # paler new band
        for x in range(0, 9, 2):
            face.set(x, 6, "S2")
    for box in sides:
        for face in box.sides:
            face.hline(0, face.w - 1, box.h - 3, "S1")
            face.hline(0, face.w - 1, box.h - 2, "S4"), face.hline(0, face.w - 1, box.h - 1, "S3")
