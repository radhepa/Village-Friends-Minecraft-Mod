"""Widow's Peak: sleek hair swept back from a sharp pointed hairline, full wings over the ears and a
collar-length back whose ends flick out."""
from anime import ring_shell
from anime_male import SIDES, chain, clump, combed_face, plate, taper
from paint import scalp

META = {"name": "Widow's Peak", "gender": "male",
        "description": "Sleek hair swept back from a sharp pointed hairline, with collar-length flicked ends."}


def build(g):
    scalp(g, 7801, side_rows=6, back_rows=8, sideburn=1)
    head = g.part("head")
    head.front.set(1, 0, None), head.front.set(6, 0, None)
    head.front.set(0, 1, None), head.front.set(7, 1, None)
    hat = ring_shell(g, 7802, side_rows=5, back_rows=8)
    combed_face(hat.top, 7803, 3)
    # The peak: the hairline dips to a point in the middle of the brow.
    hat.front.hline(0, 7, 0, None)
    hat.front.hline(2, 5, 0, "H2")
    hat.front.hline(3, 4, 1, "H1")
    taper(g, "peak", (0, -8.45, -4.3), (-4, 0, 0), ((2, 1, 1), (1, 1, 1)), seed=7810, ring=0)
    # Swept straight back from the peak, rising a little at the front.
    for i, (x, w) in enumerate(((-2.4, 2), (-.8, 2), (.8, 2), (2.4, 2))):
        plate(g, f"swept_{i}", (x, -8.4 - (i in (1, 2)) * .25, .1), (w, 1, 8), rotation=(-5, 0, -x * 3), seed=7820 + i, sheen=2)
    for side, sign in SIDES:
        wing = clump(g, f"{side}_wing", (4.4 * sign, -8.0, .9), (1, 4, 6), rotation=(12, 0, -4 * sign), seed=7830 + (sign > 0))
        combed_face(wing.right if sign < 0 else wing.left, 7832 + (sign > 0), 2, sheen=1, across_y=True)
    # The collar-length back, flicking out at the ends.
    for i, x in enumerate((-2.7, -.9, .9, 2.7)):
        chain(g, f"back_{i}", (x, -8.0, 4.5), [(2, 7, 1, (4, 0, -x)), (2, 2, 1, (36, 0, -x * 4)), (1, 1, 1, (50, 0, -x * 5))],
              seed=7840 + i * 7, ring=1)
