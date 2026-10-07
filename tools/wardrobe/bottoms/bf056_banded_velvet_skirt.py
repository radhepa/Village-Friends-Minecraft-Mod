"""Banded Velvet Skirt: a velvet skirt ringed with three pairs of narrow gilt and colored guards, over black shoes."""
from kit_female import shoes, skirt

META = {
    "name": "Banded Velvet Skirt",
    "gender": "female",
    "description": "A velvet skirt ringed with three pairs of narrow gilt-and-colored guards, over black buckled shoes.",
    "tags": ["fancy", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "velvet", 15611, top=9.8, length=12)
    for y in (1, 5, 9):
        s.band(y, "line", "A2", from_bottom=True)
        s.band(y + 1, "line", "M3", from_bottom=True)
    shoes(g, "shoe", "K", 2)
    for side in ("right", "left"):
        g.part(f"{side}_pants").front.hline(1, 2, 10, "M4")
