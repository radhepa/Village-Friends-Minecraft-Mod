"""Sheaf Binder's Arm-Guarded Blouse: a full linen blouse under a laced waist-cincher, long leather arm
guards laced against the stubble, and a hank of twisted straw bands for tying sheaves."""
from kit_female import arm_rings, bodice, chemise, lacing
from paint import k, solid

META = {
    "name": "Sheaf Binder's Arm-Guarded Blouse",
    "gender": "female",
    "description": "A full linen blouse under a laced waist-cincher, long laced leather arm guards against the stubble and a hank of twisted straw bands at the hip.",
    "tags": ["work", "rugged"],
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 51120, neckline="keyhole", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 2, "S2")                               # a gathered seam at the shoulder
    body.front.set(4, 3, "S1")
    b = bodice(g, "P", "weave", 51121, rows=(5, 9), straps=False, seams=False)
    lacing(b.front, 3, 5, 9, "ladder", lace="S4", under="P0", eyelet=None, edge="P1")
    for face in b.sides:
        face.hline(0, face.w - 1, 5, "P3")
    b.back.vline(2, 5, 9, "P1"), b.back.vline(5, 5, 9, "P1")
    # Long leather arm guards from elbow to wrist, laced up the outside and strapped at both ends.
    for side, box in zip(("right", "left"), arm_rings(g, "arm_guard", 3.6, 6, 5, inflate=.06)):
        solid(box, "L", "leather", 51122, 2, edge=False)
        for face in box.sides:
            face.hline(0, face.w - 1, 0, "L3"), face.hline(0, face.w - 1, 5, "L1")
        outer = box.right if side == "right" else box.left
        for y in range(1, 5):
            outer.set(1, y, "S4" if y % 2 else "L0")
            outer.set(3, y, "L0" if y % 2 else "S4")
            outer.set(2, y, "S3")
        box.front.set(2, 0, "M3"), box.front.set(2, 5, "M3")
        box.bottom.fill("L1")
    # A hank of twisted straw bands hung from the cincher at her left hip.
    hank = g.piece("straw_bands", "TORSO", (-1.5, 0, 0), (3, 6, 1), pivot=(2.3, 8.4, -3.3), motion="flap_front")
    for f in hank.faces:
        for y in range(f.h):
            for x in range(f.w):
                f.set(x, y, "M1" if (x + y + f.x0) % 3 == 0 else "M3" if x % 2 == 0 else "M2")   # twisted strands
    for f in hank.sides:
        f.hline(0, f.w - 1, 0, "L2")                                  # the tie round the hank
        f.hline(0, f.w - 1, f.h - 1, k("M", 2))
    loop = g.piece("straw_bands_loop", "TORSO", (-1, -1.6, 0), (2, 2, 1), pivot=(2.3, 8.4, -3.25), motion="flap_front")
    solid(loop, "M", "plain", 51123, 2, edge=False)
    loop.front.set(0, 0, "M3"), loop.front.set(1, 1, "M1")
