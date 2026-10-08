"""Drummer's Gaitered Trousers: full trousers bloused over canvas gaiters strapped and buckled up the outside."""
from kit import SIDES, footwear, leg_ring, legs, waistband
from kit_m04 import sides_of

META = {
    "name": "Drummer's Gaitered Trousers",
    "gender": "male",
    "description": "Full wool trousers bloused at the shin over pale canvas gaiters, each closed by two leather straps "
                   "buckled up the outside and a strap under the instep of a plain shoe.",
    "tags": ["martial", "sturdy", "casual"],
}

S = 34260


def build(g):
    legs(g, "P", "twill", S, rows=(0, 9), crease=False)
    waistband(g, "P", "twill", S + 2)
    footwear(g, "shoe", top=10, base=1)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:                                           # canvas gaiter over the shin and shoe
            for y in range(6, 11):
                for x in range(face.w):
                    face.set(x, y, "S3" if (x + y) % 5 else "S2")
            face.hline(0, face.w - 1, 6, "S4")
        outer = getattr(pants, sides_of(side)[0])
        outer.vline(3, 6, 10, "S1")                                        # the closing edge
        for y in (7, 9):
            outer.hline(0, 3, y, "L2"), outer.set(2, y, "M3")             # strap and buckle
            pants.front.set(0 if side == "right" else 3, y, "L2")
        pants.front.hline(0, 3, 10, "S2")
    for ring in leg_ring(g, "blouse", 4.8, "P", base=2, size=(4, 2, 4), texture="twill", inflate=.42):
        for face in ring.sides:
            face.set(1, 1, "P1"), face.set(2, 0, "P1"), face.set(3, 1, "P3")
