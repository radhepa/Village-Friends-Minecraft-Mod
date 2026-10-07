"""Starry Mage Robe: a velvet robe sewn with stars, a high standing collar, bell sleeves and a crystal pendant."""
from kit import sleeves
from kit_female import bells, girdle, over_flaps, scatter, trim
from paint import fabric, solid, strip_fabric

META = {
    "name": "Starry Mage Robe",
    "gender": "female",
    "description": "A night-dark velvet robe sewn with silver stars, a high collar, star-lined bell sleeves and a crystal pendant.",
    "tags": ["robe", "scholarly"],
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "velvet", 12901, 1)
    fabric(b.top, "P", "velvet", 12901, 2), fabric(b.bottom, "P", "velvet", 12901, 0)
    for face in b.sides:
        scatter(face, "star", "M3", "M4", step=(5, 5), y0=1)
    b.front.vline(3, 0, 11, "M2"), b.front.vline(4, 0, 11, "P0")
    sleeves(g, "P", "velvet", 12902, base=1, rows=(0, 11))
    for box in bells(g, "P", "velvet", 12903, base=1, y=4.0, h=6, size=6, lining="A2"):
        for face in box.sides:
            face.hline(0, face.w - 1, 5, "M3")
            face.set(1, 2, "M4"), face.set(4, 3, "M3")
    collar = g.piece("high_collar", "TORSO", (-4.5, -2.0, -2.6), (9, 3, 5), inflate=.06)
    solid(collar, "P", "velvet", 12904, 1)
    for face in collar.sides:
        face.hline(0, face.w - 1, 0, "M3")
    collar.front.vline(4, 0, 2, "P0")
    pendant = g.piece("crystal", "TORSO", (-.5, -1, -.5), (1, 2, 1), pivot=(0, 3.6, -2.7), inflate=.05)
    solid(pendant, "A", "smooth", 12905, 3, edge=False)
    pendant.front.set(0, 0, "A4")
    girdle(g, "girdle", 8.0, role="M", base=2, height=1, buckle=None, texture="smooth", wide=True)
    f, bk = over_flaps(g, "robe", 12, "P", "velvet", 12906, base=1, width=10, top=9.0)
    for face in (f, bk):
        scatter(face, "star", "M3", "M4", step=(5, 5), y0=1, y1=8)
        trim(face, 9, "wave", "M3")
        face.hline(0, face.w - 1, 11, "M2")
