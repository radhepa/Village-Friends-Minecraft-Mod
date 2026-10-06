"""Knee Braies & Stockings: loose linen braies gathered below the knee over wool stockings and turnshoes."""
from kit import footwear, leg_ring, legs, stockings, waistband

META = {
    "name": "Knee Braies & Stockings",
    "gender": "male",
    "description": "Loose linen braies gathered just below the knee, wool stockings and soft turnshoes.",
    "tags": ["casual", "simple"],
}


def build(g):
    for leg in legs(g, "S", "weave", 1201, base=3, rows=(0, 6), crease=False):
        for face in leg.sides:
            face.vline(1, 1, 5, "S2")
    stockings(g, "P", (7, 9), base=2)
    waistband(g, "S", "weave", 1202, base=3)
    rings = leg_ring(g, "braies_gather", 5.6, "S", base=3, size=(5, 2, 5))
    for ring in rings:
        for face in ring.sides:
            for x in range(face.w):
                face.set(x, 0, "S4" if x % 2 else "S3")
                face.set(x, 1, "S2" if x % 2 else "S1")
    footwear(g, "turnshoe", top=10)
