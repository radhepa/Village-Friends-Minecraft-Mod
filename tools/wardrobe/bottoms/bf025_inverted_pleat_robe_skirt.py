"""Inverted-Pleat Robe Skirt: a floor-length dark skirt with one deep inverted pleat, an inkhorn and pen case at the hip."""
from kit_female import shoes, skirt
from paint import solid

META = {
    "name": "Inverted-Pleat Robe Skirt",
    "gender": "female",
    "description": "A dark floor-length skirt with one deep inverted pleat, an inkhorn and pen case hung at the hip.",
    "tags": ["scholarly", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 12511, base=1, top=9.8, length=12, folds=False)
    for face in s.wide_faces:
        face.vline(4, 1, face.h - 1, "P0"), face.vline(5, 1, face.h - 1, "P0")
        face.vline(3, 2, face.h - 1, "P2"), face.vline(6, 2, face.h - 1, "P2")
    s.band(1, "line", "A1", from_bottom=True)
    s.hem("P0")
    case = g.piece("waist_pen_case", "TORSO", (-.5, 0, -1), (1, 4, 2), pivot=(5.7, 9.8, -.4), rotation=(-8, 0, 0))
    solid(case, "L", "leather", 12512, 2)
    case.left.hline(0, 1, 0, "M3")
    horn = g.piece("waist_inkhorn", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(5.7, 10.4, 1.4))
    solid(horn, "S", "smooth", 12513, 3)
    horn.top.fill("K1")
    shoes(g, "slipper", "K", 2)
