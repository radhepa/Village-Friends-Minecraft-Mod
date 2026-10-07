"""Tiered Linen Skirt: a light linen skirt in two gathered tiers, with leather shoes strapped across the instep."""
from kit import SIDES
from kit_female import gathers, shoes, skirt, tier

META = {
    "name": "Tiered Linen Skirt",
    "gender": "female",
    "description": "A breezy two-tier linen skirt with gathered seams and strapped leather shoes.",
    "tags": ["casual", "relaxed", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "S", "weave", 10511, base=3, top=9.8, length=12)
    for f in tier(g, s, "tier", 6, 6, role="S", texture="weave", seed=10512, base=3, grow=2):
        gathers(f, "S", 3, 0, 1)
        f.hline(0, f.w - 1, 0, "A2")
        f.hline(0, f.w - 1, f.h - 1, "S1")
    shoes(g, "shoe", "L", 2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.hline(0, 3, 10, "A2")
        pants.right.set(3, 10, "A2"), pants.left.set(0, 10, "A2")
