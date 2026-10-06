"""Guard's Quilted Gambeson: a channel-quilted gambeson with a standing collar, laced front, town badge and baldric."""
from kit import sleeves
from kit_female import girdle, motif, over_flaps, quilt_lines
from paint import fabric, line, solid, strip_fabric

META = {
    "name": "Guard's Quilted Gambeson",
    "gender": "female",
    "description": "A channel-quilted gambeson with a standing collar, tie-laced front, the town's badge and a sword baldric.",
    "tags": ["martial", "sturdy"],
    "covers_waist": True,
}


def build(g):
    b = g.part("body")
    strip_fabric(b, "P", "plain", 12101, 2)
    for face in b.sides:
        quilt_lines(face, "P", 2, 2)
    fabric(b.top, "P", "plain", 12101, 3), fabric(b.bottom, "P", "plain", 12101, 1)
    b.front.vline(3, 0, 11, "P0"), b.front.vline(4, 0, 11, "P3")
    for y in (2, 5, 8):
        b.front.set(3, y, "L3"), b.front.set(4, y, "L2")              # tie laces
    sleeves(g, "P", "plain", 12102, rows=(0, 11))
    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        for x in range(0, 16, 2):
            arm.strip.vline(x, 0, 11, "P1")
        arm.strip.hline(0, 15, 11, "P0")
        arm.strip.hline(0, 15, 1, "L2")                              # arming points at the shoulder
    j = g.part("jacket")
    line(j.front, 0, 0, 7, 9, "L2"), line(j.back, 7, 0, 0, 9, "L2")
    j.top.vline(1, 0, 3, "L2")
    collar = g.piece("standing_collar", "TORSO", (-4.5, -1.6, -2.6), (9, 2, 5), inflate=.08)
    solid(collar, "P", "plain", 12103, 2)
    for face in collar.sides:
        for x in range(0, face.w, 2):
            face.vline(x, 0, 1, "P1")
    badge = g.piece("badge", "TORSO", (-1, -1, -.5), (3, 3, 1), pivot=(2.2, 3.4, -2.55))
    solid(badge, "A", "plain", 12104, 2, edge=False)
    motif(badge.front, 0, 0, "diamond", a="M3", b="M4")
    girdle(g, "belt", 8.0, role="L", height=1)
    f, bk = over_flaps(g, "gambeson_skirt", 4, "P", "plain", 12105, width=10, top=9.0)
    for face in (f, bk):
        quilt_lines(face, "P", 2, 2, y0=1)
        face.hline(0, face.w - 1, 3, "P0")
