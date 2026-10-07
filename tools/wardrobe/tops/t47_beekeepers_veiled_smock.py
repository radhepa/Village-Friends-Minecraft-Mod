"""Beekeeper's Veiled Smock: a pale smock with a gauze veil gathered at the throat, long gloves and a smoker at the belt."""
from kit import belt, body, flaps, neckline, sleeves
from kit_male import blk, hood_down, sleeve_shapes
from paint import fabric

META = {
    "name": "Beekeeper's Veiled Smock",
    "gender": "male",
    "description": "A pale bee-ward's smock with a dark gauze veil gathered at the throat, hood thrown back, long gloves and a smoker.",
    "tags": ["work", "casual"],
    "locked_to": "b47_beekeepers_bound_trousers",
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 4701, base=3)
    neckline(b.front, "round", "S", base=3)
    sleeves(g, "S", "weave", 4702, base=3, rows=(0, 6))
    for side in ("right", "left"):
        glove = g.part(f"{side}_sleeve")
        fabric(glove.strip, "L", "leather", 4703, 3, 0, 6, glove.strip.w, 6)
        glove.strip.hline(0, glove.strip.w - 1, 6, "L4")
        glove.bottom.fill("L2")
    sleeve_shapes(g, "glove_cuff", "L", 3.6, (5, 2, 5), "leather", 4704, base=3, inflate=.16)
    veil = g.piece("veil_gather", "TORSO", (-5.5, -.9, -3.0), (11, 3, 6), inflate=.06)
    for face in veil.faces:
        for y in range(face.h):
            for x in range(face.w):
                face.set(x, y, "K3" if (x + y) % 3 else "K1")                 # fine dark gauze
    for face in veil.sides:
        face.hline(0, face.w - 1, 0, "S2")                               # drawcord at the throat
    hood_down(g, "S", "weave", 4706, base=3, lining="K3", y=-.6, z=3.0)
    belt(g, "belt", 9.4, role="S", base=2, height=1, buckle=None)
    can = blk(g, "smoker_can", (-3.0, 9.4, -2.75), (2, 3, 2), "M", 2, "smooth", 4707)
    can.front.set(0, 1, "M3"), can.top.fill("M1")
    blk(g, "smoker_spout", (-3.0, 8.4, -2.75), (1, 1, 1), "M", 1, "smooth", 4708, edge=False)
    bee = blk(g, "bee", (2.4, 3.6, -2.4), (1, 1, 1), "K", 2, "plain", 4709, edge=False)
    bee.top.fill("A3"), bee.front.fill("A2")
    for face in flaps(g, "smock_hem", 4, "S", "weave", 4710, base=3, top=10.6):
        face.hline(0, 8, 3, "S2")
