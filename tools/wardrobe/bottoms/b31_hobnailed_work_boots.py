"""Hobnailed Work Boots: rough twill trousers with darned knees, in laced ankle boots studded with hobnails and capped in iron."""
from kit import SIDES, footwear, legs, waistband
from kit_male import lacing, toe_pieces

META = {
    "name": "Hobnailed Work Boots",
    "gender": "male",
    "description": "Rough twill trousers with darned knees, tucked into laced ankle boots studded with hobnails and capped in iron.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 3111, rows=(0, 8), crease=False)
    waistband(g, "P", "twill", 3112)
    footwear(g, "boot", top=7, base=2)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.front.rect(1, 3, 2, 2, "P1")                               # darned knee
        leg.front.set(1, 3, "P3")
        lacing(pants.front, 1, 7, 9, "L4", "L1")
        for face in pants.sides:
            face.hline(0, face.w - 1, 7, "L3")
            for x in range(face.w):
                face.set(x, 11, "M2" if x % 3 == 1 else "K1")       # hobnails round the sole
        pants.bottom.paint(lambda x, y, cur: "M1" if x % 2 == 1 and y % 2 == 1 else "K0")
    for cap in toe_pieces(g, "toe_cap", (4, 2, 1), "M", base=2, y=9.9, z=-2.1):
        cap.front.hline(0, 3, 0, "M4")
        cap.front.set(0, 1, "M1"), cap.front.set(3, 1, "M1")
