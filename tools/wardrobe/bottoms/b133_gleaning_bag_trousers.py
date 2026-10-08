"""Gleaning-Bag Trousers: thin hemp trousers with a little tied sack bound to each thigh for gleaned grain, turned-up hems and soft shoes worn through at the toe."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_m01 import outer
from kit_male import blk, leg_blk
from paint import k, solid

META = {
    "name": "Gleaning-Bag Trousers",
    "gender": "male",
    "description": "Thin hemp trousers with a little drawstring sack bound to each thigh for gleaned grain, turned-up hems and soft old shoes worn through at the toe.",
    "tags": ["casual", "simple", "relaxed"],
}


def build(g):
    leg_boxes = legs(g, "P", "weave", 31690, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 31691)
    footwear(g, "turnshoe", top=10, base=2)
    for i, (side, leg) in enumerate(zip(SIDES, leg_boxes)):
        pants = g.part(f"{side}_pants")
        for face in leg.sides:
            face.vline(1, 2, 7, "P1")
        pants.front.set(1 + i, 11, None), leg.front.set(1 + i, 11, None)   # a toe worn through
        pants.front.set(1 + i, 10, "L1")
        hem = leg_blk(g, f"{side}_turned_hem", side, 8.2, (5, 1, 5), "P", 3, "weave", 31692 + i, inflate=.1)
        for face in hem.sides:
            face.set(1, 0, "P2"), face.set(3, 0, "P4")
        # The sack on the outer thigh, its neck drawn shut with a cord and a thong round the leg holding it.
        x = -2.6 if side == "right" else 2.6
        sack = g.piece(f"{side}_gleaning_sack", leg_bone(side), (-1, 0, -1.2), (2, 3, 2), pivot=(x, 1.6, 0),
                       inflate=.08)
        solid(sack, "S", "weave", 31694 + i, 2)
        for face in sack.sides:
            face.set(0, 1, "S1"), face.set(1, 2, "S3")
        sack.bottom.fill("S1")
        neck = blk(g, f"{side}_sack_neck", (x, .6, -.2), (1, 1, 1), "S", 3, "plain", 31696 + i, bone=leg_bone(side),
                   edge=False)
        neck.top.fill("S4")
        tie = blk(g, f"{side}_sack_tie", (x, 1.5, -.2), (2, 1, 2), "L", 2, "plain", 31698, bone=leg_bone(side),
                  edge=False, inflate=.12)
        tie.top.fill("L3")
        thong = leg_blk(g, f"{side}_thigh_thong", side, 2.6, (5, 1, 5), "L", 1, "plain", 31699, inflate=.04)
        outer(thong, side).set(2, 0, k("L", 3))
