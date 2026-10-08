"""Lambswool-Lined Boots: wool trousers tucked into calf boots lined with lambswool, the fleece showing at the cuff and up the laced front."""
from kit import SIDES, footwear, legs, waistband
from kit_m10 import leg_ring, outer
from kit_male import fur_face

META = {
    "name": "Lambswool-Lined Boots",
    "gender": "male",
    "description": "Wool trousers tucked into calf-high leather boots lined with lambswool, the fleece curling over a short cuff and showing between the thongs that lace up the front.",
    "tags": ["casual", "sturdy", "rugged"],
}


def build(g):
    for side, leg in zip(SIDES, legs(g, "P", "weave", 40680, rows=(0, 5), crease=False)):
        outer(leg, side).vline(2, 0, 5, "P1")
    waistband(g, "P", "weave", 40681)
    footwear(g, "boot", top=5, base=2)
    for i, side in enumerate(SIDES):
        pants = g.part(f"{side}_pants")
        # Fleece in the laced opening up the shin.
        for y in range(6, 10):
            pants.front.set(0, y, "L1"), pants.front.set(3, y, "L1")
            pants.front.set(1, y, "S4" if y == 6 else "S3"), pants.front.set(2, y, "S3")
        for y in (7, 9):
            pants.front.hline(0, 3, y, "L3")                              # thongs crossing the fleece
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "L1")
        # A short fleece cuff curling over the boot top.
        cuff = leg_ring(g, f"{side}_fleece_cuff", side, 4.4, (5, 2, 5), "S", 3, "plain", 40682 + i, open_bottom=False)
        for face in cuff.sides:
            fur_face(face, "S", 40684 + i, 3)
        cuff.bottom.fill("S1")
