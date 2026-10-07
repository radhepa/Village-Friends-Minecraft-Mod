"""Falconer's Gauntlet Doublet: a fitted doublet, a deep falconry gauntlet on the left arm with a hooded falcon perched on it."""
from kit import sleeves
from kit_female import buttons, girdle, neck
from paint import fabric, solid, strip_fabric

META = {
    "name": "Falconer's Gauntlet Doublet",
    "gender": "female",
    "description": "A buttoned doublet, a fringed falconry gauntlet on the left arm and a hooded falcon riding her fist.",
    "tags": ["rugged", "tailored"],
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "twill", 12201, 2)
    fabric(b.top, "P", "twill", 12201, 3), fabric(b.bottom, "P", "twill", 12201, 1)
    neck(b.front, "round", "P", 2, edge="S3")
    buttons(b.front, 4, 1, 11, "M3", step=2, placket="P1")
    for face in (b.front, b.back):
        face.vline(1, 2, 11, "P1"), face.vline(6, 2, 11, "P1")
    sleeves(g, "P", "twill", 12202, rows=(0, 11))
    g.part("right_arm").strip.hline(0, 15, 10, "S3")
    gauntlet = g.piece("gauntlet", "LEFT_ARM", (-1.6, 4.4, -2.6), (5, 6, 5), inflate=.1)
    solid(gauntlet, "L", "leather", 12203, 3)
    for face in gauntlet.sides:
        for x in range(face.w):
            face.set(x, 0, "L4" if x % 2 else "L2")                  # fringed cuff
        face.hline(0, face.w - 1, 2, "L2")
    falcon = g.piece("falcon", "LEFT_ARM", (-1, -3, -1), (2, 3, 2), pivot=(1.0, 8.6, -3.6))
    solid(falcon, "S", "plain", 12204, 3)
    for face in falcon.sides:
        face.set(0, 1, "L2"), face.set(1, 2, "L2")                  # barred breast
    falcon.front.set(0, 0, "S4"), falcon.front.set(1, 0, "S4")
    hood = g.piece("falcon_hood", "LEFT_ARM", (-1, -1, -1), (2, 1, 2), pivot=(1.0, 5.6, -3.6), inflate=.05)
    solid(hood, "L", "leather", 12205, 2, edge=False)
    hood.top.set(0, 0, "A2"), hood.top.set(1, 1, "A2")
    tail = g.piece("falcon_tail", "LEFT_ARM", (-.5, 0, -.5), (1, 2, 1), pivot=(1.0, 8.6, -2.9), rotation=(20, 0, 0))
    solid(tail, "L", "plain", 12206, 2)
    girdle(g, "belt", 7.8, role="L", height=1)
    lure = g.piece("lure_pouch", "TORSO", (-1, 0, -.5), (2, 2, 1), pivot=(-2.4, 6.6, -2.95))
    solid(lure, "L", "leather", 12207, 2)
    lure.front.set(0, 0, "S4"), lure.front.set(1, 1, "A2")
