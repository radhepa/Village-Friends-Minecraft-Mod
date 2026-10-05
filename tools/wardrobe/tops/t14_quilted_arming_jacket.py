"""Quilted Arming Jacket: a civilian gambeson, diamond-quilted, toggled up the front with a standing collar."""
from kit import body, collar, flaps, sleeves
from paint import fabric

META = {
    "name": "Quilted Arming Jacket",
    "description": "A padded, diamond-quilted jacket with leather toggles and a standing collar.",
    "tags": ["casual", "martial"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "S", "quilt", 1401, base=3)
    jacket = body(g, "S", "quilt", 1402, base=3, layer="jacket")
    jf = jacket.front
    jf.vline(4, 0, 11, "S1"), jf.vline(3, 0, 11, "S3")
    for y in (2, 4, 6, 8):
        jf.set(3, y, "L3"), jf.set(4, y, "L2"), jf.set(5, y, "L1")
    sleeves(g, "S", "quilt", 1403, base=3, rows=(0, 10), cuff="S1")
    sleeves(g, "S", "quilt", 1404, base=3, rows=(0, 5), layer="sleeve")
    c = collar(g, "collar", "S", "quilt", base=3, height=2, y=-1.2)
    c.front.set(4, 1, "L2")
    front, back = flaps(g, "skirt", 3, "S", "quilt", 1405, base=3, top=11.2, hem="S1")
    front.vline(4, 0, 2, "S0")
