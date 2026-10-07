"""Braided High Tail: drawn up to a leather tie at the crown, the tail plaited as it arcs back and falls down the back."""
from anime import cel_box, ring_shell
from anime_female import combed, finish, plait_path, pointed, points, swept_sides, tie, SIDES
from paint import scalp

META = {"name": "Braided High Tail", "gender": "female",
        "description": "Hair drawn up to a leather tie at the crown, the tail plaited as it arcs back and falls."}


def build(g):
    scalp(g, 9501, side_rows=8, back_rows=8, sideburn=0, part=2)
    swept_sides(g)
    head = g.part("head")
    combed(head.back, (1, 3, 4, 6))
    hat = ring_shell(g, 9502, side_rows=2, back_rows=5)
    combed(hat.back, (2, 5), rows=range(1, 5))
    points(g, "bang", [(-2.8, 3, 2, 2, -10), (-.6, 3, 2, 2, -16), (1.6, 2, 2, 2, -20)], 9510)
    pointed(g, "left_sidelock", (4.3, -7.6, -3.4), (0, 0, -3), 2, 6, 2, seed=9515)
    root = g.piece("tail_root", "HEAD", (-1.5, -2, -1.5), (3, 2, 3), pivot=(0, -8.2, 2.6), rotation=(-30, 0, 0))
    cel_box(root, 9520)
    tie(g, "crown_tie", (0, -9.7, 3.4), (-30, 0, 0), (3, 1, 3), y=-.5, role="L", inflate=.2)
    pivot = (0, -10.0, 3.9)
    angles = [(50, 0), (32, 0), (18, 0), (8, 0), (3, 0), (0, 0), (-2, 0), (-3, 0), (-3, 0)]
    boxes, end, rot, w = plait_path(g, "plait", pivot, angles, w=3, d=2, seed=9530, taper=6)
    finish(g, "plait", pivot, end, rot, w, 2, "A", ((2, 2), (1, 1)), seed=9550)
