"""Bright Tee: plain crew-neck tee in the palette's bright accent."""
from kit_casual import plain_tee

META = {
    "name": "Bright Tee",
    "gender": "male",
    "description": "A plain crew-neck tee in the palette's bright accent.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    plain_tee(g, "A", 2, seed=10301)
