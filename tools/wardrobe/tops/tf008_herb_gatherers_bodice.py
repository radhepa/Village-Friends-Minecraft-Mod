"""Herb-Gatherer's Bodice: a leaf-embroidered bodice with a satchel slung to the hip, sprigs poking out."""
from kit_female import bodice, chemise, lacing, motif
from paint import line, solid

META = {
    "name": "Herb-Gatherer's Bodice",
    "gender": "female",
    "description": "A leaf-embroidered bodice over a chemise, a gathering satchel at the hip with fresh sprigs poking out.",
    "tags": ["casual"],
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 10801, neckline="scoop", sleeve_rows=(0, 10))
    for arm in arms:
        arm.strip.hline(0, 15, 9, "P2"), arm.strip.hline(0, 15, 10, "S2")   # tied cuffs
    b = bodice(g, "P", "weave", 10802, rows=(2, 9), neckline="square", edge="P3")
    lacing(b.front, 3, 3, 8, "spiral", lace="S4", under="P0", eyelet=None)
    for x, mirror in ((0, False), (6, True)):
        motif(b.front, x, 4, "leaf", a="A2", c="P3")
        motif(b.front, x, 7, "leaf", a="A3", c="P3")
    motif(b.back, 2, 3, "sprig", a="A2", c="P3")
    motif(b.back, 4, 6, "sprig", a="A2", c="P3")
    j = g.part("jacket")
    line(j.front, 0, 0, 7, 8, "L2")                        # satchel strap
    line(j.back, 7, 0, 0, 8, "L2")
    j.top.vline(1, 0, 3, "L2")
    satchel = g.piece("satchel", "TORSO", (-1.5, 0, -1), (3, 3, 2), pivot=(5.2, 6.4, .8))
    solid(satchel, "L", "leather", 10803, 2)
    satchel.left.hline(0, 1, 0, "L3"), satchel.left.set(1, 1, "M3")
    satchel.front.hline(0, 2, 0, "L3")
    for i, (dx, key) in enumerate(((-.5, "P3"), (.5, "A3"))):
        sprig = g.piece(f"sprig_{i}", "TORSO", (-.5, -2, -.5), (1, 2, 1), pivot=(5.0 + dx, 6.6, .6 + dx), rotation=(0, 0, -10 + 20 * i))
        solid(sprig, key[0], "plain", 10804 + i, int(key[1]), edge=False)
        sprig.top.fill("A3" if i else "P4")
