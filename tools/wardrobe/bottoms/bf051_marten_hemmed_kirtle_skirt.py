"""Marten-Hemmed Kirtle Skirt: a pale floor-length kirtle skirt edged in a deep band of brown marten fur."""
from kit_female import fur, shoes, skirt, sub

META = {
    "name": "Marten-Hemmed Kirtle Skirt",
    "gender": "female",
    "description": "A pale floor-length kirtle skirt edged with a deep band of brown marten fur, over black pointed shoes.",
    "tags": ["fancy", "skirt", "long_skirt"],
}


def build(g):
    s = skirt(g, "S", "weave", 15111, base=3, top=9.8, length=12)
    s.paint(lambda f: fur(sub(f, 0, f.h - 3, f.w, 3), "L", 15112 + f.x0, 2))
    shoes(g, "pointed", "K", 2)
