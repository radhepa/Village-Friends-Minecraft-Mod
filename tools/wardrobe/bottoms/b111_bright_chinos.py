"""Bright Chinos: chinos in the palette's bright accent, cuffed short over the shoes."""
from kit_casual import rolled_hems, shoes, trousers

META = {
    "name": "Bright Chinos",
    "gender": "male",
    "description": "Chinos in the palette's bright accent, with short turn-ups over canvas shoes.",
    "tags": ["casual", "modern", "simple"],
}


def build(g):
    trousers(g, "A", 2, "twill", 11101, end=8)
    rolled_hems(g, "A", 3, y=7.4)
    shoes(g, "canvas", top=9)
