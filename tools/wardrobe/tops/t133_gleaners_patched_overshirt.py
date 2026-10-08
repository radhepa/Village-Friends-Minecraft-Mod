"""Gleaner's Patched Overshirt: a much-mended overshirt in patches of every cloth, its front hem gathered up into a lap-pouch bristling with gleaned wheat ears."""
from kit import body, sleeves
from kit_m01 import patch
from kit_male import blk
from paint import k, solid

META = {
    "name": "Gleaner's Patched Overshirt",
    "gender": "male",
    "description": "A much-mended overshirt pieced with patches of every cloth, its front hem gathered up and knotted into a lap-pouch bristling with gleaned wheat ears.",
    "tags": ["casual", "simple", "relaxed"],
    "covers_waist": True,
}


def build(g):
    b = body(g, "P", "weave", 31675)
    f = b.front
    f.clear(3, 0), f.clear(4, 0)
    f.set(2, 0, "P1"), f.set(5, 0, "P1"), f.vline(4, 1, 2, "P1")
    patch(f, 0, 2, 3, 3, "S", 3, stitch="L2")                              # patches in every cloth
    patch(f, 5, 5, 3, 4, "L", 3)
    patch(b.back, 1, 1, 4, 3, "A", 2, stitch="S3")
    patch(b.back, 4, 6, 3, 3, "S", 2)
    patch(b.right, 0, 4, 3, 3, "A", 2)
    patch(b.left, 1, 7, 3, 3, "S", 3, stitch="L2")
    sleeves(g, "P", "weave", 31676, rows=(0, 10), cuff="P1")
    for i, side in enumerate(("right", "left")):
        arm = g.part(f"{side}_arm")
        patch(arm.front if i == 0 else arm.back, 0, 3, 4, 3, "S" if i == 0 else "L", 3)
        arm.strip.hline(0, arm.strip.w - 1, 10, "P0")
        for x in range(0, arm.strip.w, 3):
            arm.strip.set(x, 10, "P3")                                    # frayed cuff
    cord = g.piece("rope_girdle", "TORSO", (-4.55, 8.6, -2.55), (9, 1, 5), inflate=.05)
    solid(cord, "S", "plain", 31677, 2, edge=False)
    for face in cord.sides:
        for x in range(0, face.w, 2):
            face.set(x, 0, "S1")
    # The back hem hangs loose; the front hem is gathered up into the lap-pouch.
    back = g.piece("shirt_hem_back", "TORSO", (-4.5, 0, 0), (9, 3, 1), pivot=(0, 10.8, 1.85), motion="flap_back")
    solid(back, "P", "weave", 31678, 2, edge=False)
    back.back.hline(0, 8, 2, "P1")
    patch(back.back, 5, 0, 3, 3, "L", 3)
    pouch = g.piece("lap_pouch", "TORSO", (-3.5, 0, -2), (7, 3, 2), pivot=(0, 9.4, -2.4), inflate=.05)
    solid(pouch, "P", "weave", 31679, 2)
    for face in pouch.sides:
        for x in range(0, face.w, 2):
            face.set(x, 0, "P3"), face.set(x, 1, "P1")                    # gathered folds
    pouch.top.fill("S2")
    patch(pouch.front, 0, 0, 3, 3, "S", 3)
    knot = blk(g, "lap_knot", (2.9, 9.0, -4.6), (1, 1, 1), "P", 1, "weave", 31680, edge=False)
    knot.front.set(0, 0, "P3")
    # Wheat ears bristling from the pouch: pale straws with long heavy heads.
    for i, (x, h, rz) in enumerate(((-2.4, 3, 18), (-1.4, 4, 6), (-.3, 3, -8), (.9, 4, -18), (2.0, 3, -26))):
        straw = g.piece(f"wheat_straw_{i}", "TORSO", (-.5, -h, -.5), (1, h, 1), pivot=(x, 9.6, -3.6 + (i % 2) * .5),
                        rotation=(-8, 0, rz))
        solid(straw, "S", "plain", 31681 + i, 3, edge=False)
        straw.strip.hline(0, straw.strip.w - 1, 0, k("S", 4))
        straw.strip.hline(0, straw.strip.w - 1, 1, k("L", 3))             # the ripe ear
        straw.top.fill("S4")
