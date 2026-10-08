"""Venetian Calze Hose: soled hose fitted to the leg, the left calza striped and badged with a company's woven device."""
from kit import SIDES, legs, waistband
from kit_male import stripes
from kit_m08 import roundel

META = {
    "name": "Venetian Calze Hose",
    "gender": "male",
    "description": "Close soled hose with jewelled garters, the left calza striped down the thigh and badged at the knee with the woven device of a young men's company.",
    "tags": ["fancy", "slim"],
    "rejects": ["armor"],
}


def build(g):
    legs(g, "P", "twill", 38381, rows=(0, 10), crease=False)
    waistband(g, "P", "twill", 38382)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        leg.strip.hline(0, leg.strip.w - 1, 11, "K1")                     # leather-soled feet
        leg.strip.hline(0, leg.strip.w - 1, 10, "P1")
        leg.bottom.fill("K0")
        leg.strip.hline(0, leg.strip.w - 1, 6, "A1")
        pants.strip.hline(0, pants.strip.w - 1, 6, "A2")                   # raised garter
        pants.front.set(1, 6, "M4")
    left, left_p = g.part("left_leg"), g.part("left_pants")
    stripes(left.strip, ["A2", "A2", "S3", "S3"], vertical=True, rows=range(0, 6))
    stripes(left.top, ["A2", "A2", "S3", "S3"], vertical=True)
    roundel(left_p.front, 0, 1, "M3", "A3", "M4")                          # the company's device
