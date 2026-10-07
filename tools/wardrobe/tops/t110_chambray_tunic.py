"""Chambray Tunic: plain long-sleeved pullover tunic in light chambray blue."""
from kit_casual import plain_tunic

META = {
    "name": "Chambray Tunic",
    "gender": "male",
    "description": "A plain long-sleeved pullover tunic in light chambray blue.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    plain_tunic(g, "D", 3, seed=11001)
