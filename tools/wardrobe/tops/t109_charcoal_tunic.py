"""Charcoal Tunic: plain long-sleeved pullover tunic in charcoal."""
from kit_casual import plain_tunic

META = {
    "name": "Charcoal Tunic",
    "gender": "male",
    "description": "A plain long-sleeved pullover tunic in charcoal.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    plain_tunic(g, "K", 3, seed=10901)
