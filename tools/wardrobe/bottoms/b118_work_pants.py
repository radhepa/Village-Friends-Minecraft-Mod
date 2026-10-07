"""Work Pants: tough duck-canvas work pants with double knees and triple stitching."""
from kit_casual import leather_belt, shoes, trousers

META = {
    "name": "Work Pants",
    "gender": "male",
    "description": "Tough duck-canvas work pants with double knees, triple stitching and work boots.",
    "tags": ["casual", "modern", "work", "rugged"],
}


def build(g):
    legs, body = trousers(g, "L", 3, "twill", 11801)
    for leg in legs:
        for y in (3, 8):
            leg.front.hline(0, 3, y, "L1")
        for y in range(4, 8):
            leg.front.set(0, y, "L2"), leg.front.set(3, y, "L2")
        outer = leg.right if leg is legs[0] else leg.left
        outer.vline(1, 0, 9, "S2")   # triple-stitched outseam
    leather_belt(g, "L", 1)
    shoes(g, "boot")
