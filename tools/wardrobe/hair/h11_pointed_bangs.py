"""Pointed Bangs: a fringe of tapered points over the brow, a lightly spiked crown and a pointed nape."""
from anime import back_fan, bangs, ring_shell, spike
from paint import scalp

META = {"name": "Pointed Bangs", "gender": "male", "description": "Anime-style fringe of tapered points, a lifted crown and a pointed nape."}


def build(g):
    scalp(g, 1101, side_rows=5, back_rows=8, sideburn=2)
    ring_shell(g, 1102, side_rows=4, back_rows=7)
    bangs(g, "bang", [(-4.1, ((2, 3), (1, 2)), 6), (-2.2, ((3, 2), (1, 1)), 10), (0.0, ((3, 2), (1, 1)), 0),
                      (2.2, ((3, 2), (1, 1)), -10), (4.1, ((2, 3), (1, 2)), -6)], 1110)
    for i, (x, z) in enumerate(((-2.4, -.4), (0, -1.0), (2.4, -.4), (-1.4, 2.2), (1.4, 2.2))):
        spike(g, f"crown_{i}", (x, -8.1, z), (-(z + 1) * 9, 0, x * 7), ((3, 1), (2, 1), (1, 1)), 2, 1130 + i * 3)
    back_fan(g, "nape", [(-3.0, ((2, 4), (1, 2)), 10, 10), (-1.0, ((3, 5), (1, 2)), 3, 8), (1.0, ((3, 5), (1, 2)), -3, 8),
                         (3.0, ((2, 4), (1, 2)), -10, 10)], 1150)
