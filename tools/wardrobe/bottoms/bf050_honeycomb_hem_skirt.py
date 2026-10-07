"""Honeycomb-Hem Skirt: a long skirt with a band of honeycomb at the hem and bees embroidered above, and felt boots."""
from kit_female import motif, shoes, skirt

META = {
    "name": "Honeycomb-Hem Skirt",
    "gender": "female",
    "description": "A long skirt with a honey-gold honeycomb band at the hem, bees embroidered above it and felt boots.",
    "tags": ["whimsical", "skirt", "long_skirt"],
}


def honeycomb(face):
    h = face.h
    for y in range(h - 4, h):
        for x in range(face.w):
            r = (y - (h - 4)) % 4
            gx = (x + face.x0 + (2 if (y - (h - 4)) // 2 % 2 else 0)) % 4
            edge = (r in (0, 2) and gx in (1, 2)) or (r in (1, 3) and gx in (0, 3))
            face.set(x, y, "M2" if edge else "A2")


def build(g):
    s = skirt(g, "P", "weave", 15011, top=9.8, length=11)
    s.paint(honeycomb)
    for face in s.wide_faces:
        motif(face, 1, 4, "bee", a="A2", b="S4", c="K1")
        motif(face, 6, 2, "bee", a="A2", b="S4", c="K1")
    shoes(g, "boot", "S", 1, top=9)
