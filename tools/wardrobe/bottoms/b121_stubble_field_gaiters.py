"""Stubble-Field Gaiters: short linen braies over bare knees, stiff leather gaiters buckled from shin to instep and turnshoes."""
from kit import SIDES, footwear, leg_bone, legs, waistband
from kit_m01 import gathers, outer
from kit_male import blk, leg_blk
from paint import k, solid

META = {
    "name": "Stubble-Field Gaiters",
    "gender": "male",
    "description": "Short linen braies tied above bare knees, and stiff leather gaiters buckled from shin to instep against the cut stubble, over soft turnshoes.",
    "tags": ["work", "rugged", "sturdy"],
}


def build(g):
    for leg in legs(g, "S", "weave", 31011, base=3, rows=(0, 3), crease=False):
        for face in leg.sides:
            face.vline(1, 0, 2, "S2")
    waistband(g, "S", "weave", 31012, base=3)
    footwear(g, "turnshoe", top=10, base=2)
    for i, side in enumerate(SIDES):
        leg, pants = g.part(f"{side}_leg"), g.part(f"{side}_pants")
        gathers(pants.strip, "S", 3, range(1, 4))                        # braies puffing over the tie
        pants.strip.hline(0, pants.strip.w - 1, 0, "S3")
        leg.strip.hline(0, leg.strip.w - 1, 3, "S1")
        tie = blk(g, f"{side}_braies_tie", (-2.3 if side == "right" else 2.3, 3.2, -.4), (1, 2, 1), "S", 2,
                  "plain", 31013 + i, bone=leg_bone(side), motion="sway")
        tie.strip.hline(0, tie.strip.w - 1, 1, "S4")
        # Gaiters: stiff leather from mid-shin to the instep, buckled up the outside.
        for face in pants.sides:
            for y in range(6, 11):
                face.hline(0, face.w - 1, y, "L2")
            face.hline(0, face.w - 1, 6, "L3")
            face.hline(0, face.w - 1, 10, "L1")
        for y in range(6, 10):
            pants.front.set(1 if side == "right" else 2, y, "L1")           # stitched front seam
        out = outer(pants, side)
        for y in (7, 9):
            out.set(1, y, "M3"), out.set(2, y, "L0")
        for y in range(6, 10):
            leg.strip.hline(0, leg.strip.w - 1, y, "L1")
        cuff = leg_blk(g, f"{side}_gaiter_cuff", side, 5.6, (5, 1, 5), "L", 3, "leather", 31015 + i)
        for face in cuff.sides:
            face.hline(0, face.w - 1, 0, "L4")
            face.set(2, 0, "L2")
        spat = g.piece(f"{side}_gaiter_spat", leg_bone(side), (-1.5, 0, -1), (3, 2, 1), pivot=(0, 9.6, -2.3),
                       rotation=(18, 0, 0))
        solid(spat, "L", "leather", 31017 + i, 2, edge=False)
        spat.front.hline(0, 2, 0, "L3"), spat.front.hline(0, 2, 1, "L1")
        spat.front.set(1, 1, "M3")
    cord = g.piece("waist_cord", "TORSO", (-4.55, 9.6, -2.55), (9, 1, 5), inflate=.04)
    solid(cord, "L", "plain", 31019, 3, edge=False)
    for face in cord.sides:
        for x in range(0, face.w, 2):
            face.set(x, 0, "L2")
    for i, x in enumerate((-.6, .4)):
        end = blk(g, f"waist_cord_end_{i}", (x, 10.4, -2.8), (1, 2, 1), "L", 3, "plain", 31020 + i, motion="sway")
        end.strip.hline(0, end.strip.w - 1, 1, k("L", 1))
