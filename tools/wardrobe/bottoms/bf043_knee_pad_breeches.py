"""Knee-Pad Breeches: stone-dusted breeches with strapped leather knee pads for kneeling at the wall, and laced boots."""
from kit import SIDES, leg_bone, legs, waistband
from kit_female import shoes
from paint import rnd, solid

META = {
    "name": "Knee-Pad Breeches",
    "gender": "female",
    "description": "Stone-dusted work breeches with strapped leather knee pads for kneeling at the wall, and laced ankle boots.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "P", "weave", 14311, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 14312)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for y in range(5, 10):
            for x in range(16):
                if rnd(x, y, 14313) < .08:
                    leg.strip.set(x, y, "S4")
        pad = g.piece(f"{side}_knee_pad", leg_bone(side), (-2, 0, -1), (4, 3, 1), pivot=(0, 3.4, -2.3))
        solid(pad, "L", "leather", 14314, 2)
        pad.front.hline(0, 3, 0, "L3"), pad.front.set(1, 1, "L1"), pad.front.set(2, 1, "L1")
        strap = g.piece(f"{side}_knee_strap", leg_bone(side), (-2, 0, -2), (4, 1, 4), pivot=(0, 4.4, 0), inflate=.28)
        solid(strap, "L", "leather", 14315, 1, edge=False)
    shoes(g, "ankle", "L", 2)
