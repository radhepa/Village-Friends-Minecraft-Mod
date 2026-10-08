"""Patched-Elbow Kirtle: a long-sleeved twill work kirtle with stitched leather pads on the elbows and leather-bound cuffs."""
from kit import SIDES, body
from kit_female import neck
from paint import fabric, solid, strip_fabric

META = {
    "name": "Patched-Elbow Kirtle",
    "gender": "female",
    "description": "A long-sleeved twill work kirtle with stitched leather pads over the elbows, leather-bound cuffs, and a thong-tied slit neck.",
    "tags": ["work", "sturdy"],
}


def build(g):
    b = body(g, "P", "twill", 60240)
    neck(b.front, "slit", "P", 2, edge="P1")
    b.front.set(3, 1, "L3"), b.front.set(5, 1, "L3")                 # the thong lacing the slit shut
    b.front.set(4, 3, "L3"), b.front.set(4, 4, "L2")                  # its tied end
    for face in (b.front, b.back):
        face.vline(2, 4, 11, "P1"), face.vline(5, 4, 11, "P1")
    b.back.vline(3, 1, 11, "P3")
    for face in (b.right, b.left):
        face.vline(2, 1, 11, "P1")
    for side in SIDES:
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "P", "twill", 60242 + (side == "left"), 2, 0, 11)
        fabric(arm.top, "P", "twill", 60244, 3)
        arm.strip.hline(0, 15, 9, "L3")
        arm.strip.hline(0, 15, 10, "L2"), arm.strip.hline(0, 15, 11, "L1")
        arm.front.vline(1, 1, 8, "P1")
        # The elbow pad: a stitched leather oval on the outside of each elbow.
        x = -3.4 if side == "right" else 2.4
        pad = g.piece(f"{side}_elbow_pad", "RIGHT_ARM" if side == "right" else "LEFT_ARM", (x, 2.6, -1.2), (1, 3, 3))
        solid(pad, "L", "leather", 60245, 2, edge=False)
        outer = pad.right if side == "right" else pad.left
        outer.fill("L2")
        outer.hline(0, 2, 0, "L3"), outer.set(0, 1, "L3")             # the worn, lit upper rim
        outer.set(2, 2, "L1")
