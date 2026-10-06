"""Very Long Straight: sleek hair past the waist in staggered locks, pointed bangs and chest-length sidelocks."""
from anime import ring_shell
from anime_female import fall, points, pointed, strand, SIDES
from paint import scalp

META = {"name": "Very Long Straight", "gender": "female",
        "description": "Sleek straight hair falling past the waist, pointed bangs and long face-framing sidelocks."}


def build(g):
    scalp(g, 5101, side_rows=7, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 5102, side_rows=7, back_rows=8)
    hat.top.vline(3, 0, 7, "H1")
    points(g, "bang", [(-2.7, 3, 2, 2, 8), (-.5, 3, 2, 2, 2), (1.7, 3, 2, 2, -6), (3.6, 2, 2, 2, -10)], 5110)
    for side, sign in SIDES:
        pointed(g, f"{side}_sidelock", (4.3 * sign, -7.6, -3.3), (0, 0, -3 * sign), 2, 12, 2, seed=5120 + (sign > 0))
        strand(g, f"{side}_side", (4.4 * sign, -7.8, .8), (0, 0, -3 * sign), ((1, 8),), 4, 5125 + (sign > 0))
    # Long under-layer in a soft V, then a shorter top layer: the back reads as locks, not one slab.
    fall(g, "under", [(-3.5, -7.6, 4.3, ((2, 15), (2, 2), (1, 2)), -3, 4),
                      (-1.8, -7.7, 4.6, ((3, 17), (2, 2), (1, 2)), -4, 2),
                      (0.1, -7.6, 4.3, ((3, 18), (2, 2), (1, 2)), -4, -1),
                      (2.0, -7.7, 4.6, ((3, 16), (2, 3), (1, 2)), -4, -2),
                      (3.6, -7.6, 4.3, ((2, 14), (2, 2), (1, 2)), -3, -5)], 5130, motion="sway", texture="sleek")
    fall(g, "over", [(-1.7, -7.4, 5.0, ((3, 8), (1, 2)), 2, 5), (1.6, -7.4, 5.05, ((3, 9), (1, 2)), 2, -4)], 5160,
         motion="sway", texture="sleek")
