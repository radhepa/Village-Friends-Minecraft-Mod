"""Bare-Shin Rolled Slops: wide linen slops rolled in a fat cuff above the knee, bare shins, and rawhide shoes thonged round the ankle."""
from kit import SIDES, leg_bone, waistband
from kit_m01 import gathers, outer
from kit_male import blk, leg_blk
from paint import strip_fabric

META = {
    "name": "Bare-Shin Rolled Slops",
    "gender": "male",
    "description": "Wide linen slops rolled in a fat cuff above the knee to keep them out of the pond, bare shins, and gathered rawhide shoes thonged round the ankle.",
    "tags": ["casual", "simple", "relaxed"],
    "rejects": ["armor"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "S", "weave", 31615 + i, 3, 0, 3)
        leg.top.fill("S3")
        strip_fabric(pants, "S", "weave", 31617 + i, 3, 0, 2)             # wide legs standing off
        gathers(pants.strip, "S", 3, range(1, 3), i)
        pants.strip.hline(0, pants.strip.w - 1, 0, "S4")
        roll = leg_blk(g, f"{side}_slop_roll", side, 2.6, (5, 2, 5), "S", 3, "weave", 31619 + i, inflate=.2)
        for face in roll.sides:
            face.hline(0, face.w - 1, 0, "S4"), face.hline(0, face.w - 1, 1, "S2")
            face.set(1 + i, 1, "S1")
        # Rawhide shoes: a puckered hide upper gathered on a thong, the thong wound twice round the ankle.
        for face in leg.sides:
            for y in (10, 11):
                face.hline(0, face.w - 1, y, "L3" if y == 10 else "L2")
        leg.bottom.fill("K1")
        for face in pants.sides:
            face.hline(0, face.w - 1, 11, "L2")
            face.hline(0, face.w - 1, 10, "L3")
            face.set(1, 10, "L2")                                         # puckered where the thong gathers it
        pants.bottom.fill("K0")
        thong = leg_blk(g, f"{side}_ankle_thong", side, 9.0, (5, 1, 5), "L", 1, "plain", 31621 + i, inflate=.02)
        for face in thong.sides:
            face.set(1, 0, "L3"), face.set(3, 0, "L3")
        tail = blk(g, f"{side}_thong_tail", (-2.5 if side == "right" else 2.5, 9.4, -1), (1, 2, 1), "L", 2, "plain",
                   31623, bone=leg_bone(side), motion="sway", edge=False)
        tail.strip.hline(0, tail.strip.w - 1, 1, "L1")
        outer(leg, side).vline(1, 1, 2, "S2")
    body = waistband(g, "S", "weave", 31624, base=3)
    body.front.vline(4, 10, 11, "S2")
    cord = blk(g, "waist_drawstring", (-.4, 10.2, -2.3), (1, 2, 1), "L", 3, "plain", 31624, motion="sway", edge=False)
    cord.strip.hline(0, cord.strip.w - 1, 1, "L1")
