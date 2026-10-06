"""Knee Breeches & Buckle Shoes: tailored breeches buckled below the knee, pale stockings, buckle shoes."""
from kit import SIDES, footwear, leg_bone, legs, stockings, waistband
from paint import solid

META = {
    "name": "Knee Breeches & Buckle Shoes",
    "gender": "male",
    "description": "Tailored breeches buckled below the knee, pale stockings and polished buckle shoes.",
    "tags": ["fancy", "tailored"],
}


def build(g):
    legs(g, "P", "velvet", 2701, rows=(0, 5))
    waistband(g, "P", "velvet", 2702)
    stockings(g, "S", (6, 9), base=4)
    for side in SIDES:
        g.part(f"{side}_leg").strip.hline(0, 15, 5, "P1")
        buckle = g.piece(f"{side}_knee_buckle", leg_bone(side), (-.5, -.5, -.5), (1, 1, 1),
                         pivot=(-2.2 if side == "right" else 2.2, 5.4, -.6), inflate=.08)
        solid(buckle, "M", "smooth", 2703, 3, edge=False)
    footwear(g, "shoe", top=10, base=1)
    for side in SIDES:
        g.part(f"{side}_pants").front.set(1, 10, "M3"), g.part(f"{side}_pants").front.set(2, 10, "M4")
