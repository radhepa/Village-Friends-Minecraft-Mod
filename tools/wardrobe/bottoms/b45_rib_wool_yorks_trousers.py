"""Rib-Wool Yorks Trousers: ribbed wool trousers hitched below the knee with buckled leather yorks, over heavy boots."""
from kit import SIDES, footwear, legs, waistband
from kit_male import leg_rings

META = {
    "name": "Rib-Wool Yorks Trousers",
    "gender": "male",
    "description": "Ribbed wool field trousers hitched below the knee with buckled leather straps to keep the hems from the furrow.",
    "tags": ["work", "sturdy"],
}


def build(g):
    legs(g, "P", "rib", 4511, rows=(0, 9), crease=False)
    waistband(g, "P", "rib", 4512)
    footwear(g, "boot", top=9, base=2)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for x in range(leg.strip.w):
            if x % 2 == 0:
                leg.strip.set(x, 4, "P3")                                  # cloth bunched above the strap
        leg.strip.hline(0, leg.strip.w - 1, 6, "P1")
    for ring in leg_rings(g, "yorks", 5.0, "L", (5, 1, 5), 2, "leather", 4513, inflate=.06):
        ring.front.set(2, 0, "M3")
