"""Bright Tunic: plain long-sleeved pullover tunic in the palette's bright accent."""
from kit_casual import plain_tunic

META = {
    "name": "Bright Tunic",
    "gender": "male",
    "description": "A plain long-sleeved pullover tunic in the palette's bright accent.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    plain_tunic(g, "A", 2, seed=10801)
