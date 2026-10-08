"""Novice's Undyed Tunic and Cord: a plain undyed wool tunic with its hand-sewn seams showing, girt with a twisted rope cord, a little wooden tau cross on a thong."""
from kit import body, flaps, sleeves
from kit_male import blk
from kit_m05 import cord_end
from paint import solid

META = {
    "name": "Novice's Undyed Tunic and Cord",
    "gender": "male",
    "description": "A novice's plain tunic of undyed wool with every hand-sewn seam showing, girt with a twisted rope cord knotted at the hip, and a small wooden tau cross on a leather thong.",
    "tags": ["holy", "simple"],
    "covers_waist": True,
}


def seam(face, x, y0, y1, key="S1"):
    """Running stitch: a dashed seam line."""
    for y in range(y0, y1 + 1):
        face.set(x, y, key if y % 2 == 0 else "S2")


def build(g):
    b = body(g, "S", "weave", 35320, base=3)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    f.set(2, 0, "S2"), f.set(5, 0, "S2"), f.set(3, 1, "S2"), f.set(4, 1, "S2")
    seam(f, 0, 1, 11), seam(f, 7, 1, 11)                               # side seams
    for face in (b.right, b.left):
        seam(face, 0 if face is b.right else 3, 0, 11)
    b.back.hline(0, 7, 1, "S2")                                          # yoke seam across the shoulders
    for x in range(0, 8, 2):
        b.back.set(x, 1, "S1")
    sleeves(g, "S", "weave", 35321, base=3, rows=(0, 10))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 10, "S2")
        seam(arm.back, 1, 0, 10)
    # The rope cord: twisted strands round the waist, knotted at the left hip with a long end.
    cord = g.piece("rope_cord", "TORSO", (-4.6, 9.6, -2.6), (9, 1, 5), inflate=.05)
    for face in cord.sides:
        for x in range(face.w):
            face.set(x, 0, "L3" if (x + face.x0) % 2 == 0 else "L1")
    cord.top.fill("L2"), cord.bottom.fill("L1")
    knot = blk(g, "cord_knot", (2.6, 9.4, -2.85), (2, 2, 1), "L", 2, "plain", 35322, edge=False)
    knot.front.set(0, 0, "L3"), knot.front.set(1, 1, "L3"), knot.front.set(1, 0, "L1"), knot.front.set(0, 1, "L1")
    cord_end(g, "cord_end_long", (2.9, 11.0, -2.95), 7, "L", 2, 35323, knots=(3, 6))
    cord_end(g, "cord_end_short", (2.0, 11.0, -2.95), 3, "L", 2, 35324, knots=(2,))
    # A tau cross of plain wood on a thong round the neck.
    tau_bar = g.piece("tau_bar", "TORSO", (-1, 0, -.5), (2, 1, 1), pivot=(-.5, 3.4, -2.6))
    solid(tau_bar, "L", "plain", 35325, 3, edge=False)
    tau_stem = g.piece("tau_stem", "TORSO", (-.5, 1, -.5), (1, 2, 1), pivot=(-.5, 3.4, -2.6))
    solid(tau_stem, "L", "plain", 35326, 3, edge=False)
    jacket = g.part("jacket")
    for (x, y) in ((2, 0), (2, 1), (3, 2), (5, 0), (5, 1), (4, 2)):
        jacket.front.set(x, y, "L1")                                     # the thong
    jacket.back.hline(2, 5, 0, "L1")
    front, back = flaps(g, "tunic_hem", 5, "S", "weave", 35327, base=3, top=10.8)
    for face in (front, back):
        seam(face, 4, 1, 4)
        face.hline(0, 8, 4, "S2")
