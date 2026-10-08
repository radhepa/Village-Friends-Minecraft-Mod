"""Herbalist Monk's Knee-Tied Habit: the habit's skirts gathered up and knotted at the knee for kneeling in the beds, earth-stained hose and mud-clogged garden clogs."""
from kit import SIDES, footwear, waistband
from kit_male import skirt_panels
from kit_m05 import grime, hose, knee_patch
from paint import solid

META = {
    "name": "Herbalist Monk's Knee-Tied Habit",
    "gender": "male",
    "description": "The habit's skirts gathered up and knotted at the knee so he can kneel in the herb beds, undyed hose stained with earth at both knees, and wooden garden clogs clotted with soil.",
    "tags": ["holy", "work", "robe"],
    "locked_to": "t235_herbalist_monks_garden_habit",
}


def build(g):
    hose(g, "S", 2, "weave", 35580, end=9)
    waistband(g, "P", "weave", 35581, base=1)
    footwear(g, "clog", top=9, role="L", base=3, sole="K1")
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        knee_patch(leg.front, 0, 5, "L2", "L3", w=4, h=2)                  # earth ground into the knees
        leg.front.set(1 if side == "right" else 2, 7, "L2")
        grime(pants.strip, "L1", 9, 10, ox=3 if side == "left" else 0)    # soil on the clogs
    front, back, sides = skirt_panels(g, "habit", 7, "P", "weave", 35582, base=1, top=10.6, side_len=6)
    for face in (front, back):
        for x in (2, 4, 6):
            face.vline(x, 1, 5, "P0")
        face.hline(0, 8, 5, "P2"), face.hline(0, 8, 6, "P0")                # the gathered, tied-up edge
    for box in sides:
        for face in box.sides:
            face.hline(0, face.w - 1, box.h - 1, "P0")
    # The skirt corners knotted together at each knee.
    for name, x in (("habit_knot_right", -3.4), ("habit_knot_left", 3.4)):
        knot = g.piece(name, "TORSO", (-1, 0, -1), (2, 2, 2), pivot=(x, 16.6, -2.7), motion="flap_front")
        solid(knot, "P", "weave", 35583, 2, edge=False)
        knot.front.set(0, 0, "P3"), knot.front.set(1, 1, "P0")
        tail = g.piece(name + "_end", "TORSO", (-.5, 2, -.5), (1, 2, 1), pivot=(x, 16.6, -2.7), motion="flap_front")
        solid(tail, "P", "weave", 35584, 1)
