"""Long Low Tail: long hair tied at the nape into a tail reaching the waist, long bangs and sidelocks."""
from anime import bangs, cel_box, lock, ring_shell, sidelocks
from paint import scalp, solid

META = {"name": "Long Low Tail", "description": "A long tail tied low at the nape, with centre-parted bangs and long sidelocks."}


def build(g):
    scalp(g, 2501, side_rows=5, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 2502, side_rows=4, back_rows=8)
    hat.top.vline(3, 0, 7, "H1")
    bangs(g, "bang", [(-1.6, ((3, 2), (2, 1)), 20), (1.6, ((3, 2), (2, 1)), -20), (-4.1, ((2, 4), (1, 2)), 6), (4.1, ((2, 4), (1, 2)), -6)], 2510)
    sidelocks(g, "sidelock", 10, 2520, width=1, flare=2)
    gather = g.piece("gather", "HEAD", (-2, 0, -1), (4, 3, 2), pivot=(0, -4.6, 4.3))
    cel_box(gather, 2530, ring=0)
    tie = g.piece("tie", "HEAD", (-1, -.5, -1), (2, 1, 2), pivot=(0, -1.4, 4.9), inflate=.15)
    solid(tie, "A", "plain", 2531, 2, edge=False)
    lock(g, "tail", (0, -1.0, 4.9), (-6, 0, 0), ((3, 6), (2, 4), (2, 2), (1, 2)), 2, 2540, motion="sway")
