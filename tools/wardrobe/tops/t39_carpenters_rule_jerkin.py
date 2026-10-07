"""Carpenter's Rule Jerkin: a sleeveless tweed jerkin with a chest pocket holding a folding rule and a flat pencil."""
from kit import body, neckline, roll, sleeves
from kit_male import blk, buttons
from paint import fabric

META = {
    "name": "Carpenter's Rule Jerkin",
    "gender": "male",
    "description": "A sleeveless tweed jerkin over a pushed-up shirt, a folding rule and flat pencil in the pocket and a try-square at the hip.",
    "tags": ["work", "casual"],
}


def build(g):
    b = body(g, "S", "weave", 3901, base=3)
    neckline(b.front, "round", "S", base=3)
    sleeves(g, "S", "weave", 3902, base=3, rows=(0, 6))
    roll(g, "S", 4.2, base=3)
    jacket = body(g, "P", "tweed", 3903, layer="jacket")
    jf = jacket.front
    jf.clear(3, 0), jf.clear(4, 0), jf.clear(3, 1), jf.clear(4, 1)
    jf.vline(3, 2, 11, "P1"), jf.vline(4, 2, 11, "P3")
    buttons(jf, 3, 3, 9, 2, "L3")
    # Patch pocket on the left breast, stitched in a lighter thread.
    jf.hline(4, 6, 3, "P3"), jf.vline(4, 3, 5, "P3"), jf.vline(6, 3, 5, "P3"), jf.hline(4, 6, 5, "P1")
    for face in jacket.sides:
        face.hline(0, face.w - 1, 11, "P1")
    rule = blk(g, "folding_rule", (1.0, 1.6, -2.55), (1, 3, 1), "S", 4, "plain", 3904, edge=False)
    for y in (0, 2):
        rule.front.set(0, y, "K2")
    pencil = blk(g, "flat_pencil", (2.0, 2.0, -2.55), (1, 2, 1), "A", 2, "plain", 3905, edge=False)
    pencil.front.set(0, 0, "K2")
    # A try-square hung from the hip: a wooden stock and a steel blade.
    stock = blk(g, "square_stock", (-3.2, 8.8, -2.65), (1, 4, 1), "L", 3, "plain", 3906)
    stock.front.set(0, 0, "M3")
    blade = blk(g, "square_blade", (-2.2, 11.4, -2.65), (2, 1, 1), "M", 3, "smooth", 3907, edge=False)
    blade.front.set(1, 0, "M4")
