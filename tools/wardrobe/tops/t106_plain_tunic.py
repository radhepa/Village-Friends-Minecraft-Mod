"""Plain Tunic: plain long-sleeved pullover tunic in the outfit's main color."""
from kit_casual import plain_tunic

META = {
    "name": "Plain Tunic",
    "gender": "male",
    "description": "A plain long-sleeved pullover tunic in the outfit's main color.",
    "tags": ["casual", "modern", "simple"],
    "covers_waist": True,
}


def build(g):
    plain_tunic(g, "P", 2, seed=10601)
