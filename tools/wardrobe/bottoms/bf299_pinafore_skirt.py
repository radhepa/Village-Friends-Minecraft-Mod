"""Pinafore Skirt: a knee-length pinafore skirt with two patch pockets over a long pale petticoat whose edged hem shows beneath."""
from kit_female import shoes, skirt, tier, trim
from paint import strip_fabric

META = {
    "name": "Pinafore Skirt",
    "gender": "female",
    "description": "A knee-length pinafore skirt with two deep patch pockets, worn over a long pale petticoat whose edged hem shows beneath, and low shoes.",
    "tags": ["casual", "work", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "S", "weave", 60540, base=3, top=9.8, length=11, flare=5, folds=False)
    s.paint(lambda f: trim(f, f.h - 2, "dots", "S4"))                 # the petticoat's pricked edging
    s.hem("S1")
    body = g.part("body")
    strip_fabric(body, "P", "weave", 60541, 2, 9, 11)
    faces = tier(g, s, "pinafore", y=0, h=7, role="P", texture="weave", seed=60542, grow=2, flare=7)
    for face in faces:
        face.hline(0, face.w - 1, 0, "P3")
        face.hline(0, face.w - 1, face.h - 1, "P1")
    for face in faces[:2]:
        face.vline(5, 1, face.h - 2, "P1"), face.vline(6, 1, face.h - 2, "P3")   # the centre fold
    front = faces[0]
    for x0 in (1, front.w - 5):                                         # two deep patch pockets
        front.hline(x0, x0 + 3, 2, "P3")
        front.vline(x0, 3, 4, "P1"), front.hline(x0, x0 + 3, 5, "P1")
    shoes(g, "shoe", "L", 2)
