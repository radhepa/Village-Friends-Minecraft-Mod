"""Charcoal Burner's Smoke-Grey Breeches: full wool breeches bloused into sacking leg wraps, soot-dark
knees, a tinder pouch on the hip and wooden-soled clogs."""
from kit import SIDES, footwear, legs, waistband
from kit_female import side_pouch, wraps
from paint import fabric

META = {
    "name": "Charcoal Burner's Smoke-Grey Breeches",
    "gender": "female",
    "description": "Full wool breeches bloused over sacking leg wraps, knees blackened from kneeling at the kiln, "
                   "a tinder pouch on the hip and wooden-soled clogs.",
    "tags": ["work", "rugged", "sturdy"],
}


def build(g):
    legs(g, "P", "plain", 57721, rows=(0, 6), crease=False)
    waistband(g, "P", "plain", 57722)
    body = g.part("body")
    for face in body.sides:
        face.hline(0, face.w - 1, 9, "L1")                            # a cord drawstring
    body.front.set(3, 10, "L2"), body.front.set(4, 10, "L2")
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in leg.sides:
            face.vline(1 if face is leg.front else 2, 0, 5, "P1")      # the leg seam
            face.hline(0, face.w - 1, 5, "P3"), face.hline(0, face.w - 1, 6, "P1")   # bloused over the wraps
        wraps(leg.strip, 7, 9, "S", 1, step=3)
        # Soot-dark knees, a blotch rubbed into the cloth.
        for x in range(4):
            for y in (3, 4):
                leg.front.set(x, y, "P0" if y == 4 and 0 < x < 3 else "P1")
        fabric(pants.front, "P", "plain", 57723, 2, 0, 5, 4, 1)
        pants.front.set(1, 5, "P1")
    footwear(g, "clog", top=10, role="L", base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "L3"), face.hline(0, face.w - 1, 11, "L1")
    pouch = side_pouch(g, "waist_tinder_pouch", "left", y=9.6, size=(2, 2, 2), role="L", flap="M3")
    pouch.top.fill("L3")
