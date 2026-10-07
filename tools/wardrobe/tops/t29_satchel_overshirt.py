"""Satchel & Overshirt: an open overshirt over a linen shirt, sleeves rolled, a big satchel at the hip."""
from kit import body, neckline, roll, sleeves
from paint import line, solid

META = {
    "name": "Satchel & Overshirt",
    "gender": "male",
    "description": "An open, sleeves-rolled overshirt over a linen shirt, with a deep leather satchel on a cross strap.",
    "tags": ["casual", "work"],
}


def build(g):
    b = body(g, "S", "weave", 2901, base=3)
    neckline(b.front, "round", "S", base=3)
    over = body(g, "P", "twill", 2902, layer="jacket")
    of = over.front
    for y in range(12):
        for x in (2, 3, 4, 5):
            of.clear(x, y)
        of.set(1, y, "P3"), of.set(6, y, "P1")
    of.set(0, 3, "P1"), of.set(7, 3, "P1")   # breast pocket seams
    line(of, 7, 0, 6, 2, "L2")
    line(over.back, 0, 0, 7, 9, "L2")
    over.top.vline(6, 0, 3, "L2")
    sleeves(g, "P", "twill", 2903, rows=(0, 5))
    roll(g, "P", 2.6, base=3)
    strap = g.piece("satchel_strap", "TORSO", (-.5, 0, -.5), (1, 9, 1), pivot=(2.6, -.2, -2.75), rotation=(0, 0, 32))
    solid(strap, "L", "leather", 2904, 2, edge=False)
    bag = g.piece("satchel", "TORSO", (-2, 0, -1), (4, 4, 2), pivot=(-3.6, 8.2, -1.2), rotation=(0, -20, 0))
    solid(bag, "L", "leather", 2905, 2)
    bag.front.hline(0, 3, 0, "L3"), bag.front.hline(0, 3, 1, "L3"), bag.front.set(2, 2, "M3")
    bag.front.hline(0, 3, 3, "L1")
