"""Ermine-Hemmed Skirt: a velvet skirt with a deep ermine band at the hem, white fur flecked with black tails."""
from kit_female import shoes, skirt

META = {
    "name": "Ermine-Hemmed Skirt",
    "gender": "female",
    "description": "A velvet skirt with a deep band of ermine at the hem, white fur flecked with black tails, and pointed shoes.",
    "tags": ["fancy", "skirt", "long_skirt"],
}


def ermine(face):
    for y in range(face.h - 3, face.h):
        for x in range(face.w):
            spot = (x + face.x0 + (y % 2) * 2) % 4 == 0 and y == face.h - 2
            face.set(x, y, "K1" if spot else "S4" if (x + y) % 3 else "S3")


def build(g):
    s = skirt(g, "P", "velvet", 16011, top=9.8, length=12)
    s.paint(ermine)
    shoes(g, "pointed", "K", 2)
