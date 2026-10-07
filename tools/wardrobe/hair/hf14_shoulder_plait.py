"""Shoulder Plait: everything gathered at the left nape into one thick plait brought over the shoulder."""
from anime import ring_shell
from anime_female import fall, finish, plait_path, pointed, points, strand
from paint import scalp

META = {"name": "Shoulder Plait", "gender": "female",
        "description": "One thick plait gathered at the nape and worn over the shoulder, with side-swept bangs."}


def build(g):
    scalp(g, 6401, side_rows=6, back_rows=8, sideburn=0, part=2)
    hat = ring_shell(g, 6402, side_rows=5, back_rows=7)
    hat.top.vline(2, 0, 7, "H1")
    points(g, "bang", [(-2.6, 3, 2, 2, -12), (-.4, 3, 2, 2, -18), (1.8, 2, 2, 2, -22)], 6410)
    pointed(g, "right_temple", (-4.3, -7.6, -3.4), (0, 0, 5), 2, 7, 2, seed=6420)
    strand(g, "right_side", (-4.45, -7.8, .8), (-10, 0, 8), ((1, 6),), 5, 6422)
    strand(g, "left_side", (4.45, -7.8, .8), (-14, 0, -2), ((1, 5),), 4, 6423)
    fall(g, "gather", [(-2.6, -7.5, 4.4, ((3, 6), (2, 2)), 0, -30), (0, -7.6, 4.6, ((3, 5), (2, 2)), 0, -22),
                       (2.4, -7.4, 4.4, ((2, 4),), 0, -10)], 6430)
    pivot = (3.6, -3.4, 3.2)
    angles = [(-65, -35), (-70, -20), (-60, -8), (-30, 0), (-12, 4), (-8, 4), (-6, 2), (-4, 0)]
    boxes, end, rot, w = plait_path(g, "plait", pivot, angles, w=3, d=2, seed=6440, taper=6)
    finish(g, "plait", pivot, end, rot, w, 2, "A", ((2, 2), (1, 2)), seed=6450)
