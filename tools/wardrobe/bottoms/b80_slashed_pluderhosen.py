"""Slashed Pluderhosen: baggy knee-length breeches slashed into panes over billowing accent lining, hose and wide shoes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_blk, toe_pieces

META = {
    "name": "Slashed Pluderhosen",
    "gender": "male",
    "description": "Baggy knee-length mercenary breeches slashed into panes over billowing accent lining, with hose and wide blunt shoes.",
    "tags": ["fancy", "whimsical", "martial"],
}


def build(g):
    legs(g, "S", "weave", 8011, base=3, rows=(0, 9), crease=False)
    waistband(g, "P", "velvet", 8012)
    footwear(g, "shoe", top=10, base=2)
    for i, side in enumerate(SIDES):
        tube = leg_blk(g, f"{side}_pluder", side, 0.0, (5, 6, 5), "P", 2, "velvet", 8013 + i,
                       dx=-.3 if side == "right" else .3, inflate=.16 + .04 * i)
        for face in tube.sides:
            for x in range(face.w):
                if x % 2:
                    face.vline(x, 1, 4, "A3")                             # lining billowing through the panes
            face.hline(0, face.w - 1, 5, "P1")
        tube.bottom.fill("A1")
    for toe in toe_pieces(g, "cow_mouth_toe", (4, 1, 1), "L", base=2, y=10.9, z=-2.1, inflate=.15):
        toe.front.set(0, 0, "L3"), toe.front.set(3, 0, "L3")
