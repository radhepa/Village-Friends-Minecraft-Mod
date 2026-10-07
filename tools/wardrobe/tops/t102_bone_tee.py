"""Bone Tee: plain crew-neck tee in pale bone."""
from kit_casual import plain_tee

META = {
    "name": "Bone Tee",
    "gender": "male",
    "description": "A plain crew-neck tee in pale bone.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    plain_tee(g, "S", 3, seed=10201)
