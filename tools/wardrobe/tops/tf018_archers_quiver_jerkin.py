"""Archer's Quiver Jerkin: a jerkin with dagged shoulder wings, one laced bracer, a shooting glove and a back quiver."""
from kit import sleeves
from kit_female import arm_rings, girdle, neck
from paint import fabric, k, line, solid, strip_fabric

META = {
    "name": "Archer's Quiver Jerkin",
    "gender": "female",
    "description": "A twill jerkin with dagged shoulder wings, a laced bracer, a shooting glove and a quiver across the back.",
    "tags": ["martial", "rugged"],
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "twill", 11801, 2)
    fabric(b.top, "P", "twill", 11801, 3), fabric(b.bottom, "P", "twill", 11801, 1)
    neck(b.front, "v", "P", 2, edge="P3")
    b.front.vline(4, 4, 11, "P1")
    for y in (5, 7, 9):
        b.front.set(3, y, "L3"), b.front.set(4, y, "L3")              # toggles
    sleeves(g, "S", "weave", 11802, base=3, rows=(0, 11))
    for box in arm_rings(g, "wing", -2.5, 3, 5, inflate=.12):
        solid(box, "P", "twill", 11803, 2)
        for face in box.sides:
            for x in range(face.w):
                face.set(x, 2, "P1" if x % 2 else "P3")             # dagged edge
    bracer = g.piece("left_bracer", "LEFT_ARM", (-1.5, 4.6, -2.5), (5, 4, 5), inflate=.06)
    solid(bracer, "L", "leather", 11804, 2)
    for face in bracer.sides:
        face.hline(0, face.w - 1, 0, "L3")
        for y in (1, 3):
            face.set(2, y, "S3")
    glove = g.part("right_arm")
    for y in (10, 11):
        glove.strip.hline(0, 15, y, "L2")
    glove.front.set(1, 11, "L3"), glove.front.set(2, 11, "L1")
    j = g.part("jacket")
    line(j.front, 7, 0, 1, 10, "L2"), line(j.back, 0, 0, 6, 10, "L2")
    quiver = g.piece("quiver", "TORSO", (-1.5, 0, -1.5), (3, 8, 3), pivot=(-1.6, 4.4, 4.6), rotation=(0, 0, 28))
    solid(quiver, "L", "leather", 11805, 2)
    for face in quiver.sides:
        face.hline(0, face.w - 1, 0, "L3"), face.hline(0, face.w - 1, 5, "A2")
    for i, (dx, key) in enumerate(((-.9, "S"), (0, "A"), (.9, "S"))):
        arrow = g.piece(f"arrow_{i}", "TORSO", (dx - .5, -3.0 + abs(dx) * .5, -.5), (1, 4, 1), pivot=(-1.6, 4.4, 4.6),
                        rotation=(0, 0, 28))
        solid(arrow, key, "plain", 11806 + i, 3, edge=False)
        arrow.strip.hline(0, arrow.strip.w - 1, 0, k(key, 4))
        arrow.strip.hline(0, arrow.strip.w - 1, 3, "L2")
    girdle(g, "belt", 8.2, role="L", height=1)
