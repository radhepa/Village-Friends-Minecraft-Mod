"""Clay-Splashed Skirt: a skirt splashed with slip from the potter's wheel, its damp hem darker, over soft mules."""
from kit_female import shoes, skirt, splotch, stockings_row

META = {
    "name": "Clay-Splashed Skirt",
    "gender": "female",
    "description": "A skirt splashed with grey slip from the potter's wheel, its damp hem dark, over grey stockings and mules.",
    "tags": ["work", "skirt"],
}


def build(g):
    s = skirt(g, "P", "weave", 14911, top=9.8, length=10)
    s.paint(lambda f: splotch(f, "L3", 14912 + f.x0, count=3, y0=2, y1=f.h - 3, size=1))
    splotch(s.front.front, "L2", 14913, count=3, y0=3, y1=7, size=2)
    s.band(0, "line", "P0", from_bottom=True)
    s.band(1, "line", "P1", from_bottom=True)
    stockings_row(g, "S", 8, 9, base=1)
    shoes(g, "slipper", "L", 2)
