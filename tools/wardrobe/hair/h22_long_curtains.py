"""Long Curtains: centre-parted bangs that sweep out and fall past the jaw, a pointed nape."""
from anime import back_fan, lock, ring_shell
from paint import scalp

META = {"name": "Long Curtains", "description": "Centre-parted curtain bangs falling past the jaw on both sides."}


def build(g):
    scalp(g, 2201, side_rows=6, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 2202, side_rows=6, back_rows=8)
    hat.top.vline(3, 0, 7, "H1")
    for side, sign in (("right", -1), ("left", 1)):
        lock(g, f"{side}_curtain", (.3 * sign, -8.75, -4.35), (-6, 0, 58 * -sign), ((2, 4), (1, 1)), 1, 2210 + (sign > 0), ring=None)
        lock(g, f"{side}_fall", (4.1 * sign, -7.8, -3.4), (0, 0, -3 * sign), ((2, 7), (1, 2)), 1, 2215 + (sign > 0))
        lock(g, f"{side}_side", (4.3 * sign, -7.8, -.2), (0, 0, -6 * sign), ((1, 6), (1, 1)), 3, 2218 + (sign > 0))
    back_fan(g, "nape", [(-3.0, ((2, 6), (1, 2)), 6, 6), (-1.0, ((3, 7), (1, 2)), 2, 5), (1.0, ((3, 7), (1, 2)), -2, 5), (3.0, ((2, 6), (1, 2)), -6, 6)],
             2230)
