"""Double Buns: two round buns high on either side of the crown, pointed bangs and a short layered back."""
from anime import ring_shell
from anime_female import bun, fall, pointed, points, tie, SIDES
from paint import scalp

META = {"name": "Double Buns", "gender": "female",
        "description": "Two round buns high on the crown, pointed bangs, slim sidelocks and a short layered nape."}


def build(g):
    scalp(g, 7101, side_rows=7, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 7102, side_rows=5, back_rows=7)
    hat.top.vline(3, 0, 7, "H1")
    points(g, "bang", [(-2.7, 3, 2, 2, 10), (-.5, 3, 2, 2, 2), (1.7, 3, 2, 2, -6), (3.7, 2, 2, 2, -12)], 7110)
    for side, sign in SIDES:
        pointed(g, f"{side}_sidelock", (4.3 * sign, -7.6, -3.4), (0, 0, -3 * sign), 2, 6, 2, seed=7120 + (sign > 0))
        tie(g, f"{side}_bun_band", (3.0 * sign, -8.7, .6), (0, 0, -24 * sign), (3, 1, 3), y=-.5, inflate=.1)
        bun(g, f"{side}_bun", (3.55 * sign, -10.0, .6), (0, 0, -24 * sign), (4, 3, 4), seed=7130 + (sign > 0) * 3)
    fall(g, "nape", [(-2.8, -7.4, 4.35, ((3, 6), (2, 2)), 4, 8), (-.7, -7.5, 4.7, ((3, 7), (1, 2)), 3, 2),
                     (1.4, -7.5, 4.35, ((3, 7), (2, 2)), 3, -3), (3.3, -7.4, 4.7, ((2, 6), (1, 2)), 4, -8)], 7140)
