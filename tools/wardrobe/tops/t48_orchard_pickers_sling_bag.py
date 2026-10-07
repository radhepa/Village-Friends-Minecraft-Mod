"""Orchard Picker's Sling Bag: a twill tunic with a canvas picking bag slung on the belly, apples heaped at its mouth."""
from kit import body, neckline, sleeves
from kit_male import blk
from paint import line, solid

META = {
    "name": "Orchard Picker's Sling Bag",
    "gender": "male",
    "description": "A twill harvest tunic with a canvas picking bag slung on the belly from crossed straps, apples heaped at its mouth.",
    "tags": ["casual", "work"],
}


def build(g):
    b = body(g, "P", "twill", 4801)
    neckline(b.front, "round", "P")
    sleeves(g, "P", "twill", 4802, rows=(0, 10), cuff="P1")
    for face in b.sides:
        face.hline(0, face.w - 1, 11, "P1")
    jacket = g.part("jacket")
    jacket.front.vline(1, 0, 5, "S2"), jacket.front.vline(6, 0, 5, "S2")
    for y in range(4):
        jacket.top.set(1, y, "S2"), jacket.top.set(6, y, "S2")
    line(jacket.back, 1, 0, 6, 8, "S2"), line(jacket.back, 6, 0, 1, 8, "S1")
    bag = g.piece("picking_bag", "TORSO", (-3, 0, -3), (6, 4, 3), pivot=(0, 6.2, -2.2), inflate=.05)
    solid(bag, "S", "twill", 4803, 2)
    for face in bag.sides:
        face.hline(0, face.w - 1, 0, "S3"), face.hline(0, face.w - 1, 1, "S1")   # drawn mouth
    bag.front.vline(2, 2, 3, "S1")
    bag.top.fill("S0")
    for i, (x, z) in enumerate(((-1.4, -4.0), (.2, -4.4), (1.5, -3.6))):
        apple = blk(g, f"apple_{i}", (x, 5.5, z), (1, 1, 1), "A", 2 + (i % 2), "plain", 4804 + i, edge=False)
        apple.top.fill("A4" if i != 1 else "L2")
