"""Bargeman's Tow-Rope Jerkin: a laced leather jerkin over a linen shirt, a thick tow rope looped over one shoulder
and across the chest, its spare length coiled at the hip."""
from kit import body, flaps, sleeves
from kit_m03 import coil, rope_box
from kit_male import blk, lacing

META = {
    "name": "Bargeman's Tow-Rope Jerkin",
    "gender": "male",
    "description": "A laced leather jerkin over a linen shirt, a thick tow rope looped over the shoulder and across chest "
                   "and back, its spare length coiled at the hip.",
    "tags": ["rugged", "work", "sea"],
}

ROPE_TILT = 27


def build(g):
    b = body(g, "L", "leather", 33040)
    f = b.front
    for x, y in ((2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (3, 2), (4, 2)):
        f.set(x, y, "S3")                                               # the shirt in the open neck
    f.set(2, 1, "L3"), f.set(5, 1, "L1")
    lacing(f, 3, 3, 8, "S4", "L0")
    for face in b.sides:
        face.hline(0, face.w - 1, 11, "L1")
    b.right.vline(3, 1, 10, "L1"), b.left.vline(0, 1, 10, "L1")       # side seams
    sleeves(g, "S", "weave", 33041, base=3, rows=(0, 10), cuff="S1")
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 0, "L2")                                 # the jerkin's shoulder seam
        arm.strip.hline(0, 15, 9, "S2")
    # Jerkin skirt tabs below the waist.
    for face in flaps(g, "jerkin_tabs", 2, "L", "leather", 33042, top=11.4):
        for x in (2, 6):
            face.vline(x, 0, 1, "L0")
    # The tow rope: over the left shoulder, then down across chest and back to the right hip.
    over = blk(g, "tow_rope_shoulder", (3.0, -.5, 0), (2, 1, 6), "S", 2, "plain", 33043)
    rope_box(over)
    for name, z in (("tow_rope_front", -2.6), ("tow_rope_back", 2.6)):
        strand = g.piece(name, "TORSO", (-1, 0, -.5), (2, 13, 1), pivot=(3.0, -.1, z), rotation=(0, 0, ROPE_TILT))
        rope_box(strand)
    hank = coil(g, "tow_rope_coil", (-2.2, 9.6, -3.1), (3, 4, 2), "S", 2, motion="flap_front")
    hank.front.set(1, 1, "L1")
    tail = g.piece("tow_rope_tail", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(-1.0, 11.6, -3.6), motion="sway")
    rope_box(tail)
    tail.front.set(0, 2, "S4")
