"""Laced Kirtle Bodice: a fitted kirtle bodice laced up the front over a full linen chemise."""
from kit_female import bodice, chemise, lacing

META = {
    "name": "Laced Kirtle Bodice",
    "gender": "female",
    "description": "The everyday village bodice: criss-cross lacing over a cream chemise with full gathered sleeves.",
    "tags": ["casual", "simple"],
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 10101, neckline="scoop", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 9, "S2")                    # gathered wrist band
        arm.strip.hline(0, 15, 10, "S4")
        for x in range(0, 16, 2):
            arm.strip.set(x, 11, "S2")                     # a little frill at the wrist
        arm.front.vline(1, 2, 8, "S2")                     # a soft fold down the sleeve
    b = bodice(g, "P", "weave", 10102, rows=(2, 9), neckline="square", point=True, edge="P3")
    lacing(b.front, 3, 3, 8, "x", lace="S4", under="P0", eyelet="M3")
    for face in (b.right, b.left):
        face.vline(0, 2, 9, "P1")
    b.back.vline(3, 2, 9, "P1"), b.back.vline(4, 2, 9, "P3")
