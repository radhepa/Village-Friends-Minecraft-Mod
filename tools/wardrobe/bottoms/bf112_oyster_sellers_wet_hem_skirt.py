"""Oyster Seller's Wet-Hem Skirt: a mid-calf wool skirt with a pale guard band, soaked dark to a ragged
tide line from wading out to the beds, over ribbed stockings and wooden clogs."""
from kit import SIDES
from kit_f03 import wet_hem
from kit_female import shoes, skirt
from paint import rnd

META = {
    "name": "Oyster Seller's Wet-Hem Skirt",
    "gender": "female",
    "description": "A mid-calf wool skirt soaked dark to a ragged tide line, a crust of salt above it, over ribbed stockings and clogs.",
    "tags": ["sea", "work", "skirt"],
}

SEED = 53075


def soak(face):
    face.hline(0, face.w - 1, face.h - 3, "S3")                    # the pale guard band
    face.hline(0, face.w - 1, face.h - 2, "S2")
    wet_hem(face, 4, SEED, deep_rows=1)
    top = face.h - 5
    for x in range(face.w):                                          # a crust of dried salt at the tide line
        if rnd(x + face.x0, 1, SEED) < .45 and face.get(x, top):
            face.set(x, top, "S4")
    for x in range(1, face.w, 4):                                    # water wicking up the weave
        face.set(x, top, "P1")


def build(g):
    s = skirt(g, "P", "weave", SEED, top=9.8, length=9, flare=6)
    s.paint(soak)
    for side in SIDES:
        leg = g.part(f"{side}_leg")
        for y in range(7, 10):
            for x in range(leg.strip.w):
                leg.strip.set(x, y, "S1" if x % 2 else "S2")       # ribbed stockings
    shoes(g, "clog", "L", 2)
    for side in SIDES:
        pants = g.part(f"{side}_pants")
        pants.front.hline(0, 3, 10, "L3")
        pants.front.set(1, 9, "L1"), pants.front.set(2, 9, "L1")
