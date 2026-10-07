"""Plain Tee: plain crew-neck tee in the outfit's main color."""
from kit_casual import plain_tee

META = {
    "name": "Plain Tee",
    "gender": "male",
    "description": "A plain crew-neck tee in the outfit's main color.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    plain_tee(g, "P", 2, seed=10101)
