"""Carrier's Road Gaiters: twill trousers under tall canvas gaiters hooked up the outside, a knee tongue, dusty from the road."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk
from kit_m07 import dust, leg_shell, outer

META = {
    "name": "Carrier's Road Gaiters",
    "gender": "male",
    "description": "Twill trousers under tall canvas gaiters hooked and laced up the outside, a stiff tongue over each knee and road dust thick round the ankles.",
    "tags": ["sturdy", "rugged"],
}


def build(g):
    legs(g, "P", "twill", 37060, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", 37061)
    footwear(g, "shoe", top=10, base=2)
    for side, gaiter in zip(SIDES, leg_shell(g, "gaiter", 4.6, 6, "S", 2, "weave", 37062)):
        for face in gaiter.sides:
            face.hline(0, face.w - 1, 0, "S3")
            face.hline(0, face.w - 1, 5, "S1")
            dust(face, "S1", 37064, 3, 4, .12, .4)
        o = outer(gaiter, side)
        o.vline(2, 1, 4, "S0")
        for y in (1, 3):
            o.set(1, y, "M3"), o.set(3, y, "M3")
        for y in (2, 4):
            o.set(1, y, "L2"), o.set(3, y, "L2")
        tongue = leg_blk(g, f"{side}_knee_tongue", side, 3.3, (3, 2, 1), "S", 3, "weave", 37066 + (side == "left"),
                         dz=-2.6)
        tongue.front.hline(0, 2, 0, "S4"), tongue.front.set(1, 1, "S1")
        pants = g.part(f"{side}_pants")
        pants.strip.hline(0, pants.strip.w - 1, 11, "K1")
        pants.front.hline(0, 3, 11, "L1")                              # strap under the instep
