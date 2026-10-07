"""Loose Ringlets: ear-length spiral curls falling all round the head, a few short ringlets over the
brow and soft curl clusters on the crown."""
from anime import ring_shell
from anime_male import ringlet_face, taper
from paint import curls_box, curls_face, scalp

META = {"name": "Loose Ringlets", "gender": "male",
        "description": "Ear-length spiral ringlets all round, with a few short curls over the brow."}


def build(g):
    scalp(g, 4201, side_rows=6, back_rows=8, sideburn=1)
    hat = ring_shell(g, 4202, side_rows=5, back_rows=7)
    curls_face(hat.top, 4203, 3)
    for i, (x, z) in enumerate(((-2.0, -1.6), (1.8, -2.0), (-1.6, 1.8), (2.0, 1.6))):
        box = g.piece(f"crown_{i}", "HEAD", (-1.5, -2, -1.5), (3, 2, 3), pivot=(x, -8.1, z), rotation=(0, i * 20, (i % 2) * 10 - 5))
        curls_box(box, 4210 + i * 3)
    # Short ringlets over the brow, all ending above it.
    for i, (x, rz) in enumerate(((-2.6, 10), (-.2, -4), (2.3, -12))):
        taper(g, f"brow_{i}", (x, -8.55, -4.3), (-12, 0, rz), ((2, 2, 1), (1, 1, 1)), seed=4220 + i * 3, painter=ringlet_face)
    # Ear-length ringlets round the sides, each swinging a little differently.
    for side, sign in (("right", -1), ("left", 1)):
        for j, (z, length, tilt) in enumerate(((-2.8, 4, 6), (-.4, 5, 10), (2.0, 5, 7))):
            taper(g, f"{side}_ringlet_{j}", (4.45 * sign, -7.6, z), ((j - 1) * 6, 0, -tilt * sign), ((2, length, 2), (1, 2, 1)),
                  seed=4230 + j * 5 + (sign > 0) * 17, painter=ringlet_face)
    for i, (x, length, rz) in enumerate(((-3.0, 5, 8), (-1.0, 6, 3), (1.0, 6, -3), (3.0, 5, -8))):
        taper(g, f"back_ringlet_{i}", (x, -7.4, 4.45), (10 + (i % 2) * 6, 0, rz), ((2, length, 2), (1, 2, 1)),
              seed=4270 + i * 5, painter=ringlet_face)
