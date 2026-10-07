"""Scrunchie High Ponytail: pulled up to a ruffled scrunchie at the crown, a full tail arcing back with two side strands."""
from anime import cel_box, ring_shell
from anime_female import combed, curve, pointed, points, swept_sides, SIDES
from paint import k, scalp, solid

META = {"name": "Scrunchie High Ponytail", "gender": "female",
        "description": "A full high ponytail in a ruffled scrunchie, arcing back as it falls, with pointed bangs."}


def build(g):
    scalp(g, 5901, side_rows=8, back_rows=8, sideburn=0)
    swept_sides(g)
    head = g.part("head")
    combed(head.back, (1, 3, 4, 6))
    hat = ring_shell(g, 5902, side_rows=2, back_rows=5)
    combed(hat.back, (2, 5), rows=range(1, 5))
    points(g, "bang", [(-2.6, 3, 2, 2, 10), (-.4, 3, 2, 2, 0), (1.8, 3, 2, 2, -8)], 5910)
    for side, sign in SIDES:
        pointed(g, f"{side}_sidelock", (4.3 * sign, -7.6, -3.4), (0, 0, -2 * sign), 2, 6, 2, seed=5920 + (sign > 0))
    root = g.piece("tail_root", "HEAD", (-1.5, -2, -1.5), (3, 2, 3), pivot=(0, -8.2, 2.6), rotation=(-30, 0, 0))
    cel_box(root, 5930)
    scrunchie = g.piece("scrunchie", "HEAD", (-1.5, -1, -1.5), (3, 1, 3), pivot=(0, -9.7, 3.4), rotation=(-30, 0, 0), inflate=.28)
    solid(scrunchie, "A", "plain", 5931, 2, edge=False)
    for f in scrunchie.sides:
        for x in range(f.w):
            f.set(x, 0, k("A", 3 if x % 2 == 0 else 1))
    pivot = (0, -9.9, 3.9)
    curve(g, "tail", pivot, ((3, 3, 50, 0, 2), (3, 4, 20, 0, 2), (3, 4, 6, 0, 2), (2, 4, 0, 0, 2), (1, 3, -4, 0, 1)), seed=5940,
          motion="sway")
    for side, sign in SIDES:
        curve(g, f"tail_{side}", pivot, ((2, 3, 55, -14 * sign), (2, 5, 22, -9 * sign), (1, 3, 8, -5 * sign)), seed=5950 + (sign > 0),
              motion="sway", ring=None)
