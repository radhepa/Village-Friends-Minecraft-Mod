"""Barber-Surgeon's Strapped Trousers: twill trousers buckled at shin and ankle, with a rolled case of blades strapped to the right thigh."""
from kit import SIDES, footwear, legs, waistband
from kit_m05 import leg_prop

META = {
    "name": "Barber-Surgeon's Strapped Trousers",
    "gender": "male",
    "description": "Close twill trousers buckled tight below the knee and at the ankle, a rolled leather case of lancets and razors strapped to the right thigh, over low shoes.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 35060, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 35061)
    footwear(g, "shoe", top=10, base=2)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        outer = leg.right if side == "right" else leg.left
        for y in (5, 9):
            leg.strip.hline(0, leg.strip.w - 1, y, "L2")
            outer.set(1, y, "M3")
        leg.strip.hline(0, leg.strip.w - 1, 4, "P1")
    right = g.part("right_leg")
    for y in (1, 3):
        right.strip.hline(0, right.strip.w - 1, y, "L1")                 # thigh straps
    roll = leg_prop(g, "lancet_roll", "right", (-2.5, .6, 0), (1, 4, 3), "L", 2, "leather", 35062)
    for y in (1, 3):
        roll.strip.hline(0, roll.strip.w - 1, y, "L1")
    roll.right.set(1, 1, "M3"), roll.right.set(1, 3, "M3")
    roll.top.fill("L3")
    for i, z in enumerate((-1.0, 0.0, 1.0)):                              # blade handles peeping out
        h = g.piece(f"lancet_{i}", "RIGHT_LEG", (-.5, -1, -.5), (1, 1, 1), pivot=(-2.5, .6, z))
        for face in h.faces:
            face.fill("M3" if i % 2 == 0 else "S4")
        h.top.fill("M4" if i % 2 == 0 else "S4")
