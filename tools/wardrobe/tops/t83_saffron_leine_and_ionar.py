"""Saffron Leine & Ionar: a voluminous pleated-sleeve leine shirt under a short, cropped ionar jacket edged in braid."""
from kit import body, flaps, sleeves
from kit_male import sleeve_shapes

META = {
    "name": "Saffron Leine & Ionar",
    "gender": "male",
    "description": "A Gaelic leine with vast pleated sleeves falling to the knee-length hem, under a short cropped ionar jacket edged in braid.",
    "tags": ["casual", "kilt"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "A", "weave", 8301, base=3)                             # the saffron leine
    for face in b.sides:
        for x in range(0, face.w, 2):
            face.vline(x, 7, 11, "A2")
    sleeves(g, "A", "weave", 8302, base=3, rows=(0, 10))
    for s in sleeve_shapes(g, "pleated_sleeve", "A", 1.4, (5, 8, 6), "weave", 8303, base=3, inflate=.2, dz=.6):
        for face in s.sides:
            for x in range(0, face.w, 2):
                face.vline(x, 1, 7, "A2")
            face.hline(0, face.w - 1, 7, "A1")
    jacket = g.part("jacket")                                            # the cropped ionar
    for face in jacket.sides:
        for y in range(6):
            for x in range(face.w):
                face.set(x, y, "P2" if (x + y) % 5 else "P1")
        face.hline(0, face.w - 1, 5, "M2")
    jacket.front.vline(3, 0, 5, "M2"), jacket.front.vline(4, 0, 5, "M2")
    jacket.front.hline(3, 4, 0, None), jacket.front.hline(3, 4, 1, None)
    for face in flaps(g, "leine_hem", 6, "A", "weave", 8305, base=3, top=11.0):
        for x in range(0, 9, 2):
            face.vline(x, 1, 5, "A2")
        face.hline(0, 8, 5, "A1")
