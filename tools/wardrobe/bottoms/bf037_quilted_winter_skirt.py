"""Quilted Winter Skirt: a thick diamond-quilted skirt for the cold months, over fur-topped boots."""
from kit_female import fur_box, leg_rings, shoes, skirt

META = {
    "name": "Quilted Winter Skirt",
    "gender": "female",
    "description": "A thick diamond-quilted wool skirt for deep winter, over fur-topped boots.",
    "tags": ["rugged", "skirt"],
}


def build(g):
    s = skirt(g, "P", "quilt", 13711, top=9.8, length=10, folds=False)
    s.band(0, "line", "P0", from_bottom=True)
    shoes(g, "boot", "L", 1, top=7)
    for ring in leg_rings(g, "fur_top", 7.3, 2, 5, inflate=.12):
        fur_box(ring, "S", 13712, 3)
