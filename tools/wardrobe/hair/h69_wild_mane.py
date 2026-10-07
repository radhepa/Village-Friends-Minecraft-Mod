"""Wild Mane: a big, untamed mass of long hair springing out from the crown and falling past the
shoulders in thick locks at every angle, a rough fringe above the brow."""
from anime import ring_shell
from anime_male import SIDES, clump, taper
from paint import scalp

META = {"name": "Wild Mane", "gender": "male",
        "description": "A big untamed mass of long hair springing out at every angle, past the shoulders."}


def build(g):
    scalp(g, 6901, side_rows=8, back_rows=8, sideburn=1)
    ring_shell(g, 6902, side_rows=7, back_rows=8)
    for i, (x, z, rx, rz) in enumerate(((-2.2, -1.6, 18, 24), (1.8, -2.0, 14, -20), (-1.6, 1.8, -20, 18), (2.0, 1.4, -16, -26))):
        clump(g, f"crown_{i}", (x, -8.2, z), (3, 2, 3), rotation=(rx, 0, rz), origin=(-1.5, -2, -1.5), seed=6910 + i, top_delta=2)
    for i, (x, rz) in enumerate(((-2.5, 18), (-.2, -6), (2.2, -22))):
        taper(g, f"fringe_{i}", (x, -8.8, -4.25), (-26, 0, rz), ((2, 2, 1), (1, 1, 1)), seed=6920 + i * 3, ring=0)
    # Thick locks springing out at the sides.
    for side, sign in SIDES:
        locks = (((4.55, -7.8, -3.0), -10, 10, ((2, 7, 2), (2, 3, 2), (1, 2, 1))),
                 ((4.3, -8.0, -.4), 0, 24, ((3, 4, 2), (1, 2, 1))),
                 ((4.3, -7.6, 2.9), 10, 18, ((3, 8, 2), (2, 3, 2), (1, 2, 1))))
        for j, ((x, y, z), rx, flare, segs) in enumerate(locks):
            taper(g, f"{side}_lock_{j}", (x * sign, y, z), (rx, 0, -flare * sign), segs, seed=6930 + j * 5 + (sign > 0) * 17, ring=1)
    for i, (x, rz, rx) in enumerate(((-3.0, 18, 16), (-.9, 6, 24), (1.1, -8, 20), (3.0, -20, 14))):
        taper(g, f"back_{i}", (x, -7.6, 4.4), (rx, 0, rz), ((3, 9, 2), (2, 3, 1)), seed=6970 + i * 5, ring=1)
