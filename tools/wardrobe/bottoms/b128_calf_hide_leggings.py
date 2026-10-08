"""Calf-Hide Leggings: hair-on piebald calf-hide leggings laced up the outside, tied by thongs to short linen braies, over soft hide shoes."""
from kit import SIDES, footwear, leg_bone, waistband
from kit_m01 import outer, piebald
from kit_male import blk, leg_blk
from paint import k, strip_fabric

META = {
    "name": "Calf-Hide Leggings",
    "gender": "male",
    "description": "Hair-on piebald calf-hide leggings laced up the outer leg with thongs and tied by points to short linen braies, over soft hide shoes.",
    "tags": ["rugged", "work", "simple"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "S", "weave", 31565 + i, 3, 0, 1)                # braies above the leggings
        leg.top.fill("S3")
        piebald(leg.strip, 31566 + 2 * i, ox=i * 5, rows=range(2, 10), cell=3, threshold=.46)
        piebald(pants.strip, 31567 + 2 * i, ox=i * 5, rows=range(2, 9), cell=3, threshold=.46)
        pants.strip.hline(0, pants.strip.w - 1, 2, "S4")                   # the hide's pale cut edge
        o = outer(pants, side)
        for y in range(3, 9):                                             # thong lacing up the outer seam
            o.set(1 + (y % 2), y, "L1"), o.set(2 - (y % 2), y, "L3")
        for j, x in enumerate((-1.0, 1.0)):                               # points tying them to the braies
            pt = blk(g, f"{side}_hide_point_{j}", (x, 1.4, -2.4), (1, 2, 1), "L", 3, "plain", 31570 + 2 * i + j,
                     bone=leg_bone(side), motion="sway", edge=False)
            pt.strip.hline(0, pt.strip.w - 1, 1, "L1")
    waistband(g, "S", "weave", 31574, base=3)
    body = g.part("body")
    body.front.vline(4, 10, 11, "S2")
    footwear(g, "turnshoe", top=9, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 9, "L3")
        cuff = leg_blk(g, f"{side}_hide_cuff", side, 8.6, (5, 1, 5), "L", 2, "leather", 31573, inflate=.08)
        for face in cuff.sides:
            for x in range(0, face.w, 2):
                face.set(x, 0, k("L", 3))                                 # gathered ankle tie
