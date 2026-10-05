"""High Ponytail: pulled up to a tie at the crown, a long tail sweeping down the back; pointed bangs."""
from anime import bangs, cel_box, lock, ring_shell, sidelocks
from paint import scalp, solid

META = {"name": "High Ponytail", "description": "A high, swinging ponytail with pointed bangs and slim sidelocks."}


def build(g):
    scalp(g, 1701, side_rows=4, back_rows=8, sideburn=1)
    head = g.part("head")
    for y in range(8):   # combed up toward the tie
        head.back.set(2, y, "H1"), head.back.set(5, y, "H3")
    ring_shell(g, 1702, side_rows=2, back_rows=6)
    bangs(g, "bang", [(-2.1, ((3, 2), (1, 1)), 10), (0.2, ((3, 2), (1, 1)), -2), (2.4, ((2, 2), (1, 1)), -12)], 1710)
    sidelocks(g, "sidelock", 7, 1720, width=1, flare=2)
    root = g.piece("tail_root", "HEAD", (-1.5, -2, -1.5), (3, 2, 3), pivot=(0, -8.2, 2.6), rotation=(-30, 0, 0))
    cel_box(root, 1730)
    tie = g.piece("tail_tie", "HEAD", (-1, -1, -1), (2, 1, 2), pivot=(0, -10.0, 3.6), rotation=(-30, 0, 0), inflate=.15)
    solid(tie, "A", "plain", 1731, 2, edge=False)
    lock(g, "tail", (0, -10.4, 4.2), (24, 0, 0), ((3, 5), (3, 4), (2, 3), (1, 2)), 2, 1740, motion="sway")
