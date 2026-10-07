"""Half-Up Ribbon: the top half drawn back to a ribbon bow with trailing tails, the rest falling long and loose."""
from anime import ring_shell
from anime_female import bow, fall, pointed, points, strand, SIDES
from paint import scalp

META = {"name": "Half-Up Ribbon", "gender": "female",
        "description": "The top half tied back with a ribbon bow and trailing tails, the rest long and loose."}


def build(g):
    scalp(g, 7301, side_rows=7, back_rows=8, sideburn=0)
    hat = ring_shell(g, 7302, side_rows=7, back_rows=8)
    points(g, "bang", [(-2.7, 3, 2, 2, 8), (-.5, 3, 2, 2, 0), (1.7, 3, 2, 2, -6), (3.6, 2, 2, 2, -12)], 7310)
    for side, sign in SIDES:
        pointed(g, f"{side}_sidelock", (4.3 * sign, -7.6, -3.3), (0, 0, -3 * sign), 2, 9, 2, seed=7320 + (sign > 0))
        # Locks drawn back from the temples toward the bow.
        strand(g, f"{side}_drawn", (4.5 * sign, -7.0, -1.6), (78, 0, 10 * sign), ((2, 6), (2, 1)), 1, 7325 + (sign > 0), ring=0)
    strand(g, "gathered", (0, -6.2, 5.0), (8, 0, 0), ((3, 4), (2, 2), (1, 1)), 1, 7330, motion="sway")
    bow(g, "ribbon", (0, -6.4, 5.25), facing="back", loop=(3, 2), spread=18, tails=2, tail_len=5)
    fall(g, "back", [(-3.3, -7.6, 4.3, ((3, 11), (2, 2), (1, 2)), -2, 4), (-1.1, -7.0, 4.6, ((3, 12), (2, 2), (1, 2)), -3, 1),
                     (1.1, -7.0, 4.3, ((3, 12), (2, 3), (1, 2)), -3, -1), (3.3, -7.6, 4.6, ((3, 10), (2, 2), (1, 2)), -2, -4)],
         7340, motion="sway")
