"""Sailor Lass's Wide Slops: loose sailcloth slops cut wide as two short skirts, ending open just below
the knee with a patch and a tar stain, a drawstring waist, and bare shins and feet for the deck."""
from kit import SIDES, leg_bone
from paint import fabric, solid, strip_fabric

META = {
    "name": "Sailor Lass's Wide Slops",
    "gender": "female",
    "description": "Loose sailcloth slops cut wide and open below the knee, patched and tar-stained, with bare shins and feet for the deck.",
    "tags": ["sea", "relaxed", "rugged"],
}

SEED = 53165


def build(g):
    body = g.part("body")
    strip_fabric(body, "P", "weave", SEED, 3, 9, 11)
    for f in body.sides:
        f.hline(0, f.w - 1, 9, "P4")
        for x in range(0, f.w, 2):
            f.set(x, 10, "P2")                                       # gathered on the drawstring
    fabric(body.bottom, "P", "plain", SEED, 2)
    body.front.set(3, 9, "S4"), body.front.set(4, 9, "S4"), body.front.set(3, 10, "S3")   # the tie
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "P", "weave", SEED + 1, 2, 0, 7)
        fabric(leg.top, "P", "plain", SEED, 2)
        dz = -2.5 if side == "right" else -2.38                      # stagger the faces where the two legs meet
        slop = g.piece(f"{side}_slop", leg_bone(side), (-2.5, -.3, dz), (5, 8, 5), inflate=.2)
        solid(slop, "P", "weave", SEED + 2 + (side == "left"), 3)
        for f in slop.sides:
            f.hline(0, f.w - 1, 0, "P4")
            for x in range(1, f.w, 2):
                f.vline(x, 1, 2, "P2")                               # gathers under the waist
            f.vline(2, 3, 6, "P2")                                   # a long soft fold
            f.hline(0, f.w - 1, 7, "P1")                             # the turned hem
        slop.bottom.fill("P0")
        outer = slop.right if side == "right" else slop.left
        outer.vline(2, 0, 7, "P1")                                   # the outseam
        if side == "right":
            fabric(slop.front, "S", "weave", SEED + 4, 3, 1, 3, 3, 3)    # a sailcloth patch
            slop.front.hline(1, 3, 3, "S4"), slop.front.set(1, 5, "S2"), slop.front.set(3, 5, "S2")
        else:
            slop.front.set(2, 5, "K1"), slop.front.set(3, 5, "K2"), slop.front.set(2, 6, "K2")   # tar
            slop.back.set(1, 4, "K2")
