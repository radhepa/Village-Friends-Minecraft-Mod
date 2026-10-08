"""Schoolmaster's Worn Hose and Shoes: old hose rubbed shiny at the knees and sagging in wrinkles round the ankles, in down-at-heel shoes with a cobbled patch on the toe."""
from kit import SIDES, waistband
from kit_male import leg_rings, toe_pieces
from kit_m05 import hose

META = {
    "name": "Schoolmaster's Worn Hose and Shoes",
    "gender": "male",
    "description": "Old woollen hose rubbed shiny at the knees, darned on the shin and sagging in loose wrinkles round the ankles, in down-at-heel shoes with a cobbled patch across one toe.",
    "tags": ["scholarly", "simple", "casual"],
}


def build(g):
    hose(g, "P", 1, "weave", 35500, end=11)
    waistband(g, "P", "weave", 35501, base=1)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.front.rect(1, 3, 2, 2, "P2"), leg.front.set(1 if side == "right" else 2, 3, "P3")   # shiny knee
        for y in (7, 9):                                                   # wrinkles where the hose has slipped
            leg.strip.hline(0, leg.strip.w - 1, y, "P0")
        leg.strip.hline(0, leg.strip.w - 1, 8, "P2")
        if side == "left":
            leg.front.vline(1, 5, 6, "S1"), leg.front.vline(2, 5, 6, "S2")  # a pale darn
        # Shoes: low and trodden down at the heel.
        for face in pants.sides:
            heel = face is pants.back
            for y in range(10 if not heel else 11, 12):
                for x in range(face.w):
                    face.set(x, y, "L1" if y == 11 else "L2")
            if not heel:
                face.hline(0, face.w - 1, 10, "L3")
        pants.front.set(1, 10, "L1")
        pants.back.hline(0, 3, 11, "L1")
        leg.strip.hline(0, leg.strip.w - 1, 10, "L1"), leg.strip.hline(0, leg.strip.w - 1, 11, "L0")
        leg.bottom.fill("K1"), pants.bottom.fill("K0")
    for ring in leg_rings(g, "sagging_hose", 8.2, "P", (5, 1, 5), 1, "weave", 35502, inflate=.18):
        for face in ring.sides:
            for x in range(0, face.w, 2):
                face.set(x, 0, "P2")
    for i, toe in enumerate(toe_pieces(g, "worn_toe", (4, 1, 1), "L", base=2, y=10.9, z=-2.05)):
        toe.front.set(1, 0, "L1"), toe.front.set(2, 0, "L1")
        if i == 1:
            toe.front.set(1, 0, "S2"), toe.front.set(2, 0, "L4")             # the cobbled patch
            toe.top.set(1, 0, "S2")
