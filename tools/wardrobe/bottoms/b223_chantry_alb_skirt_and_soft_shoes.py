"""Chantry Alb Skirt and Soft Shoes: the alb's ankle-length linen skirts with embroidered apparels at the hem, over soft dark shoes."""
from kit import legs, waistband
from kit_male import skirt_panels
from kit_m05 import soft_shoes

META = {
    "name": "Chantry Alb Skirt and Soft Shoes",
    "gender": "male",
    "description": "The alb's ankle-length linen skirts in soft folds, an embroidered apparel set into the hem before and behind, over soft dark shoes.",
    "tags": ["holy", "robe"],
    "locked_to": "t223_chantry_priests_stole_and_alb",
}


def apparel(face, x0, y0, w, h):
    """An embroidered panel sewn to the alb: dark border, coloured field, a gold lozenge at its heart."""
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            edge = x in (x0, x0 + w - 1) or y in (y0, y0 + h - 1)
            face.set(x, y, "A1" if edge else "A3")
    cx, cy = x0 + w // 2, y0 + h // 2
    face.set(cx, cy, "M4")
    for dx, dy in ((1, 0), (-1, 0)):
        face.set(cx + dx, cy + dy, "M2")


def build(g):
    legs(g, "S", "weave", 35100, base=3, rows=(0, 9), crease=False)
    waistband(g, "S", "weave", 35101, base=3)
    soft_shoes(g, "K", 2, top=10, sole="K0")
    front, back, sides = skirt_panels(g, "alb", 12, "S", "weave", 35102, base=3, top=10.6, side_len=11)
    for face in (front, back):
        for x in (1, 4, 7):
            face.vline(x, 1, 7, "S2")
        apparel(face, 1, 8, 7, 3)
        face.hline(0, 8, 11, "S2")
    for box in sides:
        for face in box.sides:
            face.hline(0, face.w - 1, face.h - 1, "S2")
