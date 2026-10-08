"""Eel Marsh Mud Wraps: breeches rolled above bare shins caked grey-brown with marsh mud, cross-bound with cord, and
broad wooden mud pattens strapped under the feet for walking the soft fen."""
from kit import SIDES, legs, waistband
from kit_male import leg_blk
from paint import k

META = {
    "name": "Eel Marsh Mud Wraps",
    "gender": "male",
    "description": "Breeches rolled above shins caked grey-brown with marsh mud and cross-bound with cord, over broad "
                   "wooden mud pattens strapped under the feet for the soft fen.",
    "tags": ["rugged", "relaxed", "sea"],
    "rejects": ["armor"],
}

# The mud's upper edge, per strip column: higher at the back where it splashes up.
MUD = [6, 6, 6, 7, 7, 6, 6, 7, 6, 6, 5, 5, 5, 5, 5, 6]


def build(g):
    legs(g, "P", "weave", 33460, rows=(0, 4), crease=False)
    waistband(g, "P", "weave", 33461)
    for i, side in enumerate(SIDES):
        leg = g.part(f"{side}_leg").strip
        leg.hline(0, 15, 4, "P1")
        for x, top in enumerate(MUD):
            for y in range(top, 12):
                deep = y - top
                leg.set(x, y, k("L", 1) if deep >= 3 else "K3" if deep == 0 else "L2" if (x + y) % 3 else "K3")
            if (x + i) % 4 == 0:
                leg.set(x, top - 1, "K3")                                 # a fleck flung above the cake
        # Cord binding crossing the mud, one turn below the knee and one at the ankle.
        for y, ph in ((7, 0), (9, 2)):
            for x in range(16):
                if (x + ph) % 4 == 0:
                    leg.set(x, y, "S3")
        g.part(f"{side}_leg").bottom.fill("L1")
    # Rolled breech legs above the knee.
    for i, side in enumerate(SIDES):
        roll = leg_blk(g, f"{side}_breech_roll", side, 4.0, (5, 2, 5), "P", 2, "weave", 33462 + i, inflate=.12)
        for face in roll.sides:
            face.hline(0, face.w - 1, 0, "P3"), face.hline(0, face.w - 1, 1, "P1")
        # The patten: a broad wooden board under the foot, a leather strap over the instep.
        board = leg_blk(g, f"{side}_mud_patten", side, 11.0, (5, 1, 8), "L", 3, "plain", 33464 + i, dz=-.8,
                        dx=-.6 if side == "right" else .6)
        for face in board.sides:
            for x in range(face.w):
                face.set(x, 0, "L3" if x % 3 else "L2")
        board.top.fill("L3")
        for y in range(8):
            board.top.set(0, y, "L2"), board.top.set(4, y, "L2")
        board.bottom.fill("L1")
        strap = leg_blk(g, f"{side}_patten_strap", side, 9.8, (5, 1, 4), "L", 1, "leather", 33466 + i, dz=-.4,
                        inflate=.1)
        strap.front.hline(0, 4, 0, "L2")
