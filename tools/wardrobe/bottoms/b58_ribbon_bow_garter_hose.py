"""Ribbon-Bow Garter Hose: fitted hose with ribbon garters tied in big bows below the knee, over soft pointed shoes."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_male import leg_blk
from paint import solid

META = {
    "name": "Ribbon-Bow Garter Hose",
    "gender": "male",
    "description": "Fitted hose gartered below the knee with ribbons tied in big bows whose tails flutter, over soft pointed shoes.",
    "tags": ["whimsical", "slim"],
    "rejects": ["armor"],
}


def build(g):
    legs(g, "P", "velvet", 5811, rows=(0, 9), crease=False)
    waistband(g, "P", "velvet", 5812)
    footwear(g, "turnshoe", top=10, base=2)
    for i, side in enumerate(SIDES):
        pants = g.part(f"{side}_pants")
        pants.strip.hline(0, pants.strip.w - 1, 5, "A2")
        pants.front.set(1 if side == "right" else 2, 11, "L3")
        dx = -2.2 if side == "right" else 2.2
        bow = leg_blk(g, f"{side}_garter_bow", side, 4.5, (1, 2, 3), "A", 3, "plain", 5813 + i, dx=dx, dz=-.4)
        outer = bow.right if side == "right" else bow.left
        outer.set(1, 0, "A2"), outer.set(1, 1, "A2")                       # the knot between the loops
        tail = g.piece(f"{side}_bow_tail", leg_bone(side), (-.5, 0, -.5), (1, 3, 1), pivot=(dx, 5.6, -.6),
                       rotation=(0, 0, -10 if side == "right" else 10), motion="sway")
        solid(tail, "A", "plain", 5815 + i, 2)
