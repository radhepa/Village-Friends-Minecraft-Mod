"""Mudlark's Ragged Shirt: an outgrown shirt torn at the shoulder and hem, one sleeve ripped short, mended with odd
patches, tied up with rope, and a lumpy sack of river finds hanging at the hip."""
from kit import body, sleeves
from kit_male import blk
from paint import grid, solid

META = {
    "name": "Mudlark's Ragged Shirt",
    "gender": "male",
    "description": "An outgrown shirt torn at the shoulder and hem, one sleeve ripped short, mended with odd patches, "
                   "tied up with a rope and a lumpy sack of river finds at the hip.",
    "tags": ["simple", "relaxed", "casual"],
    "covers_waist": True,
}

PATCH = ["aaa",
         "a.a",
         "aaa"]
SACK = (2.4, 9.8, -3.3)      # the sack's neck is tied to the rope here; sack and knot share the hinge


def build(g):
    b = body(g, "S", "tweed", 33480, base=2)
    f, bk = b.front, b.back
    for x in (3, 4):
        f.clear(x, 0)
    f.set(3, 1, "S1"), f.vline(4, 1, 3, "S0")                            # a ripped neck slit
    # Tears showing skin: a rent over the left breast, one on the back, and a ragged hem.
    for x, y in ((6, 4), (6, 5), (5, 5)):
        f.clear(x, y)
    f.set(5, 4, "S0"), f.set(6, 6, "S0"), f.set(4, 5, "S0")
    for x, y in ((1, 7), (2, 7), (2, 8)):
        bk.clear(x, y)
    bk.set(1, 8, "S0"), bk.set(3, 7, "S0")
    for face in b.sides:
        for x in range(face.w):
            if (x + face.x0) % 3 == 0:
                face.clear(x, 11)                                        # torn hem
            elif (x + face.x0) % 3 == 1:
                face.set(x, 11, "S0")
    # Patches of whatever cloth came to hand, stitched round with dark thread.
    f.rect(1, 6, 3, 3, "P2"), grid(f, 1, 6, PATCH, {"a": "P1"})
    f.set(2, 7, "P3")
    bk.rect(4, 2, 3, 3, "A2"), grid(bk, 4, 2, PATCH, {"a": "A1"})
    # The sleeves: the right ripped off above the elbow, the left long but frayed and holed.
    sleeves(g, "S", "tweed", 33481, rows=(0, 9))
    right = g.part("right_arm").strip
    for y in range(4, 10):
        right.hline(0, 15, y, None)
    for x in range(16):
        right.set(x, 4, "S0" if x % 2 else None)
    left = g.part("left_arm").strip
    for x in range(16):
        left.set(x, 9, "S0" if x % 3 == 0 else "S1" if x % 3 == 1 else None)
    left.clear(6, 5), left.set(5, 5, "S0"), left.set(7, 5, "S0")
    left.rect(10, 2, 3, 3, "L2"), grid(left, 10, 2, PATCH, {"a": "L1"})
    # A length of old rope for a belt, knotted at the front.
    rope = g.piece("rope_belt", "TORSO", (-4.55, 9.6, -2.55), (9, 1, 5), inflate=.05)
    for face in rope.faces:
        for y in range(face.h):
            for x in range(face.w):
                face.set(x, y, "L3" if (x + y) % 2 else "L1")
    knot = blk(g, "rope_knot", (-1.2, 10.2, -2.75), (1, 3, 1), "L", 2, "plain", 33482, motion="sway")
    knot.strip.hline(0, knot.strip.w - 1, 2, "L4")
    # The sack of river finds: lumpy sacking, a nail and a bottle neck poking out.
    sack = g.piece("finds_sack", "TORSO", (-1.5, 1.0, -1), (3, 4, 2), pivot=SACK, motion="flap_front")
    solid(sack, "S", "weave", 33483, 1)
    for face in sack.sides:
        face.set(0, 2, "S0"), face.set(2, 1, "S2"), face.set(1, 3, "S0")
    neck = g.piece("finds_sack_neck", "TORSO", (-.5, 0, -.5), (1, 1, 1), pivot=SACK, motion="flap_front")
    solid(neck, "L", "plain", 33484, 2, edge=False)
    bottle = g.piece("finds_bottle", "TORSO", (.4, .1, -.5), (1, 1, 1), pivot=SACK, motion="flap_front")
    solid(bottle, "A", "smooth", 33485, 1, edge=False)
    bottle.top.fill("A3")
