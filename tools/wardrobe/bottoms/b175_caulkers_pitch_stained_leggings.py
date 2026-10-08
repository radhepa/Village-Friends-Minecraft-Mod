"""Caulker's Pitch-Stained Leggings: close wool leggings blackened with pitch from the shin down, thick quilted leather
kneeling pads strapped over the knees, and soft turnshoes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk
from paint import k

META = {
    "name": "Caulker's Pitch-Stained Leggings",
    "gender": "male",
    "description": "Close wool leggings blackened with pitch from the shin down, quilted leather kneeling pads strapped "
                   "over both knees, and soft turnshoes.",
    "tags": ["work", "sturdy", "sea"],
}

# The pitch line climbs and dips around the leg: the first stained row per strip column.
EDGE = [7, 7, 6, 6, 7, 8, 7, 6, 6, 7, 7, 8, 8, 7, 7, 6]


def build(g):
    legs(g, "P", "rib", 33180, rows=(0, 9), crease=False)
    body = waistband(g, "P", "rib", 33181)
    body.front.set(3, 9, "P0"), body.front.set(4, 9, "P0")
    footwear(g, "turnshoe", top=10, base=1)
    for i, side in enumerate(SIDES):
        leg = g.part(f"{side}_leg").strip
        for x, top in enumerate(EDGE):
            for y in range(top, 10):
                leg.set(x, y, "K1" if y > top else "K2")
            if (x + i) % 5 == 0:
                leg.set(x, top + 1, "K3")                                # a wet gleam on the pitch
        # The kneeling pad: a quilted leather plate on a strap, standing proud of the knee.
        pad = leg_blk(g, f"{side}_knee_pad", side, 3.4, (4, 4, 1), "L", 2, "leather", 33182 + i, dz=-2.45, inflate=.05)
        f = pad.front
        for y in range(4):
            for x in range(4):
                f.set(x, y, k("L", 1 if (x + y) % 3 == 0 else 2))       # diamond stitching
        f.hline(0, 3, 0, "L3")
        strap = leg_blk(g, f"{side}_knee_strap", side, 4.6, (5, 1, 5), "L", 1, "leather", 33184 + i, inflate=.08)
        strap.right.set(2, 0, "M3") if side == "right" else strap.left.set(2, 0, "M3")
