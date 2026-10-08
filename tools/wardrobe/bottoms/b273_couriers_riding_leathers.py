"""Courier's Riding Leathers: leather riding breeches with a darker saddle seat and knee straps, in black heeled riding boots."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk
from kit_m07 import inner, outer, patch

META = {
    "name": "Courier's Riding Leathers",
    "gender": "male",
    "description": "Hard-ridden leather breeches with a darker stitched saddle seat, buckled straps below the knee and black riding boots with a stacked heel for the stirrup.",
    "tags": ["sturdy", "rugged"],
}


def build(g):
    legs(g, "L", "leather", 37100, base=3, rows=(0, 8), crease=False)
    waistband(g, "L", "leather", 37101, base=3)
    footwear(g, "boot", top=8, role="K", base=2, toe="K2", sole="K0")
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        patch(inner(leg, side), 0, 0, 4, 7, "L2", "L4")                 # saddle seat up the inner thigh
        patch(leg.back, 0, 1, 4, 4, "L2")
        leg.front.vline(1 if side == "right" else 2, 0, 7, "L2")         # front seam
        pants.strip.hline(0, pants.strip.w - 1, 5, "K1")                 # strap below the knee
        o = outer(pants, side)
        o.set(1, 5, "M3"), o.set(2, 5, "M4")
        for face in pants.sides:
            face.hline(0, face.w - 1, 8, "L1")                           # boot top
            face.set(0, 9, "K1"), face.set(face.w - 1, 9, "K1")
        inner(pants, side).hline(0, 3, 10, "K3")                         # stirrup-worn instep
        leg_blk(g, f"{side}_boot_heel", side, 11.0, (4, 1, 1), "K", 1, "smooth", 37102, dz=2.4)
