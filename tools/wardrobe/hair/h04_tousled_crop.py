"""Tousled Crop: short, textured and tidy at the sides, with a ruffled top and a little fringe."""
from paint import hair_box, scalp, shell

META = {"name": "Tousled Crop", "description": "A short textured crop with ruffled tufts and a light fringe."}

TUFTS = [(-2.4, -2.2, 14, 10), (.4, -2.6, -12, -6), (2.6, -1.0, 6, -16), (-2.6, .8, -6, 18),
         (.2, .4, 10, 4), (2.0, 2.4, -14, -10), (-1.0, 2.8, -18, 8)]


def build(g):
    scalp(g, 301, side_rows=3, back_rows=6, sideburn=1)
    shell(g, 302, side_rows=1, back_rows=4, front=[(2, 1), (3, 1), (5, 1)])
    for i, (x, z, rx, rz) in enumerate(TUFTS):
        tuft = g.piece(f"tuft_{i}", "HEAD", (-1, -1, -1), (2, 1, 2), pivot=(x, -8.45, z), rotation=(rx, 0, rz))
        hair_box(tuft, 310 + i, 2, top_delta=2)
    for i, (x, rz) in enumerate(((-2.4, 14), (.4, -6), (2.8, -16))):
        fringe = g.piece(f"fringe_{i}", "HEAD", (-1, 0, -1), (2, 1, 1), pivot=(x, -8.4, -4.3), rotation=(-18, 0, rz))
        hair_box(fringe, 330 + i, 2)
