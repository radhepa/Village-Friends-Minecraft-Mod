"""Tooled Leather Panel Skirt: a wool skirt with a stamped leather panel laced into the front, over laced ankle boots."""
from kit_female import lozenges, shoes, skirt

META = {
    "name": "Tooled Leather Panel Skirt",
    "gender": "female",
    "description": "A wool skirt with a stamped and tooled leather panel laced down the front, over laced ankle boots.",
    "tags": ["rugged", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 14411, top=9.8, length=11, folds=False)
    f = s.front.front
    lozenges(f, 3, 1, 4, 10, "L2", "L3", "L1")
    for y in range(1, 11):
        f.set(2, y, "L1" if y % 2 else "M3")                          # laced edges
        f.set(7, y, "L1" if y % 2 else "M3")
    for x in (1, 8):
        f.vline(x, 3, 9, "P1")
    s.back.back.vline(3, 3, 9, "P1"), s.back.back.vline(6, 3, 9, "P1")
    s.hem("P0")
    shoes(g, "ankle", "L", 2)
