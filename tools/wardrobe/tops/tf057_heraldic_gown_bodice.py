"""Heraldic Gown Bodice: a lady's mi-parti gown bodice, one half charged with stars, the other barred, under an ermine edge."""
from kit import sleeves
from kit_female import motif, neck
from paint import fabric, solid

META = {
    "name": "Heraldic Gown Bodice",
    "gender": "female",
    "description": "A lady's mi-parti gown bodice bearing her arms: one half sown with stars, the other barred, edged with ermine.",
    "tags": ["fancy", "gown"],
    "locked_to": "bf057_heraldic_gown_skirt",
    "covers_waist": True,
}


def halves(face, right_first):
    for y in range(face.h):
        for x in range(face.w):
            right = (x < face.w // 2) == right_first
            if right:
                face.set(x, y, "P2")
            else:
                face.set(x, y, "S3" if (y // 2) % 2 else "A2")


def build(g):
    body = g.part("body")
    halves(body.front, True)
    halves(body.back, False)
    fabric(body.right, "P", "velvet", 15702, 2)
    for y in range(body.left.h):
        body.left.hline(0, 3, y, "S3" if (y // 2) % 2 else "A2")
    fabric(body.top, "P", "velvet", 15703, 3)
    neck(body.front, "square", "P", 2)
    for x, y in ((0, 3), (1, 6), (0, 9)):
        motif(body.front, x, y, "star", a="M3", b="M4")
    motif(body.back, 5, 4, "star", a="M3", b="M4")
    j = g.part("jacket")
    for x in range(1, 7):
        j.front.set(x, 2, "S4" if x % 3 else "K1")                     # ermine edge
    sleeves(g, "P", "velvet", 15704, rows=(0, 11))
    left = g.part("left_arm")
    for y in range(12):
        left.strip.hline(0, 15, y, "S3" if (y // 2) % 2 else "A2")
    belt = g.piece("girdle", "TORSO", (-4.6, 7.8, -2.6), (9, 1, 5), inflate=.05)
    solid(belt, "M", "smooth", 15705, 3, edge=False)
    for face in belt.sides:
        for x in range(0, face.w, 2):
            face.set(x, 0, "M4")
