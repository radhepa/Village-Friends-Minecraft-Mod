"""High Twin Tails: two long tails tied high on the crown with ribbon bows, arcing out and falling to the waist."""
from anime import ring_shell
from anime_female import bow, curve, fall, pointed, points, SIDES
from paint import scalp

META = {"name": "High Twin Tails", "gender": "female",
        "description": "Two long tails tied high with ribbon bows, swinging out and down to the waist."}


def build(g):
    scalp(g, 6201, side_rows=6, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 6202, side_rows=5, back_rows=7)
    hat.top.vline(3, 0, 7, "H1")
    points(g, "bang", [(-2.6, 3, 2, 2, 12), (-.4, 3, 2, 2, 2), (1.8, 3, 2, 2, -10)], 6210)
    for side, sign in SIDES:
        pointed(g, f"{side}_sidelock", (4.3 * sign, -7.6, -3.4), (0, 0, -4 * sign), 2, 5, 2, seed=6220 + (sign > 0))
        curve(g, f"{side}_tail", (3.9 * sign, -8.9, 2.6),
              ((3, 3, 14, -72 * sign, 3), (3, 4, 10, -34 * sign, 2), (3, 4, 6, -10 * sign, 2), (2, 4, 3, -3 * sign, 2),
               (2, 3, 0, 0, 2), (1, 2, 0, 0, 1)), seed=6230 + (sign > 0) * 9, motion="sway")
        bow(g, f"{side}_bow", (4.3 * sign, -9.4, 2.2), facing="side", loop=(2, 2), spread=24)
    fall(g, "nape", [(-2.0, -7.4, 4.4, ((3, 6), (2, 2)), 4, 6), (0.2, -7.5, 4.6, ((3, 7), (1, 2)), 4, 0),
                     (2.2, -7.4, 4.4, ((3, 6), (2, 2)), 4, -6)], 6260)
