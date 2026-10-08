"""Militia Woman's Kilted Skirt over Hose: a long wool skirt hitched up at the front into a bunch at the belt so
it falls in swags, showing banded hose and low shoes, the back still hanging long."""
from kit import SIDES
from kit_female import shoes, skirt, waist_belt
from paint import line, solid

META = {
    "name": "Militia Woman's Kilted Skirt over Hose",
    "gender": "female",
    "description": "A long wool skirt hitched up at the front into a bunch at the belt so it falls in swags, over "
                   "banded hose and low shoes, the back still hanging long.",
    "tags": ["sturdy", "skirt", "simple"],
}


def build(g):
    s = skirt(g, "P", "weave", 54261, top=9.8, length=6, back_length=11, side_length=8, flare=7, folds=False)
    f = s.front.front
    for x0 in (1, 3, 6, 8):                                          # swags radiating from the hitch
        line(f, 5 if x0 > 4 else 4, 1, x0, 5, "P1")
    for x in range(f.w):
        f.set(x, 5, "P3" if x % 3 else "P1")                         # the hitched edge, rolled
    bk = s.back.back
    for x in range(2, bk.w - 1, 3):
        bk.vline(x, 2, bk.h - 2, "P1"), bk.vline(x + 1, 3, bk.h - 3, "P3")
    bk.hline(0, bk.w - 1, bk.h - 1, "P1")
    for box in (s.right, s.left):
        for face in (box.right, box.left, box.front, box.back):
            face.hline(0, face.w - 1, face.h - 1, "P1")
    # Banded hose under the hitched skirt.
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for y in range(4, 10):
            leg.strip.hline(0, 15, y, "S3" if y % 2 == 0 else "A2")
    shoes(g, "shoe", "L", 2)
    hitch = g.piece("waist_hitch", "TORSO", (-1.5, 0, -1), (3, 3, 2), pivot=(0, 9.6, -3.1))
    solid(hitch, "P", "weave", 54262, 2)
    hitch.front.vline(1, 0, 2, "P1"), hitch.front.set(0, 0, "P3"), hitch.front.set(2, 0, "P3")
    waist_belt(g, "waist_belt", 9.3, height=1)
