"""Prospector's Creek Skirt: a knee-length skirt hitched short for wading, dark and wet up to a rippled
waterline, stockings rolled down to the ankle and stout laced ankle boots."""
from kit import SIDES
from kit_female import leg_ring_fold, shoes, skirt, waist_belt
from paint import k
from wardrobe import shade

META = {
    "name": "Prospector's Creek Skirt",
    "gender": "female",
    "description": "A knee-length skirt hitched short for wading, soaked dark up to a rippled waterline, "
                   "stockings rolled down to the ankles and stout laced boots.",
    "tags": ["work", "rugged", "skirt"],
}


def wet(face, rows=3):
    """The soaked band: darker cloth below a rippled waterline, one lighter tide mark along it."""
    for x in range(face.w):
        top = face.h - rows - (1 if (x + face.x0) % 4 in (1, 2) else 0)
        for y in range(top, face.h):
            cur = face.get(x, y)
            if cur:
                face.set(x, y, shade(cur, -1))
        face.set(x, top - 1, k(face.get(x, top)[0], 3))


def build(g):
    s = skirt(g, "P", "weave", 57921, top=9.8, length=7, side_length=6, flare=7, folds=False)
    s.paint(lambda f: wet(f, 3))
    s.hem("P0")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for y in range(4, 9):
            leg.strip.hline(0, leg.strip.w - 1, y, None)            # bare calves
    for box in leg_ring_fold(g, "stocking_roll", 8.4, role="S", base=2, size=5):
        box.front.set(1, 1, "S1")
    shoes(g, "ankle", "L", 2, top=9)
    waist_belt(g, "waist_belt", 9.4, role="L", height=1)
