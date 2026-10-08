"""Wrap-Over Linen Skirt: a linen wrap skirt whose bound outer edge curves away to show the under-wrap, tied at the hip."""
from kit_female import SKIRT_FRONT, shoes, skirt, stockings_row
from paint import solid

META = {
    "name": "Wrap-Over Linen Skirt",
    "gender": "female",
    "description": "A light linen wrap skirt whose bound outer edge sweeps away in a curve to show the under-wrap, tied with a knot at the hip.",
    "tags": ["casual", "relaxed", "skirt"],
}

# Where the outer wrap's edge runs on the front panel: (x, last row it covers), right to left.
EDGE = [(0, 9), (1, 9), (2, 8), (3, 8), (4, 7), (5, 6), (6, 5), (7, 3), (8, 1), (9, 0)]


def build(g):
    s = skirt(g, "P", "weave", 60220, base=3, top=9.8, length=10, flare=6, folds=False)
    f = s.front.front
    for x, last in EDGE:
        for y in range(last + 1, f.h):
            f.set(x, y, "P2")                                          # the under-wrap, in the outer one's shadow
        f.set(x, last, "A2")                                           # the outer wrap's bound edge
        if last + 1 < f.h:
            f.set(x, last + 1, "P1")
    f.hline(0, 9, 9, "P1"), f.set(0, 9, "A2"), f.set(1, 9, "A2")
    for x in (2, 5):
        f.vline(x, 2, EDGE[x][1] - 1, "P2")                             # soft folds in the outer wrap
    b = s.back.back
    for x in (2, 6):
        b.vline(x, 3, 8, "P2"), b.vline(x + 1, 4, 8, "P4")
    s.hem("P1")
    stockings_row(g, "S", 8, 9, base=2)
    shoes(g, "turnshoe", "L", 2)
    # The tie knotted at the left hip rides the front panel.
    for pid, x, y, size in (("waist_tie_knot", 3.4, .1, (2, 2, 1)), ("waist_tie_end_0", 3.0, 1.9, (1, 4, 1)),
                            ("waist_tie_end_1", 4.0, 1.9, (1, 3, 1))):
        w, h, d = size
        box = g.piece(pid, "TORSO", (x - w / 2, y, -d - .08), size, pivot=(0, s.top, SKIRT_FRONT), motion="flap_front")
        solid(box, "P", "plain", 60221, 3, edge=False)
        box.front.set(0, h - 1, "A2")
