"""Asymmetric Bob: cut to the jaw on one side and past the collarbone on the other, with a deep fringe swept across."""
from anime import ring_shell
from anime_female import fall, pointed, strand
from paint import scalp

META = {"name": "Asymmetric Bob", "gender": "female",
        "description": "Jaw-length on one side, past the collarbone on the other, with a deep fringe swept across."}


def build(g):
    scalp(g, 10001, side_rows=8, back_rows=8, sideburn=0, part=2)
    hat = ring_shell(g, 10002, side_rows=6, back_rows=8)
    hat.top.vline(2, 0, 7, "H1")
    # A deep fringe from the part on the wearer's right, sweeping over toward the long side.
    for i, (x, length, rz) in enumerate(((-2.8, 6, -74), (-1.2, 5, -64), (.6, 4, -52))):
        strand(g, f"sweep_{i}", (x, -8.7, -4.35), (-6, 0, rz), ((2, length - 1), (1, 1)), 1, 10010 + i * 3, ring=None)
    # Short side: crisp points at the jaw.
    pointed(g, "short_front", (-4.35, -7.6, -3.2), (0, 0, 4), 2, 5, 2, seed=10020)
    pointed(g, "short_side", (-4.5, -7.8, -.2), (0, 0, 6), 2, 5, 2, seed=10022)
    strand(g, "short_cover", (-4.45, -7.8, 1.6), (0, 0, 4), ((1, 5),), 4, 10024)
    # Long side: falls past the collarbone in front, and behind the shoulder.
    pointed(g, "long_front", (4.35, -7.4, -3.2), (0, 0, -3), 2, 12, 2, seed=10030)
    strand(g, "long_mid", (4.5, -7.8, -.4), (0, 0, -3), ((2, 7), (1, 1)), 2, 10032)
    strand(g, "long_rear", (4.2, -7.6, 3.0), (2, 0, -4), ((2, 10), (2, 2), (1, 2)), 1, 10034, motion="sway")
    # The back steps down from the short side to the long side.
    fall(g, "back", [(-3.0, -7.6, 4.35, ((3, 5), (2, 2)), 2, 6), (-1.0, -7.7, 4.7, ((3, 7), (2, 2)), 0, 3),
                     (1.0, -7.6, 4.35, ((3, 9), (2, 2), (1, 1)), -2, 0), (3.0, -7.7, 4.7, ((3, 11), (2, 2), (1, 2)), -3, -3)],
         10040, motion="sway")
