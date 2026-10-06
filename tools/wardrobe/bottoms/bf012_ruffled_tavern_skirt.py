"""Ruffled Tavern Skirt: a swishing mid-calf skirt with a ruffled flounce, striped stockings and buckled black shoes."""
from kit import SIDES
from kit_female import shoes, skirt, stripes, tier

META = {
    "name": "Ruffled Tavern Skirt",
    "gender": "female",
    "description": "A mid-calf skirt finished with a ruffled flounce, over striped stockings and buckled black shoes.",
    "tags": ["casual", "whimsical", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 11211, top=9.8, length=8)
    for f in tier(g, s, "ruffle", 6, 3, role="P", seed=11212, grow=2):
        for x in range(f.w):
            f.set(x, 0, "P1" if x % 2 else "P3")
            f.set(x, 1, "P1" if x % 2 else "P2")
            f.set(x, 2, "P3" if x % 2 else "P1")
        f.hline(0, f.w - 1, f.h - 1, "A2")
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        stripes(leg.strip, ["S4", "A2"], 1, y0=6, h=4)
    shoes(g, "shoe", "K", 2)
    for side in SIDES:
        g.part(f"{side}_pants").front.hline(1, 2, 10, "M3")
