"""Seam-Banded Trousers: sober wool trousers with a narrow embroidered band down each outer seam, and soft turnshoes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import embroider

META = {
    "name": "Seam-Banded Trousers",
    "gender": "male",
    "description": "Sober wool trousers with a narrow embroidered vine running down each outer seam and round the waist, over soft turnshoes.",
    "tags": ["casual", "tailored"],
}


def build(g):
    legs(g, "P", "weave", 5511, rows=(0, 9), crease=False)
    body = waistband(g, "P", "weave", 5512)
    footwear(g, "turnshoe", top=10, base=2)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        outer = leg.right if side == "right" else leg.left
        for y in range(10):
            outer.set(1, y, "A2" if y % 3 else "A3")
            outer.set(2, y, "A1" if y % 3 == 1 else "A2")
        leg.front.vline(1 if side == "right" else 2, 1, 9, "P1")
    for face in body.sides:
        embroider(face, 10, "dots", "A3")
