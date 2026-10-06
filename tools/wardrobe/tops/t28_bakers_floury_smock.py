"""Baker's Floury Smock: a buttoned cream smock dusted with flour, a kerchief and a spoon in the pocket."""
from kit import body, neckline, roll, sleeves
from paint import rnd, solid

META = {
    "name": "Baker's Floury Smock",
    "gender": "male",
    "description": "A buttoned baker's smock, dusted with flour, a knotted kerchief and a wooden spoon in the pocket.",
    "tags": ["casual", "work"],
}


def dust(face, seed, rows):
    for y in rows:
        for x in range(face.w):
            if rnd(x, y, seed) < .18 and face.get(x, y):
                face.set(x, y, "S4")


def build(g):
    b = body(g, "S", "weave", 2801, base=3)
    neckline(b.front, "keyhole", "S", base=3)
    b.front.vline(4, 2, 11, "S2")
    for y in (3, 6, 9):
        b.front.set(4, y, "M3")
    b.front.hline(5, 7, 4, "S2"), b.front.vline(5, 4, 6, "S2"), b.front.hline(5, 7, 6, "S2")   # pocket
    dust(b.front, 2802, range(7, 12))
    dust(b.back, 2803, range(9, 12))
    sleeves(g, "S", "weave", 2804, base=3, rows=(0, 5))
    for side in ("right", "left"):
        dust(g.part(f"{side}_arm").front, 2805, range(6, 12))
    roll(g, "S", 2.6, base=3)
    kerchief = g.piece("kerchief", "TORSO", (-4.5, -.6, -2.6), (9, 1, 5), inflate=.04)
    solid(kerchief, "A", "plain", 2806, 2, edge=False)
    knot = g.piece("kerchief_knot", "TORSO", (-1, -.5, -.5), (2, 2, 1), pivot=(0, .8, -2.9))
    solid(knot, "A", "plain", 2807, 2)
    spoon = g.piece("spoon", "TORSO", (-.5, -3, -.5), (1, 3, 1), pivot=(2.6, 4.6, -2.6), rotation=(0, 0, -10))
    solid(spoon, "L", "smooth", 2808, 3, edge=False)
    spoon.strip.hline(0, spoon.strip.w - 1, 0, "L4")
