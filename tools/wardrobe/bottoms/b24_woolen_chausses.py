"""Woolen Chausses & Ankle Boots: close wool chausses with linen braies puffing above, turn-down ankle boots."""
from kit import footwear, leg_ring, legs, waistband

META = {
    "name": "Woolen Chausses",
    "description": "Fitted wool chausses with linen braies puffing above, and turn-down ankle boots.",
    "tags": ["casual", "sturdy"],
}


def build(g):
    for leg in legs(g, "P", "weave", 2401, rows=(0, 9), crease=False):
        for face in leg.sides:
            face.hline(0, face.w - 1, 0, "S3"), face.hline(0, face.w - 1, 1, "S2")
            face.vline(2, 2, 9, "P1")
    body = waistband(g, "S", "weave", 2402, base=3)
    footwear(g, "boot", top=9)
    for ring in leg_ring(g, "boot_turn", 8.2, "L", base=3, size=(5, 1, 5), texture="leather"):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "L4")
