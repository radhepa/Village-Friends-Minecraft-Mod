"""Striped Knee Hose: plain knee breeches over knee hose striped up and down, folded over at the top, in soft ankle boots."""
from kit import SIDES, footwear, legs, waistband
from kit_m10 import leg_ring, outer
from kit_male import stripes

META = {
    "name": "Striped Knee Hose",
    "gender": "male",
    "description": "Plain wool knee breeches over long knee hose striped up and down in two colours, folded over in a plain band below the knee, worn with soft ankle boots.",
    "tags": ["casual", "simple", "whimsical"],
}


def build(g):
    for side, leg in zip(SIDES, legs(g, "P", "weave", 40600, rows=(0, 5), crease=False)):
        outer(leg, side).vline(2, 0, 5, "P1")
        stripes(leg.strip, ["S4", "A2"], vertical=True, rows=range(6, 10), offset=0 if side == "right" else 1)
    waistband(g, "P", "weave", 40601)
    for i, side in enumerate(SIDES):
        fold = leg_ring(g, f"{side}_hose_fold", side, 5.0, (5, 2, 5), "S", 3, "plain", 40602 + i)
        for face in fold.sides:
            face.hline(0, face.w - 1, 0, "S4")
            face.hline(0, face.w - 1, 1, "S2")
    footwear(g, "boot", top=9, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 9, "L3")                            # the soft boot's rolled top
