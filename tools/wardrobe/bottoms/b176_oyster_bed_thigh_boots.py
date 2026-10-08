"""Oyster-Bed Thigh Boots: wet-shining leather boots to the top of the thigh, a grey silt line at the knee, buckled
garters and straps running up to the belt to hold them high."""
from kit import SIDES, belt, footwear, legs, waistband
from kit_m03 import gloss
from kit_male import leg_rings

META = {
    "name": "Oyster-Bed Thigh Boots",
    "gender": "male",
    "description": "Wet-shining leather boots reaching the top of the thigh, a grey silt line at the knee, buckled knee "
                   "garters and straps running up to the belt to hold them high.",
    "tags": ["sea", "sturdy", "work"],
}


def build(g):
    legs(g, "P", "twill", 33220, rows=(0, 1), crease=False)
    body = waistband(g, "P", "twill", 33221)
    footwear(g, "boot", top=1, base=2, sole="K0")
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in pants.sides:
            gloss(face, "L", 2, 33222 + i, rows=range(2, 10), crease=0)
            face.hline(0, face.w - 1, 1, "L3")                          # the stiff boot top
            for x in range(face.w):                                     # grey silt dried below the knee
                face.set(x, 7, "K3" if (x + face.x0) % 3 else "K2")
                if (x + face.x0) % 4 == 1:
                    face.set(x, 8, "K3")
        outer = leg.right if side == "right" else leg.left
        outer_p = pants.right if side == "right" else pants.left
        outer.vline(1, 0, 1, "L1"), outer_p.vline(1, 0, 1, "L1")       # the strap up to the belt
        side_face = body.right if side == "right" else body.left
        side_face.vline(1, 10, 11, "L1"), side_face.set(1, 9, "M3")
    belt(g, "waist_belt", 9.4, height=1, inflate=.04)
    for ring in leg_rings(g, "knee_garter", 4.4, "L", (5, 1, 5), 1, "leather", 33224, inflate=.3):
        ring.front.set(1, 0, "M3"), ring.front.set(2, 0, "M4")
    for ring in leg_rings(g, "boot_top", .6, "L", (5, 1, 5), 2, "leather", 33226, inflate=.32):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L3")
        ring.top.fill("K1")
