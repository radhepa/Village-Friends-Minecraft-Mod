"""Barefoot Canvas Slops: wide knee-length sailor's slops with a tarred hem, a rope belt and bare feet."""
from kit import SIDES, legs, waistband
from kit_male import blk, leg_blk

META = {
    "name": "Barefoot Canvas Slops",
    "gender": "male",
    "description": "Wide knee-length canvas slops with a tarred hem, held up with a knotted rope, worn barefoot on deck or shore.",
    "tags": ["sea", "relaxed", "simple"],
    "rejects": ["armor"],
}


def build(g):
    legs(g, "S", "twill", 3311, base=2, rows=(0, 6), crease=False)
    waistband(g, "S", "twill", 3312)
    for i, side in enumerate(SIDES):
        g.part(f"{side}_leg").strip.hline(0, 15, 6, "K3")
        # Wide slop legs: slightly different inflation keeps the two tubes from z-fighting at the crotch.
        tube = leg_blk(g, f"{side}_slop", side, 0.0, (5, 6, 5), "S", 2, "twill", 3313 + i,
                       dx=-.3 if side == "right" else .3, inflate=.14 + .04 * i)
        for face in tube.sides:
            face.vline(1, 1, 4, "S1"), face.vline(3, 2, 4, "S3")
            face.hline(0, face.w - 1, 5, "K3")
            face.set(2, 5, "K2")
        tube.bottom.fill("S0")
    rope = g.piece("waist_rope", "TORSO", (-4.55, 9.7, -2.55), (9, 1, 5), inflate=.05)
    for face in rope.faces:
        for x in range(face.w):
            for y in range(face.h):
                face.set(x, y, "L3" if (x + y) % 2 else "L1")
    knot = blk(g, "waist_rope_knot", (1.2, 10.4, -2.75), (1, 3, 1), "L", 2, "plain", 3316, motion="sway")
    knot.strip.hline(0, knot.strip.w - 1, 2, "L4")
