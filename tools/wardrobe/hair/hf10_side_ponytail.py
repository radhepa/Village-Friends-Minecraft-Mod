"""Side Ponytail: swept across the back to a bow below the left ear, the tail falling forward over the shoulder."""
from anime import ring_shell
from anime_female import bow, curve, fall, pointed, points, strand
from paint import scalp

META = {"name": "Side Ponytail", "gender": "female",
        "description": "Hair swept to one side into a bow-tied ponytail that falls forward over the shoulder."}


def build(g):
    scalp(g, 6001, side_rows=6, back_rows=8, sideburn=0, part=2)
    hat = ring_shell(g, 6002, side_rows=5, back_rows=7)
    hat.top.vline(2, 0, 7, "H1")
    points(g, "bang", [(-2.8, 3, 2, 2, -14), (-.6, 3, 2, 2, -20), (1.6, 2, 2, 2, -24)], 6010)
    pointed(g, "right_temple", (-4.3, -7.6, -3.4), (0, 0, 4), 2, 6, 2, seed=6020)
    strand(g, "right_side", (-4.45, -7.8, .8), (-8, 0, 6), ((1, 6),), 5, 6021)
    # The back is combed across toward the tie behind the left ear.
    fall(g, "sweep", [(-2.6, -7.6, 4.4, ((3, 6), (2, 2)), 0, -42), (-.2, -6.4, 4.55, ((3, 5), (2, 2)), 0, -48),
                      (1.6, -7.4, 4.35, ((2, 4),), 0, -30)], 6030)
    strand(g, "left_side", (4.4, -7.8, .2), (0, 0, -4), ((1, 4),), 4, 6034)
    bow(g, "bow", (5.15, -4.9, .4), facing="side", loop=(2, 2), spread=28)
    curve(g, "tail", (4.7, -4.6, 0.0), ((3, 3, -30, -25, 2), (3, 4, -35, -6, 2), (3, 4, -15, 0, 2), (2, 4, -5, 4, 2), (1, 2, -3, 4, 1)),
          seed=6040, motion="sway")
