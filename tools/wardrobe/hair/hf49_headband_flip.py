"""Headband Flip: shoulder-length hair held off the face by a cloth headband, the ends flipped up and out."""
from anime import cel_box, ring_shell
from anime_female import curve, strand, SIDES
from paint import k, scalp, solid

META = {"name": "Headband Flip", "gender": "female",
        "description": "Shoulder-length hair held back by a cloth headband, the ends flipped up and outward."}


def build(g):
    scalp(g, 9901, side_rows=8, back_rows=8, sideburn=0)
    ring_shell(g, 9902, side_rows=7, back_rows=8)
    front = g.piece("smooth_front", "HEAD", (-4, -1, -1.5), (8, 1, 3), pivot=(0, -8.45, -2.9), rotation=(10, 0, 0))
    cel_box(front, 9905, ring=None, top_delta=1, clump=4)
    band = g.piece("band_top", "HEAD", (-4.5, -1, -1), (9, 1, 2), pivot=(0, -8.65, -1.4), inflate=.1)
    solid(band, "A", "plain", 9910, 2, edge=False)
    for f in band.sides:
        f.hline(0, f.w - 1, 0, k("A", 3))
    for side, sign in SIDES:
        drop = g.piece(f"{side}_band", "HEAD", (-.5, 0, -1), (1, 4, 2), pivot=(4.65 * sign, -8.7, -1.4), inflate=.1)
        solid(drop, "A", "plain", 9911, 2, edge=False)
        strand(g, f"{side}_temple", (4.3 * sign, -7.0, -3.4), (0, 0, -4 * sign), ((1, 4), (1, 2)), 1, 9915 + (sign > 0), ring=None)
        # Side locks fall straight, then flip up and out at the shoulder.
        for j, (z, n) in enumerate(((-2.6, 6), (.6, 6))):
            curve(g, f"{side}_flip_{j}", (4.45 * sign, -7.6, z), ((2, n, 0, -3 * sign), (2, 2, 0, -50 * sign), (1, 1, 0, -80 * sign)),
                  seed=9920 + j * 5 + (sign > 0), motion="sway" if j else "none")
    for i, (x, z, rz) in enumerate(((-3.0, 4.35, 4), (-1.0, 4.7, 1), (1.0, 4.35, -1), (3.0, 4.7, -4))):
        curve(g, f"back_flip_{i}", (x, -7.8, z), ((3, 7, -2, rz), (3, 2, 45, rz * 4), (2, 1, 70, rz * 6)), seed=9940 + i * 3,
              motion="sway")
