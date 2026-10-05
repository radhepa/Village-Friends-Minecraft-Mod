"""Back Braid: a long single braid down the back tied off with a ribbon, pointed bangs in front."""
from anime import bangs, cel_box, ring_shell, sidelocks
from paint import k, scalp, solid

META = {"name": "Back Braid", "description": "A long plaited braid down the back with a ribbon tie and pointed bangs."}


def build(g):
    scalp(g, 1801, side_rows=5, back_rows=8, sideburn=1)
    ring_shell(g, 1802, side_rows=4, back_rows=7)
    bangs(g, "bang", [(-3.9, ((2, 3), (1, 1)), 8), (-1.7, ((3, 2), (1, 1)), 8), (0.5, ((3, 2), (1, 1)), -4), (2.6, ((2, 2), (1, 1)), -10)], 1810)
    sidelocks(g, "sidelock", 6, 1820, width=1)
    gather = g.piece("braid_root", "HEAD", (-2, 0, -1), (4, 3, 2), pivot=(0, -4.2, 4.4))
    cel_box(gather, 1830)
    # Plaits alternate left and right of the braid's axis, all swinging together from the nape.
    pivot = (0, -1.6, 4.9)
    for i in range(6):
        dx = -.45 if i % 2 else .45
        plait = g.piece(f"braid_{i}", "HEAD", (dx - 1, i * 1.8, -1), (2, 2, 2), pivot=pivot, rotation=(-8, 0, 0), motion="sway")
        cel_box(plait, 1840 + i, ring=0, top_delta=0)
        plait.back.set(0 if dx < 0 else 1, 1, "H1")
    tie = g.piece("braid_tie", "HEAD", (-1, 10.8, -1), (2, 1, 2), pivot=pivot, rotation=(-8, 0, 0), inflate=.1, motion="sway")
    solid(tie, "A", "plain", 1850, 2, edge=False)
    tuft = g.piece("braid_tuft", "HEAD", (-1, 11.8, -1), (2, 2, 2), pivot=pivot, rotation=(-8, 0, 0), motion="sway")
    cel_box(tuft, 1851, top_delta=0)
