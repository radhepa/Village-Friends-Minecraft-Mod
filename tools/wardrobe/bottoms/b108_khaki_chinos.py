"""Khaki Chinos: flat-front chinos in pale khaki with a leather belt and loafers."""
from kit_casual import leather_belt, shoes, trousers

META = {
    "name": "Khaki Chinos",
    "gender": "male",
    "description": "Flat-front chinos in pale khaki, slant pockets, a leather belt and plain loafers.",
    "tags": ["casual", "modern", "tailored"],
}


def build(g):
    legs, body = trousers(g, "S", 2, "twill", 10801, crease=True)
    for leg, x in zip(legs, (0, 3)):
        leg.front.set(x, 0, "S1"), leg.front.set(1 if x == 0 else 2, 1, "S1")   # slant pocket
    leather_belt(g)
    shoes(g, "leather")
