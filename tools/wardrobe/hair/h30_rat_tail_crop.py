"""Rat-Tail Crop: a short pointed crop with one thin braided tail falling from the nape."""
from anime import bangs, cel_box, lock, ring_shell, spike
from paint import scalp, solid

META = {"name": "Rat-Tail Crop", "gender": "male", "description": "A short pointed crop with a thin braided tail from the nape."}


def build(g):
    scalp(g, 3001, side_rows=4, back_rows=7, sideburn=2)
    ring_shell(g, 3002, side_rows=3, back_rows=6)
    bangs(g, "bang", [(-2.2, ((2, 2), (1, 1)), 12), (0, ((3, 2), (1, 1)), 0), (2.2, ((2, 2), (1, 1)), -12)], 3010)
    for i, (x, z) in enumerate(((-2.4, -1.4), (0, -1.8), (2.4, -1.4), (-1.6, 1.4), (1.6, 1.4))):
        spike(g, f"crop_{i}", (x, -8.1, z), (-(z + 1) * 9, 0, x * 8), ((3, 1), (1, 1)), 2, 3020 + i * 3)
    for side, sign in (("right", -1), ("left", 1)):
        lock(g, f"{side}_point", (4.25 * sign, -7.6, -1.0), (0, 0, -8 * sign), ((2, 2), (1, 1)), 2, 3040 + (sign > 0))
    pivot = (0, -1.2, 4.6)
    for i in range(6):
        dx = -.25 if i % 2 else .25
        plait = g.piece(f"rat_tail_{i}", "HEAD", (dx - .5, i * 1.15, -.5), (1, 1, 1), pivot=pivot, rotation=(-6, 0, 0), inflate=.08, motion="sway")
        cel_box(plait, 3050 + i, top_delta=0)
    tie = g.piece("rat_tail_tie", "HEAD", (-.5, 6.9, -.5), (1, 1, 1), pivot=pivot, rotation=(-6, 0, 0), inflate=.15, motion="sway")
    solid(tie, "A", "plain", 3060, 2, edge=False)
    tip = g.piece("rat_tail_tip", "HEAD", (-.5, 8.0, -.5), (1, 2, 1), pivot=pivot, rotation=(-6, 0, 0), motion="sway")
    cel_box(tip, 3061, top_delta=0)
