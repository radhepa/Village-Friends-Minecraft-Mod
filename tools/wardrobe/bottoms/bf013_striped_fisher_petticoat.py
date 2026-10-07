"""Striped Fisher Petticoat: a short striped petticoat for the shingle, worn over tall oiled sea boots."""
from kit_female import leg_ring_fold, shoes, skirt

META = {
    "name": "Striped Fisher Petticoat",
    "gender": "female",
    "description": "A calf-length linen petticoat banded in sea stripes, over tall oiled sea boots with folded tops.",
    "tags": ["sea", "sturdy", "skirt"],
}


def build(g):
    s = skirt(g, "S", "weave", 11311, base=3, top=9.8, length=8)
    s.band(1, "line", "P2", from_bottom=True)
    s.band(3, "line", "P2", from_bottom=True)
    s.band(4, "line", "P1", from_bottom=True)
    s.hem("S2")
    shoes(g, "boot", "L", 1, top=6)
    leg_ring_fold(g, "boot_fold", 5.6, "L", 2)
