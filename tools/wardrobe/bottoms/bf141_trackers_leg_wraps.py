"""Tracker's Leg Wraps: close wool trews with shaggy pelts wrapped round the shins, bound at the top and the ankle
with thongs, over soft turnshoes."""
from kit import SIDES, legs, waistband
from kit_female import fur, leg_rings, shoes, waist_belt
from paint import solid

META = {
    "name": "Tracker's Leg Wraps",
    "gender": "female",
    "description": "Close wool trews with shaggy pelts wrapped round the shins and bound with thongs at the knee "
                   "and ankle, over soft turnshoes.",
    "tags": ["rugged", "sturdy"],
}


def build(g):
    legs(g, "P", "twill", 54221, rows=(0, 9), crease=False)
    body = waistband(g, "P", "twill", 54222)
    body.front.vline(4, 9, 11, "P1")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        leg.front.vline(1 if side == "right" else 2, 1, 4, "P1")
    shoes(g, "turnshoe", "L", 2)
    for i, ring in enumerate(leg_rings(g, "pelt_wrap", 4.4, 6, 5, inflate=.16)):
        for face in ring.faces:
            fur(face, "L", 54223 + i, 3)
        for face in ring.sides:
            for x in range(face.w):                                     # ragged lower edge of the pelt
                if x % 2:
                    face.set(x, 5, "L2")
            face.vline(0, 0, 5, "L2")                                   # the overlap where the pelt wraps
        ring.bottom.fill("L1")
    for y, name in ((4.9, "knee"), (9.0, "ankle")):
        for ring in leg_rings(g, f"thong_{name}", y, 1, 5, inflate=.28):
            solid(ring, "L", "leather", 54225, 1, edge=False)
            for face in ring.sides:
                for x in range(0, face.w, 3):
                    face.set(x, 0, "L3")
            ring.front.set(2, 0, "S3")                                  # the knot
    waist_belt(g, "waist_belt", 9.4, height=1)
