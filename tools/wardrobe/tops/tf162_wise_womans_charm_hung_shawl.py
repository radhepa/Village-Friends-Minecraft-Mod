"""Wise Woman's Charm-Hung Shawl: a big triangular knitted shawl over a laced dark bodice. Its ends cross
the breast and knot under the throat, its point hangs down the back, and its fringe is strung with
charms: a bone, a holed stone, a herb bundle and a little bell."""
from kit_female import bodice, chemise, lacing, mantle, trim
from paint import fabric, k, solid

META = {
    "name": "Wise Woman's Charm-Hung Shawl",
    "gender": "female",
    "description": "A great triangular knitted shawl knotted at the breast, point down the back, its fringe strung with bones, a holed stone and herbs.",
    "tags": ["whimsical", "knit", "casual"],
}

KNOT = (0.0, 4.6, -3.0)      # the shawl's knot on the breast; the front ends hang from it


def charm(box, kind):
    """Paint one small charm."""
    if kind == "bone":
        solid(box, "S", "plain", 55048, 4, edge=False)
        for f in box.sides:
            f.set(0, 1, "S2")
            f.set(0, box.h - 1, "S3")
    elif kind == "stone":
        solid(box, "K", "smooth", 55052, 3, edge=False)
        for f in (box.front, box.back):
            f.set(1, 0, "K0"), f.set(0, 1, "K4")                       # the hole worn through it
    elif kind == "herbs":
        solid(box, "A", "plain", 55050, 2, edge=False)
        for f in box.sides:
            f.set(0, 0, "A3"), f.set(0, 1, "L2")                       # flower heads over the binding
    else:
        solid(box, "M", "smooth", 55049, 3, edge=False)
        for f in box.sides:
            f.hline(0, f.w - 1, 1, "M1")
            f.set(0, 0, "M4")
        box.bottom.fill("K1")


def fringe(face, y, x0=0, x1=None):
    """Knotted fringe: tufts every other texel."""
    x1 = face.w - 1 if x1 is None else x1
    for x in range(x0, x1 + 1):
        face.set(x, y, "P3" if x % 2 == 0 else "P0")


def build(g):
    chemise(g, "S", 3, "weave", 55041, neckline="scoop", sleeve_rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, 15, 10, "S1"), arm.strip.hline(0, 15, 11, "S2")
    b = bodice(g, "L", "leather", 55042, base=1, rows=(3, 9), neckline="square", edge="L2")
    lacing(b.front, 3, 6, 9, "ladder", lace="S3", under="L0", eyelet=None)
    # The shawl round the shoulders: a knitted band with a zigzag edge.
    shawl = mantle(g, "shawl", "P", "knit", 55043, 2, height=2, width=17, depth=6, y=-.7)
    for face in shawl.sides:
        trim(face, face.h - 1, "zigzag", "P1", "P3")
    fabric(shawl.top, "P", "knit", 55043, 3)
    # Its two ends sweep across the breast to the knot (painted on the jacket over the bodice).
    j = g.part("jacket")
    for y in range(0, 5):
        for dx in range(3):
            xr, xl = y // 2 + dx, 7 - y // 2 - dx
            j.front.set(xr, y, "P3" if dx == 0 else "P2")
            j.front.set(xl, y, "P1" if dx == 0 else "P2")
    for x in range(2, 6):
        j.front.set(x, 4, "P1")
    knot = g.piece("shawl_knot", "TORSO", (-1.5, -1, 0), (3, 2, 1), pivot=KNOT)
    solid(knot, "P", "knit", 55053, 2, edge=False)
    knot.front.set(1, 0, "P3"), knot.front.set(0, 1, "P1"), knot.front.set(2, 1, "P1")
    # Two short knitted tails hang from the knot, each ending in fringe and a charm.
    for side, x, kind, size in (("right", -1.0, "herbs", (1, 2, 1)), ("left", 1.0, "bell", (2, 2, 1))):
        tail = g.piece(f"shawl_tail_{side}", "TORSO", (x - 1, 1, 0), (2, 3, 1), pivot=KNOT, motion="flap_front")
        solid(tail, "P", "knit", 55054 + (side == "left"), 2, edge=False)
        fringe(tail.front, 2), fringe(tail.back, 2)
        c = g.piece(f"charm_{kind}", "TORSO", (x - size[0] / 2, 4, -.05), size, pivot=KNOT, motion="flap_front")
        charm(c, kind)
    # The point stepping down the back, fringed along its edges.
    # The upper steps lie still on the back; the point below the waist rides the trailing leg.
    steps = [(10, 3, 1.1, None), (8, 3, 4.0, None), (6, 2, 6.9, None), (4, 2, .8, "flap_back")]
    for i, (w, h, y, mot) in enumerate(steps):
        if mot:
            p = g.piece(f"shawl_point_{i}", "TORSO", (-w / 2, y, 0), (w, h, 1), pivot=(0, 9.0, 2.45), motion=mot)
        else:
            p = g.piece(f"shawl_point_{i}", "TORSO", (-w / 2, 0, 0), (w, h, 1), pivot=(0, y, 2.35), rotation=(4, 0, 0))
        solid(p, "P", "knit", 55044 + i, 2)
        p.back.hline(0, w - 1, 0, k("P", 2))
        for yy in range(h):
            p.back.set(0, yy, "P3" if yy % 2 == 0 else "P0")
            p.back.set(w - 1, yy, "P3" if yy % 2 == 0 else "P0")
    tip = g.piece("shawl_point_tip", "TORSO", (-1, 2.8, 0), (2, 2, 1), pivot=(0, 9.0, 2.45), motion="flap_back")
    solid(tip, "P", "knit", 55047, 1, edge=False)
    fringe(tip.back, 1)
    # Charms on the back: a knucklebone at a step corner and the holed stone at the very point.
    bone = g.piece("charm_knucklebone", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(3.4, 7.1, 3.0), motion="sway")
    charm(bone, "bone")
    stone = g.piece("charm_stone", "TORSO", (-1, 4.8, .1), (2, 2, 1), pivot=(0, 9.0, 2.45), motion="flap_back")
    charm(stone, "stone")
