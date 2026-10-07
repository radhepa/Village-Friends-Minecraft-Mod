"""Corduroy Pants: soft wide-wale cords in warm brown."""
from kit_casual import shoes, trousers

META = {
    "name": "Corduroy Pants",
    "gender": "male",
    "description": "Soft wide-wale corduroy trousers in warm brown, with leather shoes.",
    "tags": ["casual", "modern", "simple"],
}


def build(g):
    trousers(g, "L", 3, "rib", 11401)
    shoes(g, "leather")
