"""Deacon's Alb Hem: the white alb falling below the dalmatic to the ankle, its hem worked in openwork lace, over black slippers."""
from kit import legs, waistband
from kit_male import skirt_panels
from kit_m05 import soft_shoes

META = {
    "name": "Deacon's Alb Hem",
    "gender": "male",
    "description": "The white alb falling below the dalmatic to the ankle, its deep hem worked in pale openwork lace, over soft black slippers.",
    "tags": ["holy", "robe"],
    "locked_to": "t224_deacons_dalmatic",
}


def lace(face, y0):
    """Openwork lace: a drawn edge, then two offset rows of pierced holes."""
    face.hline(0, face.w - 1, y0, "S1")
    for x in range(face.w):
        face.set(x, y0 + 1, "S4" if x % 2 else "S1")
        face.set(x, y0 + 2, "S1" if x % 2 else "S4")


def build(g):
    legs(g, "S", "weave", 35140, base=3, rows=(0, 9), crease=False)
    waistband(g, "S", "weave", 35141, base=3)
    soft_shoes(g, "K", 1, top=10, sole="K0", cuff="K2")
    front, back, sides = skirt_panels(g, "alb", 12, "S", "weave", 35142, base=3, top=10.6, side_len=11)
    for face in (front, back):
        for x in (2, 6):
            face.vline(x, 1, 8, "S2")
        lace(face, 9)
    for box in sides:
        for face in box.sides:
            lace(face, face.h - 3)
