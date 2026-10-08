"""Crossbowman's Quilted Leggings: diamond-quilted padded thighs ending in a tied knee roll, knitted hose and ankle shoes."""
from kit import SIDES, footwear, leg_ring, waistband
from kit_male import lacing, lozenge
from kit_m04 import sides_of
from paint import fabric, strip_fabric

META = {
    "name": "Crossbowman's Quilted Leggings",
    "gender": "male",
    "description": "Padded leggings diamond-quilted down to a fat tied roll at the knee, laced up the outer thigh, "
                   "over dark knitted hose and buckled ankle shoes.",
    "tags": ["martial", "sturdy"],
}

S = 34060


def build(g):
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "P", "knit", S + (side == "left"), 1, 0, 9)
        fabric(leg.top, "S", "quilt", S, 2)
        for face in pants.sides:
            lozenge(face, "S", 2, step=4, ox=face.x0, rows=range(0, 5))
            face.hline(0, face.w - 1, 0, "S3")
        outer = getattr(pants, sides_of(side)[0])
        lacing(outer, 1, 1, 4, "L3", "L1")                               # laced outer seam
        leg.strip.hline(0, leg.strip.w - 1, 9, "P0")
    waistband(g, "S", "quilt", S + 2)
    footwear(g, "shoe", top=10, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        getattr(pants, sides_of(side)[0]).set(1, 10, "M3")              # ankle buckle
    for i, ring in enumerate(leg_ring(g, "knee_roll", 5.0, "S", base=2, size=(5, 2, 5), texture="quilt", inflate=.12)):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "S3"), face.hline(0, face.w - 1, 1, "S1")
            face.set(2, 1, "S2")
        tie = ring.right if i == 0 else ring.left
        tie.set(2, 0, "L3"), tie.set(2, 1, "L1")                          # the tie at the outside of the knee
