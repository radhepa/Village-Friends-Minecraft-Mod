"""Beacon Keeper's Stair-Worn Boots: thick wool trousers gone shiny at the knee, tucked into slouched ankle boots with
turned-down cuffs, toes scuffed pale by a thousand tower steps and a stitched patch on the side."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_rings
from paint import grid

META = {
    "name": "Beacon Keeper's Stair-Worn Boots",
    "gender": "male",
    "description": "Thick wool trousers worn shiny at the knee, tucked into slouched ankle boots with turned-down cuffs, "
                   "toes scuffed pale by the tower steps and a patch stitched on the side.",
    "tags": ["rugged", "sturdy", "simple"],
}

PATCH = ["sss",
         "s.s",
         "sss"]


def build(g):
    legs(g, "P", "tweed", 33340, rows=(0, 8), crease=False)
    waistband(g, "P", "tweed", 33341)
    footwear(g, "boot", top=8, base=2)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.front.hline(1, 2, 5, "P3"), leg.front.hline(1, 2, 6, "P3")    # knees worn shiny
        leg.front.set(1 if side == "right" else 2, 5, "P4")
        for face in pants.sides:
            face.hline(0, face.w - 1, 11, "K1")
        pants.front.hline(0, 3, 10, "L4"), pants.front.set(1, 11, "L3")   # scuffed toes
        outer = pants.right if side == "right" else pants.left
        grid(outer, 0, 8, PATCH, {"s": "L1"})                              # the stitched side patch
        outer.set(1, 9, "S2")
        pants.back.hline(1, 2, 11, "L3")                                    # heels worn down
    for i, ring in enumerate(leg_rings(g, "boot_cuff", 7.4, "L", (5, 1, 5), 3, "leather", 33342, inflate=.32)):
        for face in ring.sides:
            for x in range(face.w):
                face.set(x, 0, "L3" if (x + face.x0 + i) % 4 else "L1")   # slouched folds
        ring.bottom.fill("L1")
        ring.top.fill("S2")                                                 # the lining shows at the fold
