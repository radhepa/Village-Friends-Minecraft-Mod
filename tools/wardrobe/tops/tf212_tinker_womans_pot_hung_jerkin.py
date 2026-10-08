"""Tinker Woman's Pot-Hung Jerkin: a buttoned twill jerkin over a rolled-sleeve shirt, a tinker's carrying
frame on her back hung with a copper kettle and a skillet, and a string of tin cups at the hip."""
from kit import flaps, roll
from kit_f07 import front_hung, prop, strap
from kit_female import chemise, girdle, neck
from paint import fabric

META = {
    "name": "Tinker Woman's Pot-Hung Jerkin",
    "gender": "female",
    "description": "A buttoned twill jerkin over a rolled-sleeve shirt, a carrying frame on her back hung with a "
                   "copper kettle and a skillet, and tin cups clinking at her hip.",
    "tags": ["work", "rugged"],
    "covers_waist": True,
}


def build(g):
    chemise(g, "S", 3, "weave", 57101, neckline="round", sleeve_rows=(0, 4))
    roll(g, "S", 1.8, base=3)
    j = g.part("jacket")
    for face in j.sides:
        fabric(face, "P", "twill", 57102 + face.x0, 2)
    fabric(j.top, "P", "twill", 57103, 3)
    neck(j.front, "v", "P", 2, edge="P3")
    for y in range(4, 12):
        j.front.set(3, y, "P1"), j.front.set(4, y, "P3")             # the front opening
    for y in (5, 7, 9):
        j.front.set(4, y, "M3")                                      # pewter buttons
    for face in (j.right, j.left):
        face.vline(2, 0, 11, "P1")
    # The frame's shoulder straps, and a leather patch where the left strap rubs.
    for x in (1, 6):
        j.front.vline(x, 0, 6, "L2"), j.back.vline(x, 0, 10, "L1")
        j.top.vline(x, 0, 3, "L2")
    strap(j.front, 1, 7, 0, 8, "L1"), strap(j.front, 6, 7, 7, 8, "L1")
    fabric(j.back, "L", "leather", 57104, 2, 5, 2, 3, 2)
    girdle(g, "belt", 8.0, role="L", height=1)
    flaps(g, "jerkin_hem", 2, "P", "twill", 57105, width=9)

    # The carrying frame: two staves and a crossbar standing off her back.
    for i, x in enumerate((-3.4, 2.4)):
        stave = prop(g, f"frame_stave_{i}", "TORSO", (0, 0, 0), (1, 10, 1), pivot=(x, .4, 2.4), role="L",
                     texture="smooth", seed=57106 + i, base=2)
        stave.top.fill("L3")
    bar = prop(g, "frame_bar", "TORSO", (0, 0, 0), (8, 1, 1), pivot=(-4.0, 3.4, 3.4), role="L", texture="smooth",
               seed=57108, base=3, edge=False)
    bar.back.set(0, 0, "L1"), bar.back.set(7, 0, "L1")
    # A copper kettle on its bail, lid knob and spout.
    kettle = prop(g, "kettle", "TORSO", (0, 0, 0), (4, 3, 3), pivot=(-3.6, 5.6, 3.7), role="M", texture="smooth",
                  seed=57109, base=2)
    for face in kettle.sides:
        face.hline(0, face.w - 1, 0, "M3"), face.hline(0, face.w - 1, 2, "M1")
    kettle.back.set(1, 1, "M4"), kettle.top.fill("M3"), kettle.top.set(1, 1, "M1"), kettle.top.set(2, 1, "M1")
    knob = prop(g, "kettle_knob", "TORSO", (0, 0, 0), (1, 1, 1), pivot=(-2.1, 4.6, 4.7), role="M", base=1,
                seed=57110, edge=False)
    knob.top.fill("M3")
    spout = prop(g, "kettle_spout", "TORSO", (0, 0, 0), (1, 1, 2), pivot=(-4.0, 6.2, 6.6), role="M", base=2,
                 seed=57111, edge=False, rotation=(-30, 0, 0))
    spout.back.fill("M0")
    # A skillet hung by its handle from the crossbar.
    pan = prop(g, "skillet", "TORSO", (0, 0, 0), (3, 3, 1), pivot=(.9, 5.4, 3.9), role="M", texture="smooth",
               seed=57112, base=1)
    pan.back.fill("M1")
    pan.back.set(1, 1, "M3"), pan.back.set(1, 0, "M2"), pan.back.set(0, 1, "M2")     # the pan's round iron base
    handle = prop(g, "skillet_handle", "TORSO", (0, 0, 0), (1, 3, 1), pivot=(1.9, 2.6, 4.1), role="L", base=2,
                  seed=57113, edge=False)
    handle.back.set(0, 2, "M2")
    # Two tin cups on a cord at the right hip, ringing as she walks.
    front_hung(g, "cup_cord", -3.0, (-.5, 0, -1), (1, 2, 1), role="L", base=3, seed=57114, top=8.6)
    for i, dx in enumerate((-1.6, .4)):
        cup = front_hung(g, f"tin_cup_{i}", -3.0, (dx - .2, 2, -1.6), (1, 2, 1), role="M", base=3, seed=57115 + i,
                         top=8.6)
        cup.front.set(0, 0, "M4"), cup.top.fill("M0")
