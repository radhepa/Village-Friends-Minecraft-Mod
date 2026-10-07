"""Gathered Wool Skirt: an ankle-length wool skirt gathered at the hip with a contrasting guard band."""
from kit_female import shoes, skirt

META = {
    "name": "Gathered Wool Skirt",
    "gender": "female",
    "description": "Ankle-length wool skirt gathered at the hips, a cream guard band above the hem and soft turnshoes.",
    "tags": ["casual", "simple", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 10111, top=9.8, length=12)
    s.band(2, "line", "S3", from_bottom=True)
    s.band(1, "line", "S2", from_bottom=True)
    s.band(0, "line", "P1", from_bottom=True)
    shoes(g, "turnshoe", "L", 2)
