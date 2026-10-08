"""Ankle-Length Wool Skirt: a plain wool skirt to the ankle with two stitched tucks above the hem, over strapped shoes."""
from kit import SIDES
from kit_female import shoes, skirt, stockings_row

META = {
    "name": "Ankle-Length Wool Skirt",
    "gender": "female",
    "description": "A plain wool skirt to the ankle with two stitched tucks above a bound hem, over buckled strap shoes.",
    "tags": ["casual", "simple", "skirt", "long_skirt"],
}


def tucks(face):
    h = face.h
    for y in (h - 6, h - 3):
        face.hline(0, face.w - 1, y, "P3")                              # the lit fold of each tuck
        face.hline(0, face.w - 1, y + 1, "P1")                          # and the shadow it casts
    face.hline(0, face.w - 1, h - 1, "P0")


def build(g):
    s = skirt(g, "P", "weave", 60020, top=9.8, length=11, flare=5)
    s.paint(tucks)
    stockings_row(g, "S", 9, 9, base=3)
    shoes(g, "shoe", "L", 2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 9, "L1")                          # the ankle strap over the stocking
        outer = pants.right if side == "right" else pants.left
        outer.set(1, 9, "M3")
