"""Cowherd's Horn-Cup Bodice: a laced bodice under a broad flat linen collar, a coiled tether rope worn across
the body and a horn drinking cup swinging on its cord at the girdle."""
from kit_female import OVER_FRONT, bodice, chemise, collar_flat, girdle, lacing
from paint import k, solid

META = {
    "name": "Cowherd's Horn-Cup Bodice",
    "gender": "female",
    "description": "A laced bodice under a broad flat linen collar, a tether rope coiled across the body and a horn drinking cup hung on a cord at the girdle.",
    "tags": ["work", "rugged"],
}


def rope(face, points, a="S2", b="S1"):
    """A twisted rope two texels wide following a list of (x, y) centre points."""
    for i, (x, y) in enumerate(points):
        face.set(x, y, a if i % 2 else b)
        face.set(x + 1, y, b if i % 2 else a)


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 51400, neckline="high", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 8, "P2"), arm.strip.hline(0, 15, 9, "P1")      # turned-up wool cuffs
        arm.strip.hline(0, 15, 10, "P3"), arm.strip.hline(0, 15, 11, "S2")
    b = bodice(g, "P", "twill", 51401, rows=(1, 9), neckline="round", seams=True)
    lacing(b.front, 3, 2, 8, "x", lace="L3", under="P0", eyelet="M2")
    collar_flat(g, "collar", "S", 4, edge="S2")
    # The tether rope, coiled and worn across the body from the left shoulder to the right hip.
    j = g.part("jacket")
    rope(j.front, [(6 - round(y * 0.62), y) for y in range(1, 11)])
    rope(j.back, [(round(y * 0.62), y) for y in range(1, 11)])
    j.top.set(6, 3, "S2"), j.top.set(7, 3, "S1"), j.top.set(6, 2, "S1"), j.top.set(7, 2, "S2")
    coil = g.piece("rope_coil", "TORSO", (-1.5, -.5, -.5), (3, 3, 1), pivot=(-2.6, 9.0, OVER_FRONT - .6), inflate=.15,
                   motion="flap_front")
    solid(coil, "S", "plain", 51402, 2, edge=False)
    for f in coil.faces:
        for y in range(f.h):
            for x in range(f.w):
                ring = max(abs(x - (f.w - 1) / 2), abs(y - (f.h - 1) / 2))
                f.set(x, y, k("S", 1 if ring < .6 else 3 if (x + y) % 2 else 2))
    girdle(g, "girdle", 7.8, role="L", height=1)
    # The horn cup on its cord: a curved cup of horn, pale at the rim, dark at the tip.
    pivot = (2.4, 8.4, OVER_FRONT - .1)
    cord = g.piece("horn_cup_cord", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=pivot, motion="flap_front")
    solid(cord, "L", "plain", 51403, 1, edge=False)
    cup = g.piece("horn_cup", "TORSO", (-1, 2, -1.2), (2, 3, 2), pivot=pivot, rotation=(0, 0, 8), motion="flap_front")
    solid(cup, "S", "smooth", 51404, 2, edge=False)
    for f in cup.sides:
        f.hline(0, f.w - 1, 0, "S4"), f.hline(0, f.w - 1, 1, "S3")
        f.hline(0, f.w - 1, 2, "L2")
        f.set(0, 1, "M3")                                             # a little metal band at the rim
    cup.top.fill("S1"), cup.bottom.fill("L1")
