"""Hobelar's Riding Boots: saddle-seated breeches in strapped knee boots with rowel spurs."""
from kit import SIDES, footwear, leg_ring, legs, waistband
from kit_m04 import sides_of, spur

META = {
    "name": "Hobelar's Riding Boots",
    "gender": "male",
    "description": "Riding breeches with leather saddle patches on the inner thighs, in soft knee boots cinched by two "
                   "buckled straps, with rowel spurs at the heels.",
    "tags": ["martial", "sturdy", "rugged"],
}

S = 34140


def build(g):
    legs(g, "P", "twill", S, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", S + 2)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        inner = getattr(leg, sides_of(side)[1])
        inner.rect(0, 0, 4, 5, "L2")                                       # saddle seat patch
        inner.hline(0, 3, 0, "L3"), inner.hline(0, 3, 4, "L1")
    footwear(g, "boot", top=5, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for y in (7, 10):
            pants.strip.hline(0, pants.strip.w - 1, y, "L1")               # cinch straps
            getattr(pants, sides_of(side)[0]).set(1, y, "M3")
        pants.front.vline(1 if side == "right" else 2, 5, 6, "L3"), pants.front.vline(1 if side == "right" else 2, 8, 9, "L3")
    for ring in leg_ring(g, "boot_top", 4.6, "L", base=3, size=(5, 1, 5), texture="leather", inflate=.18):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L4")
            face.set(2, 0, "L1")
    for i, side in enumerate(SIDES):
        spur(g, side, y=9.9, seed=S + 4 + 2 * i)
