"""Huntress's Leather Vest: a side-laced leather vest with a fur collar over a laced-cuff shirt, a knife on the chest strap."""
from kit_female import chemise, fur_box, girdle, side_lacing, wraps
from paint import fabric, line, solid, strip_fabric

META = {
    "name": "Huntress's Leather Vest",
    "gender": "female",
    "description": "A side-laced leather vest with a fur collar over a linen shirt, wrapped cuffs and a knife on the chest strap.",
    "tags": ["rugged", "martial"],
}


def build(g):
    body, arms = chemise(g, "S", 2, "weave", 11701, neckline="slit", sleeve_rows=(0, 10), gather=False)
    for arm in arms:
        wraps(arm.strip, 7, 10, "L", 2)                               # thong-wrapped forearms
    j = g.part("jacket")
    strip_fabric(j, "L", "leather", 11702, 2, 0, 10)
    fabric(j.top, "L", "leather", 11702, 3)
    for x, y in [(3, 0), (4, 0), (3, 1), (4, 1), (3, 2), (4, 2), (4, 3)]:
        j.front.clear(x, y)
    j.front.vline(2, 0, 3, "L3"), j.front.vline(5, 0, 3, "L1")
    side_lacing(j, 2, 9, lace="S3", under="L0")
    for face in j.sides:
        face.hline(0, face.w - 1, 10, "L1")
    line(j.front, 6, 0, 1, 8, "L1")                                   # chest strap
    collar = g.piece("fur_collar", "TORSO", (-4.6, -1.3, -2.7), (9, 2, 5), inflate=.08)
    fur_box(collar, "S", 11703, 3)
    sheath = g.piece("chest_knife", "TORSO", (-.5, 0, -.5), (1, 4, 1), pivot=(1.0, 2.6, -2.75), rotation=(0, 0, 32))
    solid(sheath, "L", "leather", 11704, 1)
    hilt = g.piece("chest_knife_hilt", "TORSO", (-.5, -2, -.5), (1, 2, 1), pivot=(1.0, 2.6, -2.75), rotation=(0, 0, 32))
    solid(hilt, "M", "smooth", 11705, 3)
    girdle(g, "belt", 8.0, role="L", base=1, height=1)
