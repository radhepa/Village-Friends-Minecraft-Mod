"""Tailor's Pinned Jacket: a fitted jacket bristling with pins, a measuring ribbon round the neck, wrist pincushion and shears."""
from kit import sleeves
from kit_female import girdle, hanging, neck
from paint import fabric, solid, strip_fabric

META = {
    "name": "Tailor's Pinned Jacket",
    "gender": "female",
    "description": "A neat fitted jacket with pins down the lapel, a marked measuring ribbon, a wrist pincushion and shears.",
    "tags": ["tailored", "casual"],
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "S", "weave", 12401, 3)
    neck(b.front, "v", "S", 3)
    j = g.part("jacket")
    strip_fabric(j, "P", "twill", 12402, 2, 0, 10)
    fabric(j.top, "P", "twill", 12402, 3)
    for x, y in [(2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (3, 2), (4, 2), (3, 3), (4, 3), (3, 4), (4, 4)]:
        j.front.clear(x, y)
    for y in range(0, 5):
        j.front.set(2, y, "P3"), j.front.set(5, y, "P1")              # lapels
    for y in (1, 2, 3):
        j.front.set(1, y, "M4")                                      # pins down the lapel
    j.front.vline(4, 5, 10, "P1"), j.front.set(3, 6, "M3"), j.front.set(3, 8, "M3")
    for face in j.sides:
        face.hline(0, face.w - 1, 10, "P1")
    sleeves(g, "P", "twill", 12403, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 10, "S3"), arm.strip.hline(0, 15, 11, "S2")
    cushion = g.piece("pincushion", "LEFT_ARM", (-1.2, 7.2, -2.5), (5, 2, 5), inflate=.08)
    solid(cushion, "A", "plain", 12404, 2)
    for face in cushion.sides + [cushion.top]:
        for x in range(0, face.w, 2):
            face.set(x, 0, "M4")
    for name, x in (("ribbon_right", -1.6), ("ribbon_left", 1.6)):
        rib = g.piece(name, "TORSO", (-.5, 0, -.5), (1, 8 if x < 0 else 6, 1), pivot=(x, -.2, -2.75))
        solid(rib, "S", "plain", 12405, 4)
        for y in range(0, rib.front.h, 2):
            rib.front.set(0, y, "K2")                                # inch marks
    neckband = g.piece("ribbon_neck", "TORSO", (-4.5, -.7, -2.6), (9, 1, 5), inflate=.04)
    solid(neckband, "S", "plain", 12406, 4, edge=False)
    girdle(g, "belt", 8.0, role="L", height=1)
    cord = hanging(g, "shears_cord", 3.4, 3, role="L", top=8.8)
    shears = g.piece("shears", "TORSO", (-1, 3, -.1), (2, 3, 1), pivot=(3.4, 8.8, -3.25), motion="flap_front")
    solid(shears, "M", "smooth", 12407, 3)
    shears.front.set(0, 0, "K2"), shears.front.set(1, 0, "K2"), shears.front.set(0, 2, "M4")
