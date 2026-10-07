"""Black Tee: plain crew-neck tee in near-black ink."""
from kit_casual import plain_tee

META = {
    "name": "Black Tee",
    "gender": "male",
    "description": "A plain crew-neck tee in near-black ink.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    plain_tee(g, "K", 3, seed=10401)
