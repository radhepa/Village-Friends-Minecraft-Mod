"""Pleated Bases Skirt: a knight's short pleated cloth bases flaring to the knee over hose, hemmed in accent, with ankle boots."""
from kit import SIDES, footwear, legs, waistband
from kit_male import skirt_panels

META = {
    "name": "Pleated Bases Skirt",
    "gender": "male",
    "description": "A knight's short pleated cloth bases flaring to the knee over close hose, hemmed in accent, with ankle boots.",
    "tags": ["martial", "fancy"],
}


def build(g):
    legs(g, "S", "weave", 7311, base=2, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 7312)
    footwear(g, "boot", top=9, base=2)
    front, back, sides = skirt_panels(g, "bases", 6, "P", "weave", 7313, top=10.4, side_len=5)
    for face in (front, back):
        for x in range(face.w):
            face.vline(x, 1, 4, "P1" if x % 2 else "P3")                 # deep pleats
        face.hline(0, 8, 0, "P2"), face.hline(0, 8, 5, "A2")
    for box in sides:
        for face in box.sides:
            face.hline(0, face.w - 1, face.h - 1, "A2")
