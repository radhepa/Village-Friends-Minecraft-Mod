"""Layered Overtunic: a sleeveless overtunic, slit at the sides, over a long-sleeved undertunic."""
from kit import body, flaps, neckline, sleeves
from paint import solid

META = {
    "name": "Layered Overtunic",
    "description": "A side-slit sleeveless overtunic with banded neck and hem over a contrasting undertunic.",
    "tags": ["casual", "simple"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 2501, base=3)
    neckline(b.front, "round", "S", base=3)
    sleeves(g, "S", "weave", 2502, base=3, rows=(0, 10), cuff="A2")
    over = body(g, "P", "weave", 2503, layer="jacket")
    over.front.clear(3, 0), over.front.clear(4, 0)
    for face in (over.front, over.back):
        face.hline(1, 6, 0 if face is over.back else 1, "A2")
        face.vline(0, 6, 11, "P1"), face.vline(7, 6, 11, "P1")
    for face in (over.right, over.left):
        for y in range(6, 12):
            face.hline(0, face.w - 1, y, None)   # side slits show the undertunic
    cord = g.piece("cord_belt", "TORSO", (-4.6, 9.4, -2.6), (9, 1, 5), inflate=.06)
    solid(cord, "A", "plain", 2504, 2, edge=False)
    knot = g.piece("cord_knot", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(-2.4, 10.2, -2.8), motion="sway")
    solid(knot, "A", "plain", 2505, 3)
    front, back = flaps(g, "overtunic", 5, "P", "weave", 2506, width=8, top=11.2, hem="A2")
