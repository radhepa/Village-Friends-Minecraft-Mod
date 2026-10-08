"""Pardoner's Dusty Hose: bright close hose greyed with road dust from the knee down, badged garters with dangling points, and short pointed shoes."""
from kit import SIDES, waistband
from kit_male import leg_blk, toe_pieces
from kit_m05 import grime, hose, soft_shoes

META = {
    "name": "Pardoner's Dusty Hose",
    "gender": "male",
    "description": "Showy close hose in a bright colour, greyed with road dust from the knee down, tied below the knee with garters each pinned with a pewter badge and trailing points, in short pointed shoes.",
    "tags": ["casual", "slim"],
}


def build(g):
    hose(g, "A", 2, "weave", 35300, end=9)
    waistband(g, "A", "weave", 35301, base=1)
    soft_shoes(g, "L", 2, top=10, sole="K1")
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        grime(leg.strip, "S1", 7, 9, speck="S2")                          # road dust rising from the shoes
        leg.strip.hline(0, leg.strip.w - 1, 4, "L2")                       # garter
        grime(pants.strip, "S1", 9, 10, ox=5)
        garter = leg_blk(g, f"{side}_garter_badge", side, 3.6, (1, 1, 1), "M", 3, "smooth", 35305,
                         dx=-1.0 if side == "right" else 1.0, dz=-2.2)
        garter.front.fill("M4")
        point = leg_blk(g, f"{side}_garter_point", side, 4.6, (1, 2, 1), "L", 2, "plain", 35306,
                        dx=-2.3 if side == "right" else 2.3, dz=-.6)
        point.strip.hline(0, point.strip.w - 1, 1, "M3")                   # the aglet
    for toe in toe_pieces(g, "pointed_toe", (2, 1, 2), "L", base=2, y=10.9, z=-2.0):
        toe.front.fill("L1"), toe.top.fill("L3")
