"""Watchwoman's Night Boots: dark wool breeches and tall boots buttoned up the outer side, folded over at the top,
on thick felted soles that keep her rounds quiet."""
from kit import SIDES, leg_bone, legs, waistband
from kit_female import leg_ring_fold, shoes, waist_belt
from paint import solid

META = {
    "name": "Watchwoman's Night Boots",
    "gender": "female",
    "description": "Dark wool breeches and tall boots buttoned up the outer side and folded at the top, on thick "
                   "felted soles that keep her rounds quiet.",
    "tags": ["sturdy", "rugged"],
}


def build(g):
    legs(g, "P", "twill", 54301, base=1, rows=(0, 3), crease=False)
    body = waistband(g, "P", "twill", 54302, base=1)
    body.front.vline(3, 9, 11, "P0")
    shoes(g, "boot", "L", 1, top=3, sole="S1")
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        outer = pants.right if side == "right" else pants.left
        outer.vline(1, 4, 10, "L0")
        for y in range(4, 11, 2):
            outer.set(2, y, "M3")                                     # buttons up the outer side
        pants.front.vline(1 if side == "right" else 2, 4, 9, "L2")
    for box in leg_ring_fold(g, "boot_fold", 2.4, "L", 1):
        box.front.set(2, 1, "M3")
    for side in SIDES:
        sole = g.piece(f"{side}_felt_sole", leg_bone(side), (-2, 0, -2), (4, 1, 4), pivot=(0, 11.5, 0), inflate=.18)
        solid(sole, "S", "plain", 54303, 1, edge=False)
        for face in sole.sides:
            for x in range(0, face.w, 2):
                face.set(x, 0, "S2")
        sole.bottom.fill("S0")
    waist_belt(g, "waist_belt", 9.4, height=1)
