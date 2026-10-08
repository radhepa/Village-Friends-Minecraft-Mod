"""Tinker Woman's Patched Breeches: knee breeches mended with patches of every cloth she has, buckled knee
bands, ribbed stockings, buckled shoes and a tinker's hammer in a loop at the hip."""
from kit import SIDES, legs, waistband
from kit_f07 import patch, prop
from kit_female import leg_rings, shoes
from paint import fabric, solid

META = {
    "name": "Tinker Woman's Patched Breeches",
    "gender": "female",
    "description": "Knee breeches mended with stitched patches of every color, buckled knee bands, ribbed "
                   "stockings, buckled shoes and a little tinker's hammer in a hip loop.",
    "tags": ["work", "rugged", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 57121, rows=(0, 6), crease=False)
    body = waistband(g, "P", "twill", 57122)
    body.front.vline(3, 10, 11, "P1"), body.front.set(4, 10, "M3")   # buttoned fly flap
    r, l = g.part("right_pants"), g.part("left_pants")
    patch(r.front, 0, 1, 3, 3, "A2", "A0")
    patch(l.left, 1, 0, 3, 3, "S3", "S1")
    patch(r.back, 1, 0, 3, 2, "L2", "L0")
    patch(l.front, 1, 4, 3, 2, "P3", "P0")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for face in leg.sides:
            face.hline(0, face.w - 1, 6, "P1")                     # the gathered knee
        fabric(leg.strip, "S", "rib", 57123 + (side == "left"), 3, 0, 7, 16, 3)
    for box in leg_rings(g, "knee_band", 6.0, 1, 5, inflate=.05):
        solid(box, "L", "leather", 57125, 2, edge=False)
        box.front.set(2, 0, "M3")
        box.right.set(2, 0, "L1"), box.left.set(2, 0, "L1")
    shoes(g, "shoe", "L", 2, top=10)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.hline(1, 2, 10, "M3")                           # shoe buckles
    # A tinker's hammer in a leather loop at the front of the right hip.
    loop = prop(g, "waist_hammer_loop", "TORSO", (-1, 0, -1), (2, 1, 1), pivot=(-3.0, 9.6, -2.9), role="L",
                texture="leather", base=1, seed=57126, edge=False, motion="flap_front")
    loop.front.set(0, 0, "L2")
    shaft = prop(g, "waist_hammer", "TORSO", (-.5, -.6, -1.1), (1, 4, 1), pivot=(-3.0, 9.6, -2.9), role="L",
                 texture="smooth", base=3, seed=57127, motion="flap_front")
    shaft.front.set(0, 3, "L1")
    head = prop(g, "waist_hammer_head", "TORSO", (-1.5, -1.6, -1.1), (3, 1, 1), pivot=(-3.0, 9.6, -2.9), role="M",
                texture="smooth", base=2, seed=57128, motion="flap_front", edge=False)
    head.front.set(0, 0, "M3"), head.top.fill("M3")
