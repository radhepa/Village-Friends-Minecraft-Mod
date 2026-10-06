"""Shoulder Braid: long hair swept over to the wearer's left and plaited into one thick braid that
falls in front of the shoulder, a side-swept fringe above the brow."""
from anime import ring_shell
from anime_male import clump, combed_face, plait, plate, taper
from paint import scalp

META = {"name": "Shoulder Braid", "gender": "male",
        "description": "Long hair swept to one side into a thick braid falling in front of the shoulder."}


def build(g):
    scalp(g, 5801, side_rows=6, back_rows=8, sideburn=1, part=2)
    hat = ring_shell(g, 5802, side_rows=5, back_rows=8)
    combed_face(hat.top, 5803, 3, across_y=True)
    # A fringe swept across toward the braid side.
    for i, (x, rz) in enumerate(((-2.6, -48), (-.4, -56))):
        taper(g, f"fringe_{i}", (x, -8.7, -4.3), (-6, 0, rz), ((2, 3, 1), (1, 1, 1)), seed=5810 + i * 3, ring=0)
    # Everything swept over the crown and round the back toward the left.
    for i, (z, w) in enumerate(((-1.6, 3), (1.2, 3))):
        plate(g, f"sweep_{i}", (-1.6, -8.3 - i * .12, z), (7, 1, w), origin=(-1, -1, -w / 2), rotation=(0, 0, 6),
              seed=5820 + i, sheen=3, across=True)
    right = clump(g, "right_side", (-4.45, -8.0, .8), (1, 4, 6), rotation=(10, 0, 3), seed=5825)
    combed_face(right.right, 5826, 2, across_y=True)
    for i, (x, rz) in enumerate(((-2.0, -16), (1.0, -24))):
        back = clump(g, f"back_{i}", (x, -8.3, 4.4), (3, 6, 1), rotation=(4, 0, rz), seed=5830 + i)
        combed_face(back.back, 5832 + i, 2, sheen=1)
    gather = clump(g, "gather", (4.5, -7.6, -.2), (2, 4, 4), origin=(-1, 0, -2), rotation=(-16, 0, -4), seed=5840, ring=1)
    combed_face(gather.left, 5841, 2, sheen=1, across_y=True)
    # The braid, falling in front of the shoulder.
    plait(g, "braid", (4.6, -4.4, -3.0), 8, rotation=(-6, 0, -4), width=2, depth=2, seed=5850, tie_role="A", tuft=2, motion="sway")
