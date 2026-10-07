"""Waist-Length Layers: a long V-cut to the waist under a shoulder-blade top layer, wispy side-swept bangs."""
from anime import ring_shell
from anime_female import fall, pointed, points, strand, SIDES
from paint import scalp

META = {"name": "Waist-Length Layers", "gender": "female",
        "description": "Waist-length hair cut in a soft V with a shorter top layer and wispy side-swept bangs."}


def build(g):
    scalp(g, 5401, side_rows=7, back_rows=8, sideburn=0, part=2)
    hat = ring_shell(g, 5402, side_rows=7, back_rows=8)
    hat.top.vline(2, 0, 7, "H1")
    points(g, "bang", [(-2.9, 2, 2, 2, -12), (-1.1, 3, 2, 2, -18), (1.1, 3, 2, 2, -22), (3.2, 2, 2, 2, -16)], 5410)
    for side, sign in SIDES:
        # Chin-length face-framing layer, then the longer side falling behind the shoulder.
        pointed(g, f"{side}_frame", (4.3 * sign, -7.5, -3.3), (0, 0, -5 * sign), 2, 7, 2, seed=5420 + (sign > 0))
        strand(g, f"{side}_side", (4.4 * sign, -7.8, .6), (0, 0, -3 * sign), ((1, 7),), 4, 5424 + (sign > 0))
    fall(g, "under", [(-3.3, -7.6, 4.3, ((3, 11), (2, 2), (1, 2)), -2, 3),
                      (-1.1, -7.7, 4.65, ((3, 15), (2, 2), (1, 2)), -3, 1),
                      (1.1, -7.7, 4.3, ((3, 15), (2, 3), (1, 2)), -3, -1),
                      (3.3, -7.6, 4.65, ((3, 11), (2, 3), (1, 2)), -2, -3)], 5430, motion="sway")
    fall(g, "over", [(-2.5, -7.3, 5.05, ((3, 7), (2, 2), (1, 1)), 4, 7), (0, -7.4, 5.25, ((3, 8), (2, 2), (1, 1)), 3, 0),
                     (2.5, -7.3, 5.05, ((3, 7), (2, 2), (1, 1)), 4, -7)], 5460, motion="sway")
