"""Clasped Half-Cloak: a short wool cloak over both shoulders, pinned with a brooch, over a plain tunic."""
from kit import belt, body, neckline, sleeves
from paint import fabric, grid, k, solid

META = {
    "name": "Clasped Half-Cloak",
    "gender": "male",
    "description": "A short wool cloak over the shoulders, fastened with a brooch, over a belted tunic.",
    "tags": ["casual", "rugged"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "weave", 1301, base=3)
    neckline(b.front, "round", "S", base=3)
    sleeves(g, "S", "weave", 1302, base=3, rows=(0, 10), cuff="S2")
    belt(g, "belt", 9.6)
    # The cloak: a mantle over the shoulders and a back drape to mid-back, in deep primary wool.
    mantle = g.piece("cloak_mantle", "TORSO", (-8.5, -.6, -2.8), (17, 4, 6), inflate=.04)
    solid(mantle, "P", "weave", 1303, 1)
    fabric(mantle.top, "P", "weave", 1303, 2)
    for face in mantle.sides:
        face.hline(0, face.w - 1, 3, "P0")
        for x in range(0, face.w, 3):
            face.set(x, 1, "P0")
    mantle.front.vline(8, 0, 3, "P0")   # the cloak opens at the front
    back = g.piece("cloak_back", "TORSO", (-5, 0, 0), (10, 8, 1), pivot=(0, 3.2, 2.6), rotation=(5, 0, 0))
    solid(back, "P", "weave", 1304, 1)
    back.back.vline(3, 0, 7, "P0"), back.back.vline(6, 1, 7, "P2"), back.back.hline(0, 9, 7, "P0")
    brooch = g.piece("brooch", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(-2.4, .6, -3.1), inflate=.05)
    solid(brooch, "M", "smooth", 1305, 3, edge=False)
    brooch.front.set(0, 0, "M4"), brooch.front.set(1, 1, "A2")
