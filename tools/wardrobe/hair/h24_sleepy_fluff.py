"""Sleepy Fluff: soft, bed-tousled hair in rounded fluffy tufts pointing every which way."""
from anime import bangs, cel_box, ring_shell
from paint import scalp

META = {"name": "Sleepy Fluff", "gender": "male", "description": "Soft, tousled fluff in rounded tufts, as if just out of bed."}

TUFTS = [(-2.8, -9.0, -2.4, 20, 0, 30), (-.4, -9.4, -2.8, 30, 0, -10), (2.2, -9.1, -2.2, 18, 0, -34), (-3.4, -8.8, .6, 0, 0, 48),
         (-.8, -9.6, .2, -10, 0, 16), (1.8, -9.4, .6, -14, 0, -22), (3.6, -8.6, 1.2, 0, 0, -50), (-2.0, -9.0, 3.0, -36, 0, 18),
         (.8, -9.2, 3.2, -40, 0, -12), (-4.6, -6.0, -1.0, 0, 0, 70), (4.6, -6.2, -.4, 0, 0, -72), (0, -5.0, 4.8, -60, 0, 0)]


def build(g):
    scalp(g, 2401, side_rows=6, back_rows=8, sideburn=2)
    ring_shell(g, 2402, side_rows=5, back_rows=8)
    for i, (x, y, z, rx, ry, rz) in enumerate(TUFTS):
        tuft = g.piece(f"tuft_{i}", "HEAD", (-1.5, -1.5, -1.5), (3, 2, 3), pivot=(x, y, z), rotation=(rx, ry, rz))
        cel_box(tuft, 2410 + i * 3, base=2 + (i % 3 == 0), top_delta=1, clump=2)
    bangs(g, "bang", [(-4.1, ((2, 3), (1, 1)), 18), (-2.0, ((3, 2), (2, 1)), 12), (0.6, ((3, 2), (2, 1)), -8), (2.8, ((2, 2), (1, 1)), -18)], 2450)
