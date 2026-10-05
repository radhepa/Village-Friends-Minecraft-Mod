"""Drawstring Trousers & Wrap Boots: loose trousers with a drawstring waist, tucked into wrapped soft boots."""
from kit import SIDES, footwear, legs, waistband
from paint import solid

META = {
    "name": "Drawstring Trousers",
    "description": "Loose linen trousers with a drawstring waist, tucked into soft boots bound with straps.",
    "tags": ["casual", "simple", "relaxed"],
}


def build(g):
    for leg in legs(g, "S", "weave", 2001, rows=(0, 7), crease=False):
        for face in leg.sides:
            face.vline(1, 1, 6, "S1")
    body = waistband(g, "S", "weave", 2002)
    for face in body.sides:
        for x in range(face.w):
            face.set(x, 9, "S1" if x % 2 else "S3")
    for i, x in enumerate((-.6, .6)):
        end = g.piece(f"waist_drawstring_{i}", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(x, 9.8, -2.6), rotation=(0, 0, -10 + 20 * i))
        solid(end, "A", "plain", 2003, 2, edge=False)
    footwear(g, "boot", top=8)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            for y in (9,):
                for x in range(face.w):
                    if (x + y) % 2 == 0:
                        face.set(x, y, "L1")
