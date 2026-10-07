"""Tipped Polo: a pale polo with accent stripes tipping the collar and the sleeve bands."""
from kit_casual import collar_points, short_sleeves, shirt_body

META = {
    "name": "Tipped Polo",
    "gender": "male",
    "description": "A pale pique polo; thin accent stripes tip its collar and sleeve bands.",
    "tags": ["casual", "modern", "tailored"],
    "tucked": True,
}


def build(g):
    body = shirt_body(g, "S", 3, "weave", 11201, hem=False)
    f = body.front
    f.clear(3, 0), f.clear(4, 0)
    for y in range(1, 4):
        f.set(4, y, "S4"), f.set(3, y, "S2")
    f.set(4, 2, "M3"), f.set(4, 3, "M3")
    body.back.hline(1, 6, 0, "A2")
    short_sleeves(g, "S", 3, "weave", 11202, length=4, band="A2")
    collar_points(g, "S", 4, spread=22)
    for piece in g.pieces:   # accent tipping along each collar point
        if piece.id.endswith("collar_point"):
            piece.box.front.hline(0, 1, 1, "A2")
