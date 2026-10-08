"""Knitted Shawl over Chemise: a hand-knitted triangle shawl over a linen chemise, its ends crossed on the chest and knotted behind."""
from kit_female import chemise, hanging
from paint import fabric, k, solid

META = {
    "name": "Knitted Shawl over Chemise",
    "gender": "female",
    "description": "A hand-knitted triangle shawl over a plain linen chemise, its ends crossed over the chest and knotted at the small of the back.",
    "tags": ["casual", "knit", "simple"],
}


def band(cx, y, half=1.2):
    return lambda x, yy: yy == y and abs(x - cx) <= half


def build(g):
    body, arms = chemise(g, "S", 3, "weave", 60080, neckline="scoop", sleeve_rows=(0, 11))
    for arm in arms:
        arm.strip.hline(0, 15, 10, "S2")
        for x in range(0, 16, 2):
            arm.strip.set(x, 11, "S4")                                  # a soft frill at the wrist
    j = g.part("jacket")
    # Front: the two ends cross over the chest (left over right) and run round the waist.
    for y in range(0, 10):
        for cx, edge in ((.6 + y * .62, "P1"), (6.4 - y * .62, "P1")):
            for x in range(8):
                d = abs(x - cx)
                if d <= 1.25:
                    j.front.set(x, y, edge if d > .75 else k("P", 2 + (1 if (x + y) % 3 == 0 else 0)))
    fabric(j.front, "P", "knit", 60081, 2, 0, 8, 8, 2, mask=lambda x, y: j.front.get(x, y) is None)
    j.front.hline(0, 7, 9, "P1")
    for face in (j.right, j.left):
        fabric(face, "P", "knit", 60082, 2, 0, 0, 4, 3)
        fabric(face, "P", "knit", 60083, 2, 0, 8, 4, 2)
        face.hline(0, 3, 9, "P1")
    fabric(j.top, "P", "knit", 60084, 3)
    # Back: the triangle point falls to the waist under the knotted ends.
    for y in range(10):
        half = 4.0 if y < 3 else 4.0 - (y - 2) * .52
        for x in range(8):
            d = abs(x - 3.5)
            if d <= half:
                j.back.set(x, y, "P1" if d > half - .6 and y >= 3 else k("P", 2 - (1 if x % 3 == 2 and y % 2 == 0 else 0)))
    fabric(j.back, "P", "knit", 60085, 2, 0, 8, 8, 2)
    j.back.hline(0, 7, 9, "P1")
    # Thickness of the shawl on the shoulders and round the back of the neck.
    for side, x in (("right", -4.6), ("left", 1.6)):
        roll = g.piece(f"shawl_{side}_shoulder", "TORSO", (x, -.7, -2.7), (3, 2, 5), inflate=.04)
        solid(roll, "P", "knit", 60086 + (side == "left"), 2, edge=False)
        for face in roll.sides:
            face.hline(0, face.w - 1, 1, "P1")
    neck_roll = g.piece("shawl_neck_back", "TORSO", (-1.5, -.7, 1.7), (3, 2, 1), inflate=.04)
    solid(neck_roll, "P", "knit", 60088, 2, edge=False)
    knot = g.piece("shawl_knot", "TORSO", (-1, -1, -.5), (2, 2, 1), pivot=(0, 8.4, 2.6))
    solid(knot, "P", "knit", 60089, 2, edge=False)
    knot.back.set(0, 0, "P3"), knot.back.set(1, 1, "P1")
    for i, (x, length) in enumerate(((-.7, 4), (.7, 3))):
        tail = hanging(g, f"shawl_end_{i}", x, length, role="P", base=2, top=8.8, back=True, texture="knit")
        for face in (tail.back, tail.front):
            face.set(0, length - 1, "P4" if i else "P1")              # the fringed tips
