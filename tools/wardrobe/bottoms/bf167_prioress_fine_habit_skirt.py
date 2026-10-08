"""Prioress's Fine Habit Skirt: the habit's floor-length skirt in fine dark wool, laid in crisp wide box
pleats with a short train behind, bound at the hem and worn over soft pointed shoes."""
from kit_female import shoes, skirt

META = {
    "name": "Prioress's Fine Habit Skirt",
    "gender": "female",
    "description": "The habit's skirt in fine dark wool, laid in crisp wide box pleats with a short train, over soft pointed shoes.",
    "tags": ["holy", "robe", "fancy", "skirt", "long_skirt"],
    "locked_to": "tf167_prioress_rosary_girdle_habit",
}


def box_pleats(face):
    """Wide box pleats: a lit pleat face, its two shaded folds, repeated every five threads."""
    for x in range(face.w):
        phase = x % 5
        key = "P0" if phase == 0 else "P2" if phase in (2, 3) else "P1"
        face.vline(x, 2, face.h - 2, key)


def build(g):
    s = skirt(g, "P", "velvet", 55231, base=1, top=9.8, length=12, back_length=14, flare=6, folds=False, gather=False)
    s.paint(box_pleats, sides=False)
    for face in s.faces:
        face.hline(0, face.w - 1, 0, "P2"), face.hline(0, face.w - 1, 1, "P0")
    s.hem("K1")
    shoes(g, "pointed", "K", 2)
