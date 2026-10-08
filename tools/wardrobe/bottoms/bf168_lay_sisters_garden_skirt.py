"""Lay Sister's Garden Skirt: a calf-length skirt of undyed wool with a deep hem guard of coarse sacking
sewn on against the soil, earth-marked where she kneels, over cloth shin wraps and wooden clogs."""
from kit import SIDES
from kit_female import shoes, skirt, wraps

META = {
    "name": "Lay Sister's Garden Skirt",
    "gender": "female",
    "description": "A calf-length undyed skirt with a deep sacking hem guard, earth-marked at the knees, over shin wraps and wooden clogs.",
    "tags": ["work", "rugged", "skirt", "simple"],
}


def sacking(face, y0):
    """Coarse sacking from row y0 down: a heavy diagonal weave below a stitched seam."""
    for y in range(y0, face.h):
        for x in range(face.w):
            face.set(x, y, "L2" if (x + y) % 3 == 0 else "L3")
    face.hline(0, face.w - 1, y0, "L1")
    face.hline(0, face.w - 1, face.h - 1, "L1")


def knee_marks(face):
    """Earth worked into the cloth where she kneels: two soft smudges at knee height."""
    for x0 in (1, face.w - 4):
        face.hline(x0, x0 + 2, 3, "L2"), face.hline(x0 + 1, x0 + 2, 4, "L1")


def build(g):
    s = skirt(g, "S", "plain", 55251, base=1, top=9.8, length=9, back_length=9, flare=5, folds=True, gather=False)
    s.paint(lambda face: sacking(face, face.h - 3))
    knee_marks(s.front.front)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        wraps(leg.strip, 6, 9, role="S", base=2, step=4)
    shoes(g, "clog", "L", 2)
