"""Twin Braids: parted down the middle into two plaits that start behind the ears and hang forward on the chest."""
from anime import ring_shell
from anime_female import fall, finish, plait_path, points, strand, SIDES
from paint import scalp

META = {"name": "Twin Braids", "gender": "female",
        "description": "Two neat plaits from behind the ears, worn forward over the shoulders and tied with ribbon."}


def build(g):
    scalp(g, 6301, side_rows=7, back_rows=8, sideburn=0, part=3)
    head = g.part("head")
    head.back.vline(3, 0, 7, "H0"), head.back.vline(4, 0, 7, "H1")
    hat = ring_shell(g, 6302, side_rows=6, back_rows=7)
    hat.top.vline(3, 0, 7, "H1"), hat.back.vline(3, 0, 6, "H1")
    points(g, "bang", [(-2.4, 3, 2, 2, 6), (0, 3, 2, 2, 0), (2.4, 3, 2, 2, -6)], 6310)
    for side, sign in SIDES:
        strand(g, f"{side}_side", (4.45 * sign, -7.8, .6), (0, 0, -2 * sign), ((1, 5),), 5, 6320 + (sign > 0))
        pivot = (4.5 * sign, -3.6, .4)
        angles = [(-62, -15 * sign), (-50, -8 * sign), (-25, -2 * sign), (-10, 3 * sign), (-6, 4 * sign), (-4, 3 * sign), (-3, 2 * sign)]
        boxes, end, rot, w = plait_path(g, f"{side}_braid", pivot, angles, seed=6330 + (sign > 0) * 20)
        finish(g, f"{side}_braid", pivot, end, rot, w, 2, "A", ((2, 2), (1, 1)), seed=6340 + (sign > 0) * 20)
    fall(g, "nape", [(-1.9, -7.5, 4.4, ((3, 5), (2, 1)), 2, 24), (1.9, -7.5, 4.4, ((3, 5), (2, 1)), 2, -24)], 6380)
