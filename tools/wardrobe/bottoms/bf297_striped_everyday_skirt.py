"""Striped Everyday Skirt: a skirt of broad upright stripes in two colors, falling in folds to a dark bound hem, over pointed shoes."""
from kit_female import shoes, skirt
from paint import k

META = {
    "name": "Striped Everyday Skirt",
    "gender": "female",
    "description": "A skirt woven in broad upright stripes of two colors, falling in soft folds to a dark bound hem, over pointed shoes.",
    "tags": ["casual", "simple", "skirt", "long_skirt"],
}


def stripe_face(face):
    for y in range(face.h):
        for x in range(face.w):
            band = ((x + face.x0) // 2) % 2
            fold = (x + face.x0) % 4 == 3 and 2 <= y < face.h - 2
            face.set(x, y, k("S", 2 if fold else 3) if band else k("P", 1 if fold else 2))
        if y == 1:
            for x in range(face.w):
                if x % 2:
                    face.set(x, y, k("S" if ((x + face.x0) // 2) % 2 else "P", 1))
    face.hline(0, face.w - 1, face.h - 1, "P0")


def build(g):
    s = skirt(g, "P", "weave", 60460, top=9.8, length=11, flare=6, gather=False, folds=False)
    s.paint(stripe_face)
    shoes(g, "pointed", "L", 1)
