"""Welsh Archer's One-Shoe Leggings: close wool leggings gartered below the knee, the right foot bare for footing and the left in a rawhide brogue."""
from kit import legs, waistband
from kit_male import leg_blk
from paint import fabric

META = {
    "name": "Welsh Archer's One-Shoe Leggings",
    "gender": "male",
    "description": "Close wool leggings thonged below the knee, the hose rolled at the right ankle with that foot bare for a sure stance, the left foot in a single rawhide brogue.",
    "tags": ["rugged", "simple"],
}


def build(g):
    legs(g, "P", "twill", 38261, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 38262)
    for i, side in enumerate(("right", "left")):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.strip.hline(0, leg.strip.w - 1, 5, "L2")
        pants.strip.hline(0, pants.strip.w - 1, 5, "L3")                    # raised garter thong
        knot = leg_blk(g, f"{side}_garter_knot", side, 4.4, (1, 2, 1), "L", 2, "leather", 38263 + i,
                       dx=-1.4 if side == "right" else 1.4, dz=-2.3)
        knot.front.set(0, 1, "L1")
    # Right foot bare: the hose ends in a rolled edge at the ankle.
    right = g.part("right_leg")
    right.strip.hline(0, right.strip.w - 1, 9, "P3")
    # Left foot: one rawhide brogue thonged round the ankle.
    leg, pants = g.part("left_leg"), g.part("left_pants")
    fabric(leg.strip, "L", "leather", 38265, 2, 0, 9, leg.strip.w, 3)
    for face in pants.sides:
        fabric(face, "L", "leather", 38266, 2, 0, 9, face.w, 3)
        face.hline(0, face.w - 1, 9, "L3")
        face.hline(0, face.w - 1, 11, "K1")
    pants.strip.hline(0, pants.strip.w - 1, 10, "L1")
    pants.front.set(1, 10, "L4"), pants.front.set(2, 9, "L1")
    leg.bottom.fill("K1"), pants.bottom.fill("K0")
    toe = leg_blk(g, "left_brogue_toe", "left", 11.0, (3, 1, 1), "L", 2, "leather", 38267, dz=-2.3)
    toe.top.fill("L3")
