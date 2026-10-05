"""Sheepskin Leg Wraps: wool trousers with fleece wrapped round the shins, tied with thongs, fur cuffs."""
from kit import SIDES, footwear, leg_ring, legs, waistband
from paint import rnd

META = {
    "name": "Sheepskin Leg Wraps",
    "description": "Wool trousers with fleece bound around the shins by leather thongs, topped with fur cuffs.",
    "tags": ["rugged", "sturdy", "casual"],
}


def build(g):
    legs(g, "P", "weave", 1601, rows=(0, 5))
    waistband(g, "P", "weave", 1602)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in (leg.strip, pants.strip):
            for y in range(6 if face is leg.strip else 5, 10):
                for x in range(face.w):
                    face.set(x, y, "S4" if rnd(x, y, 1603 + face.x0) > .55 else "S3")
            for y in (7, 9) if face is pants.strip else ():
                for x in range(face.w):
                    if (x + y) % 3 == 0:
                        face.set(x, y, "L2")
    for ring in leg_ring(g, "fur_cuff", 4.6, "S", base=3, size=(5, 2, 5)):
        for face in ring.faces:
            for y in range(face.h):
                for x in range(face.w):
                    face.set(x, y, "S4" if rnd(x, y, 1604 + face.x0) > .5 else "S2")
    footwear(g, "turnshoe", top=10)
