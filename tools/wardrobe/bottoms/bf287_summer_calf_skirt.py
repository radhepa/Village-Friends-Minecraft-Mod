"""Summer Calf Skirt: a light calf-length skirt with a single deep tuck, over rope-soled shoes ribboned round bare ankles."""
from kit import SIDES
from kit_female import skirt

META = {
    "name": "Summer Calf Skirt",
    "gender": "female",
    "description": "A light calf-length skirt with one deep tuck above the hem, over rope-soled shoes tied with ribbons crossed round bare ankles.",
    "tags": ["casual", "relaxed", "skirt"],
}


def tuck(face):
    h = face.h
    face.hline(0, face.w - 1, h - 4, "P4")
    face.hline(0, face.w - 1, h - 3, "P3")
    face.hline(0, face.w - 1, h - 2, "P1")
    face.hline(0, face.w - 1, h - 1, "P2")


def build(g):
    s = skirt(g, "P", "plain", 60060, base=3, top=9.8, length=8, flare=7)
    s.paint(tuck)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        # Ribbons crossed over the bare ankle, front and back, above a strap round it.
        leg.strip.hline(0, 15, 9, "A2")
        for face in (leg.front, leg.back):
            face.set(0, 7, "A3"), face.set(3, 7, "A3")
            face.set(1, 8, "A2"), face.set(2, 8, "A2")
        # Canvas uppers on rope soles.
        leg.strip.hline(0, 15, 10, "S3")
        leg.strip.hline(0, 15, 11, "S1")
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "S3")
            for x in range(face.w):
                face.set(x, 11, "S2" if x % 2 else "L3")                  # the plaited rope sole
        pants.front.set(1, 10, "S4"), pants.front.set(2, 10, "S4")
        leg.bottom.fill("L2"), pants.bottom.fill("L1")
