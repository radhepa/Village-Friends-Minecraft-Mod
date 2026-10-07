"""Rose Braid Half-Up: two thin braids from the temples meet at the back in a small braided rosette; the rest falls long."""
from anime import ring_shell
from anime_female import braided_bun, fall, plait_along, points, SIDES
from paint import scalp

META = {"name": "Rose Braid Half-Up", "gender": "female",
        "description": "Two thin braids from the temples meeting in a braided rosette at the back, the rest long and wavy."}


def build(g):
    scalp(g, 9801, side_rows=7, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 9802, side_rows=7, back_rows=8)
    hat.top.vline(3, 0, 7, "H1")
    points(g, "bang", [(-2.6, 3, 2, 2, 12), (-.4, 3, 2, 2, 2), (1.8, 3, 2, 2, -8)], 9810)
    for side, sign in SIDES:
        plait_along(g, f"{side}_braid", [(4.75 * sign, -7.0, -2.8), (5.05 * sign, -6.5, 0), (4.4 * sign, -6.0, 3.0), (1.6 * sign, -5.7, 5.0)],
                    w=2, d=1, h=2, spacing=1.9, seed=9820 + (sign > 0) * 10, shift=.2)
    braided_bun(g, "rosette", (0, -5.7, 5.2), (-90, 0, 0), (3, 1, 3), seed=9840)
    fall(g, "back", [(-3.2, -7.6, 4.3, ((3, 6), (3, 5, .6), (2, 3, -.3), (1, 2)), -2, 4),
                     (-1.0, -5.0, 4.6, ((3, 6), (2, 5, -.5), (2, 3, .3), (1, 2)), -3, 1),
                     (1.1, -5.0, 4.3, ((3, 6), (3, 5, .5), (2, 3, -.3), (1, 2)), -3, -1),
                     (3.2, -7.6, 4.6, ((3, 6), (2, 4, -.6), (1, 3)), -2, -4)], 9850, motion="sway", texture="wave")
