"""Checkered Weave Skirt: a weaver's own checked wool skirt with a fringed woven sash and low leather shoes."""
from kit_female import shoes, skirt, stockings_row, waist_belt
from paint import solid

META = {
    "name": "Checkered Weave Skirt",
    "gender": "female",
    "description": "A home-woven checked wool skirt, a fringed sash knotted at the hip and low leather shoes.",
    "tags": ["casual", "skirt"],
}


def weave_check(face):
    """A home-woven check: dark bands every third thread, a pale overcheck every sixth."""
    for y in range(face.h):
        for x in range(face.w):
            bx, by = (x + face.x0) % 3 == 0, y % 3 == 0
            key = "P0" if bx and by else "P1" if bx or by else "P2"
            if (x + face.x0) % 6 == 3 and y % 6 == 3:
                key = "S3"
            elif ((x + face.x0) % 6 == 3 and not by) or (y % 6 == 3 and not bx):
                key = "P3"
            face.set(x, y, key)


def build(g):
    s = skirt(g, "P", "weave", 10411, top=9.8, length=11, folds=False, gather=False)
    s.paint(weave_check)
    for f in s.faces:
        f.hline(0, f.w - 1, 0, "P3"), f.hline(0, f.w - 1, f.h - 1, "P0")
    stockings_row(g, "S", 9)
    shoes(g, "shoe", "L", 2)
    sash = waist_belt(g, "waist_sash", 9.4, role="A", base=2, height=1, buckle=None, texture="plain")
    for face in sash.sides:
        for x in range(0, face.w, 2):
            face.set(x, 0, "A3")
    for i, (x, length) in enumerate(((3.0, 5), (3.8, 4))):
        tail = g.piece(f"waist_sash_tail_{i}", "TORSO", (-.5, 0, 0), (1, length, 1), pivot=(x, 9.6, -3.15), motion="flap_front")
        solid(tail, "A", "plain", 10412 + i, 2)
        tail.strip.hline(0, tail.strip.w - 1, length - 1, "S3")
