"""Abbess's Habit Skirt: the white habit's floor-length skirt in still folds, with a dark band at the hem."""
from kit_female import pleats, shoes, skirt

META = {
    "name": "Abbess's Habit Skirt",
    "gender": "female",
    "description": "The white habit's floor-length skirt, falling in still folds to a dark hem band, over black shoes.",
    "tags": ["holy", "robe", "skirt", "long_skirt"],
    "locked_to": "tf027_abbess_habit",
}


def build(g):
    s = skirt(g, "S", "weave", 12711, base=3, top=9.8, length=12, back_length=13, folds=False, gather=False)
    for face in s.wide_faces:
        pleats(face, "S", 3, 3, y0=1, lit=False)
    s.band(0, "line", "P1", from_bottom=True)
    s.band(1, "line", "P1", from_bottom=True)
    shoes(g, "shoe", "K", 2)
