"""Ploughman's Smock Frock: a long linen smock frock with honeycomb smocking, embroidered boxes and a flat collar."""
from kit import body, collar, flaps, neckline, sleeves
from kit_male import blk, ribbing
from paint import grid

META = {
    "name": "Ploughman's Smock Frock",
    "gender": "male",
    "description": "A knee-length linen smock frock, honeycomb smocking on chest and back, embroidered side boxes and a flat stitched collar.",
    "tags": ["casual", "simple", "work"],
    "covers_waist": True,
}

BOX = ["a.",
       ".a",
       "a.",
       ".a"]


def honeycomb(face, x0, x1, y0, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            face.set(x, y, "S2" if (x + y // 2) % 2 else "S3")


def build(g):
    b = body(g, "S", "weave", 4501, base=3)
    neckline(b.front, "keyhole", "S", base=3)
    for face in (b.front, b.back):
        honeycomb(face, 2, 5, 1, 7)
        face.hline(2, 5, 8, "S1")
        grid(face, 0, 2, BOX, {"a": "A2"}), grid(face, 6, 2, BOX, {"a": "A2"})
    sleeves(g, "S", "weave", 4502, base=3, rows=(0, 10))
    for side in ("right", "left"):
        ribbing(g.part(f"{side}_arm").strip, "S", 3, rows=range(7, 10))     # smocked cuffs
    flat = collar(g, "flat_collar", "S", "weave", base=3, height=1, y=-.6)
    flat.front.set(0, 0, "A2"), flat.front.set(8, 0, "A2"), flat.front.set(4, 0, "S1")
    for face in flaps(g, "frock", 7, "S", "weave", 4503, base=3, top=11.2):
        for x in range(0, 9, 2):
            face.vline(x, 0, 2, "S2")                                    # gathers under the smocking
        face.hline(0, 8, 6, "S2")
    for name, x in (("frock_right", -5.0), ("frock_left", 4.0)):
        blk(g, name, (x + .5, 11.2, 0), (1, 6, 4), "S", 3, "weave", 4504)
