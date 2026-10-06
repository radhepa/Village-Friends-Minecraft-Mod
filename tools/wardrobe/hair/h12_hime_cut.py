"""Hime Cut: blunt brow-length bangs, straight cheek-length sidelocks and long straight hair behind."""
from anime import cel_box, ring_shell
from paint import scalp

META = {"name": "Hime Cut", "gender": "male", "description": "Blunt bangs, straight cheek-length sidelocks and long sleek hair down the back."}


def build(g):
    scalp(g, 1201, side_rows=7, back_rows=8, sideburn=0)
    ring_shell(g, 1202, side_rows=7, back_rows=8)
    fringe = g.piece("blunt_fringe", "HEAD", (-4.5, 0, -1), (9, 3, 1), pivot=(0, -8.6, -4.3))
    cel_box(fringe, 1210, ring=0)
    for side, sign in (("right", -1), ("left", 1)):
        lock = g.piece(f"{side}_sidelock", "HEAD", (-1, 0, -.5), (2, 7, 1), pivot=(4.2 * sign, -7.6, -3.4))
        cel_box(lock, 1220 + (sign > 0), ring=1)
        panel = g.piece(f"{side}_curtain", "HEAD", (-.5, 0, -2.5), (1, 8, 5), pivot=(4.4 * sign, -7.8, 1.2))
        cel_box(panel, 1230 + (sign > 0), ring=1)
    for i, x in enumerate((-3.0, 0, 3.0)):
        back = g.piece(f"back_{i}", "HEAD", (-1.5, 0, 0), (3, 14, 1), pivot=(x, -7.8, 4.2), rotation=(4, 0, 0), motion="sway")
        cel_box(back, 1240 + i, ring=1)
