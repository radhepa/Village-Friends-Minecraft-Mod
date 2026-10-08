"""Anchoress's Plain Robe Skirt: the coarse robe's floor-length skirt with a short trailing back, a few
long still folds, darned patches, a frayed hem and bare feet in thong sandals."""
from kit_female import pleats, shoes, skirt
from paint import fabric

META = {
    "name": "Anchoress's Plain Robe Skirt",
    "gender": "female",
    "description": "The coarse robe's floor-length skirt in long still folds, darned and frayed at the hem, over bare thong sandals.",
    "tags": ["holy", "robe", "simple", "skirt", "long_skirt"],
    "locked_to": "tf163_anchoress_cowled_robe",
}


def darn(face, x, y, w, h):
    """A sewn-on patch: a lighter square of cloth inside a ring of dark stitching."""
    fabric(face, "P", "plain", 55103 + x * 7 + y, 2, x, y, w, h)
    for xx in range(x - 1, x + w + 1):
        face.set(xx, y - 1, "P0"), face.set(xx, y + h, "P0")
    for yy in range(y, y + h):
        face.set(x - 1, yy, "P0"), face.set(x + w, yy, "P0")


def frayed(face):
    for x in range(face.w):
        face.set(x, face.h - 1, "P0" if x % 3 else "P2")
        if x % 4 == 1:
            face.set(x, face.h - 2, "P0")


def build(g):
    s = skirt(g, "P", "plain", 55101, base=1, top=9.8, length=12, back_length=13, folds=False, gather=False)
    for face in s.wide_faces:
        pleats(face, "P", 1, 4, y0=2, lit=False)
        face.hline(0, face.w - 1, 0, "P2"), face.hline(0, face.w - 1, 1, "P0")
    darn(s.front.front, 6, 6, 2, 2)
    darn(s.back.back, 2, 8, 3, 2)
    s.paint(frayed)
    shoes(g, "sandal", "L", 2)
