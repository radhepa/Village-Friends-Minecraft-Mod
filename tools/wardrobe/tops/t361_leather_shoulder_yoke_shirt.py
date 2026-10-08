"""Leather Shoulder-Yoke Shirt: a tucked linen work shirt with a pointed yoke of stitched suede across both shoulders and leather-faced cuffs."""
from kit import SIDES, body, sleeves
from kit_male import blk
from paint import dark_seams

META = {
    "name": "Leather Shoulder-Yoke Shirt",
    "gender": "male",
    "description": "A tucked linen work shirt with a yoke of stitched suede sewn across both shoulders and dipping to a point front and back, a leather collar band and leather-faced cuffs.",
    "tags": ["casual", "work", "rugged"],
    "tucked": True,
}

# Depth of the yoke at each column (rows 0..n-1 are leather): pointed at the centre.
DEPTH = [3, 3, 3, 4, 4, 3, 3, 3]
DEPTH_FRONT = [2, 2, 3, 4, 4, 3, 2, 2]


def build(g):
    shirt = body(g, "S", "weave", 40700, base=3)
    shirt.front.clear(3, 0), shirt.front.clear(4, 0)
    shirt.front.vline(4, 1, 5, "S2"), shirt.front.set(3, 3, "L3"), shirt.front.set(3, 5, "L3")
    for x in (1, 6):
        shirt.front.vline(x, 6, 11, "S2")
    dark_seams(shirt, faces=("right", "left"))
    yoke = g.part("jacket")
    for face, depth in ((yoke.front, DEPTH_FRONT), (yoke.back, DEPTH)):
        for x, d in enumerate(depth):
            for y in range(d):
                if face is yoke.front and x in (3, 4) and y < 2:
                    continue                                              # the neck opening
                face.set(x, y, "L2" if (x + y) % 4 else "L3")
            face.set(x, d - 1, "L1")
            if d < 12:
                face.set(x, d, "L3" if x % 2 else "S2")                   # top-stitching along the edge
    for face in (yoke.right, yoke.left):
        for x in range(face.w):
            face.set(x, 0, "L2"), face.set(x, 1, "L1")
    yoke.top.fill("L3")
    blk(g, "yoke_collar", (0, -.6, 0), (9, 1, 5), "L", 2, "leather", 40701, inflate=.05, edge=False)
    sleeves(g, "S", "weave", 40702, base=3, rows=(0, 10))
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        arm.strip.hline(0, arm.strip.w - 1, 0, "L2")                      # the yoke running over the sleeve head
        arm.top.fill("L3")
        for y in (8, 9, 10):
            arm.strip.hline(0, arm.strip.w - 1, y, "L2" if y != 8 else "L3")
        (arm.right if side == "right" else arm.left).set(2, 9, "M3")
