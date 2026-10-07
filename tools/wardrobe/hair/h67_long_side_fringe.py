"""Long Side Fringe: a heavy fringe swept flat across the brow to the wearer's left, hanging past the
cheek on that side, over choppy crown layers that kick out behind and a long pointed nape. The
fringe stays above the eyes."""
from anime import ring_shell
from anime_male import chain, clump, combed_face, taper
from paint import scalp

META = {"name": "Long Side Fringe", "gender": "male",
        "description": "A heavy fringe swept across the brow and past one cheek, choppy layers kicking out behind."}


def build(g):
    scalp(g, 6701, side_rows=6, back_rows=8, sideburn=1, part=1)
    hat = ring_shell(g, 6702, side_rows=5, back_rows=8)
    combed_face(hat.top, 6703, 3, across_y=True)
    # The fringe: layered locks from the part on the right swept flat across the brow.
    for i, (y, rz, w, length) in enumerate(((-8.9, -66, 3, 6), (-8.4, -72, 2, 6), (-9.2, -60, 2, 5))):
        taper(g, f"sweep_{i}", (-2.7, y, -4.3 - i * .1), (-6, 0, rz), ((w, length, 1), (1, 1, 1)), seed=6710 + i * 3, ring=0)
    # Past the cheek on the left, outside the eye.
    chain(g, "fall_0", (4.4, -7.9, -3.5), [(2, 5, 1, (-6, 0, -6)), (2, 2, 1, (-14, 0, 2)), (1, 2, 1, (-18, 0, 6))], seed=6730, ring=1)
    taper(g, "fall_1", (4.5, -7.6, -2.0), (0, 0, -9), ((2, 5, 2), (1, 2, 1)), seed=6735, ring=1)
    # The parted side lies close.
    side = clump(g, "right_side", (-4.45, -8.0, .4), (1, 4, 6), seed=6740)
    combed_face(side.right, 6741, 2, across_y=True)
    # Choppy layers kicking out behind the crown.
    for i, (x, z, rx, rz) in enumerate(((-2.0, 1.6, -62, 14), (.4, 2.2, -70, -4), (2.4, 1.4, -58, -18))):
        taper(g, f"kick_{i}", (x, -8.3, z), (rx, 0, rz), ((3, 2, 2), (2, 1, 1), (1, 1, 1)), seed=6750 + i * 3, ring=0, up=True)
    for i, (x, length, rz) in enumerate(((-2.6, 5, 10), (-.8, 6, 3), (1.0, 6, -3), (2.8, 5, -10))):
        taper(g, f"nape_{i}", (x, -6.8, 4.45), (10, 0, rz), ((2, length, 1), (1, 2, 1)), seed=6770 + i * 3, ring=1)
