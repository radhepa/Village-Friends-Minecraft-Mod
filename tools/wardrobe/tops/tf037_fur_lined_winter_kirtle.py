"""Fur-Lined Winter Kirtle: a thick wool kirtle lined in fur at collar, front and cuffs, mittens dangling on a cord."""
from kit import body, sleeves
from kit_female import arm_rings, fur, fur_box, sub
from paint import solid

META = {
    "name": "Fur-Lined Winter Kirtle",
    "gender": "female",
    "description": "A thick winter kirtle edged with fur at the collar, down the toggled front and at the cuffs, mittens on a cord.",
    "tags": ["rugged", "casual"],
}


def build(g):
    b = body(g, "P", "twill", 13701)
    fur(sub(b.front, 3, 0, 2, 12), "S", 13702, 3)
    for y in (3, 6, 9):
        b.front.set(2, y, "L3"), b.front.set(5, y, "L3")             # horn toggles
    for face in (b.front, b.back):
        face.vline(1, 2, 11, "P1"), face.vline(6, 2, 11, "P1")
    sleeves(g, "P", "twill", 13703, rows=(0, 11))
    collar = g.piece("fur_collar", "TORSO", (-4.6, -1.6, -2.7), (9, 3, 5), inflate=.08)
    fur_box(collar, "S", 13704, 3)
    for box in arm_rings(g, "fur_cuff", 7.6, 2, 5, inflate=.1):
        fur_box(box, "S", 13705, 3)
    for side, x in (("right", -6.0), ("left", 6.0)):
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        mitt = g.piece(f"{side}_mitten", bone, (-1, 0, -.5), (2, 3, 1), pivot=(-1.0 if side == "right" else 1.0, 9.8, 2.4),
                       motion="sway")
        solid(mitt, "A", "knit", 13706, 2)
        mitt.back.hline(0, 1, 0, "S4")
