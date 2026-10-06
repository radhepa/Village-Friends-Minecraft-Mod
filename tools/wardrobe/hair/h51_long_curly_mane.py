"""Long Curly Mane: loose spiral curls past the shoulders, springing out wide at the sides, with a few
short curls over the brow and long ones framing the face."""
from anime import ring_shell
from anime_male import SIDES, ringlet_face, taper
from paint import curls_box, curls_face, scalp

META = {"name": "Long Curly Mane", "gender": "male",
        "description": "Loose spiral curls springing wide and falling past the shoulders."}


def build(g):
    scalp(g, 5101, side_rows=8, back_rows=8, sideburn=0)
    hat = ring_shell(g, 5102, side_rows=7, back_rows=8)
    curls_face(hat.top, 5103, 3)
    for i, (x, z) in enumerate(((-2.0, -1.8), (2.0, -1.6), (-1.8, 1.8), (1.9, 2.0))):
        box = g.piece(f"crown_{i}", "HEAD", (-1.5, -2, -1.5), (3, 2, 3), pivot=(x, -8.1, z), rotation=(0, i * 25, (i % 2) * 12 - 6))
        curls_box(box, 5110 + i * 3)
    for i, (x, rz) in enumerate(((-2.4, 12), (0, -4), (2.3, -14))):
        taper(g, f"brow_{i}", (x, -8.55, -4.3), (-14, 0, rz), ((2, 3, 1),), seed=5120 + i * 3, painter=ringlet_face)
    for side, sign in SIDES:
        taper(g, f"{side}_frame", (4.45 * sign, -7.8, -3.3), (-4, 0, -6 * sign), ((2, 7, 2), (1, 3, 1)), seed=5130 + (sign > 0),
              painter=ringlet_face)
        for j, (z, flare) in enumerate(((-.9, 12), (1.9, 16))):
            taper(g, f"{side}_curl_{j}", (4.5 * sign, -7.7, z), (j * 6, 0, -flare * sign), ((3, 7, 2), (2, 3, 2), (1, 2, 1)),
                  seed=5140 + j * 5 + (sign > 0) * 11, painter=ringlet_face)
    for i, (x, rz) in enumerate(((-3.0, 12), (-1.0, 4), (1.0, -4), (3.0, -12))):
        taper(g, f"back_curl_{i}", (x, -7.6, 4.5), (10 + (i % 2) * 6, 0, rz), ((3, 9, 2), (2, 3, 1)), seed=5170 + i * 5,
              painter=ringlet_face, motion="sway")
