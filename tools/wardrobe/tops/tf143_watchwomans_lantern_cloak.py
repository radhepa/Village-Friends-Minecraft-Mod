"""Watchwoman's Lantern Cloak: a dark wool cloak with a deep shoulder cape clasped at the throat, over a buttoned
plain coat, a horn-paned lantern burning at her belt and a hand bell for calling the hours."""
from kit import sleeves
from kit_female import cloak, girdle, mantle
from kit_f04 import front_prop
from paint import fabric, k, solid, strip_fabric

META = {
    "name": "Watchwoman's Lantern Cloak",
    "gender": "female",
    "description": "A dark wool cloak with a deep shoulder cape clasped at the throat over a buttoned coat, a lit "
                   "horn-paned lantern at her belt and a hand bell for calling the hours.",
    "tags": ["rugged", "sturdy"],
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "weave", 54281, 1)
    fabric(b.top, "P", "weave", 54281, 2), fabric(b.bottom, "P", "weave", 54281, 0)
    b.front.vline(3, 0, 11, "P0"), b.front.vline(4, 0, 11, "P2")
    for y in (2, 4, 6, 10):
        b.front.set(4, y, "M3")                                      # buttons down the coat
    sleeves(g, "P", "weave", 54282, base=1, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 10, "S3"), arm.strip.hline(0, 15, 11, "S2")   # shirt cuffs
    cape = mantle(g, "cloak_cape", "P", "weave", 54283, 1, height=5, width=17, depth=6, y=-.9)
    for face in cape.sides:
        face.hline(0, face.w - 1, face.h - 1, "P0")
        for x in range(1, face.w, 4):
            face.vline(x, 1, face.h - 2, "P0")                       # heavy folds
    cape.front.vline(8, 0, 4, "P0")
    clasp = g.piece("cloak_clasp", "TORSO", (-1, 0, 0), (2, 1, 1), pivot=(0, .4, -3.85))
    solid(clasp, "M", "smooth", 54285, 3, edge=False)
    upper, tail = cloak(g, "cloak", "P", "weave", 54286, base=1, width=10, length=11, tail=8, z=3.15)
    for face in (upper, tail):
        for x in (1, 4, 7):
            face.vline(x, 0, face.h - 1, "P0")
            face.vline(x + 1, 0, face.h - 1, "P2")
    tail.hline(0, 9, 7, "P0")
    girdle(g, "belt", 8.4, role="L", height=1)
    # The lantern on a short chain at the left hip: iron frame, glowing horn panes, a pierced cap and a ring.
    chain = front_prop(g, "lantern_chain", 2.6, (1, 1, 1), drop=.2)
    solid(chain, "M", "smooth", 54287, 2, edge=False)
    lantern = front_prop(g, "lantern", 2.6, (3, 4, 3), drop=1.6)
    solid(lantern, "M", "smooth", 54288, 1, edge=False)
    for face in lantern.sides:
        face.hline(0, face.w - 1, 0, "M2"), face.hline(0, face.w - 1, 3, "M1")
        face.set(1, 1, "A4"), face.set(1, 2, "S4")                    # the flame behind a horn pane
        face.set(0, 1, "M2"), face.set(2, 1, "M2"), face.set(0, 2, "M1"), face.set(2, 2, "M1")
    lantern.bottom.fill("M0")
    cap = front_prop(g, "lantern_cap", 2.6, (2, 1, 2), drop=.6, z=-2.85)
    solid(cap, "M", "smooth", 54289, 2, edge=False)
    cap.top.fill("M3"), cap.front.set(0, 0, "K1")
    # A hand bell at the right hip.
    bell = front_prop(g, "hand_bell", -2.6, (2, 2, 2), drop=1.4)
    solid(bell, "M", "smooth", 54290, 3, edge=False)
    for face in bell.sides:
        face.hline(0, face.w - 1, 1, "M2")
    bell.bottom.fill(k("K", 1))
    handle = front_prop(g, "hand_bell_handle", -2.6, (1, 2, 1), drop=-.6, z=-2.85)
    solid(handle, "L", "smooth", 54291, 2, edge=False)
