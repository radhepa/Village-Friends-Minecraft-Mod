"""Beekeeper's Bound Trousers: pale trousers corded tight at knee and ankle so no bee can climb in, with soft pale boots."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk

META = {
    "name": "Beekeeper's Bound Trousers",
    "gender": "male",
    "description": "Pale linen trousers corded tight at the knee and ankle so no bee can climb in, a mended knee and soft pale boots.",
    "tags": ["work", "casual"],
    "locked_to": "t47_beekeepers_veiled_smock",
}


def build(g):
    legs(g, "S", "weave", 4711, base=3, rows=(0, 9), crease=False)
    waistband(g, "S", "weave", 4712, base=3)
    footwear(g, "boot", top=10, base=3)
    for i, side in enumerate(SIDES):
        leg = g.part(f"{side}_leg")
        for y in (4, 8):
            for x in range(leg.strip.w):
                leg.strip.set(x, y, "K2" if x % 4 else "K3")               # tight cords
                if x % 2:
                    leg.strip.set(x, y - 1, "S2")                          # cloth gathered above
        leg.front.rect(1, 1, 2, 2, "S2")
        leg.front.set(1, 1, "S4")
        knot = leg_blk(g, f"{side}_knee_knot", side, 4.0, (1, 1, 1), "K", 3, "plain", 4713 + i,
                       dx=-2.25 if side == "right" else 2.25)
        knot.top.fill("K4")
