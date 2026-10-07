"""Astrologer's Star Robe: an open night-dark robe sewn with stars and a crescent, wide sleeves and a brass astrolabe on a cord."""
from kit import body, flaps, sleeves
from kit_male import blk, sleeve_shapes
from paint import fabric, grid, line

META = {
    "name": "Astrologer's Star Robe",
    "gender": "male",
    "description": "An open, night-dark robe sewn with little stars and a crescent moon, wide sleeves, and a brass astrolabe hanging on a cord.",
    "tags": ["scholarly", "robe"],
    "covers_waist": True,
}

STARS = ((1, 2), (6, 4), (2, 8), (5, 10), (0, 6))
MOON = [".aa",
        "a..",
        ".aa"]


def stars(face, flip=False):
    for x, y in STARS:
        x = face.w - 1 - x if flip else x
        if face.inside(x, y):
            face.set(x, y, "S4")


def build(g):
    b = body(g, "S", "weave", 9901, base=3)
    robe = body(g, "P", "velvet", 9902, base=1, layer="jacket")
    for y in range(12):
        robe.front.clear(3, y), robe.front.clear(4, y)
        robe.front.set(2, y, "M2"), robe.front.set(5, y, "M2")
    stars(robe.front), stars(robe.back, True)
    grid(robe.back, 2, 1, MOON, {"a": "M3"})
    sleeves(g, "P", "velvet", 9903, base=1, rows=(0, 10))
    for s in sleeve_shapes(g, "star_sleeve", "P", 3.6, (5, 6, 5), "velvet", 9904, base=1, inflate=.18):
        for face in s.sides:
            stars(face)
            face.hline(0, face.w - 1, 5, "M2")
    jf = g.part("jacket").front
    line(jf, 3, 0, 3, 5, "K3")
    astrolabe = blk(g, "astrolabe", (0, 6.0, -2.7), (3, 3, 1), "M", 3, "smooth", 9906, edge=False)
    astrolabe.front.set(1, 1, "K2"), astrolabe.front.set(0, 0, "M4"), astrolabe.front.hline(0, 2, 2, "M2")
    for face in flaps(g, "robe_skirt", 7, "P", "velvet", 9907, base=1, top=11.0):
        stars(face, face.name == "back")
        if face.name == "front":
            fabric(face, "S", "weave", 9908, 3, 3, 0, 3, 7)
            face.vline(2, 0, 6, "M2"), face.vline(6, 0, 6, "M2")
