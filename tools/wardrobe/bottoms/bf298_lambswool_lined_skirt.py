"""Lambswool-Lined Skirt: a heavy wool skirt lined with lambswool that shows at a front kick-slit and along the hem, over fleece-cuffed boots."""
from kit_f10 import lambswool
from kit_female import leg_rings, shoes, skirt

META = {
    "name": "Lambswool-Lined Skirt",
    "gender": "female",
    "description": "A heavy wool skirt lined with curly lambswool that shows at a front kick-slit and in a fleecy roll along the hem, over fleece-cuffed boots.",
    "tags": ["rugged", "skirt", "long_skirt"],
}


def slit(face):
    """An inverted-V kick-slit from the knee to the hem, its edges turned back over the fleece lining."""
    for y in range(5, face.h):
        half = (y - 5) * .45
        for x in range(face.w):
            d = abs(x - 4.5)
            if d < half + .5:
                face.set(x, y, "S3" if (x + y) % 3 else "S4")
            elif d < half + 1.5:
                face.set(x, y, "P3")                                   # the turned-back edge


def fleece_hem(face):
    """The lining rolled just past the hem."""
    for x in range(face.w):
        face.set(x, face.h - 1, "S4" if (x + face.x0) % 2 else "S2")


def build(g):
    s = skirt(g, "P", "weave", 60500, top=9.8, length=11, flare=6)
    slit(s.front.front)
    s.paint(fleece_hem)
    shoes(g, "boot", "L", 1, top=9)
    for ring in leg_rings(g, "fleece_cuff", 8.9, 1, 5, inflate=.12):
        for f in ring.faces:
            lambswool(f, 60501)
