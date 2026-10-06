"""Mud-Spattered Wraps: wool trousers bound from knee to ankle in linen strips, splashed with mud, over muddy turnshoes."""
from kit import SIDES, footwear, legs, waistband
from kit_male import flecks, leg_blk, wraps

META = {
    "name": "Mud-Spattered Wraps",
    "gender": "male",
    "description": "Wool trousers bound from knee to ankle in pale linen strips, splashed with mud from the sties, over muddy turnshoes.",
    "tags": ["rugged", "simple"],
}


def build(g):
    legs(g, "P", "weave", 4411, rows=(0, 9), crease=False)
    waistband(g, "P", "weave", 4412)
    footwear(g, "turnshoe", top=10, base=1)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        wraps(leg.strip, "S", range(4, 10), base=3, period=4)
        leg.strip.hline(0, leg.strip.w - 1, 3, "L2")                       # garter that holds the wraps
        flecks(leg.strip, "L1", 4413, .14, rows=range(7, 10))
        flecks(pants.strip, "L0", 4414, .2, rows=range(10, 12))
        tie = leg_blk(g, f"{side}_wrap_tie", side, 3.0, (1, 2, 1), "L", 2, "plain", 4415 + i,
                      dx=-2.3 if side == "right" else 2.3)
        tie.strip.hline(0, tie.strip.w - 1, 1, "L3")
