"""Bound Hime Sidelocks: see-through blunt bangs, long sidelocks bound with ribbon cuffs, a blunt shoulder-blade back."""
from anime import cel_box, ring_shell
from anime_female import SIDES, strand, tie
from paint import scalp

META = {"name": "Bound Hime Sidelocks", "gender": "female",
        "description": "Blunt see-through bangs and long sidelocks bound near the tips with ribbon cuffs."}


def build(g):
    scalp(g, 5601, side_rows=7, back_rows=8, sideburn=0)
    ring_shell(g, 5602, side_rows=7, back_rows=8)
    # See-through bangs: five blunt locks with a hair's gap between them.
    for i, x in enumerate((-3.4, -1.7, 0, 1.7, 3.4)):
        lock = g.piece(f"fringe_{i}", "HEAD", (-1, 0, -.5), (2, 3 if i % 2 == 0 else 2, 1), pivot=(x, -8.6, -4.3 - .08 * (i % 2)),
                       rotation=(-6, 0, 0))
        cel_box(lock, 5610 + i, ring=0)
    for side, sign in SIDES:
        pivot = (4.25 * sign, -7.6, -3.4)
        strand(g, f"{side}_sidelock", pivot, (0, 0, -2 * sign), ((2, 9),), 1, 5620 + (sign > 0))
        tie(g, f"{side}_cuff", pivot, (0, 0, -2 * sign), (2, 2, 1), y=8.2, inflate=.14)
        strand(g, f"{side}_tip", pivot, (0, 0, -2 * sign), ((2, 2), (1, 2)), 1, 5624 + (sign > 0), ring=None, start=10.2)
        curtain = g.piece(f"{side}_curtain", "HEAD", (-.5, 0, -2.5), (1, 7, 5), pivot=(4.4 * sign, -7.8, 1.1), rotation=(0, 0, -3 * sign))
        cel_box(curtain, 5628 + (sign > 0), ring=1)
    for i, (x, length, z, rx, rz) in enumerate(((-3.3, 9, 4.3, 3, 6), (-1.1, 12, 4.8, 1, 2), (1.1, 11, 4.3, 2, -1.5),
                                                (3.3, 8, 4.8, 4, -6))):
        panel = g.piece(f"back_{i}", "HEAD", (-1.5, 0, -.5), (3, length, 1), pivot=(x, -7.8, z), rotation=(rx, 0, rz), motion="sway")
        cel_box(panel, 5640 + i, ring=1)
