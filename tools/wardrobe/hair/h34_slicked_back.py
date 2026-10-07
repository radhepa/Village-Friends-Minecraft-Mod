"""Slicked Back: glossy hair combed straight back from a clean hairline in long smooth sections,
a gentle roll at the front and small points flicking out at the nape."""
from anime_male import SIDES, clump, combed_face, hat_ring, plate, taper
from paint import scalp

META = {"name": "Slicked Back", "gender": "male",
        "description": "Glossy hair combed straight back in smooth sections, small points flicking out at the nape."}


def build(g):
    scalp(g, 3401, side_rows=5, back_rows=8, sideburn=1)
    hat = hat_ring(g, 3402, rows={"back": 7, "right": 4, "left": 4})
    combed_face(hat.top, 3403, 3)
    hat.front.hline(0, 7, 0, "H2")
    # Long combed sections from the hairline to the crown, a sheen band across them.
    for i, x in enumerate((-3.0, -1.0, 1.0, 3.0)):
        plate(g, f"section_{i}", (x, -8.35 - (i % 2) * .15, .1), (2, 1, 8), rotation=(-3, 0, x * 1.5), seed=3410 + i, sheen=3)
    roll = clump(g, "front_roll", (0, -8.5, -3.7), (7, 1, 2), rotation=(16, 0, 0), origin=(-3.5, -1, -1), seed=3420, ring=None)
    combed_face(roll.top, 3421, 3, sheen=0)
    # Combed back over the ears and down the back of the head.
    for side, sign in SIDES:
        wing = clump(g, f"{side}_wing", (4.4 * sign, -8.2, .7), (1, 4, 6), rotation=(0, 0, -2 * sign), seed=3430 + (sign > 0))
        for f in (wing.right, wing.left):
            combed_face(f, 3432 + (sign > 0), 2, sheen=1, across_y=True)
    for i, x in enumerate((-2.6, 0, 2.6)):
        back = clump(g, f"back_{i}", (x, -8.9, 4.3), (3, 6, 1), rotation=(10, 0, -x * 1.5), seed=3440 + i)
        combed_face(back.back, 3443 + i, 2, sheen=1)
    for i, x in enumerate((-2.6, 0, 2.6)):
        taper(g, f"nape_{i}", (x, -3.4, 4.45), (8, 0, -x * 2), ((3, 2, 1), (1, 1, 1)), seed=3450 + i * 3, ring=0)
