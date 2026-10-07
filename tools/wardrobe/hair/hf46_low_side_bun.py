"""Low Side Bun: side-parted and swept across the back into a bun low behind the left ear, a long fringe falling to the cheek."""
from anime import ring_shell
from anime_female import aim, bun, fall, pointed, strand
from paint import scalp

META = {"name": "Low Side Bun", "gender": "female",
        "description": "A deep side part, hair swept across into a low bun behind one ear, and a long fringe to the cheek."}


def build(g):
    scalp(g, 9601, side_rows=8, back_rows=8, sideburn=0, part=5)
    head = g.part("head")
    for y in range(4, 7):   # the far side is swept back, showing the ear
        for x in range(1, 5):
            head.left.set(x, y, None)
    hat = ring_shell(g, 9602, side_rows=4, back_rows=6)
    hat.top.vline(5, 0, 7, "H1")
    strand(g, "sweep_0", (2.8, -8.7, -4.35), (-6, 0, 74), ((2, 5), (1, 1)), 1, 9610, ring=None)
    strand(g, "sweep_1", (1.2, -8.65, -4.35), (-6, 0, 64), ((2, 4), (1, 1)), 1, 9611, ring=None)
    pointed(g, "cheek_fall", (-4.3, -7.6, -3.5), (0, 0, 4), 2, 8, 2, seed=9612)
    strand(g, "right_side", (-4.45, -7.8, .8), (-12, 0, 4), ((1, 6),), 5, 9615)
    strand(g, "left_side", (4.45, -7.8, .6), (0, 0, -3), ((1, 4),), 5, 9616)
    # Everything at the back sweeps toward the bun.
    fall(g, "sweep_back", [(-2.8, -7.6, 4.4, ((3, 7), (2, 2)), 0, -40), (-.4, -6.2, 4.6, ((3, 5), (2, 2)), 0, -50),
                           (1.8, -7.4, 4.35, ((3, 4),), 0, -26), (-1.6, -3.6, 4.5, ((2, 4),), 0, -70)], 9620)
    rx, rz = aim((-.62, -.15, -.77))   # the bun's outer face looks back and to the left
    bun(g, "side_bun", (3.4, -2.6, 4.2), (rx, 0, rz), (4, 2, 4), seed=9640)
