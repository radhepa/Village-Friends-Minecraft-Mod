"""Embroidered Hem Trousers: loose trousers with a broad embroidered band at the hem and waist, soft boots."""
from kit import SIDES, footwear, legs, waistband

META = {
    "name": "Embroidered Hem Trousers",
    "description": "Loose trousers with broad embroidered bands at the hem and waist, over soft boots.",
    "tags": ["casual", "fancy"],
}


def build(g):
    legs(g, "P", "weave", 3001, rows=(0, 9), crease=False)
    body = waistband(g, "P", "weave", 3002)
    for face in body.sides:
        for x in range(face.w):
            face.set(x, 10, "A2" if x % 2 else "M3")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for x in range(leg.strip.w):
            leg.strip.set(x, 7, "A3")
            leg.strip.set(x, 8, "M3" if x % 3 == 1 else "A2")
            leg.strip.set(x, 9, "A1")
    footwear(g, "turnshoe", top=10)
