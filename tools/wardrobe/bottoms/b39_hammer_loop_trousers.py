"""Hammer-Loop Trousers: canvas work trousers with a claw hammer hanging in a thigh loop and a nail pouch at the hip."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_male import blk
from paint import solid

META = {
    "name": "Hammer-Loop Trousers",
    "gender": "male",
    "description": "Canvas work trousers with a claw hammer in a leather thigh loop, a rule pocket and a nail pouch at the hip.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "S", "twill", 3911, base=2, rows=(0, 9), crease=False)
    waistband(g, "S", "twill", 3912)
    footwear(g, "boot", top=10, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        if side == "right":
            pants.right.hline(0, 3, 2, "L2"), pants.right.hline(0, 3, 3, "L1")      # the hammer loop
        else:
            f = pants.left
            f.vline(0, 2, 6, "S1"), f.vline(3, 2, 6, "S1"), f.hline(0, 3, 6, "S1")   # rule pocket
            f.set(1, 1, "S4"), f.set(1, 2, "K2")
    handle = g.piece("hammer_handle", leg_bone("right"), (-.5, 0, -.5), (1, 5, 1), pivot=(-2.5, 1.0, 0))
    solid(handle, "L", "plain", 3913, 3)
    head = g.piece("hammer_head", leg_bone("right"), (-.5, 0, -1.5), (1, 1, 3), pivot=(-2.5, .1, 0))
    solid(head, "M", "smooth", 3914, 2, edge=False)
    head.left.set(0, 0, "M4"), head.right.set(2, 0, "M4")
    nails = blk(g, "waist_nail_pouch", (2.6, 10.2, -2.6), (3, 3, 1), "L", 2, "leather", 3915)
    nails.front.hline(0, 2, 0, "L3"), nails.front.set(1, 0, "M3"), nails.front.set(0, 0, "M2")
