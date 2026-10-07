"""Corded Lady's Mantle: a long fur-collared mantle held by tasseled cords crossed over the breast, over a velvet kirtle."""
from kit import body, sleeves
from kit_female import cloak, fur_box, mantle, neck
from paint import fabric, line, solid

META = {
    "name": "Corded Lady's Mantle",
    "gender": "female",
    "description": "A long mantle with a fur collar, held by tasseled cords crossed over the breast, over a velvet kirtle.",
    "tags": ["fancy", "robe"],
}


def build(g):
    b = body(g, "P", "velvet", 16001)
    neck(b.front, "round", "P", 2)
    sleeves(g, "P", "velvet", 16002, rows=(0, 11))
    j = g.part("jacket")
    for face in (j.front,):
        fabric(face, "S", "velvet", 16003, 3, 0, 0, 2, 12)
        fabric(face, "S", "velvet", 16003, 3, 6, 0, 2, 12)
        face.vline(1, 0, 11, "S2"), face.vline(6, 0, 11, "S2")
    line(j.front, 1, 1, 6, 5, "A2"), line(j.front, 6, 1, 1, 5, "A2")    # the crossed cords
    shoulders = mantle(g, "mantle_shoulders", "S", "velvet", 16004, 3, height=3, width=17, depth=6, y=-.7)
    shoulders.front.vline(8, 0, 2, "S1")
    collar = g.piece("fur_collar", "TORSO", (-4.6, -1.6, -2.8), (9, 2, 6), inflate=.08)
    fur_box(collar, "M", 16005, 3)
    upper, tail = cloak(g, "mantle", "S", "velvet", 16006, base=3, width=10, length=11, tail=10, z=2.75)
    for face in (upper, tail):
        face.vline(1, 0, face.h - 1, "S2"), face.vline(8, 0, face.h - 1, "S2")
    for i, x in enumerate((-1.4, 1.4)):
        tassel = g.piece(f"tassel_{i}", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(x, 5.0, -2.75))
        solid(tassel, "A", "plain", 16007 + i, 2)
        tassel.strip.hline(0, tassel.strip.w - 1, 0, "M3")
