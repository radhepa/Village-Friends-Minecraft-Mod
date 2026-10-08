"""Novgorod Side-Button Shirt: a long shirt with its neck slit set off to the side and buttoned, embroidered collar, cuffs and hem, and a tasselled cord belt."""
from kit import SIDES, body, flaps, sleeves
from kit_male import embroider
from kit_m08 import tassel
from paint import solid

META = {
    "name": "Novgorod Side-Button Shirt",
    "gender": "male",
    "description": "A long kosovorotka shirt with its neck slit set off to the left and buttoned, embroidered at the stand collar, cuffs and hem, belted with a woven cord ending in tassels.",
    "tags": ["casual", "simple"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 38481)
    f = b.front
    f.clear(3, 0), f.clear(4, 0), f.clear(5, 0)
    f.hline(0, 2, 0, "A2"), f.hline(6, 7, 0, "A2")                         # embroidered stand collar
    b.back.hline(0, 7, 0, "A2")
    embroider(b.back, 1, "dots", "A3", x0=1, x1=6)
    f.vline(5, 1, 4, "P0")                                                 # the slit, off to the left
    for y in range(1, 5):
        f.set(4, y, "A3" if y % 2 else "A1")                               # embroidered border
    f.set(6, 1, "M3"), f.set(6, 3, "M3")                                   # side buttons
    f.vline(1, 5, 11, "P1")
    sleeves(g, "P", "weave", 38482, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 8, "A1")
        embroider(arm.strip, 9, "zig", "A3", "A2")
        arm.front.vline(2, 2, 7, "P1")
    cord = g.piece("cord_belt", "TORSO", (-4.6, 9.4, -2.6), (9, 1, 5), inflate=.05)
    solid(cord, "A", "plain", 38483, 2, edge=False)
    for face in cord.sides:
        for x in range(face.w):
            face.set(x, 0, "A3" if x % 2 else "A1")                       # twisted cord
    tassel(g, "belt_tassel_0", (2.6, 10.2, -3.35), "A", length=3, cord="A1")
    tassel(g, "belt_tassel_1", (3.4, 10.2, -3.25), "A", length=2, cord="A1")
    for face in flaps(g, "shirt_hem", 4, "P", "weave", 38484, top=10.6):
        embroider(face, 2, "step", "A3", "A1")
