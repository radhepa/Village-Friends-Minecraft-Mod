"""Lay Brother's Field Boots: linen braies bunched at the knee over tall front-laced field boots with turned-down tops, caked in field mud."""
from kit import SIDES, footwear, waistband
from kit_male import lacing, leg_rings
from kit_m05 import grime
from paint import strip_fabric

META = {
    "name": "Lay Brother's Field Boots",
    "gender": "male",
    "description": "Coarse linen braies bunched at the knee over tall field boots laced up the front, their tops turned down, caked with furrow mud to the ankle.",
    "tags": ["work", "rugged", "sturdy"],
}


def build(g):
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        strip_fabric(leg, "S", "weave", 35380 + (side == "left"), 2, 0, 4)
        leg.top.fill("S2")
        for x in range(0, leg.strip.w, 3):
            leg.strip.vline(x, 1, 3, "S1")                                 # gathered folds
    waistband(g, "S", "weave", 35382)
    footwear(g, "boot", top=5, role="L", base=2, sole="K0")
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        grime(pants.strip, "L0", 8, 10, speck="L1")                       # furrow mud caked to the ankle
        lacing(pants.front, 1, 6, 10, "L4", "L1")
        pants.strip.hline(0, pants.strip.w - 1, 11, "K0")
        for x in range(0, pants.strip.w, 2):
            pants.strip.set(x, 11, "M1")                                   # hobnails at the sole edge
    for ring in leg_rings(g, "boot_turn", 4.4, "L", (5, 2, 5), 3, "leather", 35385, inflate=.12):
        for face in ring.sides:
            face.hline(0, face.w - 1, 1, "L1")
    for ring in leg_rings(g, "braies_bunch", 3.2, "S", (5, 1, 5), 3, "weave", 35387, inflate=.2):
        for face in ring.sides:
            for x in range(0, face.w, 2):
                face.set(x, 0, "S2")
