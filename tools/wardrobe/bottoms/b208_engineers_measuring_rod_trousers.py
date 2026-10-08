"""Engineer's Measuring-Rod Trousers: canvas trousers with a graduated rod carried in a long pocket down the right leg."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk
from kit_m04 import patch, sides_of

META = {
    "name": "Engineer's Measuring-Rod Trousers",
    "gender": "male",
    "description": "Straight canvas trousers with a patched left knee and a long leather pocket down the right leg holding a "
                   "graduated measuring rod marked off in pale and dark spans, over laced shoes.",
    "tags": ["work", "scholarly", "sturdy"],
}

S = 34500


def build(g):
    legs(g, "S", "twill", S, rows=(0, 9), crease=True)
    waistband(g, "S", "twill", S + 2)
    footwear(g, "shoe", top=10, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.set(1, 10, "L1"), pants.front.set(2, 10, "L1")          # laces
    patch(g.part("left_leg").front, 0, 4, 3, 3, "S", 1, "L2")
    # The rod pocket and rod on the outer right leg.
    pocket = leg_blk(g, "right_rod_pocket", "right", 1.0, (1, 7, 2), "L", 2, "leather", S + 3, dx=-2.4)
    outer = pocket.right
    outer.hline(0, 1, 0, "L4"), outer.hline(0, 1, 3, "L1"), outer.hline(0, 1, 6, "L1")
    rod = leg_blk(g, "right_measuring_rod", "right", -2.0, (1, 10, 1), "S", 3, "plain", S + 4, dx=-2.6, dz=-.2)
    for face in rod.sides:
        for y in range(10):
            face.set(0, y, "S4" if (y // 2) % 2 == 0 else "K1")            # graduated spans
    rod.top.fill("A2")
