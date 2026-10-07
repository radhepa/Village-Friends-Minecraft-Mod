"""Monk's Under-Robe: the habit's ankle-length skirts in folds over bare feet in plain strapped sandals."""
from kit import SIDES, legs, waistband
from kit_male import skirt_panels

META = {
    "name": "Monk's Under-Robe",
    "gender": "male",
    "description": "The habit's ankle-length skirts falling in deep folds, over bare feet in plain strapped sandals.",
    "tags": ["holy", "robe"],
    "locked_to": "t51_monks_scapular_habit",
}


def build(g):
    legs(g, "P", "weave", 5111, base=1, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 5112, base=1)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        pants.front.hline(0, 3, 10, "L2")                                  # strap over the instep
        for face in (pants.right, pants.left):
            face.set(1, 10, "L2"), face.set(2, 10, "L1")
        pants.strip.hline(0, pants.strip.w - 1, 11, "L1")                  # sole
        leg.bottom.fill("L0"), pants.bottom.fill("L0")
    front, back, sides = skirt_panels(g, "robe", 11, "P", "weave", 5113, base=1, top=10.6, side_len=10)
    for face in (front, back):
        for x in (2, 6):
            face.vline(x, 1, 10, "P0")
        face.vline(4, 2, 10, "P2")
        face.hline(0, 8, 10, "P0")
