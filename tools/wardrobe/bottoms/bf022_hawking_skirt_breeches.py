"""Hawking Skirt & Breeches: a knee-length hawking skirt over breeches and side-buckled boots, a lure on the hip."""
from kit import SIDES, legs
from kit_female import shoes, skirt, waist_belt
from paint import solid

META = {
    "name": "Hawking Skirt & Breeches",
    "gender": "female",
    "description": "A knee-length hawking skirt over close breeches and side-buckled boots, with a feathered lure on the hip.",
    "tags": ["rugged", "sturdy", "skirt"],
}


def build(g):
    s = skirt(g, "P", "twill", 12211, top=9.6, length=7, flare=6)
    s.band(1, "line", "L2", from_bottom=True)
    s.hem("P1")
    legs(g, "S", "twill", 12212, rows=(4, 7), crease=False)
    shoes(g, "boot", "L", 2, top=7)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        outer = pants.right if side == "right" else pants.left
        for y in (8, 10):
            outer.set(1, y, "M3"), outer.set(2, y, "L1")             # side buckles
    waist_belt(g, "waist_belt", 9.3, height=1)
    lure = g.piece("waist_lure", "TORSO", (-.5, 0, -1), (1, 3, 2), pivot=(-5.9, 9.8, -.2))
    solid(lure, "L", "leather", 12213, 2)
    lure.right.hline(0, 1, 2, "S4"), lure.right.set(0, 1, "A2")
