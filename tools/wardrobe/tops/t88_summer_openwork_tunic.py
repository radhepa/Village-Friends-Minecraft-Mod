"""Summer Openwork Tunic: a light linen tunic with drawn-thread openwork bands, short wide sleeves and side vents."""
from kit import body, neckline, sleeves
from kit_male import embroider

META = {
    "name": "Summer Openwork Tunic",
    "gender": "male",
    "description": "A light summer linen tunic with bands of drawn-thread openwork at chest, sleeves and hem, short wide sleeves and side vents.",
    "tags": ["casual", "simple", "relaxed"],
}


def openwork(face, y):
    for x in range(face.w):
        face.set(x, y, "S1" if x % 2 else "S4")
        face.set(x, y + 1, "S4" if x % 2 else "S1")


def build(g):
    b = body(g, "S", "weave", 8801, base=3)
    neckline(b.front, "keyhole", "S", base=3)
    for face in b.sides:
        openwork(face, 3)
        openwork(face, 10)
    for face in (b.right, b.left):
        face.vline(1, 8, 11, "S0")                                       # side vents
    embroider(b.front, 1, "dots", "A2", x0=1, x1=6)
    sleeves(g, "S", "weave", 8802, base=3, rows=(0, 4))
    for side in ("right", "left"):
        sleeve = g.part(f"{side}_sleeve")
        for face in sleeve.sides:
            for y in range(0, 5):
                face.hline(0, face.w - 1, y, "S3" if y < 4 else "S1")
        openwork(sleeve.strip, 2)
