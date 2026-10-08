"""Patched-Knee Work Breeches: twill knee breeches with mismatched cloth patches, corded under the knee."""
from kit import SIDES, legs, waistband
from kit_female import hose, leg_rings, shoes, waist_belt
from kit_f10 import cord
from paint import fabric, solid

META = {
    "name": "Patched-Knee Work Breeches",
    "gender": "female",
    "description": "Twill knee breeches mended with mismatched patches of other cloth, corded under the knee over ribbed stockings and low shoes.",
    "tags": ["work", "sturdy", "rugged"],
}


def build(g):
    legs(g, "P", "twill", 60260, rows=(0, 7), crease=False)
    waistband(g, "P", "twill", 60261)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.strip.hline(0, 15, 7, "P1")
        if side == "right":                                            # a square patch of undyed cloth
            fabric(pants.front, "S", "weave", 60262, 2, 0, 3, 3, 3)
            pants.front.hline(0, 2, 3, "S3")
            for x, y in ((0, 5), (2, 5), (2, 4)):
                pants.front.set(x, y, "S1")                            # running stitches round its edge
        else:                                                          # a tall patch in another cloth
            fabric(pants.front, "A", "weave", 60263, 2, 1, 2, 3, 4)
            pants.front.hline(1, 3, 2, "A3")
            pants.front.set(1, 4, "A1"), pants.front.set(3, 5, "A1")
        leg.back.vline(1 if side == "right" else 2, 0, 6, "P1")
    hose(g, "S", rows=(8, 11), base=3, texture="rib", seam=False)
    shoes(g, "shoe", "L", 2)
    for ring in leg_rings(g, "garter", 7.1, 1, 5, inflate=.05):
        solid(ring, "L", "leather", 60264, 3, edge=False)
    for side in SIDES:
        x = -2.7 if side == "right" else 2.7
        cord(g, f"{side}_garter_end", (x, 7.6, -.6), 2, role="L", base=3, end="L1",
             rotation=(0, 0, 10 if side == "right" else -10), bone="RIGHT_LEG" if side == "right" else "LEFT_LEG")
    waist_belt(g, "waist_cord", 9.4, role="L", base=2, height=1, buckle=None)
