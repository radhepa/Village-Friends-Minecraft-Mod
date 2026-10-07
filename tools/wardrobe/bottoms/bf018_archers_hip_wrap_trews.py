"""Archer's Hip-Wrap & Trews: close trews with criss-cross garters under a short wrap skirt tied at the hip."""
from kit import SIDES, legs
from kit_female import shoes, skirt, waist_belt
from paint import line

META = {
    "name": "Archer's Hip-Wrap & Trews",
    "gender": "female",
    "description": "Close wool trews criss-crossed with leather garters, under a short wrap skirt tied at the hip.",
    "tags": ["rugged", "sturdy"],
}


def build(g):
    s = skirt(g, "S", "weave", 11811, base=2, top=9.6, length=5, flare=9, folds=False)
    line(s.front.front, 8, 0, 4, 4, "S1"), line(s.front.front, 9, 0, 5, 4, "S3")   # the wrap's crossing edge
    s.hem("S1")
    legs(g, "P", "twill", 11812, rows=(3, 9), crease=False)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        strip = pants.strip
        for y in range(4, 10):
            for x in range(strip.w):
                if (x + y) % 6 == 0 or (x - y) % 6 == 0:
                    strip.set(x, y, "L2" if (x + y) % 6 == 0 else "L1")     # garters crossing in an open lattice
        strip.hline(0, strip.w - 1, 4, "L1")
    shoes(g, "turnshoe", "L", 2)
    waist_belt(g, "waist_belt", 9.3, height=1)
