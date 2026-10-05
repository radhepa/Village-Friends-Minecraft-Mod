"""Merchant's Waistcoat: double-breasted waistcoat, billowing shirt, cravat and a watch chain."""
from paint import cap, fabric, grid, k, solid, strip_fabric

META = {
    "name": "Merchant's Waistcoat",
    "description": "Double-breasted velvet waistcoat with a pocket-watch chain over a billowing shirt and cravat.",
    "tags": ["tailored", "fancy"],
}


def build(g):
    body, jacket = g.part("body"), g.part("jacket")
    strip_fabric(body, "S", "weave", 101, 3)
    cap(body, "S", texture="weave", seed=101, base=3)
    strip_fabric(jacket, "P", "velvet", 102, 2, 0, 10)
    fabric(jacket.top, "P", "velvet", 102, 3)
    f, b = jacket.front, jacket.back
    for x, y in [(2, 0), (3, 0), (4, 0), (5, 0), (3, 1), (4, 1), (3, 2), (4, 2)]:
        f.clear(x, y)
    for x, y in [(1, 0), (2, 1), (2, 2), (3, 3)]:
        f.set(x, y, "A2")
    for x, y in [(6, 0), (5, 1), (5, 2), (4, 3)]:
        f.set(x, y, "A1")
    # Pointed front hem below the waist.
    f.hline(0, 7, 10, "P1")
    f.hline(1, 2, 11, "P1"), f.hline(5, 6, 11, "P1")
    for y in (4, 6, 8):
        f.set(2, y, "M3"), f.set(5, y, "M3")
    # Pocket welts and a pocket-watch chain.
    f.hline(0, 1, 7, "P0"), f.hline(6, 7, 7, "P0")
    for x, y in [(3, 7), (4, 7), (5, 7)]:
        f.set(x, y, "M4" if x == 4 else "M2")
    # Satin back with a cinch strap.
    fabric(b, "A", "plain", 103, 1, 0, 1, 8, 9)
    b.hline(0, 7, 7, "L2"), b.set(3, 7, "M3"), b.vline(4, 1, 6, "A0")
    for face in (jacket.right, jacket.left):
        face.vline(0, 0, 9, "P1")

    for side in ("right", "left"):
        arm = g.part(f"{side}_arm")
        strip_fabric(arm, "S", "weave", 104, 3, 0, 10)
        fabric(arm.top, "S", "weave", 104, 4)
        arm.strip.hline(0, arm.strip.w - 1, 9, "S4")
        arm.strip.hline(0, arm.strip.w - 1, 10, "S2")
        (arm.right if side == "right" else arm.left).set(1, 9, "M3")
        bone = "RIGHT_ARM" if side == "right" else "LEFT_ARM"
        ox = -3.0 if side == "right" else -1.0
        puff = g.piece(f"{side}_sleeve_puff", bone, (ox - .55, -2.3, -2.55), (5, 4, 5))
        solid(puff, "S", "weave", 105, 3)
        for face in puff.sides:
            face.vline(1, 0, 3, "S2"), face.vline(3, 0, 3, "S2")
            face.hline(0, face.w - 1, 3, "S2")
        fabric(puff.top, "S", "weave", 105, 4)

    # Cravat: a knotted stock tucked into the waistcoat.
    knot = g.piece("cravat_knot", "TORSO", (-1.5, -.6, -2.75), (3, 2, 1))
    solid(knot, "A", "plain", 106, 2)
    knot.front.set(1, 0, "A3")
    fall = g.piece("cravat_fall", "TORSO", (-1, 1.3, -2.7), (2, 2, 1), rotation=(-8, 0, 0))
    solid(fall, "A", "plain", 107, 2)
    fall.front.set(0, 1, "A1")
    for name, x, rot in (("collar_right", -3.2, 20), ("collar_left", 1.2, -20)):
        tab = g.piece(name, "TORSO", (-1, 0, -.5), (2, 2, 1), pivot=(x + 1, -.4, -2.2), rotation=(0, 0, rot))
        solid(tab, "S", "weave", 108, 4, edge=False)
