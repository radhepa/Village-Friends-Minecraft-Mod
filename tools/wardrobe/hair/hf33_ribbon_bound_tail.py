"""Ribbon-Bound Tail: a long low tail bound with ribbons at intervals, so it falls in soft bubbles to the waist."""
from anime import ring_shell
from anime_female import fall, paint, pointed, points, strand, tie, SIDES
from paint import scalp

META = {"name": "Ribbon-Bound Tail", "gender": "female",
        "description": "A long low tail bound with ribbons down its length, falling in soft bubbles to the waist."}


def build(g):
    scalp(g, 8301, side_rows=7, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 8302, side_rows=5, back_rows=7)
    hat.top.vline(3, 0, 7, "H1")
    points(g, "bang", [(-1.7, 3, 2, 2, 14), (1.5, 3, 2, 2, -14), (-3.9, 2, 2, 2, 4), (3.9, 2, 2, 2, -4)], 8310)
    for side, sign in SIDES:
        pointed(g, f"{side}_sidelock", (4.3 * sign, -7.6, -3.4), (0, 0, -3 * sign), 2, 8, 2, seed=8320 + (sign > 0))
    fall(g, "gather", [(-2.2, -7.6, 4.4, ((3, 6),), 0, 14), (2.2, -7.6, 4.4, ((3, 6),), 0, -14)], 8330)
    gather = g.piece("gather_root", "HEAD", (-2, 0, -1), (4, 3, 2), pivot=(0, -4.0, 4.4))
    paint(gather, "cel", 8333, 2, ring=0)
    # The tail swells between ribbons: hair, ribbon, hair, ribbon... each band pinching it in.
    pivot, rot = (0, -1.4, 4.9), (-4, 0, 0)
    tie(g, "ribbon_0", pivot, rot, (3, 1, 2), y=-.6, inflate=.15, motion="sway")
    strand(g, "tail", pivot, rot, ((3, 4, 0, 2), (3, 4, 0, 2), (3, 3, 0, 2), (2, 2, 0, 2), (1, 2, 0, 1)), 1, 8340, motion="sway",
           start=.4)
    for i, (y, w) in enumerate(((4.4, 3), (8.4, 3), (11.4, 2))):
        tie(g, f"ribbon_{i + 1}", pivot, rot, (w, 1, 2), y=y - .5, inflate=.22, motion="sway")
