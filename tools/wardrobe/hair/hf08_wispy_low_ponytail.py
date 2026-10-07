"""Wispy Low Ponytail: a soft tail at the nape tied with a hair-wrapped band, loose wavy wisps at the temples."""
from anime import ring_shell
from anime_female import combed, fringe, paint, strand, wrap_face, SIDES
from paint import k, scalp

META = {"name": "Wispy Low Ponytail", "gender": "female",
        "description": "A soft low ponytail wrapped with its own hair, swept bangs and loose wisps at the temples."}


def build(g):
    scalp(g, 5801, side_rows=5, back_rows=8, sideburn=0)
    head = g.part("head")
    combed(head.back, (1, 2, 5, 6), rows=range(0, 6))
    hat = ring_shell(g, 5802, side_rows=3, back_rows=6)
    combed(hat.back, (2, 5), rows=range(2, 6))
    for side, sign in SIDES:
        crown = g.piece(f"crown_{side}", "HEAD", (-1.5, -1, -3), (3, 1, 6), pivot=(1.5 * sign, -8.3, .6), rotation=(-4, 0, 7 * sign))
        paint(crown, "sleek", 5803 + (sign > 0), 2, ring=None)
        strand(g, f"{side}_wisp", (4.35 * sign, -7.6, -3.5), (0, 0, -3 * sign), ((1, 4), (1, 3, .5 * sign), (1, 2, -.2 * sign)), 1,
               5806 + (sign > 0), texture="wave")
    fringe(g, "bang", [(-2.6, ((2, 2), (1, 1)), 18), (-.6, ((3, 2), (1, 1)), 12), (1.6, ((2, 2), (1, 1)), 6)], 5810)
    gather = g.piece("gather", "HEAD", (-2, 0, -1), (4, 3, 2), pivot=(0, -3.9, 4.35))
    paint(gather, "sleek", 5820, 2, ring=0)
    wrap = g.piece("hair_wrap", "HEAD", (-1.5, -.5, -1), (3, 1, 2), pivot=(0, -1.2, 4.9), inflate=.18)
    for f in wrap.sides:
        wrap_face(f, 5821, 2)
    wrap.top.fill(k("H", 3)), wrap.bottom.fill(k("H", 1))
    pivot = (0, -.9, 5.0)
    strand(g, "tail", pivot, (-4, 0, 0), ((3, 5), (2, 4), (1, 2)), 2, 5830, motion="sway")
    strand(g, "tail_wisp_r", pivot, (-2, 0, 9), ((1, 6), (1, 2)), 1, 5835, ring=None, motion="sway", z=.4)
    strand(g, "tail_wisp_l", pivot, (-6, 0, -8), ((1, 5), (1, 2)), 1, 5836, ring=None, motion="sway", z=.4)
