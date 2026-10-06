"""High Bun: sleek hair drawn up into a round bun on the crown, wisps of baby hair at the temples and nape."""
from anime import cel_box, ring_shell
from anime_female import bun, combed, strand, swept_sides, wrap_face, SIDES
from paint import k, scalp

META = {"name": "High Bun", "gender": "female",
        "description": "A neat round bun high on the crown, with soft wisps escaping at the temples and nape."}


def build(g):
    scalp(g, 7001, side_rows=8, back_rows=8, sideburn=0)
    swept_sides(g)
    head = g.part("head")
    combed(head.back, (1, 2, 5, 6))
    combed(head.top, (1, 3, 4, 6))
    hat = ring_shell(g, 7002, side_rows=2, back_rows=4)
    combed(hat.back, (2, 5), rows=range(1, 4))
    # A smooth lifted front instead of bangs, so the face is open.
    front = g.piece("smooth_front", "HEAD", (-3.5, -1, -1), (7, 1, 3), pivot=(0, -8.45, -3.0), rotation=(12, 0, 0))
    cel_box(front, 7010, ring=None, top_delta=1, clump=4)
    base = g.piece("bun_base", "HEAD", (-2, -.5, -2), (4, 1, 4), pivot=(0, -8.9, .6), rotation=(-16, 0, 0), inflate=.1)
    for f in base.sides:
        wrap_face(f, 7020, 2)
    base.top.fill(k("H", 3)), base.bottom.fill(k("H", 1))
    bun(g, "bun", (0, -10.6, .9), (-16, 0, 0), (5, 3, 5), seed=7030)
    for side, sign in SIDES:
        strand(g, f"{side}_temple_wisp", (4.3 * sign, -7.6, -3.6), (0, 0, -6 * sign), ((1, 3), (1, 2, .5 * sign)), 1,
               7040 + (sign > 0), texture="wave")
        strand(g, f"{side}_nape_wisp", (1.8 * sign, -1.3, 4.35), (8, 0, -10 * sign), ((1, 2), (1, 1)), 1, 7045 + (sign > 0), ring=None)
