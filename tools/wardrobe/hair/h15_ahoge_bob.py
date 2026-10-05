"""Ahoge Bob: a rounded jaw-length bob, soft bangs and a single strand curling up from the crown."""
from anime import bangs, cel_box, ring_shell
from paint import scalp

META = {"name": "Ahoge Bob", "description": "A rounded bob with soft bangs and one stubborn strand standing up."}


def build(g):
    scalp(g, 1501, side_rows=7, back_rows=8, sideburn=0)
    ring_shell(g, 1502, side_rows=7, back_rows=8)
    bangs(g, "bang", [(-4.15, ((2, 4), (1, 1)), 4), (-1.8, ((3, 2), (2, 1)), 6), (0.4, ((3, 2), (2, 1)), -2), (2.5, ((3, 2), (1, 1)), -8),
                      (4.15, ((2, 4), (1, 1)), -4)], 1510)
    for side, sign in (("right", -1), ("left", 1)):
        side_box = g.piece(f"{side}_bob", "HEAD", (-.5, 0, -3), (1, 7, 6), pivot=(4.3 * sign, -7.8, 1.0), rotation=(0, 0, -5 * sign))
        cel_box(side_box, 1520 + (sign > 0), ring=1)
        curl = g.piece(f"{side}_bob_curl", "HEAD", (-.5, 0, -3), (1, 1, 6), pivot=(4.1 * sign, -1.2, 1.0), rotation=(0, 0, 35 * sign))
        cel_box(curl, 1525 + (sign > 0), top_delta=0)
    back = g.piece("bob_back", "HEAD", (-4.5, 0, 0), (9, 7, 2), pivot=(0, -8.0, 3.9), rotation=(6, 0, 0))
    cel_box(back, 1530, ring=1)
    tuck = g.piece("bob_tuck", "HEAD", (-4, 0, -1), (8, 1, 2), pivot=(0, -1.3, 5.0), rotation=(-30, 0, 0))
    cel_box(tuck, 1531, top_delta=0)
    # The ahoge: two thin segments, bending forward at the tip.
    stem = g.piece("ahoge_stem", "HEAD", (-.5, -3, -.5), (1, 3, 1), pivot=(.4, -8.4, -.6), rotation=(-18, 0, 8))
    cel_box(stem, 1540, base=3, top_delta=0)
    tip = g.piece("ahoge_tip", "HEAD", (-.5, -2, -.5), (1, 2, 1), pivot=(.8, -11.2, .33), rotation=(55, 0, 14))
    cel_box(tip, 1541, base=3, top_delta=0)
