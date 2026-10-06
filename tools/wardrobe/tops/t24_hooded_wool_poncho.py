"""Hooded Wool Poncho: a striped woven poncho over the shoulders with its hood lying back."""
from kit import body, neckline, sleeves
from paint import solid

META = {
    "name": "Hooded Wool Poncho",
    "gender": "male",
    "description": "A hand-woven striped poncho draped over the shoulders, fringed at the hem, hood lying back.",
    "tags": ["casual", "rugged"],
}


def woven(face, seed=0):
    for y in range(face.h):
        band = (y + seed) % 6
        for x in range(face.w):
            key = "A2" if band == 2 else "S3" if band == 3 and x % 2 else "P1" if band == 5 else "P2"
            face.set(x, y, key)


def build(g):
    b = body(g, "S", "weave", 2401, base=3)
    neckline(b.front, "round", "S", base=3)
    sleeves(g, "S", "weave", 2402, base=3, rows=(0, 10), cuff="S2")
    for name, z in (("poncho_front", -3.0), ("poncho_back", 2.2)):
        panel = g.piece(name, "TORSO", (-4.6, 0, 0), (9, 8, 1), pivot=(0, -.2, z))
        for face in panel.faces:
            woven(face)
        for x in range(9):
            if x % 2:
                panel.front.set(x, 7, "S3"), panel.back.set(x, 7, "S3")   # fringe
    top = g.piece("poncho_shoulders", "TORSO", (-4.6, -.8, -3.0), (9, 1, 6))
    for face in top.faces:
        woven(face, 2)
    top.top.hline(3, 5, 1, "P0"), top.top.hline(3, 5, 2, "P0")
    hood = g.piece("hood", "TORSO", (-3.5, 0, 0), (7, 3, 2), pivot=(0, -1.0, 3.0), rotation=(14, 0, 0))
    solid(hood, "P", "weave", 2403, 2)
    hood.back.hline(0, 6, 0, "A2"), hood.back.vline(3, 1, 2, "P1")
