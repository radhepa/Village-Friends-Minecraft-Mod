"""Gleaner's Short Field Skirt: a shin-length skirt stitched with three deep tucks above a darned hem, over
bare calves and feet wrapped in strips of rag."""
from kit import SIDES
from kit_female import skirt, wraps
from paint import k

META = {
    "name": "Gleaner's Short Field Skirt",
    "gender": "female",
    "description": "A shin-length field skirt with three deep tucks above a darned hem, bare calves and feet bound in strips of rag.",
    "tags": ["work", "simple", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 51100, top=9.8, length=9, flare=6)
    for face in s.faces:
        for y in (face.h - 7, face.h - 5, face.h - 3):
            face.hline(0, face.w - 1, y, "P3")                       # each tuck: a lit fold over its shadow
            face.hline(0, face.w - 1, y + 1, "P1")
        face.hline(0, face.w - 1, face.h - 1, "P1")
    for box in (s.right, s.left):
        for face in (box.front, box.back):
            for y in (face.h - 7, face.h - 5, face.h - 3):
                face.set(0, y, "P3"), face.set(0, y + 1, "P1")
    darn = s.front.front
    for x, y in ((2, 7), (3, 8), (4, 7), (7, 8)):
        darn.set(x, y, "S2")                                          # darning across a worn hem
    # Bare calves, the feet and ankles bound in rag strips.
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for face in leg.sides:
            wraps(face, 9, 10, "S", 2, step=3)
        leg.strip.hline(0, leg.strip.w - 1, 11, "S1")
        leg.bottom.fill("S1")
        for face in pants.sides:
            face.hline(0, face.w - 1, 9, "S3")
            face.set(1, 10, "S2"), face.set(2, 10, "S2")
        pants.front.set(0, 10, k("S", 3)), pants.front.set(3, 10, k("S", 1))
