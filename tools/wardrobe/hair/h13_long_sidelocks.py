"""Long Sidelocks: centre-parted bangs, chest-length pointed sidelocks and hair flowing down the back."""
from anime import back_fan, bangs, ring_shell, sidelocks
from paint import scalp

META = {"name": "Long Sidelocks", "gender": "male", "description": "Centre-parted bangs, long pointed sidelocks and flowing waist-length hair."}


def build(g):
    scalp(g, 1301, side_rows=7, back_rows=8, sideburn=0, part=3)
    hat = ring_shell(g, 1302, side_rows=7, back_rows=8)
    hat.top.vline(3, 0, 7, "H1")
    bangs(g, "bang", [(-1.5, ((3, 2), (2, 1)), 22), (1.5, ((3, 2), (2, 1)), -22), (-3.9, ((2, 3), (1, 2)), 10), (3.9, ((2, 3), (1, 2)), -10)], 1310)
    sidelocks(g, "sidelock", 11, 1320, flare=3)
    back_fan(g, "mane", [(-3.0, ((3, 12), (2, 2), (1, 1)), 4, 5), (0, ((3, 13), (2, 2), (1, 1)), 0, 4), (3.0, ((3, 12), (2, 2), (1, 1)), -4, 5)],
             1330, motion="sway")
