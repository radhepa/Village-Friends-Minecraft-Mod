"""Wrapped Wool Shawl: a checked wool shawl crossed over the chest and pinned, over a tucked linen shirt."""
from kit import body, neckline, sleeves
from paint import k, solid

META = {
    "name": "Wrapped Wool Shawl",
    "gender": "male",
    "description": "A checked wool shawl wrapped over both shoulders, crossed on the chest and pinned with a brooch.",
    "tags": ["casual", "rugged"],
    "tucked": True,
}


def check(face, seed=0):
    for y in range(face.h):
        for x in range(face.w):
            gx, gy = (x + seed) % 4, y % 4
            key = "P1" if gx == 0 and gy == 0 else "P2" if gx == 0 or gy == 0 else "P3"
            if gx == 2 and gy == 2:
                key = "A2"
            face.set(x, y, key)


def build(g):
    b = body(g, "S", "weave", 2001, base=3)
    neckline(b.front, "laced", "S", base=3)
    sleeves(g, "S", "weave", 2002, base=3, rows=(0, 10), cuff="S2")
    jacket = g.part("jacket")
    jf, jb = jacket.front, jacket.back
    # The two ends cross on the chest: diagonal bands from each shoulder to the opposite hip.
    for y in range(9):
        for dx in range(3):
            for x in (y // 2 + dx, 7 - y // 2 - dx):
                if 0 <= x < 8:
                    jf.set(x, y, "P2" if (x + y) % 4 else "P1")
    for y in range(7):
        for x in range(8):
            if abs(x - 3.5) <= 3.5 - y / 2:
                jb.set(x, y, "P2" if (x + y) % 4 else "A2" if (x * y) % 7 == 3 else "P1")
    for face in (jacket.right, jacket.left):
        for y in range(3):
            face.hline(0, 3, y, "P2")
    for x in range(8):
        for y in range(4):
            jacket.top.set(x, y, "P3" if (x + y) % 3 else "P1")
    drape = g.piece("shawl_drape", "TORSO", (-4.6, -.8, -2.7), (9, 3, 5), inflate=.06)
    for face in drape.faces:
        check(face, face.x0)
    pin = g.piece("shawl_pin", "TORSO", (-.5, -.5, -.5), (1, 1, 1), pivot=(0, 4.5, -2.8), inflate=.12)
    solid(pin, "M", "smooth", 2003, 3, edge=False)
