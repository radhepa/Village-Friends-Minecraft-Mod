"""Straight-Back Cornrows: neat braids plaited flat to the scalp from the hairline straight over the
crown and down the back, ending in short braided tails at the nape."""
from anime_male import SIDES, cornrow, taper, plait_face
from paint import k

META = {"name": "Straight-Back Cornrows", "gender": "male",
        "description": "Neat braids plaited flat from the hairline straight back, ending in short tails at the nape."}

ROWS = (-3.3, -1.65, 0.0, 1.65, 3.3)


def build(g):
    head, hat = g.part("head"), g.part("hat")
    # Dark close hair under the braids, with pale parts between the rows.
    for face, rows in ((head.top, 8), (head.back, 7), (head.right, 5), (head.left, 5)):
        for y in range(rows):
            for x in range(face.w):
                face.set(x, y, k("H", 1))
    for col in (1, 3, 4, 6):
        head.top.vline(col, 0, 7, "X1")
    head.front.hline(0, 7, 0, "H1")
    head.front.set(0, 1, "H1"), head.front.set(7, 1, "H1")
    hat.front.hline(1, 6, 0, "H1")
    # Rows over the crown, then down the back of the head.
    for i, x in enumerate(ROWS):
        cornrow(g, f"row_{i}", (x, -8.0, -4.05), 8, width=1, seed=4710 + i * 5)
        cornrow(g, f"row_{i}_back", (x, -8.3, 4.0), 7, rotation=(-90, 0, x * 2), width=1, seed=4730 + i * 5, phase=1)
    # One row along each side above the ear.
    for side, sign in SIDES:
        cornrow(g, f"{side}_row", (4.0 * sign, -6.3, -3.4), 7, rotation=(0, 0, 90 * sign), width=1, seed=4750 + (sign > 0))
    # Short braided tails at the nape.
    for i, x in enumerate((-2.0, 0.0, 2.0)):
        taper(g, f"tail_{i}", (x * 1.1, -1.6, 4.5), (10, 0, -x * 4), ((1, 2, 1), (1, 1, 1)), seed=4760 + i * 3, painter=plait_face)
