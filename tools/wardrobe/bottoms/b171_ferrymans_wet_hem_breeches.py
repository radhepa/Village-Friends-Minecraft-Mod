"""Ferryman's Wet-Hem Breeches: wool breeches soaked dark from the knee bands up, dripping onto knitted stockings
above low shoes."""
from kit import SIDES, legs, waistband
from kit_m03 import drips, knit_stockings, low_shoes, soak
from kit_male import leg_rings

META = {
    "name": "Ferryman's Wet-Hem Breeches",
    "gender": "male",
    "description": "Wool breeches soaked dark from the buttoned knee bands upward, dripping down knitted stockings onto "
                   "low leather shoes.",
    "tags": ["casual", "sea", "simple"],
}


def build(g):
    legs(g, "P", "weave", 33020, rows=(0, 6), crease=False)
    body = waistband(g, "P", "weave", 33021)
    body.front.vline(4, 9, 11, "P1")
    body.front.set(4, 10, "M3")
    knit_stockings(g, "S", (7, 9), base=3, seed=33022)
    low_shoes(g, "L", 2, top=10, seed=33023)
    for side in SIDES:
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        soak(leg.strip, "P", range(2, 7), seed=33024)
        drips(leg.strip, (1, 3, 6, 9, 13), 7, "S1", 33025)
        for face in pants.sides:
            face.set(1, 10, "L4")                                         # wet glint on the shoe
    for ring in leg_rings(g, "knee_band", 6.0, "P", (5, 1, 5), 0, "weave", 33026, inflate=.06):
        for face in ring.sides:
            face.hline(0, face.w - 1, 0, "P1")
        ring.front.set(2, 0, "M3")
        ring.bottom.fill("P0")
