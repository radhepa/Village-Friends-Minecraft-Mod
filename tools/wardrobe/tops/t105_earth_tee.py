"""Earth Tee: plain crew-neck tee in warm earth brown."""
from kit_casual import plain_tee

META = {
    "name": "Earth Tee",
    "gender": "male",
    "description": "A plain crew-neck tee in warm earth brown.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    plain_tee(g, "L", 3, seed=10501)
