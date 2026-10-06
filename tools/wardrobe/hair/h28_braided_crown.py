"""Braided Crown: a plait wrapped around the head like a circlet, wispy bangs and loose sidelocks."""
from anime import bangs, cel_box, ring_shell, sidelocks
from paint import scalp

META = {"name": "Braided Crown", "gender": "male", "description": "A plait circling the head like a crown, with wispy bangs and loose sidelocks."}


def build(g):
    scalp(g, 2801, side_rows=5, back_rows=8, sideburn=0)
    ring_shell(g, 2802, side_rows=4, back_rows=7)
    # The circlet: plaits around the head just above the hairline, alternating in and out.
    plaits = [(-3.8, -4.4, 0), (-1.3, -4.6, 0), (1.3, -4.6, 0), (3.8, -4.4, 0),     # front
              (4.6, -2.0, 90), (4.7, .6, 90), (4.6, 3.2, 90),                         # wearer's left
              (2.6, 4.6, 0), (0, 4.8, 0), (-2.6, 4.6, 0),                             # back
              (-4.6, 3.2, 90), (-4.7, .6, 90), (-4.6, -2.0, 90)]                      # wearer's right
    for i, (x, z, ry) in enumerate(plaits):
        plait = g.piece(f"plait_{i}", "HEAD", (-1.3, -1, -.8), (3, 2, 2), pivot=(x, -7.7 - (i % 2) * .3, z), rotation=(0, ry, 8 if i % 2 else -8))
        cel_box(plait, 2810 + i * 3, base=2 + (i % 2), ring=0, top_delta=1, clump=2)
    bangs(g, "bang", [(-1.8, ((2, 2), (1, 1)), 10), (0.4, ((2, 2), (1, 1)), -4), (2.4, ((2, 2), (1, 1)), -12)], 2860)
    sidelocks(g, "sidelock", 7, 2870, width=1, flare=2, x=4.35)
