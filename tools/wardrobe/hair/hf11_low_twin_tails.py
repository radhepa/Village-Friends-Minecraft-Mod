"""Low Twin Tails: centre-parted and tied low behind each ear, the tails brought forward over the shoulders."""
from anime import ring_shell
from anime_female import curve, fall, link, points, strand, SIDES
from paint import k, scalp, solid

META = {"name": "Low Twin Tails", "gender": "female",
        "description": "Two soft tails tied low behind the ears and worn forward over the shoulders."}


def build(g):
    scalp(g, 6101, side_rows=7, back_rows=8, sideburn=0, part=3)
    head = g.part("head")
    head.back.vline(3, 0, 7, "H0"), head.back.vline(4, 0, 7, "H1")   # parted down the back to each tail
    hat = ring_shell(g, 6102, side_rows=6, back_rows=7)
    hat.top.vline(3, 0, 7, "H1"), hat.back.vline(3, 0, 6, "H1")
    points(g, "bang", [(-1.7, 3, 2, 2, 16), (1.5, 3, 2, 2, -16), (-4.2, 2, 2, 2, 6), (4.2, 2, 2, 2, -6)], 6110)
    for side, sign in SIDES:
        strand(g, f"{side}_side", (4.45 * sign, -7.8, .9), (0, 0, -3 * sign), ((1, 6),), 5, 6120 + (sign > 0))
        pivot = (4.6 * sign, -2.6, 2.0)
        _, _, rot = curve(g, f"{side}_tail", pivot, ((3, 3, -72, -8 * sign, 2), (3, 3, -62, -6 * sign, 2), (3, 4, -24, 0, 2),
                                                      (2, 4, -8, 3 * sign, 2), (1, 2, -4, 3 * sign, 1)),
                          seed=6130 + (sign > 0) * 9, motion="sway")
        band = link(g, f"{side}_tie", pivot, pivot, (-72, 0, -8 * sign), (3, 1, 2), "sway", inflate=.14)
        solid(band, "A", "plain", 0, 2, edge=False)
        for f in band.sides:
            f.hline(0, f.w - 1, 0, k("A", 3))
    fall(g, "nape", [(-1.9, -7.5, 4.4, ((3, 5), (2, 1)), 2, 22), (1.9, -7.5, 4.4, ((3, 5), (2, 1)), 2, -22)], 6150)
