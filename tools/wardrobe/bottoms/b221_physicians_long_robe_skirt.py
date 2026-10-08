"""Physician's Long Robe Skirt: ankle-length robe skirts slit up the front over a pale lining, hooked shut at the top, with soft round-toed shoes."""
from kit import waistband
from kit_male import skirt_panels
from kit_m05 import hose, soft_shoes

META = {
    "name": "Physician's Long Robe Skirt",
    "gender": "male",
    "description": "Ankle-length robe skirts slit up the front to the knee over a pale lining, hooked shut above with three brass hooks, over close hose and soft round-toed shoes.",
    "tags": ["robe", "scholarly"],
    "rejects": ["armor"],
}


def build(g):
    hose(g, "P", 1, "weave", 35020)
    waistband(g, "P", "velvet", 35021)
    soft_shoes(g, "L", 2, top=10, strap="L3")
    front, back, sides = skirt_panels(g, "robe", 12, "P", "velvet", 35022, top=10.6, side_len=11)
    # The front slit: lining shows between two dark edges, hooks above it.
    for y in range(5, 12):
        front.set(4, y, "S3" if y < 11 else "S2")
        front.set(3, y, "P1"), front.set(5, y, "P3")
    front.vline(4, 0, 4, "P1")
    for y in (0, 2, 4):
        front.set(4, y, "M3")
    for x in (1, 7):
        front.vline(x, 2, 11, "P1")
    for x in (2, 4, 6):
        back.vline(x, 1, 11, "P1")
    for face in (front, back):
        face.hline(0, 8, 11, "P1")
    for box in sides:
        for face in box.sides:
            face.hline(0, face.w - 1, face.h - 1, "P1")
