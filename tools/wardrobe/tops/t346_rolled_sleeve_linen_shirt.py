"""Rolled-Sleeve Linen Shirt: a plain linen work shirt with a band collar and buttoned slit, sleeves rolled high."""
from kit import SIDES, arm_bone, arm_x, body
from paint import dark_seams, k, solid

META = {
    "name": "Rolled-Sleeve Linen Shirt",
    "gender": "male",
    "description": "A plain linen work shirt with a narrow band collar and a two-button slit, its sleeves rolled in thick folds above the elbow.",
    "tags": ["casual", "simple", "work"],
    "tucked": True,
}


def build(g):
    b = body(g, "S", "weave", 40000, base=3)
    f, bk = b.front, b.back
    # Buttoned slit under a band collar.
    f.clear(3, 0), f.clear(4, 0)
    f.vline(3, 1, 4, "S4"), f.vline(4, 1, 4, "S1")
    f.set(3, 1, "L2"), f.set(3, 3, "L2")
    f.set(4, 5, "S2")
    # Yoke seam across the shoulders, gathers below it on the back.
    f.hline(0, 2, 2, "S2"), f.hline(5, 7, 2, "S2")
    bk.hline(0, 7, 2, "S2")
    for x in (1, 3, 4, 6):
        bk.set(x, 3, "S2")
    # Shirt bloused over the waistband.
    for face in (f, bk):
        for x in range(face.w):
            face.set(x, 8, "S2" if x % 3 == 1 else "S4" if x % 3 == 0 else "S3")
    dark_seams(b, faces=("right", "left"))
    jacket = g.part("jacket")
    for x in (1, 2, 5, 6):
        jacket.front.set(x, 0, "S4")
    jacket.back.hline(1, 6, 0, "S4")
    # Upper sleeves, then the thick roll; forearms bare below it.
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        for y in range(0, 5):
            arm.strip.hline(0, arm.strip.w - 1, y, "S3")
        arm.top.fill("S4")
        arm.strip.hline(0, arm.strip.w - 1, 0, "S4")
        out = arm.right if side == "right" else arm.left
        out.vline(1, 1, 3, "S2")                                          # sleeve seam
        roll = g.piece(f"{side}_sleeve_roll", arm_bone(side), (arm_x(side) - .5, 1.3, -2.5), (5, 3, 5))
        solid(roll, "S", "weave", 40001 + (side == "left"), 3)
        for face in roll.sides:
            face.hline(0, face.w - 1, 0, "S4")
            for x in range(face.w):
                face.set(x, 1, "S2" if (x + (side == "left")) % 3 == 0 else "S3")
            face.hline(0, face.w - 1, 2, "S1")
        roll.top.fill("S4"), roll.bottom.fill("S1")
