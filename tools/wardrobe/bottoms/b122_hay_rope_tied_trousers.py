"""Hay-Rope Tied Trousers: loose field trousers bound twice round each shin with twists of hay rope, and a hay-rope belt."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_m01 import twisted_box
from kit_male import blk
from paint import strip_fabric

META = {
    "name": "Hay-Rope Tied Trousers",
    "gender": "male",
    "description": "Loose field trousers bloused between twists of hay rope bound twice round each shin, a hay-rope belt with straggling ends, and low shoes.",
    "tags": ["work", "rugged", "simple"],
}


def build(g):
    legs(g, "P", "twill", 31111, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 31112)
    footwear(g, "shoe", top=10, base=1)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(pants, "P", "twill", 31120 + i, 2, 0, 9)              # roomy legs standing off
        for face in pants.sides:                                           # bloused folds between the ties
            face.vline(0, 1, 3, "P1")
            face.vline(2, 4, 5, "P3"), face.vline(1, 7, 8, "P3")
            face.set(2, 6, "P1"), face.set(1, 9, "P1")
        for face in leg.sides:
            face.vline(2, 1, 4, "P1")
        for j, y in enumerate((5.2, 8.4)):
            ring = g.piece(f"{side}_hay_rope_{j}", leg_bone(side), (-2.5, y, -2.5), (5, 1, 5), inflate=.12 + .02 * j)
            twisted_box(ring, "S", 3, ox=i + j)
            stalk = blk(g, f"{side}_hay_wisp_{j}", (-2.6 if side == "right" else 2.6, y - .2, -1.2 + j), (1, 2, 1),
                        "S", 4, "plain", 31113 + 2 * i + j, bone=leg_bone(side),
                        rotation=(0, 0, 28 if side == "right" else -28), edge=False)
            stalk.strip.hline(0, stalk.strip.w - 1, 1, "S2")
    belt = g.piece("waist_hay_rope", "TORSO", (-4.6, 9.4, -2.6), (9, 1, 5), inflate=.1)
    twisted_box(belt, "S", 3)
    for i, (x, rz) in enumerate(((-1.6, 14), (-.8, -6))):
        end = g.piece(f"waist_hay_end_{i}", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(x, 10.2, -2.85),
                      rotation=(0, 0, rz), motion="sway")
        twisted_box(end, "S", 3, ox=i)
        end.strip.hline(0, end.strip.w - 1, 2, "S4")
