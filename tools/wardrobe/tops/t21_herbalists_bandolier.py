"""Herbalist's Bandolier: a rolled-sleeve shirt crossed by a leather bandolier of corked vials and pouches."""
from kit import body, neckline, roll, sleeves
from paint import k, line, solid

META = {
    "name": "Herbalist's Bandolier",
    "description": "A work shirt crossed by a leather bandolier of corked vials, with pouches and a sprig of herbs.",
    "tags": ["casual", "work"],
    "tucked": True,
}


def build(g):
    b = body(g, "P", "twill", 2101)
    neckline(b.front, "laced", "P")
    sleeves(g, "P", "twill", 2102, rows=(0, 5))
    roll(g, "P", 2.6, base=3)
    jacket = g.part("jacket")
    jf, jb = jacket.front, jacket.back
    line(jf, 1, 0, 6, 10, "L2"), line(jf, 0, 0, 5, 10, "L1")
    line(jb, 6, 0, 1, 10, "L2"), line(jb, 7, 0, 2, 10, "L1")
    jacket.top.vline(1, 0, 3, "L2")
    # Corked vials riding the strap, glass in the accent color.
    for i, (x, y) in enumerate(((-2.6, 1.6), (-1.4, 3.4), (-.2, 5.2))):
        vial = g.piece(f"vial_{i}", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(x, y, -2.75), inflate=.05)
        solid(vial, "A", "plain", 2103 + i, 3, edge=False)
        vial.front.set(0, 0, "A4"), vial.front.set(0, 1, "A2")
        cork = g.piece(f"vial_cork_{i}", "TORSO", (-.5, -1, -.5), (1, 1, 1), pivot=(x, y, -2.75))
        solid(cork, "L", "leather", 2110 + i, 3, edge=False)
    pouch = g.piece("bandolier_pouch", "TORSO", (-1, 0, -.5), (2, 2, 1), pivot=(1.8, 7.0, -2.85))
    solid(pouch, "L", "leather", 2120, 2)
    pouch.front.hline(0, 1, 0, "L3"), pouch.front.set(1, 1, "M3")
    sprig = g.piece("herb_sprig", "TORSO", (-.5, -2, -.5), (1, 2, 1), pivot=(2.3, 7.0, -2.85), rotation=(0, 0, -14))
    solid(sprig, "S", "plain", 2121, 2, edge=False)
    sprig.front.set(0, 0, "A3"), sprig.strip.hline(0, sprig.strip.w - 1, 0, "S3")
