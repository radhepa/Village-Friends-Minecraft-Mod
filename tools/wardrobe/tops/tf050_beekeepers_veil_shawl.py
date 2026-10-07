"""Beekeeper's Veil Shawl: a netted veil worn as a shawl over a bee-embroidered bodice, a honey pot at the girdle."""
from kit_female import bodice, chemise, girdle, mantle, motif
from paint import solid

META = {
    "name": "Beekeeper's Veil Shawl",
    "gender": "female",
    "description": "A fine netted bee veil thrown over the shoulders like a shawl, a bee-embroidered bodice and a honey pot.",
    "tags": ["casual", "whimsical"],
}


def build(g):
    chemise(g, "S", 3, "weave", 15001, neckline="scoop", sleeve_rows=(0, 11))
    b = bodice(g, "P", "weave", 15002, rows=(2, 9), neckline="square", edge="P3")
    for x, y in ((0, 4), (5, 6), (1, 8)):
        motif(b.front, x, y, "bee", a="A2", b="S4", c="K1")
    motif(b.back, 2, 4, "bee", a="A2", b="S4", c="K1")
    veil = mantle(g, "veil", "S", "plain", 15003, 4, height=4, width=17, depth=6, y=-.8)
    for face in veil.faces:
        for y in range(face.h):
            for x in range(face.w):
                if (x + y) % 3 == 0 or (x - y) % 3 == 0:
                    face.set(x, y, "S2")                             # netting
    for face in veil.sides:
        face.hline(0, face.w - 1, face.h - 1, "S3")
    girdle(g, "girdle", 8.0, role="L", height=1)
    pot = g.piece("honey_pot", "TORSO", (-1, 0, -1), (2, 2, 2), pivot=(-2.8, 6.9, -3.2), inflate=.05)
    solid(pot, "M", "smooth", 15004, 2)
    pot.top.fill("S4")
    for face in pot.sides:
        face.set(0, 1, "A3")
