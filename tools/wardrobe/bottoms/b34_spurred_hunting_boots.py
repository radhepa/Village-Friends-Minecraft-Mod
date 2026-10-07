"""Spurred Hunting Boots: buff riding breeches in calf boots with buckled ankle straps and prick spurs."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk

META = {
    "name": "Spurred Hunting Boots",
    "gender": "male",
    "description": "Buff riding breeches in close calf boots, a buckled strap round each ankle and a prick spur at the heel.",
    "tags": ["sturdy", "rugged"],
}


def build(g):
    legs(g, "S", "twill", 3411, base=2, rows=(0, 5), crease=False)
    waistband(g, "S", "twill", 3412)
    footwear(g, "boot", top=5, base=2)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.front.vline(1 if side == "right" else 2, 1, 4, "S3")
        outer = pants.right if side == "right" else pants.left
        for face in pants.sides:
            face.hline(0, face.w - 1, 5, "L4")
            face.hline(0, face.w - 1, 9, "L0")
        outer.set(1, 9, "M3"), outer.set(2, 9, "M2")                 # strap buckle
        pants.back.vline(1, 6, 10, "L1")                              # back seam
        spur = leg_blk(g, f"{side}_spur", side, 10.0, (1, 1, 2), "M", 3, "smooth", 3413 + i, dz=2.7)
        spur.back.fill("M4")
