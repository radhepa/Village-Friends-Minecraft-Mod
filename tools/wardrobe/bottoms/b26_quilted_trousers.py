"""Quilted Padded Trousers: warm diamond-quilted trousers with boots, the civilian cousin of chausses."""
from kit import footwear, legs, waistband

META = {
    "name": "Quilted Trousers",
    "gender": "male",
    "description": "Warm, diamond-quilted padded trousers over plain leather boots.",
    "tags": ["casual", "sturdy", "martial"],
}


def build(g):
    legs(g, "S", "quilt", 2601, base=3, rows=(0, 8), crease=False)
    waistband(g, "S", "quilt", 2602, base=3)
    footwear(g, "boot", top=8)
