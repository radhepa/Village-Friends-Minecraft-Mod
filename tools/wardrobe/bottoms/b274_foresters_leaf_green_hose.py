"""Forester's Leaf-Green Hose: close knitted hose gartered below the knee with oak-leaf tabs, over ankle boots with a leaf-dagged cuff."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_m07 import leg_shell, outer
from paint import solid

META = {
    "name": "Forester's Leaf-Green Hose",
    "gender": "male",
    "description": "Close knitted woodland hose gartered below the knee with little oak-leaf tabs, over soft ankle boots whose turned-down cuffs are dagged like leaves.",
    "tags": ["casual", "slim", "rugged"],
}

LEAF = ["P3", "P2", "P1"]


def build(g):
    legs(g, "P", "knit", 37140, rows=(0, 8), crease=False)
    waistband(g, "P", "knit", 37141)
    footwear(g, "boot", top=8, base=2)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        o = outer(leg, side)
        o.vline(1, 0, 7, "P1")                                           # the outer seam
        leg.strip.hline(0, leg.strip.w - 1, 6, "A2")                     # the garter under the 3D band
    for i, (side, garter) in enumerate(zip(SIDES, leg_shell(g, "garter", 5.9, 1, "A", 2, "plain", 37142, inflate=.02))):
        for face in garter.sides:
            for x in range(face.w):
                face.set(x, 0, "A3" if x % 2 else "A2")
        # An oak-leaf tab hanging from the garter on the outer side.
        x = -2.6 if side == "right" else 2.6
        leaf = g.piece(f"{side}_garter_leaf", leg_bone(side), (-.5, 0, -1), (1, 3, 2),
                       pivot=(x, 6.9, -.2))
        solid(leaf, "P", "plain", 37144 + i, 3, edge=False)
        for face in leaf.sides:
            for y in range(3):
                for x in range(face.w):
                    face.set(x, y, LEAF[min(2, y + x)])
    # Leaf-dagged boot cuffs: a turned-down band whose lower edge is cut in points.
    for cuff in leg_shell(g, "boot_cuff", 7.6, 2, "L", 3, "leather", 37146, inflate=.03):
        for face in cuff.sides:
            face.hline(0, face.w - 1, 0, "L4")
            for x in range(face.w):
                face.set(x, 1, "L3" if x % 2 == 0 else "L1")
