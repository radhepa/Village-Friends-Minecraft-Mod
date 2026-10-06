"""Milkmaid Braids: two plaits rising from the nape behind each ear and pinned across the crown, one behind the other."""
from anime import ring_shell
from anime_female import combed, plait_along, strand, swept_sides, SIDES
from paint import scalp

META = {"name": "Milkmaid Braids", "gender": "female",
        "description": "Two plaits brought up from the nape and pinned across the crown, with soft wisps at the temples."}

# Each plait climbs its own side of the head from the nape, crosses the crown and tucks in above the far ear.
FRONT = [(-1.5, -.6, 5.1), (-3.8, -2.6, 4.6), (-5.15, -5.2, 2.6), (-5.15, -7.7, .1), (-3.0, -9.35, -1.0), (0, -9.7, -1.2),
         (3.0, -9.35, -1.1), (4.9, -7.9, -.8), (5.15, -6.3, -.5)]
BACK = [(1.5, -.6, 5.1), (3.8, -2.6, 4.6), (5.15, -5.4, 3.0), (5.0, -7.9, 2.6), (2.8, -9.4, 1.9), (0, -9.7, 1.7),
        (-2.8, -9.4, 1.8), (-4.7, -8.3, 1.9)]


def build(g):
    scalp(g, 6701, side_rows=8, back_rows=8, sideburn=0, part=3)
    swept_sides(g)
    head = g.part("head")
    combed(head.back, (1, 2, 5, 6))
    hat = ring_shell(g, 6702, side_rows=2, back_rows=5)
    hat.top.vline(3, 0, 7, "H1")
    plait_along(g, "front_plait", FRONT, spacing=1.95, seed=6710)
    plait_along(g, "back_plait", BACK, spacing=1.95, seed=6740, base=2)
    for side, sign in SIDES:
        strand(g, f"{side}_wisp", (4.3 * sign, -7.4, -3.6), (0, 0, -3 * sign), ((1, 4), (1, 3, .4 * sign), (1, 1)), 1,
               6780 + (sign > 0), texture="wave")
    strand(g, "fore_wisp", (-1.6, -8.6, -4.35), (-8, 0, 14), ((2, 2), (1, 1)), 1, 6785, ring=0)
