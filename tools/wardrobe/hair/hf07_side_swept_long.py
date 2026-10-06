"""Side-Swept Long: a deep left part, the fringe swept across into long locks draped over the right shoulder."""
from anime import ring_shell
from anime_female import fall, strand
from paint import scalp

META = {"name": "Side-Swept Long", "gender": "female",
        "description": "Deep-parted long hair swept across the brow and draped forward over one shoulder."}


def build(g):
    scalp(g, 5701, side_rows=7, back_rows=8, sideburn=0, part=5)
    head = g.part("head")
    for y in range(4, 7):   # the left side is tucked behind the ear
        for x in range(1, 6):
            head.left.set(x, y, None)
    hat = ring_shell(g, 5702, side_rows=7, back_rows=8)
    for y in range(3, 7):
        for x in range(0, 6):
            hat.left.set(x, y, None)
    hat.top.vline(5, 0, 7, "H1")
    for i, (x, length, rz) in enumerate(((2.8, 6, 76), (1.2, 5, 66), (3.7, 4, 60))):
        strand(g, f"sweep_{i}", (x, -8.75, -4.35), (-6, 0, rz), ((2, length - 1), (1, 1)), 1, 5710 + i * 7, ring=None)
    # Everything gathers on the wearer's right and falls forward over that shoulder.
    strand(g, "drape_0", (-4.35, -7.5, -3.6), (0, 0, 5), ((2, 6), (2, 4), (2, 3), (1, 2)), 1, 5730)
    strand(g, "drape_1", (-4.6, -7.6, -2.9), (0, 0, 9), ((3, 7), (2, 5), (1, 3)), 1, 5735, motion="sway")
    strand(g, "right_side", (-4.45, -7.8, 1.0), (0, 0, 5), ((1, 8),), 5, 5740)
    strand(g, "left_tuck", (4.3, -7.8, .2), (0, 0, -2), ((1, 3),), 4, 5741, ring=0)
    strand(g, "left_behind_ear", (4.25, -7.2, 2.2), (14, 0, -4), ((2, 6), (1, 3)), 1, 5742, motion="sway")
    fall(g, "back", [(-3.2, -7.6, 4.3, ((3, 11), (2, 3), (1, 2)), 4, 12),
                     (-1.2, -7.7, 4.7, ((3, 12), (2, 3), (1, 2)), 5, 9),
                     (.9, -7.6, 4.3, ((3, 12), (2, 2), (1, 2)), 4, 7),
                     (2.9, -7.6, 4.7, ((3, 10), (2, 2), (1, 2)), 5, 5)], 5750, motion="sway")
