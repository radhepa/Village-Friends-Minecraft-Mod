"""Forester's Horn and Hatchet Coat: a wrap-over woodland coat, an ox-horn on a baldric at the belly and a hatchet in the belt behind."""
from kit import belt, body, flaps, sleeves
from kit_male import blk
from kit_m07 import baldric
from paint import k

META = {
    "name": "Forester's Horn and Hatchet Coat",
    "gender": "male",
    "description": "A forester's wrap-over twill coat closed slantwise from shoulder to hip, a banded ox-horn riding the baldric across his belly and a hatchet thrust through the belt at his back.",
    "tags": ["rugged", "work", "casual"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "twill", 37120)
    f = b.front
    # The wrap-over front: the outer panel's edge runs from the right shoulder down to the left hip.
    for y in range(0, 12):
        x = 1 + (y * 5) // 11
        f.set(x, y, "P0")
        f.set(max(0, x - 1), y, "P3")                                    # the lit edge of the overlap
    for y in (3, 7):
        f.set(min(7, 2 + (y * 5) // 11), y, "L2")                        # tie points along the wrap
    f.set(2, 0, "P1"), f.set(3, 0, "S3"), f.set(4, 0, "S3"), f.set(5, 0, "P1")   # shirt at the throat
    sleeves(g, "P", "twill", 37121, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 9, "P3"), arm.strip.hline(0, arm.strip.w - 1, 10, "P1")
    jacket = g.part("jacket")
    baldric(jacket.front, jacket.back, from_left=True, key="L2", edge="L1", y1=8)
    belt(g, "belt", 9.4, height=1)

    # The horn: a cream ox-horn with brass bands, bell to the right hip, tip curling up.
    bell = blk(g, "horn_bell", (-2.6, 6.8, -3.2), (2, 2, 2), "S", 3, "smooth", 37122, edge=False)
    bell.right.fill("K1"), bell.right.set(0, 0, "S2")                   # the open mouth
    bell.front.vline(1, 0, 1, "M3")
    mid = blk(g, "horn_body", (-1.0, 7.3, -3.2), (2, 1, 1), "S", 3, "smooth", 37123, edge=False)
    mid.front.set(1, 0, "M2")
    tip = blk(g, "horn_tip", (.4, 6.3, -3.2), (1, 2, 1), "S", 2, "smooth", 37124, rotation=(0, 0, 28), edge=False)
    tip.front.set(0, 0, "K2")
    # The hatchet: haft through the belt at the back left, steel head above.
    haft = blk(g, "hatchet_haft", (2.0, 6.2, 2.85), (1, 7, 1), "L", 2, "plain", 37125, rotation=(0, 0, -16), edge=False)
    for face in haft.sides:
        face.set(0, 0, "L3"), face.set(0, 6, "L1")
    eye = blk(g, "hatchet_eye", (2.0, 6.2, 2.85), (2, 1, 1), "M", 1, "smooth", 37126, rotation=(0, 0, -16),
              origin=(-.5, .2, -.5), inflate=.05)
    bit = blk(g, "hatchet_bit", (2.0, 6.2, 2.85), (1, 4, 1), "M", 2, "smooth", 37127, rotation=(0, 0, -16),
              origin=(1.5, -.6, -.5))
    for face in bit.sides:
        face.set(0, 3, "M1")                                             # the bearded lower point
    bit.left.vline(0, 0, 3, "M4")                                        # the bright cutting edge
    bit.back.vline(0, 0, 2, "M3"), bit.front.vline(0, 0, 2, "M3")

    for face in flaps(g, "coat_skirt", 5, "P", "twill", 37128, top=10.6):
        face.hline(0, 8, 3, k("P", 1))
        face.hline(0, 8, 4, k("P", 3))
