"""Longbowman's Bracer Jerkin: a sleeveless jerkin over a shirt, a broad bracer on the bow arm and arrows pushed through the belt."""
from kit import belt, body, neckline, sleeves
from kit_male import arm_blk, blk
from paint import fabric

META = {
    "name": "Longbowman's Bracer Jerkin",
    "gender": "male",
    "description": "A yeoman archer's sleeveless jerkin over a linen shirt, a broad horn-and-leather bracer and arrows thrust through the belt.",
    "tags": ["martial", "rugged"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 7501, base=3)
    neckline(b.front, "laced", "S", base=3)
    sleeves(g, "S", "weave", 7502, base=3, rows=(0, 10), cuff="S2")
    jacket = body(g, "P", "twill", 7503, layer="jacket")
    jacket.front.hline(2, 5, 0, None), jacket.front.hline(3, 4, 1, None), jacket.front.hline(3, 4, 2, None)
    jacket.front.vline(3, 3, 11, "P1"), jacket.front.vline(4, 3, 11, "P3")
    for face in (jacket.right, jacket.left):
        face.vline(1, 0, 11, "P1")
    bracer = arm_blk(g, "bow_bracer", "left", 5.0, (5, 4, 5), "L", 2, "smooth", 7504, inflate=.1)
    for face in bracer.sides:
        face.hline(0, face.w - 1, 0, "L4"), face.hline(0, face.w - 1, 3, "L1")
    bracer.front.vline(2, 1, 2, "S4")                                    # horn plate
    glove = g.part("right_sleeve")
    fabric(glove.front, "L", "leather", 7505, 2, 0, 10, 4, 2)            # shooting tab
    belt(g, "belt", 9.4)
    for i, (x, rz) in enumerate(((2.2, -8), (2.9, 4), (3.6, 14))):
        arrow = blk(g, f"belt_arrow_{i}", (x, 6.6, -2.8), (1, 5, 1), "L", 3, "plain", 7506 + i, rotation=(0, 0, rz))
        arrow.strip.hline(0, arrow.strip.w - 1, 0, "S4"), arrow.strip.hline(0, arrow.strip.w - 1, 1, "A2")
