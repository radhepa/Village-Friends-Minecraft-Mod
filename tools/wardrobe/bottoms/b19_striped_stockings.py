"""Striped Stockings & Short Breeches: puffed breeches banded at the knee over bold striped stockings."""
from kit import SIDES, footwear, leg_ring, legs, waistband

META = {
    "name": "Striped Stockings & Breeches",
    "gender": "male",
    "description": "Short puffed breeches with accent knee bands over cheerfully striped stockings and buckled shoes.",
    "tags": ["casual", "whimsical"],
}


def build(g):
    legs(g, "P", "velvet", 1901, rows=(0, 5), crease=False)
    waistband(g, "P", "velvet", 1902)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for y in range(6, 10):
            leg.strip.hline(0, leg.strip.w - 1, y, "S4" if y % 2 == 0 else "A2")
    for ring in leg_ring(g, "knee_band", 4.6, "A", base=2, size=(5, 2, 5)):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "P2"), face.hline(0, face.w - 1, 1, "A2")
    footwear(g, "shoe", top=10)
    for side in SIDES:
        g.part(f"{side}_pants").front.set(1, 10, "M3"), g.part(f"{side}_pants").front.set(2, 10, "M3")
