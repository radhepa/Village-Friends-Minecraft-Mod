"""Beguine's Plain Kirtle and Mantle: a plain kirtle under a long dark mantle tied across the breast
between two pewter clasps, a white linen huik falling over the shoulders and down the back, and a
spindle wound with wool tucked into the girdle."""
from kit import body, sleeves
from kit_female import cloak, collar_flat, girdle, mantle, neck
from kit_f05 import fixed
from paint import fabric, solid

META = {
    "name": "Beguine's Plain Kirtle and Mantle",
    "gender": "female",
    "description": "A plain kirtle under a long dark mantle tied between pewter clasps, a white huik down the back and a spindle.",
    "tags": ["holy", "simple", "robe"],
}


def build(g):
    b = body(g, "P", "weave", 55121, base=2)
    neck(b.front, "round", "P", 2)
    for arm in sleeves(g, "P", "weave", 55122, base=2, rows=(0, 11)):
        arm.strip.hline(0, 15, 11, "S4")
        arm.strip.hline(0, 15, 10, "P1")
    # The mantle's front edges frame the kirtle; a cord ties across between two clasps.
    j = g.part("jacket")
    for x0 in (0, 6):
        fabric(j.front, "K", "weave", 55123, 2, x0, 1, 2, 11)
    j.front.vline(1, 1, 11, "K3"), j.front.vline(6, 1, 11, "K3")
    for face in (j.right, j.left, j.back):
        fabric(face, "K", "weave", 55124, 2, 0, 1, face.w, 11)
    j.front.hline(2, 5, 3, "M2")
    for x in (-2.6, 2.6):
        clasp = fixed(g, f"clasp_{'right' if x < 0 else 'left'}", (x, 3.5, -2.55), (1, 1, 1), "M", 3, edge=False)
        clasp.front.fill("M4")
    shoulders = mantle(g, "mantle_shoulders", "K", "weave", 55125, 2, height=3, width=17, depth=6, y=-.6)
    for face in shoulders.sides:
        face.hline(0, face.w - 1, 2, "K1")
    shoulders.front.vline(8, 0, 2, "K1")
    upper, tail = cloak(g, "mantle", "K", "weave", 55126, base=2, width=10, length=11, tail=9, z=2.6)
    for face in (upper, tail):
        face.vline(1, 0, face.h - 1, "K1"), face.vline(8, 0, face.h - 1, "K1")
    tail.hline(0, 9, 8, "K1")
    # The white huik: a collar of linen round the neck and its fall down the back.
    collar_flat(g, "huik_collar", "S", 4, edge="S3")
    fall = g.piece("huik_fall", "TORSO", (-3.5, 0, 0), (7, 8, 1), pivot=(0, -.4, 3.75), rotation=(4, 0, 0))
    solid(fall, "S", "plain", 55127, 4)
    fall.back.vline(2, 1, 7, "S3"), fall.back.vline(5, 1, 7, "S3"), fall.back.hline(0, 6, 7, "S3")
    girdle(g, "girdle", 8.0, role="L", base=1, height=1, buckle=None)
    # A spindle with its cop of spun wool, tucked through the girdle at the left hip.
    stick = fixed(g, "spindle", (2.6, 7.0, -2.95), (1, 5, 1), "L", 3, "plain", 55128, rotation=(0, 0, -12))
    stick.front.set(0, 0, "L2")
    whorl = fixed(g, "spindle_whorl", (3.1, 9.0, -2.95), (2, 1, 2), "L", 1, "plain", 55129, rotation=(0, 0, -12), edge=False)
    whorl.top.fill("L2")
    cop = fixed(g, "spindle_cop", (2.45, 5.9, -2.95), (2, 3, 2), "S", 3, "knit", 55130, rotation=(0, 0, -12))
    for face in cop.sides:
        face.hline(0, face.w - 1, 0, "S2")
