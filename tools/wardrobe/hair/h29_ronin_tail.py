"""Ronin Tail: long, loose hair tied off low on the back, messy pointed bangs and long sidelocks."""
from anime import back_fan, bangs, cel_box, lock, ring_shell, sidelocks
from paint import scalp, solid

META = {"name": "Ronin Tail", "description": "Long hair loosely tied far down the back, with messy pointed bangs."}


def build(g):
    scalp(g, 2901, side_rows=6, back_rows=8, sideburn=1)
    ring_shell(g, 2902, side_rows=5, back_rows=8)
    bangs(g, "bang", [(-4.1, ((2, 4), (1, 2)), 14), (-2.2, ((3, 2), (1, 1)), 16), (0, ((2, 2), (1, 1)), -6), (2.0, ((3, 2), (1, 1)), -14),
                      (4.1, ((2, 4), (1, 2)), -14)], 2910)
    sidelocks(g, "sidelock", 9, 2920, width=1, flare=5)
    back_fan(g, "loose", [(-3.0, ((2, 5), (1, 2)), 10, 8), (3.0, ((2, 5), (1, 2)), -10, 8)], 2930)
    mass = g.piece("mass", "HEAD", (-2, 0, -1), (4, 9, 2), pivot=(0, -7.4, 4.6), rotation=(8, 0, 0), motion="sway")
    cel_box(mass, 2940, ring=1)
    tie = g.piece("tie", "HEAD", (-1.5, 9, -1), (3, 1, 2), pivot=(0, -7.4, 4.6), rotation=(8, 0, 0), inflate=.12, motion="sway")
    solid(tie, "L", "leather", 2941, 2, edge=False)
    lock(g, "tail_end", (0, 2.6, 6.2), (8, 0, 0), ((3, 3), (2, 2), (1, 1)), 2, 2950, motion="sway")
