"""Belted Hose and Low Shoes: close wool hose strapped twice round each leg with small buckled belts, over low dark shoes."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_m10 import leg_ring, outer, tie
from paint import solid

META = {
    "name": "Belted Hose and Low Shoes",
    "gender": "male",
    "description": "Close wool hose seamed up the back and held by two little buckled leather belts round each leg, one under the knee and one above the ankle, over low dark shoes.",
    "tags": ["casual", "simple", "slim"],
}


def build(g):
    for side, leg in zip(SIDES, legs(g, "P", "plain", 40520, rows=(0, 9), crease=False)):
        leg.back.vline(1 if side == "right" else 2, 0, 9, "P1")           # back seam
        outer(leg, side).vline(2, 1, 9, "P1")
    body = waistband(g, "P", "plain", 40521)
    body.front.vline(4, 10, 11, "P1")
    footwear(g, "shoe", top=10, role="K", base=2, sole="K0")
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.hline(0, 3, 10, "K3")
    for i, side in enumerate(SIDES):
        for j, y in enumerate((4.6, 8.2)):
            strap = leg_ring(g, f"{side}_leg_belt_{j}", side, y, (5, 1, 5), "L", 2, "leather", 40522 + 2 * i + j,
                             open_bottom=False)
            for face in strap.sides:
                face.hline(0, face.w - 1, 0, "L2")
            buckle = g.piece(f"{side}_leg_buckle_{j}", leg_bone(side), (-.5, -.5, -.5), (1, 1, 1),
                             pivot=(-2.55 if side == "right" else 2.55, y + .5, -.9))
            solid(buckle, "M", "smooth", 40526 + j, 3, edge=False)
            tie(g, f"{side}_leg_belt_end_{j}", leg_bone(side), (-2.65 if side == "right" else 2.65, y + 1.0, .2),
                "L", 2, 2, 40528 + j, motion="none")
