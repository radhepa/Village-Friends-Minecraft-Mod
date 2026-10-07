"""Hitched Work Skirt: a skirt hitched up in front into the belt, over knitted leggings and laced ankle boots."""
from kit_female import hose, shoes, skirt, waist_belt

META = {
    "name": "Hitched Work Skirt",
    "gender": "female",
    "description": "A sturdy skirt hitched up into the belt at the front for field work, over knitted leggings and ankle boots.",
    "tags": ["work", "sturdy", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 10311, top=9.6, length=8, back_length=12, side_length=10, flare=4, folds=False)
    f = s.front.front
    # The front corners are caught up into the belt: the hem curves up at both sides, the lining shows.
    for x, depth in ((0, 4), (1, 3), (2, 2), (3, 1), (6, 1), (7, 2), (8, 3), (9, 4)):
        for y in range(8 - depth, 8):
            f.set(x, y, "S3" if y == 8 - depth else "S2")
    for x in (2, 7):
        f.vline(x, 1, 7 - (3 if x in (0, 9) else 2), "P1")
    f.vline(4, 1, 6, "P1"), f.vline(5, 2, 6, "P3")
    f.hline(4, 5, 7, "P1")
    back = s.back.back
    for x in (1, 4, 7):
        back.vline(x, 2, 10, "P1")
        back.vline(x + 1, 3, 9, "P3")
    back.hline(0, 9, 11, "P0")
    hose(g, "S", rows=(5, 9), base=2, texture="rib")
    shoes(g, "ankle", "L", 2, top=9)
    waist_belt(g, "waist_belt", 9.2, height=1)
