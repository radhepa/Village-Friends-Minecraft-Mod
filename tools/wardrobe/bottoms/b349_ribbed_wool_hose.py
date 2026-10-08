"""Ribbed Wool Hose: close knitted hose ribbed from waist to ankle, a knitted turnover at the knee and soft ankle shoes."""
from kit import SIDES, footwear, waistband
from kit_m10 import leg_ring, outer, tie
from kit_male import ribbing
from paint import fabric

META = {
    "name": "Ribbed Wool Hose",
    "gender": "male",
    "description": "Close hand-knitted wool hose ribbed from waist to ankle, a patterned turnover welt below each knee tied with a yarn garter, and soft ankle shoes.",
    "tags": ["casual", "simple", "knit"],
}


def build(g):
    for i, side in enumerate(SIDES):
        leg = g.part(f"{side}_leg")
        for y in range(0, 10):
            for x in range(leg.strip.w):
                leg.strip.set(x, y, "P1" if x % 3 == 2 else "P3" if x % 3 == 0 and y % 2 else "P2")
        fabric(leg.top, "P", "knit", 40160, 2)
        outer(leg, side).vline(2, 0, 9, "P0")                             # shaping seam
        # Knitted turnover welt below the knee, a two-tone band, tied off with a yarn garter.
        welt = leg_ring(g, f"{side}_knit_welt", side, 5.0, (5, 2, 5), "P", 2, "rib", 40161 + i)
        for face in welt.sides:
            for x in range(face.w):
                face.set(x, 0, "P3" if x % 2 else "P2")
                face.set(x, 1, "A2" if x % 2 else "A1")
        tie(g, f"{side}_garter_tail", "RIGHT_LEG" if side == "right" else "LEFT_LEG",
            (-2.6 if side == "right" else 2.6, 6.6, -.4), "A", 2, 2, 40163 + i)
    body = waistband(g, "P", "rib", 40165)
    for face in body.sides:
        ribbing(face, "P", 2, rows=range(9, 12), horizontal=True)
    footwear(g, "turnshoe", top=10, base=2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        for face in pants.sides:
            face.hline(0, face.w - 1, 10, "L3")                           # the shoe's rolled edge
