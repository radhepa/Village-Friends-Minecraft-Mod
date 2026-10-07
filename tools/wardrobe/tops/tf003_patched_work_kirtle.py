"""Patched Work Kirtle: a sturdy hook-fronted kirtle with darned patches, sleeves rolled to the elbow and a neck kerchief."""
from kit import body, roll, sleeves
from kit_female import neck
from paint import grid, solid

META = {
    "name": "Patched Work Kirtle",
    "gender": "female",
    "description": "A hard-wearing twill kirtle closed with hooks, darned patches, rolled sleeves and a knotted kerchief.",
    "tags": ["work", "sturdy"],
}

PATCH = ["sss", "sSs", "sss"]


def build(g):
    b = body(g, "P", "twill", 10301)
    neck(b.front, "round", "P", 2, edge="P3")
    for y in range(1, 12):
        b.front.set(4, y, "P1")
        if y % 2:
            b.front.set(3, y, "M2")                        # hook-and-eye closure
    grid(b.front, 5, 7, PATCH, {"s": "S2", "S": "S2"})
    for x, y in [(5, 7), (7, 7), (6, 8), (5, 9), (7, 9)]:
        b.front.set(x, y, "P0")                            # coarse stitches holding the patch on
    grid(b.back, 1, 3, ["ssss", "ssss", "ssss"], {"s": "L2"})
    for x, y in [(1, 3), (3, 3), (2, 5), (4, 5), (4, 4)]:
        b.back.set(x, y, "L0")
    sleeves(g, "P", "twill", 10302, rows=(0, 6))
    roll(g, "P", 3.6, base=3)
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        outer = arm.right if side == "right" else arm.left
        grid(outer, 1, 2, ["ss", "ss"], {"s": "S2"})       # elbow patches
        outer.set(1, 2, "S3")
    band = g.piece("kerchief", "TORSO", (-4.5, -.6, -2.6), (9, 1, 5), inflate=.04)
    solid(band, "A", "plain", 10303, 2, edge=False)
    knot = g.piece("kerchief_knot", "TORSO", (-1, -.5, -.5), (2, 2, 1), pivot=(-2.2, .8, -2.75), rotation=(0, 0, 15))
    solid(knot, "A", "plain", 10304, 2)
    end = g.piece("kerchief_end", "TORSO", (-.5, 0, -.5), (1, 2, 1), pivot=(-2.6, 1.6, -2.7), rotation=(0, 0, 25))
    solid(end, "A", "plain", 10305, 3)
