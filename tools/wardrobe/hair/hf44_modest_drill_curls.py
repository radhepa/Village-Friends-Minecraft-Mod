"""Modest Drill Curls: two neat spiral drills in front of the shoulders, long straight hair behind, soft pointed bangs."""
from anime import ring_shell
from anime_female import fall, points, strand, SIDES
from paint import scalp

META = {"name": "Modest Drill Curls", "gender": "female",
        "description": "Two neat spiral drill curls framing the face to the chest, with long straight hair behind."}


def drill(sign):
    """A tapering spiral: each turn a little narrower and stepped to alternate sides."""
    return ((3, 2, 0, 3), (3, 2, .3 * sign, 3), (2, 2, -.3 * sign, 2), (2, 2, .3 * sign, 2), (1, 2, 0, 1))


def build(g):
    scalp(g, 9401, side_rows=8, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 9402, side_rows=7, back_rows=8)
    hat.top.vline(3, 0, 7, "H1")
    points(g, "bang", [(-2.6, 3, 2, 2, 10), (-.4, 3, 2, 2, 2), (1.8, 3, 2, 2, -6), (3.7, 2, 2, 2, -12)], 9410)
    for side, sign in SIDES:
        strand(g, f"{side}_root", (4.5 * sign, -7.6, -3.0), (0, 0, -2 * sign), ((2, 4),), 2, 9420 + (sign > 0))
        strand(g, f"{side}_drill", (4.85 * sign, -4.0, -3.4), (0, 0, -3 * sign), drill(sign), 1, 9423 + (sign > 0) * 9,
               texture="ringlet", motion="sway")
        strand(g, f"{side}_side", (4.45 * sign, -7.8, 1.2), (0, 0, -3 * sign), ((1, 8),), 4, 9440 + (sign > 0))
    fall(g, "back", [(-3.2, -7.6, 4.3, ((3, 12), (2, 2), (1, 2)), -3, 4), (-1.0, -7.7, 4.65, ((3, 13), (2, 2), (1, 2)), -3, 1),
                     (1.1, -7.7, 4.3, ((3, 13), (2, 2), (1, 2)), -3, -1), (3.2, -7.6, 4.65, ((3, 11), (2, 2), (1, 2)), -3, -4)],
         9450, motion="sway", texture="sleek")
