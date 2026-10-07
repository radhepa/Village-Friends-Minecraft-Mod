"""Izar Wrap Skirt: a length of striped cloth wrapped round the hips and falling to mid-calf, over bare calves and thong sandals."""
from kit import SIDES, legs, waistband
from kit_male import skirt_panels, stripes
from paint import line

META = {
    "name": "Izar Wrap Skirt",
    "gender": "male",
    "description": "A length of striped cloth wrapped round the hips and tucked at the waist, falling to mid-calf over bare calves and thong sandals.",
    "tags": ["relaxed", "simple", "casual"],
    "rejects": ["armor"],
}


def build(g):
    legs(g, "S", "weave", 8811, base=3, rows=(0, 7), crease=False)
    waistband(g, "S", "weave", 8812, base=3)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.strip.hline(0, pants.strip.w - 1, 11, "L2")
        pants.front.set(1 if side == "right" else 2, 10, "L3")
        g.part(f"{side}_leg").bottom.fill("L1"), pants.bottom.fill("L1")
    front, back, sides = skirt_panels(g, "izar", 9, "S", "weave", 8813, base=3, top=10.4, side_len=8)
    for face in (front, back):
        stripes(face, ["S3", "S3", "S3", "A2", "S3", "P2"], vertical=False, offset=1)
    line(front, 1, 0, 6, 8, "S1")                                        # the wrapped overlap
    for box in sides:
        for face in box.sides:
            stripes(face, ["S3", "S3", "S3", "A2", "S3", "P2"], vertical=False, offset=1)
