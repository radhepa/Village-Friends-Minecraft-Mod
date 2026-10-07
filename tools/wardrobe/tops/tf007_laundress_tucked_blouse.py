"""Laundress's Tucked Blouse: a drawstring blouse tucked in, sleeves tied above the elbow, a kerchief knotted on the chest."""
from kit_female import chemise
from paint import fabric, solid

META = {
    "name": "Laundress's Tucked Blouse",
    "gender": "female",
    "description": "A drawstring linen blouse tucked into the skirt, sleeves tied up for the washtub and a knotted kerchief.",
    "tags": ["casual", "work"],
    "tucked": True,
}


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 10701, neckline="wide", sleeve_rows=(0, 5))
    body.front.hline(1, 6, 1, "S2")
    body.front.set(3, 1, "A2"), body.front.set(4, 1, "A3")   # the drawstring tie
    for arm in arms:
        arm.strip.hline(0, 15, 4, "A2")                    # cord tying the sleeve up
        for x in range(0, 16, 2):
            arm.strip.set(x, 5, "S2")
        arm.front.vline(2, 0, 3, "S2")
    # Kerchief over the shoulders, its ends knotted on the chest.
    j = g.part("jacket")
    for y in range(6):
        for x in range(8):
            if abs(x - 3.5) <= 3.8 - y * .65:
                j.back.set(x, y, "P2" if (x + y) % 3 else "P1")
    for x, y in [(0, 0), (1, 0), (6, 0), (7, 0), (1, 1), (2, 1), (5, 1), (6, 1), (2, 2), (5, 2)]:
        j.front.set(x, y, "P2")
    for face in (j.right, j.left):
        face.hline(0, 3, 0, "P2"), face.hline(1, 2, 1, "P1")
    fabric(j.top, "P", "weave", 10702, 3)
    knot = g.piece("kerchief_knot", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(0, 3.4, -2.6))
    solid(knot, "P", "weave", 10703, 2)
    for side, x, rot in (("right", -.6, 12), ("left", .6, -12)):
        end = g.piece(f"kerchief_end_{side}", "TORSO", (-.5, 0, -.5), (1, 3, 1), pivot=(x, 4.2, -2.6), rotation=(0, 0, rot))
        solid(end, "P", "weave", 10704, 2)
