"""Patchwork Skirt: a cheerful skirt pieced from squares of every cloth to hand, with running stitches and turnshoes."""
from kit_female import shoes, skirt

META = {
    "name": "Patchwork Skirt",
    "gender": "female",
    "description": "A cheerful skirt pieced from squares of every cloth to hand, stitched with running seams, and turnshoes.",
    "tags": ["whimsical", "casual", "skirt", "long_skirt"],
}

PATCHES = ["P2", "S3", "A2", "P3", "L3", "S2", "P1", "A3"]


def patchwork(face):
    for y in range(face.h):
        for x in range(face.w):
            px, py = (x + face.x0) // 3, (y + 1) // 3
            key = PATCHES[(px * 3 + py * 5) % len(PATCHES)]
            if (x + face.x0) % 3 == 0 or (y + 1) % 3 == 0:
                key = key if (x + y) % 2 else "K2"                    # running stitches on the seams
            face.set(x, y, key)


def build(g):
    s = skirt(g, "P", "weave", 14611, top=9.8, length=11, folds=False, gather=False)
    s.paint(patchwork)
    for face in s.faces:
        face.hline(0, face.w - 1, 0, "P1"), face.hline(0, face.w - 1, face.h - 1, "P0")
    shoes(g, "turnshoe", "L", 2)
