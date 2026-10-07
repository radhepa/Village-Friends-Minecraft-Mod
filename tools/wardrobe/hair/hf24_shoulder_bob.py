"""Shoulder Bob: a straight side-parted bob brushing the shoulders, its ends turned under, with a swept fringe."""
from anime import ring_shell
from anime_female import curve, strand, SIDES
from paint import scalp

META = {"name": "Shoulder Bob", "gender": "female",
        "description": "A straight side-parted bob to the shoulders with ends turned under and a swept fringe."}


def build(g):
    scalp(g, 7401, side_rows=8, back_rows=8, sideburn=0, part=5)
    hat = ring_shell(g, 7402, side_rows=7, back_rows=8)
    hat.top.vline(5, 0, 7, "H1")
    for i, (x, length, rz) in enumerate(((2.8, 6, 74), (1.2, 5, 64), (-.6, 4, 52))):
        strand(g, f"sweep_{i}", (x, -8.65, -4.35), (-6, 0, rz), ((2, length - 1), (1, 1)), 1, 7410 + i * 3, ring=None)
    for side, sign in SIDES:
        # Front and rear side locks, a little longer at the front, each ending in an inward turn.
        curve(g, f"{side}_front", (4.35 * sign, -7.7, -3.0), ((2, 7, 0, -4 * sign), (2, 2, -10, 30 * sign)), seed=7420 + (sign > 0))
        curve(g, f"{side}_mid", (4.45 * sign, -7.8, -.4), ((1, 7, 0, -5 * sign, 4), (1, 2, 0, 30 * sign, 4)), seed=7424 + (sign > 0))
    for i, (x, z, rz) in enumerate(((-3.2, 4.3, 5), (-1.1, 4.65, 2), (1.1, 4.3, -2), (3.2, 4.65, -5))):
        curve(g, f"back_{i}", (x, -7.8, z), ((3, 7, 3, rz), (3, 2, -38, rz)), seed=7430 + i * 3)
