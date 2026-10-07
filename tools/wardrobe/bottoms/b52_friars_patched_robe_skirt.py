"""Friar's Patched Robe Skirt: a mid-calf robe skirt with darned patches, over bare ankles in thonged sandals."""
from kit import SIDES, legs, waistband
from kit_male import skirt_panels

META = {
    "name": "Friar's Patched Robe Skirt",
    "gender": "male",
    "description": "The friar's robe falling to mid-calf, mended with patches front and back, over bare ankles and thonged sandals.",
    "tags": ["holy", "robe"],
    "locked_to": "t52_friars_corded_robe",
}


def build(g):
    legs(g, "P", "weave", 5211, rows=(0, 8), crease=False)
    waistband(g, "P", "weave", 5212)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        pants.front.set(1 if side == "right" else 2, 10, "L2")             # toe thong
        for face in (pants.right, pants.left):
            face.hline(1, 2, 10, "L2")
        pants.strip.hline(0, pants.strip.w - 1, 11, "L2")
        leg.bottom.fill("L1"), pants.bottom.fill("L1")
    front, back, sides = skirt_panels(g, "robe", 9, "P", "weave", 5213, top=10.6, side_len=8)
    front.rect(1, 4, 2, 2, "P3"), front.set(1, 4, "P1"), front.set(2, 5, "P1")
    back.rect(5, 2, 2, 2, "P1"), back.set(6, 2, "P3")
    for face in (front, back):
        face.vline(4, 1, 8, "P1")
        face.hline(0, 8, 8, "P0")
