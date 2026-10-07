"""Houppelande Train Skirt: the gown's floor-length pleated skirts, a band of fur at the hem, and pointed black shoes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import fur_face, skirt_panels

META = {
    "name": "Houppelande Train Skirt",
    "gender": "male",
    "description": "The houppelande's floor-length skirts in deep organ pleats, a band of fur at the hem, over pointed black shoes.",
    "tags": ["fancy", "robe"],
    "locked_to": "t62_magnates_floor_houppelande",
}


def build(g):
    legs(g, "P", "velvet", 6211, rows=(0, 9), crease=False)
    waistband(g, "P", "velvet", 6212)
    footwear(g, "shoe", top=10, role="K", base=1, sole="K0")
    front, back, sides = skirt_panels(g, "gown", 12, "P", "velvet", 6213, top=10.4, side_len=11)
    for face in (front, back):
        for x in range(0, 9, 2):
            face.vline(x, 0, 10, "P1")                                    # organ pleats
        for x in range(1, 9, 2):
            face.vline(x, 1, 10, "P3")
        fur_face(face, "S", 6214, 3, rows=range(11, 12))
    for box in sides:
        for face in box.sides:
            fur_face(face, "S", 6215, 3, rows=range(face.h - 1, face.h))
