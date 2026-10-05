"""Sheepskin Vest: a leather vest turned fleece-side in, its wool showing at every edge, over a wool shirt."""
from kit import body, neckline, sleeves
from paint import fabric, rnd, solid

META = {
    "name": "Sheepskin Vest",
    "description": "A shepherd's leather vest with fleece curling out at the collar, armholes and hem.",
    "tags": ["casual", "rugged"],
}


def fleece(face, x, y):
    face.set(x, y, "S4" if (x + y) % 2 else "S3")


def build(g):
    b = body(g, "P", "weave", 1901)
    neckline(b.front, "keyhole", "P")
    sleeves(g, "P", "weave", 1902, rows=(0, 10), cuff="P1")
    vest = body(g, "L", "leather", 1903, layer="jacket", rows=(0, 10))
    vf = vest.front
    for y in range(11):
        vf.clear(3, y), vf.clear(4, y)
        fleece(vf, 2, y), fleece(vf, 5, y)
    for face in vest.sides:
        for x in range(face.w):
            fleece(face, x, 10)
    vest.top.hline(0, 7, 3, "S4")
    for x in range(8):
        fleece(vest.top, x, 0)
    collar = g.piece("fleece_collar", "TORSO", (-4.6, -1.0, -2.7), (9, 2, 5), inflate=.08)
    for face in collar.faces:
        for y in range(face.h):
            for x in range(face.w):
                face.set(x, y, "S4" if rnd(x, y, 1904 + face.x0) > .4 else "S2")
    for side in ("right", "left"):
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        ox = -3.0 if side == "right" else -1.0
        cuff = g.piece(f"{side}_fleece_armhole", bone, (ox - .45, -2.2, -2.45), (5, 2, 5))
        for face in cuff.faces:
            for y in range(face.h):
                for x in range(face.w):
                    face.set(x, y, "S4" if (x + y) % 2 else "S2")
