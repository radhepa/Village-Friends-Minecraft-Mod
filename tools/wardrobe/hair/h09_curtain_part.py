"""Curtain Part: a centre part with curtain bangs sweeping to each temple, jaw-length layered sides."""
from paint import hair_box, scalp, shell

META = {"name": "Curtain Part", "gender": "male", "description": "Centre-parted curtain bangs, jaw-length layered sides and a soft nape."}


def build(g):
    scalp(g, 801, side_rows=6, back_rows=8, sideburn=1, part=3)
    shell(g, 802, side_rows=5, back_rows=7, front=[(0, 1), (0, 2), (0, 3), (0, 4), (7, 1), (7, 2), (7, 3), (7, 4),
                                                       (1, 1), (2, 1), (5, 1), (6, 1)])
    hat = g.part("hat")
    hat.top.vline(3, 0, 7, "H1"), hat.top.vline(4, 0, 7, "H1")
    for side, sign in (("right", -1), ("left", 1)):
        swoop = g.piece(f"{side}_curtain", "HEAD", (0 if sign > 0 else -3.4, 0, -1), (3, 2, 1),
                        pivot=(.15 * sign, -8.7, -4.25), rotation=(-8, 0, 16 * sign))
        hair_box(swoop, 810 + (sign > 0), 2, sheen_row=0)
        strand = g.piece(f"{side}_jaw_strand", "HEAD", (-.5, 0, -1), (1, 6, 2), pivot=(4.25 * sign, -7.6, -2.9), rotation=(0, 0, -3 * sign))
        hair_box(strand, 815 + (sign > 0), 2, sheen_row=1)
        for j, (z, length) in enumerate(((-.4, 6), (1.8, 5))):
            lock = g.piece(f"{side}_side_{j}", "HEAD", (-.5, 0, -1), (1, length, 2), pivot=(4.2 * sign, -7.8, z), rotation=(0, 0, -(4 + 2 * j) * sign))
            hair_box(lock, 820 + j + (sign > 0) * 3, 2, sheen_row=1)
        crown = g.piece(f"crown_{side}", "HEAD", (-2, -1, -3.5), (4, 1, 7), pivot=(2.2 * sign, -8.15, .2), rotation=(0, 0, 9 * sign))
        hair_box(crown, 830 + (sign > 0), 2, top_delta=1)
    for i, (x, length, rz) in enumerate(((-3.0, 6, 5), (0, 7, 0), (3.0, 6, -5))):
        lock = g.piece(f"nape_{i}", "HEAD", (-1.5, 0, 0), (3, length, 1), pivot=(x, -7.6, 4.15), rotation=(4, 0, rz))
        hair_box(lock, 840 + i, 2, sheen_row=2)
