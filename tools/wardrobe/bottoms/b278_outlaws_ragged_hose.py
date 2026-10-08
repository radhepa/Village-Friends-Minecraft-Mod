"""Outlaw's Ragged Hose: hose worn through at one knee and torn off ragged at the other shin, a rag knotted round the calf, battered turnshoes."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_male import leg_blk
from kit_m07 import outer
from paint import solid

META = {
    "name": "Outlaw's Ragged Hose",
    "gender": "male",
    "description": "Greenwood hose worn through at the left knee and torn off ragged above the right ankle, a rag knotted round one calf and battered turnshoes that have outrun the sheriff's men.",
    "tags": ["rugged", "simple", "relaxed"],
}

TORN = (8, 9, 8, 7, 9, 8, 9, 7, 8, 9, 8, 9, 7, 8, 9, 8)   # where the right leg's hose ends, column by column


def build(g):
    legs(g, "P", "weave", 37320, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 37321)
    footwear(g, "turnshoe", top=10, base=1)
    right, left = g.part("right_leg"), g.part("left_leg")
    # The right leg torn off above the ankle: bare shin below a frayed edge.
    for x, end in enumerate(TORN):
        for y in range(end + 1, 10):
            right.strip.set(x, y, None)
        right.strip.set(x, end, "P1")
    rp = g.part("right_pants")
    for x, end in enumerate(TORN):
        if x % 3 == 1:
            rp.strip.set(x, end + 1, "P2")                               # loose threads
    # The left knee worn through.
    for x, y in ((1, 5), (2, 5), (1, 6), (2, 6)):
        left.front.set(x, y, None)
    for x, y in ((0, 5), (3, 6), (2, 7), (1, 4)):
        left.front.set(x, y, "P1")                                       # frayed edges round the hole
    outer(left, "left").vline(1, 0, 9, "P1")
    outer(right, "right").vline(1, 0, 7, "P1")
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.set(1, 10, "L0"), pants.front.set(2, 11, "K1")       # split, battered toes
    # A rag knotted round the left calf, its ends swinging.
    rag = leg_blk(g, "left_calf_rag", "left", 6.8, (5, 2, 5), "S", 2, "weave", 37322)
    for face in rag.sides:
        face.hline(0, face.w - 1, 0, "S3"), face.hline(0, face.w - 1, 1, "S1")
    knot = g.piece("left_rag_knot", leg_bone("left"), (-.5, 0, -.5), (1, 2, 1), pivot=(2.7, 7.6, -.8), motion="sway")
    solid(knot, "S", "weave", 37324, 2, edge=False)
