"""Market Stallholder's Striped Skirt: an ankle-length skirt woven in broad upright stripes like a stall
awning, banded at the hem with a plain guard, over wooden clogs."""
from kit import SIDES
from kit_female import shoes, skirt, stripes

META = {
    "name": "Market Stallholder's Striped Skirt",
    "gender": "female",
    "description": "An ankle-length skirt in broad upright awning stripes with a plain guard at the hem, over wooden clogs.",
    "tags": ["casual", "simple", "skirt", "long_skirt"],
}

SEED = 53285


def awning(face):
    stripes(face, ["S3", "S3", "P2", "P2"], 1, vertical=True, y0=1, h=face.h - 4)
    for x in range(face.w):
        if face.get(x, 1) == "P2" and face.get(x - 1, 1) == "S3":
            face.vline(x, 2, face.h - 4, "P1")                       # a soft shadow beside each stripe
    face.hline(0, face.w - 1, 0, "P3")
    face.hline(0, face.w - 1, face.h - 3, "P3")                       # the plain guard band
    face.hline(0, face.w - 1, face.h - 2, "P2")
    face.hline(0, face.w - 1, face.h - 1, "P1")


def build(g):
    s = skirt(g, "P", "weave", SEED, top=9.8, length=12, flare=6, folds=False, gather=False)
    s.paint(awning)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        stripes(leg.strip, ["S2", "S2", "P1", "P1"], 1, vertical=True, y0=0, h=9)
    shoes(g, "clog", "L", 2)
