"""Bard's Lute-Slung Cotte: a long cotte with dagged bell sleeves, a lute slung across the back and a music roll at the belt."""
from kit import belt, body, flaps, neckline, sleeves
from kit_male import blk, sleeve_shapes
from paint import line, solid

META = {
    "name": "Bard's Lute-Slung Cotte",
    "gender": "male",
    "description": "A wandering player's cotte with dagged bell sleeves, a lute slung across the back on a strap and a music roll in the belt.",
    "tags": ["whimsical", "fancy"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 5801)
    neckline(b.front, "v", "P")
    sleeves(g, "P", "velvet", 5802, rows=(0, 10), cuff="A2")
    for s in sleeve_shapes(g, "dagged_sleeve", "P", 2.8, (5, 4, 5), "velvet", 5803, inflate=.15):
        for face in s.sides:
            for x in range(face.w):
                face.set(x, 3, "A2" if x % 2 else "P1")                   # dagged, accent-lined edge
        s.bottom.fill("A1")
    jacket = g.part("jacket")
    line(jacket.front, 7, 0, 0, 9, "L2"), line(jacket.back, 0, 0, 7, 9, "L2")   # lute strap
    # The lute rides across the back: a rounded body, a neck and a bent-back pegbox.
    bowl = g.piece("lute_body", "TORSO", (-2, 0, -1), (4, 5, 2), pivot=(-1.0, 4.6, 3.4), rotation=(0, 0, -35))
    solid(bowl, "L", "smooth", 5805, 3)
    bowl.back.set(1, 2, "K2"), bowl.back.set(2, 2, "K2"), bowl.back.hline(0, 3, 4, "L1")
    neck = g.piece("lute_neck", "TORSO", (-.5, -5, -.5), (1, 5, 1), pivot=(-1.0, 4.6, 3.6), rotation=(0, 0, -35))
    solid(neck, "L", "smooth", 5806, 1)
    peg = g.piece("lute_pegbox", "TORSO", (-.5, -7, -.5), (1, 2, 1), pivot=(-1.0, 4.6, 3.6), rotation=(30, 0, -35))
    solid(peg, "L", "smooth", 5807, 2)
    belt(g, "belt", 9.4, height=1)
    roll = blk(g, "music_roll", (-2.8, 8.0, -2.8), (1, 3, 1), "S", 4, "plain", 5808, rotation=(0, 0, 12))
    roll.strip.hline(0, roll.strip.w - 1, 1, "A2")
    for face in flaps(g, "hem", 4, "P", "velvet", 5809, top=10.6):
        face.hline(0, 8, 3, "A2")
