"""Cargo Pants: relaxed pants with bellows pockets on both thighs and boots."""
from kit_casual import shoes, side_pocket, trousers

META = {
    "name": "Cargo Pants",
    "gender": "male",
    "description": "Relaxed twill pants with flapped bellows pockets on both thighs, over ankle boots.",
    "tags": ["casual", "modern", "rugged"],
}


def build(g):
    trousers(g, "P", 1, "twill", 11201)
    for side in ("right", "left"):
        side_pocket(g, side, "P", 1, y=3.4)
    shoes(g, "boot")
