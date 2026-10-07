"""Fleece-Edged Skirt: a hill-country wool skirt bordered with fleece, over thong-bound leg wraps and felt boots."""
from kit import SIDES
from kit_female import fur, shoes, skirt, sub, wraps

META = {
    "name": "Fleece-Edged Skirt",
    "gender": "female",
    "description": "A thick wool skirt edged with a band of fleece, over leg wraps bound with thongs and soft felt boots.",
    "tags": ["rugged", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 11411, top=9.8, length=9)
    s.paint(lambda f: fur(sub(f, 0, f.h - 2, f.w, 2), "S", 11412, 3))
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        wraps(leg.strip, 6, 9, "S", 2)
        for face in pants.sides:
            wraps(face, 6, 9, "S", 2)
            for y in (7, 9):
                face.set(1, y, "L2")                                     # binding thongs
    shoes(g, "turnshoe", "P", 1)
