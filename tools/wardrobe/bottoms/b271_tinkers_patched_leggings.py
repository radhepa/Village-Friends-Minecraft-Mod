"""Tinker's Patched Leggings: close leggings mended with a patch of every cloth, one leg rolled, over cobbled turnshoes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk
from kit_m07 import outer, patch

META = {
    "name": "Tinker's Patched Leggings",
    "gender": "male",
    "description": "Close leggings mended with a patch of every cloth he has ever carried, a darned shin, one leg rolled to the calf and turnshoes cobbled at the toe.",
    "tags": ["rugged", "casual"],
}


def build(g):
    legs(g, "S", "twill", 37020, rows=(0, 9), crease=False)
    waistband(g, "S", "twill", 37021)
    footwear(g, "turnshoe", top=10, base=1)
    right, left = g.part("right_leg"), g.part("left_leg")
    patch(right.front, 0, 4, 4, 3, "A2", "A4")                         # knee patch
    patch(right.back, 1, 0, 3, 3, "P2")                          # seat patch
    for y in range(6, 10):                                             # darned shin
        o = outer(right, "right")
        o.set(1 + y % 2, y, "S0"), o.set(2 - y % 2, y, "S4")
    patch(left.front, 1, 1, 3, 3, "P2")                          # thigh patch
    patch(outer(left, "left"), 0, 6, 4, 3, "L3", "L1")                 # shin patch
    # A leather knee pad cobbled on over the left knee.
    pad = leg_blk(g, "left_knee_pad", "left", 3.6, (3, 3, 1), "L", 2, "leather", 37022, dz=-2.35)
    pad.front.set(0, 0, "K2"), pad.front.set(2, 0, "K2"), pad.front.set(0, 2, "K2"), pad.front.set(2, 2, "K2")
    # The right leg is rolled up to the calf, showing a stocking-dark shin below.
    roll = leg_blk(g, "right_leg_roll", "right", 7.4, (5, 2, 5), "S", 3, "twill", 37023)
    for face in roll.sides:
        face.hline(0, face.w - 1, 0, "S4"), face.hline(0, face.w - 1, 1, "S1")
    for y in range(9, 10):
        right.strip.hline(0, right.strip.w - 1, y, "K2")
    right.strip.hline(0, right.strip.w - 1, 8, "K3")
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.hline(1, 2, 10, "L3" if side == "right" else "S2")   # cobbled toe caps
