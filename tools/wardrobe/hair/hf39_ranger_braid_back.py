"""Ranger Braid-Back: a thick braid along the top of the head from the hairline, carrying on as a plait down the back;
the sides are drawn up tight and out of the way."""
from anime import ring_shell
from anime_female import braid, combed, plait_along, strand, swept_sides, SIDES
from paint import scalp

META = {"name": "Ranger Braid-Back", "gender": "female",
        "description": "A thick braid running from the hairline over the crown and on down the back, sides drawn up tight."}

TOP = [(0, -8.75, -3.9), (0, -9.4, -1.6), (0, -9.4, 1.0), (0, -8.6, 3.3), (0, -6.9, 4.85), (0, -4.6, 5.3)]


def build(g):
    scalp(g, 8901, side_rows=8, back_rows=8, sideburn=0)
    swept_sides(g)
    head = g.part("head")
    for face in (head.right, head.left):   # drawn up toward the braid
        combed(face, (1, 3, 5), rows=range(0, 3))
    combed(head.back, (1, 2, 5, 6))
    ring_shell(g, 8902, side_rows=2, back_rows=4)
    plait_along(g, "top_braid", TOP, w=3, d=2, spacing=1.8, seed=8910)
    braid(g, "tail_braid", (0, -3.6, 5.25), (-4, 0, 0), count=6, w=2, d=2, seed=8930, tie_role="L")
    for side, sign in SIDES:
        strand(g, f"{side}_wisp", (4.3 * sign, -7.4, -3.6), (0, 0, -6 * sign), ((1, 3), (1, 1, .4 * sign)), 1, 8950 + (sign > 0),
               ring=None, texture="wave")
