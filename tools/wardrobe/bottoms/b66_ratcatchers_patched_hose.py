"""Ratcatcher's Patched Hose: pied hose swapped against the coat, patched at the knees, in laced soft boots with a trap at the hip."""
from kit import SIDES, footwear, waistband
from kit_male import blk, lacing
from paint import fabric, strip_fabric

META = {
    "name": "Ratcatcher's Patched Hose",
    "gender": "male",
    "description": "Pied hose with the colours swapped against the coat, patched at the knees, laced soft boots and a spring trap at the hip.",
    "tags": ["whimsical", "work"],
    "locked_to": "t66_ratcatchers_pied_coat",
}


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        role = "P" if side == "right" else "A"
        strip_fabric(leg, role, "weave", 6611, 2, 0, 9)
        fabric(leg.top, role, "weave", 6611, 2)
        patch = "A2" if role == "P" else "P2"
        leg.front.rect(1, 3, 2, 2, patch), leg.front.set(1, 3, "S3")
    waistband(g, "P", "weave", 6612)
    footwear(g, "boot", top=8, base=2)
    for side in SIDES:
        lacing(g.part(f"{side}_pants").front, 1, 8, 10, "L4", "L1")
    trap = blk(g, "waist_rat_trap", (-3.0, 10.2, -2.6), (3, 2, 1), "L", 3, "plain", 6613)
    trap.front.hline(0, 2, 0, "M3"), trap.front.set(1, 1, "M1")
