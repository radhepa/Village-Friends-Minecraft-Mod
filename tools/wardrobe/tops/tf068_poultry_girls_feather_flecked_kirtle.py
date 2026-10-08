"""Poultry Girl's Feather-Flecked Kirtle: a plain kirtle caught all over with stray white feathers, a linen
collar band and an open grain pouch with its scoop at the girdle."""
from kit import body, sleeves
from kit_female import OVER_FRONT, girdle, lacing, neck
from paint import k, solid

META = {
    "name": "Poultry Girl's Feather-Flecked Kirtle",
    "gender": "female",
    "description": "A plain wool kirtle flecked all over with stray white feathers, a linen collar band and an open grain pouch with a wooden scoop at the girdle.",
    "tags": ["work", "casual", "simple"],
}

FEATHERS = {"front": [(1, 4), (5, 2), (6, 7), (2, 9)], "back": [(2, 3), (6, 5), (1, 8), (5, 10)],
            "right": [(1, 6)], "left": [(2, 3)]}
SLEEVE_FEATHERS = [(2, 3), (9, 6), (13, 2), (6, 9)]


def feather(face, x, y):
    """A small curled feather: a white vane, a shaded tip and the quill."""
    face.set(x, y, "S4"), face.set(x + 1, y - 1, "S4"), face.set(x + 1, y, "S3")
    face.set(x - 1, y + 1, "S2")


def build(g):
    b = body(g, "P", "weave", 51280)
    neck(b.front, "slit", "P", 2)
    lacing(b.front, 3, 1, 3, "spiral", lace="S4", under="P0", eyelet=None)
    for face in b.sides:
        face.hline(0, face.w - 1, 0, "S3")                             # the linen collar band
    b.front.set(2, 0, "S4"), b.front.set(5, 0, "S4")
    for name, spots in FEATHERS.items():
        for x, y in spots:
            feather(getattr(b, name), x, y)
    for arm in sleeves(g, "P", "weave", 51281, rows=(0, 11)):
        arm.strip.hline(0, 15, 10, "P1"), arm.strip.hline(0, 15, 11, "S3")
        for x, y in SLEEVE_FEATHERS:
            feather(arm.strip, x, y)
    girdle(g, "girdle", 7.6, role="L", height=1)
    # The grain pouch, its mouth open on the corn, a little wooden scoop stuck in it.
    pivot = (-2.4, 8.4, OVER_FRONT - .1)
    pouch = g.piece("grain_pouch", "TORSO", (-1.5, .4, -1.2), (3, 3, 2), pivot=pivot, motion="flap_front", inflate=.05)
    solid(pouch, "L", "leather", 51282, 2)
    pouch.top.fill("M3")
    pouch.top.set(0, 0, "M2"), pouch.top.set(2, 1, "M4")
    for f in pouch.sides:
        f.hline(0, f.w - 1, 0, "L3")
    pouch.front.set(1, 1, "L1"), pouch.front.set(0, 2, "L1")
    scoop = g.piece("grain_scoop", "TORSO", (.1, -1.4, -.8), (1, 2, 1), pivot=pivot, rotation=(0, 0, -16),
                    motion="flap_front")
    solid(scoop, "S", "smooth", 51283, 2, edge=False)
    scoop.top.fill("S1")
    cord = g.piece("grain_pouch_cord", "TORSO", (-.5, -.4, -.3), (1, 1, 1), pivot=pivot, motion="flap_front")
    solid(cord, "L", "plain", 51284, 1, edge=False)
    cord.front.set(0, 0, k("L", 3))
