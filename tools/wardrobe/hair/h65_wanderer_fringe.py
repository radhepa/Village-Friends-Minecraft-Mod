"""Wanderer's Fringe: a ragged, uneven fringe falling forward to the brows and long cheek locks that
curve in around the face, the crown kept flat and close so a hood sits over it."""
from anime import ring_shell
from anime_male import SIDES, chain, taper
from paint import scalp

META = {"name": "Wanderer's Fringe", "gender": "male",
        "description": "A ragged fringe to the brows and long cheek locks curving round the face, flat beneath a hood."}

# The fringe: (x, length, lean); the middle points stay above the brows, the outer ones fall longer.
FRINGE = [(-3.4, 3, 10), (-1.8, 2, 4), (-.4, 3, -2), (1.1, 2, -6), (2.6, 3, -10)]


def build(g):
    scalp(g, 6501, side_rows=7, back_rows=8, sideburn=1)
    ring_shell(g, 6502, side_rows=6, back_rows=8)
    for i, (x, length, rz) in enumerate(FRINGE):
        taper(g, f"fringe_{i}", (x, -8.6, -4.3), (-18, 0, rz), ((2, length - (1 if abs(x) < 3 else 0), 1), (1, 1, 1)),
              seed=6510 + i * 3, ring=0)
    # Cheek locks curving in toward the jaw from outside the cheeks.
    for side, sign in SIDES:
        chain(g, f"{side}_cheek", (4.45 * sign, -7.8, -3.4), [(2, 5, 1, (-4, 0, -2 * sign)), (2, 3, 1, (-26, 0, 6 * sign)),
                                                            (1, 2, 1, (-40, 0, 10 * sign))], seed=6530 + (sign > 0) * 11, ring=1)
        for j, (z, length) in enumerate(((-.8, 6), (2.0, 5))):
            taper(g, f"{side}_layer_{j}", (4.45 * sign, -7.6, z), ((j - 1) * 6, 0, -(5 + j * 4) * sign), ((2, length, 2), (1, 2, 1)),
                  seed=6550 + j * 3 + (sign > 0) * 7, ring=1)
    # A ragged back, collar-length.
    for i, (x, length, rz) in enumerate(((-3.0, 6, 10), (-1.0, 7, 2), (1.0, 6, -4), (3.0, 7, -10))):
        taper(g, f"back_{i}", (x, -7.4, 4.45), (8, 0, rz), ((2, length, 1), (1, 2, 1)), seed=6570 + i * 3, ring=1)
