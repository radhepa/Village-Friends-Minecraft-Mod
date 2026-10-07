"""Traveller's Bound-Hem Skirt: a calf-length wool skirt bound in leather against the mud, over leg wraps and walking boots."""
from kit import SIDES
from kit_female import shoes, skirt, splotch, wraps
from paint import solid

META = {
    "name": "Traveller's Bound-Hem Skirt",
    "gender": "female",
    "description": "A dark calf-length skirt with a leather-bound hem against the mud, leg wraps, walking boots and a waterskin.",
    "tags": ["sturdy", "rugged", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 13311, base=1, top=9.8, length=9)
    s.band(1, "line", "L2", from_bottom=True)
    s.band(0, "line", "L1", from_bottom=True)
    s.paint(lambda f: splotch(f, "L1", 13312 + f.x0, count=2, y0=f.h - 4, y1=f.h - 3, size=1))
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        wraps(leg.strip, 6, 8, "S", 2)
    shoes(g, "boot", "L", 2, top=9)
    skin = g.piece("waist_waterskin", "TORSO", (-.5, 0, -1.5), (1, 4, 3), pivot=(-5.8, 9.6, .4))
    solid(skin, "L", "leather", 13313, 3)
    skin.right.hline(0, 2, 0, "L1"), skin.right.set(1, 2, "L4")
