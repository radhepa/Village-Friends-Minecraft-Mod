"""Fletcher's Feather Vest: a waxed vest with a breast pouch bristling with feathers and a spool of waxed thread at the belt."""
from kit import roll
from kit_female import chemise, girdle, neck
from paint import fabric, solid, strip_fabric

META = {
    "name": "Fletcher's Feather Vest",
    "gender": "female",
    "description": "A waxed canvas vest with a breast pouch bristling with goose feathers, rolled sleeves and a thread spool.",
    "tags": ["rugged", "work"],
}


def build(g):
    chemise(g, "S", 3, "weave", 14701, neckline="v", sleeve_rows=(0, 6))
    roll(g, "S", 3.6, base=3)
    j = g.part("jacket")
    strip_fabric(j, "L", "smooth", 14702, 2, 0, 9)
    fabric(j.top, "L", "smooth", 14702, 3)
    neck(j.front, "deep_v", "L", 2)
    for y in range(4, 10):
        j.front.set(3, y, "L1")
    for face in j.sides:
        face.hline(0, face.w - 1, 9, "L1")
    pouch = g.piece("feather_pouch", "TORSO", (-1.5, 0, -.5), (3, 3, 1), pivot=(-2.2, 3.2, -2.75))
    solid(pouch, "L", "leather", 14703, 2)
    pouch.front.hline(0, 2, 0, "L3")
    for i, (dx, key, h) in enumerate(((-.9, "S4", 3), (0, "A3", 4), (.9, "P3", 3))):
        feather = g.piece(f"feather_{i}", "TORSO", (-.5, -h, -.5), (1, h, 1), pivot=(-2.2 + dx, 3.4, -2.6), rotation=(0, 0, dx * 10))
        solid(feather, key[0], "plain", 14704 + i, int(key[1]), edge=False)
        feather.front.set(0, h - 1, "S2")
    girdle(g, "belt", 8.0, role="L", base=1, height=1)
    spool = g.piece("thread_spool", "TORSO", (-1, 0, -.5), (2, 2, 1), pivot=(2.6, 7.6, -3.0), inflate=.05)
    solid(spool, "S", "plain", 14707, 3)
    spool.front.hline(0, 1, 0, "L3"), spool.front.hline(0, 1, 1, "A2")
