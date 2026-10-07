"""Linen Drawstring Pants: loose pale linen pants with a drawstring waist."""
from kit_casual import shoes, trousers
from paint import solid

META = {
    "name": "Linen Drawstring Pants",
    "gender": "male",
    "description": "Loose pale linen pants gathered by a drawstring, over canvas shoes.",
    "tags": ["casual", "modern", "relaxed"],
}


def build(g):
    trousers(g, "S", 3, "weave", 11501, loops=False, overlay=True)
    body = g.part("body")
    for face in body.sides:
        for x in range(face.w):
            face.set(x, 9, "S2" if x % 2 else "S4")
    for i, x in enumerate((-.6, .6)):
        end = g.piece(f"waist_drawstring_{i}", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(x, 9.8, -2.6),
                      rotation=(0, 0, -10 + 20 * i))
        solid(end, "S", "plain", 11502, 4, edge=False)
    shoes(g, "canvas")
