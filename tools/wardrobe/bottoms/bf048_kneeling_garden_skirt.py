"""Kneeling Garden Skirt: a mid-calf skirt with earth-stained knees and a turned hem, over wooden clogs."""
from kit_female import shoes, skirt, splotch, sub

META = {
    "name": "Kneeling Garden Skirt",
    "gender": "female",
    "description": "A mid-calf work skirt with earth-stained knees from the beds, a turned-up hem and carved wooden clogs.",
    "tags": ["work", "casual", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 14811, top=9.8, length=9)
    splotch(sub(s.front.front, 0, 4, 10, 3), "L2", 14812, count=3, size=2)
    splotch(sub(s.front.front, 0, 4, 10, 3), "L1", 14813, count=2, size=1)
    for face in s.faces:
        face.hline(0, face.w - 1, face.h - 2, "P3"), face.hline(0, face.w - 1, face.h - 1, "P1")
    shoes(g, "clog", "L", 3)
