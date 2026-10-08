"""Egg Wife's Pocketed Skirt: an ankle-length market skirt with a row of three buttoned patch pockets across
the front, a fat coin purse at the hip and buckled shoes."""
from kit_female import shoes, skirt
from paint import solid

META = {
    "name": "Egg Wife's Pocketed Skirt",
    "gender": "female",
    "description": "An ankle-length market skirt with three buttoned patch pockets across the front, a fat coin purse at the hip and buckled shoes.",
    "tags": ["casual", "simple", "skirt", "long_skirt"],
}


def pocket(face, x, y):
    for yy in range(y, y + 4):
        for xx in range(x, x + 3):
            face.set(xx, yy, "P3" if yy == y else "P2")
    face.vline(x, y, y + 3, "P1"), face.hline(x, x + 2, y + 3, "P1")
    face.hline(x, x + 2, y + 1, "P1")                                  # the flap's edge
    face.set(x + 1, y + 1, "M3")                                      # its button


def build(g):
    s = skirt(g, "P", "weave", 51260, top=9.8, length=12, flare=5)
    front = s.front.front
    pocket(front, 0, 4), pocket(front, 3, 5), pocket(front, 7, 4)     # three pockets across the front
    for face in s.faces:
        face.hline(0, face.w - 1, face.h - 3, "A2")
        face.hline(0, face.w - 1, face.h - 1, "P1")
    # The coin purse on its drawstring, hung at the front of the left hip.
    purse = g.piece("waist_coin_purse", "TORSO", (2.2, .4, -1.05), (2, 3, 1), pivot=(0, 9.8, -2.95), inflate=.1,
                    motion="flap_front")
    solid(purse, "L", "leather", 51261, 2)
    purse.front.hline(0, 1, 0, "L4"), purse.front.set(0, 1, "L1"), purse.front.set(1, 2, "M3")
    shoes(g, "shoe", "K", 2, top=10)
    for side in ("right", "left"):
        g.part(f"{side}_pants").front.set(1, 10, "M3"), g.part(f"{side}_pants").front.set(2, 10, "M3")
