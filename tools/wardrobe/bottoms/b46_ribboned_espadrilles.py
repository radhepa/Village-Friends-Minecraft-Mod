"""Ribboned Espadrilles: loose linen trousers bound at the ankle by the ribbons of rope-soled canvas espadrilles."""
from kit import SIDES, legs, waistband
from kit_male import leg_blk
from paint import line

META = {
    "name": "Ribboned Espadrilles",
    "gender": "male",
    "description": "Loose summer linen trousers gathered at the ankle by the crossing ribbons of rope-soled canvas espadrilles.",
    "tags": ["casual", "relaxed"],
    "rejects": ["armor"],
}


def build(g):
    legs(g, "S", "weave", 4611, base=3, rows=(0, 9), crease=False)
    waistband(g, "S", "weave", 4612, base=3)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        for x in range(leg.strip.w):
            leg.strip.set(x, 9, "S2" if x % 2 else "S3")                   # hem gathered at the ankle
        for y in (10, 11):
            leg.strip.hline(0, leg.strip.w - 1, y, "P2" if y == 10 else "S1")
        for face in pants.sides:
            line(face, 0, 7, 3, 9, "A2"), line(face, 3, 7, 0, 9, "A3")     # ribbons crossing round the ankle
            face.hline(0, face.w - 1, 10, "P2")                            # canvas upper
            for x in range(face.w):
                face.set(x, 11, "S2" if (x + face.x0) % 2 else "S1")       # braided rope sole
        pants.front.set(1, 10, "P3"), pants.front.set(2, 10, "P3")
        leg.bottom.fill("S1"), pants.bottom.fill("S1")
        bow = leg_blk(g, f"{side}_ribbon_bow", side, 7.6, (1, 1, 1), "A", 3, "plain", 4613 + i, dz=-2.45)
        bow.front.fill("A2")
