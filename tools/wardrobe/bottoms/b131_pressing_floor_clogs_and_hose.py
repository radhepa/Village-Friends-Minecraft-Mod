"""Pressing-Floor Clogs and Hose: short braies over ribbed hose gartered below the knee, damp at the feet, in iron-rimmed wooden clogs stuffed with straw."""
from kit import SIDES, leg_bone, waistband
from kit_m01 import outer
from kit_male import blk, leg_blk, ribbing, toe_pieces
from paint import strip_fabric

META = {
    "name": "Pressing-Floor Clogs and Hose",
    "gender": "male",
    "description": "Short braies over ribbed wool hose gartered below the knee and dark with damp at the ankle, stepping in iron-rimmed wooden clogs with straw stuffed in for warmth.",
    "tags": ["work", "simple", "casual"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        strip_fabric(leg, "S", "weave", 31640 + i, 3, 0, 2)               # braies
        leg.top.fill("S3")
        strip_fabric(pants, "S", "weave", 31642 + i, 3, 0, 2)
        for face in pants.sides:
            face.vline(1, 0, 1, "S2")
            face.hline(0, face.w - 1, 2, "S2")
        ribbing(leg.strip, "P", 2, rows=range(3, 10))                      # ribbed hose
        leg.strip.hline(0, leg.strip.w - 1, 8, "P1")
        leg.strip.hline(0, leg.strip.w - 1, 9, "P0")                       # damp from the pressing floor
        garter = leg_blk(g, f"{side}_garter", side, 4.4, (5, 1, 5), "L", 2, "leather", 31644 + i, inflate=.06)
        outer(garter, side).set(2, 0, "M3")
        tail = blk(g, f"{side}_garter_tail", (-2.5 if side == "right" else 2.5, 4.9, -.6), (1, 2, 1), "L", 2,
                   "plain", 31646 + i, bone=leg_bone(side), motion="sway", edge=False)
        tail.strip.hline(0, tail.strip.w - 1, 1, "L3")
        # The clog: a carved wooden shoe round the foot with an iron rim on the sole.
        for face in leg.sides:
            face.hline(0, face.w - 1, 10, "L3"), face.hline(0, face.w - 1, 11, "M1")
        leg.bottom.fill("M1")
        for face in pants.sides:
            face.hline(0, face.w - 1, 9, "L4")                             # the clog's lit mouth
            face.hline(0, face.w - 1, 10, "L3")
            face.hline(0, face.w - 1, 11, "M2")
            face.set(1, 10, "L2")
        pants.bottom.fill("M1")
        for x in range(0, 4, 2):
            pants.front.set(x, 9, "S4")                                   # straw poking from the clog
    for toe in toe_pieces(g, "clog_toe", (4, 2, 2), "L", base=3, texture="plain", seed=31648, y=9.9, z=-2.0,
                          inflate=.05):
        toe.top.fill("L4"), toe.top.hline(0, 3, 0, "L2")
        toe.front.hline(0, 3, 1, "M2"), toe.front.set(1, 0, "L4")
    waistband(g, "S", "weave", 31649, base=3)
    cord = g.part("body")
    cord.front.vline(4, 9, 11, "S2")
