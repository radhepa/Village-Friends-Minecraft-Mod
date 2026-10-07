"""Steppe Rider's Deel Coat: a crossover riding coat fastened at the right shoulder with toggles, cuffed sleeves and a broad sash."""
from kit import body, collar, flaps, sleeves
from kit_male import blk, sash
from paint import line

META = {
    "name": "Steppe Rider's Deel Coat",
    "gender": "male",
    "description": "A steppe rider's crossover deel fastened at the right shoulder with cloth toggles, long hoof cuffs, a broad sash and a flint pouch.",
    "tags": ["rugged", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "velvet", 8701)
    f = b.front
    line(f, 1, 0, 1, 4, "A2"), line(f, 1, 4, 7, 6, "A2")                 # the curved overlap edge
    line(f, 1, 1, 7, 5, "P1")
    for x, y in ((1, 1), (1, 3), (4, 5)):
        f.set(x + 1, y, "S4")                                            # cloth toggles
    sleeves(g, "P", "velvet", 8702, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "A2"), arm.strip.hline(0, arm.strip.w - 1, 10, "A3")
        arm.front.set(1, 11, "A2"), arm.front.set(2, 11, "A2")           # the hoof cuff over the knuckles
    stand = collar(g, "stand_collar", "A", "plain", base=2, height=1, y=-.6)
    stand.front.set(4, 0, "A1")
    sash(g, "broad_sash", "A", y=8.6, height=2, texture="plain", seed=8703, tails=((2.8, 0),), tail_len=3)
    pouch = blk(g, "flint_pouch", (-3.0, 10.6, -2.85), (2, 2, 1), "L", 2, "leather", 8705)
    pouch.front.set(0, 0, "M3")
    for face in flaps(g, "deel_skirt", 6, "P", "velvet", 8706, top=10.6, slit=True):
        face.hline(0, 8, 5, "A2")
