"""Illuminator's Gold-Leaf Smock: a loose dyed-linen smock honeycomb-smocked at the yoke, white linen
oversleeves tied at elbow and wrist to keep the work clean, flecks of gold leaf caught on the breast,
brushes in a breast pocket, and a gold-leaf book and a tooth burnisher hung from a cord."""
from kit import body, sleeves
from kit_female import arm_rings, girdle, smocking
from kit_f05 import dangle, fixed
from paint import grid

META = {
    "name": "Illuminator's Gold-Leaf Smock",
    "gender": "female",
    "description": "A smocked linen smock flecked with gold leaf, white tied oversleeves, brushes in the pocket and a gold-leaf book on a cord.",
    "tags": ["work", "whimsical", "relaxed"],
}

FLAKES = [(5, 6), (6, 7), (1, 8), (4, 9), (6, 10)]


def build(g):
    b = body(g, "P", "plain", 55361, base=2)
    for face in (b.front, b.back):
        smocking(face, "P", 2, 0, 1, h=3)
        face.hline(0, 7, 0, "P3")
        face.vline(2, 5, 11, "P1"), face.vline(5, 5, 11, "P1")      # the smock's loose folds below
    for x, y in FLAKES:
        b.front.set(x, y, "M4")                                      # gold leaf caught on the linen
    b.front.set(6, 6, "M3")
    sleeves(g, "P", "plain", 55362, base=2, rows=(0, 11))
    # White linen oversleeves, tied at the elbow and the wrist.
    for box in arm_rings(g, "oversleeve", 2.8, 7, 5, inflate=.1):
        for face in box.faces:
            for y in range(face.h):
                face.hline(0, face.w - 1, y, "S4")
        for face in box.sides:
            face.hline(0, face.w - 1, 0, "L2"), face.hline(0, face.w - 1, 6, "L2")
            face.vline(1, 1, 5, "S3"), face.vline(3, 2, 5, "S3")
            face.set(2, 0, "L3")
        box.bottom.fill("S3")
    # The breast pocket and the brushes standing in it.
    j = g.part("jacket")
    grid(j.front, 1, 3, ["ppp", "pPp", "ppp"], {"p": "P1", "P": "P2"})
    for i, (x, tip) in enumerate(((-2.5, "K1"), (-1.0, "A2"))):
        brush = fixed(g, f"brush_{i}", (x, 2.7 - i * .3, -2.45), (1, 2, 1), "L", 3, "plain", 55363 + i, edge=False)
        brush.top.fill(tip)
        for face in brush.sides:
            face.set(0, 0, tip)
    girdle(g, "cord", 8.2, role="L", base=2, height=1, buckle=None, texture="plain")
    # A little book of gold leaf on the left, the gilt edges showing; a dog-tooth burnisher on the right.
    book = dangle(g, "leaf_book", 2.6, .4, (2, 3, 1), "L", 1, "plain", top=9.0, seed=55365, edge=False)
    for face in (book.right, book.left):
        face.fill("M4")
    book.bottom.fill("M4")
    book.front.set(1, 0, "M3")
    string = dangle(g, "leaf_book_string", 2.6, -.6, (1, 1, 1), "L", 2, "plain", top=9.0, seed=55366, edge=False)
    string.front.fill("L3")
    stick = dangle(g, "burnisher", -2.4, -.4, (1, 4, 1), "L", 3, "plain", top=9.0, seed=55367, edge=False)
    stick.front.set(0, 0, "L2")
    tooth = dangle(g, "burnisher_tooth", -2.4, 3.6, (1, 1, 1), "S", 4, "plain", top=9.0, seed=55368, edge=False)
    tooth.bottom.fill("S3")
