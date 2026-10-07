"""Layered Shag: a rounded, full shag to the jaw in stacked tiers, with a thick choppy fringe straight across."""
from anime import ring_shell
from anime_female import fall, paint, points, pointed, SIDES
from paint import scalp

META = {"name": "Layered Shag", "gender": "female",
        "description": "A rounded jaw-length shag in stacked layers with a thick, choppy fringe straight across."}


def build(g):
    scalp(g, 9301, side_rows=8, back_rows=8, sideburn=0)
    ring_shell(g, 9302, side_rows=7, back_rows=8)
    points(g, "bang", [(-3.3, 2, 2, 2, 3), (-1.65, 2, 1, 2, -1), (0, 2, 2, 2, 1), (1.65, 2, 1, 2, -2), (3.3, 2, 2, 2, -4)], 9310, rx=-12)
    for side, sign in SIDES:
        upper = g.piece(f"{side}_upper_tier", "HEAD", (-.5, 0, -3), (1, 4, 6), pivot=(4.6 * sign, -8.2, .4), rotation=(0, 0, -12 * sign))
        paint(upper, "cel", 9320 + (sign > 0), 2, ring=1)
        pointed(g, f"{side}_cheek", (4.5 * sign, -7.0, -3.2), (0, 0, -6 * sign), 2, 5, 2, seed=9323 + (sign > 0))
        pointed(g, f"{side}_jaw", (4.7 * sign, -6.6, -.4), (0, 0, -9 * sign), 2, 6, 2, seed=9326 + (sign > 0))
    fall(g, "upper_back", [(-2.6, -8.0, 5.0, ((3, 5),), 14, 10), (0, -8.1, 5.2, ((3, 5),), 14, 0), (2.6, -8.0, 5.0, ((3, 5),), 14, -10)],
         9340)
    fall(g, "lower_back", [(-2.8, -6.6, 4.4, ((3, 6), (2, 2)), 4, 6), (0, -6.6, 4.6, ((3, 7), (2, 2)), 4, 0),
                           (2.8, -6.6, 4.4, ((3, 6), (2, 2)), 4, -6)], 9350, motion="sway")
