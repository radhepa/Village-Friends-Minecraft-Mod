"""Pillow Bedhead: slept-on hair, pressed flat on one side and sticking out on the other, with a
cowlick at the crown and a fringe pointing every which way."""
from anime import ring_shell
from anime_male import clump, combed_face, taper
from paint import scalp

META = {"name": "Pillow Bedhead", "gender": "male",
        "description": "Slept-on hair, flattened on one side and sticking out on the other, with a crown cowlick."}


def build(g):
    scalp(g, 3501, side_rows=5, back_rows=8, sideburn=1)
    ring_shell(g, 3502, side_rows=4, back_rows=7)
    # Pressed flat on the wearer's right, strands dragged back by the pillow.
    flat = clump(g, "pressed_side", (-4.45, -8.3, .4), (1, 4, 7), rotation=(0, 0, 3), seed=3510)
    combed_face(flat.right, 3511, 2, sheen=1, across_y=True)
    combed_face(flat.left, 3512, 2, across_y=True)
    # Sticking straight out on the wearer's left.
    for i, (y, z, rz, rx) in enumerate(((-7.7, -2.2, -64, -10), (-7.0, .4, -100, 0), (-7.4, 2.8, -78, 14))):
        taper(g, f"stuck_out_{i}", (4.1, y, z), (rx, 0, rz), ((3, 2, 2), (2, 1, 1), (1, 1, 1)), seed=3520 + i * 3, ring=0)
    # The cowlick at the back of the crown.
    taper(g, "cowlick_0", (.6, -8.3, 2.0), (-38, 0, -14), ((2, 2, 2), (1, 2, 1)), seed=3530, ring=0, up=True)
    taper(g, "cowlick_1", (-1.0, -8.3, 2.9), (-54, 0, 26), ((2, 2, 1), (1, 1, 1)), seed=3533, ring=None, up=True)
    for i, (x, z, rx, rz) in enumerate(((-2.0, -1.8, 14, 20), (1.6, -2.2, -10, -12), (2.4, .8, 12, -24))):
        clump(g, f"tuft_{i}", (x, -8.35, z), (3, 1, 3), rotation=(rx, 0, rz), origin=(-1.5, -1, -1.5), seed=3540 + i, top_delta=2)
    # A fringe pointing every which way, all of it above the brows.
    for i, (x, rz) in enumerate(((-2.6, 28), (-.4, -6), (1.8, -34))):
        taper(g, f"fringe_{i}", (x, -8.5, -4.35), (-14, 0, rz), ((2, 2, 1), (1, 1, 1)), seed=3550 + i * 3, ring=0)
    taper(g, "fringe_3", (4.2, -8.2, -3.9), (0, 0, -18), ((1, 3, 1), (1, 1, 1)), seed=3559, ring=0)
    for i, (x, y, rx, rz) in enumerate(((2.2, -6.0, 70, -20), (-.6, -5.2, 64, 10))):
        taper(g, f"back_tuft_{i}", (x, y, 4.3), (rx, 0, rz), ((2, 2, 1), (1, 1, 1)), seed=3560 + i * 3, ring=None)
