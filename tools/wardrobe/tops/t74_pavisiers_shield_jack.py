"""Pavisier's Shield Jack: a padded jack with a tall painted pavise shield slung on the back by a strap, and a falchion."""
from kit import belt, body, sleeves
from kit_male import blk
from paint import line, solid

META = {
    "name": "Pavisier's Shield Jack",
    "gender": "male",
    "description": "A shield-bearer's padded jack with a tall painted pavise slung across the back on a strap, and a short falchion.",
    "tags": ["martial", "rugged"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "quilt", 7401)
    b.front.vline(4, 0, 11, "P0")
    sleeves(g, "P", "quilt", 7402, rows=(0, 10), cuff="L2")
    jacket = g.part("jacket")
    line(jacket.front, 0, 0, 7, 8, "L2"), line(jacket.back, 7, 0, 0, 8, "L2")
    belt(g, "belt", 9.6)
    # The pavise: a tall rectangular shield with a raised central ridge and a painted stripe.
    pavise = g.piece("pavise", "TORSO", (-4, 0, 0), (8, 12, 1), pivot=(0, -.6, 3.0), rotation=(6, 0, 0))
    solid(pavise, "S", "plain", 7403, 3)
    f = pavise.back
    for y in range(12):
        f.set(3, y, "A2"), f.set(4, y, "A2")
    f.vline(0, 0, 11, "L2"), f.vline(7, 0, 11, "L2"), f.hline(0, 7, 0, "L3"), f.hline(0, 7, 11, "L1")
    f.set(3, 5, "M3"), f.set(4, 5, "M3"), f.set(3, 6, "M2"), f.set(4, 6, "M2")
    ridge = g.piece("pavise_ridge", "TORSO", (-1, 0, 0), (2, 12, 1), pivot=(0, -.6, 4.0), rotation=(6, 0, 0))
    solid(ridge, "A", "plain", 7404, 2)
    ridge.back.vline(0, 0, 11, "A3")
    blade = blk(g, "falchion", (-3.4, 10.6, -2.6), (1, 5, 2), "M", 3, "smooth", 7405, rotation=(0, 0, -6))
    blade.strip.hline(0, blade.strip.w - 1, 0, "L2")
