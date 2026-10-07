"""Cord-Tied Breeches: loose linen breeches gathered and tied below the knee, bare shins and soft toggled turnshoes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk

META = {
    "name": "Cord-Tied Breeches",
    "gender": "male",
    "description": "Loose linen breeches gathered and cord-tied below the knee over bare shins, with soft turnshoes fastened by a toggle.",
    "tags": ["work", "simple", "relaxed"],
}


def build(g):
    legs(g, "S", "weave", 3211, base=3, rows=(0, 6), crease=False)
    waistband(g, "S", "weave", 3212, base=3)
    footwear(g, "turnshoe", top=10, base=2)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for x in range(leg.strip.w):
            if x % 2:
                leg.strip.set(x, 5, "S2")                              # gathers above the tie
        leg.strip.hline(0, leg.strip.w - 1, 6, "L2")
        outer = leg.right if side == "right" else leg.left
        outer.set(1, 6, "L3"), outer.set(2, 6, "L1")
        pants.front.set(1 if side == "right" else 2, 10, "L4")       # toggle on the instep
        tail = leg_blk(g, f"{side}_cord_tail", side, 6.2, (1, 3, 1), "L", 2, "plain", 3213 + i,
                       dx=-2.3 if side == "right" else 2.3, rotation=(0, 0, 8 if side == "right" else -8))
        tail.strip.hline(0, tail.strip.w - 1, 2, "L3")
