"""Nun's Habit Skirt: the floor-length lower habit in deep plain wool, folded in long still pleats."""
from kit_female import pleats, shoes, skirt

META = {
    "name": "Nun's Habit Skirt",
    "gender": "female",
    "description": "The habit's floor-length skirt in plain dark wool, hanging in long still folds over black shoes.",
    "tags": ["holy", "robe", "skirt", "long_skirt"],
    "locked_to": "tf016_nuns_habit",
}


def build(g):
    s = skirt(g, "P", "weave", 11611, base=1, top=9.8, length=12, back_length=13, folds=False, gather=False)
    for f in s.wide_faces:
        pleats(f, "P", 1, 3, y0=1, lit=True)
    s.hem("P0")
    shoes(g, "shoe", "K", 2)
