"""Cantor's Cassock Skirt: a dark ankle-length cassock skirt with a deep box pleat before and behind, faced at the hem in colour, over tongued black shoes."""
from kit import SIDES, waistband
from kit_male import skirt_panels
from kit_m05 import hose, soft_shoes

META = {
    "name": "Cantor's Cassock Skirt",
    "gender": "male",
    "description": "A dark ankle-length cassock skirt with one deep box pleat before and behind and a coloured facing turned up at the hem, over close hose and tongued black shoes.",
    "tags": ["robe", "holy"],
    "rejects": ["armor"],
}


def box_pleat(face, x, y0, y1):
    face.vline(x - 1, y0, y1, "P0"), face.vline(x, y0, y1, "P2"), face.vline(x + 1, y0, y1, "P0")
    face.set(x, y0, "P3")


def build(g):
    hose(g, "P", 1, "smooth", 35180)
    waistband(g, "P", "smooth", 35181, base=1)
    soft_shoes(g, "K", 2, top=10, sole="K0")
    for side in SIDES:
        g.part(f"{side}_pants").front.vline(1 if side == "right" else 2, 9, 10, "K3")   # the tongue
    front, back, sides = skirt_panels(g, "cassock", 12, "P", "smooth", 35182, base=1, top=10.6, side_len=11)
    for face in (front, back):
        box_pleat(face, 4, 1, 10)
        face.hline(0, 8, 10, "A3"), face.hline(0, 8, 11, "A1")             # turned-up facing
        face.set(4, 10, "A2"), face.set(4, 11, "A0")
    for box in sides:
        for face in box.sides:
            face.hline(0, face.w - 1, face.h - 2, "A3")
            face.hline(0, face.w - 1, face.h - 1, "A1")
