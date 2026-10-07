"""Everyday Chinos: plain chinos in the outfit's main color, with canvas shoes."""
from kit_casual import shoes, trousers

META = {
    "name": "Everyday Chinos",
    "gender": "male",
    "description": "Plain flat-front chinos in the outfit's main color, worn with canvas shoes.",
    "tags": ["casual", "modern", "simple"],
}


def build(g):
    legs, body = trousers(g, "P", 2, "twill", 10901, crease=True)
    for leg, x in zip(legs, (0, 3)):
        leg.front.set(x, 0, "P1"), leg.front.set(1 if x == 0 else 2, 1, "P1")
    shoes(g, "canvas")
