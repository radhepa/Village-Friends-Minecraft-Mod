"""Curly Undercut: faded sides and nape under a mop of loose curls on top that flop forward onto the
brow, stopping above the eyes."""
from anime_male import clipped, clipped_scalp, ringlet_face, taper
from paint import curls_box, curls_face

META = {"name": "Curly Undercut", "gender": "male",
        "description": "Faded sides under a mop of loose curls flopping forward onto the brow."}

TOP = [(-2.4, -2.4, 2), (.4, -2.8, 2), (2.6, -1.8, 2), (-2.6, .6, 2), (0, .2, 3), (2.4, .8, 2), (-1.2, 2.8, 2), (1.6, 3.0, 2)]


def build(g):
    clipped_scalp(g, 5201, base=1, side_rows=7, back_rows=7, fade_rows=4, sideburn=0)
    hat = g.part("hat")
    curls_face(hat.top, 5202, 3)
    for face in (hat.right, hat.left, hat.back):
        clipped(face, 5203 + face.x0, 2, rows=[0])
    hat.front.hline(0, 7, 0, "H2")
    for i, (x, z, h) in enumerate(TOP):
        box = g.piece(f"curls_{i}", "HEAD", (-1.5, -h, -1.5), (3, h, 3), pivot=(x, -8.2, z),
                      rotation=(-8 if z < 0 else 4, (i * 29) % 40 - 20, (i % 3 - 1) * 8))
        curls_box(box, 5210 + i * 3)
    # Curls flopping forward onto the brow.
    for i, (x, rz) in enumerate(((-2.8, 14), (-.9, 4), (1.0, -6), (2.9, -16))):
        taper(g, f"flop_{i}", (x, -8.9, -4.0), (-28, 0, rz), ((2, 2, 2), (1, 2, 1)), seed=5240 + i * 3, painter=ringlet_face)
    for i, x in enumerate((-1.4, 1.4)):
        taper(g, f"crown_curl_{i}", (x, -8.6, 3.8), (40, 0, -x * 8), ((2, 2, 2), (1, 1, 1)), seed=5260 + i * 3, painter=ringlet_face)
