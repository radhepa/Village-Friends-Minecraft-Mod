"""Cream Tunic: plain long-sleeved pullover tunic in soft cream."""
from kit_casual import plain_tunic

META = {
    "name": "Cream Tunic",
    "gender": "male",
    "description": "A plain long-sleeved pullover tunic in soft cream.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    plain_tunic(g, "S", 3, seed=10701)
