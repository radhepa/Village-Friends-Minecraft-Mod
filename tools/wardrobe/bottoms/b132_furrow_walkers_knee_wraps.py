"""Furrow-Walker's Knee Wraps: loose trousers bound round the knees with spiralled linen bands for long days on soft ploughland, and low boots clotted with furrow soil."""
from kit import SIDES, footwear, legs, waistband
from kit_m01 import mud
from kit_male import leg_blk, toe_pieces, wraps
from paint import strip_fabric

META = {
    "name": "Furrow-Walker's Knee Wraps",
    "gender": "male",
    "description": "Loose trousers bound round each knee with spiralled linen bands for long days striding the soft ploughland, bloused above and below, and low boots clotted with furrow soil.",
    "tags": ["work", "rugged", "simple"],
}


def build(g):
    leg_boxes = legs(g, "P", "weave", 31665, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 31666)
    footwear(g, "boot", top=9, base=2)
    for i, (side, leg) in enumerate(zip(SIDES, leg_boxes)):
        pants = g.part(f"{side}_pants")
        strip_fabric(pants, "P", "weave", 31667 + i, 2, 0, 2)              # bloused above the wrap
        for face in pants.sides:
            face.vline(1, 0, 2, "P1"), face.set(2, 2, "P3")
        for face in leg.sides:
            face.vline(2, 6, 8, "P1"), face.set(1, 7, "P3")                # and below it
        # The knee wrap: a spiral linen band, its tucked end showing on the outside.
        wrap = leg_blk(g, f"{side}_knee_wrap", side, 2.8, (5, 3, 5), "S", 3, "weave", 31669 + i, inflate=.14)
        for face in wrap.sides:
            wraps(face, "S", range(0, 3), base=3, period=3, slope=1)
        wrap.top.fill("S4"), wrap.bottom.fill("S1")
        tie = leg_blk(g, f"{side}_ankle_tie", side, 8.4, (5, 1, 5), "L", 2, "plain", 31671 + i, inflate=.1)
        for face in tie.sides:
            face.set(2, 0, "L3")
        for face in pants.sides:
            mud(face, 31673 + i + face.x0, 10, role="L", base=1, rows=range(9, 12), splash=.15)
    for toe in toe_pieces(g, "soil_clod", (3, 1, 1), "L", base=1, texture="plain", seed=31674, y=10.9, z=-2.15,
                          inflate=.05):
        toe.top.fill("L2"), toe.front.set(1, 0, "L0")
