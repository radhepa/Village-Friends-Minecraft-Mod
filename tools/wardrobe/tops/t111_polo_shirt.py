"""Polo Shirt: a pique-knit polo with a two-button placket, collar points and ribbed cuffs."""
from kit_casual import collar_points, short_sleeves, shirt_body

META = {
    "name": "Polo Shirt",
    "gender": "male",
    "description": "A pique-knit polo with a two-button placket, a soft collar and ribbed sleeve cuffs.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    body = shirt_body(g, "P", 2, "weave", 11101)
    f = body.front
    f.clear(3, 0), f.clear(4, 0)
    for y in range(1, 4):
        f.set(4, y, "P3"), f.set(3, y, "P1")
    f.set(4, 2, "S4"), f.set(4, 3, "S4")
    body.back.hline(1, 6, 0, "P3")
    short_sleeves(g, "P", 2, "weave", 11102, length=4, band="P3")
    for side in ("right", "left"):
        g.part(f"{side}_arm").strip.hline(0, 15, 3, "P1")
    collar_points(g, "P", 3, spread=22)
