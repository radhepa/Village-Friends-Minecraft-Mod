"""Wool Trousers & Wooden Clogs: plain wool trousers with a turned hem over carved wooden clogs."""
from kit import SIDES, leg_bone, legs, waistband
from paint import solid, strip_fabric

META = {
    "name": "Wool Trousers & Clogs",
    "description": "Plain wool trousers, hems turned up, over carved wooden clogs.",
    "tags": ["work", "simple", "sturdy"],
}


def build(g):
    legs(g, "P", "weave", 1801, rows=(0, 9))
    waistband(g, "P", "weave", 1802)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 8, "P3"), face.hline(0, face.w - 1, 9, "P1")
        strip_fabric(leg, "L", "smooth", 1803, 3, 10, 11)
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "L3"), face.hline(0, face.w - 1, 11, "L2")
        leg.bottom.fill("L1"), pants.bottom.fill("L1")
        toe = g.piece(f"{side}_clog_toe", leg_bone(side), (-2, 0, -1.5), (4, 2, 2), pivot=(0, 10.1, -2.4), inflate=.05)
        solid(toe, "L", "smooth", 1804, 3, edge=False)
        toe.top.set(1, 1, "L4"), toe.top.set(2, 1, "L4")
