"""Interpreter's Two-Tongue Tabard: a tabard parted down the middle in two colours, counter-edged, laced open at the sides and cut below into two pointed tongues, over a plain shirt."""
from kit import body, neckline, sleeves
from paint import grid, solid

META = {
    "name": "Interpreter's Two-Tongue Tabard",
    "gender": "male",
    "description": "A go-between's tabard parted down the middle in two colours, each half edged in the other's, a book worked on one breast and a scroll on the other, laced open at the sides and cut below into two pointed tongues before and behind.",
    "tags": ["scholarly", "casual", "whimsical"],
    "covers_waist": True,
}

BOOK = ["aaa", "aba", "aaa"]
SCROLL = ["a.a", ".b.", "a.a"]


def half(face, x0, x1, own, other):
    for y in range(face.h):
        for x in range(x0, x1 + 1):
            face.set(x, y, f"{own}2" if (x + y) % 7 else f"{own}1")
    face.vline(x0 if x0 == 0 else x1, 0, face.h - 1, f"{other}2")       # the outer edge bound in the other colour


def build(g):
    b = body(g, "S", "weave", 35520, base=3)
    neckline(b.front, "round", "S", base=3)
    sleeves(g, "S", "weave", 35521, base=3, rows=(0, 10), cuff="S1")
    tab = g.part("jacket")
    f, bk = tab.front, tab.back
    half(f, 0, 3, "P", "A"), half(f, 4, 7, "A", "P")                    # wearer's right in P, left in A
    half(bk, 0, 3, "A", "P"), half(bk, 4, 7, "P", "A")
    for face in (f, bk):
        face.vline(3, 0, 11, face.get(3, 0)[0] + "1")                    # the parting seam
    f.clear(3, 0), f.clear(4, 0), f.set(3, 1, "P1"), f.set(4, 1, "A1")
    grid(f, 0, 3, BOOK, {"a": "A3", "b": "S4"})
    grid(f, 4, 3, SCROLL, {"a": "P3", "b": "P2"})
    tab.top.rect(0, 0, 4, 4, "P3"), tab.top.rect(4, 0, 4, 4, "A3")
    for face in (tab.right, tab.left):                                   # open sides, laced at two points
        for y in range(12):
            for x in range(face.w):
                face.clear(x, y)
        for y in (5, 9):
            face.hline(0, face.w - 1, y, "L2")
            face.set(1, y, "L3")
    for name, z, motion, face_name in (("front", -2.85, "flap_front", "front"), ("back", 1.85, "flap_back", "back")):
        for i, (x, role) in enumerate(((-2.0, "P"), (2.0, "A"))):       # each tongue matches its half
            other = "A" if role == "P" else "P"
            tongue = g.piece(f"tongue_{name}_{i}", "TORSO", (-2, 0, 0), (4, 5, 1), pivot=(x, 11.4, z), motion=motion)
            solid(tongue, role, "weave", 35522 + i, 2)
            face = getattr(tongue, face_name)
            face.vline(0, 0, 4, f"{other}2"), face.vline(3, 0, 4, f"{other}2")
            face.hline(0, 3, 0, f"{role}3")
            tip = g.piece(f"tongue_tip_{name}_{i}", "TORSO", (-1, 5, 0), (2, 1, 1), pivot=(x, 11.4, z), motion=motion)
            solid(tip, other, "plain", 35524 + i, 2, edge=False)
