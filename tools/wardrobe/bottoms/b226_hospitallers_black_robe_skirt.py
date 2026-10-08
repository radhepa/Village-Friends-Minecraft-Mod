"""Hospitaller's Black Robe Skirt: a plain black ankle robe split for riding, paternoster beads at the hip, over riding boots with prick spurs."""
from kit import SIDES, footwear, waistband
from kit_male import leg_blk, skirt_panels
from kit_m05 import hose
from paint import solid

META = {
    "name": "Hospitaller's Black Robe Skirt",
    "gender": "male",
    "description": "A brother's plain black robe to the ankle, split before and behind for the saddle, a string of paternoster beads at the hip, over riding boots with iron prick spurs.",
    "tags": ["holy", "robe", "sturdy"],
}


def build(g):
    hose(g, "K", 2, "weave", 35210, end=9)
    waistband(g, "K", "weave", 35211)
    footwear(g, "boot", top=8, role="L", base=1, sole="K0")
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 8, "L3")
        pants.front.vline(1 if side == "right" else 2, 9, 10, "L2")
        spur = leg_blk(g, f"{side}_spur", side, 10.3, (1, 1, 2), "M", 3, "smooth", 35212, dz=2.6)
        spur.right.set(1, 0, "M4"), spur.left.set(1, 0, "M4")
        strap = leg_blk(g, f"{side}_spur_strap", side, 10.2, (5, 1, 5), "L", 1, "leather", 35213, inflate=.06)
        strap.front.set(2, 0, "M3")
    front, back, sides = skirt_panels(g, "robe", 11, "K", "weave", 35214, top=10.6, side_len=10)
    for face in (front, back):
        face.vline(4, 4, 10, "K0")                                      # the riding split
        face.vline(3, 4, 10, "K1"), face.vline(5, 4, 10, "K3")
        for x in (1, 7):
            face.vline(x, 1, 10, "K1")
        face.hline(0, 8, 10, "K0")
    for box in sides:
        for face in box.sides:
            face.vline(1, 1, box.h - 2, "K1")
            face.hline(0, face.w - 1, box.h - 1, "K0")
    # Paternoster beads: a loop of wooden beads hung from the girdle, ending in a little cross.
    for i in range(5):
        bead = g.piece(f"paternoster_{i}", "TORSO", (-.5, 0, -.5), (1, 1, 1), pivot=(-5.6, 11.0 + i * 1.05, -1.2),
                       motion="flap_front")
        solid(bead, "L", "plain", 35215 + i, 3 if i % 2 == 0 else 2, edge=False)
    cross = g.piece("paternoster_cross", "TORSO", (-.5, 0, -1.5), (1, 1, 3), pivot=(-5.6, 16.6, -1.2), motion="flap_front")
    solid(cross, "S", "plain", 35221, 4, edge=False)
    stem = g.piece("paternoster_stem", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(-5.6, 16.0, -1.2), motion="flap_front")
    solid(stem, "S", "plain", 35222, 4, edge=False)
