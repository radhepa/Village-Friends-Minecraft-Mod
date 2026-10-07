"""Sidesaddle Riding Skirt: an asymmetric riding skirt cut long on the left to drape over the saddle, with tall boots."""
from kit_female import shoes, skirt
from paint import solid

META = {
    "name": "Sidesaddle Riding Skirt",
    "gender": "female",
    "description": "An asymmetric riding skirt cut long on the left to drape over a sidesaddle, a leather-bound hem and tall boots.",
    "tags": ["sturdy", "tailored", "skirt"],
}


def build(g):
    s = skirt(g, "P", "twill", 15811, top=9.8, length=9, back_length=10, sides=False)
    for name, x, ox, rot, length in (("skirt_right", -5.1, 0, 4, 8), ("skirt_left", 5.1, -1, -6, 12)):
        side = g.piece(name, "TORSO", (ox, 0, -2.5), (1, length, 5), pivot=(x, 9.8, 0), rotation=(0, 0, rot))
        solid(side, "P", "twill", 15812, 2)
        for face in side.sides:
            face.hline(0, face.w - 1, length - 1, "L2")
    for face in s.wide_faces:
        face.hline(0, face.w - 1, face.h - 1, "L2")
        for x in range(6, 10):
            face.set(x, face.h - 1, "P1")
    shoes(g, "boot", "L", 2, top=7)
