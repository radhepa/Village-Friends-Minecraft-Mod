"""Astrolabe Reader's Night Skirt: a floor-length skirt the colour of the night sky, embroidered with
constellations, bright stars joined by fine threads, above a hem band of tiny gold stars."""
from kit_female import shoes, skirt, trim
from paint import line

META = {
    "name": "Astrolabe Reader's Night Skirt",
    "gender": "female",
    "description": "A night-dark floor-length skirt embroidered with constellations, bright stars joined by fine threads, over a gold-starred hem.",
    "tags": ["scholarly", "whimsical", "skirt", "long_skirt"],
}

# Little star-pictures for each panel: points joined in order.
FRONT = [[(1, 2), (3, 1), (5, 3), (4, 5)], [(6, 7), (8, 6), (8, 9), (6, 10), (5, 8)]]
BACK = [[(1, 6), (2, 3), (4, 4), (6, 2), (8, 3)], [(2, 9), (4, 8), (6, 10)]]


def constellations(face, shapes):
    for pts in shapes:
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            line(face, x0, y0, x1, y1, "K3")
        for i, (x, y) in enumerate(pts):
            face.set(x, y, "S4" if i % 2 == 0 else "M4")


def build(g):
    s = skirt(g, "K", "plain", 55311, base=2, top=9.8, length=12, back_length=12, flare=5, folds=False, gather=False)
    for face in s.faces:
        face.hline(0, face.w - 1, 0, "K3"), face.hline(0, face.w - 1, 1, "K1")
    constellations(s.front.front, FRONT)
    constellations(s.back.back, BACK)
    for box in (s.right, s.left):
        outer = box.right if box is s.right else box.left
        outer.set(2, 3, "S4"), outer.set(1, 7, "M4")
    for face in s.faces:
        trim(face, face.h - 2, "dots", "M3")
        face.hline(0, face.w - 1, face.h - 1, "K1")
    shoes(g, "pointed", "K", 2)
