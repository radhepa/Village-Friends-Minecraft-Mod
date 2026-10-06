"""Voluminous Curls: a big, full cloud of soft curls past the shoulders, widest at the jaw, with a curly fringe."""
from anime import ring_shell
from anime_female import bubble_face, fall, paint, SIDES
from paint import scalp

META = {"name": "Voluminous Curls", "gender": "female",
        "description": "A big, full head of soft curls past the shoulders, widest at the jaw, with a curly fringe."}

CURL = ((3, 4, 0, 2), (3, 4, .5, 2), (2, 3, -.4, 2))


def build(g):
    scalp(g, 7701, side_rows=8, back_rows=8, sideburn=0, part=5)
    hat = ring_shell(g, 7702, side_rows=8, back_rows=8)
    bubble_face(hat.top, 7703, 3)
    # Crown volume: overlapping rounded masses that lift the silhouette without one helmet-like shell.
    for i, (x, y, z, rx, rz, size) in enumerate(((-2.4, -8.6, -1.8, -10, 16, (4, 2, 4)), (2.2, -8.8, -1.4, -8, -18, (4, 2, 4)),
                                                 (0, -8.9, 1.6, 10, 0, (5, 2, 4)), (-3.6, -7.2, 2.6, 0, 40, (3, 3, 4)),
                                                 (3.6, -7.2, 2.6, 0, -40, (3, 3, 4)))):
        w, h, d = size
        mass = g.piece(f"crown_{i}", "HEAD", (-w / 2, -h / 2, -d / 2), size, pivot=(x, y, z), rotation=(rx, 0, rz))
        paint(mass, "bubble", 7705 + i * 3, 2, top_delta=1)
    fall(g, "fringe", [(-2.4, -8.6, -4.4, ((3, 2, 0, 1),), -10, 12), (0, -8.7, -4.5, ((3, 2, 0, 1),), -12, -2),
                       (2.4, -8.6, -4.4, ((3, 2, 0, 1),), -10, -14)], 7720, texture="bubble", ring=None)
    for side, sign in SIDES:
        fall(g, f"{side}_mass", [(4.8 * sign, -7.0, -3.0, CURL, 0, -12 * sign), (5.0 * sign, -7.2, -.4, CURL[:2], 0, -18 * sign),
                                 (4.6 * sign, -7.0, 3.0, CURL, 4, -14 * sign)], 7730 + (sign > 0) * 20, texture="bubble",
             motion="sway")
    fall(g, "back", [(-2.4, -7.2, 4.6, CURL, 4, 12), (0, -7.4, 5.1, CURL, 6, 0), (2.4, -7.2, 4.6, CURL, 4, -12)], 7780,
         texture="bubble", motion="sway")
