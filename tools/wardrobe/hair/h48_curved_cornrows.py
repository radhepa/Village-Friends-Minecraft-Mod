"""Curved Cornrows: braids plaited flat in S-bends over the crown, gathered at the nape into a single
braided tail."""
from anime_male import SIDES, cornrow, cornrow_path, plait
from paint import k

META = {"name": "Curved Cornrows", "gender": "male",
        "description": "Cornrows plaited in S-bends over the crown and gathered into one braided tail."}


def build(g):
    head, hat = g.part("head"), g.part("hat")
    for face, rows in ((head.top, 8), (head.back, 7), (head.right, 5), (head.left, 5)):
        for y in range(rows):
            for x in range(face.w):
                face.set(x, y, k("H", 1))
    head.front.hline(0, 7, 0, "H1")
    head.front.set(0, 1, "H1"), head.front.set(7, 1, "H1")
    hat.front.hline(1, 6, 0, "H1")
    # S-bends over the crown, each row a little out of step with its neighbour.
    for i, x in enumerate((-2.9, -1.0, 1.0, 2.9)):
        bend = 22 if i % 2 == 0 else -22
        cornrow_path(g, f"row_{i}", (x, -8.0, -4.05), [(3, bend), (3, -bend), (3, bend * .6)], seed=4810 + i * 9)
    # Down the back of the head, converging on the tail.
    for i, x in enumerate((-3.0, -1.0, 1.0, 3.0)):
        cornrow(g, f"row_{i}_back", (x, -8.3, 4.0), 6, rotation=(-90, 0, x * 7), width=1, seed=4850 + i * 5, phase=1)
    for side, sign in SIDES:
        cornrow(g, f"{side}_row", (4.0 * sign, -6.4, -3.3), 7, rotation=(0, -6 * sign, 90 * sign), width=1, seed=4870 + (sign > 0))
    plait(g, "tail", (0, -2.2, 4.6), 5, rotation=(8, 0, 0), seed=4880, tie_role="A", motion="sway")
